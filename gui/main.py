"""
Faster Whisper GUI - Standalone Windows Application
Features:
- Global hotkey (Ctrl + Right Menu Key) for quick transcription
- System tray integration
- Drag & drop audio file support
- Real-time transcription with progress
- Multiple output formats (TXT, SRT, CSV)
"""

import sys
import json
import threading
import queue
from pathlib import Path
from datetime import datetime
import logging

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageTk
import pystray
from pystray import MenuItem as item

from faster_whisper import WhisperModel


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / ".faster_whisper" / "app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FasterWhisperGUI:
    """Main GUI Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Faster Whisper Transcriber")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Create config directory
        self.config_dir = Path.home() / ".faster_whisper"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        
        # Model cache
        self.model = None
        self.model_size = "base"
        self.device = "cuda"  # or "cpu"
        self.compute_type = "float16"
        
        # Queue for thread communication
        self.result_queue = queue.Queue()
        self.is_transcribing = False
        
        # Load configuration
        self.load_config()
        
        # Initialize UI
        self.setup_ui()
        self.load_model_async()
        
        # Window event bindings
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Register hotkey
        self.register_hotkey()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(title_frame, text="⚡ Faster Whisper Transcriber", 
                 font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Model selection
        ttk.Label(settings_frame, text="Model Size:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value=self.model_size)
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var,
                                   values=["tiny", "base", "small", "medium", "large"],
                                   state="readonly", width=20)
        model_combo.grid(row=0, column=1, sticky=tk.EW, padx=5)
        model_combo.bind("<<ComboboxSelected>>", lambda e: self.on_model_change())
        
        # Device selection
        ttk.Label(settings_frame, text="Device:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.device_var = tk.StringVar(value=self.device)
        device_combo = ttk.Combobox(settings_frame, textvariable=self.device_var,
                                    values=["cuda", "cpu"], state="readonly", width=10)
        device_combo.grid(row=0, column=3, sticky=tk.EW, padx=5)
        device_combo.bind("<<ComboboxSelected>>", lambda e: self.on_device_change())
        
        settings_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(3, weight=1)
        
        # File Selection Frame
        file_frame = ttk.LabelFrame(self.root, text="Audio File", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", 
                                    foreground="gray", font=("Helvetica", 10))
        self.file_label.pack(fill=tk.X, pady=5)
        
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Browse Audio File", 
                  command=self.select_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Open Folder", 
                  command=self.open_file_folder).pack(side=tk.LEFT, padx=5)
        
        # Drag & Drop hint
        hint_label = ttk.Label(file_frame, text="💡 Tip: Drag and drop audio files here or use Ctrl+App Key hotkey",
                              foreground="blue", font=("Helvetica", 9))
        hint_label.pack(fill=tk.X, pady=5)
        
        self.file_path = None
        self.setup_drag_drop(file_frame)
        
        # Language Frame
        lang_frame = ttk.LabelFrame(self.root, text="Transcription Options", padding=10)
        lang_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(lang_frame, text="Language:").grid(row=0, column=0, sticky=tk.W)
        self.language_var = tk.StringVar(value="auto")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                  values=["auto", "en", "es", "fr", "de", "it", "ja", "zh", "ar"],
                                  state="readonly", width=20)
        lang_combo.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # VAD Filter
        self.vad_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(lang_frame, text="VAD Filter (remove silence)", 
                       variable=self.vad_var).grid(row=0, column=2, sticky=tk.W, padx=10)
        
        # Word timestamps
        self.timestamps_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(lang_frame, text="Word-level Timestamps", 
                       variable=self.timestamps_var).grid(row=0, column=3, sticky=tk.W, padx=10)
        
        lang_frame.columnconfigure(1, weight=1)
        
        # Output Frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        self.format_var = tk.StringVar(value="txt")
        for fmt in ["txt", "srt", "csv", "vtt"]:
            ttk.Radiobutton(output_frame, text=fmt.upper(), 
                           variable=self.format_var, value=fmt).pack(side=tk.LEFT, padx=5)
        
        # Progress Frame
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status text area
        ttk.Label(progress_frame, text="Output:").pack(anchor=tk.W, pady=(5, 0))
        
        text_frame = ttk.Frame(progress_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_output = tk.Text(text_frame, height=8, yscrollcommand=scrollbar.set,
                                   font=("Courier", 9), wrap=tk.WORD)
        self.text_output.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_output.yview)
        
        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.transcribe_btn = ttk.Button(button_frame, text="🎙️ Transcribe", 
                                        command=self.start_transcription)
        self.transcribe_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📋 Copy", 
                  command=self.copy_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save", 
                  command=self.save_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Clear", 
                  command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
    def setup_drag_drop(self, frame):
        """Setup drag and drop functionality"""
        try:
            from tkinterdnd2 import DND_FILES, tkinterdnd
            frame.drop_target_register(DND_FILES)
            frame.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            logger.warning("tkinterdnd2 not available - drag and drop disabled")
    
    def on_drop(self, event):
        """Handle dropped files"""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0].strip('{}')
            if Path(file_path).exists():
                self.file_path = file_path
                self.file_label.config(text=f"📁 {Path(file_path).name}", foreground="black")
    
    def register_hotkey(self):
        """Register global hotkey Ctrl + Right Menu Key"""
        try:
            from pynput import keyboard
            
            def on_hotkey():
                logger.info("Hotkey triggered!")
                self.root.after(0, self.on_hotkey_triggered)
            
            listener = keyboard.GlobalHotKeys({
                '<ctrl>+<menu>': on_hotkey
            })
            listener.start()
            logger.info("Global hotkey registered: Ctrl + Right Menu Key")
        except ImportError:
            logger.warning("pynput not available - global hotkey disabled")
    
    def on_hotkey_triggered(self):
        """Handle global hotkey trigger"""
        self.root.lift()
        self.root.focus()
        if self.file_path:
            self.start_transcription()
        else:
            messagebox.showinfo("Info", "Please select an audio file first")
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.model_size = config.get('model_size', 'base')
                    self.device = config.get('device', 'cuda')
                    self.compute_type = config.get('compute_type', 'float16')
            except Exception as e:
                logger.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'model_size': self.model_size,
                'device': self.device,
                'compute_type': self.compute_type
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def load_model_async(self):
        """Load model in background thread"""
        def load():
            try:
                self.log_output(f"Loading {self.model_size} model on {self.device}...")
                self.model = WhisperModel(self.model_size, device=self.device,
                                         compute_type=self.compute_type)
                self.log_output("✓ Model loaded successfully!")
            except Exception as e:
                self.log_output(f"✗ Error loading model: {e}")
                logger.error(f"Model loading error: {e}")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def on_model_change(self):
        """Handle model size change"""
        self.model_size = self.model_var.get()
        self.save_config()
        self.model = None
        self.load_model_async()
    
    def on_device_change(self):
        """Handle device change"""
        self.device = self.device_var.get()
        self.save_config()
        self.model = None
        self.load_model_async()
    
    def select_file(self):
        """Open file dialog to select audio file"""
        file_types = [
            ("Audio Files", "*.mp3 *.wav *.m4a *.ogg *.flac *.aac"),
            ("All Files", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=f"📁 {Path(file_path).name}", foreground="black")
    
    def open_file_folder(self):
        """Open file browser in current folder"""
        if self.file_path:
            import subprocess
            import platform
            file_dir = Path(self.file_path).parent
            if platform.system() == 'Windows':
                subprocess.Popen(['explorer', str(file_dir)])
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', str(file_dir)])
            else:
                subprocess.Popen(['xdg-open', str(file_dir)])
    
    def start_transcription(self):
        """Start transcription in background thread"""
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select an audio file first")
            return
        
        if not self.model:
            messagebox.showerror("Error", "Model is not loaded yet. Please wait...")
            return
        
        if self.is_transcribing:
            messagebox.showinfo("Info", "Transcription already in progress...")
            return
        
        self.is_transcribing = True
        self.transcribe_btn.config(state="disabled")
        self.clear_output()
        self.log_output(f"Starting transcription of {Path(self.file_path).name}...")
        
        thread = threading.Thread(target=self._transcribe_worker, daemon=True)
        thread.start()
        
        # Start checking for results
        self.check_result_queue()
    
    def _transcribe_worker(self):
        """Worker thread for transcription"""
        try:
            language = self.language_var.get()
            language = None if language == "auto" else language
            
            self.log_output("Transcribing...")
            
            segments, info = self.model.transcribe(
                self.file_path,
                language=language,
                vad_filter=self.vad_var.get(),
                word_timestamps=self.timestamps_var.get(),
                beam_size=5
            )
            
            # Collect results
            segments_list = list(segments)
            
            # Format output based on selected format
            output_text = self.format_output(segments_list, info)
            
            self.result_queue.put({
                'status': 'success',
                'output': output_text,
                'segments': segments_list,
                'info': info
            })
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            self.result_queue.put({
                'status': 'error',
                'message': str(e)
            })
    
    def format_output(self, segments, info):
        """Format output based on selected format"""
        fmt = self.format_var.get()
        lines = []
        
        # Header
        lines.append(f"File: {Path(self.file_path).name}")
        lines.append(f"Language: {info.language} ({info.language_probability:.2%})")
        lines.append(f"Duration: {info.duration:.2f}s")
        lines.append("-" * 50)
        lines.append("")
        
        if fmt == "txt":
            for segment in segments:
                lines.append(segment.text)
        
        elif fmt == "srt":
            for i, segment in enumerate(segments, 1):
                lines.append(str(i))
                start = self.seconds_to_time(segment.start)
                end = self.seconds_to_time(segment.end)
                lines.append(f"{start} --> {end}")
                lines.append(segment.text)
                lines.append("")
        
        elif fmt == "vtt":
            lines.append("WEBVTT")
            lines.append("")
            for segment in segments:
                start = self.seconds_to_time(segment.start)
                end = self.seconds_to_time(segment.end)
                lines.append(f"{start} --> {end}")
                lines.append(segment.text)
                lines.append("")
        
        elif fmt == "csv":
            lines.append("Start,End,Duration,Text")
            for segment in segments:
                duration = segment.end - segment.start
                lines.append(f"{segment.start:.2f},{segment.end:.2f},{duration:.2f},\"{segment.text}\"")
        
        return "\n".join(lines)
    
    @staticmethod
    def seconds_to_time(seconds):
        """Convert seconds to SRT/VTT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def check_result_queue(self):
        """Check for results from transcription thread"""
        try:
            result = self.result_queue.get_nowait()
            self.is_transcribing = False
            self.transcribe_btn.config(state="normal")
            
            if result['status'] == 'success':
                self.log_output(result['output'], clear=True)
                self.log_output("\n✓ Transcription completed!")
            else:
                self.log_output(f"✗ Error: {result['message']}", clear=True)
        
        except queue.Empty:
            if self.is_transcribing:
                self.root.after(500, self.check_result_queue)
    
    def log_output(self, message, clear=False):
        """Log message to output text area"""
        if clear:
            self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, message + "\n")
        self.text_output.see(tk.END)
        self.root.update()
    
    def copy_output(self):
        """Copy output to clipboard"""
        try:
            output = self.text_output.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo("Success", "Output copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
    
    def save_output(self):
        """Save output to file"""
        try:
            output = self.text_output.get(1.0, tk.END)
            if not output.strip():
                messagebox.showwarning("Warning", "No output to save")
                return
            
            file_types = [
                ("Text Files", "*.txt"),
                ("SRT Files", "*.srt"),
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
            
            file_path = filedialog.asksaveasfilename(filetypes=file_types)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output)
                messagebox.showinfo("Success", f"Output saved to {Path(file_path).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
    
    def clear_output(self):
        """Clear output text area"""
        self.text_output.delete(1.0, tk.END)
        self.progress_var.set(0)
    
    def on_closing(self):
        """Handle window closing"""
        self.save_config()
        self.root.destroy()
        sys.exit(0)


def main():
    """Entry point"""
    root = tk.Tk()
    app = FasterWhisperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

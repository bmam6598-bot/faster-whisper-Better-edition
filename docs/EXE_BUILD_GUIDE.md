# Faster Whisper - Windows GUI Application Build & Usage Guide

## Features

✨ **Standalone Application** - No Python installation required  
🎙️ **Global Hotkey** - Press `Ctrl + Right Menu Key` (App key) to start transcription  
🎯 **Drag & Drop** - Drop audio files directly into the app  
⚡ **Fast Transcription** - Uses optimized CTranslate2 backend  
🌍 **Multilingual** - Support for 99+ languages  
📁 **Multiple Formats** - Export as TXT, SRT, CSV, or VTT  
💾 **GPU/CPU** - Automatic device selection (CUDA/CPU)  
🔧 **Configurable** - Model size, language, and options  

## Prerequisites

### System Requirements
- **Windows 10/11** (64-bit)
- **8GB RAM minimum** (16GB recommended for large models)
- **5GB disk space** for model weights
- **Optional: NVIDIA GPU** with CUDA 12 support (much faster)

### Build Prerequisites (for creating EXE)
- Python 3.9 or higher
- pip package manager

## Installation

### Option 1: Download Pre-built EXE (Recommended)
Coming soon! Download from releases page.

### Option 2: Build from Source

#### Step 1: Install Python
Download and install Python 3.10+ from [python.org](https://python.org)  
✓ **Check "Add Python to PATH"** during installation

#### Step 2: Clone Repository
```bash
git clone https://github.com/bmam6598-bot/faster-whisper-Better-edition.git
cd faster-whisper-Better-edition
```

#### Step 3: Install Dependencies
```bash
# Install basic requirements
pip install -r requirements.txt

# Install GUI dependencies
pip install -r requirements.gui.txt

# Install PyInstaller for building EXE
pip install pyinstaller>=6.0.0
```

#### Step 4: (Optional) Install CUDA for GPU Support
For NVIDIA GPUs (much faster transcription):

```bash
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*
```

#### Step 5: Build EXE
```bash
python build_exe.py
```

The process takes 5-10 minutes. When complete:
- ✓ EXE will be at: `dist/FasterWhisper.exe`
- ✓ Single file, no dependencies needed to run

## Usage

### Running the Application

**Option A: Direct Launch**
- Double-click `FasterWhisper.exe`
- Select an audio file
- Click "Transcribe"

**Option B: Global Hotkey**
- Press `Ctrl + Right Menu Key` (Ctrl + App Key)
- First time: select audio file
- After that: hotkey triggers transcription immediately

**Option C: Drag & Drop**
- Drag audio files onto the window
- Click "Transcribe" or use hotkey

### Supported Audio Formats
- MP3
- WAV
- M4A / AAC
- OGG
- FLAC
- And more (via FFmpeg)

### Settings Explained

| Setting | Options | Impact |
|---------|---------|--------|
| **Model Size** | tiny, base, small, medium, large | Larger = more accurate but slower |
| **Device** | CUDA, CPU | CUDA (GPU) is 5-10x faster if available |
| **Language** | auto, en, es, fr, ... | Leave as "auto" for auto-detection |
| **VAD Filter** | On/Off | Remove silent parts (recommended) |
| **Word Timestamps** | On/Off | Get timestamp for each word (slower) |
| **Output Format** | TXT, SRT, CSV, VTT | Choose your export format |

## Hotkey Setup

The application uses `Ctrl + Right Menu Key` as the global hotkey.

**Right Menu Key location:**
- Standard keyboard: Right side, between **Right Windows Key** and **Right Ctrl Key**
- Laptops: May be available via fn key combination
- Alternative: You can modify the hotkey in `gui/main.py` line ~170

### Custom Hotkey (Optional)

Edit `gui/main.py` and find the `register_hotkey()` method:

```python
listener = keyboard.GlobalHotKeys({
    '<ctrl>+<menu>': on_hotkey  # Change this
})
```

Common hotkey combinations:
- `'<ctrl>+<alt>+<shift>+<w>'` - Ctrl + Alt + Shift + W
- `'<ctrl>+<shift>+<t>'` - Ctrl + Shift + T
- `'<alt>+<f12>'` - Alt + F12

## Advanced Configuration

### Model Download
Models are automatically downloaded on first use (~1-2 GB per model).

**Cache location:** `C:\Users\YourUser\.faster_whisper\`

### Manual Model Download
```bash
# Download model in advance
python -c "from faster_whisper import WhisperModel; WhisperModel('large')"
```

### Configuration File
Settings saved in: `C:\Users\YourUser\.faster_whisper\config.json`

```json
{
  "model_size": "base",
  "device": "cuda",
  "compute_type": "float16"
}
```

## Troubleshooting

### EXE won't start
- ✓ Ensure Python 3.9+ is installed
- ✓ Check Windows Defender/Antivirus isn't blocking it
- ✓ Try running from Command Prompt: `FasterWhisper.exe`

### "Model not loaded" error
- ✓ Internet connection required for first run (model download)
- ✓ Check disk space (5+ GB free)
- ✓ Check `C:\Users\YourUser\.faster_whisper\app.log` for details

### Very slow transcription
- ✓ Using CPU? Reduce model size to "tiny" or "base"
- ✓ No CUDA? Install NVIDIA GPU drivers
- ✓ Check CPU usage in Task Manager

### Audio file not supported
- ✓ Try converting to WAV or MP3
- ✓ Use [FFmpeg](https://ffmpeg.org/download.html) to convert:
  ```bash
  ffmpeg -i input.m4a output.wav
  ```

### Hotkey not working
- ✓ Some apps capture global hotkeys (Discord, games, etc.)
- ✓ Try different hotkey combination in `gui/main.py`
- ✓ Check app.log for errors

### GPU not detected
- ✓ Install NVIDIA CUDA Toolkit 12+
- ✓ Install cuDNN 9
- ✓ Install NVIDIA drivers (latest)
- ✓ Fallback: Change device to "CPU" in settings

## Performance Tips

### For Fast Transcription
1. Use "CUDA" device (GPU)
2. Use "base" or "small" model
3. Enable "VAD Filter" (removes silence)
4. Disable "Word Timestamps"

### For High Accuracy
1. Use "large" model
2. Use "float16" compute type
3. Disable "VAD Filter"
4. Enable "Word Timestamps"

### For Low Resource Usage
1. Use "CPU" device
2. Use "tiny" model
3. Enable "VAD Filter"

## Creating Shortcuts

### Desktop Shortcut
1. Right-click `FasterWhisper.exe`
2. Send to → Desktop (create shortcut)
3. Right-click shortcut → Properties
4. Add custom icon: `gui/assets/icon.ico`

### Add to Startup
1. Press `Win + R`, type: `shell:startup`
2. Copy `FasterWhisper.exe` or shortcut here
3. App launches with Windows

### Windows Context Menu (Optional)
Create `transcribe.bat`:
```batch
@echo off
start "" "%~dp0FasterWhisper.exe"
```

## System Tray (Future Feature)

When running, app minimizes to system tray. Click tray icon to restore.

## Updating

### Check for Updates
1. Close the application
2. Re-run the build script:
   ```bash
   python build_exe.py
   ```
3. New models auto-download on first use

## Uninstall

Simply delete `FasterWhisper.exe` and the folder `C:\Users\YourUser\.faster_whisper\`

## Support

### Reporting Issues
Visit: [GitHub Issues](https://github.com/bmam6598-bot/faster-whisper-Better-edition/issues)

### Logs Location
- **Application logs:** `C:\Users\YourUser\.faster_whisper\app.log`
- **Include this when reporting issues**

## FAQ

**Q: Is my audio data sent anywhere?**  
A: No! Everything runs locally on your computer. No internet connection needed after first setup.

**Q: Can I use this commercially?**  
A: Yes, it's MIT licensed. See LICENSE file.

**Q: Why is first transcription slow?**  
A: Models need to be downloaded (~1-2 GB). Subsequent runs are much faster.

**Q: Can I transcribe livestreams?**  
A: Not directly, but you can record first then transcribe.

**Q: Multiple languages in one file?**  
A: Set language to "auto" for best results. Or set specific language if known.

## Development

### Modifying the App
1. Edit `gui/main.py`
2. Test with: `python gui/main.py`
3. Rebuild: `python build_exe.py`

### Building Portable Version
The current build is already portable! Copy `FasterWhisper.exe` to any Windows machine.

## License

MIT License - See LICENSE file

---

**Made with ❤️ using Faster Whisper**

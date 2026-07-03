"""
Build script to create Windows EXE using PyInstaller

Usage:
    python build_exe.py

This creates a standalone EXE in the dist/ folder that doesn't require Python installation.
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_exe():
    """Build standalone Windows EXE"""
    
    # Get project root
    project_root = Path(__file__).parent
    gui_main = project_root / "gui" / "main.py"
    
    if not gui_main.exists():
        print(f"Error: {gui_main} not found!")
        sys.exit(1)
    
    # PyInstaller arguments
    args = [
        str(gui_main),
        '--name=FasterWhisper',
        '--onefile',  # Single EXE file
        '--windowed',  # No console window
        '--add-data=faster_whisper:faster_whisper',  # Include faster_whisper package
        '--hidden-import=faster_whisper',
        '--hidden-import=ctranslate2',
        '--hidden-import=pyaudio',
        '--hidden-import=tkinter',
        '--hidden-import=pynput',
        '--hidden-import=pystray',
        '--hidden-import=PIL',
        f'--distpath={project_root / "dist"}',
        f'--buildpath={project_root / "build"}',
        f'--specpath={project_root}',
        '--clean',
        '--noconfirm',
    ]
    
    print("Building standalone Windows EXE...")
    print("This may take several minutes...\n")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ Build completed successfully!")
        exe_path = project_root / "dist" / "FasterWhisper.exe"
        if exe_path.exists():
            print(f"✓ EXE created at: {exe_path}")
            print("\nYou can now:")
            print("1. Add the EXE to Windows startup folder")
            print("2. Create a shortcut on your desktop")
            print("3. Use Ctrl + Right Menu Key as global hotkey")
    except Exception as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()

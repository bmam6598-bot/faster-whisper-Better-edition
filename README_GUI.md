# Faster Whisper - Windows GUI Application

A standalone Windows application for fast, local speech-to-text transcription powered by OpenAI's Whisper and CTranslate2.

## 🚀 Quick Start

### Download & Run
1. Download `FasterWhisper.exe` from [Releases](../../releases)
2. Double-click to run
3. Select audio file → Click Transcribe

### Global Hotkey
- Press `Ctrl + Right Menu Key` (Ctrl + App Key) to start transcribing
- First time: select audio file
- After that: instant transcription

## ✨ Key Features

| Feature | Details |
|---------|----------|
| 🎤 **Speech-to-Text** | Fast, accurate transcription with Whisper |
| ⚡ **GPU Support** | 5-10x faster with NVIDIA CUDA |
| 🌍 **99+ Languages** | Auto-detect or select specific language |
| 🎯 **Global Hotkey** | Ctrl + App Key for quick access |
| 📤 **Drag & Drop** | Drop audio files directly onto app |
| 💾 **Multiple Formats** | Export as TXT, SRT, CSV, or VTT |
| 📋 **Copy/Share** | Copy transcription to clipboard |
| 🔧 **Customizable** | Model size, language, voice activity detection |
| 🕐 **Timestamps** | Word-level or segment-level timing |
| 🔕 **Silent Processing** | No external API calls - everything local |

## 📦 Build from Source

### Prerequisites
- Windows 10/11 (64-bit)
- Python 3.9+ 
- pip
- 8GB+ RAM
- Optional: NVIDIA GPU for faster transcription

### Build Steps

```bash
# 1. Clone repository
git clone https://github.com/bmam6598-bot/faster-whisper-Better-edition.git
cd faster-whisper-Better-edition

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements.gui.txt
pip install pyinstaller

# 3. (Optional) GPU support with CUDA
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*

# 4. Build EXE
python build_exe.py
```

**Result:** `dist/FasterWhisper.exe` (standalone, no dependencies needed)

## 📖 Full Documentation

See [EXE_BUILD_GUIDE.md](docs/EXE_BUILD_GUIDE.md) for:
- Complete installation instructions
- Configuration and customization
- Hotkey setup and shortcuts
- Troubleshooting
- Performance optimization tips
- Development guide

## 🎯 Usage Examples

### Example 1: Basic Transcription
```
1. Launch FasterWhisper.exe
2. Click "Browse Audio File"
3. Select your audio file
4. Click "Transcribe"
5. Wait for results (progress shown)
6. Click "Copy" to copy to clipboard
```

### Example 2: Using Hotkey
```
1. Have audio file ready
2. Load it once in the app (Ctrl + App Key)
3. After that, just press Ctrl + App Key to transcribe
4. Results appear in real-time
```

### Example 3: Batch Export
```
1. Transcribe audio
2. Change output format (TXT → SRT)
3. Click "Save"
4. Choose format and location
5. Repeat for multiple formats
```

## ⚙️ Settings

**Model Size**
- `tiny` - Fastest, less accurate (~40MB)
- `base` - Fast & accurate (~140MB) ⭐ Recommended
- `small` - Better accuracy (~240MB)
- `medium` - High accuracy, slower (~769MB)
- `large` - Best accuracy, slowest (~2.9GB)

**Device**
- `cuda` - NVIDIA GPU (5-10x faster) 🚀
- `cpu` - CPU only (slower but works everywhere)

**Options**
- VAD Filter: Remove silent parts (faster, recommended)
- Word Timestamps: Get timing for each word (slower)
- Auto Language: Auto-detect or select specific language

## 🎹 Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl + Right Menu Key` | Start/Stop transcription |
| `Ctrl + C` (in app) | Copy output |
| `Escape` | Close/Minimize |

**Right Menu Key** = Key between Windows Key and Ctrl Key on right side of keyboard

## 📊 Performance

| Model | Device | Speed | Quality | RAM Used |
|-------|--------|-------|---------|----------|
| tiny | GPU | ⚡⚡⚡ | Fair | 1GB |
| base | GPU | ⚡⚡ | Good | 2GB |
| small | GPU | ⚡ | Very Good | 3GB |
| base | CPU | ⚡ | Good | 2GB |
| small | CPU | ~ | Very Good | 3GB |

*Measured on NVIDIA RTX 3070 Ti and Intel Core i7*

## 🔒 Privacy

✓ **100% Local Processing** - No data sent anywhere  
✓ **No Account Required** - No sign-ups or API keys  
✓ **No Internet Needed** - Works completely offline after setup  
✓ **Open Source** - Code is transparent and auditable  

## 🐛 Troubleshooting

### EXE won't start?
- Try running from Command Prompt: `FasterWhisper.exe`
- Check Windows Defender isn't blocking it
- See [Full Guide](docs/EXE_BUILD_GUIDE.md#troubleshooting)

### Slow transcription?
- Reduce model size (use "base" instead of "large")
- Enable GPU support (install NVIDIA drivers)
- Enable VAD Filter (removes silence)

### Hotkey not working?
- Some apps capture hotkeys (Discord, games)
- Try different hotkey in settings
- See [Full Guide](docs/EXE_BUILD_GUIDE.md) for custom hotkey setup

### "No audio device" error?
- Switch device from CUDA to CPU in settings
- Install NVIDIA drivers for GPU support
- See [Full Guide](docs/EXE_BUILD_GUIDE.md#gpu-not-detected)

## 📝 Supported Formats

**Input Audio:** MP3, WAV, M4A, AAC, OGG, FLAC, MP4, WebM, etc.

**Output Transcription:**
- **TXT** - Plain text
- **SRT** - Subtitle format with timestamps
- **VTT** - WebVTT subtitle format  
- **CSV** - Spreadsheet format with timestamps

## 🌐 Languages

Auto-detect or choose from:

English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Thai, Vietnamese, Turkish, and [99+ more](https://github.com/openai/whisper#available-models-and-languages)

## 📚 Development

### Customize the UI
Edit `gui/main.py` to modify:
- Color scheme
- Window size
- Button layout
- Hotkey combinations
- Model selection
- Output formats

### Add Features
Examples: System tray, file history, batch processing, etc.

```bash
# Run directly (for development)
python gui/main.py

# Build after changes
python build_exe.py
```

## 📄 License

MIT License - Feel free to use, modify, and distribute  
See [LICENSE](LICENSE) file for details

## 🙏 Credits

- **Whisper** - OpenAI's speech recognition model
- **CTranslate2** - Fast inference engine by OpenNMT
- **PyInstaller** - For creating standalone executables
- **Pynput** - For global hotkey support

## 🤝 Contributing

Found a bug? Have a suggestion?

1. Check [Issues](../../issues) 
2. Create new issue with details
3. Submit pull request for fixes

## 📞 Support

- 📖 **[Full Documentation](docs/EXE_BUILD_GUIDE.md)**
- 🐛 **[Report Issues](../../issues/new)**
- 💬 **[Discussions](../../discussions)**
- 📧 **Email**: support@example.com

---

**Made with ❤️ - Fast, Local, Private Speech-to-Text for Windows**

**[Download Latest Release →](../../releases)**

# YouTube to MP3 Converter

A simple, local desktop app to download YouTube videos as MP3 files. Runs entirely on your device - no server needed.

## Requirements

- **Python 3.8+**
- **FFmpeg** (must be installed and in PATH)

### Install FFmpeg

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add `bin` folder to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` / `sudo dnf install ffmpeg`

## Installation

```bash
cd yt2mp3
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Paste a YouTube URL
2. Choose save location (defaults to `~/Music/YouTube MP3`)
3. Click "Download MP3"
4. Find your MP3 in the output folder

## Features

- Clean, simple GUI
- Downloads best quality audio
- Converts to 192kbps MP3
- Remembers last download folder
- Opens output folder when done
- Runs completely offline (after initial yt-dlp install)

## Building an Executable (Optional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTube to MP3" main.py
```

The `.exe` will be in `dist/`.
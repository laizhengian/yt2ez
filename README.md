# yt2ez

A simple, local desktop app to download YouTube videos as MP3 or MP4. Runs entirely on your device - no server needed.

## Requirements

- **Python 3.8+**
- **FFmpeg** (must be installed and in PATH)

### Install FFmpeg

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add `bin` folder to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` / `sudo dnf install ffmpeg`

## Installation

```bash
cd yt2ez
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Paste a YouTube URL
2. Choose save location (defaults to `~/Music/yt2ez`)
3. Select format: MP3 (audio only) or MP4 (video + audio)
4. Click "Download"
5. Find your file in the output folder

## Features

- Clean, simple GUI
- Download MP3 (192kbps) or MP4 (best quality)
- Remembers last download folder
- Opens output folder when done
- Runs completely offline (after initial yt-dlp install)

## Building an Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "yt2ez" main.py
```

The `.exe` will be in `dist/`.
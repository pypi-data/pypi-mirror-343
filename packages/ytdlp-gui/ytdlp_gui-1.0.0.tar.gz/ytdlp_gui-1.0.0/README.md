# YT-DLP GUI

A beautiful and comprehensive graphical user interface for [yt-dlp](https://github.com/yt-dlp/yt-dlp), built with [Flet](https://flet.dev/).

## Features

- **Modern UI**: Clean, responsive interface with dark mode
- **Download Management**: Track active downloads with progress bars and download history
- **Format Selection**: Choose from various video/audio formats and quality options
- **Audio Extraction**: Download just the audio in various formats (MP3, M4A, etc.)
- **Advanced Options**: Support for subtitles, playlists, thumbnails, and more
- **Settings Management**: Import/export your download settings
- **File Management**: Easily open download folders and navigate your content

## Screenshots

(Screenshots will be added after the application is released)

## Installation

1. Ensure you have Python 3.12+ installed
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/ytdlp-gui.git
   cd ytdlp-gui
   ```
3. Install dependencies:
   ```
   pip install -e .
   ```

## Usage

Run the application:

```
python ytdlp_gui.py
```

### Basic Usage:

1. Enter a YouTube URL in the input field
2. Configure download options if needed
3. Click the Download button
4. Monitor progress in the Active Downloads tab
5. View completed downloads in the History tab

## Requirements

- Python 3.12+
- yt-dlp
- flet
- ffmpeg (for audio conversion)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the amazing downloader tool
- [Flet](https://flet.dev/) for the Flutter-powered Python UI framework

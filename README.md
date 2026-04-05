# Simple Video Downloader

A modern, cross-platform desktop application to easily download videos and audio from hundreds of supported websites (including YouTube, Instagram, Facebook, Twitter, and more). Built with Python, Qt (PySide6), and powered by `yt-dlp`.

## ✨ Features
* **Cross-Platform Extraction:** Supports downloading from all sites supported by `yt-dlp`.
* **Dynamic Resolution Selection:** Fetch and choose dynamically available video qualities (including 8K, 4K, 1080p, 720p, etc.).
* **Audio Extraction:** Option to download just the audio in Opus or MP3 formats.
* **Modern UI:** Clean, responsive, and native-feeling interface built with PySide6 (Qt). Fully respects your Windows/Linux native Default, Dark, and Light mode themes.
* **Progress Tracking:** Real-time download speeds, file size, and ETA tracking natively integrated.
* **Portable FFmpeg:** Automatically bundles and manages `ffmpeg` through Python, so you don't have to install system dependencies!

### Windows & Linux Building from Source

**Requirements for all platforms:**
* Python 3.10+

1. Clone the repository:
   ```bash
   git clone https://github.com/nuzkeser/Simple-Video-Downloader.git
   cd Simple-Video-Downloader
   ```

2. Create a virtual environment and activate it:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install all pure Python dependencies:
   ```bash
   pip install yt-dlp PySide6 imageio-ffmpeg
   ```

4. Run the application natively:
   ```bash
   python main.py
   ```

## 📦 Packaging (Windows Executable)
To build a standalone `.exe` folder that you can share with friends without them needing Python installed, you can use PyInstaller:

1. Make sure you are in your activated virtual environment.
2. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
3. Run the PyInstaller build command. (*Note: `--collect-all imageio_ffmpeg` bundles the FFmpeg engine, and `--add-data` ensures the icon is embedded for the window*):
   ```bash
   pyinstaller --noconfirm --onedir --windowed --icon "icon.ico" --add-data "icon.ico;." --collect-all imageio_ffmpeg --name "VideoDownloader" main.py
   ```
4. The compiled application will be generated in the `dist/VideoDownloader` folder!

## 📝 License
This project is open-source and available for general use.
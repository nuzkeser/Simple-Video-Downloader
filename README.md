# Simple Video Downloader

A modern GTK4/Libadwaita desktop application to easily download videos and audio from hundreds of supported websites (including YouTube, Instagram, Facebook, Twitter, and more). Built with Python and powered by `yt-dlp`.

## ✨ Features
* **Cross-Platform Extraction:** Supports downloading from all sites supported by `yt-dlp`.
* **Resolution Selection:** Fetch and choose available video qualities (1080p, 720p, 480p, 360p).
* **Audio Extraction:** Option to download just the audio in Opus or MP3 formats.
* **Modern UI:** Clean, responsive, and native-feeling Linux interface built with GTK4 and Adwaita.
* **Progress Tracking:** Real-time download speeds, file size, and ETA tracking. 
* **Custom Settings:** Configure default download locations and preferred default qualities via an integrated settings tab.

## 📦 Installation (Flatpak)
The easiest and recommended way to install Simple Video Downloader on any Linux distribution is via the provided Flatpak bundle. This bundle safely contains all necessary dependencies, including `python`, `Pillow`, `requests`, and `yt-dlp`.

1. Download the `SimpleVideoDownloader.flatpak` file.
2. Install it by running the following command in your terminal:
   ```bash
   flatpak install SimpleVideoDownloader.flatpak
   ```
3. Launch the app from your application menu or via terminal:
   ```bash
   flatpak run com.nuzkeser.SimpleVideoDownloader
   ```

## 🛠️ Building from Source
If you prefer to run the app directly from the source code, you'll need Python and a few libraries installed.

**Requirements:**
* Python 3.10+
* GTK4 & Libadwaita development headers
* `ffmpeg` (Required for Audio Extraction features)

**Setup Instructions:**
```bash
# Clone the repository
git clone https://github.com/nuzkeser/Simple-Video-Downloader.git
cd Simple-Video-Downloader

# Create a virtual environment and install dependencies
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install yt-dlp Pillow requests PyGObject

# Run the app
python main.py
```

## 📝 License
This project is open-source and available for general use.
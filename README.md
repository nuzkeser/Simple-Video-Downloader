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
If you prefer to run the app directly from the source code, you'll need Python and the GTK4 / Libadwaita development headers.

**Requirements for all platforms:**
* Python 3.10+
* `ffmpeg` (Required for Audio Extraction features)

### Linux
On Linux, install the native GTK4, Libadwaita, and system PyGObject packages through your package manager (e.g., `pacman` on Arch, `apt` on Ubuntu), and install the rest via pip:

```bash
# Clone the repository
git clone https://github.com/nuzkeser/Simple-Video-Downloader.git
cd Simple-Video-Downloader

# Create a virtual environment that can access system-level PyGObject and GTK
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Install pure Python dependencies
pip install yt-dlp Pillow requests PyGObject

# Run the app
python main.py
```

### Windows
Due to the GTK4 and Libadwaita libraries being native C integrations, building from source directly via `pip` typically fails without compiling from C source. It is officially recommended to run using [MSYS2](https://www.msys2.org/), which provides a pre-compiled GTK environment for Windows.

1. Install **MSYS2** from [msys2.org](https://www.msys2.org/).
2. Open the **"MSYS2 UCRT64"** terminal.
3. Update the package database fully (you may have to run this twice and restart the terminal if the core system updates):
   ```bash
   pacman -Syu
   ```
4. Install Python, PyGObject, GTK4, Libadwaita, and the required Python tools:
   ```bash
   pacman -S mingw-w64-ucrt-x86_64-python mingw-w64-ucrt-x86_64-python-gobject mingw-w64-ucrt-x86_64-gtk4 mingw-w64-ucrt-x86_64-libadwaita mingw-w64-ucrt-x86_64-python-pillow mingw-w64-ucrt-x86_64-python-requests
   ```
5. Install `yt-dlp` using pip:
   ```bash
   python -m pip install yt-dlp --break-system-packages
   ```
6. Navigate to your project folder inside the terminal (using MSYS2 path format, e.g., `/c/Users/...`) and run the application:
   ```bash
   cd /c/path/to/project
   python main.py
   ```

## 📝 License
This project is open-source and available for general use.
#!/bin/bash
# Activates the virtual environment and runs the Video Downloader App

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found! Please ensure it is created and yt-dlp is installed."
    echo "You can create it by running:"
    echo "python3 -m venv venv --system-site-packages && venv/bin/pip install yt-dlp Pillow requests"
    exit 1
fi

export GDK_BACKEND=wayland,x11
venv/bin/python3 main.py

import threading
import yt_dlp
from gi.repository import GLib

class VideoDownloader:
    def __init__(self):
        pass

    def fetch_metadata(self, url, on_success, on_error):
        """Fetches metadata asynchronously to avoid blocking UI."""
        def worker():
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown Title')
                    thumbnail = info.get('thumbnail', None)
                    
                    # Extract available qualities
                    formats = info.get('formats', [])
                    qualities = set()
                    
                    for f in formats:
                        height = f.get('height')
                        # Add valid video resolutions
                        if height and isinstance(height, int):
                            qualities.add(f"{height}p")
                            
                    # Sort qualities descending (e.g., 1080p, 720p, 480p)
                    sorted_qualities = sorted(list(qualities), key=lambda x: int(x.replace('p', '')), reverse=True)
                    
                    # Always provide Best and Audio Only
                    final_qualities = ["Best"] + sorted_qualities + ["Audio Only"]

                    # Call GTK callback on main thread
                    GLib.idle_add(on_success, title, thumbnail, final_qualities)
            except Exception as e:
                GLib.idle_add(on_error, str(e))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def download_video(self, url, quality, path, on_progress, on_finish, on_error):
        """Downloads video and reports progress."""
        def worker():
            format_str = 'best'
            if quality == 'audio':
                format_str = 'bestaudio/best'
            elif quality != 'best':
                # e.g., '1080p' -> '1080'
                height_str = quality.replace('p', '')
                try:
                    height = int(height_str)
                    format_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
                except ValueError:
                    pass

            def hook(d):
                if d['status'] == 'downloading':
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                    fraction = downloaded / total
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')
                    
                    GLib.idle_add(on_progress, fraction, f"Downloading: {speed} - ETA: {eta}")
                elif d['status'] == 'finished':
                    GLib.idle_add(on_progress, 1.0, "Processing file...")

            ydl_opts = {
                'format': format_str,
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'progress_hooks': [hook],
                'quiet': True,
                'no_warnings': True,
            }
            
            if quality == 'audio':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                GLib.idle_add(on_finish)
            except Exception as e:
                GLib.idle_add(on_error, str(e))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

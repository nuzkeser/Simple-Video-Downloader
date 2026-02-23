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
                    # Extract available heights
                    formats = info.get('formats', [])
                    available_heights = set()
                    
                    for f in formats:
                        height = f.get('height')
                        if height and isinstance(height, int):
                            available_heights.add(height)
                            
                    # Build available qualities based on request
                    final_qualities = []
                    for res in [1080, 720, 480, 360]:
                        # If a format with exact or greater height exists, we can offer this tier
                        # (yt-dlp will downscale or grab the closest one <= target)
                        # We'll show the option if the video has native resolution >= that tier 
                        # or if yt-dlp reported that exact tier
                        if any(h >= res for h in available_heights) or res in available_heights:
                            final_qualities.append(f"{res}p")
                    
                    # Always append audio options
                    final_qualities.extend(["Audio: Opus", "Audio: Mp3"])

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
            if quality == 'audio: opus':
                format_str = 'bestaudio/best'
            elif quality == 'audio: mp3':
                format_str = 'bestaudio/best'
            else:
                # e.g., '1080p' -> '1080'
                height_str = quality.replace('p', '')
                try:
                    height = int(height_str)
                    format_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
                except ValueError:
                    format_str = 'best'

            def hook(d):
                if d['status'] == 'downloading':
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                    fraction = downloaded / total if total > 0 else 0
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

            # Enforce .mp4 video outputs if it is a video request
            if not quality.startswith('audio'):
                ydl_opts['merge_output_format'] = 'mp4'
            
            if quality == 'audio: mp3':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            elif quality == 'audio: opus':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'opus',
                }]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                GLib.idle_add(on_finish)
            except Exception as e:
                GLib.idle_add(on_error, str(e))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

import threading
import yt_dlp
from PySide6.QtCore import QObject, Signal

class DownloaderSignals(QObject):
    metadata_success = Signal(str, object, list)
    metadata_error = Signal(str)
    progress = Signal(float, str)
    finish = Signal()
    error = Signal(str)

class VideoDownloader:
    def __init__(self):
        pass

    def fetch_metadata(self, url, on_success, on_error):
        """Fetches metadata asynchronously to avoid blocking UI."""
        signals = DownloaderSignals()
        signals.metadata_success.connect(on_success)
        signals.metadata_error.connect(on_error)
        
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
                    for res in [4320, 2160, 1440, 1080, 720, 480, 360]:
                        # If a format with exact or greater height exists, we can offer this tier
                        # We'll show the option if the video has native resolution >= that tier 
                        # or if yt-dlp reported that exact tier
                        if any(h >= res for h in available_heights) or res in available_heights:
                            if res == 4320:
                                label = "8K (4320p)"
                            elif res == 2160:
                                label = "4K (2160p)"
                            else:
                                label = f"{res}p"
                            final_qualities.append(label)
                    
                    # Always append audio options
                    final_qualities.extend(["Audio: Opus", "Audio: Mp3"])

                    # Call UI callback on main thread
                    signals.metadata_success.emit(title, thumbnail, final_qualities)
            except Exception as e:
                signals.metadata_error.emit(str(e))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.signals = signals # retain reference
        thread.start()

    def download_video(self, url, quality, path, on_progress, on_finish, on_error):
        """Downloads video and reports progress."""
        signals = DownloaderSignals()
        signals.progress.connect(on_progress)
        signals.finish.connect(on_finish)
        signals.error.connect(on_error)
        
        def worker():
            format_str = 'best'
            if quality == 'audio: opus':
                format_str = 'bestaudio/best'
            elif quality == 'audio: mp3':
                format_str = 'bestaudio/best'
            else:
                import re
                match = re.search(r'(\d+)p', quality)
                if match:
                    height = int(match.group(1))
                    format_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
                else:
                    format_str = 'best'

            def hook(d):
                if d['status'] == 'downloading':
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                    fraction = downloaded / total if total > 0 else 0
                    
                    import re
                    speed = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_speed_str', 'N/A')))
                    eta = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_eta_str', 'N/A')))
                    
                    signals.progress.emit(fraction, f"Downloading: {speed} - ETA: {eta}")
                elif d['status'] == 'finished':
                    signals.progress.emit(1.0, "Processing file...")

            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

            ydl_opts = {
                'format': format_str,
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'progress_hooks': [hook],
                'quiet': True,
                'no_warnings': True,
                'nocolor': True,
                'ffmpeg_location': ffmpeg_path,
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
                signals.finish.emit()
            except Exception as e:
                signals.error.emit(str(e))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.signals = signals
        thread.start()

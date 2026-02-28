import json
import os
import pathlib

class SettingsManager:
    def __init__(self):
        # Default save location is ~/Downloads/Video Downloader
        self.default_download_path = os.path.join(pathlib.Path.home(), "Downloads", "Video Downloader")
        self.settings_file = os.path.join(pathlib.Path.home(), ".config", "simple-video-downloader", "settings.json")
        self.settings = self._load()

    def _load(self):
        defaults = {
            "download_path": self.default_download_path,
            "default_quality": "1080p", # "1080p", "720p", "480p", "360p", "Audio: Opus", "Audio: Mp3"
            "theme": "System Default"
        }
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                for k, v in defaults.items():
                    if k not in settings:
                        settings[k] = v
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return defaults

    def save(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

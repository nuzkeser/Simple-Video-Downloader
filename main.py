import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from ui.main_window import MainWindow
from core.settings_manager import SettingsManager
from core.downloader import VideoDownloader

class VideoDownloaderApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.nuzkeser.SimpleVideoDownloader',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        # Initialize Data Managers
        self.settings = SettingsManager()
        self.downloader = VideoDownloader()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

if __name__ == '__main__':
    app = VideoDownloaderApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

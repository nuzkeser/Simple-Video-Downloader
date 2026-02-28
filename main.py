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
        # Apply theme on startup
        theme = self.settings.get("theme")
        style_manager = Adw.StyleManager.get_default()
        if theme == "Light":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif theme == "Dark":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)

        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

if __name__ == '__main__':
    app = VideoDownloaderApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

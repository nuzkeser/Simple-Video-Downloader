import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from ui.download_tab import DownloadTab
from ui.settings_tab import SettingsTab

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Video Downloader")
        self.set_default_size(650, 750)

        # Header bar
        header = Adw.HeaderBar()
        
        # View switcher title
        switcher_title = Adw.ViewSwitcherTitle()
        switcher_title.set_title("Video Downloader")
        header.set_title_widget(switcher_title)

        # Main layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(header)

        # View stack for tabs
        self.stack = Adw.ViewStack()
        
        # Connect switcher to stack
        switcher_title.set_stack(self.stack)

        # View Switcher Bar for narrow widths
        switcher_bar = Adw.ViewSwitcherBar()
        switcher_bar.set_stack(self.stack)
        
        # Add tabs
        self.download_tab = DownloadTab(self.props.application)
        self.settings_tab = SettingsTab(self.props.application)

        self.stack.add_titled(self.download_tab, "download", "Download")
        self.stack.add_titled(self.settings_tab, "settings", "Settings")
        
        # Set icons for the switcher
        self.stack.get_page(self.download_tab).set_icon_name("folder-download-symbolic")
        self.stack.get_page(self.settings_tab).set_icon_name("emblem-system-symbolic")

        box.append(self.stack)
        box.append(switcher_bar)
        
        # Make stack expand so it fills the window
        self.stack.set_vexpand(True)

        self.set_content(box)

        # Handle adaptive switcher bar
        self.breakpoint = Adw.Breakpoint.new(Adw.breakpoint_condition_parse("max-width: 500px"))
        self.breakpoint.add_setter(switcher_title, "title-visible", True)
        self.breakpoint.add_setter(switcher_bar, "reveal", True)
        self.add_breakpoint(self.breakpoint)

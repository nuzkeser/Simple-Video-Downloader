import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

class SettingsTab(Adw.PreferencesPage):
    def __init__(self, app):
        super().__init__()
        self.app = app

        group = Adw.PreferencesGroup(title="General Settings", description="Configure how and where videos are downloaded.")
        self.add(group)

        # Download Path Row
        self.path_row = Adw.ActionRow(title="Download Path")
        self.path_row.set_subtitle(self.app.settings.get("download_path"))
        
        select_btn = Gtk.Button(label="Select Folder")
        select_btn.set_valign(Gtk.Align.CENTER)
        select_btn.connect('clicked', self.on_select_folder)
        self.path_row.add_suffix(select_btn)

        # Quality Row
        self.quality_row = Adw.ComboRow(title="Default Quality")
        model = Gtk.StringList.new(["1080p", "720p", "480p", "360p", "Audio: Opus", "Audio: Mp3"])
        self.quality_row.set_model(model)
        
        # set default based on settings
        default_q = self.app.settings.get("default_quality")
        default_idx = 0
        if default_q == "720p": default_idx = 1
        elif default_q == "480p": default_idx = 2
        elif default_q == "360p": default_idx = 3
        elif default_q == "Audio: Opus": default_idx = 4
        elif default_q == "Audio: Mp3": default_idx = 5

        self.quality_row.set_selected(default_idx)
        
        self.quality_row.connect('notify::selected', self.on_quality_changed)

        group.add(self.path_row)
        group.add(self.quality_row)

    def on_select_folder(self, btn):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Select Download Folder")
        
        # Set initial folder
        initial_dir = Gio.File.new_for_path(self.app.settings.get("download_path"))
        dialog.set_initial_folder(initial_dir)
        
        dialog.select_folder(self.get_root(), None, self.on_folder_selected)

    def on_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.app.settings.set("download_path", path)
                self.path_row.set_subtitle(path)
        except GLib.Error as e:
            # User canceled or error
            pass

    def on_quality_changed(self, combo_row, param):
        selected_item = combo_row.get_selected_item()
        if selected_item:
            quality = selected_item.get_string()
            self.app.settings.set("default_quality", quality)

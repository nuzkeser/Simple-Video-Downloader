import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio
import urllib.request
import tempfile
import os

class DownloadTab(Adw.Bin):
    def __init__(self, app):
        super().__init__()
        self.app = app

        clamp = Adw.Clamp()
        clamp.set_maximum_size(600)
        self.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)
        clamp.set_child(box)

        # Overview Image
        self.thumbnail_image = Gtk.Picture()
        self.thumbnail_image.set_size_request(-1, 280)
        self.thumbnail_image.set_halign(Gtk.Align.CENTER)
        self.thumbnail_image.set_valign(Gtk.Align.CENTER)
        # Use a placeholder icon for now
        self.thumbnail_image.set_resource("/org/gtk/libgtk/icons/16x16/actions/image-missing.png")
        self.thumbnail_image.set_visible(False)

        # Fallback to an icon image instead if picture resource doesnt work
        # Try a simpler standard image file or icon
        self.fallback_icon = Gtk.Image.new_from_icon_name("media-playback-start-symbolic")
        self.fallback_icon.set_pixel_size(128)
        self.fallback_icon.add_css_class("dim-label")
        self.fallback_icon.set_size_request(-1, 280)

        # Title Label
        self.title_label = Gtk.Label(label="Paste a link to load video details")
        self.title_label.add_css_class("title-2")
        self.title_label.set_wrap(True)
        self.title_label.set_justify(Gtk.Justification.CENTER)

        # Link Entry
        self.link_entry = Gtk.Entry()
        self.link_entry.set_placeholder_text("Instagram, Facebook, YouTube, Twitter...")
        self.link_entry.set_hexpand(True)
        self.link_entry.connect('changed', self.on_link_changed)

        # Quality Dropdown
        self.quality_model = Gtk.StringList.new(["Best", "1080p", "720p", "Audio"])
        self.quality_dropdown = Gtk.DropDown(model=self.quality_model)

        # Set default quality from settings
        default_q = self.app.settings.get("default_quality")
        if default_q == "1080p": self.quality_dropdown.set_selected(1)
        elif default_q == "720p": self.quality_dropdown.set_selected(2)
        elif default_q == "audio": self.quality_dropdown.set_selected(3)

        # Input Row (Entry + Dropdown)
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        input_box.append(self.link_entry)
        input_box.append(self.quality_dropdown)

        # Download Button
        self.download_btn = Gtk.Button(label="Download")
        self.download_btn.add_css_class("suggested-action")
        self.download_btn.add_css_class("pill")
        self.download_btn.set_sensitive(False)
        self.download_btn.connect('clicked', self.on_download_clicked)

        # Download button box for centering / pill shape
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_box.append(self.download_btn)

        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_visible(False)
        self.status_label = Gtk.Label(label="")
        self.status_label.set_visible(False)
        
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        progress_box.append(self.progress_bar)
        progress_box.append(self.status_label)

        # Assemble
        # Using fallback icon initially instead of picture with broken resource
        self.image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.image_box.append(self.fallback_icon)
        self.image_box.append(self.thumbnail_image)
        
        box.append(self.image_box)
        box.append(self.title_label)
        box.append(input_box)
        box.append(btn_box)
        box.append(progress_box)

    def on_link_changed(self, entry):
        text = entry.get_text().strip()
        if text.startswith("http://") or text.startswith("https://"):
            self.download_btn.set_sensitive(False)
            self.title_label.set_label("Fetching metadata...")
            self.app.downloader.fetch_metadata(text, self._on_metadata_success, self._on_metadata_error)
        else:
            self.download_btn.set_sensitive(False)
            self.title_label.set_label("Paste a link to load video details")

    def _on_metadata_success(self, title, thumbnail_url, qualities):
        self.title_label.set_label(title)
        self.download_btn.set_sensitive(True)
        
        # Update qualities
        self.quality_model.splice(0, self.quality_model.get_n_items(), qualities)
        
        # Restore user preference if it exists in the new list
        pref = self.app.settings.get("default_quality")
        if pref == 'audio':
            pref_str = 'Audio Only'
        elif pref == 'best':
            pref_str = 'Best'
        else:
            pref_str = pref
            
        for i, q in enumerate(qualities):
            if q.lower() == pref_str.lower():
                self.quality_dropdown.set_selected(i)
                break
        
        if thumbnail_url:
            try:
                # Download thumbnail to temp file
                req = urllib.request.Request(thumbnail_url, headers={'User-Agent': 'Mozilla/5.0'})
                fd, path = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                    out_file.write(response.read())
                
                self.fallback_icon.set_visible(False)
                # Ensure the local file can be successfully bound as a Gtk.Picture via Gtk.Image replacement or Gio.File
                # Some GTK4 versions have issues with Picture.set_filename directly depending on backend formats
                gfile = Gio.File.new_for_path(path)
                self.thumbnail_image.set_file(gfile)
                self.thumbnail_image.set_visible(True)
            except Exception as e:
                print(f"Error loading thumbnail: {e}")
                self.fallback_icon.set_visible(True)
                self.thumbnail_image.set_visible(False)
        else:
            self.fallback_icon.set_visible(True)
            self.thumbnail_image.set_visible(False)

    def _on_metadata_error(self, error_msg):
        self.title_label.set_label(f"Error fetching data: {error_msg}")
        self.download_btn.set_sensitive(False)

    def on_download_clicked(self, btn):
        self.link_entry.set_sensitive(False)
        self.download_btn.set_sensitive(False)
        self.progress_bar.set_visible(True)
        self.status_label.set_visible(True)
        self.progress_bar.set_fraction(0.1)
        self.status_label.set_label("Starting download...")
        
        url = self.link_entry.get_text().strip()
        quality_item = self.quality_dropdown.get_selected_item()
        quality = quality_item.get_string().lower() if quality_item else "best"
        if quality == "audio only": quality = "audio"
        path = self.app.settings.get("download_path")
        
        self.app.downloader.download_video(
            url, quality, path, 
            self._on_download_progress, 
            self._on_download_finish, 
            self._on_download_error
        )

    def _on_download_progress(self, fraction, status_text):
        self.progress_bar.set_fraction(fraction)
        self.status_label.set_label(status_text)
        
    def _on_download_finish(self):
        self.progress_bar.set_fraction(1.0)
        self.status_label.set_label("Download completed successfully!")
        self.link_entry.set_sensitive(True)
        self.download_btn.set_sensitive(True)
        
    def _on_download_error(self, error_msg):
        self.status_label.set_label(f"Error: {error_msg}")
        self.progress_bar.set_fraction(0.0)
        self.link_entry.set_sensitive(True)
        self.download_btn.set_sensitive(True)

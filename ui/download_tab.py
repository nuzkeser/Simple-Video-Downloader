from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QProgressBar, QApplication
)
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QPixmap, QImage
import urllib.request
import threading
import os

class ThumbnailSignals(QObject):
    success = Signal(object)
    error = Signal()
    

class DownloadTab(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)

        # Image setup
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setFixedSize(500, 280)
        self.thumbnail_label.setObjectName("ImageSetup")
        self.thumbnail_label.setStyleSheet("border-radius: 10px;")
        
        self.fallback_icon = QLabel("🎬")
        self.fallback_icon.setAlignment(Qt.AlignCenter)
        self.fallback_icon.setObjectName("IconSetup")
        self.fallback_icon.setStyleSheet("font-size: 64px; border-radius: 10px;")
        self.fallback_icon.setFixedSize(500, 280)
        
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.fallback_icon)
        self.image_layout.addWidget(self.thumbnail_label)
        self.thumbnail_label.hide()
        
        img_container = QWidget()
        img_container.setLayout(self.image_layout)
        
        # Title Label
        self.title_label = QLabel("Paste a link to load video details")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.title_label.setWordWrap(True)

        # Link Entry
        self.link_entry = QLineEdit()
        self.link_entry.setPlaceholderText("Instagram, Facebook, YouTube, Twitter...")
        self.link_entry.textChanged.connect(self.on_link_changed)
        self.link_entry.setMinimumHeight(40)

        # Quality Dropdown
        self.quality_dropdown = QComboBox()
        self.quality_dropdown.addItem("Quality")
        self.quality_dropdown.setEnabled(False)
        self.quality_dropdown.setMinimumHeight(40)
        self.quality_dropdown.setMinimumWidth(160)

        # Input Row
        input_box = QHBoxLayout()
        input_box.addWidget(self.link_entry, stretch=1)
        input_box.addWidget(self.quality_dropdown)

        # Download Button
        self.download_btn = QPushButton("Download")
        self.download_btn.setEnabled(False)
        self.download_btn.setFixedSize(160, 45)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #3584e4;
                color: white;
                border-radius: 22px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: #4a4a4a;
                color: #888;
            }
            QPushButton:hover {
                background-color: #4a90e2;
            }
        """)
        self.download_btn.clicked.connect(self.on_download_clicked)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.download_btn)
        btn_layout.addStretch()

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()

        layout.addWidget(img_container, 0, Qt.AlignHCenter)
        layout.addWidget(self.title_label)
        layout.addLayout(input_box)
        layout.addLayout(btn_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        self.setLayout(layout)

    def on_link_changed(self, text):
        text = text.strip()
        if text.startswith("http://") or text.startswith("https://") or text.startswith("www."):
            self.download_btn.setEnabled(False)
            self.title_label.setText("Fetching metadata...")
            self.quality_dropdown.clear()
            self.quality_dropdown.addItem("Fetching qualities...")
            self.quality_dropdown.setEnabled(False)
            self.app.downloader.fetch_metadata(text, self._on_metadata_success, self._on_metadata_error)
        else:
            self.download_btn.setEnabled(False)
            self.title_label.setText("Paste a link to load video details")
            self.quality_dropdown.clear()
            self.quality_dropdown.addItem("Quality")
            self.quality_dropdown.setEnabled(False)

    def _on_metadata_success(self, title, thumbnail_url, qualities):
        self.title_label.setText(title)
        self.download_btn.setEnabled(True)
        
        self.quality_dropdown.clear()
        if qualities:
            self.quality_dropdown.addItems(qualities)
            self.quality_dropdown.setEnabled(True)
        else:
            self.quality_dropdown.addItem("No Qualities")
            self.quality_dropdown.setEnabled(False)

        if thumbnail_url:
            signals = ThumbnailSignals()
            signals.success.connect(self._apply_thumbnail)
            signals.error.connect(self._apply_fallback)
            
            def load_thumbnail_worker():
                try:
                    req = urllib.request.Request(
                        thumbnail_url, 
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req, timeout=10) as response:
                        img_data = response.read()
                        
                        img = QImage()
                        img.loadFromData(img_data)
                        pixmap = QPixmap.fromImage(img).scaled(500, 280, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                        
                        signals.success.emit(pixmap)
                        
                except Exception as e:
                    signals.error.emit()

            t = threading.Thread(target=load_thumbnail_worker, daemon=True)
            t.signals = signals
            t.start()
        else:
            self._apply_fallback()

    def _apply_thumbnail(self, pixmap):
        self.fallback_icon.hide()
        self.thumbnail_label.setPixmap(pixmap)
        self.thumbnail_label.show()

    def _apply_fallback(self):
        self.fallback_icon.show()
        self.thumbnail_label.hide()

    def _on_metadata_error(self, error_msg):
        self.title_label.setText(f"Error fetching data: {error_msg}")
        self.download_btn.setEnabled(False)

    def on_download_clicked(self):
        self.link_entry.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.progress_bar.show()
        self.status_label.show()
        self.progress_bar.setValue(10) # 10%
        self.status_label.setText("Starting download...")
        
        url = self.link_entry.text().strip()
        quality = self.quality_dropdown.currentText().lower()
        if not quality or quality == "quality" or quality == "fetching qualities...":
            quality = "best"
        if quality == "audio only": quality = "audio"
        path = self.app.settings.get("download_path")
        
        self.app.downloader.download_video(
            url, quality, path, 
            self._on_download_progress, 
            self._on_download_finish, 
            self._on_download_error
        )

    def _on_download_progress(self, fraction, status_text):
        self.progress_bar.setValue(int(fraction * 100))
        self.status_label.setText(status_text)
        
    def _on_download_finish(self):
        self.progress_bar.setValue(100)
        self.status_label.setText("Download completed successfully!")
        self.link_entry.setEnabled(True)
        self.download_btn.setEnabled(True)
        
    def _on_download_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.progress_bar.setValue(0)
        self.link_entry.setEnabled(True)
        self.download_btn.setEnabled(True)

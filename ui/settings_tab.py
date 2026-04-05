from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QFileDialog, QGroupBox, QLineEdit
)
from PySide6.QtCore import Qt

class SettingsTab(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        
        group_box = QGroupBox("General Settings")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(16)
        
        # Download Path Row
        path_layout = QHBoxLayout()
        path_label = QLabel("Download Path:")
        path_label.setFixedWidth(120)
        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setText(self.app.settings.get("download_path"))
        
        select_btn = QPushButton("Select Folder")
        select_btn.clicked.connect(self.on_select_folder)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_display)
        path_layout.addWidget(select_btn)
        
        # Theme Row
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setFixedWidth(120)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System Default", "Light", "Dark"])
        
        default_theme = self.app.settings.get("theme")
        self.theme_combo.setCurrentText(default_theme if default_theme else "System Default")
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        
        group_layout.addLayout(path_layout)
        group_layout.addLayout(theme_layout)
        group_box.setLayout(group_layout)
        
        layout.addWidget(group_box)
        layout.addStretch()
        
        self.setLayout(layout)

    def on_select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.app.settings.get("download_path"))
        if folder:
            self.app.settings.set("download_path", folder)
            self.path_display.setText(folder)

    def on_theme_changed(self, theme):
        self.app.settings.set("theme", theme)
        self.app.apply_theme()

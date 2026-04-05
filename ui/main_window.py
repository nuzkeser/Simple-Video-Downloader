from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon
from ui.download_tab import DownloadTab
from ui.settings_tab import SettingsTab
import os

class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()
        self.app = application
        self.setWindowTitle("Video Downloader")
        self.resize(650, 750)
        
        # Check if icon exists and set it
        if os.path.exists("icon.ico"):
            self.setWindowIcon(QIcon("icon.ico"))
        elif os.path.exists("icon.png"):
            self.setWindowIcon(QIcon("icon.png"))
            
        # Main layout widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 0;
            }
            QTabBar::tab {
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.tabs)
        
        # Tabs
        self.download_tab = DownloadTab(self.app)
        self.settings_tab = SettingsTab(self.app)
        
        self.tabs.addTab(self.download_tab, "Download")
        self.tabs.addTab(self.settings_tab, "Settings")

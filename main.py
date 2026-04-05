import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt
import ctypes

from ui.main_window import MainWindow
from core.settings_manager import SettingsManager
from core.downloader import VideoDownloader

class VideoDownloaderApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("Simple Video Downloader")
        
        # Set app ID for Windows so taskbar behaves correctly
        try:
            myappid = 'com.nuzkeser.SimpleVideoDownloader' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
            
        self.settings = SettingsManager()
        self.downloader = VideoDownloader()
        
        # Set font
        font = QFont("Segoe UI", 11)
        font.setStyleHint(QFont.SansSerif)
        self.setFont(font)

        self.apply_theme()
        
        self.main_window = MainWindow(self)
        self.main_window.show()
        
    def apply_theme(self):
        theme = self.settings.get("theme")
        self.setStyle("Fusion")
        
        base_stylesheet = """
            QLineEdit {
                padding: 10px 14px;
                border-radius: 8px;
                font-size: 14px;
            }
            QGroupBox {
                border-radius: 12px;
                margin-top: 1.5em;
                padding-top: 20px;
                padding-bottom: 20px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding-left: 15px;
                font-weight: bold;
                font-size: 15px;
            }
            QLabel {
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 0;
            }
            QTabBar::tab {
                padding: 12px 35px;
                font-size: 15px;
                font-weight: bold;
                border-bottom: 3px solid transparent;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
        """

        use_dark = False
        if theme == "Dark":
            use_dark = True
        elif theme == "System Default" or not theme:
            bg_lightness = self.style().standardPalette().color(QPalette.ColorRole.Window).lightness()
            if bg_lightness < 128:
                use_dark = True

        if use_dark:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(32, 32, 32))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(53, 132, 228))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(53, 132, 228))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            self.setPalette(palette)
            
            dark_stylesheet = base_stylesheet + """
                QLineEdit {
                    border: 1px solid #444;
                    background-color: #2b2b2b;
                    color: white;
                }
                QLineEdit:focus, QLineEdit:hover {
                    border: 1px solid #3584e4;
                    background-color: #333;
                }
                QGroupBox {
                    border: 1px solid #3d3d3d;
                    background-color: #242424;
                }
                QGroupBox::title {
                    color: #ddd;
                }
                QTabBar::tab {
                    color: #888;
                }
                QTabBar::tab:selected {
                    color: #3584e4;
                    border-bottom: 3px solid #3584e4;
                }
                QTabBar::tab:hover:!selected {
                    color: #bbb;
                }
                QPushButton {
                    background-color: #444;
                    border: 1px solid #555;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """
            self.setStyleSheet(dark_stylesheet)
        else:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
            palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
            self.setPalette(palette)
            
            light_stylesheet = base_stylesheet + """
                QLineEdit {
                    border: 1px solid #ccc;
                    background-color: #fff;
                    color: black;
                }
                QLineEdit:focus, QLineEdit:hover {
                    border: 1px solid #3584e4;
                }
                QGroupBox {
                    border: 1px solid #e0e0e0;
                    background-color: #f9f9f9;
                }
                QGroupBox::title {
                    color: #333;
                }
                QTabBar::tab {
                    color: #666;
                }
                QTabBar::tab:selected {
                    color: #3584e4;
                    border-bottom: 3px solid #3584e4;
                }
                QTabBar::tab:hover:!selected {
                    color: #333;
                }
                QPushButton {
                    background-color: #eee;
                    border: 1px solid #ccc;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #ddd;
                }
            """
            self.setStyleSheet(light_stylesheet)

if __name__ == '__main__':
    app = VideoDownloaderApp(sys.argv)
    sys.exit(app.exec())

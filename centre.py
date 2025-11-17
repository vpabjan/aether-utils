#!/usr/bin/env python3
import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class UserSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window |
Qt.WindowType.FramelessWindowHint |
Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("User Settings")
        self.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("User Settings Placeholder"))
        self.setLayout(layout)

class AetherCentre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AetherCentre")
        self.setGeometry(100, 100, 300, 400)
        self.setFixedSize(300, 400)
        self.initUI()

    def launch_app_scripts(self):
        try:
            subprocess.Popen(["python3", f"{sys.path[0]}/scripts.py"])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not launch Scripts browser: {e}")


    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        title = QLabel("Aether Linux")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        main_layout.addWidget(title)

        subtitle = QLabel("Centre")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: gray;")
        main_layout.addWidget(subtitle)

        # Buttons
        button_layout = QVBoxLayout()
        apps = [
            ("User Settings", self.open_user_settings),
            ("System Information", self.show_system_info),
            ("Firefox", lambda: self.launch_app("firefox")),
            ("Task Manager", lambda: self.launch_app("btop")),
            ("File Manager", lambda: self.launch_app("nemo")),
            ("Scripts", lambda: self.launch_app_scripts())
        ]

        for name, func in apps:
            btn = QPushButton(name)
            btn.clicked.connect(func)
            btn.setFixedHeight(40)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        # Version label
        version_label = QLabel("v0.0.1")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: gray; font-size: 12px;")
        main_layout.addWidget(version_label)

        self.setLayout(main_layout)

    def open_user_settings(self):
        self.user_window = UserSettingsWindow()
        self.user_window.show()

    def show_system_info(self):
        try:
            info = subprocess.check_output("uname -a", shell=True, text=True)
            QMessageBox.information(self, "System Information", info)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def launch_app(self, app_name):
        try:
            subprocess.Popen(app_name)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not launch {app_name}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AetherCentre()
    window.show()
    sys.exit(app.exec())

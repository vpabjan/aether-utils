#!/usr/bin/env python3
import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import webbrowser
import os


GITHUB_URL = "https://github.com/vpabjan/aether-linux"


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Aether Linux")

        # Try to make this window float in Hyprland
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        self.setFixedSize(350, 320)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("󰣇  Welcome to Aether Linux")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        """)

        subtitle = QLabel("Your new arch experience.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 12px;
            color: #333333;
        """)

        # Buttons
        btn_open = QPushButton("Open Centre")
        btn_open.clicked.connect(self.open_center)
        btn_open.setFixedHeight(40)

        btn_scripts = QPushButton("Open Scripts")
        btn_scripts.clicked.connect(self.open_scripts)
        btn_scripts.setFixedHeight(40)

        btn_info = QPushButton("Info (GitHub)")
        btn_info.clicked.connect(self.open_info)
        btn_info.setFixedHeight(40)


        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        btn_close.setFixedHeight(40)

        for b in (btn_open, btn_info, btn_close, btn_scripts):
            b.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 6px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #000000;
                    color: #ffffff;
                }
            """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(btn_open)
        layout.addWidget(btn_info)
        layout.addWidget(btn_scripts)
        layout.addWidget(btn_close)

        self.setLayout(layout)

    def open_center(self):
        """Run the second script (center.py)"""
        script_path = os.path.join(os.path.dirname(__file__), "centre.py")
        subprocess.Popen(["python3", script_path])

    def open_scripts(self):
        """Run the second script (center.py)"""
        script_path = os.path.join(os.path.dirname(__file__), "scripts.py")
        subprocess.Popen(["python3", script_path])

    def open_info(self):
        """Open GitHub link in Firefox"""
        try:
            subprocess.Popen(["firefox", GITHUB_URL])
        except FileNotFoundError:
            webbrowser.open(GITHUB_URL)


def main():
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


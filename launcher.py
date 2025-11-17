#!/usr/bin/env python3
import sys
import subprocess
import os
from functools import partial

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QGridLayout, QVBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


GITHUB_URL = "https://github.com/vpabjan/aether-linux"


def run_script(name):
    script_path = os.path.join(os.path.dirname(__file__), name)
    try:
        subprocess.Popen(["python3", script_path])
    except Exception as e:
        # fail silently for launcher usage; you can log if you want
        print("Failed to run", script_path, e)


class SymbolButton(QPushButton):
    """
    QPushButton that contains two QLabel widgets stacked:
    - big_label: large letter
    - small_label: small secondary letters
    """
    def __init__(self, big: str, small: str, callback=None, parent=None):
        super().__init__(parent)

        # make the QPushButton visually 'container-like'
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(100, 100)

        # layout inside the button
        v = QVBoxLayout(self)
        v.setContentsMargins(10, 6, 10, 6)
        v.setSpacing(2)
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # big label
        self.big_label = QLabel(big, self)
        big_font = QFont()
        big_font.setPointSize(36)
        big_font.setBold(True)
        self.big_label.setFont(big_font)
        self.big_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # small label
        self.small_label = QLabel(small, self)
        small_font = QFont()
        small_font.setPointSize(10)
        small_font.setBold(False)
        self.small_label.setFont(small_font)
        self.small_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ensure labels are transparent so button stylesheet controls look
        self.big_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.small_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        v.addWidget(self.big_label)
        v.addWidget(self.small_label)

        if callback:
            self.clicked.connect(callback)

        # Style: transparent-ish background, border, rounded corners.
        # Hover will invert color and make labels white.
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(0,0,0,0.85);
                border: 2px solid rgba(255,255,255,0.85);
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0,0,0,1);
                color: rgba(255,255,255,1)

            }
            QPushButton QLabel {
                color: #000000;
                background-color: #000000;
            }
            QPushButton:hover QLabel {
                color: #ffffff;
                background-color: #ffffff;
            }
        """)


class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aether Launcher")
        # Transparent background for the whole window
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Frameless and stay-on-top (good for floating launcher in Hyprland)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # Optional: fixed size to keep the layout consistent
        self.setFixedSize(380, 380)

        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        # buttons: (big, small, callback-or-none)
        buttons = [
            ("Al", "alacritty", self.open_alacritty),
            ("Ce", "centre", self.open_centre),
            ("Fi", "firefox", None),
            ("Sc", "scripts", self.open_scripts),
            ("X", "exit", self.close_launcher),
            ("B", "btop", None),
            ("D", "b", None),
            ("N", "w", None),
            ("H", "l", None),
        ]

        idx = 0
        for r in range(3):
            for c in range(3):
                big, small, cb = buttons[idx]
                if cb is None:
                    # dummy -> call scripts.py
                    btn = SymbolButton(big, small, callback=partial(run_script, "scripts.py"))
                else:
                    btn = SymbolButton(big, small, callback=cb)
                layout.addWidget(btn, r, c)
                idx += 1

        self.setLayout(layout)

    # behaviors
    def open_scripts(self):
        run_script("scripts.py")
        sys.exit()

    def open_alacritty(self):
        subprocess.call("/bin/alacritty");
        sys.exit()

    def open_firefox(self):
        subprocess.call("/bin/firefox");
        sys.exit()

    def open_centre(self):
        run_script("centre.py")
        self.close()
        sys.exit()

    def close_launcher(self):
        self.close()
        sys.exit()


def main():
    app = QApplication(sys.argv)

    # Optional: disable window decorations in some compositors further
    # and make sure the app has the attribute set for translucency
    window = Launcher()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

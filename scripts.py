#!/usr/bin/env python3
import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QGroupBox, QHBoxLayout, QLineEdit
)
from PyQt6.QtCore import Qt

scripts = [
    {
        "name": "Install nvidia-dkms",
        "path": "scripts/install_nvidia_dkms.sh",
        "origin": "aether-utils",
        "version": "0.1",
        "description": "Install nvidia-dkms from official Arch repo"
    },
    {
        "name": "Update System",
        "path": "scripts/update_system.sh",
        "origin": "aether-utils",
        "version": "0.1",
        "description": "Run a full system update"
    },
    {
        "name": "Install yay",
        "path": "scripts/install_yay.sh",
        "origin": "aether-utils",
        "version": "0.1",
        "description": "Installs yay from its official git repo."
    },
    {
        "name": "Install iwmenu",
        "path": "scripts/install_iwmenu.sh",
        "origin": "aether-utils",
        "version": "0.1",
        "description": "Installs iwmenu from its official git repo."
    },
    {
        "name": "Change hostname",
        "path": "scripts/change_hostname.sh",
        "origin": "aether-utils",
        "version": "0.1",
        "description": "Change this computer's hostname."
    }
]

class ScriptBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
    Qt.WindowType.Window |
    Qt.WindowType.FramelessWindowHint |
    Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Aether Scripts")
        self.setGeometry(200, 200, 800, 600)
        self.setFixedSize(800, 600)

        self.layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search scripts...")
        self.search_bar.textChanged.connect(self.update_displayed_scripts)
        self.layout.addWidget(self.search_bar)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

        # Store boxes for filtering
        self.script_boxes = []
        self.populate_scripts(scripts)

    def populate_scripts(self, script_list):
        # Clear existing
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.script_boxes = []

        for script in script_list:
            box = QGroupBox(script["name"])
            box_layout = QVBoxLayout()

            box_layout.addWidget(QLabel(f"Path: {script['path']}"))
            box_layout.addWidget(QLabel(f"Origin: {script['origin']}"))
            box_layout.addWidget(QLabel(f"Version: {script['version']}"))
            box_layout.addWidget(QLabel(f"Description: {script['description']}"))

            run_button = QPushButton("Run in Alacritty")
            run_button.clicked.connect(lambda checked, s=script: self.run_script(s))
            box_layout.addWidget(run_button)

            box.setLayout(box_layout)
            self.scroll_layout.addWidget(box)
            self.script_boxes.append((box, script))

    def update_displayed_scripts(self, text):
        text = text.lower()
        for box, script in self.script_boxes:
            if (text in script["name"].lower() or
                text in script["origin"].lower() or
                text in script["description"].lower()):
                box.show()
            else:
                box.hide()

    def run_script(self, script):
        script_path = f"{sys.path[0]}/{script['path']}"
        try:
            subprocess.Popen(["alacritty", "-e", script_path])
        except Exception as e:
            print(f"Failed to run {script_path}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScriptBrowser()
    window.show()
    sys.exit(app.exec())

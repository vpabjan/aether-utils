#!/usr/bin/env python3
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class HostnameChanger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change Hostname")
        self.setGeometry(300, 300, 400, 150)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter new hostname:"))
        self.hostname_input = QLineEdit()
        layout.addWidget(self.hostname_input)

        btn = QPushButton("Change Hostname")
        btn.clicked.connect(self.change_hostname)
        layout.addWidget(btn)

        self.setLayout(layout)

    def change_hostname(self):
        new_hostname = self.hostname_input.text().strip()
        if not new_hostname:
            QMessageBox.warning(self, "Error", "Please enter a valid hostname")
            return

        try:
            # Ask for sudo to change hostname
            subprocess.run(
                ["pkexec", "hostnamectl", "set-hostname", new_hostname],
                check=True
            )
            QMessageBox.information(self, "Success", f"Hostname changed to {new_hostname}")
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to change hostname:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HostnameChanger()
    window.show()
    sys.exit(app.exec())

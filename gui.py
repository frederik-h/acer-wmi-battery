#!/usr/bin/env python3
import os
import subprocess
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox,
                             QStyle, QFileDialog)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import Qt, QSettings, QByteArray

class BatteryControl(QWidget):

    def __init__(self):
        super().__init__()

        self.settings = QSettings("acer-battery-control", "BatteryControl")
        self.module_path = self.settings.value("module_path", "/etc/acer-battery-control-gui/", type=str)

        self.initUI()
        self.restoreLocation()

    def initUI(self):
        self.setWindowTitle("Acer Battery Control")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.setMinimumSize(400, 300)
        qr = self.frameGeometry()
        cp = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        
        # Module Path Group
        path_group = QGroupBox("Module Path")
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(self.module_path)
        self.path_input.textChanged[str].connect(self.save_module_path)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_module) 
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        path_group.setLayout(path_layout)


        # Button Health mode Group
        button_group = QGroupBox("Limit Charge 80%")
        button_group_layout = QVBoxLayout()
        self.toggle_button = QPushButton("On")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_health_mode)
        self.toggle_button.setStyleSheet("QPushButton { padding: 5px; }"
                                       "QPushButton:checked { background-color: #77dd77; }") # Green when checked
        button_group_layout.addWidget(self.toggle_button)
        button_group.setLayout(button_group_layout)

        # Button Calibration mode Group
        calib_group = QGroupBox("Calibration mode")
        calib_group_layout = QVBoxLayout()
        self.txt_note = QLabel("Before attempting the battery calibration\nConnect your laptop to a power supply")
        # style text color red
        self.txt_note.setStyleSheet("QLabel { color: red; }")
        self.toggle_button_2 = QPushButton("On")
        self.toggle_button_2.setCheckable(True)
        self.toggle_button_2.clicked.connect(self.toggle_calibration_mode)
        self.toggle_button_2.setStyleSheet("QPushButton { padding: 5px; }"
                                         "QPushButton:checked { background-color: #dd7777; }") # Red when checked
        calib_group_layout.addWidget(self.txt_note)
        calib_group_layout.addWidget(self.toggle_button_2)
        calib_group.setLayout(calib_group_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(path_group)  # Add the group box
        main_layout.addWidget(button_group)
        main_layout.addWidget(calib_group)  # Add the group box
        main_layout.addStretch(1)  # Add some space at the bottom
        self.setLayout(main_layout)


        self.update_toggle_state()

    def browse_module(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Select Module", "", "Kernel Modules (*.ko)", options=options)
        if filename:
            self.path_input.setText(os.path.dirname(filename)) # Set only the directory
            self.save_module_path(os.path.dirname(filename))
    def save_module_path(self, text):
        self.module_path = text
        self.settings.setValue("module_path", self.module_path)
        self.update_toggle_state()  # refresh after changing path

    def update_toggle_state(self):
        try:
            with open("/sys/bus/wmi/drivers/acer-wmi-battery/health_mode", "r") as f:
                value = int(f.read().strip())
                self.toggle_button.setChecked(value == 1)  # Set checked state
                self.toggle_button.setText("On" if value == 1 else "Off")
            with open("/sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode", "r") as f:
                value = int(f.read().strip())
                self.toggle_button_2.setChecked(value == 1)  # Set checked state
                self.toggle_button_2.setText("On" if value == 1 else "Off")
        except FileNotFoundError:
            self.load_module()  # Attempt to load the module if file not found
            self.update_toggle_state()  # Retry updating after loading

        except Exception as e:  # Catch other potential errors
            print(f"Error reading health_mode: {e}")

    def toggle_health_mode(self):
        value = 1 if self.toggle_button.isChecked() else 0
        command = f"echo {value} | pkexec tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode"
        try:
            subprocess.run(command, shell=True, check=True)
            self.update_toggle_state()
        except subprocess.CalledProcessError as e:
            print(f"Error toggling health mode: {e}")

    def toggle_calibration_mode(self):
        value = 1 if self.toggle_button_2.isChecked() else 0
        command = f"echo {value} | pkexec tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode"
        try:
            subprocess.run(command, shell=True, check=True)
            self.update_toggle_state()
        except subprocess.CalledProcessError as e:
            print(f"Error toggling calibration mode: {e}")

    def load_module(self):
        if self.module_path:
            command = f"pkexec make && pkexec insmod {self.module_path}/acer-wmi-battery.ko"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error loading module: {e}")

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())  # Save window geometry
        super().closeEvent(event)

    def restoreLocation(self):
        geometry = self.settings.value("geometry", QByteArray())  # type: QByteArray
        if geometry.size() > 0:  # Check if geometry data exists
            self.restoreGeometry(geometry)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatteryControl()
    ex.show()
    sys.exit(app.exec_())

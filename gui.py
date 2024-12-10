#!/usr/bin/env python3
import os
import subprocess
import sys
import socket

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

        # Check Connection Group
        check_group = QGroupBox("Check Connection")
        check_group_layout = QVBoxLayout()
        self.check_button = QPushButton("Check Connection")
        self.check_button.clicked.connect(self.check_connection)
        check_group_layout.addWidget(self.check_button)
        check_group.setLayout(check_group_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(path_group)  # Add the group box
        main_layout.addWidget(button_group)
        main_layout.addWidget(calib_group)  # Add the group box
        main_layout.addWidget(check_group)
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
            print("Module not loaded. Please load the module first.")  # or show a message in the UI
            #  Remove the recursive call here
        except Exception as e:
            print(f"Error reading modes: {e}")

    def toggle_health_mode(self):
        command = "health_mode_on" if self.toggle_button.isChecked() else "health_mode_off"
        self.send_command(command)

    def toggle_calibration_mode(self):
        command = "calibration_mode_on" if self.toggle_button_2.isChecked() else "calibration_mode_off"
        self.send_command(command)

    def load_module(self):
        if self.module_path:
            try:
                command = f"make_and_insmod {self.module_path}"  # Send combined command
                response = self.send_command(command)
                print(response) # Print both make and insmod output
            except subprocess.CalledProcessError as e:
               print(f"Error loading module: {e}")
        else: # if no errors, call update_toggle_state
               self.update_toggle_state() # Call after module is loaded

    def send_command(self, command):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock_path = "/tmp/acer-battery-control.sock"
        try:
            sock.connect(sock_path)
            sock.sendall(command.encode("utf-8"))
            response = sock.recv(4096).decode("utf-8") # Receive response from backend
            sock.close()
            self.update_toggle_state()
            return response
        except Exception as e:
            print(f"Error communicating with backend: {e}")
            return "Error"

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())  # Save window geometry
        super().closeEvent(event)

    def restoreLocation(self):
        geometry = self.settings.value("geometry", QByteArray())  # type: QByteArray
        if geometry.size() > 0:  # Check if geometry data exists
            self.restoreGeometry(geometry)

    def check_connection(self):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock_path = "/tmp/acer-battery-control.sock"
            sock.connect(sock_path)
            sock.sendall(b"ping")
            response = sock.recv(4096).decode("utf-8")
            sock.close()
            if response == "pong":
                print("Connection successful!")
                self.check_button.setStyleSheet("QPushButton { background-color: #77dd77; }")  # Green
                self.check_button.setText("Connection successful!")
            else:
                print("Unexpected response:", response)
                self.check_button.setStyleSheet("QPushButton { background-color: #dd7777; }")  # Red
                self.check_button.setText("Connection failed!")
        except Exception as e:
            print(f"Error connecting to backend: {e}")
            self.check_button.setStyleSheet("QPushButton { background-color: #dd7777; }")  # Red
            self.check_button.setText("Connection failed!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatteryControl()
    ex.show()
    sys.exit(app.exec_())

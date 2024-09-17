import sys
import serial
import threading
from collections import deque
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QListWidget, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QThread, Signal

import serial_reader as sr
import serial_writer as sw
from auto_port_detection import find_device_port


class SerialWorker(QThread):
    data_received = Signal(str)

    def __init__(self, serial_conn, parent=None):
        super().__init__(parent)
        self.serial_conn = serial_conn
        self.reader = sr.SerialReader(self.serial_conn)
        self.running = True

    def run(self):
        while self.running:
            try:
                data = next(self.reader.read_and_store_serial_data())
                if data:
                    self.data_received.emit(data)
            except Exception as e:
                print(f"Error: {e}")
                self.stop()

    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up serial connection
        self.port = find_device_port()
        self.serial_conn = serial.Serial(port=self.port, baudrate=38400, timeout=1)
        self.serial_worker = SerialWorker(self.serial_conn)
        self.serial_worker.data_received.connect(self.update_data_output)

        # Define UI components
        self.data_list_view = QListWidget()
        self.read_button = QPushButton("Read Data")
        self.write_input = QLineEdit()
        self.write_button = QPushButton("Send Data")

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.data_list_view)
        layout.addWidget(self.read_button)
        layout.addWidget(self.write_input)
        layout.addWidget(self.write_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect signals
        self.read_button.clicked.connect(self.start_reading)
        self.write_button.clicked.connect(self.send_data)

    def start_reading(self):
        """Start reading from the serial port."""
        if not self.serial_worker.isRunning():
            self.serial_worker.start()

    def stop_reading(self):
        """Stop reading from the serial port."""
        if self.serial_worker.isRunning():
            self.serial_worker.stop()

    def send_data(self):
        """Send data to the serial port."""
        data = self.write_input.text()
        if data:
            writer = sw.SerialWriter(self.serial_conn)
            writer.send_data_to_serial(data)

    def update_data_output(self, data):
        """Update the UI with new data."""
        self.data_list_view.addItem(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.setWindowTitle("Serial Data Viewer")
    window.show()
    sys.exit(app.exec())

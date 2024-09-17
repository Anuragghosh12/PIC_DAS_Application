import flet as ft
from flet import colors
import serial
import threading
from collections import deque
import serial_reader as sr
import serial_writer as sw
from auto_port_detection import find_device_port

# Define your serial communication handler
class SerialHandler:
    def __init__(self, port):
        self.serial_conn = serial.Serial(port=port, baudrate=38400, timeout=1)
        self.reader = sr.SerialReader(self.serial_conn)
        self.writer = sw.SerialWriter(self.serial_conn)
        self.reading = False
        self.data_buffer = deque(maxlen=1500)
        self.data_update_callback = None

    def start_reading(self):
        """Start reading from the serial port using a separate thread."""
        if not self.reading:
            self.reading = True
            self.read_thread = threading.Thread(target=self.read_data_thread)
            self.read_thread.daemon = True
            self.read_thread.start()

    def read_data_thread(self):
        """Thread to handle reading from the serial port."""
        while self.reading:
            try:
                data = next(self.reader.read_and_store_serial_data())  # Simulating data from the serial port
                if data:
                    self.data_buffer.append(data)
                    if self.data_update_callback:
                        self.data_update_callback(data)
            except Exception as e:
                print(f"Error: {e}")
                self.stop_reading()

    def stop_reading(self):
        """Stop reading from the serial port."""
        self.reading = False

    def send_data(self, data):
        """Send data to the serial port."""
        if self.writer:
            self.writer.send_data_to_serial(data)

    def set_data_update_callback(self, callback):
        """Set the callback function to update UI."""
        self.data_update_callback = callback

def main(page: ft.Page):
    # Set up serial connection
    port = find_device_port()
    serial_handler = SerialHandler(port)

    # Define UI components
    data_list_view = ft.ListView(
        expand=True,
        spacing=10,
        height=page.height * 0.6,  # 60% of screen height
        padding=10,
    )

    # Queue for thread-safe UI updates
    data_update_queue = deque()

    # Function to update UI with data
    def update_data_output(data=None):
        if data:
            data_update_queue.append(data)

        while data_update_queue:
            new_data_items = []
            while data_update_queue:
                data_item = data_update_queue.popleft()
                new_data_items.append(ft.Text(str(data_item), size=16))

            if new_data_items:
                data_list_view.controls.extend(new_data_items)
                page.update()

    # Set the data update callback
    serial_handler.set_data_update_callback(update_data_output)

    # UI elements
    read_button = ft.ElevatedButton(text="Read Data", on_click=lambda e: serial_handler.start_reading())
    write_input = ft.TextField(hint_text="Enter data to send", expand=True)
    write_button = ft.ElevatedButton(text="Send Data", on_click=lambda e: serial_handler.send_data(write_input.value))

    # Set up UI layout
    page.add(
        ft.Column(
            controls=[
                data_list_view,
                write_input,
                ft.Row(
                    controls=[read_button, write_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.theme = ft.Theme(color_scheme_seed='orange')
    page.update()
    # Center the window on the screen
    page.window_center()

if __name__ == "__main__":
    ft.app(main)

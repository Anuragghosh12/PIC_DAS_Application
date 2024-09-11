import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import serial
import serial_reader as sr
import serial_writer as sw
from auto_port_detection import find_device_port
import threading
from collections import deque
import time

kivy.require('2.1.0')

class MyApp(App):
    def build(self):
        self.serial_conn = None
        self.reader = None
        self.writer = None
        self.reading = False

        # Buffer to store incoming data, with max length of 100 samples
        self.data_buffer = deque(maxlen=100)

        layout = BoxLayout(orientation='vertical')

        # ScrollView to allow scrolling
        scroll_view = ScrollView(size_hint=(1, 0.7))
        layout.add_widget(scroll_view)

        # TextInput for showing received data
        self.data_output = TextInput(text='No data received yet.', readonly=True, size_hint_y=None, height=400, multiline=True)
        scroll_view.add_widget(self.data_output)

        # Button to start reading data
        self.read_button = Button(text='Read Data', size_hint_y=0.1)
        self.read_button.bind(on_press=self.start_reading)
        layout.add_widget(self.read_button)

        # TextInput for user to enter data to send
        self.write_input = TextInput(hint_text='Enter data to send', size_hint_y=0.1)
        layout.add_widget(self.write_input)

        # Button to send data
        self.write_button = Button(text='Send Data', size_hint_y=0.1)
        self.write_button.bind(on_press=self.send_data)
        layout.add_widget(self.write_button)

        # Button to quit the app
        self.quit_button = Button(text='Quit', size_hint_y=0.1)
        self.quit_button.bind(on_press=self.stop_app)
        layout.add_widget(self.quit_button)

        self.reset_serial_connection()
        return layout

    def start_reading(self, instance):
        """Start reading from the serial port using a separate thread."""
        if self.serial_conn:
            if not self.reading:
                self.reading = True
                # Start a new thread for reading data
                self.read_thread = threading.Thread(target=self.read_data_thread)
                self.read_thread.daemon = True  # Daemonize thread to exit when main thread exits
                self.read_thread.start()
                # Update the UI every 0.25 seconds to prevent UI overload
                self.ui_update_event = Clock.schedule_interval(self.update_ui, 0.25)
        else:
            self.data_output.text = "Serial connection not established."
            self.reset_serial_connection()

    def read_data_thread(self):
        """Thread to handle reading from the serial port."""
        while self.reading:
            try:
                data = next(self.reader.read_and_store_serial_data())
                if not "Stopped" in data:
                    # Add data to the buffer (deque)
                    self.data_buffer.append(data)
                else:
                    self.stop_reading()
                    Clock.schedule_once(lambda dt: self.reset_serial_connection(), 0)
            except StopIteration:
                pass  # No new data, continue
            except Exception as e:
                Clock.schedule_once(lambda dt: self.data_output.text == f"Error reading data: {e}", 0)
                self.stop_reading()
                Clock.schedule_once(lambda dt: self.reset_serial_connection(), 0)

            # Throttle reading to approximately 20 samples per second (50 ms)
            time.sleep(0.05)

    def stop_reading(self):
        """Stop reading from the serial port."""
        self.reading = False
        if hasattr(self, 'ui_update_event'):
            self.ui_update_event.cancel()

    def send_data(self, instance):
        """Send data to the serial port."""
        if self.writer:
            data = self.write_input.text
            if data.lower() != 'clear':
                self.writer.send_data_to_serial(data)
            else:
                self.update_data_output('clear')
            self.write_input.text = ''  # Clear the input field

    def stop_app(self, instance):
        """Stop the app and close the serial connection."""
        self.stop_reading()  # Ensure reading is stopped before closing the connection
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        App.get_running_app().stop()

    def reset_serial_connection(self):
        """Reset the serial connection."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        port = find_device_port()
        if port:
            try:
                self.serial_conn = serial.Serial(port=port, baudrate=38400, timeout=1)
                self.reader = sr.SerialReader(self.serial_conn)
                self.writer = sw.SerialWriter(self.serial_conn)
                self.data_output.text += "\nConnection established. Awaiting data..."
                self.data_output._scroll_y = 0  # Scroll to the bottom
            except serial.SerialException as e:
                print(f"Error accessing serial port: ")

    def update_ui(self, dt):
        """Update the data output with new data from the buffer."""
        while self.data_buffer:
            new_data = self.data_buffer.popleft()  # Get the latest data
            self.update_data_output(new_data)

    def update_data_output(self, new_data):
        """Update the data output with new data in real-time."""
        if new_data != 'clear':
            formatted_data = ' '.join(map(str, new_data))  # Format the data into a string
            self.data_output.text += f'\n{formatted_data}'  # Append new data to the text input
            self.data_output._scroll_y = 0  # Scroll to the bottom
        else:
            self.data_output.text = ""  # Clear the screen

if __name__ == "__main__":
    MyApp().run()

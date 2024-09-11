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

kivy.require('2.1.0')

class MyApp(App):
    def build(self):
        self.serial_conn = None
        self.reader = None
        self.writer = None
        self.reading = False

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
        """Start reading from the serial port."""
        if self.serial_conn:
            if not self.reading:
                self.reading = True
                # Schedule the reading to happen continuously every 0.1 seconds
                self.read_event = Clock.schedule_interval(self.read_and_store_data, 0.01)
        else:
            self.data_output.text = "Serial connection not established."
            self.reset_serial_connection()

    def stop_reading(self):
        """Stop reading from the serial port."""
        if self.reading:
            self.reading = False
            if hasattr(self, 'read_event'):
                self.read_event.cancel()
                del self.read_event

    def read_and_store_data(self, dt):
        """Fetch one line of serial data and update the UI."""
        if self.reader:
            try:
                # Read data using the generator
                try:
                    data = next(self.reader.read_and_store_serial_data())
                    if not "Stopped" in data:
                        self.update_data_output(data)
                    else:
                        self.stop_reading()
                        self.reset_serial_connection()
                except StopIteration:
                    pass  # Continue to the next cycle
            except Exception as e:
                self.data_output.text = f"Error reading data: {e}"
                self.stop_reading()
                self.reset_serial_connection()

    def send_data(self, instance):
        """Send data to the serial port."""
        if self.writer:
            data = self.write_input.text
            self.writer.send_data_to_serial(data)
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
                self.data_output.text = "Connection established. Awaiting data..."
            except serial.SerialException as e:
                print(f"Error accessing serial port: {e}")

    def update_data_output(self, new_data):
        """Update the data output with new data in real-time."""
        formatted_data = ' '.join(map(str, new_data))  # Format the data into a string
        self.data_output.text += f'\n{formatted_data}'  # Append new data to the text input
        self.data_output._scroll_y = 0  # Scroll to the bottom

if __name__ == "__main__":
    MyApp().run()

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import serial
import serial_reader as sr
import serial_writer as sw
from auto_port_detection import find_device_port
import threading

kivy.require('2.1.0')

class MyApp(App):
    def build(self):
        self.serial_conn = None
        self.reader = None
        self.writer = None
        self.data = []

        layout = BoxLayout(orientation='vertical')

        self.data_label = Label(text='No data received yet.')
        layout.add_widget(self.data_label)

        self.read_button = Button(text='Read Data')
        self.read_button.bind(on_press=self.start_reading)
        layout.add_widget(self.read_button)

        self.write_input = TextInput(hint_text='Enter data to send', size_hint_y=None, height=40)
        layout.add_widget(self.write_input)

        self.write_button = Button(text='Send Data')
        self.write_button.bind(on_press=self.send_data)
        layout.add_widget(self.write_button)

        self.quit_button = Button(text='Quit')
        self.quit_button.bind(on_press=self.stop_app)
        layout.add_widget(self.quit_button)

        return layout

    def start_reading(self, instance):
        """Start reading from the serial port in a separate thread"""
        if self.serial_conn:
            self.reader_thread = threading.Thread(target=self.read_and_store_data)
            self.reader_thread.start()
        else:
            self.data_label.text = "Serial connection not established."
            self.reset_serial_connection()

    def read_and_store_data(self):
        """Read and display serial data"""
        if self.reader:
            reset_detected = self.reader.read_and_store_serial_data()
            if reset_detected:
                self.data_label.text = "Restarting Program"
                self.reset_serial_connection()

    def send_data(self, instance):
        """Send data to the serial port"""
        if self.writer:
            data = self.write_input.text
            self.writer.send_data_to_serial(data)
            self.write_input.text = ''  # Clear the input field

    def stop_app(self, instance):
        """Stop the app and close the serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        App.get_running_app().stop()

    def reset_serial_connection(self):
        """Reset the serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        port = find_device_port()
        if port:
            try:
                self.serial_conn = serial.Serial(port=port, baudrate=38400, timeout=1)
                self.reader = sr.SerialReader(self.serial_conn)
                self.writer = sw.SerialWriter(self.serial_conn)
            except serial.SerialException as e:
                print(f"Error accessing serial port: {e}")

    def update_data_label(self, new_data):
        """Update the data label with new data"""
        self.data_label.text = '\n'.join(new_data)

    def read_and_store_data(self):
        """Read and display serial data"""
        if self.reader:
            while True:
                reset_detected = self.reader.read_and_store_serial_data()
                if reset_detected:
                    self.data_label.text = "Restarting Program"
                    self.reset_serial_connection()
                else:
                    # Fetch data from buffer and update the label
                    if self.reader.buffer:
                        new_data = [str(item) for item in self.reader.buffer[-1]]  # Show the most recent line of data
                        self.update_data_label(new_data)
                #time.sleep(0.1)  # Small delay to avoid excessive CPU usage

if __name__ == "__main__":
    MyApp().run()

import time
import serial


class SerialWriter:
    def __init__(self, port, baudrate=38400, timeout=1):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def send_data_to_serial(self,data):
        """Send data to the serial port to control the device."""
        try:
            self.ser.write(data.encode('utf-8'))
            print(f"Sent data: {data}")
            time.sleep(0.1)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.ser.close()

import time
import serial
import openpyxl
from openpyxl import Workbook

BUFFER_SIZE = 200  # Number of lines to buffer


class SerialReader:
    """Initializing the serial port and workbook"""

    def __init__(self, serial_conn, num_channels=4, retry_attempts=3, retry_delay=0.00001):
        self.ser = serial_conn
        self.num_channels = num_channels
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.buffer = []
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["Serial Number", "Channel 0", "Channel 1", "Channel 2", "Channel 3"])

    def is_valid_data(self, data):
        """Check if the data is valid and corresponds to the expected format."""
        try:
            parts = data.split()
            if len(parts) < (self.num_channels + 1):  # Total channels + serial number
                raise ValueError("Incomplete Data Received")

            # Attempt to convert each value to float or handle underscores as None
            parsed_data = [None if '_' in part else part for part in parts]
            parsed_data = [float(value) if value and value != 'None' else None for value in parsed_data]
            return parsed_data
        except (ValueError, IndexError) as e:
            print(f"Invalid Serial Data: {data}.....Error: {e}")
            return None

    def read_and_store_serial_data(self):
        """Read data, buffer it, and process in chunks."""
        try:
            while True:
                # Check for incoming serial data
                if self.ser.in_waiting > 0:
                    serial_data = self.ser.readline().decode('utf-8', errors='ignore').strip()

                    if "battery" in serial_data.lower():
                        print(f"{serial_data}")
                        print("Reset detected, stopping data capture.")
                        return True  # Indicate a reset detected

                    parsed_data = self.is_valid_data(serial_data)

                    if parsed_data:
                        # Buffer the data
                        self.buffer.append(parsed_data)

                        # Process the buffer if it is full
                        if len(self.buffer) >= BUFFER_SIZE:
                            self._process_buffer()

                        print(f"Buffered Data: {parsed_data}")

                    else:
                        print(f"Skipping invalid data: {serial_data}")

                # Small delay to avoid excessive CPU usage
                time.sleep(0.01)

        except Exception as e:
            print(f"Data capture stopped due to error: {e}")
            return True

        finally:
            # Process any remaining data in the buffer
            if self.buffer:
                self._process_buffer()

    def _process_buffer(self):
        """Process and clear the buffer."""
        for data in self.buffer:
            self.ws.append(data)
            print(f"Processing Data: {data}")

        self.wb.save("Serial_data.xlsx")
        self.buffer = []  # Clear the buffer


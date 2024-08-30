import time
import serial
import openpyxl
from openpyxl import Workbook


class SerialReader:
    """Initializing the serial port and workbook"""
    def __init__(self, port, baudrate=38400, timeout=1):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["Serial Number", "Channel 0", "Channel 1", "Channel 2", "Channel 3"])

    def is_valid_data(self, data):
        """Check if the data is valid and corresponds to the expected format."""
        try:
            # Attempt to convert each value to float or handle underscores as None
            [None if value.strip('_') == '' else float(value) for value in data.split()]
            return True
        except ValueError:
            return False

    def convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return None

    def read_and_store_serial_data(self):
        try:
            while True:
                if self.ser.in_waiting > 0:
                    try:
                        serial_data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    except UnicodeDecodeError as e:
                        print(f"Unicode Decoder Error {e}")
                        continue
                    if "battery" in serial_data.lower():
                        print(f"{serial_data}")
                        print("Reset detected, stopping data capture.")
                        continue

                    # Handle header row (usually starting with "Serial Number" or similar)
                    # if serial_data.lower().startswith("serial number"):
                    #     header = serial_data.split()
                    #     ws.append(header)
                    #     wb.save("Serial_data.xlsx")
                    #     print(f"Header: {header}")
                    #     continue

                    # Process data row if it's valid
                    if self.is_valid_data(serial_data):
                        data = serial_data.split()

                        # Replace underscores with None for closed channels
                        data = [self.convert_to_float(value) for value in data]
                        # data = [None if value.strip('_') == '' else value for value in data]

                        self.ws.append(data)
                        self.wb.save("Serial_data.xlsx")
                        print(f"Data: {data}")
                    else:
                        print(f"Invalid serial data: {serial_data}")
                        self.read_and_store_serial_data()

        except Exception as e:
            print(f"Data capture stopped due to error: {e}")

        finally:
            self.ser.close()
            print("Serial connection closed.")

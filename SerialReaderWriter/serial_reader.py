import subprocess
import time
import serial
import openpyxl
from openpyxl import Workbook


class SerialReader:
    """Initializing the serial port and workbook"""
    def __init__(self, serial_conn, num_channels=4, retry_attempts=3, retry_delay=0.00001):
        self.ser = serial_conn
        self.num_channels=num_channels
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["Serial Number", "Channel 0", "Channel 1", "Channel 2", "Channel 3"])

    def is_valid_data(self, data):
        """Check if the data is valid and corresponds to the expected format."""
        try:
            parts = data.split()
            if(len(parts) < (self.num_channels+1)): #total channels + serial number
                raise ValueError("Incomplete Data Received")
            # Attempt to convert each value to float or handle underscores as None
            #[None if value.strip('_') == '' else float(value) for value in data.split()]
            parsed_data = [None if '_' in part else part for part in parts]

            parsed_data = [float(value) if value and value != 'None' else None for value in parsed_data]
            return parsed_data
        except (ValueError,IndexError) as e:
            print(f"Invalid Serial Data:{data}.....Error: {e}")
            return None

    def convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return None

    def read_and_store_serial_data(self):
        try:
            retry_count = 0
            while True:
                #Wait for the serial input
                while self.ser.in_waiting>0:
                    #time.sleep(0.05) #Adding a short delay in between
                    try:
                        serial_data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    except UnicodeDecodeError as e:
                        print(f"Unicode Decoder Error {e}")
                        continue
                    if "battery" in serial_data.lower():
                        print(f"{serial_data}")
                        print("Reset detected, stopping data capture.")
                        return True
                        #continue


                    parsed_data = self.is_valid_data(serial_data)


                    # Handle header row (usually starting with "Serial Number" or similar)
                    # if serial_data.lower().startswith("serial number"):
                    #     header = serial_data.split()
                    #     ws.append(header)
                    #     wb.save("Serial_data.xlsx")
                    #     print(f"Header: {header}")
                    #     continue



                    # Process data row if it's valid
                    if parsed_data:


                        self.ws.append(parsed_data)
                        self.wb.save("Serial_data.xlsx")
                        print(f"Data: {parsed_data}")
                        retry_count = 0
                    else:
                        # print(f"Invalid serial data, retrying....{retry_count+1}/{self.retry_attempts}")
                        # retry_count = 1
                        # if retry_count>=self.retry_attempts:
                        #     print("Skipping line")
                        #     retry_count=0
                        if "not responding" in serial_data.lower():
                            return True
                        #self.read_and_store_serial_data()
                        #time.sleep(self.retry_delay)#wait before retrying

        except Exception as e:
            print(f"Data capture stopped due to error: {e}")
            return True

        finally:
            return True

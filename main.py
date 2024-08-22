import time
import serial
import openpyxl
from openpyxl import Workbook

# Setup Serial Connection using predefined baudrate
ser = serial.Serial(port='COM5', baudrate=38400, timeout=1)

# Create a new workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Give headers to the Excel sheet
ws.append(["Serial Number", "Channel 0", "Channel 1", "Channel 2", "Channel 3"])


def is_valid_data(data):
    """Check if the data is valid and corresponds to the expected format."""
    try:
        # Attempt to convert each value to float or handle underscores as None
        [None if value.strip('_') == '' else float(value) for value in data.split()]
        return True
    except ValueError:
        return False
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return None


def read_and_store_serial_data():
    try:
        while True:
            if ser.in_waiting > 0:
                serial_data = ser.readline().decode('utf-8').strip()

                if "reset" in serial_data.lower():
                    print("Reset detected, stopping data capture.")
                    break

                # Handle header row (usually starting with "Serial Number" or similar)
                if serial_data.lower().startswith("serial number"):
                    header = serial_data.split()
                    ws.append(header)
                    wb.save("Serial_data.xlsx")
                    print(f"Header: {header}")
                    continue

                # Process data row if it's valid
                if is_valid_data(serial_data):
                    data = serial_data.split()

                    # Replace underscores with None for closed channels
                    data=[convert_to_float(value) for value in data]
                   # data = [None if value.strip('_') == '' else value for value in data]

                    ws.append(data)
                    wb.save("Serial_data.xlsx")
                    print(f"Data: {data}")
                else:
                    print(f"Invalid serial data: {serial_data}")

    except Exception as e:
        print(f"Data capture stopped due to error: {e}")

    finally:
        ser.close()
        print("Serial connection closed.")


def send_data_to_serial(data):
    """Send data to the serial port to control the device."""
    try:
        ser.write(data.encode('utf-8'))
        print(f"Sent data: {data}")
        time.sleep(0.1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()


# Run the function to read and store serial data
read_and_store_serial_data()

# Example: Send data to the device
# send_data_to_serial("Your command here")

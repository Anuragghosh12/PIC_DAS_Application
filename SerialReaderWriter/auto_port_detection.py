import serial
import serial.tools.list_ports

def find_device_port(baudrate=38400, timeout=1):
    available_ports = serial.tools.list_ports.comports()
    for port in available_ports:
        try:
            ser = serial.Serial(port.device, baudrate=baudrate, timeout=timeout)
            ser.close()  # Immediately close the port after a successful open
            print(f"Device found on port: {port.device}")
            return port.device
        except (OSError, serial.SerialException):
            pass
    return None

# Usage example
if __name__ == "__main__":
    device_port = find_device_port()
    if device_port:
        print(f"Auto-detected port: {device_port}")
    else:
        print("No device found on any port.")

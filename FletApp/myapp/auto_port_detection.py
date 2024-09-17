import serial
import serial.tools.list_ports

def find_device_port(baudrate=38400, timeout=1):
    serial_ports = []
    available_ports = serial.tools.list_ports.comports()
    for port in available_ports:
        try:
            port_name = port.device
            with serial.Serial(port.device, baudrate=baudrate, timeout=timeout) as ser:
                ser.close()  # Immediately close the port after a successful open
            serial_ports.append(port_name)
            print(f"Device found on port: {port_name}")

        except serial.SerialException as e:
            print(f"Could not open port{port_name}: {e}")
        except PermissionError :
            print(f"Permission denied for port{port_name}")

    if serial_ports:
        preferred_ports=[port for port in serial_ports if port not in ['COM3', 'COM1']]
        if preferred_ports:
            print(f"Connected to port {preferred_ports[0]}")
            return preferred_ports[0]
        if 'COM3' in serial_ports:
            print(f"Connected to port COM3")
            return 'COM3'
        if 'COM1' in serial_ports:
            print(f"Connected to port COM1")
            return 'COM1'
    else:
        print(f"No available ports found")
        return None


# # Usage example
# if __name__ == "__main__":
#     device_port = find_device_port()
#     if device_port:
#         print(f"Auto-detected port: {device_port}")
#     else:
#         print("No device found on any port.")

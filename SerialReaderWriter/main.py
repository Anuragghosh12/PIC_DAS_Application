import serial_reader as sr
import serial_writer as sw
import serial
from SerialReaderWriter.auto_port_detection import find_device_port


def main():
    port ="COM5" #find_device_port()

    if not port:
        print("No device connected, exiting the application")
    try:
        serial_conn = serial.Serial(port=port, baudrate=38400, timeout=1)
        #Instantiating the classes
        reader = sr.SerialReader(serial_conn)
        writer = sw.SerialWriter(serial_conn)

        while True:
            user_input = input("Enter r to read data and w to write data and q to quit: ").strip().lower()

            if user_input == 'r':
                reset_detected = reader.read_and_store_serial_data()
                if reset_detected:
                    print("Restarting Program")
            elif user_input == 'w':
                data = input('Enter data to send to serial: ')
                writer.send_data_to_serial(data)
            else:
                print('Exiting program.')
                break
    except serial.SerialException as e:
        print(f"Error accessing serial port: {e}")
    finally:
        #Close the serial port
        if serial_conn.is_open:
            serial_conn.close()
            print(f"Serial connection is closed")


if __name__=="__main__":
    main()

import serial_reader as sr
import serial_writer as sw
import auto_port_detection
from SerialReaderWriter.auto_port_detection import find_device_port


def main():
    port = find_device_port()

    if not port:
        print("No device connected, exiting the application")

    #Instantiating the classes
    reader = sr.SerialReader(port)
    writer = sw.SerialWriter(port)

    while True:
        user_input = input("Enter r to read data and w to write data and q to quit: ").strip().lower()

        if user_input == 'r':
            reader.read_and_store_serial_data()
        elif user_input == 'w':
            data = input('Enter data to send to serial: ')
            writer.send_data_to_serial(data)
        else:
            print('Exiting program.')
            break
if __name__=="__main__":
    main()

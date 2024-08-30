import serial_reader as sr
import serial_writer as sw



def main():
    port = "COM5"

    #Instantiating the classes
    reader = sr(port)
    writer = sw(port)

    while True:
        user_input = input("Enter r to read data and w to write data and q to quit: ").strip().lower()

        if user_input == 'r':
            reader.read_and_store
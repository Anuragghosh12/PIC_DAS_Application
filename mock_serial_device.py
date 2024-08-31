import time
import random
import sys

def generate_mock_data():
    while True:
        # Generate a random serial number
        serial_number = random.randint(1, 100)

        # Generate random values for each channel, with a chance to leave some channels blank
        channels = []
        for _ in range(4):
            if random.choice([True, False]):
                channels.append(f"{random.uniform(0, 100):.2f}".encode('utf-8'))  # Random float value
            else:
                channels.append("____")  # Simulating a closed channel with blank data

        # Format the data as it would be received from the device
        data_line = f"{serial_number} {channels[0]} {channels[1]} {channels[2]} {channels[3]}\n"
        sys.stdout.write(data_line)
        sys.stdout.flush()

        # Wait for a short period before sending the next line of data
        time.sleep(0.05)

if __name__ == "__main__":
    generate_mock_data()

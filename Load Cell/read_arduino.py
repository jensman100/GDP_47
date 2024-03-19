import serial
import csv
from datetime import datetime

ser = serial.Serial('COM4', 9600)  # Replace 'COM3' with the correct serial port

csv_file_path = 'weight_data.csv'

try:
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time', 'Weight (N)'])  # Header for the CSV file

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"{current_time}, {data}")
                csv_writer.writerow([current_time, data])

except KeyboardInterrupt:
    print("\nData collection stopped.")
    ser.close()

# Ensure the file is closed after the KeyboardInterrupt is handled
finally:
    csv_file.close()


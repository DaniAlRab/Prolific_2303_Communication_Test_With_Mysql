import os
import time
import subprocess
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': '1234',
      'database': 'tested_devices'
}


def find_devices():
    # Define the possible devices you are looking for
    device_list = ['/dev/ttyUSB0', '/dev/ttyUSB1']

    # Find all devices that are currently connected
    connected_devices = [device for device in device_list if os.path.exists(device)]

    return connected_devices

def execute_script():
    # Replace 'your_script.sh' with the full path to your .sh file
    script_path = "your_test_script.sh"    
    try:
        subprocess.run(["bash", script_path], check=True)
        print(f"\n{current_time} Script {script_path} executed successfully.")
        device_paths()      
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute the script: {e}")



def device_paths():
    device_paths = ["/dev/ttyUSB1", "/dev/ttyUSB0"]  # List both device paths
    for device_path in device_paths:
        serial_number = get_serial_number(device_path)
        if serial_number:
            save_serial_to_db(serial_number)
        else:
            print(f"No serial number found for {device_path} or command failed.")



# Function to get the serial number
def get_serial_number(device_path):
    try:
        # Run the command to get serial information
        result = subprocess.run(
            ['udevadm', 'info', f'--name={device_path}'],
            capture_output=True,
            text=True,
            check=True
        )
        # Filter the output for the serial number
        for line in result.stdout.splitlines():
            if "ID_SERIAL" in line:
                return line.split('=')[1]  # Extract the serial number
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
    return None

# Function to save the serial number to the database
def save_serial_to_db(serial_number):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tested_devices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                serial_number VARCHAR(255) UNIQUE NOT NULL,
                test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Insert the serial number into the database
        cursor.execute("INSERT INTO tested_devices (serial_number) VALUES (%s)", (serial_number,))
        connection.commit()
        print(f"Serial number '{serial_number}' saved successfully.")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    while True:
        # Get the current time for logging in the desired format
        current_time = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
        
        devices = find_devices()
        print(f"{current_time} Checking devices...")
        
        # Check if both devices are connected
        if '/dev/ttyUSB0' in devices and '/dev/ttyUSB1' in devices:
            print(f"{current_time} Both devices are connected. Executing script...\n")
            execute_script()
            break  # Exit the loop after running the script
        else:
            print(f"{current_time} Waiting for both devices to connect...")
        
        time.sleep(5)  # Wait for 5 seconds before checking again

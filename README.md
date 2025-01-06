# Prolific 2303 Communication Test with MySQL

## Project Overview

This Python script automates the process of testing Prolific 2303 devices connected to a system via USB ports and saves the results to a MySQL database. It continuously monitors the availability of specific devices and executes a test script once both devices are detected.

---

## Key Features

- **Device Detection:**

  - Monitors the availability of devices at `/dev/ttyUSB0` and `/dev/ttyUSB1`.
  - Continuously checks for device connections every 5 seconds.

- **Script Execution:**

  - Runs a specified shell script (`your_test_script.sh`) to perform tests when both devices are connected.

- **Serial Number Retrieval:**

  - Uses the `udevadm` command to retrieve the serial number of each detected device.

- **Database Integration:**

  - Connects to a MySQL database (`tested_devices`).
  - Creates a table if it does not already exist.
  - Saves the retrieved serial numbers along with the test timestamp.

---

## Workflow

1. **Device Monitoring:**
   - The script continuously monitors the presence of `/dev/ttyUSB0` and `/dev/ttyUSB1`.
2. **Script Execution:**
   - Once both devices are detected, it executes the shell script (`your_test_script.sh`).
3. **Serial Number Extraction:**
   - Retrieves serial numbers of both devices using the `udevadm` command.
4. **Database Logging:**
   - Saves the serial numbers and timestamps to a MySQL database.

---

## Requirements

- **Python Modules:**
  - `os`, `time`, `subprocess`, `datetime`
  - `mysql-connector-python`
- **MySQL Server:**
  - Database: `tested_devices`
  - User credentials with access rights.
- **Shell Script:**
  - Replace `your_test_script.sh` with the path to your actual script.

---

## Configuration

- **Database Settings:**
  Update the `db_config` dictionary with your MySQL credentials:
  ```python
  db_config = {
      'host': 'localhost',
      'user': 'user',
      'password': '1234',
      'database': 'tested_devices'
  }
  ```
- **Test Script Path:**
  Replace `your_test_script.sh` with the actual path to your shell script.

---

## Usage

1. Ensure both devices are connected.
2. Run the script:
   ```bash
   python3 script_name.py
   ```
3. Monitor logs for device detection and script execution status.
4. Check the database for saved test results.

---

## Notes

- The script terminates after successfully detecting devices and executing the test script.
- Logs include timestamps for easy debugging.
- Serial numbers are stored as unique entries to avoid duplication in the database.

---

## Example Log Output

```
[01-01-2025 12:00:00] Checking devices...
[01-01-2025 12:00:05] Both devices are connected. Executing script...
[01-01-2025 12:00:10] Script executed successfully.
Serial number '12345678' saved successfully.
```

---


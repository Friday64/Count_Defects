# Defect Counter App

The Defect Counter App is a simple defect tracking tool built with Python and Kivy. It enables users to record and track counts of different types of manufacturing defects and automatically saves data to a CSV file for persistence between sessions. Users can increment counts, reset all counts, and the app periodically saves the data to prevent loss in case of unexpected closures.

## Features

- **Defect Tracking**: Counts various types of defects with an easy-to-use interface.
- **Data Persistence**: Stores defect counts in a CSV file, automatically saved every 30 seconds.
- **Reset Functionality**: Provides a "Reset Counts" button to reset all defect counts to zero.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/defect-counter-app.git
    cd defect-counter-app

2. **Install dependencies: Ensure you have Python installed, then install Kivy**:

    ```bash
    pip install kivy
    Run the app:
    ```
    ```bash
    python defect_counter.py
    ```
## How to Use
1. Launch the app using python defect_counter.py.
2. Click on any defect button to increment its count.
3. View the current count displayed beside each defect.
4. Click "Reset Counts" to reset all counts to zero.
5. The app automatically saves all counts to a counts.csv file every 30 seconds, ensuring data is retained for future sessions.
## File Structure
1. defect_counter.py: The main application code.
2. counts.csv: The CSV file where defect counts are stored (created if it doesn't exist).
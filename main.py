import csv
import os
from typing import Self
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

class Defect_CounterApp(App):
    def build(self):
        self.layout = GridLayout(cols=2, rows=14, padding=10, spacing=10)
        self.selected_index = 0  # Initialize selected defect index
        self.defect_data = [
            {'name': 'Defective Solder'},
            {'name': 'Missing Components'},
            {'name': 'Wrong Parts'},
            {'name': 'Reversed Components'},
            {'name': 'Damaged Components'},
            {'name': 'Damaged PCB'},
            {'name': 'Loose Hardware'},
            {'name': 'Wrong Hardware'},
            {'name': 'Poor Workmanship'},
            {'name': 'Improperly Masked'},
            {'name': 'Improperly Cleaned'},
            {'name': 'Wiring Defects'}
        ]

        self.check_csv()
        self.load_counts()

        for i, data in enumerate(self.defect_data):
            btn = Button(text=data['name'], size_hint_y=None, height=44)
            # Capture the correct index using a default argument in the lambda function
            btn.bind(on_release=lambda btn, index=i: self.increment_count(index))  
            self.layout.add_widget(btn)
            if 'count' not in data:
                data['count'] = 0
            data['label'] = Label(text=str(data['count']), size_hint_y=None, height=44)
            self.layout.add_widget(data['label'])

        reset_button = Button(text='Reset Counts')
        reset_button.bind(on_release=self.reset_counts)
        self.layout.add_widget(reset_button)

        return self.layout

    def check_csv(self):
        """
        Checks if 'counts.csv' exists, and creates it if it doesn't.
        """
        if not os.path.exists('counts.csv'):
            try:
                with open('counts.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    # Write initial counts (all zeros)
                    writer.writerow([0] * len(self.defect_data)) 
                print("Created counts.csv file.")
            except Exception as e:
                print(f"Error creating counts.csv: {e}")

    def load_counts(self):
        """
        Loads defect counts from a CSV file when the app starts.
        """
        try:
            with open('counts.csv', 'r') as file:
                reader = csv.reader(file)
                row = next(reader, None)  # Read the first (and only) row, or None if file is empty
                if row is None:
                    # If file is empty, set counts to 0
                    for data in self.defect_data:
                        data['count'] = 0
                else:
                    # If file is not empty, load counts from file
                    for i, count in enumerate(row):
                        if i < len(self.defect_data):  # Ensure we don't go out of bounds
                            self.defect_data[i]['count'] = int(count)
        except FileNotFoundError:
            # If file doesn't exist, set counts to 0
            for data in self.defect_data:
                data['count'] = 0
        except Exception as e:
            print(f"Error loading counts: {e}")

    def increment_count(self, index):
        """
        Increments the count for the selected defect type.
        """
        if 'count' not in self.defect_data[index]:
            self.defect_data[index]['count'] = 0
        self.defect_data[index]['count'] += 1
        self.defect_data[index]['label'].text = str(self.defect_data[index]['count'])
        self.save_counts()

    def reset_counts(self, instance):
        """
        Resets all defect counts to zero.
        """
        for data in self.defect_data:
            data['count'] = 0
            data['label'].text = str(data['count'])
        self.save_counts()

    def save_counts(self):
        """
        Saves the defect counts to a CSV file.
        """
        try:
            with open('counts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # Write counts to file
                writer.writerow([data['count'] for data in self.defect_data])
        except Exception as e:
            print(f"Error saving counts: {e}")

if __name__ == '__main__':
    Defect_CounterApp().run()
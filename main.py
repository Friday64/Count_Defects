import csv
import os
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
            {'name': 'Defective Solder', 'count': 0},
            {'name': 'Missing Components', 'count': 0},
            {'name': 'Wrong Parts', 'count': 0},
            {'name': 'Reversed Components', 'count': 0},
            {'name': 'Damaged Components', 'count': 0},
            {'name': 'Damaged PCB', 'count': 0},
            {'name': 'Loose Hardware', 'count': 0},
            {'name': 'Wrong Hardware', 'count': 0},
            {'name': 'Poor Workmanship', 'count': 0},
            {'name': 'Improperly Masked', 'count': 0},
            {'name': 'Improperly Cleaned', 'count': 0},
            {'name': 'Wiring Defects', 'count': 0}
        ]

        # Create buttons and labels, and store label references
        for i, data in enumerate(self.defect_data):
            btn = Button(text=data['name'], size_hint_y=None, height=44)
            # Capture the correct index using a default argument in the lambda function
            btn.bind(on_release=lambda btn, index=i: self.increment_count(index))  
            self.layout.add_widget(btn)
            data['label'] = Label(text=str(data['count']), size_hint_y=None, height=44)
            self.layout.add_widget(data['label'])


        reset_button = Button(text='Reset Counts')
        reset_button.bind(on_release=self.reset_counts)
        self.layout.add_widget(reset_button)

        self.load_counts()  # Load counts from CSV
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

    def increment_count(self, index):
        """
        Increments the count for the selected defect type.
        """
        print(f"Incrementing count for index: {index}")  # Print the index for debugging
        self.defect_data[index]['count'] += 1
        self.defect_data[index]['label'].text = str(self.defect_data[index]['count'])
        self.save_counts()

    def reset_all_counts(self, instance):
        """  when Reset Counts is clicked, opens a window with yes or no buttons, then reset
            the counts and only reset all counts if user confirms yes on the dialog window button, if no is clicked, closes the window and do nothing
        """
        popup = Popup(title='Reset All Counts', content=Label(text='Are you sure you want to reset all counts?'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()
        yes = Button(text='Yes')
        no = Button(text='No')
        yes.bind(on_press=lambda instance: self.reset_counts(instance))
        no.bind(on_press=lambda instance: popup.dismiss())
        popup.content.add_widget(yes)
        popup.content.add_widget(no)

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
                writer.writerow([data['count'] for data in self.defect_data])
        except Exception as e:
            print(f"Error saving counts: {e}")

    def load_counts(self):
        """
        Loads defect counts from a CSV file when the app starts.
        """
        try:
            with open('counts.csv', 'r') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i < len(self.defect_data):  # Ensure we don't go out of bounds
                        self.defect_data[i]['count'] = int(row[i])
                        self.defect_data[i]['label'].text = str(self.defect_data[i]['count'])
        except FileNotFoundError:
            print("Counts file not found. Starting with default counts.")
        except Exception as e:
            print(f"Error loading counts: {e}")

    def start_window(self):
        """
        Starts the Kivy window and runs the application.
        """
        self.run()

    def stop(self, *args, **kwargs):
        """
        Stops the Kivy window and saves the counts.
        """
        self.save_counts()
        super().stop(*args, **args)

if __name__ == '__main__':
    app = Defect_CounterApp()
    app.start_window()
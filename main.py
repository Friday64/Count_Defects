import csv
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

class Defect_CounterApp(App):
    def build(self):
        self.layout = GridLayout(cols=2, rows=14, padding=10, spacing=10) 
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
            btn.bind(on_release=lambda btn, index=i: self.increment_count(index))
            self.layout.add_widget(btn)

            data['count'] = data.get('count', 0)  # Simplified count initialization
            data['label'] = Label(text=str(data['count']), size_hint_y=None, height=44)
            self.layout.add_widget(data['label'])

        reset_button = Button(text='Reset Counts')
        reset_button.bind(on_release=self.reset_counts)
        self.layout.add_widget(reset_button)

        Clock.schedule_interval(self.save_counts, 30)  # Schedule save_counts every 30 seconds

        return self.layout

    def check_csv(self):
        """
        Checks if 'counts.csv' exists, and creates it if it doesn't.
        """
        if not os.path.exists('counts.csv'):
            try:
                with open('counts.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
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
                row = next(reader, None)  # Get first row or None if file is empty
                for i, data in enumerate(self.defect_data):
                    data['count'] = int(row[i]) if row else 0  # Simplified count loading
        except Exception as e:
            print(f"Error loading counts: {e}")

    def save_counts(self, dt):  # Add dt argument for Kivy Clock
        """
        Saves defect counts to a CSV file.
        """
        try:
            with open('counts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data['count'] for data in self.defect_data])
            print("Saved counts to counts.csv file.")
        except Exception as e:
            print(f"Error saving counts: {e}")

    def increment_count(self, index):
        """
        Increments the count of a defect.
        """
        self.defect_data[index]['count'] += 1
        self.defect_data[index]['label'].text = str(self.defect_data[index]['count'])

        #Save the updated count to the CSV file
        self.save_counts(None)  # Pass None for dt when called manually
    def reset_counts(self, instance):
        """
        Resets all defect counts to 0.
        """
        for data in self.defect_data:
            data['count'] = 0
            data['label'].text = '0'
        self.save_counts(None)  # Pass None for dt when called manually

    #function to save the counts to the CSV file on when x is pressed
    def on_pause(self):
        self.save_counts(None)  # Pass None for dt when called manually
        return True
    

if __name__ == '__main__':
    Defect_CounterApp().run()
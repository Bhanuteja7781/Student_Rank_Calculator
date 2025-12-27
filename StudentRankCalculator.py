import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk
import os

class StudentRankCalculator:
    def __init__(self):
        self.df = None
        self.subjects = []
    
    def run(self):
        print("\n=== Student Rank Calculator ===")
        self.df = self.get_student_data()

        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6 or X to exit): ").strip().lower()

            if choice == '1':
                self.show_student_data()
            elif choice == '2':
                self.calculate_and_display_ranks()
            elif choice == '3':
                self.show_top_students()
            elif choice == '4':
                self.export_ranked_data()
            elif choice == '5':
                self.plot_rank_bar_chart()
            elif choice == '6':
                self.generate_report()
            elif choice == 'x':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def get_student_data(self):
        print("\nChoose Input Method:")
        print("1. Manual Entry")
        print("2. Load from CSV")
        print("3. Use Sample Data")
        choice = input("Enter choice (1-3): ").strip()

        if choice == '1':
            return self.manual_entry()
        elif choice == '2':
            return self.load_from_csv()
        else:
            return self.sample_data()

    def manual_entry(self):
        students = []
        print("\nEnter student data. Leave name blank to stop.")
        self.subjects = input("Enter subject names separated by commas (e.g., Math,Science,English): ").strip().split(',')

        while True:
            name = input("\nStudent Name: ").strip()
            if not name:
                break
            scores = {}
            for sub in self.subjects:
                while True:
                    try:
                        s = float(input(f"{sub.strip()} Score (0-100): "))
                        if 0 <= s <= 100:
                            scores[sub.strip()] = s
                            break
                        else:
                            print("Enter a score between 0 and 100.")
                    except:
                        print("Invalid input!")
            students.append({'Name': name, **scores})
        return pd.DataFrame(students)

    def load_from_csv(self):
        root = Tk()
        root.withdraw()
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        root.destroy()
        if not path:
            print("No file selected. Using sample data.")
            return self.sample_data()
        try:
            df = pd.read_csv(path)
            if 'Name' not in df.columns:
                raise Exception("CSV must include a 'Name' column.")
            self.subjects = [col for col in df.columns if col != 'Name']
            return df
        except Exception as e:
            print(f"Error: {e}")
            return self.sample_data()

    def sample_data(self):
        data = {
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
            'Math': [88, 76, 92, 85],
            'Science': [92, 85, 88, 79],
            'English': [85, 78, 95, 88]
        }
        self.subjects = ['Math', 'Science', 'English']
        return pd.DataFrame(data)

    def show_menu(self):
        print("\n=== MAIN MENU ===")
        print("1. View Student Data")
        print("2. Calculate & Display Ranks")
        print("3. Show Top Students")
        print("4. Export Ranked Data to CSV")
        print("5. Plot Rank Bar Chart")
        print("6. Generate Full Report")
        print("X. Exit")

    def show_student_data(self):
        print("\nStudent Data:\n")
        print(self.df)
        print("\nStats:\n", self.df[self.subjects].describe())

    def calculate_and_display_ranks(self):
        self.df['Average'] = self.df[self.subjects].mean(axis=1)
        self.df['Rank'] = self.df['Average'].rank(ascending=False, method='min').astype(int)
        ranked_df = self.df.sort_values('Rank')
        print("\nRanked Student List:\n")
        print(ranked_df[['Rank', 'Name', 'Average'] + self.subjects])

    def show_top_students(self):
        if 'Rank' not in self.df.columns:
            self.calculate_and_display_ranks()
        top_rank = self.df['Rank'].min()
        top_students = self.df[self.df['Rank'] == top_rank]
        print(f"\nTop Student(s) with Rank {top_rank}:\n")
        print(top_students[['Name', 'Average']])

    def export_ranked_data(self):
        if 'Rank' not in self.df.columns:
            self.calculate_and_display_ranks()
        filename = "ranked_students.csv"
        self.df.sort_values('Rank').to_csv(filename, index=False)
        print(f"\nData exported to {filename}")

    def plot_rank_bar_chart(self):
        if 'Rank' not in self.df.columns:
            self.calculate_and_display_ranks()
        ranked = self.df.sort_values('Rank')
        plt.barh(ranked['Name'], ranked['Average'], color='skyblue')
        plt.xlabel('Average Score')
        plt.title('Student Ranks')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def generate_report(self):
        self.calculate_and_display_ranks()
        self.show_top_students()
        self.export_ranked_data()
        self.plot_rank_bar_chart()

if __name__ == "__main__":
    StudentRankCalculator().run()

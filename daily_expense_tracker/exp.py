import mysql.connector
from datetime import datetime

class DailyExpenseTracker:
    def __init__(self):
        # Initialize the connection to MySQL database
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",       # Replace with your MySQL username, typically "root"
                password="",   # Replace with your MySQL password
                database="daily_expenses_db"
            )
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            exit(1)

    def greet_user(self):
        print("Hello! Welcome to the Daily Expenses Tracker.")
        self.user_name = input("Please enter your name: ")
        
        # Validate date input
        while True:
            self.date = input("Enter the date (YYYY-MM-DD): ")
            try:
                datetime.strptime(self.date, "%Y-%m-%d")  # Validate the date format
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def get_meal_expenses(self):
        while True:
            try:
                self.breakfast = float(input("Enter breakfast expenses: "))
                self.lunch = float(input("Enter lunch expenses: "))
                self.dinner = float(input("Enter dinner expenses: "))
                break  # Exit loop if input is valid
            except ValueError:
                print("Please enter valid numeric values for expenses.")

    def get_other_expenses(self):
        while True:
            try:
                self.extra = float(input("Enter other expenses (e.g., tea, juice): "))
                self.travel = float(input("Enter travel expenses: "))
                break  # Exit loop if input is valid
            except ValueError:
                print("Please enter valid numeric values for expenses.")

    def calculate_total(self):
        self.total = self.breakfast + self.lunch + self.dinner + self.extra + self.travel
        print(f"\nTotal expenses for {self.date} are: {self.total:.2f}")

    def store_expenses(self):
        # Insert collected data into the database
        try:
            self.cursor.execute('''
            INSERT INTO expenses (user_name, date, breakfast, lunch, dinner, extra, travel, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.user_name, self.date, self.breakfast, self.lunch, self.dinner, self.extra, self.travel, self.total))
            self.conn.commit()
            print("Your data has been saved in the database.")
        except mysql.connector.Error as err:
            print(f"Error saving data to the database: {err}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")

    def run(self):
        # Running the sequence of operations
        self.greet_user()
        self.get_meal_expenses()
        self.get_other_expenses()
        self.calculate_total()
        self.store_expenses()
        self.close_connection()

# Create an instance of the class and run the program
if __name__ == "__main__":
    expense_tracker = DailyExpenseTracker()
    expense_tracker.run()

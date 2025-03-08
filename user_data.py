import sqlite3

class User_data:
    def __init__(self):
        self.db = sqlite3.connect("user_info.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                EmailID TEXT,
                First_name TEXT NOT NULL,
                Last_name TEXT NOT NULL,
                Username TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL
            )
        ''')

    def adder(self, email_ID, fname, lname, username, password):
        # Check if username or email already exists
        self.cursor.execute("SELECT * FROM user_data WHERE Username = ? OR EmailID = ?", (username, email_ID))
        existing_user = self.cursor.fetchone()

        if existing_user:
            return False  # Indicate that the user already exists

        query = """INSERT INTO user_data (EmailID, First_name, Last_name, Username, Password) 
                   VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(query, (email_ID, fname, lname, username, password))
        self.db.commit()
        return True  # Indicate successful signup

    def get_user(self, username, password):
        query = "SELECT * FROM user_data WHERE Username = ? AND Password = ?"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

    def get_user_by_username(self, username):
        """Retrieve the email of a user by their username."""
        query = "SELECT EmailID FROM user_data WHERE Username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()  # Returns (email,) or None

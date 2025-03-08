import sqlite3

class DatabaseManager:
    def __init__(self, db_path="my_database.db",rec_path="user_info.db"):
        self.db_path = db_path
        self.create_tables()
        self.rec_path=rec_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    def rec_get_conn(self):
        rec_conn=sqlite3.connect(self.rec_path,check_same_thread=False)
        rec_conn.row_factory=sqlite3.Row
        return rec_conn

    def create_tables(self):
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                EmailID TEXT UNIQUE NOT NULL,
                First_name TEXT NOT NULL,
                Last_name TEXT NOT NULL,
                Username TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL
            )
        """)

        # Create movies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genre TEXT NOT NULL
            )
        """)

        # Create shows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT NOT NULL,
                show_time TEXT NOT NULL,
                tickets_available INTEGER NOT NULL
            )
        """)

        # Create bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                movie_name TEXT NOT NULL,
                show_time TEXT NOT NULL,
                seat_number TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def add_movie(self, name, genre):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO movies (name, genre) VALUES (?, ?)", (name, genre))
                conn.commit()
                return True, "Movie added successfully!"
            except sqlite3.IntegrityError:
                return False, "Movie already exists!"

    def add_show(self, movie_name, show_time, tickets_available):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shows (movie_name, show_time, tickets_available) VALUES (?, ?, ?)",
                (movie_name, show_time, tickets_available)
            )
            conn.commit()

    def get_movies(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies")
            return cursor.fetchall()

    def get_shows_by_movie(self, movie_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM shows WHERE movie_name = ?", (movie_name,))
            ids=cursor.fetchall()
            list1=[]
            for i in ids:
                list1.append(i)
            return list1

    def remove_show(self, show_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM shows WHERE id = ?", (show_id,))
            conn.commit()
            return True, "Slot removed successfully!"


    def booked_tickets(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
        cursor.execute("SELECT * FROM ")  # Assuming this table exists
        tickets = cursor.fetchall()
        return tickets


if __name__ == '__main__':
    db = DatabaseManager()
    db.create_tables()

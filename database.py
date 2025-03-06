import sqlite3

class adder:
    def __init__(self, db_name="my_database.db"):
        self.data = sqlite3.connect(db_name)
        self.cursor = self.data.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            genre TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            show_time TEXT NOT NULL,
            tickets_available INTEGER,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
        ''')

        self.data.commit()

    def add(self, name, genre):
        # Insert movie into movies table
        self.cursor.execute("INSERT INTO movies (name, genre) VALUES (?, ?)", (name, genre))
        movie_id = self.cursor.lastrowid  # Get the inserted movie's ID


        self.data.commit()
        print("Updated list is: \n")
        self.printer()

    def remove(self,name):
        self.data.execute("DELETE FROM movies WHERE name= ?",(name,))
        self.data.commit()
        print("Updated list is: \n")
        self.printer()

    def update(self,domain,updated,movie):
        self.data.execute(f"UPDATE movies SET {domain} = ? WHERE name = ?", (updated, movie))
        self.data.commit()
        print("Updated Value is: ")
        self.printer()

    def printer(self):
        self.cursor.execute("SELECT * FROM movies")
        movies = self.cursor.fetchall()
        for movie in movies:
            print(movie)

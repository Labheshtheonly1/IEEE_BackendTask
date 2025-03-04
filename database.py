import sqlite3

class adder:
    def __init__(self, db_name="my_database.db"):
        self.data = sqlite3.connect(db_name)
        self.cursor = self.data.cursor()
        self.create_table()  # Calling the method inside __init__

    def create_table(self):  # Instance method
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            genre TEXT,
            tickets_available INTEGER
        )
        ''')
        self.data.commit()


    def add(self,name,genre,seats):
        self.data.execute("INSERT INTO movies (name , genre, tickets_available) Values(?, ?, ?)",
                     (name,genre,seats))
        self.data.commit()
        print("Updated list is: \n")
        self.cursor.execute("SELECT * FROM movies")
        movies = self.cursor.fetchall()
        for movie in movies:
            print(movie)

    def remove(self,name):
        self.data.execute("DELETE FROM movies WHERE name= ?",(name,))
        self.data.commit()
        print("Updated list is: \n")
        self.cursor.execute("SELECT * FROM movies")
        movies = self.cursor.fetchall()
        for movie in movies:
            print(movie)





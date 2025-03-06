import sqlite3
movies_=[]
Rec=sqlite3.connect("User_record.db")
rec_cursor=Rec.cursor()
conn=sqlite3.connect("my_database.db")
cursor=conn.cursor()

class Movie:
    def __init__(self):
        pass
    def screening(self):
        cursor.execute("SELECT name FROM movies")
        movies=cursor.fetchall()
        global movies_
        for i in movies:
            movies_.append(i[0])
            print(i[0])


class Booking:
    def __init__(self):
        self.reser = sqlite3.connect("reservation.db")
        self.res_cursor = self.reser.cursor()
        self.create_table()

    def create_table(self):
        self.res_cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            Email_ID TEXT,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            MovieName TEXT,
            ShowTime TEXT,
            tickets_Booked INTEGER
        )
        ''')
        self.reser.commit()

    def booking(self):
        movie_name = input("Which movie do you want to watch? ")

        # Fetch available show slots for the selected movie
        cursor.execute("SELECT show_time, tickets_available FROM shows WHERE movie_name = ?", (movie_name,))
        shows = cursor.fetchall()

        if not shows:
            print("No available shows for this movie.")
            return

        print("Available Show Times:")
        for i, (time, tickets) in enumerate(shows, 1):
            print(f"{i}. {time} ({tickets} tickets available)")

        slot_choice = int(input("Select the show number: ")) - 1
        if slot_choice < 0 or slot_choice >= len(shows):
            print("Invalid choice.")
            return

        show_time, available_tickets = shows[slot_choice]

        fname = input("Enter Your First Name: ")
        lname = input("Enter your Last Name: ")
        tickets = int(input("Enter the No. of Tickets: "))

        if tickets > available_tickets:
            print("Not enough tickets available for this show.")
            return

        # Fetch Email ID
        rec_cursor.execute("SELECT EmailID FROM user_info WHERE First_name = ? AND Last_name = ?", (fname, lname))
        ID = rec_cursor.fetchone()

        if ID is None:
            print("Error: User not found in the database.")
            return

        ID_ = ID[0]

        try:
            # Insert reservation record
            self.reser.execute("INSERT INTO Reservations (Email_ID, fname, lname, MovieName, ShowTime, tickets_Booked) "
                               "VALUES (?, ?, ?, ?, ?, ?)", (ID_, fname, lname, movie_name, show_time, tickets))

            # Update available tickets for the selected show slot
            conn.execute(
                "UPDATE shows SET tickets_available = tickets_available - ? WHERE movie_name = ? AND show_time = ?",
                (tickets, movie_name, show_time))

            self.reser.commit()
            conn.commit()
            print(f"Tickets Booked for {movie_name} at {show_time}!")

        except sqlite3.Error as e:
            print("Database error:", e)

    def cancel_ticket(self):
        movie_name = input("Which movie do you want to cancel: ")
        show_time = input("Enter the show time of your booking (e.g., '10:00 AM'): ")
        fname = input("Enter Your First Name: ")
        lname = input("Enter your Last Name: ")

        # Fetch reservation details
        self.res_cursor.execute(
            "SELECT tickets_Booked FROM Reservations WHERE fname = ? AND lname = ? AND MovieName = ? AND ShowTime = ?",
            (fname, lname, movie_name, show_time))
        booking = self.res_cursor.fetchone()

        if booking is None:
            print("No booking found.")
            return

        tickets_to_cancel = booking[0]

        try:
            # Delete reservation
            self.res_cursor.execute(
                "DELETE FROM Reservations WHERE fname = ? AND lname = ? AND MovieName = ? AND ShowTime = ?",
                (fname, lname, movie_name, show_time))
            # Restore available tickets
            self.res_cursor.execute('''
                       UPDATE shows 
                       SET tickets_available = tickets_available + ? 
                       WHERE movie_id = (SELECT id FROM movies WHERE name = ?) AND show_time = ?
                   ''', (tickets_to_cancel, movie_name, show_time))
            self.reser.commit()
            conn.commit()
            print(
                f"Your booking for {movie_name} at {show_time} has been canceled. {tickets_to_cancel} tickets have been restored.")
        except sqlite3.Error as e:
            print("Database error:", e)




from database import adder
Adder=adder()


class Admin:
    def __init__(self):
        pass

    def addmovie(self):
        movie_amount = int(input("How many movies do you want to add: "))
        for i in range(movie_amount):
            values = input(f"Enter Movie and info of {i + 1} (Format: Name,Genre,TotalTickets): ")
            info = values.split(",")
            movie = info[0]
            movie_genre = info[1]
            # Add movie to database
            Adder.add(name=movie, genre=movie_genre)

            # Adding show slots for the movie
            num_slots = int(input(f"How many show slots for '{movie}': "))
            for j in range(num_slots):
                show_time = input(f"Enter Show {j + 1} Time (HH:MM AM/PM format): ")
                slot_tickets = int(input(f"Enter tickets available for {show_time}: "))
                Adder.data.execute("INSERT INTO shows (movie_name, show_time, tickets_available) VALUES (?, ?, ?)",
                                   (movie, show_time, slot_tickets))
                Adder.data.commit()

            print(f"Movie '{movie}' added with {num_slots} show slots.")

    def removemovie(self):
        trash = input("Which Movie do you want to remove: ")
        Adder.remove(name=trash)
        Adder.data.execute("DELETE FROM shows WHERE movie_name= ?", (trash,))
        Adder.data.commit()
        print(f"All shows for '{trash}' have been removed.")

    def updateinfo(self):
        Adder.printer()
        movie = input("Which movie's info do you want to change: ")
        domain = input("Which field do you want to update (name, genre, tickets_available): ")
        updated_value = input("Updated Value: ")
        Adder.update(domain=domain, movie=movie, updated=updated_value)











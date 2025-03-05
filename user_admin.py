from database import adder
Adder=adder()
class Admin:
    def __init__(self):
        pass
    def addmovie(self):
        movie_amount=int(input("How many movies you want to add:"))
        for i in range(movie_amount):
            values=input(f"Enter Movie and info of {i+1}: ")
            info=values.split(",")
            movie=info[0]
            movie_genre=info[1]
            ticket_set=int(info[2])
            Adder.add(name=movie,genre=movie_genre,seats=ticket_set)

    def removemovie(self):
        trash=input("Which Movie you want to remove: ")
        Adder.remove(name=trash)

    def updateinfo(self):
        Adder.printer()
        movie=input("Which movie's info you want to change: ")
        domain=input("Which Domain you want to Change (name, genre, tickets_available): ")
        updated_value=input("Updated Value: ")
        Adder.update(domain=domain,movie=movie,updated=updated_value)










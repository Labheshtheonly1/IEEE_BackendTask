import sqlite3
from database import adder
Adder=adder()

data=sqlite3.connect("mydatabase.db")
cursor=data.cursor()
class Admin:
    def __init__(self):
        pass
    def addmovie(self):
        movie_amount=int(input("How many movies you want to add:"))
        for i in range(movie_amount):
            movie=input(f"Enter Movie No.{i+1}")
            movie_genre=input("Genre of this movie? : ")
            ticket_set=int(input("Enter no of tickets to Alot this show: "))

            Adder.add(name=movie,genre=movie_genre,seats=ticket_set)

    def removemovie(self):
        trash=input("Which Movie you want to remove: ")
        Adder.remove(name=trash)






import flask
import os
from Movies import Movie,Booking
from user_admin import Admin
import user_admin

admin=Admin()
movie=Movie()
booking=Booking()
Username=input("Please Enter Your Username: ")
Password=input("Please Enter You Password: ")
if Username=="Admin" and Password=="Admin@123":
    os.system("cls")
    print("Welcome Admin! Which Movie Would you Add or Remove Today!?")
    des=input()
    if des=="Add":
        admin.addmovie()
        print("Updated list is:")
        print(user_admin.list1)
    elif des=="Remove":
        admin.removemovie()
        print("Updated List is:")
        print(user_admin.list1)
else:
    print("Which Movie Would you like to watch Today!")
    movie.screening()
    booking.booking()

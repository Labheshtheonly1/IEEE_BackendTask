import user_admin
movies=user_admin.list1
with open("Movie_list.txt","r") as list:
    line=list.readlines()
class Movie:
    def __init__(self):
        pass
    def screening(self):
        for i in line:
            print(i)
class Booking:
    def __init__(self):
        pass

    def booking(self):
        Total_seats1=100
        Available_seats1=100

        Total_seats2=100
        Available_seats2=100

        Total_seats3=100
        Available_seats3=100
        selection=int(input("Enter the Number of your preferred Movie: "))
        if selection==1:
            print(f"You booked {movies[0]}")

            Tickets=int(input('Enter the number of Tickets you want:'))
            print("Seats Booked!!")
            Available_seats1 = Available_seats1 - Tickets
            print(f"Seats Left: {Available_seats1}")
        if selection==2:
            print(f"You booked {movies[1]}")
            Tickets = int(input('Enter the number of Tickets you want:'))
            print("Seats Booked!!")
            Available_seats2 = Available_seats2 - Tickets
            print(f"Seats Left: {Available_seats2}")
        if selection==3:
            print(f"You booked {movies[2]}")
            Tickets1 = int(input('Enter the number of Tickets you want:'))
            print("Seats Booked!!")
            Available_seats3 = Available_seats3 - Tickets1
            print(f"Seats Left: {Available_seats3}")


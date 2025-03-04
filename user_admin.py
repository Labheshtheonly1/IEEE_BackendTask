with open("movies_list.txt","w+") as list1:
    pass
class Admin:
    def __init__(self):
        pass
    def addmovie(self):
        movie_amount=int(input("How many movies you want to add:"))
        for i in range(movie_amount):
            list1.write(input(f"Enter Movie No.{i}\n"))

    def removemovie(self):
        Remover=True
        while Remover:
            removed=input("Enter the Name of Movie which you want to Remove")
            if removed in list1:
                list1.remove(removed)
                Remover=False
            else:
                print("Looks like you entered the wrong movie! Please Try again.")





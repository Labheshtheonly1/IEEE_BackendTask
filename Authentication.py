import sqlite3
from user_admin import Admin
admin=Admin()
class UserInfo:
    def __init__(self):
        self.Data=sqlite3.connect("User_record.db")
        self.Cursor=self.Data.cursor()
        self.create_table()
        self.login_counter=0


    def create_table(self):
        self.Cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
        EmailID TEXT,
        Username TEXT NOT NULL,
        Password TEXT
        )
        ''')
        self.Data.commit()


    def sign_up(self):
        Email=input("Enter Your Email-ID")
        Username=input("Set Your Username: ")
        Passwword=input("Set Your Password: ")
        self.Data.execute("INSERT INTO user_info (EmailID, Username, Password) Values(?, ?, ?)"
                          ,(Email,Username,Passwword))
        self.Data.commit()
        self.Log_in()

    def Log_in(self):

        User_name=input("Please Enter your Username: ")
        Pass_word=input("PLease Enter your Password: ")
        if User_name == "Admin" and Pass_word == "Admin@123":
            print(f"Welcome {User_name}!")
            print("Choose your Action.\n 1) Add Movie\n2) Remove Movie\n3) Update Info")
            des = input()
            if des == "1":
                admin.addmovie()
            elif des == "2":
                admin.removemovie()
            elif des == "3":
                admin.updateinfo()
        else:
            try:
                # Fetch the password for the given username
                self.Cursor.execute("SELECT Password FROM user_info WHERE Username = ?", (User_name,))
                stored_password = self.Cursor.fetchone()
                if stored_password:  # If username exists
                    if stored_password[0] == Pass_word:  # Compare passwords
                        print("Authentication successful!")
                        print("Loging in....")

                    else:
                        if self.login_counter<3:
                            print("Incorrect password!, Please Log in Again!.")
                            self.login_counter += 1
                            self.Log_in()
                        else:
                            print("Sorry Your Account has been terminated!")
                else:
                    print("Username not found!, Please Sign up.")
                    self.sign_up()
            except sqlite3.Error as e:
                print("Database error:", e)
    def Authenticator(self):
        IN = input("1.) Signup \n2.)Log in\n")
        if IN == "1":
            self.sign_up()
        elif IN=="2":
            self.Log_in()
        else:
            print("Error Enter Valid Input")
            self.Authenticator()


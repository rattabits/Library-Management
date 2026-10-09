import subprocess
import sys

class Library:
    def __init__(self,name):
        self._name = name
        self._books = []
        self._users = []
    @property
    def name(self):
        return self._name

    @property
    def books(self):
        return self._books.copy()
    
    @property
    def users(self):
        return self._users.copy()
    
    #Method 

    def add_books(self,title,pn,subject):
        book = {
            "title" : title,
            "page_num" : pn,
            "subject" : subject,
            "is_available" : True
        }
        self._books.append(book)
        print(f"{book['title']} has been added...")

    def show_all_books(self):
        for item in self._books:
            print(item["title"])

    def show_available_books(self):
        for item in self._books:
            if item["is_available"] == True:
                print(f"{item["title"]} is available")

    def remove_book(self ,title):
        found = False
        for book in self._books:
            if book["title"].lower() == title.lower():
                found = True
                self._books.remove(book)
                print("The book deleted successfuly...")
                break
        if not found:
            print("The book is not exist...")

    def borrow_book(self,title):
        for book in self._books:
            if book["title"].lower() == title.lower():
                if not book["is_available"]:
                    return False
                book["is_available"] = False
                return True
        return False
       
    def return_book(self ,title):
        for book in self._books:
            if book["title"].lower() == title.lower():
                book["is_available"] = True
                return True
            
class Users:
    def __init__(self,username,password):
        self._username = username
        self.password = password

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        raise AttributeError("You can't access to passwords")

    @password.setter
    def password(self,value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 character with (a-z/0-9/#_!)")
        if " " in value:
            raise ValueError("Don't use space in your password")
        self._password = value
    
class Admin(Users):

    _admin_dict = {}

    def __init__(self,username,password ,lib):
        super().__init__(username,password)
        self._lib = lib

    #Methods
    def add_book(self,title,pn,subject):
        self._lib.add_books(title,pn,subject)

    def remove_book(self,title):
        self._lib.remove_book(title)

    def show_all_books(self):
        self._lib.show_all_books()
    @classmethod
    def sign_up(cls ,username ,password):
        cls._admin_dict[username] = password

    @classmethod
    def sign_in(cls ,username ,password):
        if username in cls._admin_dict.keys():
            if cls._admin_dict[username] == password:
                return True
        print("Wrong username !")


class Students(Users):

    _students_dict = {}

    def __init__(self ,username,password,lib):
        super().__init__(username,password)
        self._lib = lib
        self._books = []

    @property
    def books(self):
        return self._books.copy()
    
    def show_available_books(self):
        self._lib.show_available_books()

    def borrow_book(self,title):
        if self._lib.borrow_book(title):
            self.books.append(title)
        print("Book is not exist...")

    def return_book(self ,title):
        if self._lib.return_book(title):
            self.books.remove(title)
        print()

    @classmethod
    def sign_up(cls ,username ,password):
        if username in cls._students_dict:
            print("We have a student with this username try another one")
            return False
        cls._students_dict[username] = password
    
    @classmethod
    def sign_in(cls ,username ,password):
        if username in cls._students_dict.keys():
            if cls._students_dict[username] == password:
                return True
            else:
                print("Incorrect Password")
                
#-----------------------------------test------------------------------
def show_menue(req ,username=None):
    if req == 0:
        print("1- Loogin")
        print("2- Signup")
        print("3- Exit")
        print("4- Main menue")
    elif req == 1:
        print(f"--- Welcome {username} ---")
        print("1- show all books")
        print("2- borrow book")
        print("3- Exit")
        print("4- Main menue")
    elif req == 2:
        print(f"--- Welcome {username} ---")
        print("1- add book")
        print("2- remove book")
        print("3- show all books")
        print("4- Main menue")

def clear_screen():
    subprocess.run(["clear"])

def main():
    lib = Library("shahid beheshti")
    while True:
        print("Wellcome to your library !")
        show_menue(0)
        opt = input("Enter your choice: ")

        if opt == '1':
            clear_screen()
            print("--- Login Page ---")
            cho = input("Admin/Student: ")
            if cho.lower() == 'student':
                clear_screen()
                print("--- Student Login Page ---")
                username = input("Enter your Username: ")
                password = input("Enter your Password: ")
                if Students.sign_in(username ,password):
                    std_obj = Students(username ,password ,lib)
                    clear_screen()
                    show_menue(1,username)
                    opt = input("Enter your choice: ")
                    if opt == '1':
                        std_obj.show_available_books()
                        show_menue(1,username)
                    elif opt == '2':
                        std_obj.show_available_books()
                        title = input("Which book you want? ")
                        std_obj.borrow_book(title)
                        show_menue(1,username)
                    elif opt == '3':
                        clear_screen()
                        sys.exit(0)
                    elif opt == '4':
                        clear_screen()
                        show_menue(0)
            else:
                clear_screen()
                print("--- Admin Login Page ---")
                username = input("Enter your Username: ")
                password = input("Enter your Password: ")
                if Admin.sign_in(username ,password):
                    std_obj = Admin(username ,password ,lib)
                    clear_screen()
                    show_menue(2,username)
                    opt = input("Enter your choice: ")
                    if opt == '1':
                        title = input("Enter Title: ")
                        pn = input("Enter PN: ")
                        subject = input("Enter Subject: ")
                        std_obj.add_book(title ,pn ,subject)
                        show_menue(2,username)
                    elif opt == '2':
                        title = input("Which book you want to ? ")
                        std_obj.remove_book(title)
                        show_menue(2,username)
                    elif opt == '3':
                        clear_screen()
                        std_obj.show_all_books()
                        show_menue(2,username)
                    elif opt == '4':
                        clear_screen()
                        show_menue(0)
        elif opt == '2':
            clear_screen()
            print("--- Regestration Page ---")
            cho = input("What's your role? (Admin-Student)")
            if cho.lower() == 'admin':
                username = input("what's your Username: ")
                password = input("what's your Password: ")
                if Admin.sign_up(username ,password):
                    print("You signed up successfuly as an admin...")
            else:
                username = input("Enter your Username: ")
                password = input("Enter your Password: ")
                clear_screen()
                if Students.sign_up(username ,password):
                    print("You signed up successfuly as student...")
        elif opt == '3':
            clear_screen()
            sys.exit(0)

        elif opt == '4':
            clear_screen()
            show_menue(0)
main()
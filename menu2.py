import getpass
strongPasswordInfomation = "I recommend a password that is at least 8 characters long with a mix of letters, numbers and special characters."

def addNewUser(cursor):
    fullName = (input("\nPlease enter your first and last name here:  ")).split()
    if len(fullName)==2:
        username,password = addUsername()
        firstName = fullName.pop(0)
        lastName = fullName.pop(0)
        newUser = User(firstName,lastName,username,password)
        newUser.createNewUser(cursor)
    else:
        print("\nOops, looks like you didn't enter your full name...")
        addNewUser(cursor)

def addUsername():
    username = input("\nPlease enter your username/email here:   ")
    correctUsername = input("\nIs this the correct username? (Y):  ")
    if correctUsername.lower() == "y":
        password = addPassword()
        return username,password
    else:
        addUsername()

def addPassword():
    password = getpass.getpass("\nPlease enter your password here:    ")
    correctPassword = input("\nWould you like to submit this password? (Y): ")
    if correctPassword.lower == "y":
        return password
    else:
        addPassword()

def logIn(cursor):
    username = input("\nPlease enter your username/email here:   ")
    password = getpass.getpass("\nPlease enter your password here:    ")
    if User.loginUser(username,password,cursor) == True:
        True ############
    else:
        print("\nHmmmmmm, it looks like the information you entered is incorrect... Please try again.")
        logIn(cursor)


def mainMenu(cursor):
    loginOrAdd = input("\nWould you like to login or add a new user? (L or A):  ")
    if loginOrAdd.lower() == "l":
        logIn(cursor)
    elif loginOrAdd.lower() == "a":
        addNewUser(cursor)

cursor = 0
mainMenu(cursor)
from User import User,NewUser

import getpass
strongPasswordInfomation = "I recommend a password that is at least 8 characters long with a mix of letters, numbers and special characters."

def addUsername():
    def addPassword():
        password = getpass.getpass("\nPlease enter your password here (you won't be able to see it!):    ")
        print("password: ",password)
        correctPassword = input("\nWould you like to submit this password? (Y): ")
        if correctPassword.lower() == "y":
            return password
        else:
            return addPassword()
    username = input("\nPlease enter your username/email here:   ")
    correctUsername = input("\nIs this the correct username? (Y):  ")
    if correctUsername.lower() == "y":
        password = addPassword()
        return username,password
    else:
        return addUsername()

def addNewUser(conn,cursor):
    fullName = (input("\nPlease enter your first and last name here:  ")).split()
    correctName= input("\nIs this the correct name? (Y):  ")
    if len(fullName)==2 and correctName.lower() == "y":
        username,password = addUsername()
        firstName = fullName.pop(0)
        lastName = fullName.pop(0)
        newUser = NewUser(username,password,firstName,lastName)
        newUser.createNewUser(cursor)
        passwordVault(newUser,conn,cursor)
    else:
        print("\nOops, looks like you didn't enter your full name...")
        addNewUser(conn,cursor)

def logIn(conn,cursor):
    username = input("\nPlease enter your username/email here:   ")
    password = getpass.getpass("\nPlease enter your password here:    ")
    currentUser = User(username, password)
    if currentUser.loginUser(username, password, cursor) != False:
        passwordVault(currentUser, conn, cursor)
    else:
        print("\nHmmmmmm, it looks like the information you entered is incorrect... Please try again.")
        logIn(conn,cursor)

############################################################################################

def mainMenu(conn,cursor):
    loginOrAdd = input("\nWould you like to login or add a new user? (L or A):  ")
    if loginOrAdd.lower() == "l":
        logIn(conn,cursor)
    elif loginOrAdd.lower() == "a":
        addNewUser(conn,cursor)

def passwordVault(currentUser,conn,cursor):
    conn.commit()
    print("\nWelcome to Password Vault!  \nThis is a simple password manager that allows you to store, retrieve and generate your passwords.  \nEnjoy!")
    def options():
        retrieveAddStored = input("\nWould you like to retrieve information, add new information or see all of your stored information? (R or A or S):  ")
        if retrieveAddStored.lower() == "r":
            infoOnCurrentUser = currentUser.retrieveInfo(cursor)
            print(infoOnCurrentUser)
        elif retrieveAddStored.lower() == "a":
            itemName = input("\nPlease enter the name of the application or website:  ")
            username,password = addUsername()
            currentUser.addItem(itemName,username,password,cursor)

        else:
            print("\nHmmmm, looks like you didn't enter an option... Try again.")
            options()
    options()
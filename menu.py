import getpass
from User import User,NewUser
from randomGeneration import takingInputs

strongPasswordInfomation = "I recommend a password that is at least 8 characters long with a mix of letters, numbers and special characters."

def addUsername():
    def addPassword():
        password = getpass.getpass("\nPlease enter your password here (you won't be able to see it!):    ")
        correctPassword = input("\nWould you like to submit this password? (Y): ")
        if correctPassword.lower() == "y":
            return password
        else:
            return addPassword()
        
    username = input("\nPlease enter your username/email here:   ")
    correctUsername = input("\nIs this the correct username? (Y):  ")

    try:
        if correctUsername.lower() == "y" or correctUsername == "":
            optionForRandomGeneration = input("\nWould you like to randomly generate a password? (Y or N): ")
            while True:
                if optionForRandomGeneration.lower() == "y" or optionForRandomGeneration == "":
                    print("\nPlease randomly type on the keyboard: (Press the \"tab\" key to submit)")
                    randomlyGeneratedPassword = takingInputs()
                    pressEnter = input("\nPress enter to submit your password: ")
                    lengthOfRGPassword = 0
                    for i in range(len(randomlyGeneratedPassword)-1,0,-1):
                        if not str(randomlyGeneratedPassword[i]).isdigit():
                            lengthOfRGPassword = str(i)
                            break
                    desriredLengthOfRGPassword = input("\nHow long would you like your password to be? (up to "+str(lengthOfRGPassword)+"): ")
                    password = randomlyGeneratedPassword[:int(desriredLengthOfRGPassword)]
                    print("\nHere is your password:"+password+"\n"+strongPasswordInfomation)
                    userApproval = input("\nWould you like to submit this password? (Y): ")
                    if userApproval.lower() == "y" or userApproval == "":
                        return username,password
                    else:
                        continue
                    
        elif optionForRandomGeneration.lower() == "n":
            password = addPassword()
            return username,password
        else:
            print("\nHmmmm, that didn't seem to work... Try again.")
            return addUsername()
    except:
        print("\nHmmmm, that didn't seem to work... Try again.")
        return addUsername()
        
def addNewUser(conn,cursor):
    fullName = (input("\nPlease enter your first and last name here:  ")).split()
    correctName= input("\nIs this the correct name? (Y):  ")
    if len(fullName)==2 and correctName.lower() == "y" or "":
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
    while True:
        username = input("\nPlease enter your username/email here:   ")
        password = getpass.getpass("\nPlease enter your password here:    ")
        if len(username) > 0 and len(password) > 0:
            currentUser = User(username, password)
            if currentUser.loginUser(username, password, cursor) != False:
                passwordVault(currentUser, conn, cursor)
                break
        else:
            print("\nHmmmmmm, it looks like the information you entered is incorrect... Please try again.")

###########################################################################################################

def mainMenu(conn,cursor):
    loginOrAdd = input("\nWould you like to login or add a new user? (L or A):  ")
    if loginOrAdd.lower() == "l":
        logIn(conn,cursor)
    elif loginOrAdd.lower() == "a":
        addNewUser(conn,cursor)

def passwordVault(currentUser, conn, cursor):
    conn.commit()
    print("\nWelcome to Password Vault! \nThis is a simple password manager that allows you to store, retrieve, and generate your passwords. \nEnjoy!")
    while True:
        retrieveOrAdd = input("\nWould you like to retrieve information or add new information? (R or A): ")

        if retrieveOrAdd.lower() == "r":
            currentUser.retrieveLogins(cursor)
            itemName = input("\nPlease enter the name of the application or website that you want to retrieve: ")
            currentUser.retrieveItem(itemName,cursor)

        elif retrieveOrAdd.lower() == "a":
            itemName = input("\nPlease enter the name of the application or website: ")
            username,password = addUsername()
            successful = currentUser.addItem(itemName,username,password,cursor)
            if successful:
                conn.commit()
            else:
                continue

        else:
            print("\nHmmmm, looks like you didn't enter an option... Try again.")

        userChoice = input("\nWould you like to continue? (yes/no): ")
        if userChoice.lower() != "yes" or "":
            break
import getpass
from User import User,NewUser
from randomGeneration import randomGeneration

strongPasswordInfomation = "I recommend a password that is at least 8 characters long with a mix of letters, numbers and special characters."

def addPassword():
        password = getpass.getpass("\nPlease enter your password here (you won't be able to see it!):    ")
        correctPassword = input("\nWould you like to submit this password? (Y): ")
        if correctPassword.lower() == "y" or correctPassword == "":
            return password
        else:
            return addPassword()

def addUsername():
    username = input("\nPlease enter your username/email here:   ")
    correctUsername = input("\nIs this the correct username? (Y):  ")

    try:
        if correctUsername.lower() == "y" or correctUsername == "":
            optionForRandomGeneration = input("\nWould you like to randomly generate a password? (Y or N): ")
            while True:
                if optionForRandomGeneration.lower() == "y" or optionForRandomGeneration == "":
                    print("\nPlease randomly type on the keyboard: (Press the \"tab\" key to submit)")
                    randomlyGeneratedPassword = randomGeneration()
                    pressEnter = input("\nPress \"Enter\" to commit: ")
                    if pressEnter:
                        lengthOfRGPassword = 0
                        for i in range(len(randomlyGeneratedPassword)-1,0,-1):
                            if not str(randomlyGeneratedPassword[i]).isdigit():
                                lengthOfRGPassword = str(i)
                                break
                        desriredLengthOfRGPassword = input("\nHow long would you like your password to be? (up to "+str(lengthOfRGPassword)+" characters): ")
                        password = randomlyGeneratedPassword[:int(desriredLengthOfRGPassword)]
                        print("\nHere is your password: "+password+"\n"+strongPasswordInfomation)
                        userApproval = input("\nWould you like to submit this password? (Y): ")
                        if userApproval.lower() == "y" or userApproval == "":
                            return username,password
                        else:
                            continue

                elif optionForRandomGeneration.lower() == "n":
                    password = addPassword()
                    return username,password
        else:
            return addUsername()
    except:
        print("\nHmmmm, that didn't seem to work... Try again.")
        return addUsername()
        
def addNewUser(conn,cursor):
    fullName = (input("\nPlease enter your first and last name here:  ")).split()
    correctName= input("\nIs this the correct name? (Y):  ")
    if len(fullName)==2 and (correctName.lower() == "y" or correctName.lower() == ""):
        username,password = addUsername()
        firstName = fullName.pop(0)
        lastName = fullName.pop(0)
        newUser = NewUser(username,password,firstName,lastName)
        newUser.createNewUser(cursor)
        passwordVault(newUser,conn,cursor)
    else:
        print("\nOops, looks like something went wrong... Try again.")
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
            print("\nOops, looks like something went wrong... Try again.")

###########################################################################################################

def mainMenu(conn,cursor):
    while True:
        loginOrAdd = input("\nWould you like to login or add a new user? (L or A):  ")
        if loginOrAdd.lower() == "l":
            logIn(conn,cursor)
        elif loginOrAdd.lower() == "a":
            addNewUser(conn,cursor)
        else:
            print("\nOops, looks like something went wrong... Try again.")

def passwordVault(currentUser, conn, cursor):
    conn.commit()
    print("\nWelcome to Password Vault! \nThis is a simple password manager that allows you to store, retrieve, and generate your passwords. \nEnjoy!")

    while True:
        while True:
            retrieveOrAdd = input("\nWould you like to see your access logs, retrieve, export or add new information? (access logs OR R/E/A): (press \"Enter\" to sign out)  ")
            if retrieveOrAdd.lower() == "r":
                successful = currentUser.retrieveLogins(cursor)
                if successful:
                    conn.commit()
                    continue
                else:
                    continue
            elif retrieveOrAdd.lower() == "a":
                itemName = input("\nPlease enter the name of the application or website: ")
                username, password = addUsername()
                successful = currentUser.addItem(itemName, username, password, cursor)
                if successful:
                    conn.commit()
                    continue
                else:
                    continue
            elif retrieveOrAdd.lower() == "e":
                currentUser.exportInfo(cursor)
                continue
            elif retrieveOrAdd == "":
                mainMenu(conn,cursor)
            elif retrieveOrAdd.lower() == "access logs":
                currentUser.accessLogs(cursor)
            else:
                print("\nHmmmm, looks like you didn't enter a valid option... Try again.")

        userChoice = input("\nWould you like to continue? (yes/no): ")
        if userChoice.lower() != "yes" and userChoice != "":
            break

import sqlite3
from datetime import datetime

#Connecting to SQL database and creating cursor
connectionToDatabase = sqlite3.connect("/home/arun/Documents/NEA/mainDatabase.db")
cursor = connectionToDatabase.cursor()


strongPasswordInfomation = "I recommend a password that is at least 8 characters long with a mix of letters, numbers and special characters."

#Creates tables using createTables.sql file
with open("createTables.sql","r") as createTablesFile:
    createTables = createTablesFile.read()
    cursor.executescript(createTables)
    connectionToDatabase.commit()

#Creates a class for the user
class User():
    def __init__(self,firstName,lastName,username,password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.hashedPassword = hashFunction(password)
    def createNewUser(self):
        addUserToDatabase = """
        INSERT INTO Users(firstName,lastName,masterUsername,masterHashedPassword)
        VALUES (?,?,?,?)
        """
        cursor.execute(addUserToDatabase,(self.firstName,self.lastName,self.username,self.hashedPassword))

def mainMenu():
    #Makes a variable for a while loop in case the user doesn't enter L or A
    LorA = False
    while LorA != True:
        #Gives user options of what they would like to do
        loginOrAdd = input("\nWould you like to login or add a new user? (L or A):  ")
        #Gives the user the options for logging in
        if loginOrAdd == "l" or loginOrAdd == "L":
            LorA = True
            username = input("\nPlease enter your username/email here:   ")
            username.lower()
            password = input("\nPlease enter your password here:    ")

    
        #Takes user input for adding a new user
        elif loginOrAdd == "a" or loginOrAdd == "A":
            LorA = True
            correctUsername = False
            #While loop ensures that the user enters the correct username
            while correctUsername != True:
                #While loop validation to check the user enters their full name
                correctFullName = False
                while correctFullName != True:
                    fullName = (input("\nPlease enter your first and last name here:  ")).split()
                    if len(fullName) >=2:
                        firstName = fullName.pop(0)
                        lastName = fullName.pop(0)
                        correctFullName = True
                    else:
                        correctFullName = False
                        print("\nOops, looks like you didn't enter your full name...")
                newUsername = input("\nWhat would you like your new username to be (you can use your email)?    ")
                newUsername.lower()
                checkUsername = input("\nPlease enter your username again:    ")
                checkUsername.lower()
                if newUsername == checkUsername:
                    correctUsername = True
                    correctPassword = False

            #While loop ensures that the user enters the correct password
                    while correctPassword != True:
                        newPassword = input("\nWhat would you like your master password to be: ("+strongPasswordInfomation+")     ")
                        checkPassword = input("\nPlease enter your master password again:     ")
                        if newPassword == checkPassword:
                            print("Ok! You're ready to go!")
                            correctPassword = True
                            newUser = User(firstName,lastName,newUsername,newPassword)
                            newUser.createNewUser()
                        else:
                            print("\n Hmmmmmm, the passwords you entered do not match...  Please try again.")
                            correctPassword = False
                else:
                    print("\n Hmmmmmm, the usernames you entered do not match...  Please try again.")
                    correctUsername = False
        else:
            print("\n Oops, looks like you didn't enter L or A... Try again!")
    
def hashFunction(password):
    #sumOfUnicodes is the sum of all the squared unicode numerical codes
    sumOfUnicodes = 0
    password  = list(password)
    for i in range(len(password)):
        sumOfUnicodes += (ord(password[i]))**2
    sumOfUnicodes = list(str(sumOfUnicodes))
    firstAndLastDigit = int(sumOfUnicodes[0] + sumOfUnicodes[-1])
    middleDigits = int("".join(sumOfUnicodes[1:-1]))
    return (firstAndLastDigit**2)*(middleDigits**2)

mainMenu()
connectionToDatabase.commit()
connectionToDatabase.close()
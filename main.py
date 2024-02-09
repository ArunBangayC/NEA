import sqlite3

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
        self.__firstName = firstName
        self.__lastName = lastName
        self.__username = username
        self.__hashedPassword = User.__hashFunction(password)
    
    def createNewUser(self):
        addUserToDatabase = """
        INSERT INTO Users(firstName,lastName,masterUsername,masterHashedPassword)
        VALUES (?,?,?,?)
        """
        cursor.execute(addUserToDatabase,(self.__firstName,self.__lastName,self.__username,self.__hashedPassword))
    
    def loginUser(username,password):
        checkUserInDatabase = """
        SELECT masterUsername,masterHashedPassword
        FROM Users
        WHERE masterUsername = ? AND masterHashedPassword = ?
        """
        password = User.__hashFunction(password)
        cursor.execute(checkUserInDatabase,(username,password))
        usernameAndPassword = cursor.fetchone()
        if usernameAndPassword[0] == username and usernameAndPassword[1] == password:
            print("\nYou have successfully logged in!")
            return True
        else:
            print("\nHmmmmmm, it looks like the username or password you entered is incorrect... Please try again.")
            return False

    def __hashFunction(password):
        #sumOfPassword is the sum of all the squared unicode numerical codes from the password
        sumOfPassword = 0
        password  = list(password)
        for i in range(len(password)):
            sumOfPassword += (ord(password[i]))**2
        listOfSumOfPassword = list(str(sumOfPassword))
        firstAndLastDigit = int(listOfSumOfPassword[0] + listOfSumOfPassword[-1])
        middleDigits = int("".join(listOfSumOfPassword[1:-1]))
        productOfSquares = ((firstAndLastDigit**2)*(middleDigits**2))**2
        finalHash = hex(productOfSquares ^ sumOfPassword)
        return finalHash


def mainMenu():
    #Makes a variable for a while loop in case the user doesn't enter L or A
    LorA = False
    while LorA != True:
        #Gives user options of what they would like to do
        loginOrAdd = input("\nWould you like to login or add a new user? (L or A):  ")
        #Gives the user the options for logging in
        if loginOrAdd.lower() == "l":
            LorA = True
            loginAttempt = False
            while loginAttempt != True:
                username = input("\nPlease enter your username/email here:   ")
                username.lower()
                password = input("\nPlease enter your password here:    ")
                try: 
                    if User.loginUser(username,password) == True:
                        loginAttempt = True
                    else:
                        loginAttempt = False
                except:
                    print("\nHmmmmmm, it looks like the information you entered is incorrect... Please try again.")
                    loginAttempt = False
        #Takes user input for adding a new user
        elif loginOrAdd.lower() == "a":
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
                            newUser._User__createNewUser()
                        else:
                            print("\n Hmmmmmm, the passwords you entered do not match...  Please try again.")
                            correctPassword = False
                else:
                    print("\n Hmmmmmm, the usernames you entered do not match...  Please try again.")
                    correctUsername = False
        else:
            print("\n Oops, looks like you didn't enter L or A... Try again!")

mainMenu()
connectionToDatabase.commit()
connectionToDatabase.close()
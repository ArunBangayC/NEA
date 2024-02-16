class User():
    def __init__(self,firstName,lastName,username,password):
        self.__firstName = firstName
        self.__lastName = lastName
        self.__username = username
        self.__hashedPassword = User
    
    def createNewUser(self,cursor):
        addUserToDatabase = """
        INSERT INTO Users(firstName,lastName,masterUsername,masterHashedPassword)
        VALUES (?,?,?,?)
        """
        cursor.execute(addUserToDatabase,(self.__firstName,self.__lastName,self.__username,self.__hashedPassword))
    
    def loginUser(username,password,cursor):
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
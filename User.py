from encryption import keyGeneration

class User():
    def __init__(self,username,password):
        self.__username = username
        self.__hashedPassword = self.__hashFunction(password)

    def retrieveInfo(self,cursor):
        try:
            userID = self.userID(cursor)
            grabInfo = """
            SELECT itemName,username
            FROM Password Vault
            WHERE userID = ?"""
            userInfo = cursor.execute(grabInfo,(userID))
            return userInfo
        except:
            print("\nIt looks like we couldn't find your passwords... Please try again.")
            return False
        
    def addItem(self,itemName,username,password,cursor):
        try:
            userID = self.userID(cursor)
            encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration(password)
            addItem = """
            INSERT INTO "Password Vault"(userID,itemName,username,encryptedPassword,originalLengthOfPassword,paddedd)
            VALUES (?,?,?,?,?,?)"""
            cursor.execute(addItem,(userID,itemName,username,encryptedPassword,originalLengthOfPassword,padded))
            print("\nYou have successfully added a new item!")
        except:
            print("\nIt looks like we couldn't add your item... Please try again.")
            return False

    def loginUser(username,password,cursor):
        checkUserInDatabase = """
        SELECT masterUsername,masterHashedPassword
        FROM Logins
        WHERE masterUsername = ? AND masterHashedPassword = ?
        """
        password = User.__hashFunction(password)
        cursor.execute(checkUserInDatabase,(username,password))
        usernameAndPassword = cursor.fetchone()
        if usernameAndPassword[0] == username and usernameAndPassword[1] == password:
            print("\nYou have successfully logged in!")
            grabUserInfo = """
            SELECT userID,firstName,lastName
            FROM Logins
            WHERE masterUsername = ? AND masterHashedPassword = ?
            """
            userInfo = cursor.execute(grabUserInfo,(username,password))
            return userInfo
        else:
            print("\nHmmmmmm, it looks like the username or password you entered is incorrect... Please try again.")
            return False

    def userID(self,cursor):
        getUserID = """
            SELECT userID
            FROM Logins
            WHERE masterUsername = ?"""
        return cursor.execute(getUserID,(self.__username))

    @staticmethod
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

class NewUser(User):
    def __init__ (self,username,password,firstName,lastName,):
        super().__init__(username,password)
        self.__firstName = firstName
        self.__lastName = lastName
    def createNewUser(self,cursor):
        addUserToDatabase = """
        INSERT INTO Logins(firstName,lastName,masterUsername,masterHashedPassword)
        VALUES (?,?,?,?)
        """
        cursor.execute(addUserToDatabase,(self.__firstName,self.__lastName,self._User__username,self._User__hashedPassword))
        print("\nYou have successfully added a new user!")
        grabUserInfo = """
        SELECT userID
        FROM Logins
        WHERE firstName = ? AND lastName = ?
        """
        userID = cursor.execute(grabUserInfo,(self.__firstName,self.__lastName))
        return userID,self.__firstName,self.__lastName
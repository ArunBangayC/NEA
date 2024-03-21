from encryption import keyGeneration
from tabulate import tabulate   

class User():
    def __init__(self,username,password):
        self.__username = username
        self.__hashedPassword = self.__hashFunction(password)

    def retrieveInfo(self,cursor):
        userID = self.__userID(cursor)
        grabInfo = """
        SELECT itemName,username
        FROM "Password Vault"
        WHERE userID = ?"""
        userInfo = cursor.execute(grabInfo,(userID,))
        userInfo = cursor.fetchall()
        for i in range(len(userInfo)):
            print("\nItem Name: ",userInfo[i][0],"\nUsername: ",userInfo[i][1])
        
        '''
        except:
            print("\nIt looks like we couldn't find your passwords... Please try again.")
            return False
            '''
            
    def addItem(self,itemName,username,password,cursor):
        try:
            userID = self.__userID(cursor)
            encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration(password)
            print(userID,itemName,username,encryptedPassword,encryptedDEK,originalLengthOfPassword,paddedPassword) 
            addItemToPasswordVault = """
                INSERT INTO "Password Vault" (userID,itemName,username,encryptedPassword,encryptedDEK,originalLengthOfPassword,padded)
                VALUES (?,?,?,?,?,?,?)"""
            cursor.execute(addItemToPasswordVault, (userID,itemName,username,encryptedPassword,encryptedDEK,originalLengthOfPassword,paddedPassword))
            itemID = self.__itemID(cursor)
            addItemToKEKs = """
                INSERT INTO "KEKs"(itemID,KEK,padded)
                VALUES (?,?,?)"""
            cursor.execute(addItemToKEKs,(itemID,KEK,paddedDEK))
            print("\nYou have successfully added a new item!")
            return True
        except:
            print("\nIt looks like we couldn't add your item... Please try again.")
            return False
    
    def __itemID(self,cursor):
        getItemID = """
            SELECT itemID
            FROM "Password Vault"
            WHERE userID = ?"""
        userID = (self.__userID(cursor))
        cursor.execute(getItemID,(userID,))
        return cursor.fetchone()[0]
    
    def __userID(self,cursor):
        getUserID = """
            SELECT userID
            FROM Logins
            WHERE masterUsername = ?"""
        cursor.execute(getUserID,(self.__username,))
        return cursor.fetchone()[0]

    
    @staticmethod
    def loginUser(username, password, cursor):
        checkUserInDatabase = """
        SELECT masterUsername, masterHashedPassword
        FROM Logins
        WHERE masterUsername = ? AND masterHashedPassword = ?
        """
        hashedPassword = User.__hashFunction(password)
        cursor.execute(checkUserInDatabase, (username, hashedPassword))
        usernameAndPassword = cursor.fetchone()
        try:
            if usernameAndPassword[0] == username and usernameAndPassword[1] == hashedPassword:
                print("\nYou have successfully logged in!")
                grabUserInfo = """
                SELECT userID, firstName, lastName
                FROM Logins
                WHERE masterUsername = ? AND masterHashedPassword = ?
                """
                userInfo = cursor.execute(grabUserInfo, (username, hashedPassword))
                return userInfo
            else:
                print("\nHmmmmmm, it looks like the username or password you entered is incorrect... Please try again.")
                return False
        except:
            print("\nHmmmmmm, it looks like the username or password you entered is incorrect... Please try again.")
            return False

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
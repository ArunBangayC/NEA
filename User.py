import getpass
import csv
from tabulate import tabulate
from accessLog import addToAccessLogs
from randomGeneration import randomGeneration
from encryption import keyGeneration
from decryption import decryption

class User():
    def __init__(self,username,password):
        self.__username = username
        self.__hashedPassword = self.__hashFunction(password)

    def updateInfo(self,cursor):
        userID = self.__userID(cursor)
        itemToUpdate = input("\nPlease enter the name of the application or website that you want to update: ")
        getItemId = """
        SELECT itemID,itemName
        FROM "Password Vault"
        WHERE userID = ?"""
        cursor.execute(getItemId,(userID,))
        itemInfo = cursor.fetchall()
        for i in itemInfo:
            if (i[1]).lower() == itemToUpdate.lower():
                itemID = i[0]
                break

        infoToUpdate = input("\nWould you like to update your item name, username, or password? (I, U, P): ")
        while True:
            if infoToUpdate.lower() == "i":
                try:
                    while True:
                        newItemName = input("\nPlease enter the new item name: ")
                        correctItemName = input("\nIs this the correct item name? (Y or N): ")
                        if correctItemName.lower() == "y" or correctItemName == "":
                            break
                        else:
                            continue
                    updateItemName = """
                    UPDATE "Password Vault"
                    SET itemName = ?
                    WHERE itemID = ?"""
                    cursor.execute(updateItemName,(newItemName,itemID))
                    print("\nYou have successfully updated the item name!")
                    addToAccessLogs(("updatedNameFor"+itemToUpdate+"To"+newItemName),userID,itemID,cursor)
                    return True
                except:
                    print("\nIt looks something went wrong... Please try again.")
                    return False
            
            elif infoToUpdate.lower() == "u":
                try:
                    while True:
                            newUsername = input("\nPlease enter the new username: ")
                            correctUserame = input("\nIs this the correct username? (Y or N): ")
                            if correctUserame.lower() == "y" or correctUserame == "":
                                break
                            else:
                                continue
                    updateUsername = """
                    UPDATE "Password Vault"
                    SET username = ?
                    WHERE itemID = ?"""
                    cursor.execute(updateUsername,(newUsername,itemID))
                    print("\nYou have successfully updated the username!")
                    addToAccessLogs(("updatedUsernameFor"+itemToUpdate),userID,itemID,cursor)
                    return True
                except:
                    print("\nIt looks something went wrong... Please try again.")
                    return False
            
            elif infoToUpdate.lower() == "p":
                try:
                    while True:
                        optionToRandomlyGenerate = input("\nWould you like to randomly generate a password? (Y or N): ")
                        if optionToRandomlyGenerate.lower() == "y" or optionToRandomlyGenerate == "":
                            while True:
                                print("\nPlease randomly type on the keyboard: (Press the \"tab\" key to submit)")
                                randomlyGeneratedPassword = randomGeneration()
                                pressEnter = input("\nPress enter to submit your password: ")
                                if pressEnter == "":
                                    lengthOfRGPassword = 0
                                    for i in range(len(randomlyGeneratedPassword)-1,0,-1):
                                        if not str(randomlyGeneratedPassword[i]).isdigit():
                                            lengthOfRGPassword = str(i)
                                            break
                                    desriredLengthOfRGPassword = input("\nHow long would you like your password to be? (up to "+str(lengthOfRGPassword)+"): ")
                                    password = randomlyGeneratedPassword[:int(desriredLengthOfRGPassword)]
                                    print("\nHere is your password:"+password)
                                    userApproval = input("\nWould you like to submit this password? (Y): ")
                                    if userApproval.lower() == "y" or userApproval == "":
                                        encryptedPassword, encryptedDEK, KEK = keyGeneration(password)
                                        updatePassword = """
                                        UPDATE "Password Vault"
                                        SET encryptedPassword = ?, encryptedDEK = ?
                                        WHERE itemID = ?"""
                                        updateKEK = """
                                        UPDATE "KEKs"
                                        SET KEK = ?
                                        WHERE itemID = ?"""
                                        cursor.execute(updatePassword,(encryptedPassword,encryptedDEK,itemID))
                                        cursor.execute(updateKEK,(KEK,itemID))
                                        print("\nYou have successfully updated the password!")
                                        addToAccessLogs(("updatedPasswordFor"+itemToUpdate),userID,itemID,cursor)
                                        return True
                                    else:
                                        continue
                        elif optionToRandomlyGenerate.lower() == "n":
                            while True:
                                password = getpass.getpass("\nPlease enter your new password here : ")
                                correctPassword = input("\nAre you sure you want to submit this password? (Y or N): ")
                                if correctPassword.lower() == "y" or correctPassword == "":
                                    encryptedPassword, encryptedDEK, KEK = keyGeneration(password)
                                    updatePassword = """
                                    UPDATE "Password Vault"
                                    SET encryptedPassword = ?, encryptedDEK = ?
                                    WHERE itemID = ?"""
                                    updateKEK = """
                                    UPDATE "KEKs"
                                    SET KEK = ?
                                    WHERE itemID = ?"""
                                    cursor.execute(updatePassword,(encryptedPassword,encryptedDEK,itemID))
                                    cursor.execute(updateKEK,(KEK,itemID))
                                    print("\nYou have successfully updated the password!")
                                    addToAccessLogs(("updatedPasswordFor"+itemToUpdate),userID,itemID,cursor)
                                    return True
                                else:
                                    continue
                        else:
                            print("\nIt looks like you didn't enter an option... Please try again.")

                                    
                except:
                    print("\nIt looks something went wrong... Please try again.")
                    return False
            else:
                print("\nIt looks like you didn't enter an option... Please try again.")
                continue



    def retrieveLogins(self,cursor):
        try:
            userID = self.__userID(cursor)
            grabInfo = """
            SELECT itemName,username,itemID
            FROM "Password Vault"
            WHERE userID = ?"""
            cursor.execute(grabInfo,(userID,))
            userInfo = cursor.fetchall()

            #Makes a separate list of the item name and username that is given to the user, userInfo retains the itemID.
            itemNameAndUsername = []
            for i in userInfo:
                itemNameAndUsername.append((i[0],i[1]))

            print(tabulate(itemNameAndUsername,headers=["Item Name:","Username:"],tablefmt="simple_grid"))
        
            itemName = input("\nPlease enter the name of the application or website that you want to retrieve or enter \"update\"/\"U\" if you want to update information on an existing item: ")

            if itemName.lower() != "update" and itemName.lower() != "u":
                for i in userInfo:
                    if (i[0]).lower() == itemName.lower():
                        itemID = i[2]
                        break
                
                grabItemInfo = """
                SELECT itemName,username,encryptedPassword,encryptedDEK
                FROM "Password Vault"
                WHERE itemID = ?"""

                cursor.execute(grabItemInfo,(itemID,))
                itemInfo = cursor.fetchone()
                
                grabKEKInfo = """
                SELECT KEK
                FROM "KEKs"
                WHERE itemID = ?"""
                cursor.execute(grabKEKInfo,(itemID,))
                KEKInfo = cursor.fetchone()

                encryptedPassword = itemInfo[2]
                encryptedDEK = itemInfo[3]

                decryptedDEK = decryption(encryptedDEK,KEKInfo[0])
                password = decryption(encryptedPassword,decryptedDEK)

                print("\nItem Name: ",itemInfo[0])
                print("Username: ",itemInfo[1])
                print("Password: ",password)

                addToAccessLogs(("retrieveLoginFor"+itemInfo[0]),userID,itemID,cursor)
                return True
            else:
                self.updateInfo(cursor)
                return True
        except:
            print("\nIt looks like we couldn't find your passwords... Please try again.")
            return False
        
    def exportInfo(self,cursor):
        confirmation = input("\nAre you sure you would like to export your passwords? (please type \"yes\" in full): ")
        # try:
        if confirmation.lower() == "yes":
            getPasswordInfo = """
            SELECT pv.itemName, pv.username, pv.encryptedPassword, pv.encryptedDEK, k.KEK
            FROM "Password Vault" AS pv
            INNER JOIN "KEKs" AS k ON pv.itemID = k.itemID
            """
            cursor.execute(getPasswordInfo)
            passwordInfo = cursor.fetchall()

            exportInfo = []
            for item in passwordInfo:
                itemName,username,encryptedPassword,encryptedDEK, KEK = item
                decryptedDEK = decryption(encryptedDEK, KEK)
                decryptedPassword = decryption(encryptedPassword, decryptedDEK)
                decryptedPassword = decryptedPassword.replace("\x00","")
                exportInfo.append([itemName,username,decryptedPassword])
            
            filePath = input("\nPlease enter the file path where you would like to save your information: ")

            try:
                with open(filePath,"w",newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(['Item Name', 'Username', 'Password'])
                    for item in exportInfo:
                        file.write(item[0]+","+item[1]+","+item[2]+"\n")
                    return True
            except:
                print("\nIt looks like we couldn't find the file... Please try again.")
                return False

            
    def addItem(self,itemName,username,password,cursor):
        try:
            userID = self.__userID(cursor)
            encryptedPassword,encryptedDEK,KEK = keyGeneration(password)
            addItemToPasswordVault = """
                INSERT INTO "Password Vault" (userID,itemName,username,encryptedPassword,encryptedDEK)
                VALUES (?,?,?,?,?)"""
            cursor.execute(addItemToPasswordVault, (userID,itemName,username,encryptedPassword,encryptedDEK))
            itemID = self.__itemID(itemName,cursor)
            addItemToKEKs = """
                INSERT INTO "KEKs"(itemID,KEK)
                VALUES (?,?)"""
            cursor.execute(addItemToKEKs,(itemID,KEK))
            print("\nYou have successfully added a new item!")
            addToAccessLogs("addInformation",userID,itemID,cursor)
            return True
        except:
            print("\nIt looks like something went wrong... Please try again.")
            return False
    
    def __itemID(self,itemName,cursor):
        getItemID = """
            SELECT itemID
            FROM "Password Vault"
            WHERE userID = ? AND itemName = ?"""
        userID = (self.__userID(cursor))
        cursor.execute(getItemID,(userID,itemName))
        itemID = cursor.fetchall()
        return itemID[0][-1]
    
    def __userID(self,cursor):
        getUserID = """
            SELECT userID
            FROM "Logins"
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
                FROM "Logins"
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
        INSERT INTO "Logins"(firstName,lastName,masterUsername,masterHashedPassword)
        VALUES (?,?,?,?)
        """
        cursor.execute(addUserToDatabase,(self.__firstName,self.__lastName,self._User__username,self._User__hashedPassword))
        print("\nYou have successfully added a new user!")
        grabUserInfo = """
        SELECT userID
        FROM "Logins"
        WHERE firstName = ? AND lastName = ?
        """
        userID = cursor.execute(grabUserInfo,(self.__firstName,self.__lastName))
        return userID,self.__firstName,self.__lastName
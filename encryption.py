from randomGeneration import takingInputs

def encryption(password, DEK, KEK):
    def listOfUnicodes(parameter):
        listOfParameter = list(parameter)
        listOfUnicodes = []
        for i in range(len(listOfParameter)):
            listOfUnicodes.append(ord(listOfParameter[i]))
        return listOfUnicodes

    def matrixOperableLists(passwordList,DEKList):
        print("passwordList:",passwordList)
        lengthOfPL = len(passwordList)
        print(DEKList)
        separatedList = []
        
        def separateIntoListOf2x2Matrices(list):
            for i in range(0,lengthOfPL,4):
                miniList = passwordList[i:i+4]
                separatedList.append(miniList)
        
        def separateIntoListOf3x3Matrices(list):
            for i in range(0,lengthOfPL,9):
                miniList = passwordList[i:i+9]
                separatedList.append(miniList)

        def equalLength(passwordList,DEKList):
            lengthOfPL = len(passwordList)
            DEKList = DEKList[:lengthOfPL]
            return DEKList

        if lengthOfPL%4==0:
            DEKList = equalLength(passwordList,DEKList)
            passwordList = separateIntoListOf2x2Matrices(passwordList)
            DEKList = separateIntoListOf2x2Matrices(DEKList)
            return passwordList,DEKList
        elif lengthOfPL%9==0:
            DEKList = equalLength(passwordList,DEKList)
            passwordList = separateIntoListOf3x3Matrices(passwordList)
            DEKList = separateIntoListOf3x3Matrices(DEKList)
            return passwordList,DEKList
        else:
            for i in range(1,8):
                if (lengthOfPL+i)%9==0:
                    extractOfKEKList = DEKList[lengthOfPL+i-9:lengthOfPL]
            DEKList = equalLength(passwordList,DEKList)
            passwordList.append(extractOfKEKList)
            passwordList = separateIntoListOf3x3Matrices(passwordList)
            DEKList = separateIntoListOf3x3Matrices(DEKList)
            return passwordList,DEKList
    
    def multiplyingMatrices(matrix,multiplier):
        length = len(matrix)
        finalMatrix = []

        for i in range(length):
            row = []
            for j in range(length):
                row.append(0)
            finalMatrix.append(row)
        print("finalMatrix:",finalMatrix)

        for i in range(length):
            for j in range(length):
                for k in range(length):
                    finalMatrix[i][j] += matrix[i][k] * multiplier[k][j]

        return finalMatrix

    def is2x2MatrixSingular(matrix):
        #matrix is in form [[a,b],[c,d]]
        determinant = (matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0])
        if determinant == 0:
            return True
        else:
            return False
    
    def is3x3MatrixSingular(matrix):
        #matrix is in form [[a,b,c],[d,e,f],[g,h,i]]
        determinant = (matrix[0][0]*((matrix[1][1]*matrix[2][2])-(matrix[1][2]*matrix[2][1]))) - (matrix[0][1]*((matrix[1][0]*matrix[2][2])-(matrix[1][2]*matrix[2][0]))) + (matrix[0][2]*((matrix[1][0]*matrix[2][1])-(matrix[1][1]*matrix[2][0])))
        if determinant == 0:
            return True
        else:
            return False
    

        
    listOfPasswordCodes = listOfUnicodes(password)
    listOfDEKCodes = listOfUnicodes(DEK)

    XORpassword =[]
    for i in range(len(listOfPasswordCodes)):
        XORpassword.append(listOfPasswordCodes[i] ^ listOfDEKCodes[i])
    print("XOR password",XORpassword)
    
    separatedPasswordList = matrixOperableLists(XORpassword,listOfDEKCodes)

    #Code to shorten the DEK to the length of the password
    lengthOfPassword = len(separatedPasswordList)
    separatedDEKList = separatedDEKList[:lengthOfPassword]

    for i in range(len(separatedPasswordList)):
        lengthOfList = len(separatedPasswordList[i])
        print(lengthOfList)
        if lengthOfList == 4 and is2x2MatrixSingular(separatedDEKList[i]) == False:
            separatedPasswordList[i] = multiplyingMatrices(separatedDEKList[i],separatedDEKList[i])
        elif lengthOfList == 9 and is3x3MatrixSingular(separatedDEKList[i]) == False:
            separatedPasswordList[i] = multiplyingMatrices(separatedDEKList[i],separatedDEKList[i])
        elif lengthOfList == 4 and is2x2MatrixSingular(separatedDEKList[i]) == True:
            #The way I have designed how my program means that if the length of the matrix is a 2x2 matrix, any elements before is also a 2x2 matrix
            try:
                separatedPasswordList[i] = multiplyingMatrices(separatedPasswordList[i],separatedDEKList[i-1])
            except:
                return False
        elif lengthOfList == 9 and is3x3MatrixSingular(separatedDEKList[i]) == True:
            if len(separatedDEKList[i-1]) == 9:
                separatedPasswordList[i] = multiplyingMatrices(separatedPasswordList[i],separatedDEKList[i-1])
    return separatedPasswordList

def keyGeneration(password):
    print("Please randomly type on the keyboard: ")
    DEK = takingInputs(False)
    print("Please randomly type on the keyboard again: ")
    KEK = takingInputs(False)
    print(encryption(password,DEK,KEK))

password = "Password1234"
keyGeneration(password)
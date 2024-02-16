from randomGeneration import takingInputs

def encryption(password, DEK, KEK):
    def listOfUnicodes(parameter):
        listOfParameter = list(parameter)
        listOfUnicodes = []
        for i in range(len(listOfParameter)):
            listOfUnicodes.append(ord(listOfParameter[i]))
        return listOfUnicodes

    def matrixOperableList(parameter):
        lengthOfParameter = len(parameter)
        separatedList = []
        if lengthOfParameter%4==0:
            for i in range(0,len(parameter),4):
                miniList = parameter[i:i+4]
                separatedList.append(miniList)
        elif lengthOfParameter%4==2:
            for i in range(0,len(parameter)-19,4):
                miniList = parameter[i:i+4]
                separatedList.append(miniList)
            separatedList.append(parameter[lengthOfParameter-18:lengthOfParameter])
        elif lengthOfParameter%9==0:
            for i in range(0,len(parameter),9):
                miniList = parameter[i:i+9]
                separatedList.append(miniList)
        elif lengthOfParameter%4 == 3:
            if (lengthOfParameter-9)%4 == 2:
                for i in range(0,lengthOfParameter-14,4):
                    miniList = parameter[i:i+4]
                    separatedList.append(miniList)
                separatedList.append(parameter[lengthOfParameter-13:lengthOfParameter-12])
                for i in range(lengthOfParameter-11,lengthOfParameter-1,3):
                    miniList = parameter[i:i+3]
                    separatedList.append(miniList)
            else:
                for i in range(0,lengthOfParameter-11,4):
                    miniList = parameter[i:i+4]
                    print(miniList)
                    separatedList.append(miniList)
                separatedList.append(parameter[lengthOfParameter-10:lengthOfParameter-1])
        return separatedList
    
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

    #Code to shorten the DEK to the length of the password
    lengthOfPassword = len(listOfPasswordCodes)
    listOfDEKCodes = listOfDEKCodes[:lengthOfPassword]

    XORpassword =[]
    for i in range(len(listOfPasswordCodes)):
        XORpassword.append(listOfPasswordCodes[i] ^ listOfDEKCodes[i])
    print("XOR password",XORpassword)
    
    separatedPasswordList = matrixOperableList(XORpassword)
    separatedDEKList = matrixOperableList(listOfDEKCodes)

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
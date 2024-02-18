from randomGeneration import takingInputs

def encryption(password, DEK, KEK):
    def listOfUnicodes(parameter):
        listOfParameter = list(parameter)
        listOfUnicodes = []
        for i in range(len(listOfParameter)):
            listOfUnicodes.append(ord(listOfParameter[i]))
        return listOfUnicodes

    def matrixOperableLists(passwordList,DEKList):
        originalLengthOfPL = len(passwordList)
        
        def separateIntoListOf2x2Matrices(list):
            separatedList = []
            for i in range(0,len(list),4):
                miniList = list[i:i+4]
                separatedList.append(miniList)
            for i in range(len(separatedList)):
                separatedList[i] = [separatedList[i][:2],separatedList[i][2:]]
            return separatedList
        
        def separateIntoListOf3x3Matrices(list):
            separatedList = []
            for i in range(0,len(list),9):
                miniList = list[i:i+9]
                separatedList.append(miniList)
            for i in range(len(separatedList)):
                separatedList[i] = [separatedList[i][:3],separatedList[i][3:6],separatedList[i][6:9]]
            return separatedList

        def equalLength(DEKList):
            DEKList = DEKList[:newLengthOfPL]
            return DEKList

        if originalLengthOfPL%4==0:
            DEKList = equalLength(DEKList)
            passwordList = separateIntoListOf2x2Matrices(passwordList)
            DEKList = separateIntoListOf2x2Matrices(DEKList)
            return passwordList,DEKList
        elif originalLengthOfPL%9==0:
            DEKList = equalLength(DEKList)
            passwordList = separateIntoListOf3x3Matrices(passwordList)
            DEKList = separateIntoListOf3x3Matrices(DEKList)
            return passwordList,DEKList
        else:
            nextMultipleOf9 = originalLengthOfPL + (9 - originalLengthOfPL%9)
            extractOfDEKList = DEKList[originalLengthOfPL:nextMultipleOf9]
            passwordList += extractOfDEKList
            newLengthOfPL = len(passwordList)
            DEKList = equalLength(DEKList)
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
    
    separatedPasswordList,separatedDEKList = matrixOperableLists(XORpassword,listOfDEKCodes)
    print("separatedPasswordList:",separatedPasswordList)
    print("separatedDEKList:",separatedDEKList)

    for i in range(len(separatedPasswordList)):
        lengthOfList = len(separatedPasswordList[i])
        if lengthOfList == 4:
            if is2x2MatrixSingular(separatedDEKList[i]) == False:
                separatedPasswordList[i] = multiplyingMatrices(separatedPasswordList[i],separatedDEKList[i])
            else:
                #The way I have designed how my program means that if the length of the matrix is a 2x2 matrix, any elements before is also a 2x2 matrix
                try:
                    separatedPasswordList[i] = multiplyingMatrices(separatedPasswordList[i],separatedDEKList[i-1])
                except:
                    return False
        elif lengthOfList == 9:
            if is3x3MatrixSingular(separatedDEKList[i]) == False:
                separatedPasswordList[i] = multiplyingMatrices(separatedPasswordList[i],separatedDEKList[i])
            else:
                if len(separatedDEKList[i-1]) == 9:
                    separatedPasswordList[i] = multiplyingMatrices(separatedPasswordList[i],separatedDEKList[i-1])
    return separatedPasswordList

def keyGeneration(password):
    print("Please randomly type on the keyboard: ")
    DEK = takingInputs(False)
    print("Please randomly type on the keyboard again: ")
    KEK = takingInputs(False)
    print("final: ",encryption(password,DEK,KEK))

password = "Password123"
keyGeneration(password)
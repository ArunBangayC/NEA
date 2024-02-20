from randomGeneration import takingInputs

def listOfUnicodes(parameter):
        listOfParameter = list(parameter)
        listOfUnicodes = []
        for i in range(len(listOfParameter)):
            listOfUnicodes.append(ord(listOfParameter[i]))
        return listOfUnicodes

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

def matrixOperableLists(textList,keyList):
    originalLengthOfT = len(textList)

    def equalLength(keyList,lengthOfT):
        keyList = keyList[:lengthOfT]
        return keyList

    if originalLengthOfT%4==0:
        keyList = equalLength(keyList,originalLengthOfT)
        textList = separateIntoListOf2x2Matrices(textList)
        keyList = separateIntoListOf2x2Matrices(keyList)
        return textList,keyList
    elif originalLengthOfT%9==0:
        keyList = equalLength(keyList,originalLengthOfT)
        textList = separateIntoListOf3x3Matrices(textList)
        keyList = separateIntoListOf3x3Matrices(keyList)
        return textList,keyList
    else:
        nextMultipleOf9 = originalLengthOfT + (9 - originalLengthOfT%9)
        extractOfkeyList = keyList[originalLengthOfT:nextMultipleOf9]
        textList += extractOfkeyList
        newLengthOfT = len(textList)
        keyList = equalLength(keyList,newLengthOfT)
        textList = separateIntoListOf3x3Matrices(textList)
        keyList = separateIntoListOf3x3Matrices(keyList)
        return textList,keyList

def multiplyingMatrices(matrix, multiplier):
    endProduct = []
    for a in range(len(matrix)):
        finalMatrix = []
        matrixSublist = matrix[a]
        multiplierSublist = multiplier[a]
        for i in range(len(matrixSublist)):
            row = []
            for j in range(len(matrixSublist)):
                row.append(0)
            finalMatrix.append(row)
        for i in range(len(matrixSublist)):
            for j in range(len(matrixSublist)):
                for k in range(len(matrixSublist)):
                    finalMatrix[i][j] += matrixSublist[i][k]*multiplierSublist[k][j]
        endProduct.append(finalMatrix)
    return endProduct

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
    
def XORList(list,key):
    XORtext =[]
    for i in range(len(list)):
        XORtext.append(list[i] ^ key[i])
    return XORtext

def encryption(plaintext, key):
    listOfPlaintextCodes = listOfUnicodes(plaintext)
    listOfKeyCodes = listOfUnicodes(key)
    
    XORPlaintextCodes = XORList(listOfPlaintextCodes,listOfKeyCodes)

    separatedPlaintextList,separatedKeyList = matrixOperableLists(XORPlaintextCodes,listOfKeyCodes)

    for i in range(len(separatedPlaintextList)):
        lengthOfList = len(separatedPlaintextList[i])
        if lengthOfList == 4:
            if is2x2MatrixSingular(separatedKeyList[i]) == False:
                separatedPlaintextList[i] = multiplyingMatrices(separatedPlaintextList[i],separatedKeyList[i])
            else:
                keyGeneration(plaintext)
        elif lengthOfList == 9:
            if is3x3MatrixSingular(separatedKeyList[i]) == False:
                separatedPlaintextList[i] = multiplyingMatrices(separatedPlaintextList[i],separatedKeyList[i])
            else:
                keyGeneration(plaintext)
    return separatedPlaintextList,separatedKeyList

def keyGeneration(password):
    print("Please randomly type on the keyboard: ")
    DEK = takingInputs(False)
    print("Please randomly type on the keyboard again: ")
    KEK = takingInputs(False)
    encryptedPassword,DEKList = encryption(password,DEK)
    print("encryptedPassword: ",encryptedPassword)
    print("DEK: ",DEK)
    '''
    encryptedPassword = encryption(password,DEK)
    encryptedDEK = encryption(DEK,KEK)
    print("encryptedPassword: ",encryptedPassword)
    print("DEK: ",DEK)
    return encryptedPassword,encryptedDEK


print(keyGeneration("password"))
'''
from randomGeneration import randomGeneration

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

def equalLength(keyList,lengthOfT):
    keyList = keyList[:lengthOfT]
    return keyList

def matrixOperableLists(textList,keyList,originalLengthOfP):
    if originalLengthOfP%4==0:
        keyList = equalLength(keyList,originalLengthOfP)
        textList = separateIntoListOf2x2Matrices(textList)
        keyList = separateIntoListOf2x2Matrices(keyList)
        return textList,keyList
    elif originalLengthOfP%9==0:
        keyList = equalLength(keyList,originalLengthOfP)
        textList = separateIntoListOf3x3Matrices(textList)
        keyList = separateIntoListOf3x3Matrices(keyList)
        return textList,keyList
    else:
        nextMultipleOf9 = originalLengthOfP + (9 - originalLengthOfP%9)
        extractOfkeyList = keyList[originalLengthOfP:nextMultipleOf9]
        textList += extractOfkeyList
        newLengthOfP = len(textList)
        keyList = equalLength(keyList,newLengthOfP)
        textList = separateIntoListOf3x3Matrices(textList)
        keyList = separateIntoListOf3x3Matrices(keyList)
        return textList,keyList


def multiplyingMatrices(matrix, multiplier):
    finalMatrix = []

    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            row.append(0)
        finalMatrix.append(row)
    
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                finalMatrix[i][j] += matrix[i][k]*multiplier[k][j]

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
    
def XORList(list,key):
    XORtext = []
    for i in range(len(list)):
        XORtext.append(list[i] ^ key[i])
    return XORtext

def settingLengthOfKeys(ciphertext,key):
        if len(ciphertext)%4 != 0 and len(ciphertext)%9 != 0:
            nextMultipleOf9 = len(ciphertext) + (9 - len(ciphertext)%9)
            key = key[:nextMultipleOf9]
        elif len(ciphertext)%4 == 0 or len(ciphertext)%9 == 0:
            key = key[:len(ciphertext)]
        return key

def encryption(plaintext,key):
    listOfPlaintextCodes = listOfUnicodes(plaintext)
    listOfKeyCodes = listOfUnicodes(key)
    
    originalLengthOfP = len(plaintext)
    XORKeyCodes = equalLength(listOfKeyCodes,originalLengthOfP)

    XORPlaintextCodes = XORList(listOfPlaintextCodes,XORKeyCodes)

    separatedPlaintextList,separatedKeyList = matrixOperableLists(XORPlaintextCodes,listOfKeyCodes,originalLengthOfP)

    encryptedMatrix = []
    for i in range(len(separatedPlaintextList)):
        lengthOfList = len(separatedPlaintextList[i])
        if lengthOfList == 2:
            if is2x2MatrixSingular(separatedKeyList[i]) == False:
                encryptedMatrix.append(multiplyingMatrices(separatedPlaintextList[i],separatedKeyList[i]))
        elif lengthOfList == 3:
            if is3x3MatrixSingular(separatedKeyList[i]) == False:
                encryptedMatrix.append(multiplyingMatrices(separatedPlaintextList[i],separatedKeyList[i]))
        else:
            keyGeneration(plaintext)

    # Addition for 3NF
    hexMatrix = []
    lengthsOfMatrices = []
    for i in range(len(encryptedMatrix)):
        for j in range(len(encryptedMatrix[i])):
            for k in range(len(encryptedMatrix[i][j])):
                hexMatrix.append(hex(encryptedMatrix[i][j][k]))
                lengthsOfMatrices.append(len(hex(encryptedMatrix[i][j][k])))

    encryptedPassword = "".join(hexMatrix)

    return encryptedPassword

def keyGeneration(password):
    print("\nPlease randomly type on the keyboard: (Press the \"tab\" key to submit)")
    DEK = randomGeneration()
    print("\nPlease randomly type on the keyboard again: (Press the \"tab\" key to submit)")
    KEK = randomGeneration()
    DEK = settingLengthOfKeys(password,DEK)
    KEK = settingLengthOfKeys(DEK,KEK)
    encryptedPassword = encryption(password,DEK)
    encryptedDEK = encryption(DEK, KEK)
    return encryptedPassword,encryptedDEK,KEK
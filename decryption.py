import json
from encryption import listOfUnicodes, separateIntoListOf2x2Matrices, separateIntoListOf3x3Matrices, XORList, multiplyingMatrices

def determinantOf2x2Matrix(matrix):
    return (matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0])

def determinantOf3x3Matrix(matrix):
    return (matrix[0][0]*determinantOf2x2Matrix([[matrix[1][1],matrix[1][2]],[matrix[2][1],matrix[2][2]]]))-(matrix[1][0]*determinantOf2x2Matrix([[matrix[0][1],matrix[0][2]],[matrix[2][1],matrix[2][2]]]))+(matrix[2][0]*determinantOf2x2Matrix([[matrix[0][1],matrix[0][2]],[matrix[1][1],matrix[1][2]]]))

def inverseOf2x2Matrix(matrix):
    #matrix is given as [[a,b],[c,d]]
    inverseMatrix = [[0,0],[0,0]]
    determinant = determinantOf2x2Matrix(matrix)
    reciprocalOfDeterminant = float(1/determinant)
    adjugateOfMatrix = [[matrix[1][1],(-1*matrix[0][1])],[(-1*matrix[1][0]),matrix[0][0]]]
    for i in range(len(adjugateOfMatrix)):
        for j in range(len(adjugateOfMatrix[i])):
            inverseMatrix[i][j] += (reciprocalOfDeterminant*float(adjugateOfMatrix[i][j]))
    return inverseMatrix

def inverseOf3x3Matrix(matrix):
    #matrix is given as [[a,b,c],[d,e,f],[g,h,i]]
    inverseMatrix = [[0,0,0],[0,0,0],[0,0,0]]
    determinant = determinantOf3x3Matrix(matrix)
    reciprocalOfDeterminant = 1/determinant
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            listOfRemainingRows = [0,1,2]
            listOfRemainingElements = [0,1,2]
            listOfRemainingRows.remove(i)
            listOfRemainingElements.remove(j)
            inverseMatrix[i][j] = determinantOf2x2Matrix([[matrix[listOfRemainingRows[0]][listOfRemainingElements[0]], matrix[listOfRemainingRows[0]][listOfRemainingElements[1]]], [matrix[listOfRemainingRows[1]][listOfRemainingElements[0]], matrix[listOfRemainingRows[1]][listOfRemainingElements[1]]]])
    for i in range(len(inverseMatrix)):
        if i != 1:
            inverseMatrix[i][1] *= -1
        else:
            inverseMatrix[i][0] *= -1
            inverseMatrix[i][2] *= -1
    
    def transposeMatrix(matrix):
        matrix[0][1],matrix[1][0] = matrix[1][0],matrix[0][1]
        matrix[0][2],matrix[2][0] = matrix[2][0],matrix[0][2]
        matrix[1][2],matrix[2][1] = matrix[2][1],matrix[1][2]
        return matrix
    
    inverseMatrix = transposeMatrix(inverseMatrix)

    for i in range(len(inverseMatrix)):
        for j in range(len(inverseMatrix)):
            inverseMatrix[i][j] *= reciprocalOfDeterminant
    return inverseMatrix

def decryption(ciphertext,key):
    lengthOfCiphertext = len(ciphertext)
    key = listOfUnicodes(key)
    
    def keyToMatrix(key):
        if len(key)%4 == 0:
            matrixKey = separateIntoListOf2x2Matrices(key)
            return matrixKey
        elif len(key)%9 == 0:
            matrixKey = separateIntoListOf3x3Matrices(key)
            return matrixKey
        else:
            nextMultipleOf9 = len(ciphertext) + (9 - len(ciphertext)%9)
            return separateIntoListOf3x3Matrices(key[:nextMultipleOf9])
    
    keyMatrix = keyToMatrix(key)

    inverseKey = []
    for i in range(len(keyMatrix)):
        if lengthOfCiphertext%4 == 0:
            inverseKey.append(inverseOf2x2Matrix(keyMatrix[i]))
        else:
            inverseKey.append(inverseOf3x3Matrix(keyMatrix[i]))

    print("ciphertext: ", ciphertext)
    print("inverseKey: ", inverseKey)
    result = multiplyingMatrices(ciphertext,inverseKey)

    ciphertextList = []
    keyMatrixList = []
    
    for i in range(len(ciphertext)):
        for j in range(len(ciphertext[i])):
            for k in range(len(ciphertext[i][j])):
                ciphertextList.append(ciphertext[i][j][k])

    for i in range(len(key)):
        keyMatrixList.append(key[i])

    
    XORciphertext = XORList(ciphertextList,keyMatrixList)
    for i in range(len(XORciphertext)):
        XORciphertext[i] = chr(XORciphertext[i])

    ciphertext = ''.join(XORciphertext)
    print("ciphertext: ", ciphertext)
    return ciphertext
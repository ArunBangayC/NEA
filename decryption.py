from encryption import listOfUnicodes, separateIntoListOf2x2Matrices, separateIntoListOf3x3Matrices, XORList

def determinantOf2x2Matrix(matrix):
    return (matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0])

def inverseOf2x2Matrix(matrix):
    #matrix is given as [[a,b],[c,d]]
    inverseMatrix = [[0,0],[0,0]]
    determinant = determinantOf2x2Matrix(matrix)
    reciprocalOfDeterminant = float(1/determinant)
    adjugateOfMatrix = [[matrix[1][1],(-1*matrix[0][1])],[(-1*matrix[1][0]),matrix[0][0]]]
    print(adjugateOfMatrix)
    for i in range(len(adjugateOfMatrix)):
        for j in range(len(adjugateOfMatrix[i])):
            inverseMatrix[i][j] += (reciprocalOfDeterminant*float(adjugateOfMatrix[i][j]))
    return inverseMatrix

def inverseOf3x3Matrix(matrix):
    #matrix is given as [[a,b,c],[d,e,f],[g,h,i]]
    inverseMatrix = [[0,0,0],[0,0,0],[0,0,0]]
    determinant = (matrix[0][0]*determinantOf2x2Matrix([[matrix[1][1],matrix[1][2]],[matrix[2][1],matrix[2][2]]]))-(matrix[1][0]*determinantOf2x2Matrix([[matrix[0][1],matrix[0][2]],[matrix[2][1],matrix[2][2]]]))+(matrix[2][0]*determinantOf2x2Matrix([[matrix[0][1],matrix[0][2]],[matrix[1][1],matrix[1][2]]]))
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

    key = listOfUnicodes(key)
    
    sumOfElements = 0
    for i in range(len(ciphertext)):
        for j in range(len(ciphertext[i])):
            for k in range(len(ciphertext[i][j])):
                sumOfElements += 1
    
    key = key[:sumOfElements]
    keyMatrix = keyToMatrix(key)
    print("keyMatrix: ",keyMatrix)

    inverseKey = []
    for i in range(len(ciphertext)):
        if sumOfElements%4 == 0:
            inverseKey.append(inverseOf2x2Matrix(keyMatrix[i]))
        else:
            inverseKey.append(inverseOf3x3Matrix(keyMatrix[i]))

    ciphertextList = []
    keyMatrixList = []
    for i in range(len(keyMatrix)):
        for j in range(len(keyMatrix)):
            for k in range(len(keyMatrix)):
                keyMatrixList.append(keyMatrix[i][j][k])
                ciphertextList.append(ciphertext[i][j][k])

    XORciphertext = XORList(ciphertextList,keyMatrixList)
    ciphertext = []
    for i in range(len(XORciphertext)):
        XORciphertext[i] = chr(XORciphertext[i])
    ciphertext = ''.join(XORciphertext)
    return ciphertext

print(decryption([[[48, 18], [73, 36]], [[70, 91], [64, 2]]],"@s:W142f8-26|YO&7e01020E163\89]81mo309an80rOA9|b2O3O302>\51789625462709646504122308875126078951622392920510153359360000000"))
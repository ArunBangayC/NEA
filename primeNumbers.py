def multiplyingMatrices(matrix,multiplier):
        length = len(matrix)
        finalMatrix = []

        for i in range(length):
            row = []
            for j in range(length):
                row.append(0)
            finalMatrix.append(row)
        print(finalMatrix)

        for i in range(length):
            for j in range(length):
                for k in range(length):
                    finalMatrix[i][j] += matrix[i][k] * multiplier[k][j]

        return finalMatrix

print(multiplyingMatrices([[1,2],[3,4]],[[5,6],[7,8]]))
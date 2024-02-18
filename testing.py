def multiplyingMatrices(matrix, multiplier):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                for l in range(len(matrix)):
                    matrix[i][k][l] = matrix[i][k][l] * multiplier[i][j][l]
    return matrix
matrix = [[[106, 20, 48], [51, 66, 30], [70, 93, 65]], [[4, 79, 57], [48, 52, 44], [55, 69, 49]]]
multiplier = [[[58, 117, 67], [64, 53, 113], [52, 57, 112]], [[54, 124, 57], [48, 52, 44], [55, 69, 49]]]

print(multiplyingMatrices(matrix, multiplier))
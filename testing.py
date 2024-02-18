def matrixOperableLists(passwordList,dEKList):
    lengthOfPL = len(passwordList)
    separatedList = []

    def separateIntoListOf2x2Matrices(list):
        for i in range(0,len(passwordList),4):
            miniList = passwordList[i:i+4]
            separatedList.append(miniList)
    
    def separateIntoListOf3x3Matrices(list):
        for i in range(0,len(passwordList),9):
            miniList = passwordList[i:i+9]
            separatedList.append(miniList)

    if lengthOfPL%4==0:
        separateIntoListOf2x2Matrices(passwordList)
    elif lengthOfPL%9==0:
        separateIntoListOf3x3Matrices(passwordList)
    else:
        for i in range(1,8):
            if (lengthOfPL+i)%9==0:
                extractOfKEKList = dEKList[lengthOfPL+i-9:lengthOfPL]
            passwordList.append(extractOfKEKList)
            separateIntoListOf3x3Matrices(passwordList)
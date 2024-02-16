def matrixOperableList(parameter):
    separatedList = []
    for i in range(0,len(parameter),4):
        miniList = parameter[i:i+4]
        separatedList.append(miniList)
    return separatedList

lis = [1,2,3,4,5,6,7,8,9,10]
print(matrixOperableList(lis))
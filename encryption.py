from randomGeneration import takingInputs

def listOfUnicodes(parameter):
    listOfParameter = list(parameter)
    listOfUnicodes = []
    for i in range(len(listOfParameter)):
        listOfUnicodes.append(ord(listOfParameter[i]))

def matrixOperableList(parameter):
    separatedList = []
    for i in range(0,len(parameter),4):
        miniList = parameter[i:i+4]
        separatedList.append(miniList)

def encryption(password, DEK, KEK):
    listOfPasswordCodes = listOfUnicodes(password)
    listOfDEKCodes = listOfUnicodes(DEK)
    XORpassword =[]
    for i in range(len(listOfPasswordCodes)):
        XORpassword.append(listOfPasswordCodes[i] ^ listOfDEKCodes[i])
    def 


def keyGeneration(password):
    print("Please randomly type on the keyboard: ")
    DEK = takingInputs()
    print("Please randomly type on the keyboard again: ")
    KEK = takingInputs()
    encryption(password,DEK,KEK)

password = "Password123"
keyGeneration(password)
def hashFunction(username,password):
    #sumOfPassword is the sum of all the squared unicode numerical codes from the password
    sumOfPassword = 0
    password  = list(password)
    for i in range(len(password)):
        sumOfPassword += (ord(password[i]))**2
    sumOfPassword = list(str(sumOfPassword))
    firstAndLastDigit = int(sumOfPassword[0] + sumOfPassword[-1])
    middleDigits = int("".join(sumOfPassword[1:-1]))
    productOfSquares = ((firstAndLastDigit**2)*(middleDigits**2))**2
    #sumOfUsername is the sum of all the unicode numerical codes from the username
    sumOfUsername = 0
    username = list(username)
    for i in range(len(username)):
        sumOfUsername += ord(username[i])
    finalHash = hex(productOfSquares ^ sumOfUsername)
    return finalHash

print(hashFunction("username","password"))
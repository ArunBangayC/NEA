    #Encodes the first digits
    sumOfLastTime = 0
    print(keyPressMilliseconds)
    first4Digits = False
    while first4Digits != True:
        for digit in str(keyPressMilliseconds[lastElementOfTimes]):
            digit = int(digit)
            sumOfLastTime += digit
            if digit < 4 and hasattr(next,"char"):
                largeRandomList[digit] = encoding[int(largeRandomList[digit])]
                first4Digits = True
            else:
                lessThan4 = False
                backOfList = -1
                while lessThan4 != True:
                    for next in str(keyPressMilliseconds[backOfList]):
                        try:
                            next = int(next)
                            if digit < 4 and hasattr(recordedKeyPresses[digit], "char"):
                                 largeRandomList[digit] = encoding[int(largeRandomList[digit])]
                                 first4Digits = True
                                 lessThan4 = True
                        except:
                            backOfList -= 1
                            lessThan4 = False

    #Encodes the other digits
    for time in keyPressMilliseconds:
        sumOfDigits = 0
        for digit in keyPressMilliseconds:
            sumOfDigits += digit
        if sumOfDigits % 2:
            index = (largeRandomList[sumOfDigits]*10) + (largeRandomList[sumOfDigits+1])
            if index <= 82:
                largeRandomList[sumOfDigits] = encoding[index]
                largeRandomList.remove(largeRandomList[sumOfDigits+1])
            else:
                largeRandomList[sumOfDigits] = encoding[sumOfDigits]

finalRandomNumber = ""
for element in largeRandomList:
    finalRandomNumber += largeRandomList[element]

print(finalRandomNumber)
from pynput import keyboard
import time
import psutil

encoding = ['g', ':', 's', '*', 'C', '@', 'y', 'L', 'W', 'u', '(', 'E', '=', 'O', 'q', '>', 'm', '{', 'x', 't', '!', 'K', 'S', '<', '/', 'V', 'B', ',', 'F', '+', 'J', 'U', 'b', 'o', 'M', 'Q', '&', 'Z', ';', 'N', 'T', '"', 'j', 'Y', 'w', 'X', 'G', '}', ']', '|', 'h', 'R', '-', '$', "'", 'p', 'D', '#', '\\', 'c', 'i', 'k', 'd', 'P', 'n', 'l', 'e', 'I', 'f', 'A', 'v', 'r', ')', '%', '[', '.', 'a', '_', 'H', 'z', '?']
len36 = False

def addLettersAndChars(keyPressMilliseconds,interruptsOnKeyPress,longRandomNumber):
    longRandomList = list(str(longRandomNumber))

    #Encodes the first digits
    lessThan4 = False
    while lessThan4 != True:
        for i in range(len(keyPressMilliseconds)):
            for digit in str(keyPressMilliseconds[i]):
                digit = int(digit)
                try:
                    if digit<4 and int(longRandomList[digit]):
                        longRandomList[digit] = encoding[int(longRandomList[digit])]
                        lessThan4 = True
                except:
                    pass

    #Encodes the other digits
    for i in range(len(keyPressMilliseconds)):
        sumOfDigits = 0
        for digit in str(keyPressMilliseconds[i]):
            sumOfDigits += int(digit)
        try:
            if int(longRandomList[sumOfDigits]) and int(longRandomList[sumOfDigits+1]):
                index = (int(longRandomList[sumOfDigits]))*10 + (int(longRandomList[sumOfDigits+1]))
                index = int(index)
                if sumOfDigits % 2 == 0 and index <= 81:
                    longRandomList[sumOfDigits] = encoding[index]
                    longRandomList.pop(sumOfDigits + 1)
                elif sumOfDigits % 2 == 1 and index <= 81:
                    longRandomList[sumOfDigits] = encoding[index]
        except:
            pass
    for i in range(len(interruptsOnKeyPress)):
        sumOfInterrupt = 0
        for interrupt in str(interruptsOnKeyPress[i]):
            try:
                if int(interrupt):
                    sumOfInterrupt += int(interrupt)
                    try:
                        if int(longRandomList[sumOfInterrupt]) and int(longRandomList[sumOfInterrupt+1]):
                            index = (int(longRandomList[sumOfInterrupt]))*10 + (int(longRandomList[sumOfInterrupt+1]))
                            index = int(index)
                            if sumOfInterrupt % 2 == 0 and index <= 81:
                                longRandomList[sumOfInterrupt] = encoding[index]
                                longRandomList.pop(sumOfInterrupt + 1)
                            elif sumOfInterrupt % 2 == 1 and index <= 81:
                                longRandomList[sumOfInterrupt] = encoding[index]
                    except:
                        pass
            except:
                pass
    randomPassword = longRandomList[:36]
    for i in range(len(randomPassword)):
        randomPassword[i] = str(randomPassword[i])
    randomPassword = ''.join(randomPassword)
    return randomPassword

def takingInputs():
    len36 = False
    while len36 != True:
        recordedKeyPresses = []
        keyPressTimes = []
        interruptsOnKeyPress = []
        keyPressMilliseconds = []

        def onPress(key):
            #Adds recorded key presses to recordedKeyPresses list
            recordedKeyPresses.append(key)
            keyPressTimes.append(int(time.monotonic()*1000))
            interrupt= psutil.cpu_stats().interrupts
            interruptsOnKeyPress.append(interrupt)

        def onRelease(key):
            #Stops the listener when enter is pressed
            if key == keyboard.Key.enter:
                return False
    
        #Starts the listener
        with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
            listener.join()

        sumOfUnicodes = 0
        for key in recordedKeyPresses:
            if hasattr(key, 'char'): #Checks if the key pressed is a character
                sumOfUnicodes += ord(key.char)

        productOfDigits = 1
        for time in keyPressTimes:
            last4Digits = time % 10000
            keyPressMilliseconds.append(last4Digits)
            productOfDigits *= last4Digits

        sumOfInterrupts = 0
        for i in range(len(interruptsOnKeyPress)):
            sumOfInterrupts += interruptsOnKeyPress[i]

        longRandomNumber = (productOfDigits*sumOfUnicodes*sumOfInterrupts)

        if len(str(longRandomNumber)) >= 36:
            len36 = True
            random = addLettersAndChars(keyPressMilliseconds,interruptsOnKeyPress,longRandomNumber)
            return random
        else:
            len36 = False
            print("You didn't type enough characters...  Try again!")
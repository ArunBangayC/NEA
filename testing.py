from pynput import keyboard
import time
import psutil

encoding = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", "|", "\\", ";", ":", "'", "\"", ",", "<", ".", ">", "/", "?"]
len36 = False

def addLettersAndChars(keyPressMilliseconds,largeRandomNumber):
    lengthOfTimes = len(keyPressMilliseconds)
    largeRandomList = list(str(largeRandomNumber))

    #Encodes the first digits
    lessThan4 = False
    while lessThan4 != True:
        for i in range(len(keyPressMilliseconds)):
            for digit in str(keyPressMilliseconds[i]):
                digit = int(digit)
                try:
                    if digit<4 and int(largeRandomList[digit]):
                        largeRandomList[digit] = encoding[int(largeRandomList[digit])]
                        lessThan4 = True
                except:
                    pass

    #Encodes the other digits
    for time in keyPressMilliseconds:
        sumOfDigits = 0
        for digit in keyPressMilliseconds:
            sumOfDigits += digit
        if sumOfDigits % 2:
            index = largeRandomList[sumOfDigits]*10 + largeRandomList[sumOfDigits+1]
            if index <= 82:
                largeRandomList[sumOfDigits] = encoding[index]
                largeRandomList.remove(largeRandomList[sumOfDigits+1])
        elif sumOfDigits % 2 == 1:
            largeRandomList[sumOfDigits] = encoding[index]
    randomPassword = largeRandomList[:36]
    randomPassword = ''.join(randomPassword)
    return randomPassword


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
        print(addLettersAndChars(keyPressMilliseconds,longRandomNumber))
    else:
        len36 = False
        print("You didn't type enough characters...  Try again!")


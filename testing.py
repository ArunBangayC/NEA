from pynput import keyboard
import time
import psutil

recordedKeyPresses = []
keyPressTimes = []
interruptsOnKeyPress = []

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

print("Sum of unicodes:",str(sumOfUnicodes))

sumOfTimes = 1
for time in keyPressTimes:
    last4Digits = time % 10000
    sumOfTimes = sumOfTimes * last4Digits

sumOfInterrupts = 0
for i in range(len(interruptsOnKeyPress)):
    sumOfInterrupts += interruptsOnKeyPress[0]

print("Sum of times:",str(sumOfTimes))

longRandomNumber = (sumOfTimes*sumOfUnicodes*sumOfInterrupts)

print("Long random number:",str(longRandomNumber))
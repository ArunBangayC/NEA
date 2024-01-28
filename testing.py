from pynput import keyboard
import time
import psutil

interrupts = psutil.cpu_stats().interrupts

recordedKeyPresses = []
keyPressTimes = []

def onPress(key):
    #Adds recorded key presses to recordedKeyPresses list
    recordedKeyPresses.append(key)
    keyPressTimes.append(int(time.monotonic()*1000))

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

print("Sum of times:",str(sumOfTimes))

longRandomNumber = (sumOfTimes*sumOfUnicodes*interrupts)

long_number = 12345678901234567890
unicode_representation = ""

# Convert each digit of the long number to its Unicode representation
for digit in str(longRandomNumber):
    unicode_representation += chr(ord(digit) + 65)  # Adding 65 to convert to Unicode characters
    
print("Unicode representation:", unicode_representation)

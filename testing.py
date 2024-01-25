from pynput import keyboard

recordedKeyPresses = []

def onPress(key):
    #Adds recorded key presses to recordedKeyPresses list
    recordedKeyPresses.append(str(key))

def kill(key):
    #Stops listening when enter is pressed
    if key == keyboard.Key.enter:
        return False
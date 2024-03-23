from encryption import keyGeneration
from decryption import decryption

encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration("Secure234")
print("\ndecryption: ",decryption(encryptedDEK,KEK)) 

# print(determinantOf3x3Matrix([[4, 85, 22], [95, 49, 92], [0, 0, 12]]))
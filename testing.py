from encryption import keyGeneration
from decryption import decryption,inverseOf3x3Matrix,determinantOf3x3Matrix

encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration("Secure2345678")
DEK = decryption(encryptedDEK,KEK)
print("ciphertext: ",decryption(encryptedPassword,DEK))

# print(inverseOf3x3Matrix([[4,8,9],[4,5,6],[7,8,9]]))
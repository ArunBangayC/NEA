from encryption import keyGeneration
from decryption import decryption

encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration("Secure2345678")
DEK = decryption(encryptedDEK,KEK)
print("ciphertext: ",decryption(encryptedPassword,DEK))
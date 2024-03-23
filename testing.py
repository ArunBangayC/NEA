from encryption import keyGeneration
from decryption import decryption

encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration("Secure2345")
DEK = decryption(encryptedDEK,KEK)
print(decryption(encryptedPassword,DEK))
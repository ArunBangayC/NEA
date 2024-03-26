from encryption import keyGeneration
from decryption import decryption,inverseOf3x3Matrix,determinantOf3x3Matrix

encryptedPassword,encryptedDEK,KEK= keyGeneration("pass")
DEK = decryption(encryptedDEK,KEK)
print(decryption(encryptedPassword,DEK))
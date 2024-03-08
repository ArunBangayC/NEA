from encryption import keyGeneration

encryptedPassword,encryptedDEK,KEK,originalLengthOfPassword,paddedPassword,paddedDEK = keyGeneration("Password123")

print(encryptedPassword)
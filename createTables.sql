-- Creates primary table "Logins"
-- Longest recorded full name is 49 characters, so VARCHAR(50) for first or last name will be more than sufficient.

CREATE TABLE IF NOT EXISTS "Logins"(
    "userID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "firstName" VARCHAR(50) NOT NULL,
    "lastName" VARCHAR(50) NOT NULL,
    "masterUsername" VARCHAR(50) NOT NULL,
    "masterHashedPassword" VARCHAR(255) NOT NULL
);


-- Creates table "Password Vault" to store user's encrypted passwords
CREATE TABLE IF NOT EXISTS "Password Vault"(
    "userID" INTEGER,   
    "itemID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "itemName" VARCHAR(50) NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "encryptedPassword" VARCHAR(255) NOT NULL,
    "encryptedDEK" VARCHAR(255) NOT NULL,
    "originalLengthOfPassword" INTEGER NOT NULL,
    "padded" BOOLEAN NOT NULL,
    "matrixLengths" INTEGER NOT NULL,
    FOREIGN KEY ("userID") REFERENCES "Logins"("userID")
);

CREATE TABLE IF NOT EXISTS "KEKs"(
    "itemID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "KEK" VARCHAR(255) NOT NULL,
    "padded" BOOLEAN NOT NULL,
    FOREIGN KEY ("itemID") REFERENCES "Password Vault"("itemID")
);

CREATE TABLE IF NOT EXISTS "Access Logs"( 
    "userID" INTEGER NOT NULL,
    "itemID" INTEGER NOT NULL,
    "dateCreated" DATETIME NOT NULL,
    "lastAccessed" DATETIME NOT NULL,
    "functionApplied" DATETIME NOT NULL,
    FOREIGN KEY ("userID") REFERENCES "Logins"("userID"),
    FOREIGN KEY ("itemID") REFERENCES "PasswordVault"("itemID")
)
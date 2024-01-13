-- Creates primary table "Users"
-- Longest recorded full name is 49 characters, so VARCHAR(50) for first or last name will be more than sufficient.

CREATE TABLE IF NOT EXISTS "Users"(
    "userID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "firstName" VARCHAR(50) NOT NULL,
    "lastName" VARCHAR(50) NOT NULL,
    "masterUsername" VARCHAR(50) NOT NULL,
    "masterHashedPassword" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Password Vault"(
    "userID" INTEGER NOT NULL,
    "itemName" VARCHAR(50) NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "encryptedPassword" VARCHAR(255) NOT NULL,
    FOREIGN KEY ("userID") REFERENCES "Users"("userID")
)
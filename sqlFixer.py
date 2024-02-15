import sqlite3

connectionToDatabase = sqlite3.connect("/home/arun/Documents/NEA/mainDatabase.db")
cursor = connectionToDatabase.cursor()

deleteTables = """
DROP TABLE IF EXISTS "Users";
DROP TABLE IF EXISTS "Password Vault"
"""
cursor.executescript(deleteTables)
connectionToDatabase.commit()
connectionToDatabase.close()
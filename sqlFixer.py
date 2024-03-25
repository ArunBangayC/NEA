import sqlite3

connectionToDatabase = sqlite3.connect("/home/arun/Documents/NEA/mainDatabase.db")
cursor = connectionToDatabase.cursor()

deleteTables = """
DROP TABLE IF EXISTS "Logins";
DROP TABLE IF EXISTS "Password Vault";
DROP TABLE IF EXISTS "KEKs";
DROP TABLE IF EXISTS "AccessLogs"
"""
cursor.executescript(deleteTables)
connectionToDatabase.commit()
connectionToDatabase.close()
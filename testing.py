import sqlite3
connectionToDatabase = sqlite3.connect("/home/arun/Documents/NEA/mainDatabase.db")
cursor = connectionToDatabase.cursor()

query = "DROP TABLE IF EXISTS Users"

cursor.execute(query)
connectionToDatabase.close()
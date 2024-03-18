from User import User
import sqlite3

connectionToDatabase = sqlite3.connect("/home/arun/Documents/NEA/mainDatabase.db")
cursor = connectionToDatabase.cursor()

with open("createTables.sql","r") as createTablesFile:
    createTables = createTablesFile.read()
    cursor.executescript(createTables)
    connectionToDatabase.commit()

    getUserID = """
        SELECT userID
        FROM Logins"""
    cursor.execute(getUserID)
    print(cursor.fetchone())

connectionToDatabase.commit()
connectionToDatabase.close()
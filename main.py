import sqlite3
import menu as menu

#Connecting to SQL database and creating cursor
connectionToDatabase = sqlite3.connect("/home/arun/Documents/NEA/mainDatabase.db")
cursor = connectionToDatabase.cursor()

with open("createTables.sql","r") as createTablesFile:
    createTables = createTablesFile.read()
    cursor.executescript(createTables)
    connectionToDatabase.commit()
    
#Calls the mainMenu function from the menu.py file
menu.mainMenu(cursor)
connectionToDatabase.commit()
connectionToDatabase.close()
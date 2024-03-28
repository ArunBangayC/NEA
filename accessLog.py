from datetime import datetime

def addToAccessLogs(functionApplied,userID,itemID,cursor):
    currentDateTime = datetime.now().isoformat()
    if functionApplied == "addInformation" or functionApplied == "createNewUser":
        if functionApplied == "addInformation":
            getItemName = """
            SELECT itemName
            FROM "Password Vault"
            WHERE itemID = ?
            """
            cursor.execute(getItemName,(itemID,))
            itemName = cursor.fetchone()[0]
            addToLog ="""
            INSERT INTO "Access Logs"(userID,itemID,dateCreated,lastAccessed,functionApplied)
            VALUES(?,?,?,?,?)
            """
            cursor.execute(addToLog,(userID,itemID,currentDateTime,currentDateTime,(functionApplied+itemName)))
        else:
            getUsername = """
            SELECT masterUsername
            FROM "Logins"
            WHERE userID = ?
            """
            cursor.execute(getUsername,(userID,))
            username = cursor.fetchone()[0]
            addToLog ="""
            INSERT INTO "Access Logs"(userID,itemID,dateCreated,lastAccessed,functionApplied)
            VALUES(?,?,?,?,?)
            """
            cursor.execute(addToLog,(userID,itemID,currentDateTime,currentDateTime,(functionApplied+username)))
    else:
        getDateCreated ="""
        SELECT dateCreated
        FROM "Access Logs"
        WHERE itemID = ?
        """
        cursor.execute(getDateCreated,(itemID,))
        dateCreated = cursor.fetchall()
        if len(dateCreated) > 0:
            addToLog ="""
            INSERT INTO "Access Logs"(userID,itemID,dateCreated,lastAccessed,functionApplied)
            VALUES(?,?,?,?,?)
            """
            cursor.execute(addToLog,(userID,itemID,dateCreated[0][0],currentDateTime,functionApplied))
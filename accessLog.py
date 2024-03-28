from datetime import datetime

def addToAccessLogs(functionApplied,userID,itemID,cursor):
    currentDateTime = datetime.now().isoformat()
    if functionApplied == "addInformation" or functionApplied == "createNewUser":
        addToLog ="""
        INSERT INTO "Access Logs"(userID,itemID,dateCreated,lastAccessed,functionApplied)
        VALUES(?,?,?,?,?)
        """
        cursor.execute(addToLog,(userID,itemID,currentDateTime,currentDateTime,functionApplied))
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
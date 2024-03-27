from datetime import datetime

def addToAccessLogs(functionApplied,userID,itemID,cursor):
    currentDateTime = datetime.now()
    if functionApplied == "addInformation" or functionApplied == "createNewUser":
        addToLog = '''
        INSERT INTO "Access Logs"(userID,itemID,dateCreated,lastAccessed,functionApplied)
        VALUES(?,?,?,?,?)
        '''
        cursor.execute(addToLog,(userID,itemID,currentDateTime,currentDateTime,functionApplied))
    else:
        addToLog = '''
        INSERT INTO "Access Logs"(userID,itemID,lastAccessed,functionApplied)
        

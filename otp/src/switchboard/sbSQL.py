# LastSeenDB

getInfoSELECT = "SELECT * FROM playerinfo WHERE playerId=%s"

setInfoREPLACE = "REPLACE INTO playerinfo (playerId,avatarName,playerName,openChatEnabledYesNo,location,sublocation) VALUES (%s,%s,%s,%s,%s,%s)"

setInfoINSERT = "INSERT INTO playerinfo (playerId,avatarName,playerName,openChatEnabledYesNo,location,sublocation) VALUES (%s,%s,%s,%s,%s,%s)"

setInfoUPDATE = "UPDATE playerinfo SET avatarName=%s,playerName=%s,openChatEnabledYesNo=%s,location=%s,sublocation=%s WHERE playerId=%s"

#sbMaildb

getMailSELECT = "SELECT * FROM recipientmail WHERE recipientId=%s"

putMailINSERT = "INSERT INTO recipientmail (recipientId,senderId,message) VALUES (%s,%s,%s)"

deleteMailDELETE = "DELETE FROM recipientmail WHERE messageId=%s AND recipientId=%s"

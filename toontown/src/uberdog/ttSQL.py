from toontown.parties import PartyGlobals
#sbMaildb

getMailSELECT = "SELECT * FROM ttrecipientmail WHERE recipientId=%s"

putMailINSERT = "INSERT INTO ttrecipientmail (recipientId,senderId,message,dateSent) VALUES (%s,%s,%s,NULL)"

deleteMailDELETE = "DELETE FROM ttrecipientmail WHERE messageId=%s AND recipientId=%s"

getPartySELECT = "SELECT * FROM ttParty WHERE partyId=%s"

getMultiplePartiesSELECT = "SELECT * FROM ttParty WHERE partyId IN %s"

getMultiplePartiesSortedSELECT = "SELECT * FROM ttParty WHERE partyId IN %s ORDER BY startTime"

getPartyOfHostSELECT = "SELECT * FROM ttParty WHERE hostId=%s"

getPartyOfHostSortedSELECT = "SELECT * FROM ttParty WHERE hostId=%s ORDER BY startTime"

getPartyOfHostMatchingStatusSELECT = "SELECT * FROM ttParty WHERE hostId=%s and statusId=%s"

putPartyINSERT = "INSERT INTO ttParty (hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, statusId, creationTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, now())"

partyPrivateUPDATE = "UPDATE ttParty SET isPrivate=%s where partyId=%s"

partyStatusUPDATE = "UPDATE ttParty SET statusId=%s where partyId=%s"

partyMultipleStatusUPDATE = "UPDATE ttParty SET statusId=%s where partyId IN %s"

partyForceFinishForStartedUPDATE = "UPDATE ttParty SET statusId=" + str(PartyGlobals.PartyStatus.Finished) + " where statusId=" + str(PartyGlobals.PartyStatus.Started)+ " and endTime< %s"

partyGetPartiesGoingToFinishedSELECT = "SELECT partyId, hostId FROM ttParty where statusId=" + str(PartyGlobals.PartyStatus.Started)+ " and endTime< %s"

partyForceNeverStartedForCanStartUPDATE = "UPDATE ttParty SET statusId=" + str(PartyGlobals.PartyStatus.NeverStarted) + " where statusId=" + str(PartyGlobals.PartyStatus.CanStart)+ " and endTime< %s"

partyGetPartiesGoingToNeverStartedSELECT = "SELECT partyId, hostId FROM ttParty where statusId=" + str(PartyGlobals.PartyStatus.CanStart)+ " and endTime< %s"

deletePartyDELETE = "DELETE FROM ttParty WHERE hostId=%s"

getInvitesSELECT = "SELECT * FROM ttInvite WHERE guestId=%s"

putInviteINSERT =  "INSERT INTO ttInvite (partyId, guestId) VALUES (%s,%s)"

deleteInviteByPartyDELETE = "DELETE FROM ttInvite WHERE partyId=%s"

getRepliesSELECT = "SELECT * FROM ttInvite where partyId=%s"

getOneInviteSELECT = "SELECT * FROM ttInvite WHERE inviteId=%s"

inviteUPDATE = "UPDATE ttInvite SET statusId=%s WHERE inviteId=%s"

getInviteesOfPartySELECT = "SELECT guestId FROM ttInvite where partyId=%s"

getPartiesAvailableToStart = "SELECT partyId,hostId FROM ttParty WHERE startTime <= %s AND statusId = %s"

getLastHostParty = "SELECT MAX(partyId) FROM ttParty where hostId = %s" 

getMultiplePartiesSortedFutureNotCancelledSELECT = "SELECT * FROM ttParty WHERE partyId IN %s ORDER BY startTime"

getNonCancelledFuturePartiesSELECT = "SELECT * FROM ttParty WHERE (partyId IN %s) and (startTime >= '%s') and statusId!=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime LIMIT %s"

getCancelledFuturePartiesSELECT = "SELECT * FROM ttParty WHERE (partyId IN %s) and (startTime >= '%s') and statusId=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime LIMIT %s"

getNonCancelledPastPartiesSELECT = "SELECT * FROM ttParty WHERE (partyId IN %s) and (startTime < '%s') and statusId!=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime DESC LIMIT %s"

getCancelledPastPartiesSELECT = "SELECT * FROM ttParty WHERE (partyId IN %s) and (startTime < '%s') and statusId=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime DESC LIMIT %s"

getHostNonCancelledFuturePartiesSELECT = "SELECT * FROM ttParty WHERE (hostId = %s) and (startTime >= '%s') and statusId!=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime LIMIT %s"

getHostCancelledFuturePartiesSELECT = "SELECT * FROM ttParty WHERE (hostId = %s) and (startTime >= '%s') and statusId=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime LIMIT %s"

getHostNonCancelledPastPartiesSELECT = "SELECT * FROM ttParty WHERE (hostId = %s) and (startTime < '%s') and statusId!=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime DESC LIMIT %s"

getHostCancelledPastPartiesSELECT = "SELECT * FROM ttParty WHERE (hostId = %s) and (startTime < '%s') and statusId=" + str(PartyGlobals.PartyStatus.Cancelled) + " ORDER BY startTime DESC LIMIT %s"

"""
The OTP Avatar Manager UD handles all the avatar accross all
districts.

############################################################
# Notes
############################################################
# + How do we order avatars (slot concept)? (by avatar_id)
#   A: I will add a creation timestamp and sort by that.
#      we will update toontown later
# - What happens when I downgrade and cannot hold as many avatars?
# + Need to pass MAX_NUM_AVS through to avatar manager
# - Security of who is allowed to play an avatar (avatarDetails)?
# - how many simultaneous handled by Roger/DISL?
# + AvatarManagerUD needs to keep dict of who is playing what avatar (handle races)
# - Delete avatars from game DB STATESERVER_OBJECT_DELETE_DISK
# + get master family account id onto uberdog avatar manager
#   A: I can add to the account online event
# - allow master family account to delete any avatars
# - Delete (move to another table?) 
#    - Cleanup friends
#    - Cleanup inventory, ships, etc (check in game)
# - Undelete / restore
# - Move avatar
# + Creation date
# - Deletion date
# + shared data communicated to client
# + client GUI to lock and unlock
# + dc message to lock and unlock
# + create table if it is not there
# + Create a lock for the slot when an avatar is under construction (uber dict)
# + test same account logging in twice (boot sequence may seem odd)
# + avatar in use dict
# - handle avatar not found in game Db (and timeout condition)
# - handle uberdog crashing: need to rediscover login state
# - dont allow accounts without access to play
# 
############################################################

"""

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from otp.ai import AIMsgTypes
from otp.distributed import OtpDoGlobals
from otp.uberdog.UberDogUtil import ManagedAsyncRequest
from otp.uberdog.RejectCode import RejectCode
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from otp.uberdog import MySQLAccountAvatarsDB

from direct.directnotify.DirectNotifyGlobal import directNotify
notify = directNotify.newCategory('AvatarManagerUD')

class AsyncRequestRemove(ManagedAsyncRequest):
    notify = notify

    def __init__(self, distObj, replyToChannelId, subId, accountId, avatarId,
                 confirmPassword):
        self.rejectString = "rejectRemoveAvatar"
        ManagedAsyncRequest.__init__(self, distObj, distObj.air, replyToChannelId, key=avatarId)
        self.subId = subId
        self.accountId = accountId
        self.avatarId = avatarId
        self.confirmPassword = confirmPassword
        self.neededObjects[avatarId] = None
        self.askForObject(avatarId)

    def finish(self):
        # Let the snapshot system know this guy is gone
        self.air.sendUpdateToGlobalDoId("SnapshotDispatcherUD",
                                        "avatarDeleted",
                                        OtpDoGlobals.OTP_DO_ID_SNAPSHOT_DISPATCHER,
                                        [self.avatarId])

        # Also let the guild system know this guy is gone
        if __dev__ and uber.air.isGuildManager:
            uber.air.guildManager.avatarDeleted(self.avatarId)        
        self.air.sendUpdateToGlobalDoId("GuildManagerUD",
                                        "avatarDeleted",
                                        OtpDoGlobals.OTP_DO_ID_PIRATES_GUILD_MANAGER,
                                        [self.avatarId])        
        self.removeAvatar()
        # Resend the avatar list for security since it changed now
        self.distObj.sendAvIdList(self.accountId)
        ManagedAsyncRequest.finish(self)

    def removeAvatar(self):
        try:
            # Remove the avatar from the subId->avatar DB
            self.distObj.db.removeAvatarFromSubscription(self.avatarId, self.subId)
            uber.air.writeServerEvent('removeAvatar', self.avatarId, '%s|%s' % (self.accountId, self.subId))

            # NOTE: We do not remove the avatar from the game DB. The
            # avatar is left in so that customer service can restore
            # avatars. There will be a script that scrubs over the mysql db
            # looking for avatars deleted more than X days ago and then
            # really delete them from the game DB.
            # self.air.requestDeleteDoIdFromDisk(avatar.getDoId())
            
            # Tell the client the remove is done
            self.distObj.sendUpdateToAccountId(self.accountId, "removeAvatarResponse", [self.avatarId, self.subId])
        except ValueError:
            self.sendRejectCode(RejectCode.NO_AVATAR)

#-----------------------------------------------------------------------------

class OtpAvatarManagerUD(DistributedObjectGlobalUD):
    """
    The Avatar Manager UD is a global object.

    See Also:
        "otp/src/guild/AvatarManager.py"
        "otp/src/guild/AvatarManagerAI.py"
        "otp/src/configfiles/otp.dc"
    """
    if __debug__:
        notify = notify

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.DBuser = uber.config.GetString("mysql-user", "ud_rw")
        self.DBpasswd = uber.config.GetString("mysql-passwd", "r3adwr1te")

        self.DBhost = uber.config.GetString("accountavatars-db-host", "localhost")
        self.DBport = uber.config.GetInt("accountavatars-db-port", 3306)
        self.DBname = uber.config.GetString("accountavatars-db-name", "avatars")

        self.db = MySQLAccountAvatarsDB.MySQLAccountAvatarsDB(host = self.DBhost,
                                                              port = self.DBport,
                                                              user = self.DBuser,
                                                              passwd = self.DBpasswd,
                                                              dbname = self.DBname)


        # Must define our async requests in subclasses on a per-game basis
        self.AsyncRequestAvatarList=None
        self.AsyncRequestCreateAvatar=None
        self.AsyncRequestRemove=AsyncRequestRemove
        
        self.asyncRequests={}

        # Dictionary to track accountIds that are currently in the process
        # of creating avatars. This is a locking system so you do not get
        # multiple family members logged in at the same time exceeding the
        # max number of avatars they are allowed.
        # Dict of {accountId : subId}
        self.__pendingCreatesForAccount = {}
        # Dict of {subId : numPending}
        self.__pendingCreatesForSubscription = {}

    def getPendingCreatesForAccount(self, accountId):
        return self.__pendingCreatesForAccount.get(accountId, 0)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.accept("accountOnline", self.accountOnline)
        self.accept("accountOffline", self.accountOffline)
        self.accept("avatarOnlinePlusAccountInfo", self.avatarOnline)
        self.accept("avatarOffline", self.avatarOffline)
        self.sendUpdateToChannel(AIMsgTypes.CHANNEL_CLIENT_BROADCAST, "online", [])
        self.sendUpdateToChannel(AIMsgTypes.OTP_CHANNEL_AI_AND_UD_BROADCAST, "online", [])
    
    def delete(self):
        self.ignoreAll()
        for i in self.asyncRequests.values():
            i.delete()
        self.asyncRequests={}
        DistributedObjectGlobalUD.delete(self)

    #----------------------------------

    @report(types = ['args'], dConfigParam = 'orphanedavatar')
    def removePriorAccountsAvatar(self, accountId):
        """
        This is called from a local instance of the OtpAvatarManagerUD object
        when it detects that a player is trying to recover an avatar
        orphaned by a client agent crash.  If you want to hook into
        this process, override 'removePriorAvatar()' in your game-specific
        subclass.
        """
        priorAvatar = self.air.getAccountOnlineAvatar(accountId)
        if priorAvatar:
            if config.GetBool('want-orphanedavatar-report', 0):
                assert self.notify.warning('found orphaned avatar: (%s,%s)' % (accountId, avatarId))
            self.removePriorAvatar(accountId, priorAvatar)
            pass
        pass
    
    @report(types = ['args'], dConfigParam = 'orphanedavatar')
    def removePriorAvatar(self, accountId, avatarId):
        """
        Override this if you want to hook into the orphaned
        avatar recovery process.
        """
        self.air.requestDeleteDoId(avatarId)
        self.air.avatarOffline(accountId, avatarId)

        self.air.sendUpdateToGlobalDoId('AvatarFriendsManagerUD',
                                        'avatarOffline',
                                        OtpDoGlobals.OTP_DO_ID_AVATAR_FRIENDS_MANAGER,
                                        [avatarId])
        pass

    @report(types = ['args'], dConfigParam = 'avatarmgr')
    def accountOnline(self, accountId):
        pass

    @report(types = ['args'], dConfigParam = 'avatarmgr')
    def accountOffline(self, accountId):
        i = self.asyncRequests.pop(accountId, None)
        if i is not None:
            i.delete()
        self.clearPendingAvatarCreates(accountId)
        return


    @report(types = ['args'], dConfigParam = 'avatarmgr')
    def avatarOnline(self,avatarId,accountId,playerName,playerNameApproved,
                     openChatEnabled,createFriendsWithChat,chatCodeCreation):
        self.db.lastPlayed(avatarId, accountId)
        pass
    
    @report(types = ['args'], dConfigParam = 'avatarmgr')
    def avatarOffline(self, avatarId):
        pass
    
    def clearPendingAvatarCreates(self, accountId):
        subId = self.__pendingCreatesForAccount.pop(accountId, None)
        if subId:
            numPending = self.__pendingCreatesForSubscription.get(subId, 0)
            if numPending == 1:
                # Remove the entry, this was the only pending create
                self.__pendingCreatesForSubscription.pop(subId, None)
                return 1
            elif numPending > 1:
                self.__pendingCreatesForSubscription[subId] -= 1
                return 1
            elif numPending == 0:
                # None found... a little odd, but we can let this pass
                return 1
            else:
                self.notify.warning("clearPendingAvatarCreates: accountId: %s, subId: %s, numPending: %s" % (accountId, subId, numPending))
                return 0
        else:
            # accountId had none pending... a little odd, but I guess it is ok
            return 1

    def getNumAvatarsPendingCreate(self, subId):
        # How many are pending creation on this subscription?
        numPending = self.__pendingCreatesForSubscription.get(subId, 0)
        return numPending

    def getNumAvatarsCreatedOrPending(self, subId):
        """
        Return the total number of avatars created on disk plus the
        number of avatars that this account or any family members logged in
        are currently in the process of creating.
        # NOTE: this does a DB query, so only call sparingly
        """        
        # How many avatars has the family already created on disk?
        numCreated = len(self.db.getAvatarIdsForSubscription(subId))
        numPending = self.getNumAvatarsPendingCreate(subId)
        # Add up the two and return the result
        return (numCreated + numPending)

    #----------------------------------
    
    @report(types = ['args'], dConfigParam = 'avatarmgr')
    def requestAvatarList(self, senderId):
        accountId = senderId
        replyToChannel = self.air.getSenderReturnChannel()

        if not self.air.checkAccountId(accountId):
            reasonCode = RejectCode.INVALID_ACCOUNT
            self.sendUpdateToAccountId(accountId, "rejectAvatarList", [RejectCode.INVALID_ACCOUNT])
            return reasonCode

        # if an avatar associated with this account was orphaned
        # by a suicidal client agent, remove-from-ram the avatar now
        self.removePriorAccountsAvatar(accountId)

        # Get the avatar records for all family member's subscriptions
        accountDetails = self.air.getAccountDetails(accountId)

        # Request the avatars from the database for all subscriptions that
        # this account has access to. That info comes from the DISL play
        # token through the login message.
        avatarIds = []
        avatarRecords = {}
        for subId in accountDetails.subDetails.keys():
            avatarData = self.db.getAvatarIdsForSubscription(subId)
            avatarRecords[subId] = avatarData
            avatarIds.extend([record[0] for record in avatarData])

        # Note: we dont call sendAvIdList because that would hit MySQL
        # again. We'll just call the update ourselves to prevent the wasted
        # db queries.
        # The game server sniffs this message to enfore security.
        self.sendUpdateToAccountId(accountId, "sendAvIdList", [avatarIds])

        assert self.notify.debug("accountId: %s avatarRecords: %s" % (accountId, avatarRecords))
        self.AsyncRequestAvatarList(self, replyToChannel, accountId, avatarRecords)
        return 1

    def sendAvIdList(self, accountId):
        # Tell the game server the list of avatars this account is allowed to play
        avatarIds = []
        # Get the avatar records for all family member's subscriptions
        accountDetails = self.air.getAccountDetails(accountId)

        if accountDetails is None:
            self.notify.warning('tried to send avId list for account %s that has since logged out' % (accountId))
            return

        for subId in accountDetails.subDetails.keys():
            avatarData = self.db.getAvatarIdsForSubscription(subId)
            avatarIds.extend([record[0] for record in avatarData])
        # The game server sniffs this message to enfore security
        self.sendUpdateToAccountId(accountId, "sendAvIdList", [avatarIds])
        
    def requestRemoveAvatar(self, senderId, avatarId, subId, confirmPassword):
        replyToChannel = self.air.getSenderReturnChannel()
        accountId = senderId

        if not self.air.checkAccountId(accountId):
            reasonCode = RejectCode.INVALID_ACCOUNT
            self.sendUpdateToAccountId(accountId, "rejectRemoveAvatar", [reasonCode])
            return reasonCode

        avatarRecords = self.db.getAvatarIdsForSubscription(subId)
        avatarIds = [record[0] for record in avatarRecords]
        creatorIds = [record[1] for record in avatarRecords]

        if avatarId not in avatarIds:
            self.notify.warning("accountId: %s tried to delete avatarId: %s not on subId: %s" %
                                (accountId, avatarId, subId))
            reasonCode = RejectCode.NOT_YOUR_AVATAR
            self.sendUpdateToAccountId(accountId, "rejectRemoveAvatar", [reasonCode])
            return reasonCode

        if self.air.isAvatarOnline(avatarId):
            self.notify.warning("accountId: %s tried to delete avatarId: %s currently in use" %
                                (accountId, avatarId))
            reasonCode = RejectCode.AVATAR_ONLINE
            self.sendUpdateToAccountId(accountId, "rejectRemoveAvatar", [reasonCode])
            return reasonCode

        # Rule: When using linked accounts, you can only delete avatars you created
        creatorId = creatorIds[avatarIds.index(avatarId)]
        if simbase.config.GetBool('allow-linked-accounts', 0) and \
           accountId != creatorId:
            self.notify.warning("accountId: %s tried to delete avatarId: %s from another creatorId: %s" %
                                (accountId, avatarId, creatorId))
            reasonCode = RejectCode.NOT_YOUR_AVATAR
            self.sendUpdateToAccountId(accountId, "rejectRemoveAvatar", [reasonCode])
            return reasonCode

        # TODO: allow master family account to delete any avatars
        
        # TODO: check confirm password

        self.air.writeServerEvent('requestRemoveAvatar', avatarId, '%s|%s' % (accountId, subId))

        self.AsyncRequestRemove(self, replyToChannel, subId, accountId, avatarId, confirmPassword)
        return 1

    def requestAvatarName(self, avatarName):
        avatarId = self.air.getAvatarIdFromSender()
        self.air.sendUpdateToDoId('DistributedAvatar', 'setName', avatarId, [avatarName])
        
    def requestShareAvatar(self, senderId, avatarId, subId, shared):
        replyToChannel = self.air.getSenderReturnChannel()
        accountId = senderId
        
        if not self.air.checkAccountId(accountId):
            reasonCode = RejectCode.INVALID_ACCOUNT
            self.sendUpdateToAccountId(accountId, "rejectShareAvatar", [reasonCode])
            return reasonCode
        
        # You can only toggle the shared flag on avatars you created
        # TODO: allow master family account to toggle any avatars
        avatarRecords = self.db.getAvatarIdsForSubscription(subId)
        avatarIds = [record[0] for record in avatarRecords]
        creatorIds = [record[1] for record in avatarRecords]

        if avatarId not in avatarIds:
            self.notify.warning("accountId: %s tried to share avatarId: %s he did not create" %
                                (accountId, avatarId))
            reasonCode = RejectCode.NOT_YOUR_AVATAR
            self.sendUpdateToAccountId(accountId, "rejectShareAvatar", [reasonCode])
            return reasonCode
        
        # Rule: You can only share avatars you created
        creatorId = creatorIds[avatarIds.index(avatarId)]
        if accountId != creatorId:
            self.notify.warning("accountId: %s tried to share avatarId: %s from another creatorId: %s" %
                                (accountId, avatarId, creatorId))
            reasonCode = RejectCode.NOT_YOUR_AVATAR
            self.sendUpdateToAccountId(accountId, "rejectShareAvatar", [reasonCode])
            return reasonCode
        
        self.air.writeServerEvent('requestShareAvatar', avatarId,
                                  '%s|%s|%s' % (accountId, subId, shared))

        self.db.setSharedFlag(avatarId, subId, shared)
        self.sendUpdateToAccountId(accountId, "shareAvatarResponse", [avatarId, subId, shared])
        return 1

    def requestAvatarSlot(self, senderId, subId, slot):
        replyToChannel = self.air.getSenderReturnChannel()
        accountId = senderId
            
        if not self.air.checkAccountId(accountId):
            reasonCode = RejectCode.INVALID_ACCOUNT
            self.sendUpdateToAccountId(accountId, "rejectAvatarSlot", [reasonCode, subId, slot])
            return reasonCode

        # Put a lock to fill the spot in case a simultaneous login wants to
        # create an avatar at the same time.
        oldSubId = self.__pendingCreatesForAccount.get(accountId)
        if oldSubId:
            # Hmm... this account already has a slot. Strange.
            self.notify.warning("accountId: %s already had a slot reserved for subId: %s" %
                                (accountId, oldSubId))
            # Let's clear it and move forward
            del self.__pendingCreatesForAccount[accountId]
            oldNumPending = self.__pendingCreatesForSubscription.get(oldSubId, 0)
            if oldNumPending > 0:
                self.__pendingCreatesForSubscription[oldSubId] -= 1
        
        # Make sure the family has not exceeded max num avatars
        totalNumAvatars = self.getNumAvatarsCreatedOrPending(subId)
        maxNumAvatars = self.getMaxNumAvatars(accountId, subId)
        if totalNumAvatars >= maxNumAvatars:
            reasonCode = RejectCode.MAX_AVATAR_LIMIT
            self.sendUpdateToAccountId(accountId, "rejectAvatarSlot", [reasonCode, subId, slot])
            return reasonCode

        # Put a lock to fill the spot in case a simultaneous login wants to
        # create an avatar at the same time.
        self.__pendingCreatesForAccount[accountId] = subId
        curVal = self.__pendingCreatesForSubscription.get(subId, 0)
        self.__pendingCreatesForSubscription[subId] = curVal + 1
        self.sendUpdateToAccountId(accountId, "avatarSlotResponse", [subId, slot])


    @report(types = ['args'], dConfigParam = 'avatarmgr')
    def requestPlayAvatar(self, senderId, avatarId, subId):
        replyToChannel = self.air.getSenderReturnChannel()
        accountId = senderId

        if not self.air.checkAccountId(accountId):
            reasonCode = RejectCode.INVALID_ACCOUNT
            self.sendUpdateToAccountId(accountId, "rejectPlayAvatar", [RejectCode.INVALID_ACCOUNT, avatarId])
            return reasonCode

        playingAccountId = self.air.getAvatarAccountOnline(avatarId)
        if playingAccountId:
            if playingAccountId == accountId:
                # We already think this requesting avatarId is online playing this avatar.
                self.notify.warning("avatar is already online: %s played by same accountId: %s" %
                                    (avatarId, playingAccountId))
                reasonCode = RejectCode.AVATAR_ONLINE
                self.sendUpdateToAccountId(accountId, "rejectPlayAvatar", [reasonCode, avatarId])
                return reasonCode
            else:
                self.notify.warning("avatar is already online: %s played by another accountId: %s" %
                                    (avatarId, playingAccountId))
                reasonCode = RejectCode.AVATAR_ONLINE
                self.sendUpdateToAccountId(accountId, "rejectPlayAvatar", [reasonCode, avatarId])
                return reasonCode

        accountDetails = self.air.getAccountDetails(accountId)
        subDetails = accountDetails.subDetails.get(subId)
        if not subDetails:
            self.notify.warning("avatar %s is not on this subscription: %s" %
                                (avatarId, subId))
            reasonCode = RejectCode.NOT_YOUR_AVATAR
            self.sendUpdateToAccountId(accountId, "rejectPlayAvatar", [reasonCode, avatarId])
            return reasonCode

        
        # Ok, you can play this avatar.
        # First let's remove-from-ram if the avatar is somehow still out there
        self.air.requestDeleteDoId(avatarId)
        
        # Let's go ahead and mark this avatar as online since we are expecting him soon.
        self.sendUpdateToAccountId(accountId, "playAvatarResponse",
                                  [avatarId, subDetails.subId, subDetails.subAccess, subDetails.subFounder])
        return

    def getMaxNumAvatars(self, accountId, subId):
        accountDetails = self.air.getAccountDetails(accountId)
        if accountDetails:
            return accountDetails.getMaxNumAvatars(subId)
        else:
            self.notify.warning("getMaxNumAvatars: account is not online")
            return 0

    def getMaxNumAvatarSlots(self, accountId, subId):
        accountDetails = self.air.getAccountDetails(accountId)
        if accountDetails:
            return accountDetails.maxAvatarSlots
        else:
            self.notify.warning("getMaxNumAvatarSlots: account is not online")
            return 0


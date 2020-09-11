from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.AsyncRequest import AsyncRequest
from toontown.uberdog import PartiesUdConfig
from toontown.uberdog.PartiesUdLog import partiesUdLog
from toontown.uberdog.ttMaildb import ttMaildb
from toontown.toonbase import ToontownGlobals
from toontown.uberdog.ttPartyDb import ttPartyDb
from toontown.uberdog.ttInviteDb import ttInviteDb

class DistributedMailManagerUD(DistributedObjectGlobalUD):
    """UD side class for the mail manager."""
    
    notify = DirectNotifyGlobal.directNotify.newCategory("DistrubtedMailManagerUD")
    
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        user = uber.config.GetString("mysql-user", '')
        passwd = uber.config.GetString("mysql-passwd",'')
        if not user:
            user = PartiesUdConfig.ttDbUser
        if not passwd:
            passwd = PartiesUdConfig.ttDbPasswd        
        self.mailDB = ttMaildb(host=PartiesUdConfig.ttDbHost,
                               port=PartiesUdConfig.ttDbPort,
                               user = user,
                               passwd = passwd,                               
                               db=PartiesUdConfig.ttDbName)
        
    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.accept("avatarOnlinePlusAccountInfo", self.avatarOnlinePlusAccountInfo, [])        
        
    def sendSimpleMail(self, senderId, recipientId, simpleText):
        """Testing to send a simple text message to another."""
        DistributedMailManagerUD.notify.debug("sendSimpleMail( senderId=%d, recipientId=%d, simpleText='%s')" %(senderId, recipientId, simpleText))
        self.mailDB.putMail(recipientId, senderId, simpleText)

    def avatarLoggedIn(self, avatarId):
        """Handle an avatar just logging in."""
        DistributedMailManagerUD.notify.debug("avatarLoggedIn( avatarId=%d )" %avatarId)
        # for now we get all the mail, then send it across the wire to the client.
        
        result = self.mailDB.getMail(avatarId)

        DistributedMailManagerUD.notify.debug('mailDB.getMail returned %d items for avatarID %d' % (len(result), avatarId))
        self.numMailItems = len(result)
        mailStr = str(result)

        replyToChannelAI = self.air.getSenderReturnChannel()

        #sefl.sendUpdateToChannel( replyToChannelAI, 'avatarLoggedInMailResponse',
        #                          mailStr)
        #if result:
        #    myGAR = GetAvatarForMailRequest(self, replyToChannelAI,
        #                                    avatarId, result, numMailItems)
        self.mail = result
        self.avatarId = avatarId
        formattedMail = []
        numOld = 0
        numNew = 0
        for item in self.mail:
            senderId = item['senderId']
            datetime = item['lastupdate']
            year = datetime.year
            month = datetime.month
            day = datetime.day
            msgId = item['messageId']
            body = item['message']
            readFlag = item['readFlag']
            formattedMail.append( (msgId, senderId, year, month, day, body) )
            if readFlag:
                numOld += 1
            else:
                numNew += 1
        
        DistributedMailManagerUD.notify.debug("Calling DistributedToon::setMail across the network with avatarId %d" %self.avatarId )
        self.air.sendUpdateToDoId(
            "DistributedToon",
            "setMail",
            self.avatarId,
            [formattedMail],
        )
        # for now,  inform the AI that a toon has X number of mail
        #self.distObj.sendUpdateToChannel(self.replyToChannelId, "setNumMailItems", 
        #                         [self.avatarId, self.numMailItems])
        #        #return an Accept message to the AI caller

        DistributedMailManagerUD.notify.debug("Calling DistributedToon::setNumMailItems( %d ) across the network with avatarId %d" %(self.numMailItems, self.avatarId) )
        self.air.sendUpdateToDoId(
            "DistributedToon",
            "setNumMailItems",
            self.avatarId,
            [self.numMailItems],
        )

        simpleMailNotify = ToontownGlobals.NoItems
        if numNew:
            simpleMailNotify = ToontownGlobals.NewItems
        elif numOld:
            simpleMailNotify = ToontownGlobals.OldItems
        
        DistributedMailManagerUD.notify.debug("Calling DistributedToon::setSimpleMailNotify( %d ) across the network with avatarId %d" %(simpleMailNotify, self.avatarId) )
        self.air.sendUpdateToDoId(
            "DistributedToon",
            "setSimpleMailNotify",
            self.avatarId,
            [simpleMailNotify],
        )

    def avatarOnlinePlusAccountInfo(self,avatarId,accountId,playerName,
                                    playerNameApproved,openChatEnabled,
                                    createFriendsWithChat,chatCodeCreation):
        # otp server is telling us an avatar just logged in
        # this is far far better than having the AI be the one to tell us
        assert self.notify.debugCall()
        assert avatarId

        self.notify.debug("avatarOnlinePlusAccountInfo")
        self.avatarLoggedIn(avatarId)

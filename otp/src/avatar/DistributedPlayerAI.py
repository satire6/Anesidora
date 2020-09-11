
from direct.showbase import GarbageReport
from otp.ai.AIBaseGlobal import *
from otp.avatar import DistributedAvatarAI
from otp.avatar import PlayerBase
from otp.otpbase import OTPGlobals

class DistributedPlayerAI(DistributedAvatarAI.DistributedAvatarAI,
                          PlayerBase.PlayerBase):
    def __init__(self, air):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        PlayerBase.PlayerBase.__init__(self)
        self.friendsList = []

    if __dev__:
        def generate(self):
            self._sentExitServerEvent = False
            DistributedAvatarAI.DistributedAvatarAI.generate(self)

    def announceGenerate(self):
        DistributedAvatarAI.DistributedAvatarAI.announceGenerate(self)
        self._doPlayerEnter()

    def _announceArrival(self):
        self.sendUpdate('arrivedOnDistrict', [self.air.districtId])

    def _announceExit(self):
        # clear out the 'arrivedOnDistrict' field
        self.sendUpdate('arrivedOnDistrict', [0])

    def _sendExitServerEvent(self):
        """call this in your delete() function. This would be an
        override of delete(), but player classes typically use
        multiple inheritance, and some other base class gets to
        call down the chain to DistributedObjectAI before this
        class gets a chance, and self.air & self.doId are removed
        in the first call to DistributedObjectAI.delete(). Better
        would be reference counting calls to generate() and delete()
        in base classes that appear more than once in a class'
        inheritance heirarchy"""
        self.air.writeServerEvent('avatarExit', self.doId, '')
        if __dev__:
            self._sentExitServerEvent = True

    def delete(self):
        if __dev__:
            # make sure _sendExitServerEvent() was called
            assert self._sentExitServerEvent
            del self._sentExitServerEvent
        self._doPlayerExit()
        if __dev__:
            GarbageReport.checkForGarbageLeaks()
        DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def isPlayerControlled(self):
        return True
    
    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedAvatarAI.DistributedAvatarAI.setLocation(self, parentId, zoneId, teleport)
        if self.isPlayerControlled():
            # hmm, did this come from a hacker trying to get somewhere they shouldn't be?
            if not self.air._isValidPlayerLocation(parentId, zoneId):
                self.notify.info('booting player %s for doing setLocation to (%s, %s)' % (
                    self.doId, parentId, zoneId))
                self.air.writeServerEvent('suspicious', self.doId,
                                          'invalid setLocation: (%s, %s)' % (parentId, zoneId))
                self.requestDelete()
            
    def _doPlayerEnter(self):
        self.incrementPopulation()
        self._announceArrival()

    def _doPlayerExit(self):
        self._announceExit()
        self.decrementPopulation()

    # override if you don't want to affect the population count for a
    # particular PlayerAI
    def incrementPopulation(self):
        self.air.incrementPopulation()
    def decrementPopulation(self):
        # use simbase in case we've already deleted self.air
        simbase.air.decrementPopulation()

    def b_setChat(self, chatString, chatFlags):
        # Local
        self.setChat(chatString, chatFlags)
        # Distributed
        self.d_setChat(chatString, chatFlags)

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate("setChat", [chatString, chatFlags])

    def setChat(self, chatString, chatFlags):
        # I guess on the AI side there is nothing to do here
        pass

    def d_setMaxHp(self, maxHp):
        DistributedAvatarAI.DistributedAvatarAI.d_setMaxHp(self, maxHp)
        self.air.writeServerEvent('setMaxHp', self.doId, '%s' % maxHp)

    def d_setSystemMessage(self, aboutId, chatString):
        self.sendUpdate("setSystemMessage", [aboutId, chatString])

    def d_setCommonChatFlags(self, flags):
        self.sendUpdate("setCommonChatFlags", [flags])

    def setCommonChatFlags(self, flags):
        pass

    def d_friendsNotify(self, avId, status):
        self.sendUpdate("friendsNotify", [avId, status])

    def friendsNotify(self, avId, status):
        pass

    def setAccountName(self, accountName):
        self.accountName = accountName

    def getAccountName(self):
        return self.accountName

    def setDISLid(self, id):
        self.DISLid = id        

    def d_setFriendsList(self, friendsList):
        self.sendUpdate("setFriendsList", [friendsList])

    def setFriendsList(self, friendsList):
        self.friendsList = friendsList
        self.notify.debug("setting friends list to %s" % self.friendsList)

    def getFriendsList(self):
        return self.friendsList

    def extendFriendsList(self, friendId, friendCode):
        # This is called only by the friend manager when a new friend
        # transaction is successfully completed.  Its purpose is
        # simply to update the AI's own copy of the avatar's friends
        # list, mainly so that the quest manager can reliably know
        # if the avatar has any friends.

        # First, see if we already had this friend.
        for i in range(len(self.friendsList)):
            friendPair = self.friendsList[i]
            if friendPair[0] == friendId:
                # We did.  Update the code.
                self.friendsList[i] = (friendId, friendCode)
                return

        # We didn't already have this friend; tack it on.
        self.friendsList.append((friendId, friendCode))

        # Note that if an avatar *breaks* a friendship, the AI never
        # hears about it.  So our friends list will not be 100%
        # up-to-date, but it will at least be good enough for the
        # quest manager.


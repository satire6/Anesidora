"""DistributedCCharBase module: contains the DistributedCCharBase class"""

from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from otp.avatar import DistributedAvatarAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class DistributedCCharBaseAI(DistributedAvatarAI.DistributedAvatarAI):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // DistributedCCharBase:  base class for all classic characters
    //                       such as Mickey and Minnie, who hang out
    //                       in the safezones
    //
    ////////////////////////////////////////////////////////////////////
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCCharBaseAI")

    def __init__(self, air, name):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        self.setName(name)
        self.exitOff()

        # We do not want to move into the transitionCostume state unless signalled to do so.
        self.transitionToCostume = 0
        self.diffPath = None

    def delete(self):
        self.ignoreAll()
        DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def exitOff(self):
        self.__initAttentionSpan()
        self.__clearNearbyAvatars()

    ## network messages
    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        # this avatar has come within blathering range
        self.notify.debug("adding avatar " + str(avId) +
                          " to the nearby avatar list")

        # check if he's already on the list
        if avId not in self.nearbyAvatars:
            # add new avatar to nearby list
            self.nearbyAvatars.append(avId)
        else:
            # This should not happen
            self.air.writeServerEvent('suspicious', avId, 'CCharBase.avatarEnter')
            self.notify.warning("Avatar %s already in nearby avatars!"
                                % (avId))


        # create an info dict for the avatar
        self.nearbyAvatarInfoDict[avId] = {}
        self.nearbyAvatarInfoDict[avId]['enterTime'] = globalClock.getRealTime()
        self.nearbyAvatarInfoDict[avId]['lastChatTime'] = 0

        # re-sort the list
        self.sortNearbyAvatars()

        self.__interestingAvatarEventOccured()

        # Hang a hook to handle this avatar exiting
        avExitEvent = self.air.getAvatarExitEvent(avId)
        self.acceptOnce(avExitEvent, self.__handleExitedAvatar, [avId])

        self.avatarEnterNextState()

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        self.__doAvatarExit(avId)

    def __doAvatarExit(self, avId):
        avId = self.air.getAvatarIdFromSender()
        # this avatar has made his escape
        self.notify.debug("removing avatar " + str(avId) +
                          " from the nearby avatar list")
        # is the avatar on the list...?
        if not avId in self.nearbyAvatars:
            # this is OK, mickeys always send an exit
            # for their local toon on destruction
            self.notify.debug("avatar " + str(avId) +
                              " not in the nearby avatar list")
        else:
            # get rid of the exit handler
            avExitEvent = self.air.getAvatarExitEvent(avId)
            self.ignore(avExitEvent)

            del self.nearbyAvatarInfoDict[avId]
            self.nearbyAvatars.remove(avId)

            self.avatarExitNextState()

    def avatarEnterNextState():
        # meant to be over-ridden by a child class that has a state machine
        pass
    def avatarExitNextState():
        # meant to be over-ridden by a child class that has a state machine
        pass

    def __clearNearbyAvatars(self):
        self.nearbyAvatars = []
        self.nearbyAvatarInfoDict = {}

    def sortNearbyAvatars(self):
        def nAv_compare(a, b, nAvIDict = self.nearbyAvatarInfoDict):
            # if a has been around longer than b,
            # a is 'greater' than b
            # for integers, result would be (a-b)
            # so if a < b, we return <0
            # for timestamps, if ts1 < ts2, ts1 is older
            # and therefore 'greater', so result is ts2 - ts1
            tsA = nAvIDict[a]['enterTime']
            tsB = nAvIDict[b]['enterTime']
            if tsA == tsB:
                return 0
            elif tsA < tsB:
                return -1
            else:
                return 1

        self.nearbyAvatars.sort(nAv_compare)

    def getNearbyAvatars(self):
        return self.nearbyAvatars

    def __avatarSpoke(self, avId):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character detects that an avatar near
        //             it has spoken, this allows the character to respond
        // Parameters: avId, the avatar that spoke
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        now = globalClock.getRealTime()
        if self.nearbyAvatarInfoDict.has_key(avId):
            self.nearbyAvatarInfoDict[avId]['lastChatTime'] = now
            self.__interestingAvatarEventOccured()

    # Mickey attention span simulator
    def __initAttentionSpan(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   initialize the attention span simulator properly
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.__avatarTimeoutBase = 0

    def __interestingAvatarEventOccured(self, t=None):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   this should be called when we want the character
        //             to respond to something the avatar has done such
        //             as walked up next to the character or spoken while
        //             near the character
        // Parameters: t, time at which this event occured
        // Changes:    self.__avatarTimeoutBase
        ////////////////////////////////////////////////////////////////////
        """
        if t == None:
            t = globalClock.getRealTime()
        self.__avatarTimeoutBase = t

    def lostInterest(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   check to see if this character has lost interest
        //             in whatever it is currently doing
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        now = globalClock.getRealTime()
        if now > (self.__avatarTimeoutBase + 50.):
            return 1
        return 0

    def __handleExitedAvatar(self, avId):
        # avatar went away
        self.__doAvatarExit(avId)

    def setNearbyAvatarChat(self, msg):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("setNearbyAvatarChat: avatar "
                          + str(avId) + " said " + str(msg))
        self.__avatarSpoke(avId)

    def setNearbyAvatarSC(self, msgIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug(
            "setNearbyAvatarSC: avatar %s said SpeedChat phrase %s" %
            (avId, msgIndex))
        self.__avatarSpoke(avId)

    def setNearbyAvatarSCCustom(self, msgIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug(
            "setNearbyAvatarSCCustom: avatar %s said custom "
            "SpeedChat phrase %s" % (avId, msgIndex))
        self.__avatarSpoke(avId)

    def setNearbyAvatarSCToontask(self,
                                  taskId, toNpcId, toonProgress, msgIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug(
            "setNearbyAvatarSCToontask: avatar %s said %s" %
            (avId, (taskId, toNpcId, toonProgress, msgIndex)))
        self.__avatarSpoke(avId)

    def getWalk(self):
        # This is called when the char is created on the AI to return
        # the initial walk source and destination points.  It doesn't
        # return anything meaningful, but the empty string is the code
        # to a client to hang out and wait for a subsequent message.
        return ('', '', 0)

    def walkSpeed(self):
        return 0.1
        
    def handleHolidays(self):
        self.CCChatter = 0        
        if hasattr(simbase.air, "holidayManager"):
            if ToontownGlobals.CRASHED_LEADERBOARD in simbase.air.holidayManager.currentHolidays:            
                self.CCChatter = ToontownGlobals.CRASHED_LEADERBOARD 
            elif ToontownGlobals.CIRCUIT_RACING_EVENT in simbase.air.holidayManager.currentHolidays:            
                self.CCChatter = ToontownGlobals.CIRCUIT_RACING_EVENT
            elif ToontownGlobals.WINTER_CAROLING in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.WINTER_CAROLING
            elif ToontownGlobals.WINTER_DECORATIONS in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.WINTER_DECORATIONS
            elif ToontownGlobals.VALENTINES_DAY in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.VALENTINES_DAY
            elif ToontownGlobals.APRIL_FOOLS_COSTUMES in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.APRIL_FOOLS_COSTUMES
            elif ToontownGlobals.SILLY_CHATTER_ONE in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_ONE
            elif ToontownGlobals.SILLY_CHATTER_TWO in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_TWO
            elif ToontownGlobals.SILLY_CHATTER_THREE in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_THREE
            elif ToontownGlobals.SILLY_CHATTER_FOUR in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR
            elif ToontownGlobals.SILLY_CHATTER_FIVE in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR

    def getCCLocation(self):
        # This function is used to differentiate between the same classic
        # char in different locations.  Sub class should override this
        # function to return a location number other than zero.
        return 0

    def getCCChatter(self):
        self.handleHolidays()
        return self.CCChatter
        
    #################################################################
    # This function is used to call it's counterpart on the client
    # end to fade the character away
    #################################################################
    def fadeAway(self):
        self.sendUpdate("fadeAway", [])

    ############################################################
    # In order to transition to the next costume, precedence
    # must be given to transitionCostume during
    # __decideNextState function
    ############################################################
    def transitionCostume(self):
        self.transitionToCostume = 1

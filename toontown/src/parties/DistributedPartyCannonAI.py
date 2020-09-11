#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: DistributedPartyCannonAI handles the AI instance of a cannon at a party.
#          It keeps track if a toon is inside the cannon. Note that it does not
#          keep track of flying toons; that's the job of DistributedPartyCannonActivityAI
#-------------------------------------------------------------------------------

from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.distributed import DistributedObjectAI

from toontown.toonbase import ToontownGlobals
from toontown.minigame import CannonGameGlobals
from toontown.minigame import Trajectory
from toontown.parties import PartyGlobals

class DistributedPartyCannonAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory("DistributedPartyCannonAI")
    #notify.setDebug(True)

    CANNON_LIT_EVENT = "D_PARTY_CANNON_LIT"
    
    def __init__(self, air, activityDoId, x, y, z, h, p, r):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        # TODO: Take this out when all cannons come from db
        z = 0
        self.posHpr = [x, y, z, h, p, r]
        self.toonInsideAvId = 0
        self.activityDoId = activityDoId
        self.timeoutTask = None
        self.rotation = 0.0
        self.angle = 0.0
        self.lit = False
        self.toonEnteredTime = 0

    def delete(self):
        self.ignoreAll()
        self.__stopTimeout()
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    # Distributed (clsend airecv)
    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        # No toon inside, may enter cannon
        inActivity = False
        parentActivity = simbase.air.doId2do.get(self.activityDoId)
        if parentActivity:
            inActivity = parentActivity.party.isInActivity(avId)
        if not self.isToonInside() and not inActivity:
            self.__placeToonInside(avId)
        else:
            if self.toonInsideAvId != avId:
                # don't kick out a toon already inside the cannon
                self.notify.debug("requestEnter() - cannon already occupied")
                self.sendUpdateToAvatarId(avId, "requestExit", [])
            else:
                self.notify.warning("got requestEnter from toon already inside it.")
            
#===============================================================================
# Attributes
#===============================================================================
    def isToonInside(self):
        return (self.toonInsideAvId != 0)
    
    def getToonInsideId(self):
        return self.toonInsideAvId
    
    def isReadyToFire(self):
        return self.isToonInside() and self.lit

    def __placeToonInside(self, avId):
        """
        Prepares a toon to be inside the cannon.
        """
        self.notify.debug("__placeToonInside %s" % avId)
        self.toonEnteredTime = globalClock.getFrameTime()
        self.__stopTimeout()
        self.toonInsideAvId = avId
        self.notify.debug("Sending PartyGlobals.CANNON_MOVIE_LOAD for %d" % avId)
        self.d_setMovie(PartyGlobals.CANNON_MOVIE_LOAD, self.toonInsideAvId)

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])
        self.acceptOnce("bootAvFromParty-%d" % avId,
                        self.__handleBootMessage, extraArgs=[avId])

    def __clearToonInside(self):
        self.notify.debug("%d __clearToonInside self.toonInsideAvId=%d" % (self.doId, self.toonInsideAvId))
        self.toonInsideAvId = 0
        self.lit = False
        self.__stopTimeout()
    
    # Distributed (broadcast, ram)
    def d_setMovie(self, mode, avId):
        self.notify.debug("d_setMovie mode=%s, avId=%s" % (str(mode), str(avId)))
        #if mode == PartyGlobals.CANNON_MOVIE_CLEAR:
        #    from direct.showbase.PythonUtil import StackTrace
        #    print StackTrace()
        self.sendUpdate("setMovie", [mode, avId])
        
    # Distributed (aisend clrecv)
    def setCannonPosition(self, zRot, angle):
        avId = self.air.getAvatarIdFromSender()
        # a client is sending a position update for their cannon
        #self.notify.debug("setCannonPosition: %d: zRot = %d, angle = %d" % (avId, zRot, angle))
        self.rotation = zRot
        self.angle = angle
        self.d_updateCannonPosition(avId)
        
    # Distributed (broadcast ram)
    def d_updateCannonPosition(self, avId):
        self.sendUpdate("updateCannonPosition", [avId, self.rotation, self.angle])
        
    # Distributed (required broadcast ram)
    def getPosHpr(self):
        return self.posHpr

    # Distributed (required broadcast ram)
    # Needs this because setPartyId is dc required.
    def getActivityDoId(self):
        return self.activityDoId

    # Distributed (clsend airecv)
    # a client is telling us that their cannon's fuse is lit
    def setCannonLit(self, zRot, angle):
        avId = self.air.getAvatarIdFromSender()
        self.__cannonIsLit(avId, zRot, angle)
        
    def __cannonIsLit(self, avId, zRot, angle):
        if avId == self.toonInsideAvId:
            self.__stopTimeout()
            self.lit = True
            self.rotation = zRot
            self.angle = angle
            self.notify.debug("__cannonIsLit: %d: zRot = %d, angle = %d" % (avId, zRot, angle))
            # Send out that this cannon is ready to fire.            
            messenger.send(DistributedPartyCannonAI.CANNON_LIT_EVENT, [self.doId, self.toonEnteredTime])
        else:
            self.notify.warning("__cannonIsLit but avId=%s toonInsideAvId=%s" % (str(avId), str(self.toonInsideAvId)))
            
    # Distributed (clsend airecv)
    def setFired(self):
        assert(self.notify.debug("%s setFired" % self.doId))
        senderId = self.air.getAvatarIdFromSender()
        if self.lit:
            self.ignore(self.air.getAvatarExitEvent(senderId))
            self.ignore("bootAvFromParty-%d" % senderId)
            self.notify.debug("sending PartyGlobals.CANNON_MOVIE_CLEAR for %d" % self.toonInsideAvId)
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_CLEAR, self.toonInsideAvId)
            self.__clearToonInside()
        else:
            self.notify.warning("%d setFired called but not lit" % self.doId)

    # Distributed (clsend airecv)
    def setLanded(self, avId):
        assert(self.notify.debug("%s setLanded" % self.doId))
        self.ignore(self.air.getAvatarExitEvent(avId))
        self.ignore("bootAvFromParty-%d" % avId)
        self.notify.debug("%d sending PartyGlobals.CANNON_MOVIE_LANDED for %d" % (self.doId,avId))
        self.d_setMovie(PartyGlobals.CANNON_MOVIE_LANDED, avId)
        self.__clearToonInside()

#===============================================================================
# Functions
#===============================================================================
    # Distributed (clsend airecv)
    def setTimeout(self):
        senderId = self.air.getAvatarIdFromSender()
        if senderId == self.toonInsideAvId:
            self.__startTimeout(PartyGlobals.CANNON_TIMEOUT + 3)

    def __startTimeout(self, timeLimit):
        # Sets the timeout counter running.  If __stopTimeout() is not
        # called before the time expires, we'll exit the avatar.  This
        # prevents avatars from hanging out in the fishing spot all
        # day.
        self.notify.debug("__startTimeout %s" % self.taskName("timeout"))
        self.__stopTimeout()
        self.notify.debug("done calling __stopTimeout, really starting it %s" % self.taskName("timeout"))
        self.timeoutTask = taskMgr.doMethodLater(timeLimit,
                                                 self.__handleTimeoutTask,
                                                 self.taskName("timeout"))

    def __stopTimeout(self):
        """
        Stops a previously-set timeout from expiring.
        """
        self.notify.debug("__stopTimeout %s" % self.taskName("timeout"))
        if self.timeoutTask != None:
            taskMgr.remove(self.timeoutTask)
            self.timeoutTask = None
            self.notify.debug("%d __stopTimeout successful" % self.doId)
        else:
            self.notify.debug("%d __stopTimeout no timeoutTask" % self.doId)

    def __handleTimeoutTask(self, task):
        """
        Called when a timeout expires, this sends the avatar home
        """
        self.notify.warning('Timeout expired! toonInside=%s' % str(self.toonInsideAvId))
        #self.__cannonIsLit(self.toonInsideAvId, self.rotation, self.angle)
        self.__doExit()
        return Task.done

    def __handleUnexpectedExit(self, avId):
        """
        Handle in case the client crashes and the toon disappears, etc.
        """
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        if self.toonInsideAvId == avId:
            self.__doExit()
            self.__clearToonInside()

    def __handleBootMessage(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' got booted.')
        self.__doExit()

    def __doExit(self):
        """
        Take the avatar out of the cannon because he's been in it
        too long without firing.
        """
        self.notify.debug("__doExit sending PartyGlobals.CANNON_MOVIE_FORCE_EXIT to %d" % self.toonInsideAvId)
        self.d_setMovie(PartyGlobals.CANNON_MOVIE_FORCE_EXIT, self.toonInsideAvId)
        self.__clearToonInside()

    def forceInsideToonToExit(self):
        """just call __doExit."""
        self.__doExit()

from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectAI
from toontown.minigame import Trajectory
from toontown.estate import DistributedCannonAI
from toontown.estate import CannonGlobals
from toontown.minigame import CannonGameGlobals

#class DistributedLawbotCannonAI (DistributedCannonAI.DistributedCannonAI):
class DistributedLawbotCannonAI (DistributedObjectAI.DistributedObjectAI):

    notify = directNotify.newCategory("DistributedLawbotCannonAI")

    def __init__(self, air, lawbotBoss, index, x, y, z, h, p, r):
        assert self.notify.debug('__init__')
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        #DistributedCannonAI.DistributedCannonAI.__init__(self, air, 0, x, y ,z, h, p, r)
        
        self.index = index
        self.posHpr = [x, y, z, h, p, r]
        self.boss = lawbotBoss
        self.bossId = lawbotBoss.doId
        self.avId = 0 #which avatar is using this cannon

    def delete(self):
        assert self.notify.debug('delete')
        self.ignoreAll()
        #self.__stopTimeout()
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
        
    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one
    def getBossCogId(self):
        return self.boss.doId

    def getIndex(self):
        return self.index
                 


    def getPosHpr(self):
        assert self.notify.debug('getPosHpr')
        return self.posHpr

    def canEnterCannon(self):
        avId = self.air.getAvatarIdFromSender()
        
        if self.boss.getCannonBallsLeft(avId) == 0:
            return False

        if not self.boss.state == 'BattleTwo':
            #self.notify.warning('got cannon requestEnter with state at %s' % self.boss.state)
            return False

        if not ( (self.avId == 0) or (self.avId == avId) ):
            return False

        return True
        

    def requestEnter(self):
        assert self.notify.debug('requestEnter')
        avId = self.air.getAvatarIdFromSender()

        if not self.canEnterCannon():
            return
        
        if (self.avId == 0) or (self.avId == avId):
            self.avId = avId

            self.boss.toonEnteredCannon(self.avId, self.index)
            cannonBallsLeft = self.boss.getCannonBallsLeft(avId)
            assert self.notify.debug('%d cannonBallsLeft=%d' %(avId,cannonBallsLeft))
            self.setMovie(CannonGlobals.CANNON_MOVIE_LOAD, self.avId, cannonBallsLeft)

            # Handle unexpected exit
            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            self.__handleUnexpectedExit, extraArgs=[avId])

        else:
            self.air.writeServerEvent('suspicious', avId, 'DistributedCannonAI.requestEnter cannon already occupied')
            self.notify.warning("requestEnter() - cannon already occupied")


    def setMovie(self, mode, avId, extraInfo):
        self.avId = avId
        self.sendUpdate("setMovie", [mode, avId, extraInfo])
        
    
    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.__doExit()

    def __doExit(self):
        # Take the avatar out of the cannon because he's been in it
        # too long without firing. Or he could have just pressed the leave cannon button
        assert self.notify.debug('__doExit')
        self.setMovie(CannonGlobals.CANNON_MOVIE_FORCE_EXIT, self.avId,0)
        self.avId = 0
        
    def requestLeave(self):
        assert self.notify.debug('requestLeave')
        avId = self.air.getAvatarIdFromSender()
        if (self.avId != 0):
            self.__doExit()
        else:
            self.air.writeServerEvent('suspicious', avId, 'DistributedCannonAI.requestLeave cannon not occupied')
            self.notify.warning("requestLeave() - cannon not occupied")

    def setCannonPosition(self, zRot, angle):
        avId = self.air.getAvatarIdFromSender()
        # a client is sending a position update for their cannon
        self.notify.debug("setCannonPosition: " + str(avId) +
                          ": zRot=" + str(zRot) + ", angle=" + str(angle))
        self.sendUpdate("updateCannonPosition", [avId, zRot, angle])

    def setLanded(self):
        assert(self.notify.debug("%s setLanded" % self.doId))
        self.ignore(self.air.getAvatarExitEvent(self.avId))

        if self.canEnterCannon():
            self.requestEnter()
        else:
            self.setMovie(CannonGlobals.CANNON_MOVIE_LANDED, 0, 0)        

    def setCannonLit(self, zRot, angle):
        """Handle the client telling AI he's firing his cannon."""
        assert self.notify.debug('setCannon:it')

        if not self.boss.state == 'BattleTwo':
            self.notify.debug('ignoring setCannonList since boss in state %s' % self.boss.state)
            return 
        
        avId = self.air.getAvatarIdFromSender()

        if self.boss.getCannonBallsLeft(avId) == 0:
            self.notify.debug('ignoring setCannonList since no balls left for %s' % avId)
            return
        
        #self.__stopTimeout()
        # a client is telling us that their cannon's fuse is lit
        self.notify.debug("setCannonLit: " + str(avId) + ": zRot=" +
                          str(zRot) + ", angle=" + str(angle))
        fireTime = CannonGameGlobals.FUSE_TIME
        # set the cannon to go off in the near future
        self.sendUpdate("setCannonWillFire", [avId, fireTime, zRot, angle,
                                globalClockDelta.getRealNetworkTime()])
        self.boss.decrementCannonBallsLeft(avId)

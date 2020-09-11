from otp.level import DistributedEntityAI
from toontown.coghq import MoleFieldBase
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal

class DistributedMoleFieldAI(DistributedEntityAI.DistributedEntityAI,
                             MoleFieldBase.MoleFieldBase):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMoleFieldAI')

    def __init__(self, level, entId):
        """Constructor for the AI Molefield."""
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)

        self.whackedMoles = {} # key is mole Index, value is the popupNum it was whacked
        self.numMolesWhacked = 0
        self.roundsFailed = 0
        self.started = 0

        self.challengeDefeated = False
        
    def announceGenerate(self):
        """Load fields dependent on required fields."""
        DistributedEntityAI.DistributedEntityAI.announceGenerate(self)
        self.numMoles = self.numSquaresX * self.numSquaresY
        self.moleFieldEndTimeTaskName = self.uniqueName('moleFieldEndTime')
        self.GameDuration = self.timeToPlay
        numToons = 0
        
        if hasattr(self, 'level'):
            numToons =  len(self.level.presentAvIds)
        
        self.moleTarget = self.molesBase + (self.molesPerPlayer * numToons)

    def delete(self):
        """Clean up."""
        DistributedEntityAI.DistributedEntityAI.delete(self)
        self.removeAllTasks()                

    def setClientTriggered(self):
        """A player entered us, start the moles."""
        if not hasattr(self, 'gameStartTime'):
            self.gameStartTime = globalClock.getRealTime()
        if not self.started:
            self.b_setGameStart(globalClockDelta.localToNetworkTime(\
                                self.gameStartTime), self.moleTarget, self.timeToPlay)
            self.started = 1

    def b_setGameStart(self, timestamp, moleTarget, timeToPlay):
        # send the distributed message first, so that any network msgs
        # sent by the subclass upon start of the game will arrive
        # after the game start msg
        self.d_setGameStart(timestamp, moleTarget, timeToPlay)
        self.setGameStart(timestamp)

    def d_setGameStart(self, timestamp, moleTarget, timeToPlay):
        self.notify.debug("BASE: Sending setGameStart")
        self.sendUpdate("setGameStart", [timestamp, moleTarget, timeToPlay])

    def setGameStart(self, timestamp):
        """
        This method gets called when all avatars are ready
        Inheritors should call this plus the code to start the game
        """
        self.GameDuration = self.timeToPlay
        self.notify.debug("BASE: setGameStart")
        self.prepareForGameStartOrRestart()

    def prepareForGameStartOrRestart(self):
        """Zero out needed fields on a start or restart of the mole field."""
        self.GameDuration = self.timeToPlay
        self.scheduleMoles()
        self.whackedMoles = {} # key is mole Index, value is the popupNum it was whacked
        # makes sure we don't reset self.numMolesWhacked, otherwise a solo player will
        # never finish
        self.doMethodLater(self.timeToPlay, self.gameEndingTimeHit, self.moleFieldEndTimeTaskName  )


    def whackedMole(self, moleIndex, popupNum):
        """Handle the client whacking a mole."""
        # TODO check with self.schedule if it really is a valid mole whack
        validMoleWhack = False
        if self.whackedMoles.has_key(moleIndex):
            if self.whackedMoles[moleIndex] < popupNum:
                validMoleWhack = True
        else:
            self.whackedMoles[moleIndex] = popupNum
            validMoleWhack = True

        if validMoleWhack:
            # we have a valid mole whack
            self.numMolesWhacked += 1
            self.sendUpdate('updateMole',[moleIndex, self.WHACKED])
            self.sendUpdate('setScore', [self.numMolesWhacked])

        self.checkForTargetReached()
        
    def whackedBomb(self, moleIndex, popupNum, timestamp):
        """Handle the client whacking a mole."""
        # TODO check with self.schedule if it really is a valid mole whack
        senderId = self.air.getAvatarIdFromSender()
        #timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('reportToonHitByBomb',[senderId, moleIndex,timestamp])
        

    def checkForTargetReached(self):
        """Check if the target number of moles has been reached. Then end if needed"""
        if self.numMolesWhacked >= self.moleTarget:
            if not self.challengeDefeated:
                self.forceChallengeDefeated()

    def forceChallengeDefeated(self, pityWin = False):
        """Force the mole field to be defeated and open the door."""
        self.challengeDefeated = True
        self.removeTask(self.moleFieldEndTimeTaskName)
        # unlock the door blocking this room
        roomId = self.getLevelDoId()
        room = simbase.air.doId2do.get(roomId)
        if room:
            self.challengeDefeated = True
            room.challengeDefeated()
            # tell the lock that it should open
            eventName = self.getOutputEventName()
            messenger.send(eventName,[1])
            if pityWin:
                self.sendUpdate('setPityWin')
                
        
    def gameEndingTimeHit(self, task):
        """Handle the game hitting its ending time."""
        # tell the ai to damage the playing toons
        if (self.numMolesWhacked < self.moleTarget) and (self.roundsFailed < 4):
            roomId = self.getLevelDoId()
            room = simbase.air.doId2do.get(roomId)
            self.roundsFailed += 1
            #if room:
            #    playerIds = room.presentAvIds
            #    for avId in playerIds:
            #        av = simbase.air.doId2do.get(avId)
                    #if av:
                    #    av.takeDamage(self.DamageOnFailure, quietly=0)
                    #    room.sendUpdate('forceOuch',[self.DamageOnFailure])
            self.restartGame()
        elif self.roundsFailed >= 4:
            # take pity on the player and open the door, he's already lost 80 laff
            if not self.challengeDefeated:
                self.forceChallengeDefeated(pityWin = True)
            
    def damageMe(self):
        roomId = self.getLevelDoId()
        room = simbase.air.doId2do.get(roomId)
        if not room:
            # this can come from a lagging client
            # or come in between our requestDelete and delete calls
            return
        senderId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(senderId)
        playerIds = room.presentAvIds
        if av and (senderId in playerIds):
            av.takeDamage(self.DamageOnFailure, quietly=0)
            room.sendUpdate('forceOuch',[self.DamageOnFailure])

    def restartGame(self):
        if not hasattr(self, 'entId'):
            return
        """Restart the game since the target wasn't reached."""
        self.gameStartTime = globalClock.getRealTime()
        self.started = 0
        self.b_setGameStart(globalClockDelta.localToNetworkTime(\
                            self.gameStartTime), self.moleTarget, self.timeToPlay)       

    def getScore(self):
        """Return the current score."""
        return self.numMolesWhacked
        

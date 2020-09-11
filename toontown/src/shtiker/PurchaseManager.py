from pandac.PandaModules import *
from PurchaseManagerConstants import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import TravelGameGlobals

class PurchaseManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("PurchaseManager")

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.playAgain = 0

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        self.ignoreAll()

    def setPlayerIds(self, *playerIds):
        self.notify.debug("setPlayerIds: %s" % (playerIds,))
        self.playerIds = playerIds

    def setNewbieIds(self, newbieIds):
        self.notify.debug("setNewbieIds: %s" % (newbieIds,))
        self.newbieIds = newbieIds

    def setMinigamePoints(self, *mpArray):
        self.notify.debug("setMinigamePoints: %s" % (mpArray,))
        self.mpArray = mpArray

    def setPlayerMoney(self, *moneyArray):
        self.notify.debug("setPlayerMoney: %s" % (moneyArray,))
        self.moneyArray = moneyArray

    def setPlayerStates(self, *stateArray):
        self.notify.debug("setPlayerStates: %s" % (stateArray,))
        self.playerStates = stateArray
        # Do whatever you do to update the gui states of the players
        # only do this if we are generated and have localToon
        if self.isGenerated() and self.hasLocalToon:
            self.announcePlayerStates()

    def setCountdown(self, timestamp):
        self.countdownTimestamp = timestamp

    def announcePlayerStates(self):
        messenger.send("purchaseStateChange", [self.playerStates])

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.hasLocalToon = self.calcHasLocalToon()
        if self.hasLocalToon:
            # let the rest of the system know the player states
            self.announcePlayerStates()
            # Start the countdown...
            et = globalClockDelta.localElapsedTime(self.countdownTimestamp)
            remain = PURCHASE_COUNTDOWN_TIME - et
            # Hang hooks for when the buttons get hit
            self.acceptOnce("purchasePlayAgain", self.playAgainHandler)
            self.acceptOnce("purchaseBackToToontown",
                            self.backToToontownHandler)
            self.acceptOnce("purchaseTimeout", self.setPurchaseExit)
            self.accept("boughtGag", self.__handleBoughtGag)
            # Do whatever you do to display the purchase screen here
            base.cr.playGame.hood.fsm.request("purchase",
                                                   [self.mpArray,
                                                    self.moneyArray,
                                                    self.playerIds,
                                                    self.playerStates,
                                                    remain,
                                                    self.metagameRound,
                                                    self.votesArray])

    def calcHasLocalToon(self):
        """ returns true if we 'own' localToon """
        retval = ((base.localAvatar.doId not in self.newbieIds) and
                (base.localAvatar.doId in self.playerIds))

        if self.metagameRound > -1 and \
           self.metagameRound < TravelGameGlobals.FinalMetagameRoundIndex:
            # if we are in the middle of a metagame ignore newbieness
            retval = base.localAvatar.doId in self.playerIds

        self.notify.debug('calcHasLocalToon returning %s' % retval)
        return retval
        

    def playAgainHandler(self):
        self.d_requestPlayAgain()

    def backToToontownHandler(self):
        self.notify.debug("requesting exit to toontown...")
        self.d_requestExit()
        self.playAgain = 0
        self.setPurchaseExit()
        
    def d_requestExit(self):
        self.sendUpdate("requestExit", [])

    def d_requestPlayAgain(self):
        self.notify.debug("requesting play again...")
        self.sendUpdate("requestPlayAgain", [])
        self.playAgain = 1
        # Go into "Waiting for other players" state...

    def d_setInventory(self, invString, money, done):
        # Report our inventory to the server
        self.sendUpdate("setInventory", [invString, money, done])

    def __handleBoughtGag(self):
        # Send each gag purchase to the AI as we go.
        self.d_setInventory(base.localAvatar.inventory.makeNetString(),
                            base.localAvatar.getMoney(), 0)

    def setPurchaseExit(self):
        if self.hasLocalToon:
            self.ignore("boughtGag")
            # Report our purchases
            self.d_setInventory(base.localAvatar.inventory.makeNetString(),
                                base.localAvatar.getMoney(), 1)
            # Shutdown the purchase window, and go to where we are supposed
            # to go
            messenger.send("purchaseOver", [self.playAgain])

    def setMetagameRound(self, round):
        self.notify.debug("setMetagameRound: %s" % (round,))        
        self.metagameRound = round

    def setVotesArray(self, votesArray):
        """
        Since we now convert some votes left to beans, we need to pass this
        information to the client, so we can put it in the show
        """
        self.notify.debug('setVotesArray: %s' % votesArray)
        self.votesArray = votesArray

from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from PurchaseManagerConstants import *
import copy
from direct.task.Task import Task

from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import TravelGameGlobals

class PurchaseManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("PurchaseManagerAI")

    def __init__(self, air, playerArray, mpArray, previousMinigameId,
                 trolleyZone, newbieIdList=[], votesArray =None, metagameRound=-1,
                 desiredNextGame = None):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.playerIds = copy.deepcopy(playerArray)
        self.minigamePoints = copy.deepcopy(mpArray)
        self.previousMinigameId = previousMinigameId
        self.trolleyZone = trolleyZone
        self.newbieIds = copy.deepcopy(newbieIdList)
        self.isShutdown = 0
        if votesArray:
            self.votesArray = copy.deepcopy(votesArray)
        else:
            self.votesArray = []
        
        self.metagameRound = metagameRound #this refers to the previous game played
        self.desiredNextGame = desiredNextGame

        # pad playerIds and minigamePoints to have 4 numbers; pad with zeroes
        for i in range(len(self.playerIds), 4):
            self.playerIds.append(0)
        for i in range(len(self.minigamePoints), 4):
            self.minigamePoints.append(0)

        # Initialize the states of the players
        self.playerStates = [None, None, None, None]
        self.playersReported = [None, None, None, None]

        assert (len(self.playerIds) == len(self.playerStates) == len(self.minigamePoints))

        # create an array to keep track of the player's starting money
        self.playerMoney = [0, 0, 0, 0]

        # set up the initial states of all toons
        for i in range(len(self.playerIds)):
            avId = self.playerIds[i]
            # 0 means no player, 1, 2, and 3 are suits.
            if avId <= 3:
                self.playerStates[i] = PURCHASE_NO_CLIENT_STATE
                self.playersReported[i] = PURCHASE_CANTREPORT_STATE
            # Player is in dictionary
            elif self.air.doId2do.has_key(avId):
                if avId not in self.getInvolvedPlayerIds():
                    # either we are a normal purchaseMgr with some newbies, or
                    # we're a newbie purchaseMgr with non-newbies; either way,
                    # this toon does not belong to us. Mark them as having
                    # chosen to leave
                    self.playerStates[i] = PURCHASE_EXIT_STATE
                    self.playersReported[i] = PURCHASE_REPORTED_STATE
                else:
                    self.playerStates[i] = PURCHASE_WAITING_STATE
                    self.playersReported[i] = PURCHASE_UNREPORTED_STATE
            # Player must be disconnected
            else:
                self.playerStates[i] = PURCHASE_DISCONNECTED_STATE
                self.playersReported[i] = PURCHASE_CANTREPORT_STATE

        # more processing for the toons that we 'own'
        for avId in self.getInvolvedPlayerIds():
            # 0 means no player, 1, 2, and 3 are suits.
            if avId > 3 and self.air.doId2do.has_key(avId):
                self.acceptOnce(self.air.getAvatarExitEvent(avId),
                                self.__handleUnexpectedExit,
                                extraArgs=[avId])
                av = self.air.doId2do[avId]
                avIndex = self.findAvIndex(avId)
                # record the starting money for reward screen
                money = av.getMoney()
                if avIndex == None:
                    self.notify.warning('__init__ avIndex is none but avId=%s' % avId)
                    continue
                self.playerMoney[avIndex] = money
                # Update us and the client avatar with t
                av.addMoney(self.minigamePoints[avIndex])

                # Log the completion (and beans won) to the event server
                self.air.writeServerEvent('minigame',
                                          avId, '%s|%s|%s|%s' % (
                    self.previousMinigameId, self.trolleyZone,
                    self.playerIds, self.minigamePoints[avIndex]))

                if self.metagameRound == TravelGameGlobals.FinalMetagameRoundIndex:
                    # lets add some extra beans from the remaining votes
                    numPlayers = len (self.votesArray)
                    extraBeans = self.votesArray[avIndex] * \
                                 TravelGameGlobals.PercentOfVotesConverted[numPlayers] / 100.0
                    av.addMoney(extraBeans)
                    # Log the completion (and extra beans won) to the event server
                    self.air.writeServerEvent('minigame_extraBeans',
                                              avId, '%s|%s|%s|%s' % (
                        self.previousMinigameId, self.trolleyZone,
                        self.playerIds, extraBeans))

        # Flags to indicate state.
        #self.receivingInventory = 0
        # NOTE: JNS changed this to be one because it wasn't properly
        # handling the case of people exiting to Toontown. This bears
        # further examination.
        self.receivingInventory = 1
        self.receivingButtons = 1
        return None

    def delete(self):
        taskMgr.remove(self.uniqueName("countdown-timer"))
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def getInvolvedPlayerIds(self):
        """ everyone but the newbies """
        avIds = []
        for avId in self.playerIds:
            if not avId in self.newbieIds:
                avIds.append(avId)
            else:
                # this is a newbie, but if we are in the middle of a metagame
                # make him continue
                if self.metagameRound > -1 and \
                   self.metagameRound < TravelGameGlobals.FinalMetagameRoundIndex:
                    avIds.append(avId)
                
                
        return avIds

    def getMinigamePoints(self):
        return self.minigamePoints

    def getPlayerIds(self):
        return self.playerIds

    def getNewbieIds(self):
        return self.newbieIds

    def getPlayerMoney(self):
        return self.playerMoney

    def d_setPlayerStates(self, stateArray):
        self.sendUpdate("setPlayerStates", stateArray)
        return None

    def getPlayerStates(self):
        return self.playerStates

    # The countdown starts when we create the screen.
    def getCountdown(self):
        assert(self.notify.debug("Starting the purchase countdown..."))
        self.startCountdown()
        return globalClockDelta.getRealNetworkTime()

    def startCountdown(self):
        if not config.GetBool('disable-purchase-timer', 0):
            taskMgr.doMethodLater(PURCHASE_COUNTDOWN_TIME, self.timeIsUpTask,
                                  self.uniqueName("countdown-timer"))

    # Client requests
    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        avIndex = self.findAvIndex(avId)
        if avIndex is None:
            self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestExit: unknown avatar: %s' %
                                      (avId, ))
            return
        if self.receivingButtons:
            if self.air.doId2do.has_key(avId):
                av = self.air.doId2do[avId]
                if avIndex == None:
                    self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestExit not on list')
                    self.notify.warning("Avatar " + str(avId) +
                                        " requested Exit, but is not on the list!")
                else:
                    avState = self.playerStates[avIndex]
                    if ((avState == PURCHASE_PLAYAGAIN_STATE) or
                        (avState == PURCHASE_WAITING_STATE)):
                        self.playerStates[avIndex] = PURCHASE_EXIT_STATE
                        self.handlePlayerLeaving(avId)
                    else:
                        self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestExit invalid transition to exit')
                        self.notify.warning("Invalid transition to exit state.")
            else:
                self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestExit unknown avatar')
                self.notify.warning("Avatar " + str(avId) +
                                    " requested Exit, but is not in doId2do." +
                                    " Assuming disconnected.")
                self.playerStates[avIndex] = PURCHASE_DISCONNECTED_STATE
                self.playersReported[avIndex] = PURCHASE_CANTREPORT_STATE
                self.ignore(self.air.getAvatarExitEvent(avId))
            self.d_setPlayerStates(self.playerStates)
            if self.getNumUndecided() == 0:
                self.timeIsUp()
        else:
            self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestExit not receiving requests now')
            self.notify.warning(
                "Avatar " + str(avId) +
                " requested Exit, but I am not receiving button requests now.")
        return None

    def requestPlayAgain(self):
        avId = self.air.getAvatarIdFromSender()
        if self.findAvIndex(avId) == None:
            self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestPlayAgain: unknown avatar')
            return
        if self.receivingButtons:
            if self.air.doId2do.has_key(avId):
                av = self.air.doId2do[avId]
                avIndex = self.findAvIndex(avId)
                if avIndex == None:
                    self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestPlayAgain not on list')
                    self.notify.warning(
                        "Avatar " + str(avId) +
                        " requested PlayAgain, but is not on the list!")
                else:
                    avState = self.playerStates[avIndex]
                    if (avState == PURCHASE_WAITING_STATE):
                        self.notify.debug(str(avId) + " wants to play again")
                        self.playerStates[avIndex] = PURCHASE_PLAYAGAIN_STATE
                    else:
                        self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestPlayAgain invalid transition to PlayAgain')
                        self.notify.warning(
                            "Invalid transition to PlayAgain state.")
            else:
                self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestPlayAgain unknown avatar')
                self.notify.warning(
                    "Avatar " + str(avId) +
                    " requested PlayAgain, but is not in doId2do." +
                    " Assuming disconnected.")
                avIndex = self.findAvIndex(avId)
                self.playerStates[avIndex] = PURCHASE_DISCONNECTED_STATE
                self.playersReported[avIndex] = PURCHASE_CANTREPORT_STATE
                self.ignore(self.air.getAvatarExitEvent(avId))
            self.d_setPlayerStates(self.playerStates)
            if self.getNumUndecided() == 0:
                self.timeIsUp()
        else:
            self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.requestPlayAgain not receiving requests now')
            self.notify.warning(
                "Avatar " + str(avId) +
                " requested PlayAgain, but I am not receiving button " +
                "requests now.")
        return None

    def setInventory(self, blob, newMoney, done):
        avId = self.air.getAvatarIdFromSender()
        if self.receivingInventory:
            if self.air.doId2do.has_key(avId):
                av = self.air.doId2do[avId]
                avIndex = self.findAvIndex(avId)
                if avIndex == None:
                    self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.setInventory not on list')
                    self.notify.warning(
                        "Avatar " + str(avId) +
                        " requested purchase, but is not on the list!")
                else:
                    newInventory = av.inventory.makeFromNetString(blob)
                    currentMoney = av.getMoney()
                    if av.inventory.validatePurchase(newInventory, currentMoney, newMoney):
                        av.setMoney(newMoney)
                        if not done:
                            return
                        # Sanity check for double reporting
                        if (self.playersReported[avIndex] != PURCHASE_UNREPORTED_STATE):
                            self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.setInventory bad report state')
                            self.notify.warning(
                                "Bad report state: " +
                                str(self.playersReported[avIndex]))
                        else:
                            # Tell the state server about the purchase
                            av.d_setInventory(av.inventory.makeNetString())
                            av.d_setMoney(newMoney)
                    else:
                        self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.setInventory invalid purchase')
                        self.notify.warning("Avatar " + str(avId) +
                                            " attempted an invalid purchase.")
                        # Make sure the avatar is in sync with the AI.
                        av.d_setInventory(av.inventory.makeNetString())
                        av.d_setMoney(av.getMoney())
                        
                    # Record report
                    self.playersReported[avIndex] = PURCHASE_REPORTED_STATE
                    # Test to see if we are waiting on anyone else
                    if self.getNumUnreported() == 0:
                        self.shutDown()
                        
        else:
            self.air.writeServerEvent('suspicious', avId, 'PurchaseManager.setInventory not receiving inventory')
            self.notify.warning("Not receiving inventory. Ignored " +
                                str(avId) + "'s request")
        return None

    # Time is up, clients! You can send your inventory requests now!
    def d_setPurchaseExit(self):
        self.sendUpdate("setPurchaseExit", [])
        return None

    # When time is up, let everyone know.
    def timeIsUpTask(self, task):
        self.timeIsUp()
        return Task.done

    def timeIsUp(self):
        assert(self.receivingButtons)
        # Tell the clients that time is up
        self.d_setPurchaseExit()
        # Remove the countdown
        taskMgr.remove(self.uniqueName("countdown-timer"))
        # No longer receiving buttons
        self.receivingButtons = 0
        # Now receiving inventory
        self.receivingInventory = 1
        # Hang out, waiting for inventory info to come in.
        return None

    def getVotesArrayMatchingPlayAgainList(self, playAgainList):
        """
        make sure votesArray is consistent with those playing again,
        since someone may have dropped
        """
        retval = []

        for playAgainIndex in range(len(playAgainList)):
            avId = playAgainList[playAgainIndex]
            origIndex = self.playerIds.index(avId)
            if self.votesArray and origIndex < len(self.votesArray) :
                retval.append(self.votesArray[origIndex])
            else:
                retval.append(0)
            

        return retval

    def shutDown(self):
        if self.isShutdown:
            # We no longer own the zoneId.  If we accidentally come by
            # here again, we don't want to try to deallocate it again (or
            # hand it off to another minigame).
            # Note: We cannot set the zoneId to None because the AIRepository
            # needs to remove us from the zoneId2doIds dict
            # Maybe someone called shutDown twice.
            self.notify.warning("Got shutDown twice")
            return
        self.isShutdown = 1

        # This must be imported here rather than at the top of the
        # file in order to avoid circular imports.
        from toontown.minigame import MinigameCreatorAI

        # Does anyone want to play again?
        playAgainNum = self.getNumPlayAgain()
        assert(playAgainNum >=0 and playAgainNum <= 4)
        # If so, start a minigame in this zone
        if playAgainNum > 0:
            playAgainList = self.getPlayAgainList()
            newVotesArray = self.getVotesArrayMatchingPlayAgainList(playAgainList)
            newRound = self.metagameRound;
            newbieIdsToPass = [] 
            if newRound > -1:
                newbieIdsToPass= self.newbieIds # we must pass this on
                if newRound < TravelGameGlobals.FinalMetagameRoundIndex:
                    newRound+= 1
                else:
                    newRound = 0
                    newVotesArray = [TravelGameGlobals.DefaultStartingVotes] * len(playAgainList)
                    
            # but if we only have one player left, don't start the metagame
            if len(playAgainList) == 1 and \
               simbase.config.GetBool('metagame-min-2-players', 1):
                newRound = -1
                    
            MinigameCreatorAI.createMinigame(
                self.air, playAgainList,
                self.trolleyZone,
                minigameZone = self.zoneId,
                previousGameId = self.previousMinigameId,
                newbieIds = newbieIdsToPass,
                startingVotes = newVotesArray, 
                metagameRound = newRound,
                desiredNextGame = self.desiredNextGame)
        # If not, deallocate this zone, so it can be reused in the future.
        else:
            MinigameCreatorAI.releaseMinigameZone(self.zoneId)

        # That's it for us!
        self.requestDelete()

        # Don't listen for any more unexpected avatar exit events.
        self.ignoreAll()
        return None

    # Find the index for a given avId. Return None if there isn't one.
    def findAvIndex(self, avId):
        for i in range(len(self.playerIds)):
            if avId == self.playerIds[i]:
                return i
        return None

    # Return the number of players that we are still waiting on.
    def getNumUndecided(self):
        undecidedCounter = 0
        for playerState in self.playerStates:
            if playerState == PURCHASE_WAITING_STATE:
                undecidedCounter += 1
        return undecidedCounter

    def getPlayAgainList(self):
        playAgainList = []
        assert(len(self.playerStates) == 4)
        for i in range(len(self.playerStates)):
            if self.playerStates[i] == PURCHASE_PLAYAGAIN_STATE:
                playAgainList.append(self.playerIds[i])
        return playAgainList

    def getNumPlayAgain(self):
        playAgainCounter = 0
        for playerState in self.playerStates:
            if playerState == PURCHASE_PLAYAGAIN_STATE:
                playAgainCounter += 1
        return playAgainCounter

    def getNumUnreported(self):
        unreportedCounter = 0
        for playerState in self.playersReported:
            if playerState == PURCHASE_UNREPORTED_STATE:
                unreportedCounter += 1
            elif playerState == PURCHASE_REPORTED_STATE:
                pass
            elif playerState == PURCHASE_CANTREPORT_STATE:
                pass
            else:
                self.notify.warning("Weird report state: " + str(playerState))
        return unreportedCounter

    def __handleUnexpectedExit(self, avId):
        self.notify.warning("Avatar: " + str(avId) +
                            " has exited unexpectedly")
        # Find the avatar's index
        index = self.findAvIndex(avId)
        if index == None:
            self.notify.warning("Something is seriously screwed up..." +
                                "An avatar exited unexpectedly, and they" +
                                " are not on my list!")
        else:
            self.playerStates[index] = PURCHASE_DISCONNECTED_STATE
            self.playersReported[index] = PURCHASE_CANTREPORT_STATE
            self.d_setPlayerStates(self.playerStates)
            if self.receivingButtons:
                if self.getNumUndecided() == 0:
                    self.timeIsUp()
            # changed from elif to if to force cleanup (they were leaking) - grw
            if self.receivingInventory:
                if self.getNumUnreported() == 0:
                    self.shutDown()

        return None

    def handlePlayerLeaving(self, avId):
        pass

    def getMetagameRound(self):
        return self.metagameRound

    def getVotesArray(self):
        return self.votesArray

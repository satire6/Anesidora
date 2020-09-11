"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""

from DistributedMinigameAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.minigame import PlayingCardGlobals
from toontown.minigame import PlayingCard
from toontown.minigame.PlayingCard import PlayingCardBase
from toontown.minigame import PlayingCardDeck
from toontown.minigame import PairingGameGlobals
from toontown.ai.ToonBarrier import ToonBarrier

class DistributedPairingGameAI(DistributedMinigameAI):

    notify = directNotify.newCategory("DistributedPairingGameAI")

    OneCardInMultiplayer = True # do we restrict it to one card open
    TurnDownTwoAtATime = True # when we open a 3rd card, do we close down the other 2 

    def __init__(self, air, minigameId):
        try:
            self.DistributedPairingGameAI_initialized
        except:
            self.DistributedPairingGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedPairingGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['play']),
                                    State.State('play',
                                                self.enterPlay,
                                                self.exitPlay,
                                                ['cleanup']),
                                    State.State('cleanup',
                                                self.enterCleanup,
                                                self.exitCleanup,
                                                ['inactive']),
                                    ],
                                   # Initial State
                                   'inactive',
                                   # Final State
                                   'inactive',
                                   )

            # Add our game ClassicFSM to the framework ClassicFSM
            self.addChildGameFSM(self.gameFSM)

            self.gameFSM.enterInitialState()

            self.deckSeed = random.randint(0, 4000000)
            #self.deckSeed = 0
            self.faceUpDict  = {} # which cards are face up per toon
            self.inactiveList = [] # which cards are out of play
            self.maxOpenCards = 2
            self.points = 0
            self.flips = 0
            self.matches = 0
            self.cards = []
            self.gameDuration = 90
    
    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")

        # make sure we broadcast how many cards open per toon
        if self.OneCardInMultiplayer and len(self.avIdList) > 1:
            self.maxOpenCards = 1
        self.sendUpdate('setMaxOpenCards',[self.maxOpenCards])
        
        DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules

        # init face up dict and other fields
        for avId in self.avIdList:
            self.faceUpDict[avId] = []
        self.deck = PairingGameGlobals.createDeck(self.deckSeed, self.numPlayers)
        for index in xrange(len(self.deck.cards)):
            cardValue = self.deck.cards[index]
            oneCard = PlayingCardBase(cardValue)
            self.cards.append(oneCard)

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.setGameAbort(self)

    def calcLowFlipBonus(self):
        lowFlipModifier = PairingGameGlobals.calcLowFlipModifier(self.matches, self.flips)
        bonus = lowFlipModifier * self.matches
        self.notify.debug('low flip bonus = %d' % bonus)
        return bonus
            
    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        lowFlipBonus = 0
        for avId in self.avIdList:
            self.scoreDict[avId] = max(1, self.points)
            # we know the flips and the matches, calculate low
            lowFlipBonus = self.calcLowFlipBonus()
            self.scoreDict[avId] += lowFlipBonus
            
            if self.matches == len(self.cards) / 2:
                self.scoreDict[avId] += round(len(self.cards) / 4.)
                self.logAllPerfect()                

        # Log balancing variables to the event server
        logAvId = self.avIdList[0]
        self.air.writeServerEvent('minigame_pairing',
                                  self.doId, '%s|%s|%s|%s|%s|%s|%s|%s' % (
            ToontownGlobals.PairingGameId,
            self.getSafezoneId(), self.avIdList, self.scoreDict[logAvId],
            self.gameDuration, self.matches, self.flips, lowFlipBonus)) 
        
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # when the game is done, call gameOver()
        #self.gameOver()
        # set up a barrier to wait for the 'game done' msgs
        def allToonsDone(self=self):
            self.notify.debug('allToonsDone')
            self.sendUpdate('setEveryoneDone')
            if not PairingGameGlobals.EndlessGame:
                self.gameOver()

        def handleTimeout(avIds, self=self):
            self.notify.debug(
                'handleTimeout: avatars %s did not report "done"' %
                avIds)
            self.setGameAbort()

        self.gameDuration = PairingGameGlobals.calcGameDuration(self.getDifficulty())
        self.doneBarrier = ToonBarrier(
            'waitClientsDone',
            self.uniqueName('waitClientsDone'),
            self.avIdList,
            self.gameDuration + MinigameGlobals.latencyTolerance,
            allToonsDone, handleTimeout)

    def exitPlay(self):
        self.doneBarrier.cleanup()
        del self.doneBarrier        
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def getDeckSeed(self):
        return self.deckSeed

    def isCardFaceUp(self, deckOrderIndex):
        retval = False
        for key in self.faceUpDict.keys():
            if deckOrderIndex in self.faceUpDict[key]:
                retval = True
                break
        return retval

    def isCardFaceDown(self, deckOrderIndex):
        return not self.isCardFaceUp(deckOrderIndex)

    def checkForMatch(self):
        faceUpList = []
        for oneToonFaceUpList in self.faceUpDict.values():
            faceUpList += oneToonFaceUpList
        for i in range(len(faceUpList)):
            cardA = faceUpList[i]
            for j in range(i+1, len(faceUpList)):
                cardB = faceUpList[j]
                if self.cards[cardA].rank == self.cards[cardB].rank:
                    return cardA,cardB
        return -1, -1

    def handleMatch(self, cardA, cardB):
        self.notify.debug('we got a match %d %d' % (cardA, cardB))

        for key in self.faceUpDict.keys():
            if cardA in self.faceUpDict[key]:
                self.faceUpDict[key].remove(cardA)
            if cardB in self.faceUpDict[key]:
                self.faceUpDict[key].remove(cardB)                        

        self.inactiveList.append(cardA)
        self.inactiveList.append(cardB)

    def turnDownCard(self, cardA):
        self.notify.debug('turning down card %d' % cardA)
        for key in self.faceUpDict.keys():
            if cardA in self.faceUpDict[key]:
                self.faceUpDict[key].remove(cardA)

    def openCardRequest(self, deckOrderIndex, bonusGlowCard):
        # some other toon opened the card slightly ahead
        if self.isCardFaceUp(deckOrderIndex):
            return

        if self.gameFSM.getCurrentState().getName() != 'play':
            return
        
        #import pdb; pdb.set_trace()
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'openCardRequest from non-player av %s' % avId)
            return
        cardsToTurnDown = []
        faceUpList = self.faceUpDict[avId]
        numCardsFaceUpAtStart = len(faceUpList)        
        if len(faceUpList) >= self.maxOpenCards:
            oldestCard = faceUpList.pop(0)
            cardsToTurnDown.append(oldestCard)
        if self.TurnDownTwoAtATime and numCardsFaceUpAtStart == 2:
            secondOldestCard = faceUpList.pop(0)
            cardsToTurnDown.append(secondOldestCard)
        cardToTurnUp = deckOrderIndex
        self.faceUpDict[avId].append(cardToTurnUp)
        cardA, cardB = self.checkForMatch()
        matchingCard = -1
        if cardA > -1:
            self.handleMatch(cardA, cardB)
            if cardA == deckOrderIndex:
                matchingCard = cardB
            else:
                matchingCard = cardA
            pointsToGive = 1
            if bonusGlowCard in [cardA,cardB]:
                # TODO do some sanity checking that the bonus was legit
                pointsToGive += 1
            self.points += pointsToGive
            self.matches += 1

        self.flips += 1
        self.sendUpdate('openCardResult',[cardToTurnUp, avId, matchingCard, self.points, cardsToTurnDown])


    def reportDone(self):
        if self.gameFSM.getCurrentState().getName() != 'play':
            return

        avId = self.air.getAvatarIdFromSender()
        # all of the objects on this avatar's client have landed
        # or been caught
        self.notify.debug('reportDone: avatar %s is done' % avId)
        self.doneBarrier.clear(avId)

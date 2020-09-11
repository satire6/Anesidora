#################################################################
# File: DistributedPondBingoManager.py
# Purpose: Performs the client-side handling of the
#          Fishing Bingo Gameplay. It generates the necessary
#          card, maintains state, and shows the appropriate
#          GUI for those players who have entered a fishing
#          spot during the alotted Bingo Gameplay.
#################################################################

#################################################################
# Direct Specific Modules
#################################################################
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task

#################################################################
# Toontown Specific Modules
#################################################################
from toontown.fishing import BingoGlobals
from toontown.fishing import BingoCardGui
from toontown.fishing import FishGlobals
from toontown.fishing import NormalBingo
from toontown.fishing import FourCornerBingo
from toontown.fishing import DiagonalBingo
from toontown.fishing import ThreewayBingo
from toontown.fishing import BlockoutBingo
from direct.showbase import RandomNumGen
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

#################################################################
# Python Specific Modules
#################################################################
import time

class DistributedPondBingoManager(DistributedObject.DistributedObject, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPondBingoManager")
    #notify.setDebug(True)

    cardTypeDict = { BingoGlobals.NORMAL_CARD: NormalBingo.NormalBingo,
                     BingoGlobals.FOURCORNER_CARD: FourCornerBingo.FourCornerBingo,
                     BingoGlobals.DIAGONAL_CARD: DiagonalBingo.DiagonalBingo,
                     BingoGlobals.THREEWAY_CARD: ThreewayBingo.ThreewayBingo,
                     BingoGlobals.BLOCKOUT_CARD: BlockoutBingo.BlockoutBingo }
    
#################################################################
# Construction and Destruction Method Definitions
#################################################################
    # Method:  __init__
    # Purpose: This method initializes the Manager object as
    #          well as the FSM and DO objects from which it
    #          inherits.
    # Input: cr - The client repository.
    # Output: None
    ############################################################
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedPondBingoManager')
      
        self.cardId = 0
        self.jackpot = 0
        self.pond = None
        self.spot = None
        self.card = None
        self.hasEntered = 0
        self.initGameState = None
        self.lastCatch = None
        self.typeId = BingoGlobals.NORMAL_CARD

    #############################################################
    # Method: generate
    # Purpose: This method overrides the DistributedObject
    #          generate Method, possibly performing additional
    #          initialization.
    # Input: None
    # Output: None
    #############################################################                         
    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.card = BingoCardGui.BingoCardGui()
        self.card.reparentTo(aspect2d, 1)
        self.card.hideNextGameTimer()
        self.notify.debug('generate: DistributedPondBingoManager')
        
    #############################################################
    # Method: delete
    # Purpose: This method overrides the DistributedObject
    #          delete Method, cleans up unnecessary data so
    #          that we can avoid memory leaks.
    # Input: None
    # Output: None
    ############################################################# 
    def delete(self):
        del self.pond.pondBingoMgr
        self.pond.pondBingoMgr = None
        
        del self.pond
        self.pond = None

        # Cleanup the FSM, put it into the 'Off' State.
        FSM.FSM.cleanup(self)

        # Destroy the instance of the card.
        self.card.destroy()
        del self.card

        self.notify.debug('delete: Deleting Local PondManager %s'%(self.doId))
        DistributedObject.DistributedObject.delete(self)
    
#################################################################
# Distributed Method Definitions
#################################################################
    # Method: d_cardUpdate
    # Purpose: This method sends a message to the AI requesting
    #          that it check whether a legal Cell within the
    #          card has been checked.
    # Input: cellId - Cell ID Number to be checked by the AI.
    #        genus - Fish Genus to be checked by the AI.
    #        species - Fish Species to be checked by the AI.
    # Output: Returns the slot index or None
    ############################################################
    def d_cardUpdate(self, cellId, genus, species):
        self.sendUpdate("cardUpdate", [self.cardId, cellId, genus, species])

    ############################################################
    # Method: d_bingoCall
    # Purpose: This method sends a message to the AI requesting
    #          that it verifies a bingo victory and inform the
    #          other clients playing the game if it is.
    # Input: None
    # Output: None
    ############################################################
    def d_bingoCall(self):
        self.sendUpdate("handleBingoCall", [self.cardId])

#################################################################
# Gameplay Method Definitions
#################################################################
    # Method: setCardState
    # Purpose: This method receives the initial card and game
    #          state from the AI, and calls the appropriate
    #          methods to generate the actual card to match
    #          the one found on the AI. This data arrives after
    #          each new card is generated on the AI or when
    #          a client first enters a FishingSpot.
    # Input: cardId - The current Card ID Number
    #        typeId - The type of Card or Game to be played.
    #        tileSeed - Seed necessary to generate the exact
    #                   same card found on the AI by the RNG.
    #        gameState - Current Game State of the Card. This
    #                    is represented by a bitstring.
    # Output: None
    ############################################################
    def setCardState(self, cardId, typeId, tileSeed, gameState):
        self.cardId = cardId
        self.typeId = typeId
        self.tileSeed = tileSeed
        self.jackpot = BingoGlobals.getJackpot(typeId)
        self.initGameState = gameState

    #############################################################
    # Method: checkForUpdate
    # Purpose: This method is a callback function which is
    #          called each time a Cell GUI button is pressed.
    #          It determines the appropriate game logic.
    # Input: cellId - The Cell ID Number to check for an
    #                 update and victory.
    # Output: None
    ############################################################
    def checkForUpdate(self, cellId):
        # Make Certain that we have a catch, otherwise
        # we don't check the card for a cell update and
        # a possible victory.
        if self.lastCatch is not None:
            genus = self.lastCatch[0]
            species = self.lastCatch[1]
            # Send Message to the AI to check for an update
            self.d_cardUpdate(cellId, genus, species)
            success = self.card.cellUpdateCheck(cellId, genus, species)
            if success == BingoGlobals.WIN:
                self.lastCatch = None
                self.enableBingo()
                self.pond.getLocalToonSpot().cleanupFishPanel()
                self.pond.getLocalToonSpot().hideBootPanel()
            elif success == BingoGlobals.UPDATE:
                self.lastCatch = None
                self.pond.getLocalToonSpot().cleanupFishPanel()
                self.pond.getLocalToonSpot().hideBootPanel()
        else:
            self.notify.warning("CheckForWin: Attempt to Play Cell without a valid catch.")

    #############################################################
    # Method: updateGameState
    # Purpose: This method receives the updated card/game state
    #          information from the AI. It sets the new game
    #          state and appropriately updates the card GUI
    #          to reflect that change.
    # Input: gameState - Current Game State of the Card.
    #        cellId - Id of the cell that was updated
    # Output: None
    ############################################################
    def updateGameState(self, gameState, cellId):
        # Game State comes in as a 32 bit-string where
        # each bit represents an occupied or unoccupied
        # cell in the bingo card. For instance, the
        # bit string: 00000000 00000000 00000000 00001111
        # tells us that in row 0, cells 0-3 are occupied
        # by "bingo markers".
        game = self.card.getGame()
        if game is not None:
            game.setGameState(gameState)
            self.card.cellUpdate(cellId)

    #############################################################
    # Method: _generateCard
    # Purpose: This method safely removes an existing card
    #          before it generates a new one based-on the
    #          current card type and tileSeed.
    # Input: None
    # Output: None
    ############################################################
    def __generateCard(self):
        self.notify.debug("__generateCard: %s" % self.typeId)
        # A card has already been generated, but we are
        # moving on to a new card at this point. We must
        # delete the reference to the old card before generating
        # a reference to the new card.
        if self.card.getGame():
            self.card.removeGame()

        # Generate the new game and update the card gui.
        game = self.__cardChoice()
        game.setGameState(self.initGameState)
        self.card.addGame(game)
        self.card.generateCard(self.tileSeed, self.pond.getArea())
        color = BingoGlobals.getColor(self.typeId)
        self.card.setProp('image_color', VBase4(color[0],color[1], color[2],color[3]))
        color = BingoGlobals.getButtonColor(self.typeId)
        self.card.bingo.setProp('image_color', VBase4(color[0],color[1], color[2],color[3]))
        
        if self.hasEntered:
            self.card.loadCard()
            self.card.show()
        else:
            self.card.hide()

    #############################################################
    # Method: showCard
    # Purpose: This method is used to actually show the bingo
    #          card GUI. In order to prevent the BingoCard GUI
    #          from appearing before the Casting GUI of the
    #          fishing spot, this method is called in sequence
    #          of the FishingSpot "Entering' Movie.
    # Input: None
    # Output: None
    ############################################################
    def showCard(self):
        if (self.state != 'Off' or self.state != 'CloseEvent') and self.card.getGame():
            self.card.loadCard()
            self.card.show()
        elif self.state == 'GameOver':
            self.card.show()
        elif self.state == 'Reward':
            self.card.show()
        elif self.state == 'WaitCountdown':
            self.card.show()
            self.card.showNextGameTimer(TTLocalizer.FishBingoNextGame)
        elif self.state == 'Intermission':
            self.card.showNextGameTimer(TTLocalizer.FishBingoIntermission)
            self.card.show()
        self.hasEntered = 1    

    #############################################################
    # Method: __cardChoice
    # Purpose: This method actually generates the appropriate
    #          card based-on the current Card/Game Type.
    # Input: None
    # Output: None
    ############################################################
    def __cardChoice(self):
        return self.cardTypeDict.get(self.typeId)()

    #############################################################
    # Method: checkForBingo
    # Purpose: This method checks the current for bingo in the
    #          current state of the card. It is called whenever
    #          the bingo button has been clicked. Since there
    #          would not be a cell update this method is used
    #          in place of CellUpdateCheck.
    # Input: None
    # Output: None
    ############################################################
    def checkForBingo(self):
        success = self.card.checkForBingo()
        if success:
            self.d_bingoCall()
            self.request('Reward')

    #############################################################
    # Method: enableBingo
    # Purpose: This method enables the Bingo Button. The Bingo
    #          button may or may not be enabled. Of course, we
    #          can always enable the button and merely set the
    #          checkForBingo callback once the ai confirms a
    #          a victory has been detected.
    # Input: None
    # Output: BingoCard of TypeId
    ############################################################
    def enableBingo(self):
        self.card.setBingo(DGG.NORMAL, self.checkForBingo)

#################################################################
# Accessor and Mutator Method Definitions
#################################################################
    # Method: setPondDoId
    # Purpose: This method receives the Pond DoId number so that
    #          the Manager can properly generate bingo cards
    #          based-on the specific fish found within that
    #          particular pond.
    # Note: This is a required method for the Manager.
    # Input: pondId - Pond DoId Number for which this Manager
    #                 is associated.
    # Output: None
    #############################################################
    def setPondDoId(self, pondId):
        self.pond = base.cr.doId2do[pondId]
        self.pond.setPondBingoManager(self)

    #############################################################
    # Method: setState
    # Purpose: This method receives an updated state information
    #          from the AI. For instance, if the AI timer has
    #          expired, it will tell each client in the game
    #          to change to the timeout state since the game
    #          is over.
    # Input: state - The transitional state.
    #        timeStamp - The AI time that a state may require
    #                    as a parameter.
    # Output: None
    ############################################################
    def setState(self, state, timeStamp):
        self.notify.debug("State change: %s -> %s" % (self.state, state))

        self.request(state, timeStamp)

    #############################################################
    # Method: setLastCatch
    # Purpose: This method receives the last fish caught by the
    #          client. This reference is used to determine if
    #          there is a bingo match when a player clicks on
    #          the bingo card. This method sets the last catch
    #          reference, and is called by the FishingSpot.
    # Input: catch - A tuple containing the (genus, species) of
    #                the fish last caught by the client.
    # Output: None
    #############################################################
    def setLastCatch(self, catch):
        #self.lastCatch = FishGlobals.BingoBoot
        self.lastCatch = catch

        # we also tell the card so it can indicate which squares
        # match
        self.card.fishCaught(catch)

    def castingStarted(self):
        if self.card:
            self.card.castingStarted()

    #############################################################
    # Method: setSpot
    # Purpose: This method receives the FishingSpot where the
    #          avatar or localToon is currently stationed.
    # Input: spot - The fishingspot that houses the localtoon.
    # Output: None
    #############################################################
    def setSpot(self, spot):
        self.spot = spot

    #############################################################
    # Method: setJackpot
    # Purpose: This method receives the jackpot for the next
    #          game. It is called whenever the AI needs to set
    #          the dynamic jackpot for the super bingo game.
    #          Otherwise, the jackpot is set in the setCardState
    #          method for normal games.
    # Input: jackpot - The jackpot of upcoming game.
    # Output: None
    #############################################################
    def setJackpot(self, jackpot):
        self.jackpot = jackpot

#################################################################
# Finite State Machine Methods
#################################################################
#  - FSM States:
#     - Off           Transitions To WaitCountdown
#     - Off           Transitions To Playing
#     - WaitCountdown Transitions To Playing
#     - Playing       Transitions To Reward or GameOver
#     - Reward        Transitions To WaitCountdown or Off
#     - GameOver      Transitions To WaitCountdown or Off
#################################################################

    ################################################################# 
    # Method: enterOff
    # Purpose: This method is called when the AI determines that
    #          the Bingo Night has ended or when a client leaves a
    #          fishing spot.
    # Input: None
    # Output: None
    #################################################################
    def enterOff(self):
        self.notify.debug('enterOff: Enter Off State')

        # Unbind the spot reference        
        del self.spot
        self.spot = None
        
        if self.card.getGame:
            self.card.removeGame()
        self.card.hide()

        self.card.stopNextGameTimer()
           
        self.hasEntered = 0
        self.lastCatch = None
        #del self.initGameState

    ################################################################# 
    # Method: filterOff
    # Purpose: This method is called when a client joins a
    #          FishingSpot. Allows only a transition to the
    #          WaitCountdown or Playing States.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################
    def filterOff(self, request, args):
        if request == 'Intro':
            return 'Intro'
        elif request == 'WaitCountdown':
            return (request, args)
        elif request == 'Playing':
            self.__generateCard()
            self.card.setJackpotText(str(self.jackpot))        
            return (request, args)
        elif request == 'Intermission':
            return (request, args)
        elif request == 'GameOver':
            return (request, args)
        elif request == 'Reward':
            # of a toon joins during the reward phase, just show him Game Over
            return ('GameOver', args)
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - Off to Reward
            #   - Off to GameOver
            self.notify.debug("filterOff: Invalid State Transition from, Off to %s" %(request))

    ################################################################# 
    # Method:  exitOff
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. (Likely will be removed.)
    # Input: None
    # Output: None
    #################################################################
    def exitOff(self):
        self.notify.debug('exitOff: Exit Off State')

    ################################################################# 
    # Method:  enterIntro
    # Purpose: This method is called when the AI tells the client
    #          to enter the Intro phase for the Beginning of Fish
    #          Bingo Night.
    # Input: something we don't need from FSM
    # Output: None
    #################################################################
    def enterIntro(self, args=None):
        self.notify.debug('enterIntro: Enter Intro State')

        # Players will typically receive
        # Tell the fishing spot to update the logos
        # Show the card
        self.pond.setSpotGui()
        self.hasEntered = 1
        #self.card.show()

    ################################################################# 
    # Method: filterIntro
    # Purpose: This method is called when the AI tells the client
    #          to transition into the next game state.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################
    def filterIntro(self, request, args):
        if request == 'WaitCountdown':
            return (request, args)
        else:
            self.notify.debug('filterIntro: Invalid State Transition from Intro to %s' %(request))

    ################################################################# 
    # Method:  exitIntro
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. (Likely will be removed.)
    # Input: None
    # Output: None
    #################################################################
    def exitIntro(self):
      self.notify.debug('exitIntro: Exit Intro State')

    ################################################################# 
    # Method:  enterWaitCountdown
    # Purpose: This method is called when the AI tells the client
    #          to enter the Countdown phase for the next game. This
    #          method generates a card, and sets the timer according
    #          to the timeStamp that the AI provided.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterWaitCountdown(self, timeStamp):
        self.notify.debug('enterWaitCountdown: Enter WaitCountdown State')
        # Generate the new card for the next game.
        #self.__generateCard()
        
        # Start the Countdown for the next game.
        time = BingoGlobals.TIMEOUT_SESSION - globalClockDelta.localElapsedTime(timeStamp[0])
        self.card.startNextGameCountdown(time)

        if self.hasEntered:
            self.card.showNextGameTimer(TTLocalizer.FishBingoNextGame)

    ################################################################# 
    # Method: filterWaitCountdown
    # Purpose: This method is called when the AI determines that
    #          the Countdown phase has ended. It allows only a
    #          transition to the Playing state.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################
    def filterWaitCountdown(self, request, args):
        if request == 'Playing':
            return (request, args)
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - WaitCountdown to Reward
            #   - WaitCountdown to GameOver
            #   - WaitCountdown to Off
            self.notify.debug("filterOff: Invalid State Transition from WaitCountdown to %s" %(request))

    ################################################################# 
    # Method:  exitWaitCountdown
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it resets
    #          the Manager timer.
    # Input: None
    # Output: None
    #################################################################
    def exitWaitCountdown(self):
        self.notify.debug('exitWaitCountdown: Exit WaitCountdown State')
        # Generate the new card for the next game.
        if self.pond:
            self.__generateCard()
            self.card.setJackpotText(str(self.jackpot))
            
            self.card.resetGameTimer()
            self.card.hideNextGameTimer()

    ################################################################# 
    # Method:  enterPlaying
    # Purpose: This method is called when the AI tells the client
    #          to enter the Playing phase. It sets the timer
    #          according to the timeStamp that the AI provided,
    #          and enables buttons on the card.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterPlaying(self, timeStamp):
        self.notify.debug('enterPlaying: Enter Playing State')
        self.lastCatch = None

        session = BingoGlobals.getGameTime(self.typeId)        
        time = session - globalClockDelta.localElapsedTime(timeStamp[0])
        self.card.startGameCountdown(time)

        # Check to determine if there is a card to enable.
        self.card.enableCard(self.checkForUpdate)

    ################################################################# 
    # Method: filterPlaying
    # Purpose: This method is called when the AI determines that
    #          the Playing phase has ended. It allows only a
    #          transition to the Reward state for a win or the
    #          GameOver State for a loss.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################   
    def filterPlaying(self, request, args):
        if request == 'Reward':
            return (request, args)
        elif request == 'GameOver':
            return (request, args)
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - Playing to WaitCountdown
            #   - Playing to Off
            self.notify.debug("filterOff: Invalid State Transition from Playing to %s" %(request))

    ################################################################# 
    # Method:  exitPlaying
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it resets
    #          the Manager timer.
    # Input: None
    # Output: None
    #################################################################
    def exitPlaying(self):
        self.notify.debug('exitPlaying: Exit Playing State')
        self.card.resetGameTimer()

    ################################################################# 
    # Method:  enterReward
    # Purpose: This method is called when the AI tells the client
    #          to enter the Reward Phase due to a victory. It
    #          disables the card so that players can no longer
    #          click on the buttons which would allow for invalid
    #          gameplay.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterReward(self, timeStamp):
        self.notify.debug('enterReward: Enter Reward State')
        if self.card:
            self.card.setBingo()
            self.card.removeGame()
            self.card.setGameOver(TTLocalizer.FishBingoVictory)
        localToonSpot = self.pond.getLocalToonSpot()
        if localToonSpot:
            localToonSpot.setJarAmount(self.jackpot)
        self.jackpot = 0

    ################################################################# 
    # Method: filterReward
    # Purpose: This method is called when the AI determines that
    #          the Reward phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################   
    def filterReward(self, request, args):
        if request == 'WaitCountdown':
            return (request, args)
        elif request == 'Intermission':
            return (request, args)
        elif request == 'CloseEvent':
            return 'CloseEvent'
        elif request == 'Off':
            return 'Off'
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - Reward to Playing
            #   - Reward to GameOver
            self.notify.debug("filterOff: Invalid State Transition from Reward to %s" %(request))

    ################################################################# 
    # Method:  exitReward
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. (Likely will be removed.)
    # Input: None
    # Output: None
    #################################################################
    def exitReward(self):
        self.notify.debug('exitReward: Exit Reward State')
        self.card.setGameOver('')

    ################################################################# 
    # Method:  enterGameOver
    # Purpose: This method is called when the AI tells the client
    #          to enter the GameOver Phase due to a loss. It
    #          disables the card so that players can no longer
    #          click on the buttons which would allow for invalid
    #          gameplay.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterGameOver(self, timeStamp):
        self.notify.debug('enterGameOver: Enter GameOver State')
        self.card.setBingo()
        self.card.removeGame()
        self.card.setGameOver(TTLocalizer.FishBingoGameOver)

    ################################################################# 
    # Method: filterGameOver
    # Purpose: This method is called when the AI determines that
    #          the GameOver phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    ################################################################# 
    def filterGameOver(self, request, args):
        if request == 'WaitCountdown':
            return (request, args)
        elif request == 'Intermission':
            return (request, args)
        elif request == 'CloseEvent':
            return 'CloseEvent'
        elif request == 'Off':
            return 'Off'
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - GameOver to Playing
            #   - Playing to Reward
            self.notify.debug("filterOff: Invalid State Transition from GameOver to %s" %(request))

    ################################################################# 
    # Method:  exitGameOver
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. (Likely will be removed.)
    # Input: None
    # Output: None
    #################################################################
    def exitGameOver(self):
        self.notify.debug('exitGameOver: Exit GameOver State')
        self.card.setGameOver('')
        self.card.resetGameTypeText()

    ################################################################# 
    # Method:  enterIntermission
    # Purpose: This method is called when the AI tells the client
    #          to enter the GameOver Phase due to a loss. It
    #          disables the card so that players can no longer
    #          click on the buttons which would allow for invalid
    #          gameplay.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterIntermission(self, timeStamp):
        self.notify.debug('enterIntermission: Enter Intermission State')
        if self.hasEntered:
            self.card.showNextGameTimer(TTLocalizer.FishBingoIntermission)
        self.notify.debug('enterIntermission: timestamp %s'%(timeStamp[0]))
        elapsedTime = globalClockDelta.localElapsedTime(timeStamp[0])
        self.notify.debug('enterIntermission: elapsedTime %s'%(elapsedTime))
        waitTime = BingoGlobals.HOUR_BREAK_SESSION - elapsedTime
        self.notify.debug('enterIntermission: waitTime %s'%(waitTime))
        self.card.startNextGameCountdown(waitTime)
             
    ################################################################# 
    # Method: filterGameOver
    # Purpose: This method is called when the AI determines that
    #          the GameOver phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    ################################################################# 
    def filterIntermission(self, request, args):
        if request == 'WaitCountdown':
            return (request, args)
        elif request == 'Off':
            return 'Off'
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - GameOver to Playing
            #   - Playing to Reward
            self.notify.warning("filterOff: Invalid State Transition from GameOver to %s" %(request))

    ################################################################# 
    # Method:  exitGameOver
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. (Likely will be removed.)
    # Input: None
    # Output: None
    #################################################################
    def exitIntermission(self):
        self.notify.debug('enterIntermission: Exit Intermission State')

    ################################################################# 
    # Method:  enterCloseEvent
    # Purpose: This method is called when the AI tells the client
    #          to enter the GameOver Phase due to a loss. It
    #          disables the card so that players can no longer
    #          click on the buttons which would allow for invalid
    #          gameplay.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterCloseEvent(self, timestamp):
        self.notify.debug('enterCloseEvent: Enter CloseEvent State')
        # Perform Show Closing code here! This will only occur
        # when Bingo night comes to a close. Not when a player exits
        # a fishing spot.
        self.card.hide()
        self.pond.resetSpotGui()
             
    ################################################################# 
    # Method: filterCloseEvent
    # Purpose: This method is called when the AI determines that
    #          the GameOver phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    ################################################################# 
    def filterCloseEvent(self, request, args):
        if request == 'Off':
            return 'Off'
        else:
            # Do not allow invalid State Transitions to occur.
            # Invalid State Transitions:
            #   - GameOver to Playing
            #   - Playing to Reward
            self.notify.warning("filterOff: Invalid State Transition from GameOver to %s" %(request))

    ################################################################# 
    # Method:  exitCloseEvent
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. (Likely will be removed.)
    # Input: None
    # Output: None
    #################################################################
    def exitCloseEvent(self):
        self.notify.debug('exitCloseEvent: Exit CloseEvent State')
        

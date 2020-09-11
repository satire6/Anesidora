#################################################################
# File: DistributedPondBingoManagerAI.py
# Purpose: Performs the AI handling of the  Fishing Bingo
#          Gameplay. It generates the necessary card, maintains
#          game state, and handles the arrival and departure of
#          players who have entered a fishing  spot during the
#          alotted Bingo Gameplay.
#################################################################

#################################################################
# Direct Specific Modules
#################################################################
from direct.distributed import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.task import Task

#################################################################
# Toontown Specific Modules
#################################################################
from toontown.fishing import BingoGlobals
from toontown.fishing import FishGlobals
from toontown.fishing import NormalBingo
from toontown.fishing import FourCornerBingo
from toontown.fishing import DiagonalBingo
from toontown.fishing import ThreewayBingo
from toontown.fishing import BlockoutBingo
from direct.showbase import RandomNumGen

#################################################################
# Python Specific Modules
#################################################################
import time

#################################################################
# Global Constants
#################################################################
BG = BingoGlobals

class DistributedPondBingoManagerAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPondBingoManagerAI")
    #notify.setDebug(True)

    # Class Dictionary used as a c-like switch
    TimeoutSwitch = { BG.NORMAL_GAME: 'WaitCountdown',
                      BG.INTERMISSION: 'Intermission',
                      BG.CLOSE_EVENT: 'CloseEvent' }

    # Class Dictionary used as a c-like switch
    cardTypeDict = { BG.NORMAL_CARD: NormalBingo.NormalBingo,
                     BG.FOURCORNER_CARD: FourCornerBingo.FourCornerBingo,
                     BG.DIAGONAL_CARD: DiagonalBingo.DiagonalBingo,
                     BG.THREEWAY_CARD: ThreewayBingo.ThreewayBingo,
                     BG.BLOCKOUT_CARD: BlockoutBingo.BlockoutBingo }

#################################################################
# Construction and Destruction Method Definitions
#################################################################
    # Method: __init__
    # Purpose: This method performs the initial construction
    #          of the AI Manager as well as the FSM and DOAI
    #          objects from which it inherits.
    # Input: air - Reference to the AI Repository
    #        pond - Reference to the Fishing Pond that this
    #               ManagerAI is associated with. Each pond will
    #               have an associated ManagerAI.
    # Output: None
    #############################################################  
    def __init__(self, air, pond):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedPondBingoManagerAI')

        self.cardId = 0
        self.card = None
        self.jackpot = 0
        self.tileSeed = 0
        self.timeStamp = 0

        self.maxPlayers = 0
        self.numMarkedCells = 0

        self.pond = pond
        self.timerTask = None
        self.nextGameSuper = False
        self.finalGame = BG.NORMAL_GAME
        self.typeId = BingoGlobals.NORMAL_CARD
        self.avId2Fish = {}

    #############################################################
    # Method: generate
    # Purpose: This method overrides the DistributedObjectAI
    #          generate Method, possibly performing additional
    #          initialization.
    # Input: None
    # Output: None
    #############################################################              
    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)
        self.notify.debug('generate: DistributedPondBingoManagerAI')

    #############################################################
    # Method: disable
    # Purpose: This method overrides the DistributedObjectAI
    #          disable Method, possibly cleans up any
    #          unnecessary data.
    # Input: None
    # Output: None
    #############################################################   
    def disable(self):
        DistributedObjectAI.DistributedObjectAI.disable(self)

    #############################################################
    # Method: delete
    # Purpose: This method overrides the DistributedObjectAI
    #          delete Method, cleans up unnecessary data so
    #          that we can avoid memory leaks.
    # Input: None
    # Output: None
    ############################################################# 
    def delete(self):
        del self.pond.pondBingoMgr
        self.pond.pondBingoMgr = None
        
        del self.pond
        del self.avId2Fish

        if self.card:
            self.card.destroy()
        del self.card


        self.__stopTimeout()
        if self.air.bingoMgr:
            self.air.bingoMgr.removePondBingoMgrAI(self.getDoId())

        FSM.FSM.cleanup(self)
        self.__stopTimeout()
        DistributedObjectAI.DistributedObjectAI.delete(self)

#################################################################
# Distributed Method Definitions
#################################################################
    # Method: d_sendCardState
    # Purpose: This method sends a distributed call to the
    #          client so that it properly updates the card
    #          information of the current game.
    # Input: avId - the id of the avatar.
    # Output: None
    #############################################################        
    def d_setCardState(self, avId):
        gameState = (self.card and [self.card.gameState] or [4096])[0]   
        self.sendUpdateToAvatarId(avId,
                                  "setCardState",
                                  [ self.cardId,
                                    self.typeId,
                                    self.tileSeed,
                                    gameState ] )

    #############################################################
    # Method: d_setJackpot
    # Purpose: This method sends a distributed call to the
    #          client so that it properly updates the jackpot
    #          information of the current game.
    # Input: avId - the id of the avatar.
    # Output: None
    #############################################################
    def d_setJackpot(self, avId):
        self.sendUpdateToAvatarId(avId, "setJackpot", [self.jackpot])

    #############################################################
    # Method: d_updateGameState
    # Purpose: This method sends a distributed call to the
    #          client so that it properly updates the local
    #          game state of the card to match the ongoing bingo
    #          game.
    # Input: avId - the id of the avatar.
    # Output: None
    #############################################################     
    def d_updateGameState(self, avId, cellId):
        # incase AI comes up right before the hour, and someone
        # enters before card was generated.
        gameState = (self.card and [self.card.gameState] or [4096])[0]        
        self.sendUpdateToAvatarId(avId,
                                  "updateGameState",
                                  [ gameState, cellId ] )
   
    #############################################################
    # Method: d_setState
    # Purpose: This method sends a distributed call to the
    #          client; informing it that a state change must
    #          occur.
    # Input: avId - the id of the avatar.
    # Output: None
    #############################################################
    def d_setState(self, avId, state):
        self.sendUpdateToAvatarId(avId, "setState",
                                  [ state, self.timeStamp ] )

    #############################################################
    # Method: d_enableBingo
    # Purpose: This method sends a distributed call to the
    #          client; informing it that a state change must
    #          occur.
    # Input: avId - the id of the avatar.
    # Output: None
    #############################################################
    def d_enableBingo(self, avId):
        self.sendUpdateToAvatarId(avId, "enableBingo", [])

#################################################################
# Gameplay Method Definitions
#################################################################
    # Method: generateCard
    # Purpose: This method generates a random Card and
    #          determines what type of game will be played.
    # Input: None
    # Output: None
    #############################################################
    def generateCard(self):
        if self.card:
            self.card.destroy()
            del self.card
            
        self.tileSeed = RandomNumGen.randHash(globalClock.getRealTime())

        # Determine whether the next game should be a super game. If
        # we are coming out of an intermission, then it will be a
        # super game. These occur each hour on the hour, and for the
        # last game of the evening.
        if self.nextGameSuper:
            self.notify.info("generateCard: SUPER CARD GENERATION")
            self.typeId = BingoGlobals.BLOCKOUT_CARD
            self.jackpot = self.air.bingoMgr.getSuperJackpot(self.zoneId)

            # If this was an hourly super jackpot, not the final game of the
            # evening, reset so that we don't go into another intermission
            # at the end of this game. Otherwise, we want to transition
            # to the CloseEvent state after the game has ended, either by
            # a win or "loss."
            if self.finalGame == BG.INTERMISSION:
                self.finalGame = BG.NORMAL_GAME
            self.nextGameSuper = False
        else:
            rng = RandomNumGen.RandomNumGen(self.tileSeed)
            self.typeId = rng.randint(BingoGlobals.NORMAL_CARD,
                                      BingoGlobals.THREEWAY_CARD)
            self.jackpot = BingoGlobals.getJackpot(self.typeId)

        self.card = self.__cardChoice()
        self.card.generateCard(self.tileSeed, self.pond.getArea())
        self.cardId += 1

        self.numMarkedCells= 0
        self.maxPlayers = len(self.avId2Fish)

        
    #############################################################    
    # Method: __cardChoice 
    # Purpose: This method generates generates the appropriate
    #          BingoCard based-on the current Card/Game Type.
    # Input: None
    # Output: BingoCard of TypeId
    #############################################################
    def __cardChoice(self):
        return self.cardTypeDict.get(self.typeId)()
      
    #############################################################
    # Method: cardUpdate
    # Purpose: This method receives card and fish information
    #          from a client whenever the client attempts to
    #          place a "bingo marker" on the board. This method
    #          checks to make certain that the client has the
    #          same cardId, and if the game is in the 'Playing'
    #          state before it checks to see if there was a
    #          successful update and victory.
    # Input: cardId - The card id number to check against.
    #        cellId - Id of the card cell to check against.
    #        genus - Genus of the fish to check against.
    #        species - Species of the fish to check against.
    # Output: None
    #############################################################
    def cardUpdate(self, cardId, cellId, genus, species):
      # First, check to make certain we have the proper card.
      if self.cardId == cardId:
          # Check to see if the card has already been marked
          if self.card and self.card.cellCheck(cellId):
              self.notify.debug("cardUpdate: Cell already marked.")
              return
              
          # We have the proper card, check to make sure we have the same fish.
          avId = self.air.getAvatarIdFromSender()
          if self.isUpdateValid(avId, genus, species):
              self.numMarkedCells += 1
              success = self.card.cellUpdateCheck(cellId, genus, species)
              if success == BingoGlobals.WIN:
                  self.avId2Fish[avId] = ( None, None )
                  for id in self.avId2Fish.keys():
                      if id != avId:
                          self.notify.debug('cardUpdate: avId %s enable Bingo' %(id))
                          self.d_updateGameState(id, cellId)
                          self.d_enableBingo(id)
              elif success == BingoGlobals.UPDATE:
                  self.avId2Fish[avId] = ( None, None )
                  for id in self.avId2Fish.keys():
                      if id != avId:
                          self.notify.debug('cardUpdate: avId %s Update only' %(id))
                          self.d_updateGameState(id, cellId)
              else:
                  self.notify.debug("cardUpdate: No Update was Made.")
          else:
              self.notify.warning("cardUpdate: Invalid Play attempt.")
      elif cardId > self.cardId:
          # The cardId of the client should never be greater
          # than the cardId of the AI. Log this as suspicious.
          self.notify.warning("cardUpdate: Client CardId %s is greater than AI CardID %s." % (cardId, self.cardId))
      elif (self.cardId-cardId) > 2:
          # The cardId of the client is far behind that of the AI.
          # This could be a hack attempt. Mark as suspicious.
          self.notify.warning("cardUpdate: Client CardId %s is far behind AI CardId %s." % (cardId, self.cardId))
      else:
          # The cardId is behind the client, but this could be a latency issue. Just ignore
          # the attempt.
          self.notify.debug("cardUpdate: Not Valid card, could be a latency Issue.")

    #############################################################    
    # Method: isUpdateValid
    # Purpose: This method determines whether a player is sending
    #          a valid update option. For instance, are we even
    #          in the proper game state? Does the fish type that
    #          a client is sending match what the AI has for it?
    # Input: id - id of the avatar who sent the check request
    #        genus - genus of the fish
    #        species - species of the fish
    # Output: returns 1 for valid, 0 for invalid
    #############################################################
    def isUpdateValid(self, id, genus, species):
        result = 1
        if self.state != 'Playing':
            self.notify.debug('isUpdateValid: Not in Play State.')
            result = 0

        # Check if the av catch matches the catch sent in. Essentially,
        # validate that the user and the ai have matching fish. Otherwise,
        # it could be a hack attempt. Without this check, a hacker could
        # send a boot every time, virtually guaranteeing a win.
        if self.avId2Fish.has_key(id):
            if self.avId2Fish[id] != (genus, species):
                self.notify.warning('isUpdateValid: Avatar and AI Fish do not match.')
                result = 0
        else:
            result = 0
        return result

    #############################################################    
    # Method: handleBingoCall
    # Purpose: This method calls a quick check after a client
    #          claims it has "won." It does not check against
    #          a cell thus, there is no reason for the
    #          cellUpdateCheck call.
    # Input: cardId - cardId that the client claims to have won 
    # Output: None
    #############################################################
    def handleBingoCall(self, cardId):
        if self.jackpot == 0:
            # someone has already called bingo... ignore this
            self.notify.warning("handleBingoCall: Bingo call attempted twice (no big deal).")
            return
            
        if self.cardId == cardId:
            success = self.card.checkForBingo()
            if success:
                #tell everyone to make this toon say "Bingo!"
                avId = self.air.getAvatarIdFromSender()
                av = self.air.doId2do.get(avId)
                if av:
                    av.b_announceBingo()
                else:
                    self.notify.warning('handleBingoCall: avId %s not found in doId2do' %(id))

                if self.typeId == BingoGlobals.BLOCKOUT_CARD:
                    self.air.bingoMgr.handleSuperBingoWin(self.zoneId)
                self.timeLeft = self.timerTask.wakeTime - globalClock.getFrameTime()
                self.__stopTimeout()
                self.request('Reward')
        elif cardId > self.cardId:
            # The cardId of the client should never be greater
            # than the cardId of the AI. Log this as suspicious.
            self.notify.warning("handleBingoCall: Client CardId %s is greater than AI CardID %s." % (cardId, self.cardId))
        elif (self.cardId-cardId) > 2:
            # The cardId of the client is far behind that of the AI.
            # This could be a hack attempt. Mark as suspicious.
            self.notify.warning("handleBingoCall: Client CardId %s is far behind AI CardId %s." % (cardId, self.cardId))
        else:
            # The cardId is behind the client, but this could be a latency issue. Just ignore
            # the attempt.
            self.notify.debug("handleBingoCall: Not Valid card, could be a latency Issue.")

    #############################################################    
    # Method: handleSuperBingoLoss
    # Purpose: This method handles the case when a super bingo
    #          game has been lost. This is different than a
    #          normal timeout in that ponds are "competing"
    #          against one another in the same hood. Thus, they
    #          the losers must handle a loss gracefully since it
    #          is not a normal "timeout" loss. In other words,
    #          another pond won so we must shut down the game.
    # Input: None 
    # Output: None
    #############################################################
    def handleSuperBingoLoss(self):
        self.__stopTimeout()
        self.request('GameOver')
                
    ############################################################
    # Method: addAvToGame
    # Purpose: This method adds id of the avatar entering a
    #          fishing spot to the list of Bingo Players.
    # Input: avId - the id of the avatar to be added.
    # Output: Returns success or failure
    ############################################################
    def addAvToGame(self, avId):
        # Defensive coding at this point. Make sure that there
        # is a valid slot open within the list.
        self.notify.debug("addAvToGame: Adding avId %s to avId2Fish" % (avId))
        self.avId2Fish[avId] = ( None, None )

        #track this info for logging
        numPlayers = len(self.avId2Fish)
        if numPlayers > self.maxPlayers:
            self.maxPlayers = numPlayers

        # send the card state
        self.d_setCardState(avId)
        if self.typeId == BingoGlobals.BLOCKOUT_CARD:
            self.d_setJackpot(avId)
        self.d_setState(avId, self.state)        
        return 1        
 
    ############################################################
    # Method: removeAvFromGame
    # Purpose: This method removes id of the avatar exiting a
    #          fishing spot to the list of Bingo Players.
    # Input: avId - the id of the avatar to be added.
    # Output: Returns success or failure
    ############################################################
    def removeAvFromGame(self, avId):
        if self.avId2Fish.has_key(avId):
            self.notify.debug("removeAvFromGame: Removing avId %s from avId2Fish" % (avId))
            del self.avId2Fish[avId]
        else:
            self.notify.warning("addAvToGame: AvId not present in game")
            return 0
        return 1

    ############################################################
    # Method: startup
    # Purpose: This method is called by the BingoManagerAI when
    #          Bingo Night begins. It simply requests a
    #          transition to the WaitCountdown state where the
    #          first card will be generated.
    # Input: None
    # Output: None
    ############################################################
    def startup(self, initState='Intro'):
        # This method should begin the transition from the
        # initial 'Off' State to the 'Playing' State.
        self.request(initState)

    ############################################################
    # Method: __startTimeout
    # Purpose: This method generates a task that acts as a
    #          a timer. It calls the specified callback method
    #          after the time period expires. It also records
    #          a timestamp for when the timer began.
    # Input: name - unique name for the task.
    #        callback - callback method to handle the case when
    #                   the timer expires.
    #        time - amount of time before the timer expires.
    # Output: None
    ############################################################
    def __startTimeout(self, name, callback, time, params = None):
        self.__stopTimeout()
        self.timerTask = taskMgr.doMethodLater(time,
                                               callback,
                                               self.taskName(name),
                                               params)

    ############################################################
    # Method: __stopTimeout
    # Purpose: This method stops a previously invoked timer
    #          task before it can be completed. The callback
    #          method is not called when this happens.
    # Input: None
    # Output: None
    ############################################################
    def __stopTimeout(self):
        if self.timerTask is not None:
            taskMgr.remove(self.timerTask.name)
        self.timerTask = None

    ############################################################
    # Method: __handleDefaultTimeout
    # Purpose: This method handles the 
    #          timeout by requesting a transition to the Playing
    #          state.
    # Input: state - receives the next state that should be
    #                requested.
    # Output: None
    ############################################################
    def __handleDefaultTimeout(self, state):
        #check to make sure we haven't been deleted
        if hasattr(self, "zoneId"):
            self.request(state)
        return Task.done

    ############################################################
    # Method: __handleTimeout
    # Purpose: This method handles the actual Reward/Timeout
    #          state timeout by requesting a transition to the
    #          WaitCountdown state.
    # Input: task - a task object that called this method
    # Output: None
    ############################################################
    def __handleGameOverTimeout(self, task):
        nextState = DistributedPondBingoManagerAI.TimeoutSwitch.get(self.finalGame)
        self.request(nextState)
        return Task.done

    ############################################################
    # Method: __handleCloseEventTimeout
    # Purpose: This method tells the AI that its time to start
    #          shutting down.
    # Input: task - a task object that called this method
    # Output: None
    ############################################################
    def __handleCloseEventTimeout(self, task):
        taskMgr.remove(task)
        self.shutdown()
        
#################################################################
# Accessor and Mutator Method Definitions
#################################################################   
    # Method: getPondDoId
    # Purpose: This method returns the DistributedObject Id of
    #          the pond that it is associated to.
    # Input: None
    # Output: PondDoId - DistributedObject Id of the pond
    #############################################################
    def getPondDoId(self):
        return self.pond.getDoId()

    ###########################################################
    # Method: setAvCatch
    # Purpose: This updates the current avatar catch with the
    #          latest fish that was caught on the client
    #          side.
    # Input: avId - avatar to update
    #        catch - latest catch of the avatar
    # Output: None
    ###########################################################
    def setAvCatch(self, avId, catch):
        if self.avId2Fish.has_key(avId):
            self.avId2Fish[avId] = catch

            # For cheating / testing
            # self.avId2Fish[avId] = FishGlobals.BingoBoot

    ###########################################################
    # Method: setFinalGame
    # Purpose: This method sets the final game of the evening.
    # Input: finalGame - sets finalGame value
    # Output: None
    ###########################################################
    def setFinalGame(self, finalGame):
        self.finalGame = finalGame
            
#################################################################
# Finite State Machine Methods
#################################################################
#  - FSM States:
#     - Off           Transitions To WaitCountdown
#     - WaitCountdown Transitions To Playing
#     - Playing       Transitions To Reward or GameOver
#     - Reward        Transitions To WaitCountdown, Intermission,
#                                    CloseEvent, or Off
#     - GameOver      Transitions To WaitCountdown, Intermission,
#                                    CloseEvent, or Off
#     - Intermission  Transitions To WaitCountdown
#     - CloseEvent    Transitions To Off
#################################################################

    ################################################################# 
    # Method: filterOff
    # Purpose: This method is called when the BingoManagerAI starts
    #          the BingoCard Holiday.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################
    def filterOff(self, request, args):
        if request == 'WaitCountdown':
            return "WaitCountdown"
        elif request == 'Intermission':
            return "Intermission"
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitOff
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. It updates the avIdList
    #          so that any clients who already occupied a fishing
    #          spot would be recognized by the ManagerAI during the
    #          game.
    # Input: None
    # Output: None
    #################################################################
    def exitOff(self):
        if hasattr(self, "zoneId"):
            zoneId = self.zoneId
        else:
            zoneId = None
        self.notify.debug("exitOff: Exit Off State in zone %s" % (zoneId))

    ################################################################# 
    # Method:  enterIntro
    # Purpose: This method is called when the BingoManagerAI starts
    #          Bingo Night and tells the ManagerAI to enter the
    #          Introduction phase. It determines if there are players
    #          currently at a fishing pond. If so, it tells those
    #          players to enter the intro state of bingo night.
    # Input: None
    # Output: None
    #################################################################
    def enterIntro(self):
        self.notify.debug("enterIntro: Enter Intro State in zone %s" % (self.zoneId))

        # Assumption: The BingoManagerAI will behave as a
        # weekly holiday. Thus, it is possible for clients
        # to already be at a fishing spot when this AI object
        # is created. To resolve this, we must update the
        # avIdList before the game begins.

        # This code block could be placed in enterPlaying;
        # however, that seems silly to call this for
        # every game since the spots handle entering and
        # exiting already.
        avIdList = self.pond.avId2SpotDict.keys()
        if avIdList:
            self.notify.debug('enterIntro: Avatars %s found at Fishing Pond in zone %s' %(avIdList, self.zoneId))
            for id in avIdList:
                self.avId2Fish[id] = (None, None)
                self.d_setState(id, 'Intro')
        else:
            self.notify.debug('enterIntro: No Avatars found at Fishing Pond in zone %s' %(self.zoneId))

        self.__startTimeout(self.uniqueName('IntroTimer-%s'%(self.doId)),
                            self.__handleDefaultTimeout,
                            BingoGlobals.INTRO_SESSION,
                            ['WaitCountdown'])

    ################################################################# 
    # Method: filterIntro
    # Purpose: This method is called when the ManagerAI timer expires
    #          indicating the Intro phase has ended. It allows 
    #          only a transition to the WaitCountdown state.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################
    def filterIntro(self, request, args):
        if request == 'WaitCountdown':
            return 'WaitCountdown'
        else:
            self.notify.debug('filterIntro: Invalid State Transition from Intro Phase to %s' %(request))
    
    ################################################################# 
    # Method:  exitIntro
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. It updates the avIdList
    #          so that any clients who already occupied a fishing
    #          spot would be recognized by the ManagerAI during the
    #          game.
    # Input: None
    # Output: None
    #################################################################
    def exitIntro(self):
        self.notify.debug("exitIntro: Exit Intro State in zone %s" % (self.zoneId))

    ################################################################# 
    # Method:  enterWaitCountdown
    # Purpose: This method is called when the BingoManagerAI starts
    #          Bingo Night and tells the ManagerAI to enter the
    #          WaitCountdown phase. It generates a new card and
    #          starts the Countdown timer. In addition, it tells the
    #          ManagerAI to send the necessary cardState to each
    #          client as well as a request for each to enter the
    #          WaitCountdown State as well.
    # Input: None
    # Output: None
    #################################################################
    def enterWaitCountdown(self):
        self.notify.debug("enterWaitCountdown: Enter WaitCountdown State in zone %s" % (self.zoneId))
     
        self.generateCard()
        self.timeStamp = globalClockDelta.getRealNetworkTime()

        self.__startTimeout(self.uniqueName('WaitTimer-%s'%(self.doId)),
                            self.__handleDefaultTimeout,
                            BingoGlobals.TIMEOUT_SESSION,
                            ['Playing'])

        for id in self.avId2Fish.keys():
            self.d_setCardState(id)
            if self.typeId == BingoGlobals.BLOCKOUT_CARD:
                self.d_setJackpot(id)
            self.d_setState(id, 'WaitCountdown')
           
    ################################################################# 
    # Method: filterWaitCountdown
    # Purpose: This method is called when the ManagerAI timer expires
    #          indicating the Countdown phase has ended. It allows 
    #          only a transition to the Playing state.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################
    def filterWaitCountdown(self, request, args):
        if request == 'Playing':
            return 'Playing'
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitWaitCountdown
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it cleans
    #          up the timeStamp so that and older time will not
    #          accidentally be sent to the clients.
    # Input: None
    # Output: None
    #################################################################
    def exitWaitCountdown(self):
        self.notify.debug("exitWaitCountdown: Exit WaitCountdown State in zone %s" % (self.zoneId))
        del self.timeStamp
        self.__stopTimeout()

    ################################################################# 
    # Method:  enterPlaying
    # Purpose: This method is called after the WaitCountdown Timer
    #          expired. It generates the gameplay timer, and tells
    #          the ManagerAI to request for each client to enter the
    #          playing state as well.
    # Input: None
    # Output: None
    #################################################################
    def enterPlaying(self):
        self.notify.debug("enterPlaying: Enter Playing State in zone %s" % (self.zoneId))
        self.timeStamp = globalClockDelta.getRealNetworkTime()
        
        self.__startTimeout(self.uniqueName('GameTimer-%s'%(self.doId)),
                            self.__handleDefaultTimeout, 
                            BingoGlobals.getGameTime(self.typeId),
                            ['GameOver'])
        # Change the client state for each player
        # participating in the game.
        for id in self.avId2Fish.keys():
            # Reset Fish for each player in the game.
            self.avId2Fish[id] = (None, None)
            self.d_setState(id, 'Playing')
            
    ################################################################# 
    # Method: filterPlaying
    # Purpose: This method is called when Gameplay timer has expired
    #          or a victory has been achieved by the clients.
    #          It allows only a transition to the Reward state for
    #          a win or the Timeout State for a loss.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    ################################################################# 
    def filterPlaying(self, request, args):
        if request == 'Reward':
            return 'Reward'
        elif request == 'SuperReward':
            return 'SuperReward'
        elif request == 'GameOver':
            return 'GameOver'
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitPlaying
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it
    #          increments the cardId and cleans up the timeStamp so
    #          that an old time is not accidentally sent to the
    #          clients.
    # Input: None
    # Output: None
    #################################################################
    def exitPlaying(self):
        self.notify.debug("exitPlaying: Exit Playing State in zone %s" %(self.zoneId))
        del self.timeStamp
        self.__stopTimeout()

    ################################################################# 
    # Method:  enterReward
    # Purpose: This method is called when ManagerAI detects a
    #          victory by the clients. It creates a Reward timer
    #          that will transition to the next phase.
    # Input: timeStamp - the time when the AI started the countdown
    #                    period.
    # Output: None
    #################################################################
    def enterReward(self):
        self.notify.debug("enterReward: Enter Reward State in zone %s" %(self.zoneId))
        self.timeStamp = globalClockDelta.getRealNetworkTime()
        avId = self.air.getAvatarIdFromSender()
        winningIds = []
        for id in self.avId2Fish.keys():
            if (id is not None):
                winningIds.append(str(id))
                av = self.air.doId2do.get(id, None)
                if av:
                    av.addMoney(self.jackpot)
                else:
                    self.notify.warning('enterReward: avId %s not found in doId2do' %(id))
                if (id != avId):
                    self.notify.debug('enterReward: avId %s Update and Win' %(id))
                    self.d_setState(id, 'Reward')

        #log a bingo win (pondId, gameType, jackpot, winners)
        self.air.writeServerEvent('fishBingoWin', self.zoneId, '%s|%s|%s|%s' % (self.typeId, self.jackpot, self.timeLeft, "|".join(winningIds)) )
        
        self.jackpot = 0
        self.__startTimeout(self.uniqueName('RewardTimer-%s'%(self.doId)),
                            self.__handleGameOverTimeout,
                            BingoGlobals.REWARD_TIMEOUT)

    ################################################################# 
    # Method: filterReward
    # Purpose: This method is called when the ManagerAI determines 
    #          that the Reward phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################  
    def filterReward(self, request, args):
        if request == 'WaitCountdown':
            return 'WaitCountdown'
        elif request == 'Intermission':
            return 'Intermission'
        elif request == 'CloseEvent':
            return 'CloseEvent'
        elif request == 'Off':
            return 'Off'
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitReward
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it
    #          cleans up the timeStamp so that an old time is not
    #          accidentally sent to the clients.
    # Input: None
    # Output: None
    #################################################################
    def exitReward(self):
        self.notify.debug("exitReward: Exit Reward State in zone %s" %(self.zoneId))
        del self.timeStamp
        self.__stopTimeout()

    ################################################################# 
    # Method:  enterGameOver
    # Purpose: This method is called when the Gameplay Timer expires
    #          thus resulting in a loss. It generates a Timeout
    #          timer, and tells each client to enter the Timeout
    #          state.
    # Input: None
    # Output: None
    #################################################################
    def enterGameOver(self):
        self.notify.debug("enterGameOver: Enter GameOver State in zone %s" %(self.zoneId))
        # Retrieve the timestamp for entering the GameOver
        # state.
        self.timeStamp = globalClockDelta.getRealNetworkTime()
        for id in self.avId2Fish:
            self.d_setState(id, 'GameOver')
            
        #log a bingo loss (pondId, gameType, jackpot, number of marked spots, max players)
        self.air.writeServerEvent('fishBingoLoss', self.zoneId, '%s|%s|%s|%s' % (self.typeId, self.jackpot, self.numMarkedCells, self.maxPlayers) )
        
        self.__startTimeout(self.uniqueName('GameOverTimer-%s'%(self.doId)),
                            self.__handleGameOverTimeout,
                            BG.REWARD_TIMEOUT)

    ################################################################# 
    # Method: filterGameOver
    # Purpose: This method is called when the ManagerAI determines 
    #          that the Timeout phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################  
    def filterGameOver(self, request, args):
        if request == 'WaitCountdown':
            return 'WaitCountdown'
        elif request == 'Intermission':
            return 'Intermission'
        elif request == 'CloseEvent':
            return 'CloseEvent'
        elif request == 'Off':
            return 'Off'
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitCloseEvent
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it
    #          cleans up the timeStamp so that an old time is not
    #          accidentally sent to the clients.
    # Input: None
    # Output: None
    #################################################################
    def exitGameOver(self):
        self.notify.debug("exitGameOver: Exit GameOver State in zone %s" %(self.zoneId))
        del self.timeStamp
        self.__stopTimeout()

    ################################################################# 
    # Method:  enterIntermission
    # Purpose: This method is called when the Gameplay Timer expires
    #          thus resulting in a loss. It generates a Timeout
    #          timer, and tells each client to enter the Timeout
    #          state.
    # Input: None
    # Output: None
    #################################################################
    def enterIntermission(self):
        self.notify.debug("enterIntermission: Enter Intermission State in zone %s" %(self.zoneId))
        self.nextGameSuper = True
        #self.timeStamp = globalClockDelta.getRealNetworkTime()
        self.timeStamp = self.air.bingoMgr.getIntermissionTime()

        for id in self.avId2Fish.keys():
            self.d_setState(id, 'Intermission')

    ################################################################# 
    # Method: filterIntermission
    # Purpose: This method is called when the ManagerAI determines 
    #          that the Timeout phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################  
    def filterIntermission(self, request, args):
        if request == 'WaitCountdown':
            return 'WaitCountdown'
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitIntermission
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it
    #          cleans up the timeStamp so that an old time is not
    #          accidentally sent to the clients.
    # Input: None
    # Output: None
    #################################################################
    def exitIntermission(self):
        self.notify.debug("exitIntermission: Exit Intermission State in zone %s" %(self.zoneId))
        del self.timeStamp
        self.__stopTimeout()

    ################################################################# 
    # Method:  enterCloseEvent
    # Purpose: This method is called when the Gameplay Timer expires
    #          thus resulting in a loss. It generates a Timeout
    #          timer, and tells each client to enter the Timeout
    #          state.
    # Input: None
    # Output: None
    #################################################################
    def enterCloseEvent(self):
        self.notify.debug("enterCloseEvent: Enter CloseEvent State in zone %s" %(self.zoneId))
        self.timeStamp = globalClockDelta.getRealNetworkTime()

        for id in self.avId2Fish.keys():
            self.d_setState(id, 'CloseEvent')

        self.__startTimeout(self.uniqueName('CloseEventTimer-%s'%(self.doId)),
                            self.__handleCloseEventTimeout,
                            BG.CLOSE_EVENT_TIMEOUT)

    ################################################################# 
    # Method: filterCloseEvent
    # Purpose: This method is called when the ManagerAI determines 
    #          that the Timeout phase has ended. It allows only a
    #          transition to the WaitCountdown or Off states.
    # Input: request - The transitional state.
    #        args - additional arguments needed for the transition.
    # Output: None
    #################################################################  
    def filterCloseEvent(self, request, args):
        if request == '0ff':
            return 'Off'
        else:
            return self.defaultFilter(request, args)

    ################################################################# 
    # Method:  exitCloseEvent
    # Purpose: This method is called after a transition to a new
    #          state has been accepted. Before leaving, it
    #          cleans up the timeStamp so that an old time is not
    #          accidentally sent to the clients.
    # Input: None
    # Output: None
    #################################################################
    def exitCloseEvent(self):
        self.notify.debug("exitCloseEvent: Exit CloseEvent State in zone %s" %(self.zoneId))
        del self.timeStamp
        self.__stopTimeout()

    ################################################################# 
    # Method:  shutdown
    # Purpose: This method requests a delete on this distributed ai
    #          object. The final game of the evening has been played
    #          so now it shuts itself down.
    # Input: None
    # Output: None
    #################################################################
    def shutdown(self):
        if not self.isDeleted():
            self.notify.debug("shutdown: Deleting Manager %s of zone %s" % (self.getDoId(), self.zoneId))
            self.requestDelete()

    ################################################################# 
    # Method:  resumeBingoNight
    # Purpose: This method transitions to the waitcountdown state
    #          once an intermission timeout has expired. Typically,
    #          the super bingo game should be played next.
    # Input: None
    # Output: None
    #################################################################
    def resumeBingoNight(self):
        self.__stopTimeout()
        self.request('WaitCountdown')

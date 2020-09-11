"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""

from toontown.minigame.DistributedMinigameAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import TravelGameGlobals
from toontown.toonbase import ToontownGlobals

class DistributedTravelGameAI(DistributedMinigameAI):

    notify = directNotify.newCategory("DistributedTravelGameAI")

    def __init__(self, air, minigameId):
        try:
            self.DistributedTravelGameAI_initialized
        except:
            self.DistributedTravelGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedTravelGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['waitClientsChoices']),
                                    State.State('waitClientsChoices',
                                                self.enterWaitClientsChoices,
                                                self.exitWaitClientsChoices,
                                                ['processChoices','cleanup']),
                                    State.State('processChoices',
                                                self.enterProcessChoices,
                                                self.exitProcessChoices,
                                                ['waitClientsChoices', 'cleanup']),
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

            # for each avatar, keep track of the starting and current votes
            self.currentVotes = {}

            # for each avatar, keep track how many votes, and which direction he wants to go
            self.avatarChoices = {}

            # we always start at node 0
            self.currentSwitch = 0
            self.destSwitch =0

            # log who get the bonus beans
            self.gotBonus = {}
            self.desiredNextGame = -1

            self.boardIndex = random.choice(range(len(TravelGameGlobals.BoardLayouts)))
            
    
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
        DistributedMinigameAI.setGameReady(self)
        self.calcMinigames()
        self.calcBonusBeans()
        # all of the players have checked in
        # they will now be shown the rules

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('waitClientsChoices')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")

        scoreList = []
        curVotesList = []
        bonusesList = []
        for avId in self.avIdList:
            scoreList.append(self.scoreDict[avId])
            curVotesList.append(self.currentVotes[avId])
            bonusesList.append((self.avIdBonuses[avId][0],self.avIdBonuses[avId][1]))
        # Log balancing variables to the event server
        self.air.writeServerEvent('minigame_travel',
                                  self.doId, '%s|%s|%s|%s|%s|%s|%s|%s' % (
            ToontownGlobals.TravelGameId,
            self.getSafezoneId(), self.avIdList, scoreList,
            self.boardIndex, curVotesList, bonusesList,
            self.desiredNextGame)) 
        
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterWaitClientsChoices(self):
        self.notify.debug("enterWaitClientsChoices")
        # Clear out choices for this round
        self.resetChoices()
        # Start the timeout
        taskMgr.doMethodLater(TravelGameGlobals.InputTimeout,
                              self.waitClientsChoicesTimeout,
                              self.taskName("input-timeout"))
        self.sendUpdate("setTimerStartTime",
                        [globalClockDelta.getFrameNetworkTime()])

    def exitWaitClientsChoices(self):
        taskMgr.remove(self.taskName("input-timeout"))

    def enterProcessChoices(self):
        """
        From the avatar choices, figure out which direction to go
        """
        # all this hoopla so we can support a switch going to 3 or more directions
        self.directionVotes = []
        for dir in range(TravelGameGlobals.MaxDirections):
            self.directionVotes.append( [dir,0] )

        for key in self.avatarChoices:
            choice = self.avatarChoices[key]
            numVotes = choice[0]
            direction = choice[1]
            self.directionVotes[direction][1] += numVotes

        #we have the votes totalled up per direction, lets sort it
        def voteCompare( directionVoteA, directionVoteB):
            if directionVoteA[1] < directionVoteB[1]:
                return -1
            elif directionVoteA[1] == directionVoteB[1]:
                return 0
            else:
                return 1
       
        self.directionVotes.sort( voteCompare, reverse=True)

        winningVotes = self.directionVotes[0][1]

        self.winningDirections = []
        #in case of a tie go through each
        self.notify.debug('self.directionVotes = %s' % self.directionVotes)
        for vote in self.directionVotes:
            if vote[1] == winningVotes:
                self.winningDirections.append( vote[0])
                self.notify.debug('add direction %d to winning directions' % vote[0])

        self.directionReason = TravelGameGlobals.ReasonVote
        if len(self.winningDirections) > 1:
            self.notify.debug('multiple winningDirections=%s' % self.winningDirections)
            self.directionReason = TravelGameGlobals.ReasonRandom
            
        #TODO insert tie breaking code here for first place finishers
        self.directionToGo = random.choice(self.winningDirections)

        self.notify.debug('self.directionToGo =%d' % self.directionToGo)

        self.votesArray = []
        self.directionArray = []

        for avId in self.avIdList:
            vote = self.avatarChoices[avId][0]
            direction = self.avatarChoices[avId][1]
            if vote < 0:
                vote = 0
            self.votesArray.append(vote)
            self.directionArray.append(direction)

        #calculate the new switch we're going to
        curSwitch = TravelGameGlobals.BoardLayouts[self.boardIndex][self.currentSwitch]
        self.destSwitch = curSwitch['links'][self.directionToGo]
       
        self.checkForEndGame()

    def exitProcessChoices(self):
        taskMgr.remove(self.taskName("move-timeout"))
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def setExpectedAvatars(self, avIds):
        """
        Override the base behavior, to just make sure we have reasonable starting votes
        """
        DistributedMinigameAI.setExpectedAvatars(self, avIds)

    def createDefaultStartingVotes(self):
        """
        just make sure we have good numbers
        """
        for avId in self.avIdList:
            self.startingVotes[avId] = TravelGameGlobals.DefaultStartingVotes
            self.currentVotes[avId] = TravelGameGlobals.DefaultStartingVotes

    def waitClientsChoicesTimeout(self, task):
        self.notify.debug("waitClientsChoicesTimeout: did not hear from all clients")
        # Anybody who did not choose gets a 0 for their input
        for avId in self.avatarChoices.keys():
            if self.avatarChoices[avId] == (-1,0):
                self.avatarChoices[avId] = (0,0)

        # Go ahead and process choices
        self.gameFSM.request('processChoices')
        return Task.done

    def resetChoices(self):
        # Reset all avatar choices
        for avId in self.avIdList:
            # Initialize toons to -1 so we can tell they have not picked yet
            self.avatarChoices[avId] = (-1,0)


    def setAvatarChoice(self, votes,  direction):
        avatarId = self.air.getAvatarIdFromSender()
        self.notify.debug("setAvatarChoice: avatar: " + str(avatarId)
                          + " votes: " + str(votes) + " direction: " + str(direction))

        # Record this choice in the choices dictionary
        # Check to make sure it is valid first
        self.avatarChoices[avatarId] = self.checkChoice(avatarId, votes,direction)

        #make sure we decrement his current votes
        self.currentVotes[avatarId] -= self.avatarChoices[avatarId][0]

        if self.currentVotes[avatarId] < 0:
            self.notify.warning('currentVotes < 0  avId=%s, currentVotes=%s' %
                                (avatarId, self.currentVotes[avatarId]))

        self.notify.debug('currentVotes = %s' % self.currentVotes)
        self.notify.debug('avatarChoices = %s' % self.avatarChoices)        

        # Tell the clients this avatar chose, but do not tell them
        # what he chose until all avatars have chosen
        self.sendUpdate("setAvatarChose", [avatarId])

        # See if everybody has chosen
        if self.allAvatarsChosen():
            self.notify.debug("setAvatarChoice: all avatars have chosen")
            self.gameFSM.request('processChoices')
        else:
            self.notify.debug("setAvatarChoice: still waiting for more choices")

    def checkChoice(self, avId, votes, direction):
        """
        make sure the avatar's choices are legal
        """
        retDir = direction
        if direction < 0 or direction >= TravelGameGlobals.MaxDirections:
            self.notify.debug('invalid direction %d. Using 0.' % direction)
            retDir =0

        availableVotes = self.currentVotes[avId]
        retVotes = min( votes, availableVotes)
        retVotes = max( votes, 0)

        return (retVotes, retDir)
        
    def allAvatarsChosen(self):
        """
        Returns true if all avatars playing have chosen their votes
        """
        for avId in self.avatarChoices.keys():
            choice = self.avatarChoices[avId]
            if (choice[0] == -1) and not (self.stateDict[avId] == EXITED):
                return False
            
        # If you get here, all avatars must have chosen
        return True

    def isLeaf(self, switchIndex):
        """
        returns True if the given switch is a leaf
        """
        retval = False
        links = TravelGameGlobals.BoardLayouts[self.boardIndex][switchIndex]['links']
        if len(links) == 0:
            retval = True
        return retval

    def giveBonusBeans(self, endingSwitch):
        """
        give the bonus beans if a toon reaches his goal
        """
        noOneGotBonus = True
        for avId in self.avIdBonuses.keys():
            self.scoreDict[avId] = 0
            if self.avIdBonuses[avId][0] == endingSwitch and \
               not self.stateDict[avId] == EXITED:
                noOneGotBonus = False
                self.scoreDict[avId] = self.avIdBonuses[avId][1]
                self.gotBonus[avId] =  self.avIdBonuses[avId][1]

        # if no one reached the secret goal, give everyone 1 bean
        if noOneGotBonus:
            for avId in self.avIdBonuses.keys():
                self.scoreDict[avId] = 1         
        

    def checkForEndGame(self):
        """
        check if the game has ended or not, and figure what state to go to next
        """
        self.notify.debug("checkForEndgame: ")        
        self.currentSwitch = self.destSwitch
        didWeReachMiniGame = self.isLeaf(self.currentSwitch)

        numPlayers = len(self.avIdList)
        if TravelGameGlobals.SpoofFour:
            numPlayers = 4
        delay = TravelGameGlobals.DisplayVotesTimePerPlayer * (numPlayers +1) + \
                TravelGameGlobals.MoveTrolleyTime + TravelGameGlobals.FudgeTime
        
        if didWeReachMiniGame:
            self.desiredNextGame = self.switchToMinigameDict[self.currentSwitch]
            taskMgr.doMethodLater(delay,
                                  self.moveTimeoutTaskGameOver,
                                  self.taskName("move-timeout"))
            self.giveBonusBeans(self.currentSwitch)
        else:
            # Wait for the clients to show all the votes and move the trolley
            taskMgr.doMethodLater(delay,
                                  self.moveTimeoutTask,
                                  self.taskName("move-timeout"))

        # Send the update to the clients of the avatar choices
        self.sendUpdate("setServerChoices", [self.votesArray,
                                             self.directionArray,
                                             self.directionToGo,
                                             self.directionReason,
                                             ])            
            
    def moveTimeoutTask(self, task):
        self.notify.debug("Done waiting for trolley move")
        self.gameFSM.request('waitClientsChoices')
        return Task.done

    def moveTimeoutTaskGameOver(self,task):
        self.notify.debug("Done waiting for trolley move, gmae over")
        # If somebody won let the base class know that the game is over
        self.gameOver()        
        return Task.done

    def calcMinigames(self):
        """
        set up which minigames are assigned to which switch
        """
        numPlayers = len(self.avIdList)
        allowedGames = list(ToontownGlobals.MinigamePlayerMatrix[numPlayers])
        from toontown.minigame import MinigameCreatorAI
        allowedGames = MinigameCreatorAI.removeUnreleasedMinigames(allowedGames)
        #allowedGames = [1,2,13,14,15,16] # uncomment to see the newest icons
        self.switchToMinigameDict = {}
        for switch in TravelGameGlobals.BoardLayouts[self.boardIndex].keys():
            if self.isLeaf(switch):
                if len(allowedGames) == 0:
                    #if we somehow don't have enough allowed games, just
                    #start reusing
                    allowedGames = list(ToontownGlobals.MinigamePlayerMatrix[numPlayers])
                    allowedGames = MinigameCreatorAI.removeUnreleasedMinigames(allowedGames)
                minigame = random.choice(allowedGames)
                self.switchToMinigameDict[switch] = minigame
                allowedGames.remove(minigame)
        
        switches = []
        minigames = []
        for key in self.switchToMinigameDict.keys():
            switches.append( key)
            minigames.append( self.switchToMinigameDict[key])
        
        self.sendUpdate("setMinigames", [switches, minigames])

    def calcBonusBeans(self):
        """
        figure out where the bonus beans go
        """
        possibleLeaves = []
        for switch in TravelGameGlobals.BoardLayouts[self.boardIndex].keys():
            if self.isLeaf(switch):
                possibleLeaves.append(switch)

        self.avIdBonuses = {}
        for avId in self.avIdList:
            switch = random.choice(possibleLeaves)
            possibleLeaves.remove(switch)
            beans = TravelGameGlobals.BoardLayouts[self.boardIndex][switch]['baseBonus']
            baseBeans = TravelGameGlobals.BaseBeans;
            numPlayerMultiplier = len(self.avIdList) / 4.0
            roundMultiplier = (self.metagameRound / 2.0) + 1.0
            beans *= baseBeans * numPlayerMultiplier * roundMultiplier
            self.avIdBonuses[avId] = (switch,beans)

        switches = []
        beans = []

        for avId in self.avIdList:
            switches.append( self.avIdBonuses[avId][0])
            beans.append( self.avIdBonuses[avId][1])

        self.sendUpdate("setBonuses", [switches, beans])


    def setStartingVote(self, avId, startingVote):
        DistributedMinigameAI.setStartingVote(self,avId,startingVote)
        self.currentVotes[avId] = startingVote
        self.notify.debug('setting current  vote of avId=%d to %d' % (avId,startingVote))

    def handleExitedAvatar(self, avId):
        """
        An avatar bailed out because he lost his connection or quit
        unexpectedly.
        We have decided when this happens, we will just kill the
        minigame altogether. But the travel game is special.
        We need to continue until the trolley reaches a destination
        """
        # TODO: what if they have all exited already?
        self.notify.warning("DistrbutedTravelGameAI: handleExitedAvatar: avatar id exited: " +
                            str(avId))
        self.stateDict[avId] = EXITED

        allExited = True
        for avId in self.avIdList:
            if avId in self.stateDict.keys() and self.stateDict[avId]!=EXITED:
                allExited =False
                break
            
        if allExited:
            self.setGameAbort()

    def getBoardIndex(self):
        return self.boardIndex

    def hasScoreMult(self):
        return 0

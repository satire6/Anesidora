
from math import *
from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import random
from direct.task.Task import Task
import RaceGameGlobals

"""
# Trolley manager code:
import DistributedRaceGameAI
# allocate a zone
zoneId = simbase.air.allocateZone()
print zoneId
# Create the minigame
mg = DistributedRaceGameAI.DistributedRaceGameAI(simbase.air)
# Generate it in that zone
mg.generateWithRequired(zoneId)
# set the expected avatars directly
# (I do not think this needs to be an update)
mg.setExpectedAvatars(100000016, 1, 2, 3)
"""

class DistributedRaceGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        try:
            self.DistributedRaceGameAI_initialized
        except:
            self.DistributedRaceGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)
            self.gameFSM = ClassicFSM.ClassicFSM('DistributedRaceGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['waitClientsChoices']),
                                    State.State('waitClientsChoices',
                                                self.enterWaitClientsChoices,
                                                self.exitWaitClientsChoices,
                                                ['processChoices', 'cleanup']),
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

            self.avatarChoices = {}
            self.avatarPositions = {}
            self.chancePositions = {}
            self.rewardDict = {}

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)
        self.resetChancePositions()
        self.resetPositions()

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
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
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def anyAvatarWon(self, positionDict):
        for avId, position in positionDict.items():
            if position >= RaceGameGlobals.NumberToWin:
                # If any single avatar won, return true
                self.notify.debug("anyAvatarWon: Somebody won")
                return 1
        # If we checked all avatars and nobody won, return 0
        self.notify.debug("anyAvatarWon: Nobody won")
        return 0

    def allAvatarsChosen(self):
        # Returns true if all avatars playing have chosen their number
        for choice in self.avatarChoices.values():
            # If the choice is -1, that avId has not chosen yet
            if (choice == -1):
                return 0
        # If you get here, all avatars must have chosen
        return 1

    def checkChoice(self, choice):
        # Handle an invalid choice gracefully by returning the first choice value
        if (choice not in RaceGameGlobals.ValidChoices):
            self.notify.warning("checkChoice: invalid choice: " + str(choice))
            return RaceGameGlobals.ValidChoices[0]
        else:
            return choice

    def resetChoices(self):
        # Reset all avatar choices
        for avId in self.avIdList:
            # Initialize toons to -1 so we can tell they have not picked yet
            self.avatarChoices[avId] = -1

    def resetPositions(self):
        # Reset all avatar positions to 0
        for avId in self.avIdList:
            self.avatarPositions[avId] = 0

    def resetChancePositions(self):
        # reset the chance positions randomly
        chancePositions = []
        for avId in self.avIdList:
            pos = random.randint(5, RaceGameGlobals.NumberToWin - 1)
            self.chancePositions[avId] = pos
            # pick a random reward for this chance card
            self.rewardDict[avId] = random.randint(0, len(RaceGameGlobals.ChanceRewards) - 1)
            # make a simple array to send to client
            chancePositions.append(pos)
        self.sendUpdate("setChancePositions", [chancePositions])

    def setAvatarChoice(self, choice):
        avatarId = self.air.getAvatarIdFromSender()
        self.notify.debug("setAvatarChoice: avatar: " + str(avatarId)
                          + " chose: " + str(choice))

        # Record this choice in the choices dictionary
        # Check to make sure it is valid first
        self.avatarChoices[avatarId] = self.checkChoice(choice)

        # Tell the clients this avatar chose, but do not tell them
        # what he chose until all avatars have chosen
        self.sendUpdate("setAvatarChose", [avatarId])

        # See if everybody has chosen
        if self.allAvatarsChosen():
            self.notify.debug("setAvatarChoice: all avatars have chosen")
            self.gameFSM.request('processChoices')
        else:
            self.notify.debug("setAvatarChoice: still waiting for more choices")

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterWaitClientsChoices(self):
        self.notify.debug("enterWaitClientsChoices")
        # Clear out choices for this round
        self.resetChoices()
        # Start the timeout
        taskMgr.doMethodLater(RaceGameGlobals.InputTimeout,
                              self.waitClientsChoicesTimeout,
                              self.taskName("input-timeout"))
        self.sendUpdate("setTimerStartTime",
                        [globalClockDelta.getFrameNetworkTime()])

    def exitWaitClientsChoices(self):
        taskMgr.remove(self.taskName("input-timeout"))

    def waitClientsChoicesTimeout(self, task):
        self.notify.debug("waitClientsChoicesTimeout: did not hear from all clients")

        # Anybody who did not choose gets a 0 for their input
        for avId in self.avatarChoices.keys():
            if self.avatarChoices[avId] == -1:
                self.avatarChoices[avId] = 0

        # Go ahead and process choices
        self.gameFSM.request('processChoices')
        return Task.done

    def enterProcessChoices(self):
        self.notify.debug("enterProcessChoices: ")
        # Pack up the choice, position, and reward arrays to send to client
        self.choiceArray = []
        self.positionArray = []
        self.rewardArray = []

        # start from the the left most lane and process move
        for avId in self.avIdList:
            choice = self.avatarChoices[avId]
            freq = self.avatarChoices.values().count(choice)
            self.processChoice(avId, choice, freq)
            
        # make this list once and just use copies
        masterList = []
        for avId in self.avIdList:
            masterList.append(-1)
            
        # do this until there are no more rewards this turn
        done = 0
        rewarded = 0
        while not done:
            self.notify.debug("enterProcessChoice: notDone")
            # this will keep track of this turns rewards only
            rewardList = masterList[:]
            for avId in self.avIdList:
                reward = self.processReward(avId)
                # stop processing rewards after finding the first one
                # (we will have to process the results of that first)
                if reward != -1:
                
                    rewarded = 1
                    rewardList[self.avIdList.index(avId)] = reward
                    self.rewardArray += rewardList
            
                    for av in self.avIdList:
                        if (av == avId):
                            # modify the pickers
                            self.processChoice(av,
                                               RaceGameGlobals.ChanceRewards[reward][0][0])
                        else:
                            # modify the others
                            self.processChoice(av,
                                               RaceGameGlobals.ChanceRewards[reward][0][1])

                    # if this player got a reward, we are done
                    break

            if not rewarded:
                self.rewardArray += rewardList
                    
            self.notify.debug("      rewardList: " + str(rewardList))
            self.notify.debug("      rewardArray: " + str(self.rewardArray))
        
            # re-check rewards after moving
            done = rewardList.count(-1) == len(rewardList) 
        self.checkForWinners()
            
    def processChoice(self, avId, choice, freq=1):
        self.notify.debug("processChoice: av = " + str(avId) + " choice = " +
                          str(choice))        
        # only update if the choice is unique
        if (freq == 1):
            # 0 is not a choice!
            if choice != 0:
                # if we have crossed the finish line do nothing
                if self.avatarPositions[avId] < RaceGameGlobals.NumberToWin:
                    # Add this choice to the current position
                    self.avatarPositions[avId] += choice
                    # make sure we don't back off the board
                    if (self.avatarPositions[avId] < 0):
                        self.avatarPositions[avId] = 0

        # Build up the choice array
        self.choiceArray.append(choice)
        # Build up the position array that we will send to the clients
        self.positionArray.append(self.avatarPositions[avId])

        self.notify.debug("Process choice (" + str(choice) + ") for av: " + str(avId))
        self.notify.debug("      choiceArray: " + str(self.choiceArray))
        self.notify.debug("    positionArray: " + str(self.positionArray))

    
    def processReward(self, rewardee):
        self.notify.debug("processReward: " + str(rewardee))
        reward = -1
        # if we moved check to see if we landed on chance marker
        if (self.avatarPositions[rewardee] == self.chancePositions[rewardee]):
            # get the reward for this position
            reward = self.rewardDict[rewardee]
            # add in any extra jellybeans
            bonus = RaceGameGlobals.ChanceRewards[reward][2]
            self.scoreDict[rewardee] = self.scoreDict[rewardee] + bonus
            # make the chance marker go away
            self.chancePositions[rewardee] = -1

        return reward

        
    def checkForWinners(self):
        self.notify.debug("checkForWinners: ")        
        # Send the update to the clients of the avatar choices
        self.sendUpdate("setServerChoices", [self.choiceArray, self.positionArray, self.rewardArray])

        delay = 0.0
        for reward in self.rewardArray:
            # -1 is the nonreward marker
            if reward != -1:
                # It takes at least 7 seconds to process a reward
                # This really should take into account the length of time
                # it takes the avatars to walk for each reward. Its on the todo list
                delay += 7.0

        if self.anyAvatarWon(self.avatarPositions):
            numWinners = 0
            for avId in self.avIdList:
                if (self.avatarPositions[avId] >= RaceGameGlobals.NumberToWin):
                    numWinners = numWinners + 1
            # calculate player's winnings
            for avId in self.avIdList:
                # Losers get number of squares / 2.
                newJellybeans = ceil(self.avatarPositions[avId] * 0.5)

                if (self.avatarPositions[avId] >= RaceGameGlobals.NumberToWin):
                    # lone winners get full reward, ties get a little less to encourage competition
                    newJellybeans = RaceGameGlobals.NumberToWin
                    if (numWinners > 1):
                        newJellybeans = newJellybeans - 3

                self.scoreDict[avId] = self.scoreDict[avId] + newJellybeans
            # Wait for the clients to show all the rewards
            taskMgr.doMethodLater(delay,
                                  self.rewardTimeoutTaskGameOver,
                                  self.taskName("reward-timeout"))
        else:
            # Wait for the clients to show all the rewards
            taskMgr.doMethodLater(delay,
                                  self.rewardTimeoutTask,
                                  self.taskName("reward-timeout"))

        
    def oldEnterProcessChoices(self, recurse = 0):
        self.notify.debug("enterProcessChoices")
        # Pack up the choice, position, and reward arrays
        # choice array must be in correct order
        # iterate through avIdList to get correct order
        if not recurse:
            self.choiceArray = []
            self.positionArray = []
            self.rewardArray = []
        for avId in self.avIdList:
            choice = self.avatarChoices[avId]
            reward = -1
            if choice != 0:
                # See how many people chose this number
                freq = self.avatarChoices.values().count(choice)

                # If this is not a recursive call (ie the result
                # of a chance card) only update if the choice is unique
                if (recurse or (freq == 1)):
                    # Add this choice to the current position
                    self.avatarPositions[avId] += choice
                    # make sure we don't back off the board
                    if (self.avatarPositions[avId] < 0):
                        self.avatarPositions[avId] = 0
                    # if we moved check to see if we landed on chance marker
                    if (self.avatarPositions[avId] == self.chancePositions[avId]):
                        # get the reward for this position
                        reward = self.rewardDict[avId]

                        # add in any extra jellybeans
                        self.scoreDict[avId] = self.scoreDict[avId] + RaceGameGlobals.ChanceRewards[reward][2]
                        # make the chance marker go away
                        self.chancePositions[avId] = -1

            # Build up the choice array
            self.choiceArray.append(choice)
            # Build up the position array that we will send to the clients
            self.positionArray.append(self.avatarPositions[avId])
            # fill in the reward array
            self.rewardArray.append(reward)

        self.notify.debug("      choiceArray: " + str(self.choiceArray))
        self.notify.debug("    positionArray: " + str(self.positionArray))
        self.notify.debug("      rewardArray: " + str( self.rewardArray))

        # recursively process the new positions based on the rewards
        thisTurnRewards = self.rewardArray[-len(self.avatarPositions):]
        rewardIndex = 0
        for reward in thisTurnRewards:
            if reward != -1:
                for avId in self.avIdList:
                    if (self.avIdList.index(avId) == rewardIndex):
                        # modify the pickers
                        self.avatarChoices[avId] = RaceGameGlobals.ChanceRewards[reward][0][0]
                    else:
                        # modify the others
                        self.avatarChoices[avId] = RaceGameGlobals.ChanceRewards[reward][0][1]
                self.enterProcessChoices(1)
            rewardIndex += 1

        # only check end conditions on base case
        if (not recurse):
            # Send the update to the clients of the avatar choices
            self.sendUpdate("setServerChoices", [self.choiceArray, self.positionArray, self.rewardArray])

            delay = 0.0
            for reward in self.rewardArray:
                # -1 is the nonreward marker
                if reward != -1:
                    # It takes at least 7 seconds to process a reward
                    # This really should take into account the length of time
                    # it takes the avatars to walk for each reward. Its on the todo list
                    delay += 7.0

            if self.anyAvatarWon(self.avatarPositions):
                numWinners = 0
                for avId in self.avIdList:
                    if (self.avatarPositions[avId] >= RaceGameGlobals.NumberToWin):
                        numWinners = numWinners + 1
                # calculate player's winnings
                for avId in self.avIdList:
                    # Losers get number of squares / 2.
                    newJellybeans = ceil(self.avatarPositions[avId] * 0.5)

                    if (self.avatarPositions[avId] >= RaceGameGlobals.NumberToWin):
                        # lone winners get full reward, ties get a little less to encourage competition
                        newJellybeans = RaceGameGlobals.NumberToWin
                        if (numWinners > 1):
                            newJellybeans = newJellybeans - 3

                    self.scoreDict[avId] = self.scoreDict[avId] + newJellybeans
                # Wait for the clients to show all the rewards
                taskMgr.doMethodLater(delay,
                                      self.rewardTimeoutTaskGameOver,
                                      self.taskName("reward-timeout"))
            else:
                # Wait for the clients to show all the rewards
                taskMgr.doMethodLater(delay,
                                      self.rewardTimeoutTask,
                                      self.taskName("reward-timeout"))

        return None


    def rewardTimeoutTaskGameOver(self, task):
        self.notify.debug("Done waiting for rewards, game over")
        # If somebody won let the base class know that the game is over
        self.gameOver()
        return Task.done

    def rewardTimeoutTask(self, task):
        self.notify.debug("Done waiting for rewards")
        self.gameFSM.request('waitClientsChoices')
        return Task.done

    def exitProcessChoices(self):
        taskMgr.remove(self.taskName("reward-timeout"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

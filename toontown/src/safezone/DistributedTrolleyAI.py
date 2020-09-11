from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from TrolleyConstants import *

from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import MinigameCreatorAI
from toontown.quest import Quests
from toontown.minigame import  TrolleyHolidayMgrAI
from toontown.minigame import  TrolleyWeekendMgrAI
from toontown.toonbase import ToontownAccessAI

class DistributedTrolleyAI(DistributedObjectAI.DistributedObjectAI):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        "DistributedTrolleyAI")

    def __init__(self, air):
        """__init__(air)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.seats = [None, None, None, None]

        # Flag that tells whether the trolley is currently accepting boarders
        self.accepting = 0

        self.trolleyCountdownTime = \
                          simbase.config.GetFloat("trolley-countdown-time",
                                                  TROLLEY_COUNTDOWN_TIME)
        
        self.fsm = ClassicFSM.ClassicFSM('DistributedTrolleyAI',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['entering']),
                            State.State('entering',
                                        self.enterEntering,
                                        self.exitEntering,
                                        ['waitEmpty']),
                            State.State('waitEmpty',
                                        self.enterWaitEmpty,
                                        self.exitWaitEmpty,
                                        ['waitCountdown']),
                            State.State('waitCountdown',
                                        self.enterWaitCountdown,
                                        self.exitWaitCountdown,
                                        ['waitEmpty', 'allAboard']),
                            State.State('allAboard',
                                        self.enterAllAboard,
                                        self.exitAllAboard,
                                        ['leaving', 'waitEmpty']),
                            State.State('leaving',
                                        self.enterLeaving,
                                        self.exitLeaving,
                                        ['entering'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()

    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        DistributedObjectAI.DistributedObjectAI.delete(self)


    def findAvailableSeat(self):
        for i in range(len(self.seats)):
            if self.seats[i] == None:
                return i
        return None

    def findAvatar(self, avId):
        for i in range(len(self.seats)):
            if self.seats[i] == avId:
                return i
        return None

    def countFullSeats(self):
        avCounter = 0
        for i in self.seats:
            if i:
                avCounter += 1
        return avCounter

    def rejectingBoardersHandler(self, avId):
        self.rejectBoarder(avId)

    def rejectBoarder(self, avId):
        self.sendUpdateToAvatarId(avId, "rejectBoard", [avId])

    def acceptingBoardersHandler(self, avId):
        self.notify.debug("acceptingBoardersHandler")
        seatIndex = self.findAvailableSeat()
        if seatIndex == None:
            self.rejectBoarder(avId)
        else:
            self.acceptBoarder(avId, seatIndex)

    def acceptBoarder(self, avId, seatIndex):
        self.notify.debug("acceptBoarder")
        # Make sure we have a valid seat number
        assert((seatIndex >= 0) and (seatIndex <=3))
        # Make sure the seat is empty
        assert(self.seats[seatIndex] == None)
        # Make sure this avatar isn't already seated
        if (self.findAvatar(avId) != None):
            return
        # Put the avatar in that seat
        self.seats[seatIndex] = avId
        # Add a hook that handles the case where the avatar exits
        # the district unexpectedly
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])
        # Record the time of boarding
        self.timeOfBoarding = globalClock.getRealTime()
        # Tell the clients to put the avatar in that seat
        self.sendUpdate("fillSlot" + str(seatIndex),
                        [avId])
        # Put us into waitCountdown state... If we are already there,
        # this won't do anything.
        self.waitCountdown()

    def __handleUnexpectedExit(self, avId):
        self.notify.warning("Avatar: " + str(avId) +
                            " has exited unexpectedly")
        # Find the exiter's seat index
        seatIndex = self.findAvatar(avId)
        # Make sure the avatar is really here
        if seatIndex == None:
            pass
        else:
            # If the avatar is here, his seat is now empty.
            self.clearFullNow(seatIndex)
            # Tell the clients that the avatar is leaving that seat
            self.clearEmptyNow(seatIndex)
            #self.sendUpdate("emptySlot" + str(seatIndex),
            #                [avId, globalClockDelta.getRealNetworkTime()])
            # If all the seats are empty, go back into waitEmpty state
            if self.countFullSeats() == 0:
                self.waitEmpty()

    def rejectingExitersHandler(self, avId):
        self.rejectExiter(avId)

    def rejectExiter(self, avId):
        # This doesn't have to do anything. If your exit is rejected,
        # you'll know because the trolley leaves.
        pass

    def acceptingExitersHandler(self, avId):
        self.acceptExiter(avId)

    def acceptExiter(self, avId):
        # Find the exiter's seat index
        seatIndex = self.findAvatar(avId)
        # It is possible that the avatar exited the shard unexpectedly.
        if seatIndex == None:
            pass
        else:
            # Empty that seat
            self.clearFullNow(seatIndex)
            # Tell the clients that the avatar is leaving that seat
            self.sendUpdate("emptySlot" + str(seatIndex),
                            [avId, globalClockDelta.getRealNetworkTime()])
            # If all the seats are empty, go back into waitEmpty state
            if self.countFullSeats() == 0:
                self.waitEmpty()
            # Wait for the avatar to be done leaving the seat, and then
            # declare the emptying overwith...
            taskMgr.doMethodLater(TOON_EXIT_TIME,
                                  self.clearEmptyNow,
                                  self.uniqueName("clearEmpty-%s" % seatIndex),
                                  extraArgs = (seatIndex,))

    def clearEmptyNow(self, seatIndex):
        self.sendUpdate("emptySlot" + str(seatIndex),
                        [0, globalClockDelta.getRealNetworkTime()])

    def clearFullNow(self, seatIndex):
        # Get the avatar id
        avId = self.seats[seatIndex]
        # If there is no one sitting there, that is kind of strange.
        if avId == 0:
            self.notify.warning("Clearing an empty seat index: " +
                                str(seatIndex) + " ... Strange...")
        else:
            # Empty that seat
            self.seats[seatIndex] = None
            # Tell the clients that the avatar is no longer in that seat
            self.sendUpdate("fillSlot" + str(seatIndex),
                            [0])
            # If the avatar isn't in a seat, we don't care anymore, so
            # remove the hook to handle unexpected exits.
            self.ignore(simbase.air.getAvatarExitEvent(avId))

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.fsm.getCurrentState().getName()

    def requestBoard(self, *args):
        self.notify.debug("requestBoard")
        avId = self.air.getAvatarIdFromSender()
        if (self.findAvatar(avId) != None):
            self.notify.warning("Ignoring multiple requests from %s to board." % (avId))
            return        

        av = self.air.doId2do.get(avId)
        if av:
            newArgs = (avId,) + args
            
            if not ToontownAccessAI.canAccess(avId, self.zoneId):
                self.notify.warning("Tooon %s does not have access to the trolley." % (avId))
                self.rejectingBoardersHandler(*newArgs)
                return
                
            # Only toons with hp greater than 0 may board the trolley.
            if (av.hp > 0) and self.accepting:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning(
                "avid: %s does not exist, but tried to board a trolley" % avId
                )

    def requestExit(self, *args):
        self.notify.debug("requestExit")
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            newArgs = (avId,) + args
            if self.accepting:
                self.acceptingExitersHandler(*newArgs)
            else:
                self.rejectingExitersHandler(*newArgs)
        else:
            self.notify.warning(
                "avId: %s does not exist, but tried to exit a trolley" % avId
                )

    ##### How you start up the trolley #####
    def start(self):
        self.enter()

    ##### Off state #####

    def enterOff(self):
        self.accepting = 0
        # Maybe this task cleanup shouldn't be here, but I didn't know
        # where else to put it, since emptying the seats isn't associated
        # with any particular task. Perhaps I should have made a nested
        # State machine of TrolleyOn, or some such, but it seemed like a lot
        # of work for a few crummy tasks.

        # If we don't have a doId yet, we can't possibly have these
        # tasks running.
        if hasattr(self, "doId"):
            for seatIndex in range(4):
                taskMgr.remove(self.uniqueName("clearEmpty-" +
                                                         str(seatIndex)))

    def exitOff(self):
        self.accepting = 0

    ##### Entering state #####

    def enter(self):
        self.fsm.request('entering')

    def enterEntering(self):
        self.d_setState('entering')
        self.accepting = 0
        self.seats = [None, None, None, None]
        taskMgr.doMethodLater(TROLLEY_ENTER_TIME, self.waitEmptyTask,
                              self.uniqueName('entering-timer'))

    def exitEntering(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('entering-timer'))

    ##### WaitEmpty state #####

    def waitEmptyTask(self, task):
        self.waitEmpty()
        return Task.done

    def waitEmpty(self):
        if hasattr(self,'fsm') and self.fsm:
            self.fsm.request("waitEmpty")
        else:
            self.notify.warning("waitEmpty no fsm avoided AI crash TOON-1984")

    def enterWaitEmpty(self):
        self.d_setState('waitEmpty')
        self.accepting = 1

    def exitWaitEmpty(self):
        self.accepting = 0

    ##### WaitCountdown state #####

    def waitCountdown(self):
        self.fsm.request("waitCountdown")

    def enterWaitCountdown(self):
        self.d_setState('waitCountdown')
        self.accepting = 1
        # Start the countdown...
        taskMgr.doMethodLater(self.trolleyCountdownTime, self.timeToGoTask,
                              self.uniqueName('countdown-timer'))

    def timeToGoTask(self, task):
        # It is possible that the players exited the district
        if self.countFullSeats() > 0:
            self.allAboard()
        else:
            self.waitEmpty()
        return Task.done

    def exitWaitCountdown(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))

    ##### AllAboard state #####

    def allAboard(self):
        self.fsm.request("allAboard")

    def enterAllAboard(self):
        self.accepting = 0
        currentTime = globalClock.getRealTime()

        elapsedTime = currentTime - self.timeOfBoarding
        self.notify.debug("elapsed time: " + str(elapsedTime))
        waitTime = max(TOON_BOARD_TIME - elapsedTime, 0)
        taskMgr.doMethodLater(waitTime, self.leaveTask,
                              self.uniqueName('waitForAllAboard'))

    def exitAllAboard(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('waitForAllAboard'))

    ##### Leaving state #####

    def leaveTask(self, task):
        # It is possible that the players exited the district
        if self.countFullSeats() > 0:
            self.leave()
        else:
            self.waitEmpty()
        return Task.done

    def leave(self):
        self.fsm.request("leaving")

    def enterLeaving(self):
        self.d_setState('leaving')
        self.accepting = 0
        taskMgr.doMethodLater(TROLLEY_EXIT_TIME, self.trolleyLeftTask,
                              self.uniqueName('leaving-timer'))

    def trolleyLeftTask(self, task):
        self.trolleyLeft()
        return Task.done

    def trolleyLeft(self):
        numPlayers = self.countFullSeats()

        # It is possible the players exited the district
        if (numPlayers > 0):

            # create a list of ids of players that have never ridden the
            # trolley, before we inform the quest manager that they've
            # ridden
            newbieIds = []
            for avId in self.seats:
                if avId:
                    toon = self.air.doId2do.get(avId)
                    if toon:
                        if Quests.avatarHasTrolleyQuest(toon):
                            if not Quests.avatarHasCompletedTrolleyQuest(toon):
                                newbieIds.append(avId)

            """ This was moved to NewbiePurchaseManagerAI. We want to make
            sure that newbies go through the gag tutorial. Therefore we only
            mark their quest as complete when they exit the tutorial purchase
            screen through normal means.

            toonRodeTrolley() was only being used for the single first-time
            trolley quest, so I renamed it to toonRodeTrolleyFirstTime() and
            only call it from the newbie PurchaseMgr.
            
            # Update the quest manager in case any toon had a trolley quest
            for avId in self.seats:
                if avId:
                    toon = self.air.doId2do.get(avId)
                    self.air.questManager.toonRodeTrolley(toon)
            """

            # Make a nice list for the minigame
            playerArray = []
            for i in self.seats:
                if i not in [None, 0]:
                    playerArray.append(i)
            # Create a minigame

            startingVotes = None
            metagameRound = -1
            trolleyGoesToMetagame = simbase.config.GetBool('trolley-goes-to-metagame', 0)
            trolleyHoliday = bboard.get( TrolleyHolidayMgrAI.TrolleyHolidayMgrAI.PostName)
            trolleyWeekend = bboard.get( TrolleyWeekendMgrAI.TrolleyWeekendMgrAI.PostName)
            if trolleyGoesToMetagame or trolleyHoliday or trolleyWeekend:
                metagameRound = 0
                if simbase.config.GetBool('metagame-min-2-players', 1) and \
                   len(playerArray) == 1:
                    # but if there's only 1, bring it back to a regular minigame
                    metagameRound = -1

            mgDict = MinigameCreatorAI.createMinigame(self.air,
                                                      playerArray,
                                                      self.zoneId,
                                                      newbieIds=newbieIds,
                                                      startingVotes = startingVotes,
                                                      metagameRound = metagameRound)
            minigameZone = mgDict["minigameZone"]
            minigameId = mgDict["minigameId"]

            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                # Tell each player on the trolley that they should enter the
                # minigame now.
                if avId:
                    assert(avId > 0)
                    self.sendUpdateToAvatarId(avId, "setMinigameZone",
                                              [minigameZone, minigameId])
                    # Clear the fill slot
                    self.clearFullNow(seatIndex)
        else:
            self.notify.warning("The trolley left, but was empty.")

        # Switch back into entering mode.
        self.enter()

    def exitLeaving(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('leaving-timer'))

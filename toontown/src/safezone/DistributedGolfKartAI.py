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
from toontown.golf import GolfManagerAI
from toontown.golf import GolfGlobals
import random

class DistributedGolfKartAI(DistributedObjectAI.DistributedObjectAI):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        "DistributedGolfKartAI")

    def __init__(self, air, golfCourse, x, y, z, h, p, r):
        """__init__(air)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.seats = [None, None, None, None]
        self.golfCourse = golfCourse # which course does this cart lead to
        self.posHpr = (x, y ,z, h, p, r)
        self.color = ( random.randint(GolfGlobals.KartColors[self.golfCourse][0][0],
                                      GolfGlobals.KartColors[self.golfCourse][0][1]),
                       random.randint(GolfGlobals.KartColors[self.golfCourse][1][0],
                                      GolfGlobals.KartColors[self.golfCourse][1][1]),
                       random.randint(GolfGlobals.KartColors[self.golfCourse][2][0],
                                        GolfGlobals.KartColors[self.golfCourse][2][1]))

        # For the medium course, fix it to be yellow
        if(self.golfCourse == 1):
            if(self.color[0] + self.color[1] <= 255):
                self.color = (self.color[0], self.color[0] + self.color[1], self.color[2])
            else:
                self.color = (self.color[0], 255, self.color[2])

        # Flag that tells whether the trolley is currently accepting boarders
        self.accepting = 0

        self.trolleyCountdownTime = \
                          simbase.config.GetFloat("trolley-countdown-time",
                                                  TROLLEY_COUNTDOWN_TIME)
        
        self.fsm = ClassicFSM.ClassicFSM('DistributedGolfKartAI',
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
            self.ignore(self.air.getAvatarExitEvent(avId))

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
        # State machine of GolfKartOn, or some such, but it seemed like a lot
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
        self.fsm.request("waitEmpty")

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

        avIdList = []
        # It is possible the players exited the district
        if (numPlayers > 0):
             for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                avIdList.append(avId)
                # Clear the fill slot                
                self.clearFullNow(seatIndex)

             golfZone = GolfManagerAI.GolfManagerAI().readyGolfCourse(avIdList,
                                                                 self.golfCourse)
             for avId in avIdList:
                 # Tell each player on the trolley that they should enter the
                 # minigame now.
                 if avId:
                     assert(avId > 0)
                     self.sendUpdateToAvatarId(avId, "setGolfZone", [golfZone, 0])
                #self.sendUpdateToAvatarId(avId, "setMinigameZone",
                #                          [minigameZone, minigameId])
        else:
            self.notify.warning("The trolley left, but was empty.")

        # Switch back into entering mode.
        self.enter()

    def exitLeaving(self):
        self.accepting = 0
        self.color = ( random.randint(GolfGlobals.KartColors[self.golfCourse][0][0],
                                      GolfGlobals.KartColors[self.golfCourse][0][1]),
                       random.randint(GolfGlobals.KartColors[self.golfCourse][1][0],
                                      GolfGlobals.KartColors[self.golfCourse][1][1]),
                       random.randint(GolfGlobals.KartColors[self.golfCourse][2][0],
                                      GolfGlobals.KartColors[self.golfCourse][2][1]))

        # For the medium course, fix it to be yellow
        if(self.golfCourse == 1):
            if(self.color[0] + self.color[1] <= 255):
                self.color = (self.color[0], self.color[0] + self.color[1], self.color[2])
            else:
                self.color = (self.color[0], 255, self.color[2])
                
        self.sendUpdate("setColor",
                        [self.color[0], self.color[1], self.color[2]])
        taskMgr.remove(self.uniqueName('leaving-timer'))

    def getGolfCourse(self):
        return self.golfCourse

    def getPosHpr( self ):
        return self.posHpr

    def getColor(self):
        return self.color

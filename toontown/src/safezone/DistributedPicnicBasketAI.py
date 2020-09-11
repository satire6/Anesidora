from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from TrolleyConstants import *

from toontown.toonbase import ToontownGlobals

from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task 
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import RandomNumGen
from toontown.minigame import MinigameCreatorAI
from toontown.quest import Quests
from toontown.minigame import  TrolleyHolidayMgrAI
from toontown.golf import GolfManagerAI
from toontown.golf import GolfGlobals


class DistributedPicnicBasketAI(DistributedObjectAI.DistributedObjectAI):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        "DistributedPicnicBasketAI")

    def __init__(self, air, tableNumber, x, y, z, h, p, r):
        """__init__(air)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.seats = [None, None, None, None]
        self.posHpr = (x, y ,z, h, p, r)
        self.tableNumber = int(tableNumber)
        self.seed = RandomNumGen.randHash(globalClock.getRealTime())

        # Flag that tells whether the trolley is currently accepting boarders
        self.accepting = 0
        self.numPlayersExiting = 0

        self.trolleyCountdownTime = \
                          simbase.config.GetFloat("picnic-countdown-time",
                                                  ToontownGlobals.PICNIC_COUNTDOWN_TIME)
        
        self.fsm = ClassicFSM.ClassicFSM('DistributedPicnicBasketAI',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['waitEmpty']),
                            State.State('waitEmpty',
                                        self.enterWaitEmpty,
                                        self.exitWaitEmpty,
                                        ['waitCountdown']),
                            State.State('waitCountdown',
                                        self.enterWaitCountdown,
                                        self.exitWaitCountdown,
                                        ['waitEmpty'])],
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

    def rejectingBoardersHandler(self, avId, si):
        self.rejectBoarder(avId)

    def rejectBoarder(self, avId):
        self.sendUpdateToAvatarId(avId, "rejectBoard", [avId])

    def acceptingBoardersHandler(self, avId, si):
        self.notify.debug("acceptingBoardersHandler")
        seatIndex = si
        if not seatIndex == None:
            self.acceptBoarder(avId, seatIndex)

    def acceptBoarder(self, avId, seatIndex):
        self.notify.debug("acceptBoarder %d" % avId)
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
            self.clearEmptyNowUnexpected(seatIndex)
            #self.sendUpdate("emptySlot" + str(seatIndex),
            #                [avId, globalClockDelta.getRealNetworkTime()])
            # If all the seats are empty, go back into waitEmpty state
            if self.countFullSeats() == 0:
                self.waitEmpty()

    def clearEmptyNowUnexpected(self, seatIndex):
        self.sendUpdate("emptySlot" + str(seatIndex),
                        [1, globalClockDelta.getRealNetworkTime()])

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
            #if self.countFullSeats() == 0:
            #    self.waitEmpty()
            
            # Wait for the avatar to be done leaving the seat, and then
            # declare the emptying overwith...
            taskMgr.doMethodLater(TOON_EXIT_TIME,
                                  self.clearEmptyNow,
                                  self.uniqueName("clearEmpty-%s" % seatIndex),
                                  extraArgs = (seatIndex,))

    def clearEmptyNow(self, seatIndex):
        self.notify.debugStateCall(self)
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

    def d_setState(self, state, seed):
        self.sendUpdate('setState', [state, seed, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.fsm.getCurrentState().getName()

    def requestBoard(self,si):
        self.notify.debug("requestBoard")
        avId = self.air.getAvatarIdFromSender()
        if (self.findAvatar(avId) != None):
            self.notify.warning("Ignoring multiple requests from %s to board." % (avId))
            return        

        av = self.air.doId2do.get(avId)
        if av:
            # Only toons with hp greater than 0 may board the trolley.
            if (av.hp > 0) and self.accepting and self.seats[si] == None:
                self.notify.debug("accepting boarder %d" % avId)
                self.acceptingBoardersHandler(avId, si)
            else:
                self.notify.debug("rejecting boarder %d" % avId)
                self.rejectingBoardersHandler(avId, si)
        else: 
            self.notify.warning(
                "avid: %s does not exist, but tried to board a trolley" % avId
                )

    def requestExit(self, *args):
        self.notify.debug("requestExit")
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            # Check to make sure the AI hasn't already told the players to exit
            if (self.countFullSeats() > 0):
                newArgs = (avId,) + args
                self.numPlayersExiting += 1
                if self.accepting:
                    self.acceptingExitersHandler(*newArgs)
                else:
                    self.rejectingExitersHandler(*newArgs)
            else:
                self.notify.debug("Player tried to exit after AI already kicked everyone out")
        else:
            self.notify.warning(
                "avId: %s does not exist, but tried to exit a trolley" % avId
                )

    def doneExit(self):
        # Check to make sure that player has exited before waiting for new toons

        if(self.numPlayersExiting > 0):
            self.numPlayersExiting -= 1
            if (self.numPlayersExiting == 0 and self.countFullSeats() == 0):
                self.waitEmpty()

    ##### How you start up the trolley #####
    def start(self):
        self.waitEmpty()

    ##### Off state #####

    def enterOff(self):
        self.accepting = 0
        # Maybe this task cleanup shouldn't be here, but I didn't know
        # where else to put it, since emptying the seats isn't associated
        # with any particular task. Perhaps I should have made a nested
        # State machine of PicnicBasketOn, or some such, but it seemed like a lot
        # of work for a few crummy tasks.

        # If we don't have a doId yet, we can't possibly have these
        # tasks running.
        if hasattr(self, "doId"):
            for seatIndex in range(4):
                taskMgr.remove(self.uniqueName("clearEmpty-" +
                                                         str(seatIndex)))

    def exitOff(self):
        self.accepting = 0

    ##### WaitEmpty state #####

    def waitEmptyTask(self, task):
        self.waitEmpty()
        return Task.done

    def waitEmpty(self):
        self.fsm.request("waitEmpty")

    def enterWaitEmpty(self):
        self.notify.debugStateCall(self)
        self.d_setState('waitEmpty', self.seed)
        self.seats = [None, None, None, None]
        self.accepting = 1

    def exitWaitEmpty(self):
        self.notify.debugStateCall(self)        
        self.accepting = 0

    ##### WaitCountdown state #####

    def waitCountdown(self):
        self.notify.debugStateCall(self)        
        self.fsm.request("waitCountdown")

    def enterWaitCountdown(self):
        self.notify.debugStateCall(self)                
        self.d_setState('waitCountdown', self.seed)
        self.accepting = 1
        # Start the countdown...
        taskMgr.doMethodLater(self.trolleyCountdownTime, self.timeToGoTask,
                              self.uniqueName('countdown-timer'))

    def timeToGoTask(self, task):
        # It is possible that the players exited the district
        assert self.notify.debugStateCall(self)
        self.accepting = 0
        if self.countFullSeats() > 0:
            for x in range(len(self.seats)):
                if not (self.seats[x] == None):
                    self.sendUpdateToAvatarId(self.seats[x], "setPicnicDone", [])
                    self.acceptExiter(self.seats[x])
                    self.numPlayersExiting += 1
        self.waitEmpty()
        return Task.done

    def exitWaitCountdown(self):
        self.notify.debugStateCall(self)                
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))

    def getPosHpr(self):
        return self.posHpr

    def getTableNumber(self):
        return self.tableNumber
    

from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from ElevatorConstants import *

from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownAccessAI

class DistributedElevatorAI(DistributedObjectAI.DistributedObjectAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorAI")

    def __init__(self, air, bldg, numSeats = 4, antiShuffle = 0, minLaff = 0):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.type = ELEVATOR_NORMAL
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.bldg = bldg
        self.bldgDoId = bldg.getDoId()
        self.seats = []
        self.setAntiShuffle(antiShuffle)
        self.setMinLaff(minLaff)
        if self.antiShuffle:
            if not hasattr(simbase.air, "elevatorTripId"):
                simbase.air.elevatorTripId = 1
            self.elevatorTripId = simbase.air.elevatorTripId
            simbase.air.elevatorTripId += 1
        else:
            self.elevatorTripId = 0
            
        for seat in range(numSeats):
            self.seats.append(None)
        #self.seats = [None, None, None, None]
        # Flag that tells whether the elevator is currently accepting boarders
        self.accepting = 0
        self.fsm = ClassicFSM.ClassicFSM('DistributedElevatorAI',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['opening',
                                         'closed',
                                         ]),
                            State.State('opening',
                                        self.enterOpening,
                                        self.exitOpening,
                                        ['waitEmpty', 'waitCountdown']),
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
                                        ['closing', 'waitEmpty']),
                            State.State('closing',
                                        self.enterClosing,
                                        self.exitClosing,
                                        ['closed', 'waitEmpty']),
                            State.State('closed',
                                        self.enterClosed,
                                        self.exitClosed,
                                        ['opening']),
                            ],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()
        self.boardingParty = None

    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        del self.bldg
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
    def setBoardingParty(self, party):
        self.boardingParty = party

    def generate(self):
        self.start()
        DistributedObjectAI.DistributedObjectAI.generate(self)
        
    def getBldgDoId(self):
        return self.bldgDoId

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
        
    def countOpenSeats(self):
        openSeats = 0
        for i in range(len(self.seats)):
            if self.seats[i] == None:
                openSeats += 1
        return openSeats

    def rejectingBoardersHandler(self, avId, reason = 0, wantBoardingShow = 0):
        self.rejectBoarder(avId, reason)

    def rejectBoarder(self, avId, reason = 0):
        self.sendUpdateToAvatarId(avId, "rejectBoard", [avId, reason])

    def acceptingBoardersHandler(self, avId, reason = 0, wantBoardingShow = 0):
        self.notify.debug("acceptingBoardersHandler")
        seatIndex = self.findAvailableSeat()
        if seatIndex == None:
            self.rejectBoarder(avId, REJECT_NOSEAT)
        else:
            self.acceptBoarder(avId, seatIndex, wantBoardingShow)
        return None

    def acceptBoarder(self, avId, seatIndex, wantBoardingShow = 0):
        self.notify.debug("acceptBoarder")
        # Make sure we have a valid seat number
        #assert((seatIndex >= 0) and (seatIndex <=3))
        assert((seatIndex >= 0) and (seatIndex <=7))
        # Make sure the seat is empty
        assert(self.seats[seatIndex] == None)
        # Make sure this avatar isn't already seated
        if (self.findAvatar(avId) != None):
            return        
        # Put the avatar in that seat
        self.seats[seatIndex] = avId
        # Record the time of boarding
        self.timeOfBoarding = globalClock.getRealTime()
        
        if wantBoardingShow:
            self.timeOfGroupBoarding = globalClock.getRealTime()
        
        # Tell the clients to put the avatar in that seat
        self.sendUpdate("fillSlot" + str(seatIndex), [avId, wantBoardingShow])

    def rejectingExitersHandler(self, avId):
        self.rejectExiter(avId)

    def rejectExiter(self, avId):
        # This doesn't have to do anything. If your exit is rejected,
        # you'll know because the elevator leaves.
        pass

    def acceptingExitersHandler(self, avId):
        self.acceptExiter(avId)

    def clearEmptyNow(self, seatIndex):
        self.sendUpdate("emptySlot" + str(seatIndex),
                        [0, 0, globalClockDelta.getRealNetworkTime(), 0])

    def clearFullNow(self, seatIndex):
        # Get the avatar id
        avId = self.seats[seatIndex]
        # If there is no one sitting there, that is kind of strange.
        if avId == None:
            self.notify.warning("Clearing an empty seat index: " +
                                str(seatIndex) + " ... Strange...")
        else:
            # Empty that seat
            self.seats[seatIndex] = None
            # Tell the clients that the avatar is no longer in that seat
            self.sendUpdate("fillSlot" + str(seatIndex), [0, 0])
            # If the avatar isn't in a seat, we don't care anymore, so
            # remove the hook to handle unexpected exits.
            self.ignore(self.air.getAvatarExitEvent(avId))

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.fsm.getCurrentState().getName()

    def avIsOKToBoard(self, av):
        return (av.hp > self.minLaff) and self.accepting
        
    def checkBoard(self, av):
        if (av.hp < self.minLaff):
            return REJECT_MINLAFF
        return 0

    def requestBoard(self, *args):
        self.notify.debug("requestBoard")
        avId = self.air.getAvatarIdFromSender()
        if (self.findAvatar(avId) != None):
            self.notify.warning("Ignoring multiple requests from %s to board." % (avId))
            return        

        av = self.air.doId2do.get(avId)
        if av:
            # Only toons with hp greater than the minLaff may board the elevator.
            boardResponse = self.checkBoard(av)
            newArgs = (avId,) + args + (boardResponse,)
            
            # Check that player has full access
            if not ToontownAccessAI.canAccess(avId, self.zoneId):
                self.notify.warning("Toon %s does not have access to theeleavtor. " % (avId))
                self.rejectingBoardersHandler(*newArgs)
                return
            
            # Toons who have an active Boarding Group and
            # are not the leader will be rejected if they try to board the elevator.
            if self.boardingParty and self.boardingParty.hasActiveGroup(avId) and \
               (self.boardingParty.getGroupLeader(avId) != avId):
                self.notify.warning('Rejecting %s from boarding the elevator because he is already part of a Boarding Group.' %avId)
                self.rejectingBoardersHandler(*newArgs)
                return
                
            if boardResponse == 0:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning(
                "avid: %s does not exist, but tried to board an elevator"
                % avId
                )
        return
        
    def partyAvatarBoard(self, avatar, wantBoardingShow = 0):
        av = avatar
        avId = avatar.doId
        
        if (self.findAvatar(avId) != None):
            self.notify.warning("Ignoring multiple requests from %s to board." % (avId))
            return
        
        if av: 
            # Only toons with hp greater than the minLaff may board the elevator.
            boardResponse = self.checkBoard(av)
            newArgs = (avId,)  + (boardResponse,) + (wantBoardingShow,)
            if boardResponse == 0:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning("avid: %s does not exist, but tried to board an elevator" % avId)
        return

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
                "avId: %s does not exist, but tried to exit an elevator" % avId
                )
        return

    ##### How you start up the elevator #####
    def start(self):
        self.open()

    ##### Off state #####

    def enterOff(self):
        self.accepting = 0
        self.timeOfBoarding = None
        self.timeOfGroupBoarding = None
        # Maybe this task cleanup shouldn't be here, but I didn't know
        # where else to put it, since emptying the seats isn't associated
        # with any particular task. Perhaps I should have made a nested
        # State machine of TrolleyOn, or some such, but it seemed like a lot
        # of work for a few crummy tasks.
        if hasattr(self, "doId"):
            for seatIndex in range(len(self.seats)):
                taskMgr.remove(self.uniqueName("clearEmpty-" + str(seatIndex)))

    def exitOff(self):
        self.accepting = 0

    ##### Opening state #####

    def open(self):
        self.fsm.request('opening')

    def enterOpening(self):
        self.d_setState('opening')
        self.accepting = 0
        for seat in self.seats:
            seat = None

    def exitOpening(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('opening-timer'))

    ##### WaitCountdown state #####

    def enterWaitCountdown(self):
        self.d_setState('waitCountdown')
        self.accepting = 1

    def exitWaitCountdown(self):
        print("exit wait countdown")
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))
        self.newTrip()

    ##### AllAboard state #####

    def enterAllAboard(self):
        self.accepting = 0

    def exitAllAboard(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('waitForAllAboard'))

    ##### Closing state #####

    def enterClosing(self):
        self.d_setState('closing')
        self.accepting = 0

    def exitClosing(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('closing-timer'))

    ##### Closed state #####

    def enterClosed(self):
        self.d_setState('closed')

    def exitClosed(self):
        return

    ##### WaitEmpty state #####

    def enterWaitEmpty(self):
        self.d_setState('waitEmpty')
        self.accepting = 1
        

    def exitWaitEmpty(self):
        self.accepting = 0
        
    def setElevatorTripId(self, id):
        self.elevatorTripId = id
        
    def getElevatorTripId(self):
        return self.elevatorTripId
        
        
    def newTrip(self):
        if self.antiShuffle:
            self.elevatorTripId = simbase.air.elevatorTripId
            if simbase.air.elevatorTripId > 2100000000:
               simbase.air.elevatorTripId = 1 
            simbase.air.elevatorTripId += 1
            self.sendUpdate("setElevatorTripId", [self.elevatorTripId])

    def setAntiShuffle(self, antiShuffle):
        self.antiShuffle = antiShuffle
        
    def getAntiShuffle(self):
        return self.antiShuffle
        
    def setMinLaff(self, minLaff):
        self.minLaff = minLaff
        
    def getMinLaff(self):
        return self.minLaff

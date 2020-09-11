from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from ElevatorConstants import *

from direct.distributed import DistributedObjectAI
#from direct.fsm import ClassicFSM
#from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM


class DistributedElevatorFSMAI(DistributedObjectAI.DistributedObjectAI, FSM):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorFSMAI")
    #"""    
    defaultTransitions = {
        'Off'             : [ 'Opening', 'Closed'],
        'Opening'         : [ 'WaitEmpty', 'WaitCountdown', 'Opening', 'Closing'  ],
        'WaitEmpty'       : [ 'WaitCountdown', "Closing" ],
        'WaitCountdown'   : [ 'WaitEmpty', 'AllAboard', "Closing" ],
        'AllAboard'       : [ 'WaitEmpty', "Closing" ],
        'Closing'         : [ 'Closed', 'WaitEmpty', 'Closing', 'Opening'  ],
        'Closed'          : [ 'Opening' ],
    }
    #"""
    id = 0
        
    def __init__(self, air, bldg, numSeats = 4, antiShuffle = 0, minLaff = 0):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.__init__( self, "Elevator_%s_FSM" % ( self.id ) )
        self.type = ELEVATOR_NORMAL
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.bldg = bldg
        self.bldgDoId = bldg.getDoId()
        self.seats = []
        for seat in range(numSeats):
            self.seats.append(None)
        #self.seats = [None, None, None, None]
        # Flag that tells whether the elevator is currently accepting boarders
        self.accepting = 0
        #self.setupStates()
        #self.fsm.enterInitialState()
        self.setAntiShuffle(antiShuffle)
        self.setMinLaff(minLaff)
        if self.antiShuffle:
            if not hasattr(simbase.air, "elevatorTripId"):
                simbase.air.elevatorTripId = 1
            self.elevatorTripId = simbase.air.elevatorTripId
            simbase.air.elevatorTripId += 1
        else:
            self.elevatorTripId = 0
            
        

    def delete(self):
        #self.requestFinalState()
        #del self.fsm
        del self.bldg
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def generate(self):
        #print("distributedElevator.generate")
        DistributedObjectAI.DistributedObjectAI.generate(self)
        self.start()
        
    def getBldgDoId(self):
        return self.bldgDoId

    def findAvailableSeat(self):
        for i in range(len(self.seats)):
            if self.seats[i] == None:
                return i
        return None

    def findAvatar(self, avId):
        #print("find Avatar")
        #print self.seats
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

    def rejectingBoardersHandler(self, avId, reason = 0):
        self.rejectBoarder(avId, reason)

    def rejectBoarder(self, avId, reason = 0):
        self.sendUpdateToAvatarId(avId, "rejectBoard", [avId, reason])

    def acceptingBoardersHandler(self, avId, reason = 0):
        self.notify.debug("acceptingBoardersHandler")
        seatIndex = self.findAvailableSeat()
        if seatIndex == None:
            #print("rejectBoarder")
            self.rejectBoarder(avId, REJECT_NOSEAT)
        else:
            #print("acceptBoarder")
            self.acceptBoarder(avId, seatIndex)
        return None

    def acceptBoarder(self, avId, seatIndex):
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
        # Tell the clients to put the avatar in that seat
        self.sendUpdate("fillSlot" + str(seatIndex),
                        [avId])

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
                        [0, 0, globalClockDelta.getRealNetworkTime()])

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
            self.sendUpdate("fillSlot" + str(seatIndex),
                            [0])
            # If the avatar isn't in a seat, we don't care anymore, so
            # remove the hook to handle unexpected exits.
            self.ignore(self.air.getAvatarExitEvent(avId))

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.state

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
            newArgs = (avId,) + args
            # Only toons with hp greater than the minLaff may board the elevator.
            boardResponse = self.checkBoard(av)
            newArgs = (avId,) + args + (boardResponse,)
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

    def requestExit(self, *args):
        if hasattr(self, 'air'):
            #print("REQUEST DGG.EXIT")
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
        #print("DistributedElevatorAI.enterOff")
        self.accepting = 0
        self.timeOfBoarding = None
        # Maybe this task cleanup shouldn't be here, but I didn't know
        # where else to put it, since emptying the seats isn't associated
        # with any particular task. Perhaps I should have made a nested
        # State machine of TrolleyOn, or some such, but it seemed like a lot
        # of work for a few crummy tasks.
        if hasattr(self, "doId"):
            for seatIndex in range(len(self.seats)):
                taskMgr.remove(self.uniqueName("clearEmpty-" + str(seatIndex)))

    def exitOff(self):
        #print("DistributedElevatorAI.exitOff")
        self.accepting = 0

    ##### Opening state #####

    def open(self):
        self.request('Opening')

    def enterOpening(self):
        #print("DistributedElevatorAI.enterOpening")
        self.d_setState('Opening')
        self.accepting = 0
        for seat in self.seats:
            seat = None

    def exitOpening(self):
        #print("DistributedElevatorAI.exitOpening")
        self.accepting = 0
        taskMgr.remove(self.uniqueName('opening-timer'))

    ##### WaitCountdown state #####

    def enterWaitCountdown(self):
        #print("DistributedElevatorAI.enterWaitCountdown")
        self.d_setState('WaitCountdown')
        self.accepting = 1

    def exitWaitCountdown(self):
        #print("DistributedElevatorAI.exitWaitCountdown")
        print("exit wait countdown")
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))
        self.newTrip()

    ##### AllAboard state #####

    def enterAllAboard(self):
        #print("DistributedElevatorAI.enterAllAboard")
        self.accepting = 0

    def exitAllAboard(self):
        #print("DistributedElevatorAI.exitAllAboard")
        self.accepting = 0
        taskMgr.remove(self.uniqueName('waitForAllAboard'))

    ##### Closing state #####

    def enterClosing(self):
        #print("DistributedElevatorAI.enterClosing")
        self.d_setState('Closing')
        self.accepting = 0

    def exitClosing(self):
        #print("DistributedElevatorAI.exitClosing")
        self.accepting = 0
        taskMgr.remove(self.uniqueName('closing-timer'))

    ##### Closed state #####

    def enterClosed(self):
        #print("DistributedElevatorAI.enterClosed")
        if hasattr(self, "doId"):
            print self.doId
        self.d_setState('Closed')

    def exitClosed(self):
        #print("DistributedElevatorAI.exitClosed")
        return

    ##### WaitEmpty state #####

    def enterWaitEmpty(self):
        #print("DistributedElevatorAI.enterWaitEmpty")
        #print("WAIT EMPTY")
        for i in range(len(self.seats)):
            self.seats[i] = None
        print self.seats
        self.d_setState('WaitEmpty')
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

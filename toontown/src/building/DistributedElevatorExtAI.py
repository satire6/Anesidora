from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from ElevatorConstants import *

import DistributedElevatorAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal

class DistributedElevatorExtAI(DistributedElevatorAI.DistributedElevatorAI):
    
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorExtAI")
    
    def __init__(self, air, bldg, numSeats = 4, antiShuffle = 0, minLaff = 0): #antiShufflePOI
        DistributedElevatorAI.DistributedElevatorAI.__init__(
            self, air, bldg, numSeats, antiShuffle = antiShuffle, minLaff = minLaff)
        # Do we need this?
        # self.zoneId, dummy = bldg.getExteriorAndInteriorZoneId()
        # Flag that tells if any Toon has jumped out of the elevator yet
        # (this is used to prevent the griefers who jump off at the last 
        # second)
        self.anyToonsBailed = 0
        self.boardingParty = None

    def delete(self):
        # TODO: We really need an immediate clear here
        # At least it does not crash the AI anymore
        for seatIndex in range(len(self.seats)):
            avId = self.seats[seatIndex]
            if avId:
                self.clearFullNow(seatIndex)
                self.clearEmptyNow(seatIndex)
        DistributedElevatorAI.DistributedElevatorAI.delete(self)
        


    def d_setFloor(self, floorNumber):
        self.sendUpdate('setFloor', [floorNumber])

    def acceptBoarder(self, avId, seatIndex, wantBoardingShow = 0):
        DistributedElevatorAI.DistributedElevatorAI.acceptBoarder(self, avId, seatIndex, wantBoardingShow)
        # Add a hook that handles the case where the avatar exits
        # the district unexpectedly
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])
        # Put us into waitCountdown state... If we are already there,
        # this won't do anything.
        self.fsm.request("waitCountdown")

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
                self.fsm.request('waitEmpty')

    def acceptExiter(self, avId):
        #print("DistributedElevatorExtAI.acceptExiter")
        # Find the exiter's seat index
        seatIndex = self.findAvatar(avId)
        # It is possible that the avatar exited the shard unexpectedly.
        if seatIndex == None:
            pass
        else:
            # Empty that seat
            self.clearFullNow(seatIndex)
            # Make sure there's no griefing by jumping off the elevator
            # at the last second  
            bailFlag = 0
            timeToSend = self.countdownTime
            if self.antiShuffle:
                myTask = taskMgr.getTasksNamed(self.uniqueName('countdown-timer'))[0]
                #print myTask.name
                #print myTask.runningTotal
                #print myTask.dt
                #print myTask.time
                #print myTask.wakeTime - globalClock.getFrameTime() 
                #self.uniqueName('countdown-timer')
                timeLeft = myTask.wakeTime - globalClock.getFrameTime()
                # This fixes an AI crash with a huge negative timeLeft. AI crash on 04/20/10. timeLeft = -44002.155374000002.
                # myTask.wakeTime became zero for some reason.
                timeLeft = max(0, timeLeft)
                timeToSet = timeLeft + 10.0
                timeToSet = min(timeLeft + 10.0, self.countdownTime)
                self.setCountdown(timeToSet)
                timeToSend = timeToSet
                self.sendUpdate("emptySlot" + str(seatIndex),
                [avId, 1, globalClockDelta.getRealNetworkTime(), timeToSend])
            elif (self.anyToonsBailed == 0):
                bailFlag = 1
                # Reset the clock
                self.resetCountdown()
                self.anyToonsBailed = 1
                self.sendUpdate("emptySlot" + str(seatIndex),
                [avId, bailFlag, globalClockDelta.getRealNetworkTime(), timeToSend])
            else:
                self.sendUpdate("emptySlot" + str(seatIndex),
                [avId, bailFlag, globalClockDelta.getRealNetworkTime(), timeToSend])
                
            # Tell the clients that the avatar is leaving that seat

            # If all the seats are empty, go back into waitEmpty state
            if self.countFullSeats() == 0:
                self.fsm.request('waitEmpty')
            # Wait for the avatar to be done leaving the seat, and then
            # declare the emptying overwith...
            taskMgr.doMethodLater(TOON_EXIT_ELEVATOR_TIME,
                                  self.clearEmptyNow,
                                  self.uniqueName("clearEmpty-%s" % seatIndex),
                                  extraArgs = (seatIndex,))


    def enterOpening(self):
        DistributedElevatorAI.DistributedElevatorAI.enterOpening(self)
        taskMgr.doMethodLater(ElevatorData[ELEVATOR_NORMAL]['openTime'],
                              self.waitEmptyTask,
                              self.uniqueName('opening-timer'))


    ##### WaitEmpty state #####

    def waitEmptyTask(self, task):
        self.fsm.request('waitEmpty')
        return Task.done

    def enterWaitEmpty(self):
        DistributedElevatorAI.DistributedElevatorAI.enterWaitEmpty(self)
        self.anyToonsBailed = 0

    ##### WaitCountdown state #####

    def enterWaitCountdown(self):
        DistributedElevatorAI.DistributedElevatorAI.enterWaitCountdown(self)
        # Start the countdown...
        taskMgr.doMethodLater(self.countdownTime, self.timeToGoTask,
                              self.uniqueName('countdown-timer'))

    def timeToGoTask(self, task):
        # It is possible that the players exited the district
        if self.countFullSeats() > 0:
            self.fsm.request("allAboard")
        else:
            self.fsm.request('waitEmpty')
        return Task.done
    
    def resetCountdown(self):
        taskMgr.remove(self.uniqueName('countdown-timer'))
        taskMgr.doMethodLater(self.countdownTime, self.timeToGoTask,
                              self.uniqueName('countdown-timer'))
                              
    def setCountdown(self, timeToSet):
        
        taskMgr.remove(self.uniqueName('countdown-timer'))
        taskMgr.doMethodLater(timeToSet, self.timeToGoTask,
                          self.uniqueName('countdown-timer'))
        
    def enterAllAboard(self):
        DistributedElevatorAI.DistributedElevatorAI.enterAllAboard(self)
        currentTime = globalClock.getRealTime()
        elapsedTime = currentTime - self.timeOfBoarding
        self.notify.debug("elapsed time: " + str(elapsedTime))
        waitTime = max(TOON_BOARD_ELEVATOR_TIME - elapsedTime, 0)

        waitTime += self.getBoardingShowTimeLeft()
        taskMgr.doMethodLater(waitTime, self.closeTask,
                              self.uniqueName('waitForAllAboard'))

    def getBoardingShowTimeLeft(self):
        # This method returns the amount of time left from the last time the
        # group boarding started. Max time is GROUP_BOARDING_TIME.
        # If we get a number that is not between 0 and GROUP_BOARDING_TIME return 0.
        currentTime = globalClock.getRealTime()
        timeLeft = 0.0
                
        if hasattr(self, 'timeOfGroupBoarding') and self.timeOfGroupBoarding:
            elapsedTime = currentTime - self.timeOfGroupBoarding
            timeLeft = max(MAX_GROUP_BOARDING_TIME - elapsedTime, 0)
            # In case the timeLeft is more than the theoretical maximum
            if (timeLeft > MAX_GROUP_BOARDING_TIME):
                timeLeft = 0.0
        
        return timeLeft
    
    ##### Closing state #####    
    def closeTask(self, task):
        # It is possible that the players exited the district
        if self.countFullSeats() > 0:
            self.fsm.request("closing")
        else:
            self.fsm.request('waitEmpty')
        return Task.done

    def enterClosing(self):
        DistributedElevatorAI.DistributedElevatorAI.enterClosing(self)
        taskMgr.doMethodLater(ElevatorData[ELEVATOR_NORMAL]['closeTime'],
                              self.elevatorClosedTask,
                              self.uniqueName('closing-timer'))

    def elevatorClosedTask(self, task):
        self.elevatorClosed()
        return Task.done

    def _createInterior(self):
        self.bldg.createSuitInterior()

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()

        # It is possible the players exited the district
        if (numPlayers > 0):

            # Tell the building to get a suit interior ready for us
            self._createInterior()

            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                # Tell each player on the elevator that they should enter the
                # building now.
                if avId:
                    assert(avId > 0)
                    # Clear the fill slot
                    self.clearFullNow(seatIndex)
        else:
            self.notify.warning("The elevator left, but was empty.")

        # Switch back into opening mode.
        self.fsm.request("closed")
        
            
    def requestExit(self, *args):
        self.notify.debug("requestExit")
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if self.boardingParty and self.boardingParty.getGroupLeader(avId) and avId:
            #exit all in boarding party
            if avId == self.boardingParty.getGroupLeader(avId):
                memberIds = self.boardingParty.getGroupMemberList(avId)
                for memberId in (memberIds):
                    member = simbase.air.doId2do.get(memberId)
                    if member:
                        #print("elevator exit member")
                        if self.accepting:
                            self.acceptingExitersHandler(memberId)
                        else:
                            self.rejectingExitersHandler(memberId)
            else:
                #print("elevator rejecting group member")
                self.rejectingExitersHandler(avId)
        else:
            if av:
                newArgs = (avId,) + args
                if self.accepting:
                    #print("elevator exit leader")
                    self.acceptingExitersHandler(*newArgs)
                else:
                    self.rejectingExitersHandler(*newArgs)
            else:
                self.notify.warning(
                    "avId: %s does not exist, but tried to exit an elevator" % avId
                    )
            return



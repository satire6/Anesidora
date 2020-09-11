from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from toontown.building import ElevatorConstants
from toontown.building import DistributedElevatorFSMAI
#from direct.fsm import ClassicFSM
#from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

class DistributedClubElevatorAI(DistributedElevatorFSMAI.DistributedElevatorFSMAI):
    
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedElevatorFloorAI")
    #"""    
    defaultTransitions = {
        'Off'             : [ 'Opening', 'Closed'],
        'Opening'         : [ 'WaitEmpty', 'WaitCountdown', 'Opening', 'Closing'  ],
        'WaitEmpty'       : [ 'WaitCountdown', "Closing", 'WaitEmpty'],
        'WaitCountdown'   : [ 'WaitEmpty', 'AllAboard', "Closing", 'WaitCountdown'  ],
        'AllAboard'       : [ 'WaitEmpty', "Closing" ],
        'Closing'         : [ 'Closed', 'WaitEmpty', 'Closing', 'Opening'  ],
        'Closed'          : [ 'Opening' ],
    }
    #"""
    id = 0
    DoBlockedRoomCheck = simbase.config.GetBool("elevator-blocked-rooms-check",1)  
    
    def __init__(self, air, lawOfficeId,bldg, avIds, markerId = None, numSeats = 4, antiShuffle = 0, minLaff = 0):
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.__init__(
            self, air, bldg, numSeats, antiShuffle = antiShuffle, minLaff = minLaff)
        FSM.__init__( self, "ElevatorFloor_%s_FSM" % ( self.id ) )    
        # Do we need this?
        # self.zoneId, dummy = bldg.getExteriorAndInteriorZoneId()
        # Flag that tells if any Toon has jumped out of the elevator yet
        # (this is used to prevent the griefers who jump off at the last 
        # second)
        # self.type =  ElevatorConstants.ELEVATOR_STAGE
        self.type = ElevatorConstants.ELEVATOR_COUNTRY_CLUB
        self.countdownTime = ElevatorConstants.ElevatorData[self.type]['countdown']
        self.lawOfficeId = lawOfficeId
        self.anyToonsBailed = 0
        self.avIds = avIds
        self.isEntering = 0
        self.isLocked = 0
        self.setLocked(0)
        self.wantState = None
        self.latchRoom = None
        self.setLatch(markerId)
        self.zoneId = bldg.zoneId
        
    def generate(self):
        #print("DistributedElevatorFloorAI.generate")
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.generate(self)
        
    def generateWithRequired(self, zoneId):
        #print ("DistributedElevatorFloorAI generateWithRequired")
        self.zoneId = zoneId
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.generateWithRequired(self, self.zoneId)


    def delete(self):
        # TODO: We really need an immediate clear here
        # At least it does not crash the AI anymore
        for seatIndex in range(len(self.seats)):
            avId = self.seats[seatIndex]
            if avId:
                self.clearFullNow(seatIndex)
                self.clearEmptyNow(seatIndex)
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.delete(self)
        
    def getEntranceId(self):
        return self.entranceId

    def d_setFloor(self, floorNumber):
        self.sendUpdate('setFloor', [floorNumber])
        
    def avIsOKToBoard(self, av):
        #print("DistributedElevatorFloorAI.avIsOKToBoard %s %s" % (self.accepting, self.isLocked))
        return (av.hp > 0) and self.accepting and not self.isLocked

    def acceptBoarder(self, avId, seatIndex):
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.acceptBoarder(self, avId, seatIndex)
        # Add a hook that handles the case where the avatar exits
        # the district unexpectedly
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])
        # Put us into waitCountdown state... If we are already there,
        # this won't do anything.

        #import pdb; pdb.set_trace()
        if self.state == "WaitEmpty" and (self.countFullSeats() < self.countAvsInZone()):
                self.request("WaitCountdown")
                self.bldg.elevatorAlert(avId)
        elif (self.state in ("WaitCountdown", "WaitEmpty")) and (self.countFullSeats() >= self.countAvsInZone()):
            taskMgr.doMethodLater(ElevatorConstants.TOON_BOARD_ELEVATOR_TIME, self.goAllAboard, self.quickBoardTask)
    
    def countAvsInZone(self):
        matchingZones = 0
        for avId in self.bldg.avIds:
            av = self.air.doId2do.get(avId)
            if av:
                if av.zoneId == self.bldg.zoneId:
                    matchingZones += 1
        return matchingZones
                
                
    def goAllAboard(self, throwAway = 1):
        self.request("Closing")
        return Task.done

    def __handleUnexpectedExit(self, avId):
        #print("DistributedElevatorFloorAI.__handleUnexpectedExit")
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
                self.request('WaitEmpty')
            

    def acceptExiter(self, avId):
        #print("DistributedElevatorFloorAI.acceptExiter")
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
            if (self.anyToonsBailed == 0):
                bailFlag = 1
                # Reset the clock
                self.resetCountdown()
                self.anyToonsBailed = 1
            # Tell the clients that the avatar is leaving that seat
            self.sendUpdate("emptySlot" + str(seatIndex),
                      [avId, bailFlag, globalClockDelta.getRealNetworkTime()])
            # If all the seats are empty, go back into waitEmpty state
            if self.countFullSeats() == 0:
                self.request('WaitEmpty')
            # Wait for the avatar to be done leaving the seat, and then
            # declare the emptying overwith...
            taskMgr.doMethodLater(ElevatorConstants.TOON_EXIT_ELEVATOR_TIME,
                                  self.clearEmptyNow,
                                  self.uniqueName("clearEmpty-%s" % seatIndex),
                                  extraArgs = (seatIndex,))


    def enterOpening(self):
        #print("DistributedElevatorFloorAI.enterOpening %s" % (self.doId))
        self.d_setState('Opening')
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.enterOpening(self)
        taskMgr.doMethodLater(ElevatorConstants.ElevatorData[ElevatorConstants.ELEVATOR_NORMAL]['openTime'],
                              self.waitEmptyTask,
                              self.uniqueName('opening-timer'))
                              
    def exitOpening(self):
        #print("DistributedElevatorFloorAI.exitOpening %s" % (self.doId))
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.exitOpening(self)
        if self.isLocked:
            self.wantState = 'closed'
        if self.wantState == 'closed':
            self.demand('Closing')
            


    ##### WaitEmpty state #####

    def waitEmptyTask(self, task):
        #print("DistributedElevatorFloorAI.waitEmptyTask %s" % (self.doId))
        self.request('WaitEmpty')
        return Task.done

    def enterWaitEmpty(self):
        self.lastState = self.state
        #print("DistributedElevatorFloorAI.enterWaitEmpty  %s %s from %s" % (self.isLocked, self.doId, self.state))
        #print("WAIT EMPTY FLOOR VATOR")
        for i in range(len(self.seats)):
            self.seats[i] = None
        print self.seats
        if self.wantState == 'closed':
            self.demand('Closing')
        else:
            self.d_setState('WaitEmpty')
            self.accepting = 1

            



    ##### WaitCountdown state #####

    def enterWaitCountdown(self):
        self.lastState = self.state
        #print("DistributedElevatorFloorAI.enterWaitCountdown %s from %s" % (self.doId, self.state))
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.enterWaitCountdown(self)
        # Start the countdown...
        taskMgr.doMethodLater(self.countdownTime, self.timeToGoTask,
                              self.uniqueName('countdown-timer'))
        if self.lastState == 'WaitCountdown':
            pass
            #import pdb; pdb.set_trace()

    def timeToGoTask(self, task):
        #print("DistributedElevatorFloorAI.timeToGoTask %s" % (self.doId))
        # It is possible that the players exited the district
        if self.countFullSeats() > 0:
            self.request("AllAboard")
        else:
            self.request('WaitEmpty')
        return Task.done

    def resetCountdown(self):
        taskMgr.remove(self.uniqueName('countdown-timer'))
        taskMgr.doMethodLater(self.countdownTime, self.timeToGoTask,
                              self.uniqueName('countdown-timer'))

    def enterAllAboard(self):
        #print("DISELEFLOORAI enter allAboard")
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.enterAllAboard(self)
        currentTime = globalClock.getRealTime()
        elapsedTime = currentTime - self.timeOfBoarding
        self.notify.debug("elapsed time: " + str(elapsedTime))
        waitTime = max(ElevatorConstants.TOON_BOARD_ELEVATOR_TIME - elapsedTime, 0)
        taskMgr.doMethodLater(waitTime, self.closeTask,
                              self.uniqueName('waitForAllAboard'))

    ##### Closing state #####

    def closeTask(self, task):
        #print("DistributedElevatorFloorAI.closeTask %s" % (self.doId))
        # It is possible that the players exited the district
        if self.countFullSeats() >= 1:#len(self.avIds):
            self.request("Closing")
            #print("closing")
        else:
            self.request('WaitEmpty')
            #print("wait empty")
        return Task.done

    def enterClosing(self):
        #print("DistributedElevatorFloorAI.enterClosing %s" % (self.doId))
        if self.countFullSeats() > 0:
            self.sendUpdate("kickToonsOut")
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.enterClosing(self)
        taskMgr.doMethodLater(ElevatorConstants.ElevatorData[ElevatorConstants.ELEVATOR_STAGE]['closeTime'],
                              self.elevatorClosedTask,
                              self.uniqueName('closing-timer'))
        self.d_setState('Closing')

    def elevatorClosedTask(self, task):
        #print("DistributedElevatorFloorAI.elevatorClosedTask %s" % (self.doId))
        self.elevatorClosed()
        return Task.done

    def elevatorClosed(self):
        if self.isLocked:
            self.request("Closed")
            return
        #print("ELEVATOR CLOSED DOING CALCS")
        numPlayers = self.countFullSeats()
       # print(" NUMBER OF PLAYERS IS %s" % (numPlayers))
        # It is possible the players exited the district
        if (numPlayers > 0):
            
            # Create a factory interior just for us

            # Make a nice list for the factory
            players = []
            for i in self.seats:
                if i not in [None, 0]:
                    players.append(i)
            #lawOfficeZone = self.bldg.createLawOffice(self.lawOfficeId,
            #                                      self.entranceId, players)
            
            sittingAvIds = [];
            
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    # Tell each player on the elevator that they should enter the factory
                    # And which zone it is in
                    #self.sendUpdateToAvatarId(avId, "setLawOfficeInteriorZone", [lawOfficeZone])
                    # Clear the fill slot
                    #self.clearFullNow(seatIndex)
                    sittingAvIds.append(avId)
                    pass
            for avId in self.avIds:
                if not avId in sittingAvIds:
                    #print("THIS AV ID %s IS NOT ON BOARD" % (avId))
                    pass
                    
            
                    
            self.bldg.startNextFloor()                    
            
        else:
            self.notify.warning("The elevator left, but was empty.")
        self.request("Closed")
        
    def setLocked(self, locked):
        self.isLocked = locked
        if locked:
            if self.state == 'WaitEmpty':
                self.request('Closing') 
            if self.countFullSeats() == 0:
                self.wantState = 'closed'
            else:
                self.wantState = 'opening'
        else:
            self.wantState = 'waitEmpty'
            if self.state == 'Closed':
                self.request('Opening') 
                
    def getLocked(self):
        return self.isLocked
        
    def unlock(self):
        #print("DistributedElevatorFloorAI.unlock %s %s" % (self.isLocked, self.doId))
        if self.isLocked:
            self.setLocked(0)
        #self.request('Opening')    
        
    def lock(self):
        #print("DistributedElevatorFloorAI.lock %s %s" % (self.isLocked, self.doId))
        if not self.isLocked:
            self.setLocked(1)
            #if self.state != 'Closed' or self.state != 'Closing':
                #self.request('Closing')  
            #self.beClosed()

        
    def start(self):
        #print("DistributedElevatorFloorAI.start %s" % (self.doId))
        self.quickBoardTask = self.uniqueName("quickBoard")
        self.request('Opening')
        #self.beClosed()
        
    def beClosed(self):
        #print("DistributedElevatorFloorAI.beClosed %s" % (self.doId))
        #self.request('closed')
        pass
        
    def setEntering(self, entering):
        self.isEntering = entering
        
    def getEntering(self):
        return self.isEntering
        
    def enterClosed(self):
        #print("DistributedElevatorFloorAI.enterClosed %s" % (self.doId))
        #import pdb; pdb.set_trace()
        DistributedElevatorFSMAI.DistributedElevatorFSMAI.enterClosed(self)
        ##### WaitEmpty state #####
        # Switch back into opening mode since we allow other Toons onboard
        if self.wantState == 'closed':
            pass
        else:
            self.demand("Opening")
            
            
    def enterOff(self):
        self.lastState = self.state
        #print("DistributedElevatorFloorAI.enterOff")
        if self.wantState == 'closed':
            self.demand('Closing')
        elif self.wantState == 'waitEmpty':
            self.demand('WaitEmpty')
            
    def setPos(self, pointPos):
        self.sendUpdate('setPos', [pointPos[0],pointPos[1],pointPos[2]])
        
    def setH(self, H):
        self.sendUpdate('setH', [H])
        
    def setLatch(self, markerId):
        self.latch = markerId
        #self.sendUpdate('setLatch', [markerId])
        
    def getLatch(self):
        return self.latch

    def checkBoard(self, av):
        if (av.hp < self.minLaff):
            return ElevatorConstants.REJECT_MINLAFF
        if self.DoBlockedRoomCheck and self.bldg:
            if hasattr(self.bldg, "blockedRooms"):
                if self.bldg.blockedRooms:
                    return ElevatorConstants.REJECT_BLOCKED_ROOM        
        return 0

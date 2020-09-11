""" DistributedCogdoInterior module"""

from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *

from toontown.building import ElevatorUtils
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from direct.fsm import State
from toontown.battle import BattleBase
from toontown.hood import ZoneUtil
from toontown.cogdominium.CogdoLayout import CogdoLayout

class DistributedCogdoInterior(DistributedObject.DistributedObject):
    """
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                                                   'DistributedCogdoInterior')

    id = 0

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.toons = []
        self.activeIntervals = {}

        self.openSfx = base.loadSfx("phase_5/audio/sfx/elevator_door_open.mp3")
        self.closeSfx = base.loadSfx("phase_5/audio/sfx/elevator_door_close.mp3")

        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []

        self.distBldgDoId = None

        # we increment this each time we come out of an elevator:
        self.currentFloor = -1

        self.elevatorName = self.__uniqueName('elevator')
        self.floorModel = None

        self.elevatorOutOpen = 0

        # initial cog positions vary based on the cog office model
        self.BottomFloor_SuitPositions = [
                         Point3(0, 15, 0),
                         Point3(10, 20, 0),
                         Point3(-7, 24, 0),
                         Point3(-10, 0, 0)]
        self.BottomFloor_SuitHs = [75, 170, -91, -44]   # Heading angles

        self.Cubicle_SuitPositions = [
                         Point3(0, 18, 0),
                         Point3(10, 12, 0),
                         Point3(-9, 11, 0),
                         Point3(-3, 13, 0)]
        self.Cubicle_SuitHs = [170, 56, -52, 10]

        self.BossOffice_SuitPositions = [
                         Point3(0, 15, 0),
                         Point3(10, 20, 0),
                         Point3(-10, 6, 0),
                         Point3(-17, 34, 11),
                         ]
        self.BossOffice_SuitHs = [170, 120, 12, 38]

        self.waitMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_toon_winning_indoor.mid')
        self.elevatorMusic = base.loadMusic(
            'phase_7/audio/bgm/tt_elevator.mid')

        self.fsm = ClassicFSM.ClassicFSM('DistributedCogdoInterior',
                        [State.State('WaitForAllToonsInside',
                                self.enterWaitForAllToonsInside,
                                self.exitWaitForAllToonsInside,
                                ['Elevator']),
                        State.State('Elevator',
                                self.enterElevator,
                                self.exitElevator,
                                ['Game']),
                        State.State('Game',
                                self.enterGame,
                                self.exitGame,
                                ['Battle']),
                        State.State('Battle',
                                self.enterBattle,
                                self.exitBattle,
                                ['Resting', 
                                'Reward', 
                                'ReservesJoining']),
                        State.State('ReservesJoining',
                                self.enterReservesJoining,
                                self.exitReservesJoining,
                                ['Battle']),
                        State.State('Resting',
                                self.enterResting,      
                                self.exitResting,
                                ['Elevator']),
                        State.State('Reward',
                                self.enterReward,
                                self.exitReward,
                                ['Off']),
                        State.State('Off',
                                self.enterOff,
                                self.exitOff,
                                ['Elevator', 
                                'WaitForAllToonsInside',
                                'Battle']),
                ],
                # Initial State
                'Off',
                # Final State
                'Off',
                )

        # make sure we're in the initial state
        self.fsm.enterInitialState()

    def __uniqueName(self, name):
        DistributedCogdoInterior.id += 1
        return (name + '%d' % DistributedCogdoInterior.id)

    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.notify.debug("generate()"))
        DistributedObject.DistributedObject.generate(self)

        # listen for the generate event, which will be thrown after the
        # required fields are filled in
        self.announceGenerateName = self.uniqueName('generate')
        self.accept(self.announceGenerateName, self.handleAnnounceGenerate)

        # Load the elevator model
        self.elevatorModelIn = loader.loadModel(
                                'phase_5/models/modules/elevator')
        self.leftDoorIn = self.elevatorModelIn.find('**/left-door')
        self.rightDoorIn = self.elevatorModelIn.find('**/right-door')

        self.elevatorModelOut = loader.loadModel(
                                'phase_5/models/modules/elevator')
        self.leftDoorOut = self.elevatorModelOut.find('**/left-door')
        self.rightDoorOut = self.elevatorModelOut.find('**/right-door')

    def setElevatorLights(self, elevatorModel):
        """
        Sets up the lights on the interior elevators to represent the
        number of floors in the building, and to light up the current
        floor number.
        """
        npc=elevatorModel.findAllMatches("**/floor_light_?;+s")
        for i in range(npc.getNumPaths()):
            np=npc.getPath(i)
            # Get the last character, and make it zero based:
            floor=int(np.getName()[-1:])-1

            if (floor == self.currentFloor):
                np.setColor(LIGHT_ON_COLOR)
            elif floor < self.layout.getNumGameFloors():
                if self.isBossFloor(self.currentFloor):
                    np.setColor(LIGHT_ON_COLOR)
                else:
                    np.setColor(LIGHT_OFF_COLOR)
            else:
                np.hide()

    def handleAnnounceGenerate(self, obj):
        """
        handleAnnounceGenerate is called after all of the required fields are
        filled in
        'obj' is another copy of self
        """
        self.ignore(self.announceGenerateName)

        assert(self.notify.debug('joining DistributedCogdoInterior'))
        # Update the minigame AI to join our local toon doId
        self.sendUpdate('setAvatarJoined', [])

    def disable(self):
        assert(self.notify.debug('disable()'))
        self.fsm.requestFinalState()
        self.__cleanupIntervals()
        self.ignoreAll()
        self.__cleanup()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        assert(self.notify.debug('delete()'))
        del self.waitMusic
        del self.elevatorMusic
        del self.openSfx
        del self.closeSfx
        del self.fsm
        # No more battle multiplier
        base.localAvatar.inventory.setBattleCreditMultiplier(1)
        DistributedObject.DistributedObject.delete(self)

    def isBossFloor(self, floorNum):
        if self.layout.hasBossBattle():
            if self.layout.getBossBattleFloor() == floorNum:
                return True
        return False

    def __cleanup(self):
        self.toons = []
        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []
        # Clean up elevator models
        if (self.elevatorModelIn != None):
            self.elevatorModelIn.removeNode()
        if (self.elevatorModelOut != None):
            self.elevatorModelOut.removeNode()
        # Clean up current floor
        if (self.floorModel != None):
            self.floorModel.removeNode()
        self.leftDoorIn = None
        self.rightDoorIn = None
        self.leftDoorOut = None
        self.rightDoorOut = None

    def __addToon(self, toon):
        assert(self.notify.debug('addToon(%d)' % toon.doId))
        self.accept(toon.uniqueName('disable'),
                        self.__handleUnexpectedExit, extraArgs=[toon])

    def __handleUnexpectedExit(self, toon):
        self.notify.warning('handleUnexpectedExit() - toon: %d' % toon.doId)
        self.__removeToon(toon, unexpected=1)

    def __removeToon(self, toon, unexpected=0):
        assert(self.notify.debug('removeToon() - toon: %d' % toon.doId))
        if (self.toons.count(toon) == 1):
            self.toons.remove(toon) 
        self.ignore(toon.uniqueName('disable'))

    def __finishInterval(self, name):
        """ Force the specified interval to jump to the end
        """
        if (self.activeIntervals.has_key(name)):
            interval = self.activeIntervals[name]
            if (interval.isPlaying()):
                assert(self.notify.debug('finishInterval(): %s' % \
                        interval.getName()))
                interval.finish()

    def __cleanupIntervals(self):
        for interval in self.activeIntervals.values():
            interval.finish()
        self.activeIntervals = {}

    def __closeInElevator(self):
        self.leftDoorIn.setPos(3.5, 0, 0)
        self.rightDoorIn.setPos(-3.5, 0, 0)

    ##### Messages from the server #####

    def getZoneId(self):
        return self.zoneId

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def getExtZoneId(self):
        return self.extZoneId

    def setExtZoneId(self, extZoneId):
        self.extZoneId = extZoneId

    def getDistBldgDoId(self):
        return self.distBldgDoId

    def setDistBldgDoId(self, distBldgDoId):
        self.distBldgDoId = distBldgDoId

    def setNumFloors(self, numFloors):
        self.layout = CogdoLayout(numFloors)

    def getToonIds(self):
        toonIds = []
        for toon in self.toons:
            toonIds.append(toon.doId)
        return toonIds

    def setToons(self, toonIds, hack):
        assert(self.notify.debug('setToons(): %s' % toonIds))
        self.toonIds = toonIds
        oldtoons = self.toons
        self.toons = []
        for toonId in toonIds:
            if (toonId != 0):
                if (self.cr.doId2do.has_key(toonId)):
                    toon = self.cr.doId2do[toonId]
                    toon.stopSmooth()
                    self.toons.append(toon)
                    if (oldtoons.count(toon) == 0):
                        assert(self.notify.debug('setToons() - new toon: %d' % \
                                toon.doId))
                        self.__addToon(toon)
                else:
                    self.notify.warning('setToons() - no toon: %d' % toonId)
        for toon in oldtoons:
            if (self.toons.count(toon) == 0):
                self.__removeToon(toon)

    def setSuits(self, suitIds, reserveIds, values):
        assert(self.notify.debug('setSuits(): active %s reserve %s values %s' \
                % (suitIds, reserveIds, values)))
        oldsuits = self.suits
        self.suits = []
        self.joiningReserves = []
        for suitId in suitIds:
            if (self.cr.doId2do.has_key(suitId)):
                suit = self.cr.doId2do[suitId]
                self.suits.append(suit)
                # Set this on the client
                suit.fsm.request('Battle')
                # This will allow client to respond to setState() from the
                # server from here on out
                suit.buildingSuit = 1
                suit.reparentTo(render)
                if (oldsuits.count(suit) == 0):
                    assert(self.notify.debug('setSuits() suit: %d joining' % \
                        suit.doId))
                    self.joiningReserves.append(suit)
            else:
                self.notify.warning('setSuits() - no suit: %d' % suitId)
        self.reserveSuits = []
        assert(len(reserveIds) == len(values))
        for index in range(len(reserveIds)):
            suitId = reserveIds[index]
            if (self.cr.doId2do.has_key(suitId)):
                suit = self.cr.doId2do[suitId]
                self.reserveSuits.append((suit, values[index]))
            else:
                self.notify.warning('setSuits() - no suit: %d' % suitId)

        if (len(self.joiningReserves) > 0):
            assert(self.notify.debug('setSuits() reserves joining'))
            self.fsm.request('ReservesJoining')
    
    def setState(self, state, timestamp):
        assert(self.notify.debug("setState(%s, %d)" % \
                                (state, timestamp)))
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    ##### Messages to the server #####

    def d_elevatorDone(self):
        assert(self.notify.debug('network:elevatorDone(%d)' % base.localAvatar.doId))
        self.sendUpdate('elevatorDone', [])

    def d_reserveJoinDone(self):
        assert(self.notify.debug('network:reserveJoinDone(%d)' % base.localAvatar.doId))
        self.sendUpdate('reserveJoinDone', [])

    # Specific State Functions

    ##### Off state #####
    
    def enterOff(self, ts=0):
        assert(self.notify.debug('enterOff()'))
        return None
    
    def exitOff(self):
        return None

    ##### WaitForAllToonsInside state #####

    def enterWaitForAllToonsInside(self, ts=0):
        assert(self.notify.debug('enterWaitForAllToonsInside()'))
        return None

    def exitWaitForAllToonsInside(self):        
        return None

    ##### Elevator state #####

    def __playElevator(self, ts, name, callback):
        # Load the floor model 

        SuitHs = []   # Heading angles
        SuitPositions = []

        if self.floorModel:
            self.floorModel.removeNode()
            self.floorModel = None

        if (self.currentFloor == 0):
            # bottom floor
            SuitHs = self.BottomFloor_SuitHs
            SuitPositions = self.BottomFloor_SuitPositions
        if self.isBossFloor(self.currentFloor):
            # Top floor
            self.floorModel = loader.loadModel('phase_7/models/modules/boss_suit_office')
            SuitHs = self.BossOffice_SuitHs
            SuitPositions = self.BossOffice_SuitPositions            
        else:
            # middle floor
            SuitHs = self.Cubicle_SuitHs
            SuitPositions = self.Cubicle_SuitPositions

        if self.floorModel:
            self.floorModel.reparentTo(render)

            # We need to name this something more useful (and we'll need the
            # location of the opposite elevator as well)
            elevIn = self.floorModel.find('**/elevator-in')
            elevOut = self.floorModel.find('**/elevator-out')
        else:
            # TODO: TEMP
            floorModel = loader.loadModel('phase_7/models/modules/boss_suit_office')
            elevIn = floorModel.find('**/elevator-in').copyTo(render)
            elevOut = floorModel.find('**/elevator-out').copyTo(render)
            floorModel.removeNode()

        # store elevOut until it's needed
        self.elevOut = elevOut

        # Position the suits

        assert(len(self.suits) <= 4)
        for index in range(len(self.suits)):
            assert(self.notify.debug('setting suit: %d to pos: %s' % \
                (self.suits[index].doId, SuitPositions[index])))
            self.suits[index].setPos(SuitPositions[index])
            if (len(self.suits) > 2):
                self.suits[index].setH(SuitHs[index])
            else:
                self.suits[index].setH(170)  # if there's 2 or 1 suits, make them face fwd since there's no other suits they would be to be talking to
            self.suits[index].loop('neutral')

        # Position the toons
        for toon in self.toons:
            toon.reparentTo(self.elevatorModelIn)
            assert(self.toonIds.count(toon.doId) == 1)
            index = self.toonIds.index(toon.doId)
            assert(index >= 0 and index <= 3)
            toon.setPos(ElevatorPoints[index][0],
                        ElevatorPoints[index][1],
                        ElevatorPoints[index][2])
            toon.setHpr(180, 0, 0)
            toon.loop('neutral')

        # Show the elevator and position it in the correct place for the floor
        self.elevatorModelIn.reparentTo(elevIn)
        # Start with the doors in closed position
        self.leftDoorIn.setPos(3.5, 0, 0)
        self.rightDoorIn.setPos(-3.5, 0, 0)

        # Position the camera behind the toons
        camera.reparentTo(self.elevatorModelIn)
        camera.setH(180)
        camera.setPos(0, 14, 4)

        # Play elevator music
        base.playMusic(self.elevatorMusic, looping=1, volume=0.8)

        # Ride the elevator, then open the doors.
        track = Sequence(
            ElevatorUtils.getRideElevatorInterval(ELEVATOR_NORMAL),
            ElevatorUtils.getOpenInterval(self, self.leftDoorIn, self.rightDoorIn,
                                          self.openSfx, None, type = ELEVATOR_NORMAL),
            Func(camera.wrtReparentTo, render),
            )
                         
        for toon in self.toons:
            track.append(Func(toon.wrtReparentTo, render))
        track.append(Func(callback))
        track.start(ts)
        self.activeIntervals[name] = track
        
    def enterElevator(self, ts=0):
        # Load model for the current floor and the suit models for the floor
        assert(self.notify.debug('enterElevator()'))

        self.currentFloor += 1
        self.cr.playGame.getPlace().currentFloor = self.currentFloor
        self.setElevatorLights(self.elevatorModelIn)
        self.setElevatorLights(self.elevatorModelOut)

        # hide elevator from previous floor (if any)
        # unless it's the top floor, in that case leave it where it is
        if not self.isBossFloor(self.currentFloor):
            self.elevatorModelOut.detachNode()
        
        self.__playElevator(ts, self.elevatorName, self.__handleElevatorDone)

        # Get the floor multiplier
        mult = ToontownBattleGlobals.getCreditMultiplier(self.currentFloor)
        # Now set the inventory battleCreditMult
        base.localAvatar.inventory.setBattleCreditMultiplier(mult)

    def __handleElevatorDone(self):
        assert(self.notify.debug('handleElevatorDone()'))
        self.d_elevatorDone()

    def exitElevator(self):
        self.elevatorMusic.stop()
        self.__finishInterval(self.elevatorName)
        return None

    def enterGame(self, ts=0):
        assert(self.notify.debug('enterElevator()'))
        pass

    def exitGame(self):
        pass
    
    ##### Battle state #####

    def __playCloseElevatorOut(self, name):
        # Close the elevator doors
        track = Sequence(
            Wait(SUIT_LEAVE_ELEVATOR_TIME),
            Parallel(SoundInterval(self.closeSfx),
                     LerpPosInterval(self.leftDoorOut, 
                                     ElevatorData[ELEVATOR_NORMAL]['closeTime'],
                                     ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL),
                                     startPos=Point3(0, 0, 0), 
                                     blendType='easeOut'),
                     LerpPosInterval(self.rightDoorOut,
                                     ElevatorData[ELEVATOR_NORMAL]['closeTime'],
                                     ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL),
                                     startPos=Point3(0, 0, 0),
                                     blendType='easeOut')
                     ),
            )
        track.start()
        self.activeIntervals[name] = track

    def enterBattle(self, ts=0):
        assert(self.notify.debug('enterBattle()'))

        # now that we're in the barrel room, show the exit elevator
        # Show the elevator and position it in the correct place for the floor
        self.elevatorModelOut.reparentTo(self.elevOut)
        # Start with the doors in closed position
        self.leftDoorOut.setPos(3.5, 0, 0)
        self.rightDoorOut.setPos(-3.5, 0, 0)

        if (self.elevatorOutOpen == 1):
            self.__playCloseElevatorOut(self.uniqueName('close-out-elevator'))
            # Watch reserve suits as they walk from the elevator
            camera.setPos(0, -15, 6)
            camera.headsUp(self.elevatorModelOut)
        return None

    def exitBattle(self):
        if (self.elevatorOutOpen == 1):
            self.__finishInterval(self.uniqueName('close-out-elevator'))
            self.elevatorOutOpen = 0
        return None

    ##### ReservesJoining state #####

    def __playReservesJoining(self, ts, name, callback):
        # Position the joining suits
        index = 0
        assert(len(self.joiningReserves) <= 4)
        for suit in self.joiningReserves:
            suit.reparentTo(render)
            suit.setPos(self.elevatorModelOut, Point3(ElevatorPoints[index][0],
                                                      ElevatorPoints[index][1],
                                                      ElevatorPoints[index][2]))
            index += 1
            suit.setH(180)
            suit.loop('neutral')

        # Aim the camera at the far elevator
        track = Sequence(
            Func(camera.wrtReparentTo, self.elevatorModelOut),
            Func(camera.setPos, Point3(0, -8, 2)),
            Func(camera.setHpr, Vec3(0, 10, 0)),

            # Open the elevator doors
            Parallel(SoundInterval(self.openSfx),
                     LerpPosInterval(self.leftDoorOut, 
                                     ElevatorData[ELEVATOR_NORMAL]['closeTime'],
                                     Point3(0, 0, 0), 
                                     startPos=ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL),
                                     blendType='easeOut'),
                     LerpPosInterval(self.rightDoorOut,
                                     ElevatorData[ELEVATOR_NORMAL]['closeTime'],
                                     Point3(0, 0, 0), 
                                     startPos=ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL),
                                     blendType='easeOut'),
                     ),

            # Hold the camera angle for a couple of beats
            Wait(SUIT_HOLD_ELEVATOR_TIME),

            # Reparent the camera to render (enterWaitForInput will
            # position it properly again by the battle)
            Func(camera.wrtReparentTo, render),
            Func(callback),
            )
        track.start(ts)
        self.activeIntervals[name] = track

    def enterReservesJoining(self, ts=0):
        assert(self.notify.debug('enterReservesJoining()'))
        self.__playReservesJoining(ts, self.uniqueName('reserves-joining'),
                                       self.__handleReserveJoinDone)
        return None

    def __handleReserveJoinDone(self):
        assert(self.notify.debug('handleReserveJoinDone()'))
        self.joiningReserves = []
        self.elevatorOutOpen = 1
        self.d_reserveJoinDone()

    def exitReservesJoining(self):
        self.__finishInterval(self.uniqueName('reserves-joining'))
        return None

    ##### Resting state #####

    def enterResting(self, ts=0):
        assert(self.notify.debug('enterResting()'))
        base.playMusic(self.waitMusic, looping=1, volume=0.7)
        self.__closeInElevator()
        return

    def exitResting(self):
        self.waitMusic.stop()
        return

    ##### Reward state #####

    def enterReward(self, ts=0):
        assert(self.notify.debug('enterReward()'))
        base.localAvatar.b_setParent(ToontownGlobals.SPHidden)
        request = {
            "loader": ZoneUtil.getBranchLoaderName(self.extZoneId),
            "where": ZoneUtil.getToonWhereName(self.extZoneId),
            "how": "elevatorIn",
            "hoodId": ZoneUtil.getHoodId(self.extZoneId),
            "zoneId": self.extZoneId,
            "shardId": None,
            "avId": -1,
            "bldgDoId": self.distBldgDoId
            }
        # Presumably, suitInterior.py has hung a hook waiting for
        # this request. I mimicked what DistributedDoor was doing.
        messenger.send("DSIDoneEvent", [request])
        return None

    def exitReward(self):
        return None

    ##### Reset state #####

    #def enterReset(self, ts=0):
    #    assert(self.notify.debug('enterReset()'))
    #    self.__cleanup()
    #    return None

    #def exitReset(self):
    #    return None

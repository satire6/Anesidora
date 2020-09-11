from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import BulletinBoardWatcher
from otp.otpbase import OTPGlobals
from toontown.toonbase  import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.coghq import CountryClubLayout
from toontown.coghq import DistributedCountryClubRoom
from toontown.coghq import CountryClubRoom
from toontown.coghq import FactoryCameraViews
from direct.gui import OnscreenText
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *

class DistributedCountryClub(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCountryClub')

    ReadyPost = 'CountryClubReady'
    WinEvent = 'CountryClubWinEvent'
    doBlockRooms = base.config.GetBool('block-country-club-rooms',1)

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.lastCamEnterRoom = 0

        self.titleColor = (1,1,1,1)
        self.titleText = OnscreenText.OnscreenText(
            "",
            fg = self.titleColor,
            shadow = (0,0,0,1),
            font = ToontownGlobals.getSignFont(),
            pos = (0,-0.5),
            scale = 0.10,
            drawOrder = 0,
            mayChange = 1,
            )
        self.titleSequence = None

    def generate(self):
        self.notify.debug('generate: %s' % self.doId)
        DistributedObject.DistributedObject.generate(self)

        bboard.post('countryClub', self)

        self.roomWatcher = None
        self.geom = None
        self.rooms = []
        self.hallways = []
        self.allRooms = []
        self.curToonRoomNum = None
        self.allBlockedRooms = []
        
        base.localAvatar.setCameraCollisionsCanMove(1)

        # place local toon here just in case we don't have an entrancePoint
        # entity set up
        base.localAvatar.reparentTo(render)
        base.localAvatar.setPosHpr(0,0,0,0,0,0)

        self.accept('SOSPanelEnter', self.handleSOSPanel)

        # add special camera views
        self.factoryViews = FactoryCameraViews.FactoryCameraViews(self)

        # add factory menu to SpeedChat
        base.localAvatar.chatMgr.chatInputSpeedChat.addFactoryMenu()
        
        self.__setupHighSky()
        
    def startSky(self):
        # Parent the sky to our camera, the task will counter rotate it
        self.sky = loader.loadModel('phase_12/models/bossbotHQ/BossTestSkyBox')
        self.sky.reparentTo(camera)
        # Nowadays we use a CompassEffect to counter-rotate the sky
        # automatically at render time, rather than depending on a
        # task to do this just before the scene is rendered.
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        self.sky.setBin('background', 0)
        #base.ccsky = self.sky
        # Since we are using a CompassEffect, we don't have to spawn a
        # task.  Some hoods may spawn a task anyway, to do some
        # additional work (like rotating clouds).

    def stopSky(self):
        # Remove the sky task just in case it was spawned.
        taskMgr.remove("skyTrack")
        self.sky.remove()#reparentTo(hidden)
        
    def __setupHighSky(self):
        self.startSky()
        sky = self.sky

        # Rotate the sky around so the more interesting part is
        # visible.
        sky.setH(150)
        sky.setZ(-100)
        
    def __cleanupHighSky(self):
        # Turn the sky off
        
        # self.cloudRing.removeNode()
        sky = self.sky
        sky.setH(0)
        sky.setZ(0)
        self.stopSky()

    # required fields
    def setZoneId(self, zoneId):
        self.zoneId = zoneId
        
    def setCountryClubId(self, id):
        DistributedCountryClub.notify.debug('setCountryClubId: %s' % id)
        self.countryClubId = id

    def setFloorNum(self, num):
        DistributedCountryClub.notify.debug('floorNum: %s' % num)
        self.floorNum = num
        self.layout = CountryClubLayout.CountryClubLayout(self.countryClubId, self.floorNum, self.layoutIndex)
        
    def setLayoutIndex(self, layoutIndex):
        self.layoutIndex = layoutIndex
            
    def getLayoutIndex(self):
        return self.layoutIndex

    def setRoomDoIds(self, roomDoIds):
        self.roomDoIds = roomDoIds
        self.roomWatcher = BulletinBoardWatcher.BulletinBoardWatcher(
            'roomWatcher-%s' % self.doId,
            [DistributedCountryClubRoom.getCountryClubRoomReadyPostName(doId)
             for doId in self.roomDoIds], self.gotAllRooms)

    def gotAllRooms(self):
        self.notify.debug('countryClub %s: got all rooms' % self.doId)
        self.roomWatcher.destroy()
        self.roomWatcher = None

        self.geom = render.attachNewNode('countryClub%s' % self.doId)

        # fill out our table of rooms
        for doId in self.roomDoIds:
            self.rooms.append(base.cr.doId2do[doId])
            self.rooms[-1].setCountryClub(self)

        self.notify.info('countryClubId %s, floor %s, %s' % (
            self.countryClubId, self.floorNum, self.rooms[0].avIdList))

        rng = self.layout.getRng()
        numRooms = self.layout.getNumRooms()

        for i, room in enumerate(self.rooms):
            # there's a hallway between each pair of rooms
            if i == 0:
                room.getGeom().reparentTo(self.geom)
            else:
                # attach the room to the preceding hallway
                room.attachTo(self.hallways[i-1], rng)
            self.allRooms.append(room)
            self.listenForFloorEvents(room)
            
            if i < (numRooms-1):
                # add a hallway leading out of the room
                hallway = CountryClubRoom.CountryClubRoom(self.layout.getHallwayModel(i))
                hallway.attachTo(room, rng)
                hallway.setRoomNum((i*2)+1)
                hallway.initFloorCollisions()
                hallway.enter()
                self.hallways.append(hallway)
                self.allRooms.append(hallway)
                self.listenForFloorEvents(hallway)

        # listen for camera-ray/floor collision events
        def handleCameraRayFloorCollision(collEntry, self=self):
            name = collEntry.getIntoNode().getName()
            self.notify.debug('camera floor ray collided with: %s' % name)
            prefix = CountryClubRoom.CountryClubRoom.FloorCollPrefix
            prefixLen = len(prefix)
            if (name[:prefixLen] == prefix):
                try:
                    roomNum = int(name[prefixLen:])
                except:
                    DistributedLevel.notify.warning(
                        'Invalid zone floor collision node: %s'
                        % name)
                else:
                    self.camEnterRoom(roomNum)
        self.accept('on-floor', handleCameraRayFloorCollision)

        if bboard.has('countryClubRoom'):
            self.warpToRoom(bboard.get('countryClubRoom'))

        # get this event name before we send out our first setZone
        firstSetZoneDoneEvent = self.cr.getNextSetZoneDoneEvent()
        # wait until the first viz setZone completes before announcing
        # that we're ready to go
        def handleFirstSetZoneDone():
            self.notify.debug('countryClubHandleFirstSetZoneDone')
            self.accept('takingScreenshot', self.handleScreenshot)
            # do this here; the elevator (which does an iris out) is guaranteed to
            # be gone by now, so if it's going to do an iris out, it's already done
            base.transitions.irisIn()
            # NOW we're ready.
            bboard.post(DistributedCountryClub.ReadyPost, self)
        self.acceptOnce(firstSetZoneDoneEvent, handleFirstSetZoneDone)

        # listen to all of the network zones; no network visibility for now
        zoneList = [OTPGlobals.UberZone, self.zoneId]
        for room in self.rooms:
            zoneList.extend(room.zoneIds)
        base.cr.sendSetZoneMsg(self.zoneId, zoneList)

    def listenForFloorEvents(self, room):
        roomNum = room.getRoomNum()
        floorCollName = room.getFloorCollName()

        # listen for zone enter events from floor collisions
        def handleZoneEnter(collisionEntry,
                            self=self, roomNum=roomNum):
            self.toonEnterRoom(roomNum)
            floorNode = collisionEntry.getIntoNode()
            if floorNode.hasTag('ouch'):
                room = self.allRooms[roomNum]
                ouchLevel = room.getFloorOuchLevel()
                room.startOuch(ouchLevel)
        self.accept('enter%s' % floorCollName, handleZoneEnter)

        # also listen for zone exit events for the sake of the
        # ouch system
        def handleZoneExit(collisionEntry,
                           self=self, roomNum=roomNum):
            floorNode = collisionEntry.getIntoNode()
            if floorNode.hasTag('ouch'):
                self.allRooms[roomNum].stopOuch()
        self.accept('exit%s' % floorCollName, handleZoneExit)

    def getAllRoomsTimeout(self):
        self.notify.warning('countryClub %s: timed out waiting for room objs' %
                            self.doId)
        # TODO: abandon going to the countryClub, go back

    def toonEnterRoom(self, roomNum):
        self.notify.debug('toonEnterRoom: %s' % roomNum)
        if roomNum != self.curToonRoomNum:
            if self.curToonRoomNum is not None:
                self.allRooms[self.curToonRoomNum].localToonFSM.request(
                    'notPresent')
            self.allRooms[roomNum].localToonFSM.request('present')
            self.curToonRoomNum = roomNum

    def camEnterRoom(self, roomNum):
        self.notify.debug('camEnterRoom: %s' % roomNum)
        blockRoomsAboveThisNumber = len(self.allRooms)
        if self.allBlockedRooms and self.doBlockRooms:
            # assume that blocked rooms is sorted
            blockRoomsAboveThisNumber = self.allBlockedRooms[0]
        if (roomNum % 2) == 1:
            # this is a hallway; we should see the rooms on either side
            # and the hallways leading out of them
            minVis = roomNum-2
            maxVis = roomNum+2
        else:
            # we're in a room, we only need to see the adjacent hallways
            minVis = roomNum-1
            maxVis = roomNum+1
        for i, room in enumerate(self.allRooms):
            if i < minVis or i > maxVis:
                if not room.getGeom().isEmpty():
                    room.getGeom().stash()
            else:
                if i <= blockRoomsAboveThisNumber:
                    if not room.getGeom().isEmpty():
                        room.getGeom().unstash()
                else:
                    if not room.getGeom().isEmpty():
                        room.getGeom().stash()
        self.lastCamEnterRoom = roomNum

    def setBossConfronted(self, avId):
        # the avId has already been vetted by the room that received the msg
        if avId == base.localAvatar.doId:
            return
        av = base.cr.identifyFriend(avId)
        if av is None:
            return
        base.localAvatar.setSystemMessage(
            avId, TTLocalizer.CountryClubBossConfrontedMsg % av.getName())

    def warpToRoom(self, roomId):
        # returns False if invalid roomId
        # find a room with the right id
        for i in xrange(len(self.rooms)):
            room = self.rooms[i]
            if room.roomId == roomId:
                break
        else:
            return False
        base.localAvatar.setPosHpr(room.getGeom(), 0,0,0, 0,0,0)
        # account for the hallways
        self.camEnterRoom(i*2)
        return True

    def disable(self):
        self.notify.debug('disable')
        
        if self.titleSequence:
            self.titleSequence.finish()
        self.titleSequence = None
        
        self.__cleanupHighSky()

        self.ignoreAll()

        for hallway in self.hallways:
            hallway.exit()

        self.rooms = []
        for hallway in self.hallways:
            hallway.delete()
        self.hallways = []
        self.allRooms = []

        if self.roomWatcher:
            self.roomWatcher.destroy()
            self.roomWatcher = None

        if self.geom is not None:
            self.geom.removeNode()
            self.geom = None

        base.localAvatar.setCameraCollisionsCanMove(0)

        if (hasattr(self, 'relatedObjectMgrRequest')
                and self.relatedObjectMgrRequest):
            self.cr.relatedObjectMgr.abortRequest(self.relatedObjectMgrRequest)
            del self.relatedObjectMgrRequest

        DistributedObject.DistributedObject.disable(self)
        

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        self.ignore('SOSPanelEnter')
        bboard.remove('countryClub')
        # remove factory menu from SpeedChat
        base.localAvatar.chatMgr.chatInputSpeedChat.removeFactoryMenu()
        # remove special camera views
        self.factoryViews.delete()
        del self.factoryViews
        
    def handleSOSPanel(self, panel):
        # make a list of toons that are still in the countryClub
        avIds = []
        for avId in self.rooms[0].avIdList:
            # if a toon dropped and came back into the game, they won't
            # be in the factory, so they won't be in the doId2do.
            if base.cr.doId2do.get(avId):
                avIds.append(avId)
        panel.setFactoryToonIdList(avIds)

    def handleScreenshot(self):
        base.addScreenshotString('countryClubId: %s, floor (from 1): %s' % (
            self.countryClubId, self.floorNum+1))
        if hasattr(self, 'currentRoomName'):
            base.addScreenshotString('%s' % self.currentRoomName)

    def setBlockedRooms(self, blockedRooms):
        """Handle the AI telling us which rooms are blocked."""
        assert self.notify.debugStateCall()
        # note the blockedRooms we get from the ai does not consider hallways
        self.blockedRooms = blockedRooms
        self.computeBlockedRoomsAndHallways()
        self.camEnterRoom(self.lastCamEnterRoom)

    def computeBlockedRoomsAndHallways(self):
        """Compute all blocked rooms which includes hallways."""
        self.allBlockedRooms = []
        for roomIndex in self.blockedRooms:
            # this assumes one hallway in between each room
            self.allBlockedRooms.append(roomIndex*2)
        self.allBlockedRooms.sort()
        self.notify.debug('self.allBlockedRooms =%s' % self.allBlockedRooms)

    def setCountryClubZone(self, zoneId):
        """Handle the AI telling us the new zone id after boarding the elevator."""
        base.cr.sendSetZoneMsg(zoneId)
        base.cr.playGame.getPlace().fsm.request("walk")
        scale = base.localAvatar.getScale()
        base.camera.setScale(scale)

    def elevatorAlert(self, avId):
        if base.localAvatar.doId != avId:
            name = base.cr.doId2do[avId].getName()
            self.showInfoText(TTLocalizer.CountryClubToonEnterElevator % (name))
            #av = base.localAvatar
            #message = TLocalizer.stageToonEnterElevator % (name)
            #av.setSystemMessage( 0, message)                    

    def showInfoText(self, text = "hello world"):
        description = text
        if description and description != '':
            self.titleText.setText(description)
            self.titleText.setColor(Vec4(*self.titleColor))
            self.titleText.setColorScale(1,1,1,1)
            self.titleText.setFg(self.titleColor)
            
            if self.titleSequence:
                self.titleSequence.finish()


            self.titleSequence = None
            self.titleSequence =  Sequence(
                            Func(self.showTitleText),
                            Wait(3.1),
                            LerpColorScaleInterval(self.titleText, duration=0.5, colorScale = Vec4(1,1,1,0.0)),
                            Func(self.hideTitleText),
                        )
                    
            self.titleSequence.start()
        
            
            
    def showTitleText(self):
        if self.titleText:
            self.titleText.show()
        
    def hideTitleText(self):
        if self.titleText or 1:
            self.titleText.hide()
    

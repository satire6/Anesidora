from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals
from toontown.coghq import CountryClubRoomSpecs
from direct.directnotify import DirectNotifyGlobal
import random

class CountryClubRoom(DirectObject.DirectObject):
    """Represents the geometry of a single room of a mint. This includes
    hallways. Handles logic for matching up doorways to doorways of
    adjacent rooms."""

    notify = DirectNotifyGlobal.directNotify.newCategory('CountryClubRoom')    
    
    FloorCollPrefix = 'mintFloorColl'
    CashbotMintDoorFrame = 'phase_10/models/cashbotHQ/DoorFrame'
    
    def __init__(self, path=None):
        if path is not None:
            if path in CountryClubRoomSpecs.BossbotCountryClubConnectorRooms:
                loadFunc = loader.loadModelCopy
            else:
                loadFunc = loader.loadModel
            self.setGeom(loadFunc(path))
        
        self.localToonFSM = ClassicFSM.ClassicFSM('CountryClubRoomLocalToonPresent',
                                          [State.State('off',
                                                       self.enterLtOff,
                                                       self.exitLtOff,
                                                       ['notPresent']),
                                           State.State('notPresent',
                                                       self.enterLtNotPresent,
                                                       self.exitLtNotPresent,
                                                       ['present']),
                                           State.State('present',
                                                       self.enterLtPresent,
                                                       self.exitLtPresent,
                                                       ['notPresent']),
                                           ],
                                           # Initial State
                                           'notPresent',
                                           # Final State
                                           'notPresent',
                                           )
        self.localToonFSM.enterInitialState()

    def delete(self):
        del self.localToonFSM

    def enter(self):
        self.localToonFSM.request('notPresent')
    def exit(self):
        self.localToonFSM.requestFinalState()
        
    def setRoomNum(self, num):
        # First room in the mint is room zero, first hallway is one, second
        # room is two, etc.
        self.roomNum = num
    def getRoomNum(self):
        return self.roomNum

    def setGeom(self, geom):
        assert self.notify.debugStateCall()
        if geom == None:
            import pdb; pdb.set_trace()
        self.__geom = geom
    def getGeom(self):
        return self.__geom

    def _getEntrances(self):
        return self.__geom.findAllMatches('**/ENTRANCE*')
    def _getExits(self):
        return self.__geom.findAllMatches('**/EXIT*')

    def attachTo(self, other, rng):
        # attach an entrance doorway of this room to another room's exit doorway
        otherExits = other._getExits()
        entrances = self._getEntrances()

        otherDoor = otherExits[0] #rng.choice(otherExits)
        thisDoor = rng.choice(entrances)
        geom = self.getGeom()
        otherGeom = other.getGeom()

        self.notify.debug('thisDoor = %s' % thisDoor)
        self.notify.debug('otherDoor = %s' % otherDoor)
        self.notify.debug('thisGeom = %s' % geom)
        self.notify.debug('otherGeom = %s' % otherGeom)

        debugAxis1 = None # loader.loadModel('models/misc/xyzAxis')
        if debugAxis1:
            debugAxis1.reparentTo(thisDoor)
        
        debugAxis2 = None # loader.loadModel('models/misc/smiley')
        if debugAxis2:
            debugAxis2.reparentTo(otherDoor)
            debugAxis2.setColorScale(0.5,0.5,0.5,1)

        tempNode = otherDoor.attachNewNode('tempRotNode')
        geom.reparentTo(tempNode)
        geom.clearMat()
        # position our door at our origin so that it's on top of the other door
        newGeomPos = Vec3(0)-thisDoor.getPos(geom)
        self.notify.debug('newGeomPos = %s' % newGeomPos)
        geom.setPos(newGeomPos)
        # rotate so that our door is facing the right way
        newTempNodeH = -thisDoor.getH(otherDoor)
        self.notify.debug('newTempNodeH =%s' % newTempNodeH)
        tempNode.setH(newTempNodeH)
        geom.wrtReparentTo(otherGeom.getParent())
        tempNode.removeNode()

        #doorFrame = loader.loadModel(CountryClubRoom.CashbotMintDoorFrame)
        #doorFrame.reparentTo(thisDoor)

    def getFloorCollName(self):
        return '%s%s' % (CountryClubRoom.FloorCollPrefix, self.roomNum)

    def initFloorCollisions(self):
        # call this after calling setGeom and before adding anything under
        # the room geometry
        
        # we handle floor collisions differently from a standard level. Our
        # entire level is going to be treated as one 'zone' (this level
        # represents one room of the mint)
        allColls = self.getGeom().findAllMatches('**/+CollisionNode')
        # which of them, if any, are floors?
        floorColls = []
        for coll in allColls:
            bitmask = coll.node().getIntoCollideMask()
            if not (bitmask & ToontownGlobals.FloorBitmask).isZero():
                floorColls.append(coll)
        if len(floorColls) > 0:
            # rename the floor collision nodes, and make sure no other
            # nodes have that name
            floorCollName = self.getFloorCollName()
            others = self.getGeom().findAllMatches(
                '**/%s' % floorCollName)
            for other in others:
                other.setName('%s_renamed' % floorCollName)
            for floorColl in floorColls:
                floorColl.setName(floorCollName)

    # states for 'localToon present' FSM
    def enterLtOff(self):
        pass
    def exitLtOff(self):
        pass

    def enterLtNotPresent(self):
        # called when localToon is no longer in this room
        pass
    def exitLtNotPresent(self):
        pass

    def enterLtPresent(self):
        # called when localToon is in this room
        pass
    def exitLtPresent(self):
        pass

    if __debug__:
        def _showAxes(self):
            self.axes = []
            axis = loader.loadModel("models/misc/xyzAxis.bam")
            axis.setColorOff()
            # last 1 overrides default colorScale
            axis.setColorScale(1,1,1,1,1)
            for doorway in self._getEntrances() + self._getExits():
                self.axes.append(axis.copyTo(doorway))
            self.axes.append(axis.copyTo(self.model))
            self.axes[-1].setScale(.6)

        def _isolateAxis(self, index):
            for i in range(len(self.axes)):
                if i == index:
                    self.axes[i].show()
                else:
                    self.axes[i].hide()

        def _hideAxes(self):
            for axis in self.axes:
                axis.removeNode()
            del self.axes


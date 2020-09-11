""" DistributedBuilding module: contains the DistributedBuilding
    class, the client side representation of a 'building'."""

from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.directtools.DirectGeometry import *
from ElevatorConstants import *
from ElevatorUtils import *
from SuitBuildingGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
import random
from toontown.suit import SuitDNA
from toontown.toonbase import TTLocalizer
from toontown.distributed import DelayDelete
from toontown.toon import TTEmote
from otp.avatar import Emote
from toontown.hood import ZoneUtil

class DistributedBuilding(DistributedObject.DistributedObject):
    """
    DistributedBuilding class:  The client side representation of a
    'building' which can be taken over by bad guys and toons.  Each
    of these buildings can also be 'entered' by bad guys and toons.
    This object also has a server side representation of it,
    DistributedBuildingAI.  This object has to worry about updating
    the display of the building and all of its components on the
    client's machine.  The display of the building is either 'toon
    owned' or 'bad guy owned'.
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuilding')

    # the initial height of suit buildings when a toon building is taken over
    #
    SUIT_INIT_HEIGHT = 125

    # Where to load the takeover sound effects from
    TAKEOVER_SFX_PREFIX = "phase_5/audio/sfx/"

    def __init__(self, cr):
        """constructor for the DistributedBuilding"""
        DistributedObject.DistributedObject.__init__(self, cr)
        assert(self.debugPrint("__init()"))
        self.interactiveProp = None

        self.suitDoorOrigin = None
        self.elevatorModel = None

        self.fsm = ClassicFSM.ClassicFSM('DistributedBuilding',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['waitForVictors',
                                         'waitForVictorsFromCogdo',
                                         'becomingToon',
                                         'becomingToonFromCogdo',
                                         'toon',
                                         'clearOutToonInterior',
                                         'becomingSuit',
                                         'suit',
                                         'clearOutToonInteriorForCogdo',
                                         'becomingCogdo',
                                         'cogdo']),
                            State.State('waitForVictors',
                                        self.enterWaitForVictors,
                                        self.exitWaitForVictors,
                                        ['becomingToon',
                                         ]),
                            State.State('waitForVictorsFromCogdo',
                                        self.enterWaitForVictorsFromCogdo,
                                        self.exitWaitForVictorsFromCogdo,
                                        ['becomingToonFromCogdo',
                                         ]),
                            State.State('becomingToon',
                                        self.enterBecomingToon,
                                        self.exitBecomingToon,
                                        ['toon']),
                            State.State('becomingToonFromCogdo',
                                        self.enterBecomingToonFromCogdo,
                                        self.exitBecomingToonFromCogdo,
                                        ['toon']),
                            State.State('toon',
                                        self.enterToon,
                                        self.exitToon,
                                        ['clearOutToonInterior', 'clearOutToonInteriorForCogdo']),
                            State.State('clearOutToonInterior',
                                        self.enterClearOutToonInterior,
                                        self.exitClearOutToonInterior,
                                        ['becomingSuit']),
                            State.State('becomingSuit',
                                        self.enterBecomingSuit,
                                        self.exitBecomingSuit,
                                        ['suit']),
                            State.State('suit',
                                        self.enterSuit,
                                        self.exitSuit,
                                        ['waitForVictors',
                                         'becomingToon',        # debug only
                                         ]),
                            State.State('clearOutToonInteriorForCogdo',
                                        self.enterClearOutToonInteriorForCogdo,
                                        self.exitClearOutToonInteriorForCogdo,
                                        ['becomingCogdo']),
                            State.State('becomingCogdo',
                                        self.enterBecomingCogdo,
                                        self.exitBecomingCogdo,
                                        ['cogdo']),
                            State.State('cogdo',
                                        self.enterCogdo,
                                        self.exitCogdo,
                                        ['waitForVictorsFromCogdo',
                                         'becomingToonFromCogdo',        # debug only
                                         ])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                          )
        self.fsm.enterInitialState()
        # self.generate will be called automatically.

        # TODO: Eventually, bossLevel will be one of the
        # required fields. 
        self.bossLevel = 0

        # multitrack used to animate the transitions between suit and toon
        # buildings
        #
        self.transitionTrack = None

        # reference to the elevator created when a building is a suit type
        #
        self.elevatorNodePath = None

        # The list of toons who just won the building back.
        self.victorList = [0, 0, 0, 0]

        # This becomes a Label for the text that is displayed while
        # we are waiting for the elevator doors to open.
        self.waitingMessage = None

        # Placeholders for sound effects.
        self.cogDropSound = None
        self.cogLandSound = None
        self.cogSettleSound = None
        self.cogWeakenSound = None
        self.toonGrowSound = None
        self.toonSettleSound = None
        
    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.debugPrint("generate()"))
        DistributedObject.DistributedObject.generate(self)
        self.mode = 'toon'
        # (the default is to be a toon building, so toonTakeOver()
        # can ignore the first call for toon take over).
        self.townTopLevel=self.cr.playGame.hood.loader.geom
        assert(not self.townTopLevel.isEmpty())
    
    def disable(self):
        assert(self.debugPrint("disable()"))
        # Go to the off state when the object is put in the cache
        self.fsm.request("off")
        del self.townTopLevel
        self.stopTransition()
        DistributedObject.DistributedObject.disable(self)
        # self.delete() will automatically be called.
    
    def delete(self):
        assert(self.debugPrint("delete()"))
        if self.elevatorNodePath:
            self.elevatorNodePath.removeNode()
            del self.elevatorNodePath
            del self.elevatorModel
            if hasattr(self, 'cab'):
                del self.cab
            del self.leftDoor
            del self.rightDoor
        del self.suitDoorOrigin
        self.cleanupSuitBuilding()
        self.unloadSfx()
        del self.fsm
        DistributedObject.DistributedObject.delete(self)
    
    def setBlock(self, block, interiorZoneId):
        self.block = block
        self.interiorZoneId = interiorZoneId
    
    def setSuitData(self, suitTrack, difficulty, numFloors):
        assert(self.debugPrint("setSuitData(%s, %d, %d)" %(suitTrack, difficulty, numFloors)))
        self.track=suitTrack
        self.difficulty=difficulty
        self.numFloors=numFloors
    
    def setState(self, state, timestamp):
        assert(self.debugPrint("setState(%s, %d)" % (state, timestamp)))
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def getSuitElevatorNodePath(self):
        """getElevatorNodePath(self)

        Returns the elevator node path associated with the suit
        building.  This assumes the building is in suit mode.  If the
        building is not in suit mode (in particular, if it hasn't had
        any mode at all set yet), assumes the building is meant to be
        in suit mode and switches it immediately.
        """
        if self.mode != 'suit':
            self.setToSuit()

        assert(self.elevatorNodePath != None)
        return self.elevatorNodePath

    def getCogdoElevatorNodePath(self):
        if self.mode != 'cogdo':
            self.setToCogdo()

        assert(self.elevatorNodePath != None)
        return self.elevatorNodePath

    def getSuitDoorOrigin(self):
        if self.mode != 'suit':
            self.setToSuit()

        return self.suitDoorOrigin

    def getCogdoDoorOrigin(self):
        if self.mode != 'cogdo':
            self.setToCogdo()

        return self.suitDoorOrigin

    def getBossLevel(self):
        return self.bossLevel

    def setBossLevel(self, bossLevel):
        self.bossLevel = bossLevel

    def setVictorList(self, victorList):
        self.victorList = victorList
    
    ##### off state #####
    
    def enterOff(self):
        assert(self.debugPrint("enterOff()"))
    
    def exitOff(self):
        assert(self.debugPrint("exitOff()"))

    ##### waitForVictors state #####
    def enterWaitForVictors(self, ts):
        if self.mode != 'suit':
            self.setToSuit()
        victorCount = self.victorList.count(base.localAvatar.doId)
        if victorCount == 1:
            self.acceptOnce("insideVictorElevator", self.handleInsideVictorElevator)

            # Since the localToon is on the elevator, we should
            # position the camera in front of the building so we have
            # something to look at while we're waiting for everyone to
            # load up the zone.  This duplicates the camera setup in
            # the beginning of walkOutCameraTrack().
            camera.reparentTo(render)
            camera.setPosHpr(self.elevatorNodePath,
                             0, -32.5, 9.4, 0, 348, 0)
            base.camLens.setFov(52.0)

            # Are we waiting for any other players to come out?
            anyOthers = 0
            for v in self.victorList:
                if v != 0 and v != base.localAvatar.doId:
                    anyOthers = 1

            if anyOthers:
                self.waitingMessage = DirectLabel(
                    text = TTLocalizer.BuildingWaitingForVictors,
                    text_fg = VBase4(1,1,1,1),
                    text_align = TextNode.ACenter,
                    relief = None,
                    pos = (0, 0, 0.35),
                    scale = 0.1)

        elif victorCount == 0:
            pass
        else:
            self.error("localToon is on the victorList %d times" % victorCount)

        # Make sure the elevator doors are still closed in this state.
        closeDoors(self.leftDoor, self.rightDoor)

        # And turn off the elevator light.
        for light in self.floorIndicator:
            if light != None:
                light.setColor(LIGHT_OFF_COLOR)
            
        return

    def handleInsideVictorElevator(self):
        self.sendUpdate("setVictorReady", [])
        return

    def exitWaitForVictors(self):
        self.ignore("insideVictorElevator")
        if self.waitingMessage != None:
            self.waitingMessage.destroy()
            self.waitingMessage = None
        return
    
    ##### waitForVictorsFromCogdo state #####
    def enterWaitForVictorsFromCogdo(self, ts):
        if self.mode != 'cogdo':
            self.setToCogdo()
        victorCount = self.victorList.count(base.localAvatar.doId)
        if victorCount == 1:
            self.acceptOnce("insideVictorElevator", self.handleInsideVictorElevatorFromCogdo)

            # Since the localToon is on the elevator, we should
            # position the camera in front of the building so we have
            # something to look at while we're waiting for everyone to
            # load up the zone.  This duplicates the camera setup in
            # the beginning of walkOutCameraTrack().
            camera.reparentTo(render)
            camera.setPosHpr(self.elevatorNodePath,
                             0, -32.5, 9.4, 0, 348, 0)
            base.camLens.setFov(52.0)

            # Are we waiting for any other players to come out?
            anyOthers = 0
            for v in self.victorList:
                if v != 0 and v != base.localAvatar.doId:
                    anyOthers = 1

            if anyOthers:
                self.waitingMessage = DirectLabel(
                    text = TTLocalizer.BuildingWaitingForVictors,
                    text_fg = VBase4(1,1,1,1),
                    text_align = TextNode.ACenter,
                    relief = None,
                    pos = (0, 0, 0.35),
                    scale = 0.1)

        elif victorCount == 0:
            pass
        else:
            self.error("localToon is on the victorList %d times" % victorCount)

        # Make sure the elevator doors are still closed in this state.
        closeDoors(self.leftDoor, self.rightDoor)

        # And turn off the elevator light.
        for light in self.floorIndicator:
            if light != None:
                light.setColor(LIGHT_OFF_COLOR)
            
        return

    def handleInsideVictorElevatorFromCogdo(self):
        self.sendUpdate("setVictorReady", [])
        return

    def exitWaitForVictorsFromCogdo(self):
        self.ignore("insideVictorElevator")
        if self.waitingMessage != None:
            self.waitingMessage.destroy()
            self.waitingMessage = None
        return
    
    ##### becomingToon state #####
    
    def enterBecomingToon(self, ts):
        assert(self.debugPrint("enterBecomingToon() %s" %(str(self.getDoId()))))
        # Start animation:
        self.animToToon(ts)
    
    def exitBecomingToon(self):
        assert(self.debugPrint("exitBecomingToon()"))
        # Stop animation:
    
    ##### becomingToonFromCogdo state #####
    
    def enterBecomingToonFromCogdo(self, ts):
        assert(self.debugPrint("enterBecomingToonFromCogdo() %s" %(str(self.getDoId()))))
        # Start animation:
        self.animToToonFromCogdo(ts)
    
    def exitBecomingToonFromCogdo(self):
        assert(self.debugPrint("exitBecomingToonFromCogdo()"))
        # Stop animation:
    
    ##### toon state #####
    
    def enterToon(self, ts):
        assert(self.debugPrint("enterToon()"))
        if self.getInteractiveProp():
            self.getInteractiveProp().buildingLiberated(self.doId)
        self.setToToon()
    
    def exitToon(self):
        assert(self.debugPrint("exitToon()"))
    
    ##### ClearOutToonInterior state #####
    
    def enterClearOutToonInterior(self, ts):
        assert(self.debugPrint("enterClearOutToonInterior()"))

    def exitClearOutToonInterior(self):
        assert(self.debugPrint("exitClearOutToonInterior()"))
    
    ##### becomingSuit state #####
    
    def enterBecomingSuit(self, ts):
        assert(self.debugPrint("enterBecomingSuit()"))
        # Start animation:
        #print "enterBecomingSuit %s" %(str(self.getDoId()))
        self.animToSuit(ts)

    def exitBecomingSuit(self):
        assert(self.debugPrint("exitBecomingSuit()"))
        # Stop animation:
        pass
    
    ##### suit state #####
    
    def enterSuit(self, ts):
        assert(self.debugPrint("enterSuit()"))
        #print "enterSuit %s" %(str(self.getDoId()))
        self.makePropSad()
        self.setToSuit()
    
    def exitSuit(self):
        assert(self.debugPrint("exitSuit()"))
    
    ##### ClearOutToonInterior state #####
    
    def enterClearOutToonInteriorForCogdo(self, ts):
        assert(self.debugPrint("enterClearOutToonInteriorForCogdo()"))

    def exitClearOutToonInteriorForCogdo(self):
        assert(self.debugPrint("exitClearOutToonInteriorForCogdo()"))
    
    ##### becomingCogdo state #####
    
    def enterBecomingCogdo(self, ts):
        assert(self.debugPrint("enterBecomingCogdo()"))
        # Start animation:
        #print "enterBecomingCogdo %s" %(str(self.getDoId()))
        self.animToCogdo(ts)

    def exitBecomingCogdo(self):
        assert(self.debugPrint("exitBecomingCogdo()"))
        # Stop animation:
        pass
    
    ##### cogdo state #####
    
    def enterCogdo(self, ts):
        assert(self.debugPrint("enterCogdo()"))
        #print "enterCogdo %s" %(str(self.getDoId()))
        self.setToCogdo()
    
    def exitCogdo(self):
        assert(self.debugPrint("exitCogdo()"))
    
    #####
    
    def getNodePaths(self):
        assert(self.debugPrint("getNodePaths()"))
        # Toon flat buildings:
        nodePath=[]
        # Find all tb or sb of this block, even stashed (";+s") ones:
        npc = self.townTopLevel.findAllMatches(
                "**/?b" + str(self.block) + ":*_DNARoot;+s")
        assert(npc.getNumPaths()>0)
        for i in range(npc.getNumPaths()):
            nodePath.append(npc.getPath(i))
        return nodePath

    def loadElevator(self, newNP):
        assert(self.debugPrint("loadElevator(newNP=%s)"%(newNP,)))
        # Load up an elevator
        self.elevatorNodePath = hidden.attachNewNode("elevatorNodePath")
        self.elevatorModel = loader.loadModel(
                "phase_4/models/modules/elevator")

        # Put up a display to show the current floor of the elevator
        self.floorIndicator=[None, None, None, None, None]
        npc=self.elevatorModel.findAllMatches("**/floor_light_?;+s")
        for i in range(npc.getNumPaths()):
            np=npc.getPath(i)
            # Get the last character, and make it zero based:
            floor=int(np.getName()[-1:])-1
            self.floorIndicator[floor]=np
            if floor < self.numFloors:
                np.setColor(LIGHT_OFF_COLOR)
            else:
                np.hide()
        
        self.elevatorModel.reparentTo(self.elevatorNodePath)

        if self.mode == 'suit':
            # Add in a corporate icon
            self.cab = self.elevatorModel.find('**/elevator')
            cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
            dept = chr(self.track)
            if dept == 'c':
                corpIcon = cogIcons.find('**/CorpIcon').copyTo(self.cab)
            elif dept == 's':
                corpIcon = cogIcons.find('**/SalesIcon').copyTo(self.cab)
            elif dept == 'l':
                corpIcon = cogIcons.find('**/LegalIcon').copyTo(self.cab)
            elif dept == 'm':
                corpIcon = cogIcons.find('**/MoneyIcon').copyTo(self.cab)
            corpIcon.setPos(0,6.79,6.8)
            corpIcon.setScale(3)
            from toontown.suit import Suit
            corpIcon.setColor(Suit.Suit.medallionColors[dept])
            cogIcons.removeNode()
        
        self.leftDoor = self.elevatorModel.find("**/left-door")
        self.rightDoor = self.elevatorModel.find("**/right-door")
        
        # Find the door origin
        self.suitDoorOrigin = newNP.find("**/*_door_origin")
        assert(not self.suitDoorOrigin.isEmpty())
        
        # Put the elevator under the door origin
        self.elevatorNodePath.reparentTo(self.suitDoorOrigin)
        self.normalizeElevator()
        return

    def loadAnimToSuitSfx(self):
        """loadAnimToSuitSfx(self)
        Loads up the sound effects necessary for the animToSuit effect.
        """
        if self.cogDropSound == None:
            self.cogDropSound = base.loadSfx(self.TAKEOVER_SFX_PREFIX + "cogbldg_drop.mp3")
            self.cogLandSound = base.loadSfx(self.TAKEOVER_SFX_PREFIX + "cogbldg_land.mp3")
            self.cogSettleSound = base.loadSfx(self.TAKEOVER_SFX_PREFIX + "cogbldg_settle.mp3")
            self.openSfx = base.loadSfx("phase_5/audio/sfx/elevator_door_open.mp3")

    def loadAnimToToonSfx(self):
        """loadAnimToToonSfx(self)
        Loads up the sound effects necessary for the animToToon effect.
        """
        if self.cogWeakenSound == None:
            self.cogWeakenSound = base.loadSfx(self.TAKEOVER_SFX_PREFIX + "cogbldg_weaken.mp3")
            self.toonGrowSound = base.loadSfx(self.TAKEOVER_SFX_PREFIX + "toonbldg_grow.mp3")
            self.toonSettleSound = base.loadSfx(self.TAKEOVER_SFX_PREFIX + "toonbldg_settle.mp3")
            self.openSfx = base.loadSfx("phase_5/audio/sfx/elevator_door_open.mp3")

    def unloadSfx(self):
        """unloadSfx(self)
        Unloads any sound effects that may have been loaded.
        """
        if self.cogDropSound != None:
            self.cogDropSound = None
            self.cogLandSound = None
            self.cogSettleSound = None
            self.openSfx = None
            
        if self.cogWeakenSound != None:
            self.cogWeakenSound = None
            self.toonGrowSound = None
            self.toonSettleSound = None
            self.openSfx = None
        
    def _deleteTransitionTrack(self):
        if self.transitionTrack:
            DelayDelete.cleanupDelayDeletes(self.transitionTrack)
            self.transitionTrack = None

    def animToSuit(self, timeStamp):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   create the multitrack that contains the animation
        //             sequence to transition this building from a toon to
        //             suit building
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        assert(self.debugPrint("animToSuit(timeStamp=%s)"%(timeStamp,)))
        self.stopTransition()
        if self.mode != 'toon':
            self.setToToon()
        self.loadAnimToSuitSfx()
        
        # first find the side building portions
        #
        sideBldgNodes = self.getNodePaths()

        # now find and position the landmark portion of the suit building
        # Copy the suit landmark building, based on suit track & difficulty:
        #
        nodePath=hidden.find(self.getSbSearchString())
        assert(not nodePath.isEmpty())
        newNP = self.setupSuitBuilding(nodePath)
        # Make sure the doors are closed for now.
        closeDoors(self.leftDoor, self.rightDoor)
        newNP.stash()
        sideBldgNodes.append(newNP)

        # create intervals to position and/or hide/stash the building parts
        # depending if it is part of the toon or suit version
        #
        soundPlayed = 0  # don't want to play sound for every part 
        tracks = Parallel(name = self.taskName('toSuitTrack'))
        for i in sideBldgNodes:
            name=i.getName()
            timeForDrop = TO_SUIT_BLDG_TIME*0.85
            if (name[0]=='s'):
                #print 'anim2suit: suit flat scale: %s' % repr(i.getScale())
                # set the position of the node, then unstash it to show it
                showTrack = Sequence(
                    name = self.taskName('ToSuitFlatsTrack') +
                    '-' + str(sideBldgNodes.index(i)))
                initPos = Point3(0, 0, self.SUIT_INIT_HEIGHT) + \
                          i.getPos()
                showTrack.append(Func(i.setPos, initPos))
                showTrack.append(Func(i.unstash))

                # Assumption: The last item on sideBldgNodes is actually
                # the landmark bldg itself.
                if i == sideBldgNodes[len(sideBldgNodes) - 1]:
                    showTrack.append(Func(self.normalizeElevator))
                #print "moving suit bldg part from %s to %s"%(str(initPos),
                #                                             str(i.getPos()))
                if not soundPlayed:
                    showTrack.append(Func(
                        base.playSfx, self.cogDropSound, 0, 1, None, 0.))
                showTrack.append(LerpPosInterval(
                    i, timeForDrop,
                    i.getPos(), name = self.taskName('ToSuitAnim') + '-' +
                    str(sideBldgNodes.index(i))))
                if not soundPlayed:
                    showTrack.append(Func(
                        base.playSfx, self.cogLandSound, 0, 1, None, 0.))
                showTrack.append(self.createBounceTrack(
                    i, 2, 0.65,
                    TO_SUIT_BLDG_TIME-timeForDrop,
                    slowInitBounce=1.0))
                if not soundPlayed:
                    showTrack.append(Func(
                        base.playSfx, self.cogSettleSound, 0, 1, None, 0.))
                tracks.append(showTrack)
                
                if not soundPlayed:
                    soundPlayed = 1
                #print "moving suit flat from %s to %s"%(str(initPos),
                #                                        str(i.getPos()))
                # lerp the alpha in for the building part, making sure to
                # remove the transparency transition when the fade is done
                # CCC is it ok if we have this other track also manipulate
                # the same building flat as the previously created track?
                # I know this can be an issue if the flat is removed, but
                # that should not happen in this multi-track
                #
                #showTrack = Sequence()
                #showTrack.append(Func(i.setTransparency, 1))
                #showTrack.append(LerpFunctionInterval(
                #    i.setAlphaScale, fromData=0, toData=1,
                #    duration=TO_SUIT_BLDG_TIME*0.20))
                #showTrack.append(FunctionInterval(i.clearTransparency))
                #tracks.append(showTrack)

            elif (name[0]=='t'):
                hideTrack = Sequence(
                    name = self.taskName('ToSuitToonFlatsTrack'))
                # figure how long till the toon building will start to be
                # compressed by the suit building coming down on it
                #
                timeTillSquish = (self.SUIT_INIT_HEIGHT - 20.0) / \
                                 self.SUIT_INIT_HEIGHT
                timeTillSquish *= timeForDrop
                #hideTrack.append(Wait(timeTillSquish))
                hideTrack.append(LerpFunctionInterval(
                    self.adjustColorScale, fromData=1,
                    toData=0.25,
                    duration=timeTillSquish,
                    extraArgs=[i]))
                hideTrack.append(LerpScaleInterval(
                    i, timeForDrop-timeTillSquish,
                    Vec3(1, 1, 0.01)))
                hideTrack.append(Func(i.stash))
                hideTrack.append(Func(i.setScale, Vec3(1)))
                hideTrack.append(Func(i.clearColorScale))
                tracks.append(hideTrack)

        # bundle up all of our tracks for the entire transition and start
        # playing
        #
        self.stopTransition()
        self._deleteTransitionTrack()
        self.transitionTrack = tracks
        
        #print "transitionTrack: %s" % self.transitionTrack
        #print "starting track at %s" % globalClock.getFrameTime()
        self.transitionTrack.start(timeStamp)
    
    def setupSuitBuilding(self, nodePath):
        assert(self.debugPrint("setupSuitBuilding(nodePath=%s)"%(nodePath,)))
        dnaStore=self.cr.playGame.dnaStore
        level = int(self.difficulty / 2) + 1
        suitNP=dnaStore.findNode("suit_landmark_"
                +chr(self.track)+str(level))

        # If you want to make the suit buildings visible from a
        # distance, uncomment the following line, and comment out
        # the three lines under it.
        #suitBuildingNP=suitNP.copyTo(self.townTopLevel)
        zoneId = dnaStore.getZoneFromBlockNumber(self.block)
        zoneId = ZoneUtil.getTrueZoneId(zoneId, self.interiorZoneId)
        newParentNP = base.cr.playGame.hood.loader.zoneDict[zoneId]
        suitBuildingNP = suitNP.copyTo(newParentNP)

        # Setup the sign:
        buildingTitle = dnaStore.getTitleFromBlockNumber(self.block)
        if not buildingTitle:
            buildingTitle = TTLocalizer.CogsInc
        else:
            buildingTitle += TTLocalizer.CogsIncExt
        buildingTitle += ("\n%s" % SuitDNA.getDeptFullname(chr(self.track)))
        
        # Try to find this signText in the node map
        textNode = TextNode("sign")
        textNode.setTextColor(1.0, 1.0, 1.0, 1.0)
        textNode.setFont(ToontownGlobals.getSuitFont())
        textNode.setAlign(TextNode.ACenter)
        textNode.setWordwrap(17.0)
        textNode.setText(buildingTitle)

        # Since the text is wordwrapped, it may flow over more
        # than one line.  Try to adjust the scale and position of
        # the sign accordingly.
        textHeight = textNode.getHeight()
        zScale = (textHeight + 2) / 3.0
        
        # Determine where the sign should go:
        signOrigin=suitBuildingNP.find("**/sign_origin;+s")
        assert(not signOrigin.isEmpty())
        # Get the background:
        backgroundNP=loader.loadModel("phase_5/models/modules/suit_sign")
        assert(not backgroundNP.isEmpty())
        backgroundNP.reparentTo(signOrigin)
        backgroundNP.setPosHprScale(0.0, 0.0, textHeight * 0.8 / zScale,
                                    0.0, 0.0, 0.0,
                                    8.0, 8.0, 8.0 * zScale)
        backgroundNP.node().setEffect(DecalEffect.make())
        # Get the text node path:
        signTextNodePath = backgroundNP.attachNewNode(textNode.generate())
        assert(not signTextNodePath.isEmpty())
        # Scale the text:
        signTextNodePath.setPosHprScale(0.0, 0.0, -0.21 + textHeight * 0.1 / zScale,
                                        0.0, 0.0, 0.0,
                                        0.1, 0.1, 0.1 / zScale)
        # Clear parent color higher in the hierarchy
        signTextNodePath.setColor(1.0, 1.0, 1.0, 1.0)
        # Decal sign onto the front of the building:
        frontNP = suitBuildingNP.find("**/*_front/+GeomNode;+s")
        assert(not frontNP.isEmpty())
        backgroundNP.wrtReparentTo(frontNP)
        frontNP.node().setEffect(DecalEffect.make())

        # Rename the building:
        suitBuildingNP.setName("sb"+str(self.block)+":_landmark__DNARoot")
        suitBuildingNP.setPosHprScale(nodePath,
                                      0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0,
                                      1.0, 1.0, 1.0)
        # Get rid of any transitions and extra nodes
        suitBuildingNP.flattenMedium()
        self.loadElevator(suitBuildingNP)
        return suitBuildingNP
    
    def cleanupSuitBuilding(self):
        if hasattr(self, "floorIndicator"):
            del self.floorIndicator

    def adjustColorScale(self, scale, node):
        node.setColorScale(scale, scale, scale, 1)

    def animToCogdo(self, timeStamp):
        assert(self.debugPrint("animToCogdo(timeStamp=%s)"%(timeStamp,)))
        self.stopTransition()
        if self.mode != 'toon':
            self.setToToon()
        self.loadAnimToSuitSfx()
        
        # first find the side building portions
        #
        sideBldgNodes = self.getNodePaths()

        # now find and position the landmark portion of the cogdo building
        # Copy the cogdo landmark building, based on difficulty:
        #
        nodePath=hidden.find(self.getSbSearchString())
        assert(not nodePath.isEmpty())
        newNP = self.setupCogdo(nodePath)
        # Make sure the doors are closed for now.
        closeDoors(self.leftDoor, self.rightDoor)
        newNP.stash()
        sideBldgNodes.append(newNP)

        for np in sideBldgNodes:
            if not np.isEmpty():
                np.setColorScale(.6,.6,.6,1.)

        # create intervals to position and/or hide/stash the building parts
        # depending if it is part of the toon or cogdo version
        #
        soundPlayed = 0  # don't want to play sound for every part 
        tracks = Parallel(name = self.taskName('toCogdoTrack'))
        for i in sideBldgNodes:
            name=i.getName()
            timeForDrop = TO_SUIT_BLDG_TIME*0.85
            if (name[0]=='s'):
                #print 'anim2suit: suit flat scale: %s' % repr(i.getScale())
                # set the position of the node, then unstash it to show it
                showTrack = Sequence(
                    name = self.taskName('ToCogdoFlatsTrack') +
                    '-' + str(sideBldgNodes.index(i)))
                initPos = Point3(0, 0, self.SUIT_INIT_HEIGHT) + \
                          i.getPos()
                showTrack.append(Func(i.setPos, initPos))
                showTrack.append(Func(i.unstash))

                # Assumption: The last item on sideBldgNodes is actually
                # the landmark bldg itself.
                if i == sideBldgNodes[len(sideBldgNodes) - 1]:
                    showTrack.append(Func(self.normalizeElevator))
                #print "moving suit bldg part from %s to %s"%(str(initPos),
                #                                             str(i.getPos()))
                if not soundPlayed:
                    showTrack.append(Func(
                        base.playSfx, self.cogDropSound, 0, 1, None, 0.))
                showTrack.append(LerpPosInterval(
                    i, timeForDrop,
                    i.getPos(), name = self.taskName('ToCogdoAnim') + '-' +
                    str(sideBldgNodes.index(i))))
                if not soundPlayed:
                    showTrack.append(Func(
                        base.playSfx, self.cogLandSound, 0, 1, None, 0.))
                showTrack.append(self.createBounceTrack(
                    i, 2, 0.65,
                    TO_SUIT_BLDG_TIME-timeForDrop,
                    slowInitBounce=1.0))
                if not soundPlayed:
                    showTrack.append(Func(
                        base.playSfx, self.cogSettleSound, 0, 1, None, 0.))
                tracks.append(showTrack)
                
                if not soundPlayed:
                    soundPlayed = 1
                #print "moving suit flat from %s to %s"%(str(initPos),
                #                                        str(i.getPos()))
                # lerp the alpha in for the building part, making sure to
                # remove the transparency transition when the fade is done
                # CCC is it ok if we have this other track also manipulate
                # the same building flat as the previously created track?
                # I know this can be an issue if the flat is removed, but
                # that should not happen in this multi-track
                #
                #showTrack = Sequence()
                #showTrack.append(Func(i.setTransparency, 1))
                #showTrack.append(LerpFunctionInterval(
                #    i.setAlphaScale, fromData=0, toData=1,
                #    duration=TO_SUIT_BLDG_TIME*0.20))
                #showTrack.append(FunctionInterval(i.clearTransparency))
                #tracks.append(showTrack)

            elif (name[0]=='t'):
                hideTrack = Sequence(
                    name = self.taskName('ToCogdoToonFlatsTrack'))
                # figure how long till the toon building will start to be
                # compressed by the cogdo coming down on it
                #
                timeTillSquish = (self.SUIT_INIT_HEIGHT - 20.0) / \
                                 self.SUIT_INIT_HEIGHT
                timeTillSquish *= timeForDrop
                #hideTrack.append(Wait(timeTillSquish))
                hideTrack.append(LerpFunctionInterval(
                    self.adjustColorScale, fromData=1,
                    toData=0.25,
                    duration=timeTillSquish,
                    extraArgs=[i]))
                hideTrack.append(LerpScaleInterval(
                    i, timeForDrop-timeTillSquish,
                    Vec3(1, 1, 0.01)))
                hideTrack.append(Func(i.stash))
                hideTrack.append(Func(i.setScale, Vec3(1)))
                hideTrack.append(Func(i.clearColorScale))
                tracks.append(hideTrack)

        # bundle up all of our tracks for the entire transition and start
        # playing
        #
        self.stopTransition()
        self._deleteTransitionTrack()
        self.transitionTrack = tracks
        
        #print "transitionTrack: %s" % self.transitionTrack
        #print "starting track at %s" % globalClock.getFrameTime()
        self.transitionTrack.start(timeStamp)

    def setupCogdo(self, nodePath):
        assert(self.debugPrint("setupCogdo(nodePath=%s)"%(nodePath,)))
        dnaStore=self.cr.playGame.dnaStore
        level = int(self.difficulty / 2) + 1
        suitNP=dnaStore.findNode("suit_landmark_"
                +'s'+str(level))

        # If you want to make the suit buildings visible from a
        # distance, uncomment the following line, and comment out
        # the three lines under it.
        #suitBuildingNP=suitNP.copyTo(self.townTopLevel)
        zoneId = dnaStore.getZoneFromBlockNumber(self.block)
        zoneId = ZoneUtil.getTrueZoneId(zoneId, self.interiorZoneId)
        newParentNP = base.cr.playGame.hood.loader.zoneDict[zoneId]
        suitBuildingNP = suitNP.copyTo(newParentNP)

        # Setup the sign:
        buildingTitle = dnaStore.getTitleFromBlockNumber(self.block)
        if not buildingTitle:
            buildingTitle = TTLocalizer.Cogdominiums
        else:
            buildingTitle += TTLocalizer.CogdominiumsExt
        
        # Try to find this signText in the node map
        textNode = TextNode("sign")
        textNode.setTextColor(1.0, 1.0, 1.0, 1.0)
        textNode.setFont(ToontownGlobals.getSuitFont())
        textNode.setAlign(TextNode.ACenter)
        textNode.setWordwrap(17.0)
        textNode.setText(buildingTitle)

        # Since the text is wordwrapped, it may flow over more
        # than one line.  Try to adjust the scale and position of
        # the sign accordingly.
        textHeight = textNode.getHeight()
        zScale = (textHeight + 2) / 3.0
        
        # Determine where the sign should go:
        signOrigin=suitBuildingNP.find("**/sign_origin;+s")
        assert(not signOrigin.isEmpty())
        # Get the background:
        backgroundNP=loader.loadModel("phase_5/models/modules/suit_sign")
        assert(not backgroundNP.isEmpty())
        backgroundNP.reparentTo(signOrigin)
        backgroundNP.setPosHprScale(0.0, 0.0, textHeight * 0.8 / zScale,
                                    0.0, 0.0, 0.0,
                                    8.0, 8.0, 8.0 * zScale)
        backgroundNP.node().setEffect(DecalEffect.make())
        # Get the text node path:
        signTextNodePath = backgroundNP.attachNewNode(textNode.generate())
        assert(not signTextNodePath.isEmpty())
        # Scale the text:
        signTextNodePath.setPosHprScale(0.0, 0.0, -0.21 + textHeight * 0.1 / zScale,
                                        0.0, 0.0, 0.0,
                                        0.1, 0.1, 0.1 / zScale)
        # Clear parent color higher in the hierarchy
        signTextNodePath.setColor(1.0, 1.0, 1.0, 1.0)
        # Decal sign onto the front of the building:
        frontNP = suitBuildingNP.find("**/*_front/+GeomNode;+s")
        assert(not frontNP.isEmpty())
        backgroundNP.wrtReparentTo(frontNP)
        frontNP.node().setEffect(DecalEffect.make())

        # Rename the building:
        suitBuildingNP.setName("sb"+str(self.block)+":_landmark__DNARoot")
        suitBuildingNP.setPosHprScale(nodePath,
                                      0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0,
                                      1.0, 1.0, 1.0)
        # Get rid of any transitions and extra nodes
        suitBuildingNP.flattenMedium()
        suitBuildingNP.setColorScale(.6,.6,.6,1.)
        self.loadElevator(suitBuildingNP)
        return suitBuildingNP

    def animToToon(self, timeStamp):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   create the multitrack that contains the animation
        //             sequence to transition this building from a suit to
        //             toon building
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # TODO: Incorporate the toons coming out of the elevator into
        # this multitrack. There will also need to be something like
        # exitCompleted...
        self.stopTransition()
        if self.mode != 'suit':
            self.setToSuit()

        self.loadAnimToToonSfx()

        # create intervals to position and/or hide/stash the building parts
        # depending if it is part of the toon or suit version
        #
        suitSoundPlayed = 0 # don't want to play sound for every part
        toonSoundPlayed = 0 # don't want to play sound for every part        
        bldgNodes = self.getNodePaths()
        tracks = Parallel()
        for i in bldgNodes:
            name=i.getName()
            if (name[0]=='s'):
                hideTrack = Sequence(
                    name = self.taskName('ToToonSuitFlatsTrack'))
                # have the suit building scale away
                #
                #origPos = i.getPos()
                #print "sidebldgpos: %s" % str(origPos)
                #tgtPos = Point3(
                #    Point3(0,0,-self.SUIT_INIT_HEIGHT) + \
                #    origPos)
                # shake the suit building on the x and y axis as it goes down
                #
                landmark = name.find("_landmark_") != -1
                #hideTrack.append(LerpPosInterval(
                #    i, TO_TOON_BLDG_TIME,
                #    tgtPos, name = self.taskName('ToToonAnim')))
                #hideTrack.append(LerpFunctionInterval(
                #    self.shakePart,
                #    extraArgs=[i,landmark,
                #               origPos.getX(),origPos.getY()]))
                #print 'anim2toon: suit flat scale: %s' % repr(i.getScale())
                if not suitSoundPlayed:
                    hideTrack.append(Func(
                        base.playSfx, self.cogWeakenSound, 0, 1, None, 0.))
                hideTrack.append(self.createBounceTrack(
                    i, 3, 1.2, TO_TOON_BLDG_TIME*0.05,
                    slowInitBounce=0.0))
                hideTrack.append(self.createBounceTrack(
                    i, 5, 0.8, TO_TOON_BLDG_TIME*0.10,
                    slowInitBounce=0.0))
                hideTrack.append(self.createBounceTrack(
                    i, 7, 1.2, TO_TOON_BLDG_TIME*0.17,
                    slowInitBounce=0.0))
                hideTrack.append(self.createBounceTrack(
                    i, 9, 1.2, TO_TOON_BLDG_TIME*0.18,
                    slowInitBounce=0.0))
                realScale = i.getScale()
                hideTrack.append(LerpScaleInterval(
                    i, TO_TOON_BLDG_TIME*0.10,
                    Vec3(realScale[0], realScale[1], 0.01)))
                if landmark:
                    # the landmark portion is recreated each time a suit
                    # building is generated, so we can just completely remove
                    # the node
                    #
                    hideTrack.append(Func(i.removeNode))
                else:
                    # make sure to relocate the suit building part to its
                    # original position above the ground so when it is shown
                    # again it it in its original, correct location (or set
                    # the scale to 1, depending on how the toToon transition
                    # is implemented)
                    #
                    hideTrack.append(Func(i.stash))
                    #hideTrack.append(FunctionInterval(
                    #    i.setPos, extraArgs = [origPos]))
                    hideTrack.append(Func(i.setScale, Vec3(1)))
                if not suitSoundPlayed:
                    suitSoundPlayed = 1
                tracks.append(hideTrack)
            elif (name[0]=='t'):
                hideTrack = Sequence(
                    name = self.taskName('ToToonFlatsTrack'))
                # show the toon portion of the building and set up the
                # transparency transition so we can slowly fade it in
                #
                hideTrack.append(Wait(TO_TOON_BLDG_TIME*0.5))
                if not toonSoundPlayed:
                    hideTrack.append(Func(
                        base.playSfx, self.toonGrowSound, 0, 1, None, 0.))
                hideTrack.append(Func(i.unstash))
                hideTrack.append(Func(i.setScale, Vec3(1,1,0.01)))
                #hideTrack.append(Func(i.setTransparency, 1))
                # lerp the alpha in for the building part, making sure to
                # remove the transparency transition when the fade is done
                #
                #hideTrack.append(LerpFunctionInterval(
                #    i.setAlphaScale, fromData=0.15, toData=1,
                #    duration=TO_TOON_BLDG_TIME*0.25))
                #hideTrack.append(Func(i.clearTransparency))
                if not toonSoundPlayed:
                    hideTrack.append(Func(
                        base.playSfx, self.toonSettleSound, 0, 1, None, 0.))
                hideTrack.append(self.createBounceTrack(
                    i, 11, 1.2, TO_TOON_BLDG_TIME*0.5,
                    slowInitBounce=4.0))
                tracks.append(hideTrack)
                if not toonSoundPlayed:
                    toonSoundPlayed = 1

        # bundle up all of our tracks for the entire transition and start
        # playing
        #
        self.stopTransition()
        #self.transitionTrack = Parallel(tracks, self.taskName(
        #    'ToToonMTrack'))
        bldgMTrack = tracks

        #print "transitionTrack: %s" % self.transitionTrack
        #print "starting track at %s" % globalClock.getFrameTime()

        # TODO: integrate the toons running out of the building into
        # the multitrack. For now, Just plant them outside the elevator.
        localToonIsVictor = self.localToonIsVictor()

        if localToonIsVictor:
            camTrack = self.walkOutCameraTrack()

        victoryRunTrack, delayDeletes = self.getVictoryRunTrack()

        trackName = self.taskName('toToonTrack')
        self._deleteTransitionTrack()
        if localToonIsVictor:
            freedomTrack1 = Func(
                self.cr.playGame.getPlace().setState,
                "walk")
            freedomTrack2 = Func(
                base.localAvatar.d_setParent,
                ToontownGlobals.SPRender)
            
            self.transitionTrack = Parallel(camTrack,
                                            Sequence(victoryRunTrack,
                                                     bldgMTrack,
                                                     freedomTrack1,
                                                     freedomTrack2,
                                                     ),
                                            name = trackName)
        else:
            self.transitionTrack = Sequence(victoryRunTrack,
                                            bldgMTrack,
                                            name = trackName
                                            )

        self.transitionTrack.delayDeletes = delayDeletes

        if localToonIsVictor:
            self.transitionTrack.start(0)
        else:
            self.transitionTrack.start(timeStamp)

        return

    def animToToonFromCogdo(self, timeStamp):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   create the multitrack that contains the animation
        //             sequence to transition this building from a cogdo to
        //             toon building
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # TODO: Incorporate the toons coming out of the elevator into
        # this multitrack. There will also need to be something like
        # exitCompleted...
        self.stopTransition()
        if self.mode != 'cogdo':
            self.setToCogdo()

        self.loadAnimToToonSfx()

        # create intervals to position and/or hide/stash the building parts
        # depending if it is part of the toon or suit version
        #
        suitSoundPlayed = 0 # don't want to play sound for every part
        toonSoundPlayed = 0 # don't want to play sound for every part        
        bldgNodes = self.getNodePaths()
        tracks = Parallel()
        for i in bldgNodes:
            i.clearColorScale()
            name=i.getName()
            if (name[0]=='s'):
                hideTrack = Sequence(
                    name = self.taskName('ToToonCogdoFlatsTrack'))
                # have the suit building scale away
                #
                #origPos = i.getPos()
                #print "sidebldgpos: %s" % str(origPos)
                #tgtPos = Point3(
                #    Point3(0,0,-self.SUIT_INIT_HEIGHT) + \
                #    origPos)
                # shake the suit building on the x and y axis as it goes down
                #
                landmark = name.find("_landmark_") != -1
                #hideTrack.append(LerpPosInterval(
                #    i, TO_TOON_BLDG_TIME,
                #    tgtPos, name = self.taskName('ToToonAnim')))
                #hideTrack.append(LerpFunctionInterval(
                #    self.shakePart,
                #    extraArgs=[i,landmark,
                #               origPos.getX(),origPos.getY()]))
                #print 'anim2toon: suit flat scale: %s' % repr(i.getScale())
                if not suitSoundPlayed:
                    hideTrack.append(Func(
                        base.playSfx, self.cogWeakenSound, 0, 1, None, 0.))
                hideTrack.append(self.createBounceTrack(
                    i, 3, 1.2, TO_TOON_BLDG_TIME*0.05,
                    slowInitBounce=0.0))
                hideTrack.append(self.createBounceTrack(
                    i, 5, 0.8, TO_TOON_BLDG_TIME*0.10,
                    slowInitBounce=0.0))
                hideTrack.append(self.createBounceTrack(
                    i, 7, 1.2, TO_TOON_BLDG_TIME*0.17,
                    slowInitBounce=0.0))
                hideTrack.append(self.createBounceTrack(
                    i, 9, 1.2, TO_TOON_BLDG_TIME*0.18,
                    slowInitBounce=0.0))
                realScale = i.getScale()
                hideTrack.append(LerpScaleInterval(
                    i, TO_TOON_BLDG_TIME*0.10,
                    Vec3(realScale[0], realScale[1], 0.01)))
                if landmark:
                    # the landmark portion is recreated each time a suit
                    # building is generated, so we can just completely remove
                    # the node
                    #
                    hideTrack.append(Func(i.removeNode))
                else:
                    # make sure to relocate the suit building part to its
                    # original position above the ground so when it is shown
                    # again it it in its original, correct location (or set
                    # the scale to 1, depending on how the toToon transition
                    # is implemented)
                    #
                    hideTrack.append(Func(i.stash))
                    #hideTrack.append(FunctionInterval(
                    #    i.setPos, extraArgs = [origPos]))
                    hideTrack.append(Func(i.setScale, Vec3(1)))
                if not suitSoundPlayed:
                    suitSoundPlayed = 1
                tracks.append(hideTrack)
            elif (name[0]=='t'):
                hideTrack = Sequence(
                    name = self.taskName('ToToonFromCogdoFlatsTrack'))
                # show the toon portion of the building and set up the
                # transparency transition so we can slowly fade it in
                #
                hideTrack.append(Wait(TO_TOON_BLDG_TIME*0.5))
                if not toonSoundPlayed:
                    hideTrack.append(Func(
                        base.playSfx, self.toonGrowSound, 0, 1, None, 0.))
                hideTrack.append(Func(i.unstash))
                hideTrack.append(Func(i.setScale, Vec3(1,1,0.01)))
                #hideTrack.append(Func(i.setTransparency, 1))
                # lerp the alpha in for the building part, making sure to
                # remove the transparency transition when the fade is done
                #
                #hideTrack.append(LerpFunctionInterval(
                #    i.setAlphaScale, fromData=0.15, toData=1,
                #    duration=TO_TOON_BLDG_TIME*0.25))
                #hideTrack.append(Func(i.clearTransparency))
                if not toonSoundPlayed:
                    hideTrack.append(Func(
                        base.playSfx, self.toonSettleSound, 0, 1, None, 0.))
                hideTrack.append(self.createBounceTrack(
                    i, 11, 1.2, TO_TOON_BLDG_TIME*0.5,
                    slowInitBounce=4.0))
                tracks.append(hideTrack)
                if not toonSoundPlayed:
                    toonSoundPlayed = 1

        # bundle up all of our tracks for the entire transition and start
        # playing
        #
        self.stopTransition()
        #self.transitionTrack = Parallel(tracks, self.taskName(
        #    'ToToonMTrack'))
        bldgMTrack = tracks

        #print "transitionTrack: %s" % self.transitionTrack
        #print "starting track at %s" % globalClock.getFrameTime()

        # TODO: integrate the toons running out of the building into
        # the multitrack. For now, Just plant them outside the elevator.
        localToonIsVictor = self.localToonIsVictor()

        if localToonIsVictor:
            camTrack = self.walkOutCameraTrack()

        victoryRunTrack, delayDeletes = self.getVictoryRunTrack()

        trackName = self.taskName('toToonFromCogdoTrack')
        self._deleteTransitionTrack()
        if localToonIsVictor:
            freedomTrack1 = Func(
                self.cr.playGame.getPlace().setState,
                "walk")
            freedomTrack2 = Func(
                base.localAvatar.d_setParent,
                ToontownGlobals.SPRender)
            
            self.transitionTrack = Parallel(camTrack,
                                            Sequence(victoryRunTrack,
                                                     bldgMTrack,
                                                     freedomTrack1,
                                                     freedomTrack2,
                                                     ),
                                            name = trackName)
        else:
            self.transitionTrack = Sequence(victoryRunTrack,
                                            bldgMTrack,
                                            name = trackName
                                            )

        self.transitionTrack.delayDeletes = delayDeletes

        if localToonIsVictor:
            self.transitionTrack.start(0)
        else:
            self.transitionTrack.start(timeStamp)

        return

    def walkOutCameraTrack(self):
        track = Sequence(
            # Put the camera under render
            Func(camera.reparentTo, render),
            # Watch the toons come out of the door
            Func(camera.setPosHpr,
                 self.elevatorNodePath,
                 0, -32.5, 9.4, 0, 348, 0),
            Func(base.camLens.setFov, 52.0),
            Wait(VICTORY_RUN_TIME),
            # Watch the building transform
            Func(camera.setPosHpr,
                 self.elevatorNodePath,
                 0, -32.5, 17, 0, 347, 0),
            Func(base.camLens.setFov, 75.0),
            Wait(TO_TOON_BLDG_TIME),
            # Put the camera fov back to normal
            Func(base.camLens.setFov, 52.0),
            )
        return track

    def plantVictorsOutsideBldg(self):
        #print "planting Victors %s !" % self.victorList
        retVal = 0
        for victor in self.victorList:
            if victor != 0 and self.cr.doId2do.has_key(victor):
                toon = self.cr.doId2do[victor]
                toon.setPosHpr(self.elevatorModel, 0, -10, 0, 0, 0, 0)
                toon.startSmooth()
                if victor == base.localAvatar.getDoId():
                    retVal = 1
                    self.cr.playGame.getPlace().setState('walk')
        return retVal

    def getVictoryRunTrack(self):
        # Put each toon in the elevator
        origPosTrack = Sequence()
        delayDeletes = []
        i = 0
        for victor in self.victorList:
            if victor != 0 and self.cr.doId2do.has_key(victor):
                toon = self.cr.doId2do[victor]
                delayDeletes.append(DelayDelete.DelayDelete(toon, 'getVictoryRunTrack'))
                toon.stopSmooth()
                toon.setParent(ToontownGlobals.SPHidden)
                origPosTrack.append(Func(toon.setPosHpr,
                                         self.elevatorNodePath,
                                         apply(Point3, ElevatorPoints[i]),
                                         Point3(180, 0, 0)))
                origPosTrack.append(Func(toon.setParent,
                                         ToontownGlobals.SPRender))
            i += 1

        # Open the elevator doors
        openDoors = getOpenInterval(self, self.leftDoor, self.rightDoor,
                                    self.openSfx, None)

        # Run the toons out of the elevator
        runOutAll = Parallel()
        i = 0
        for victor in self.victorList:
            if victor != 0 and self.cr.doId2do.has_key(victor):
                toon = self.cr.doId2do[victor]
                p0 = Point3(0, 0, 0)
                p1 = Point3(ElevatorPoints[i][0],
                            ElevatorPoints[i][1] - 5.0,
                            ElevatorPoints[i][2])
                p2 = Point3(ElevatorOutPoints[i][0],
                            ElevatorOutPoints[i][1],
                            ElevatorOutPoints[i][2])
                
                runOutSingle = Sequence(
                    # Disallow body emotes so we don't slide
                    Func(Emote.globalEmote.disableBody, toon, "getVictory"),
                    # Start the run animation
                    Func(toon.animFSM.request, "run"),
                    # Move the toon out of the elevator
                    LerpPosInterval(toon, TOON_VICTORY_EXIT_TIME * 0.25,
                                    p1, other=self.elevatorNodePath),
                    # Run him from there to his observation point
                    Func(toon.headsUp, self.elevatorNodePath, p2),
                    LerpPosInterval(toon, TOON_VICTORY_EXIT_TIME * 0.50,
                                    p2, other=self.elevatorNodePath),
                    # Turn the toon around to face the building
                    LerpHprInterval(toon, TOON_VICTORY_EXIT_TIME * 0.25,
                                    Point3(0, 0, 0),
                                    other=self.elevatorNodePath),
                    # Stop the toon from running
                    Func(toon.animFSM.request, "neutral"),
                    # Free the toon up to walk around on his own again
                    Func(toon.startSmooth),
                    Func(Emote.globalEmote.releaseBody, toon, "getVictory"),
                    )
                runOutAll.append(runOutSingle)
            i += 1
                
        victoryRunTrack = Sequence(origPosTrack,
                                   openDoors,
                                   runOutAll,
                                   )
        
        return (victoryRunTrack, delayDeletes)
                    
    def localToonIsVictor(self):
        retVal = 0
        for victor in self.victorList:
            if victor == base.localAvatar.getDoId():
                retVal = 1
        return retVal

    def createBounceTrack(self, nodeObj, numBounces, startScale,
                          totalTime, slowInitBounce=0.0):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        if not nodeObj or numBounces < 1 or \
           startScale == 0.0 or totalTime == 0:
            self.notify.warning(
                "createBounceTrack called with invalid parameter")
            return
        
        # add an extra bounce to make sure the object
        # is properly scaled to 1 on the last lerpScaleInterval
        #
        result = Sequence()
        numBounces+=1
        
        # calculate how long, in seconds, each bounce should last, make
        # the time of each bounce smaller if we want to extend the length
        # the initial bounce
        #
        if slowInitBounce:
            bounceTime = totalTime/(numBounces + slowInitBounce - 1.0)
        else:
            bounceTime = totalTime/float(numBounces)

        # if specified, the first bounce lasts the length of 3 bounces,
        # useful for when initially appearing, the first bounce of the
        # object is more pronounced than the others
        #
        if slowInitBounce:
            currTime = bounceTime * float(slowInitBounce)
        else:
            currTime = bounceTime

        # determine the how much of a change in scale the first bounce
        # will produce based on the node's base scale (current scale)
        # and the given start scale
        #
        realScale = nodeObj.getScale()
        currScaleDiff = startScale - realScale[2]

        # create a lerpScaleInterval for each bounce, making sure to
        # figure out the new scale, which progressively gets closer
        # to our base scale
        #
        for currBounceScale in range(numBounces):
            # determine the direction that this scale should go,
            # alternating for each lerpScaleInterval to simulate
            # a spring effect
            # 
            if currBounceScale == numBounces-1:
                currScale = realScale[2]
            elif currBounceScale%2:
                currScale = realScale[2] - currScaleDiff
            else:
                currScale = realScale[2] + currScaleDiff
            result.append(LerpScaleInterval(
                nodeObj, currTime,
                Vec3(realScale[0], realScale[1], currScale),
                blendType='easeInOut'))

            # the scale diff from the base gets smaller for each
            # consecutive bounce, and make sure to update for
            # possibly a new amount of time the next bounce will
            # take
            #
            currScaleDiff *= 0.5
            currTime = bounceTime

        return result

    def stopTransition(self):
        if self.transitionTrack:
            self.transitionTrack.finish()
            self._deleteTransitionTrack()
        
    def setToSuit(self):
        assert(self.debugPrint("setToSuit()"))
        self.stopTransition()
        if self.mode == 'suit':
            return
        self.mode = 'suit'
        
        nodes=self.getNodePaths()
        for i in nodes:
            name=i.getName()
            if (name[0]=='s'):
                if (name.find("_landmark_") != -1):
                    # an old suit landmark instance.
                    i.removeNode()
                else:
                    # Suit flat buildings:
                    # i.show()
                    i.unstash()
            elif (name[0]=='t'):
                if (name.find("_landmark_") != -1):
                    # Toon landmark buildings:
                    i.stash()
                else:
                    # Toon flat buildings:
                    # i.hide()
                    i.stash()

        # Copy the suit landmark building, based on the suit track and
        # difficulty:
        npc=hidden.findAllMatches(self.getSbSearchString())
        
        assert(npc.getNumPaths()>0)
        for i in range(npc.getNumPaths()):
            nodePath=npc.getPath(i)
            self.adjustSbNodepathScale(nodePath)
            self.notify.debug("net transform = %s" % str(nodePath.getNetTransform()))
            self.setupSuitBuilding(nodePath)
    
    def setToCogdo(self):
        assert(self.debugPrint("setToCogdo()"))
        self.stopTransition()
        if self.mode == 'cogdo':
            return
        self.mode = 'cogdo'
        
        nodes=self.getNodePaths()
        for i in nodes:
            name=i.getName()
            if (name[0]=='s'):
                if (name.find("_landmark_") != -1):
                    # an old suit landmark instance.
                    i.removeNode()
                else:
                    # Suit flat buildings:
                    # i.show()
                    i.unstash()
            elif (name[0]=='t'):
                if (name.find("_landmark_") != -1):
                    # Toon landmark buildings:
                    i.stash()
                else:
                    # Toon flat buildings:
                    # i.hide()
                    i.stash()

        for np in nodes:
            if not np.isEmpty():
                np.setColorScale(.6,.6,.6,1.)

        # Copy the suit landmark building, based on the suit track and
        # difficulty:
        npc=hidden.findAllMatches(self.getSbSearchString())
        
        assert(npc.getNumPaths()>0)
        for i in range(npc.getNumPaths()):
            nodePath=npc.getPath(i)
            self.adjustSbNodepathScale(nodePath)
            self.notify.debug("net transform = %s" % str(nodePath.getNetTransform()))
            self.setupCogdo(nodePath)
    
    def setToToon(self):
        assert(self.debugPrint("setToToon() mode=%s" % (self.mode)))
        self.stopTransition()
        if self.mode == 'toon':
            return
        self.mode = 'toon'
        
        # Clear reference to the suit door.
        self.suitDoorOrigin = None
        # Go through nodes, and do the right thing.
        nodes=self.getNodePaths()
        for i in nodes:
            i.clearColorScale()
            name=i.getName()
            if (name[0]=='s'):
                if (name.find("_landmark_") != -1):
                    i.removeNode()
                else:
                    # Suit flat buildings:
                    # i.hide()
                    i.stash()
            elif (name[0]=='t'):
                if (name.find("_landmark_") != -1):
                    # Toon landmark buildings:
                    i.unstash()
                else:
                    # Toon flat buildings:
                    # i.show()
                    i.unstash()
                        
    def normalizeElevator(self):
        # Normalize the size of the elevator
        # The suit building probably has a funny scale on it,
        # but by doing this, we normalize the scale on the elevator.
        self.elevatorNodePath.setScale(render, Vec3(1, 1, 1))
        self.elevatorNodePath.setPosHpr(0, 0, 0, 0, 0, 0)
        return
    
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('block', '?'))+' '+message)

    def getSbSearchString(self):
        """Return a string to use when looking for the suit building nodepath."""
        result = "landmarkBlocks/sb" + str(self.block) + \
                 ":*_landmark_*_DNARoot"
        return result

    def adjustSbNodepathScale(self, nodePath):
        """Animated buildings needs a scale hack, this does nothing for reg bldg."""
        pass

    def getVisZoneId(self):
        """Retur our visibible Zone Id."""
        # this computation is taken from DistributedBuildingMgrAI
        exteriorZoneId = base.cr.playGame.hood.dnaStore.getZoneFromBlockNumber(self.block)
        visZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.zoneId)
        return visZoneId

    def getInteractiveProp(self):
        """Get our associated interactive prop, if any."""
        result = None
        if self.interactiveProp:
            result = self.interactiveProp
        else:
            visZoneId = self.getVisZoneId()
            if base.cr.playGame.hood:
                loader = base.cr.playGame.hood.loader
                if hasattr(loader,"getInteractiveProp"):
                    self.interactiveProp = loader.getInteractiveProp(visZoneId)
                    result = self.interactiveProp
                    self.notify.debug("self.interactiveProp = %s" % self.interactiveProp)
                else:
                   self.notify.warning("no loader.getInteractiveProp self.interactiveProp is None")
            else:
               self.notify.warning("no hood self.interactiveProp is None")        
        return result


    def makePropSad(self):
        """Make an interactive prop near us be sad when we're a cog building."""
        self.notify.debug("makePropSad")
        if self.getInteractiveProp():
            if self.getInteractiveProp().state == "Sad":
                #import pdb; pdb.set_trace()
                pass
            self.getInteractiveProp().gotoSad(self.doId)

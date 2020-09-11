"""TownLoader module: contains the TownLoader class"""

from pandac.PandaModules import *
from toontown.battle.BattleProps import *
from toontown.battle.BattleSounds import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import cleanupDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import TownBattle
from toontown.toon import Toon
from toontown.battle import BattleParticles
from direct.fsm import StateData
from toontown.building import ToonInterior
from toontown.hood import QuietZoneState
from toontown.hood import ZoneUtil
from direct.interval.IntervalGlobal import *

class TownLoader(StateData.StateData):
    """
    TownLoader class
    """

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("TownLoader")
    
    # special methods

    def __init__(self, hood, parentFSMState, doneEvent):
        """
        TownLoader constructor: create a play game ClassicFSM
        """
        assert self.notify.debug("__init__()")
        StateData.StateData.__init__(self, doneEvent)
        self.hood=hood
        self.parentFSMState = parentFSMState
        self.fsm = ClassicFSM.ClassicFSM('TownLoader',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['quietZone', 'street', 'toonInterior']),
                            State.State('street',
                                        self.enterStreet,
                                        self.exitStreet,
                                        ['quietZone']),
                            State.State('toonInterior',
                                        self.enterToonInterior,
                                        self.exitToonInterior,
                                        ['quietZone']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['street', 'toonInterior']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )
        self.branchZone = None        
        self.canonicalBranchZone = None        
        self.placeDoneEvent = "placeDone"
        self.townBattleDoneEvent = 'town-battle-done'

    def loadBattleAnims(self):
        # These are here so the tutorial can overwrite them
        Toon.loadBattleAnims()

    def unloadBattleAnims(self):
        # These are here so the tutorial can overwrite them
        Toon.unloadBattleAnims()

    def load(self, zoneId):
        assert self.notify.debug("load()")

        # We'll need to know this to rename the visibility zones
        # correctly.
        self.zoneId = zoneId
        
        # Prepare the state machine
        self.parentFSMState.addChild(self.fsm)
        # load Toon battle anims and props
        self.loadBattleAnims()
        # props loaded on the fly now
        #globalPropPool.loadProps()     
        # TODO: Based on the zone id, load that branch
        self.branchZone = ZoneUtil.getBranchZone(zoneId)
        self.canonicalBranchZone = ZoneUtil.getCanonicalBranchZone(zoneId)
        # Load the music:
        self.music = base.loadMusic(self.musicFile)
        self.activityMusic = base.loadMusic(self.activityMusicFile)
        self.battleMusic = base.loadMusic(
                'phase_3.5/audio/bgm/encntr_general_bg.mid')
        # Load the battle UI:
        self.townBattle = TownBattle.TownBattle(self.townBattleDoneEvent)
        self.townBattle.load()

    def unload(self):
        assert self.notify.debug("unload()")
        # unload Toon battle anims and props
        self.unloadBattleAnims()
        globalPropPool.unloadProps()
        globalBattleSoundCache.clear()
        BattleParticles.unloadParticles()
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        del self.fsm
        del self.streetClass
        self.landmarkBlocks.removeNode()
        del self.landmarkBlocks
        # Clear out the old neighborhoods suit points
        self.hood.dnaStore.resetSuitPoints()
        # Clear out the battle cells
        self.hood.dnaStore.resetBattleCells()
        del self.hood
        del self.nodeDict
        del self.zoneDict
        del self.fadeInDict
        del self.fadeOutDict
        del self.nodeList
        self.geom.removeNode()
        del self.geom
        self.townBattle.unload()
        self.townBattle.cleanup()
        del self.townBattle
        del self.battleMusic
        del self.music
        del self.activityMusic
        del self.holidayPropTransforms
        self.deleteAnimatedProps()
        # remove any dfa dialogs
        cleanupDialog("globalDialog")
        # Get rid of any references to models or textures from this town
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enter(self, requestStatus):
        assert self.notify.debug("enter(requestStatus="+str(requestStatus)+")")
        self.fsm.enterInitialState()
        self.setState(requestStatus["where"], requestStatus)

    def exit(self):
        assert self.notify.debug("exit()")
        self.ignoreAll()

    def setState(self, stateName, requestStatus):
        assert(self.notify.debug("setState(stateName="
                +str(stateName)+", requestStatus="+str(requestStatus)+")"))
        self.fsm.request(stateName, [requestStatus])

    # start state

    def enterStart(self):
        assert self.notify.debug("enterStart()")
        
    def exitStart(self):
        assert self.notify.debug("exitStart()")

    # street state

    def enterStreet(self, requestStatus):
        assert(self.notify.debug(
                "enterStreet(requestStatus="+str(requestStatus)+")"))
        self.acceptOnce(self.placeDoneEvent, self.streetDone)
        self.place=self.streetClass(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        #self.hood.place = self.place
        base.cr.playGame.setPlace(self.place)
        
        # The following call could actually take us out of the town
        # altogether, switching us out of street mode, unloading our
        # hood, and all the bad consequences that could go along with
        # that, if this is a teleport attempt to a toon who has moved
        # on.  It should therefore be the very last thing this
        # function does, because anything done after this call might
        # be invalid.
        self.place.enter(requestStatus)
        
    def exitStreet(self):
        assert self.notify.debug("exitStreet()")
        self.place.exit()
        self.place.unload()
        self.place=None
        #self.hood.place = self.place
        base.cr.playGame.setPlace(self.place)

    
    def streetDone(self):
        self.requestStatus=self.place.doneStatus
        assert(self.notify.debug(
                "streetDone() doneStatus="+str(self.requestStatus)))
        status=self.place.doneStatus
        # Check the loader, incase this is a change to a SuitInterior:
        if (status["loader"] == "townLoader" and
            ZoneUtil.getBranchZone(status["zoneId"]) == self.branchZone and
            status["shardId"] == None):
            self.fsm.request("quietZone", [status])            
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)

    # toonInterior state

    def enterToonInterior(self, requestStatus):
        assert self.notify.debug("enterToonInterior()")
        self.acceptOnce(self.placeDoneEvent, self.handleToonInteriorDone)
        self.place=ToonInterior.ToonInterior(self,
                                             self.fsm.getStateNamed("toonInterior"),
                                             self.placeDoneEvent)
        #self.hood.place = self.place 
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)
        
    def exitToonInterior(self):
        assert self.notify.debug("exitToonInterior()")
        self.ignore(self.placeDoneEvent)
        #self.hood.place = None
        self.place.exit()
        self.place.unload()
        self.place=None
        base.cr.playGame.setPlace(self.place)
    
    def handleToonInteriorDone(self):
        assert self.notify.debug("handleToonInteriorDone()")
        status=self.place.doneStatus
        if (ZoneUtil.getBranchZone(status["zoneId"]) == self.branchZone and
            status["shardId"] == None):
            self.fsm.request("quietZone", [status])            
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)

    # quietZone state

    def enterQuietZone(self, requestStatus):
        assert self.notify.debug("enterQuietZone()")
        self.quietZoneDoneEvent = "quietZoneDone"
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(
                self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        assert self.notify.debug("exitQuietZone()")
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData=None

    def handleQuietZoneDone(self):
        status=self.quietZoneStateData.getRequestStatus()
        assert(self.notify.debug("handleQuietZoneDone()\n  base.cr.handlerArgs="
                +str(status)))
        # Change to the destination state:
        self.fsm.request(status["where"], [status])

    # final state

    def enterFinal(self):
        assert self.notify.debug("enterFinal()")
    
    def exitFinal(self):
        assert self.notify.debug("exitFinal()")

    def createHood(self, dnaFile, loadStorage=1):
        assert self.notify.debug("createHood(dnaFile="+str(dnaFile)+")")
        # The tutorial does not use this
        if loadStorage:
            # Load the generic town storage if asked for
            loader.loadDNAFile(self.hood.dnaStore, "phase_5/dna/storage_town.dna")
            self.notify.debug("done loading %s" % "phase_5/dna/storage_town.dna")
            # Load the specific town storage
            loader.loadDNAFile(self.hood.dnaStore, self.townStorageDNAFile)
            self.notify.debug("done loading %s" % self.townStorageDNAFile)
        node = loader.loadDNAFile(self.hood.dnaStore, dnaFile)
        self.notify.debug("done loading %s" % dnaFile)

        if node.getNumParents() == 1:
            # If the node already has a parent arc when it's loaded, we must
            # be using the level editor and we want to preserve that arc.
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            # Otherwise, we should create a new arc for the node.
            self.geom = hidden.attachNewNode(node)

        # self.geom = hidden.attachNewNode(node)
        # Make the vis dictionaries
        self.makeDictionaries(self.hood.dnaStore)
        # Reparent Landmark block nodes:
        self.reparentLandmarkBlockNodes()
        # Rename the floor polys to have the same name as the
        # visgroup they are in... This makes visibility possible.
        self.renameFloorPolys(self.nodeList)
        self.createAnimatedProps(self.nodeList)
        # Record position of all holiday props before everything is flattened
        self.holidayPropTransforms = {}
        npl = self.geom.findAllMatches('**/=DNARoot=holiday_prop')
        for i in range(npl.getNumPaths()):
            np = npl.getPath(i)
            np.setTag('transformIndex', `i`)
            self.holidayPropTransforms[i] = np.getNetTransform()
        # Flatten the neighborhood
        #self.geom.flattenMedium()
        self.notify.info("skipping self.geom.flattenMedium")
        # Preload all textures in neighborhood
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)
        # Make a convenient search name for the town root
        self.geom.setName('town_top_level')

    def reparentLandmarkBlockNodes(self):
        """
        reparent the landmark block stub nodes into a 'bucket' under
        hidden.  We just use these for pos, hpr, and scale
        """
        assert self.notify.debug("reparentLandmarkBlockNodes()")
        bucket=self.landmarkBlocks=hidden.attachNewNode("landmarkBlocks")
        npc=self.geom.findAllMatches("**/sb*:*_landmark_*_DNARoot")
        for i in range(npc.getNumPaths()):
            nodePath=npc.getPath(i)
            nodePath.wrtReparentTo(bucket)
        npc=self.geom.findAllMatches("**/sb*:*animated_building*_DNARoot")
        for i in range(npc.getNumPaths()):
            nodePath=npc.getPath(i)
            nodePath.wrtReparentTo(bucket)  

    def makeDictionaries(self, dnaStore):
        """
        Extract the juicy bits from the dna, then unload as much as possible
        """
        assert self.notify.debug("makeDictionaries()")
        # A map of zone ID's to a list of nodes that are visible from
        # that zone.
        self.nodeDict = {}
        
        # A map of zone ID's to the particular node that corresponds
        # to that zone.
        self.zoneDict = {}
        
        # A list of all visible nodes
        self.nodeList = []

        self.fadeInDict = {}
        self.fadeOutDict = {}

        # NOTE: this should change to find the groupnodes in
        # the dna storage instead of searching through the tree

        # Colors for fading zones
        a1 = Vec4(1,1,1,1)
        a0 = Vec4(1,1,1,0)

        numVisGroups = dnaStore.getNumDNAVisGroups()
        for i in range(numVisGroups):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            groupName = base.cr.hoodMgr.extractGroupName(groupFullName)
            zoneId = int(groupName)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            
            groupNode = self.geom.find("**/" + groupFullName)
            if groupNode.isEmpty():
                self.notify.error("Could not find visgroup")
            else:
                # Temporary hack (to be replaced with tag interface):
                # mangle the name to put the modified zoneId back in,
                # but keep the extra flags following the zoneId.
                if ":" in groupName:
                    groupName = "%s%s" % (zoneId, groupName[groupName.index(":"):])
                else:
                    groupName = "%s" % (zoneId)
                groupNode.setName(groupName)

            self.nodeDict[zoneId] = []
            self.nodeList.append(groupNode)
            self.zoneDict[zoneId] = groupNode

            fadeDuration = 0.5

            self.fadeOutDict[groupNode] = Sequence(
                Func(groupNode.setTransparency, 1),
                LerpColorScaleInterval(groupNode, fadeDuration,
                                       a0, startColorScale = a1),
                Func(groupNode.clearColorScale),
                Func(groupNode.clearTransparency),
                Func(groupNode.stash),
                name = "fadeZone-" + str(zoneId),
                autoPause = 1)

            self.fadeInDict[groupNode] = Sequence(
                Func(groupNode.unstash),
                Func(groupNode.setTransparency, 1),
                LerpColorScaleInterval(groupNode, fadeDuration,
                                       a1, startColorScale = a0),
                Func(groupNode.clearColorScale),
                Func(groupNode.clearTransparency),
                name = "fadeZone-" + str(zoneId),
                autoPause = 1)

        # Now that all the zoneDict has been filled in, fill in the nodeDict
        for i in range(numVisGroups):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            zoneId = int(base.cr.hoodMgr.extractGroupName(groupFullName))
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            for j in range(dnaStore.getNumVisiblesInDNAVisGroup(i)):
                visName = dnaStore.getVisibleName(i, j)
                groupName = base.cr.hoodMgr.extractGroupName(visName)
                # visNode = self.geom.find("**/" + visName)
                nextZoneId = int(groupName)
                nextZoneId = ZoneUtil.getTrueZoneId(nextZoneId, self.zoneId)
                visNode = self.zoneDict[nextZoneId]
                self.nodeDict[zoneId].append(visNode)

        # Now that we have extracted the vis groups we do not need
        # the dnaStore to keep them around
        # Remove all references to the town specific models and textures
        self.hood.dnaStore.resetPlaceNodes()
        self.hood.dnaStore.resetDNAGroups()
        self.hood.dnaStore.resetDNAVisGroups()
        self.hood.dnaStore.resetDNAVisGroupsAI()       

    def renameFloorPolys(self, nodeList):
        assert self.notify.debug("renameFloorPolys()")
        for i in nodeList:
            # Get all the collision nodes in the vis group
            collNodePaths = i.findAllMatches("**/+CollisionNode")
            numCollNodePaths = collNodePaths.getNumPaths()
            visGroupName = i.node().getName()
            for j in range(numCollNodePaths):
                collNodePath = collNodePaths.getPath(j)
                bitMask = collNodePath.node().getIntoCollideMask()
                if bitMask.getBit(1):
                    # Bit 1 is the floor collision bit. This renames
                    # all floor collision polys to the same name as their
                    # visgroup.
                    collNodePath.node().setName(visGroupName)

    def createAnimatedProps(self, nodeList):
        assert self.notify.debug("createAnimatedProps()")
        self.animPropDict = {}
        self.zoneIdToInteractivePropDict = {}
        for i in nodeList:
            # Get all the anim in the vis group
            animPropNodes = i.findAllMatches("**/animated_prop_*")
            numAnimPropNodes = animPropNodes.getNumPaths()
            for j in range(numAnimPropNodes):
                animPropNode = animPropNodes.getPath(j)

                if animPropNode.getName().startswith('animated_prop_generic'):
                    className = 'GenericAnimatedProp'
                elif animPropNode.getName().startswith('animated_prop_'):
                    name = animPropNode.getName()[len('animated_prop_'):]
                    splits = name.split('_')
                    className = splits[0]
                else:
                    # The node name should be "animated_prop_ClassName_DNARoot"
                    # So strip off the first and last junk to get the ClassName
                    className = animPropNode.getName()[14:-8]
                    
                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])

                classObj = getattr(symbols[className], className)
                animPropObj = classObj(animPropNode)
                animPropList = self.animPropDict.setdefault(i, [])
                animPropList.append(animPropObj)
                

            interactivePropNodes = i.findAllMatches("**/interactive_prop_*")
            numInteractivePropNodes = interactivePropNodes.getNumPaths()
            for j in range(numInteractivePropNodes):
                interactivePropNode = interactivePropNodes.getPath(j)
                className = 'InteractiveAnimatedProp'
                if "hydrant" in interactivePropNode.getName():
                    className = "HydrantInteractiveProp"
                elif "trashcan" in interactivePropNode.getName():
                    className = "TrashcanInteractiveProp"
                elif "mailbox" in interactivePropNode.getName():
                    className = "MailboxInteractiveProp"

                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])

                classObj = getattr(symbols[className], className)
                interactivePropObj = classObj(interactivePropNode)
                # [gjeon] I think we can use animPropList to store interactive props
                animPropList = self.animPropDict.get(i)
                if animPropList is None:
                    animPropList = self.animPropDict.setdefault(i, []) 
                animPropList.append(interactivePropObj)
                if interactivePropObj.getCellIndex() == 0:
                    zoneId = int(i.getName())
                    if not zoneId in self.zoneIdToInteractivePropDict:
                        self.zoneIdToInteractivePropDict[zoneId] = interactivePropObj
                    else:
                        self.notify.error("already have interactive prop %s in zone %s" %
                                          (self.zoneIdToInteractivePropDict, zoneId))
                    
            animatedBuildingNodes = i.findAllMatches("**/*:animated_building_*;-h")
            for np in animatedBuildingNodes:
                if np.getName().startswith('sb'):
                    animatedBuildingNodes.removePath(np)
                    
            numAnimatedBuildingNodes = animatedBuildingNodes.getNumPaths()
            for j in range(numAnimatedBuildingNodes):
                animatedBuildingNode = animatedBuildingNodes.getPath(j)
                className = 'GenericAnimatedBuilding'

                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])

                classObj = getattr(symbols[className], className)
                animatedBuildingObj = classObj(animatedBuildingNode)
                # [gjeon] I think we can use animPropList to store interactive props
                animPropList = self.animPropDict.get(i)
                if animPropList is None:
                    animPropList = self.animPropDict.setdefault(i, []) 
                animPropList.append(animatedBuildingObj)

    def deleteAnimatedProps(self):
        for zoneNode, animPropList in self.animPropDict.items():
            for animProp in animPropList:
                animProp.delete()
        del self.animPropDict

    def enterAnimatedProps(self, zoneNode):
        for animProp in self.animPropDict.get(zoneNode, ()):            
            animProp.enter()

    def exitAnimatedProps(self, zoneNode):
        for animProp in self.animPropDict.get(zoneNode, ()):
            animProp.exit()
        
    def getInteractiveProp(self, zoneId):
        """Return the interactive prop for the battle cell at zone id, may return None"""
        result = None
        if zoneId in self.zoneIdToInteractivePropDict:
            result = self.zoneIdToInteractivePropDict[zoneId]
        return result
        
    

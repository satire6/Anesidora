"""SafeZoneLoader module: contains the SafeZoneLoader class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.hood import ZoneUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from toontown.launcher import DownloadForceAcknowledge
from toontown.toon import HealthForceAcknowledge
from toontown.tutorial import TutorialForceAcknowledge
from toontown.toonbase.ToontownGlobals import *
from toontown.building import ToonInterior
from toontown.hood import QuietZoneState

class SafeZoneLoader(StateData.StateData):
    """SafeZoneLoader class"""

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("SafeZoneLoader")

    def __init__(self, hood, parentFSMState, doneEvent):
        """
        SafeZoneLoader constructor: 
        """
        assert(self.notify.debug("__init__(hood="+str(hood)
                +", parentFSMState="+str(parentFSMState)
                +", doneEvent="+str(doneEvent)+")"))
        StateData.StateData.__init__(self, doneEvent)
        self.hood = hood
        self.parentFSMState = parentFSMState
        self.fsm = ClassicFSM.ClassicFSM('SafeZoneLoader',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['quietZone', 
                                        'playground',
                                         'toonInterior']),
                            State.State('playground',
                                        self.enterPlayground,
                                        self.exitPlayground,
                                        ['quietZone']),
                            State.State('toonInterior',
                                        self.enterToonInterior,
                                        self.exitToonInterior,
                                        ['quietZone']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['playground', 'toonInterior']),
                            State.State('golfcourse', #REMOVE THIS STATE
                                           self.enterGolfcourse,
                                           self.exitGolfcourse,
                                           ['quietZone', 'playground']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )
        self.placeDoneEvent = "placeDone"
        self.place=None
        self.playgroundClass = None

    def load(self):
        assert(self.notify.debug("load()"))
        self.music = base.loadMusic(self.musicFile)
        self.activityMusic = base.loadMusic(self.activityMusicFile)
        self.createSafeZone(self.dnaFile)
        self.parentFSMState.addChild(self.fsm)

    def unload(self):
        assert(self.notify.debug("unload()"))
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        self.geom.removeNode()
        del self.geom
        del self.fsm
        del self.hood
        del self.nodeList
        del self.playgroundClass
        del self.music
        del self.activityMusic
        del self.holidayPropTransforms
        self.deleteAnimatedProps()
        self.ignoreAll()
        # Get rid of any references to models or textures from this safe zone
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enter(self, requestStatus):
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        self.fsm.enterInitialState()
        # Let the safe zone manager know that we are here.
        messenger.send("enterSafeZone")
        self.setState(requestStatus["where"], requestStatus)

    def exit(self):
        assert(self.notify.debug("exit()"))
        # Let the safe zone manager know that we are leaving
        messenger.send("exitSafeZone")

    def setState(self, stateName, requestStatus):
        assert(self.notify.debug("setState(stateName="
                +str(stateName)+", requestStatus="+str(requestStatus)+")"))
        self.fsm.request(stateName, [requestStatus])
    
    def createSafeZone(self, dnaFile):
        assert(self.notify.debug("createSafeZone()"))
        # Load the safe zone specific models and textures
        # The estate has no safeZoneStorageDNAFile
        if self.safeZoneStorageDNAFile:
            loader.loadDNAFile(self.hood.dnaStore, self.safeZoneStorageDNAFile)
        # Load the actual safe zone dna
        node = loader.loadDNAFile(self.hood.dnaStore, dnaFile)

        if node.getNumParents() == 1:
            # If the node already has a parent arc when it's loaded, we must
            # be using the level editor and we want to preserve that arc.
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            # Otherwise, we should create a new arc for the node.
            self.geom = hidden.attachNewNode(node)
        # Make the vis dictionaries
        self.makeDictionaries(self.hood.dnaStore)
        self.createAnimatedProps(self.nodeList)
        # Record position of all holiday props before everything is flattened
        self.holidayPropTransforms = {}
        npl = self.geom.findAllMatches('**/=DNARoot=holiday_prop')
        for i in range(npl.getNumPaths()):
            np = npl.getPath(i)
            np.setTag('transformIndex', `i`)
            self.holidayPropTransforms[i] = np.getNetTransform()
        # Flatten the safe zone
        self.geom.flattenMedium()
        # Preload all textures in neighborhood
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)

    def makeDictionaries(self, dnaStore):
        assert(self.notify.debug("makeDictionaries()"))
        # A list of all visible nodes
        self.nodeList = []
        # There should only be one vis group
        for i in range(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            groupName = base.cr.hoodMgr.extractGroupName(groupFullName)
            groupNode = self.geom.find("**/" + groupFullName)
            if groupNode.isEmpty():
                self.notify.error("Could not find visgroup")
            self.nodeList.append(groupNode)
        self.removeLandmarkBlockNodes()
        # Now that we have extracted the vis groups we do not need
        # the dnaStore to keep them around
        # Remove all references to the safezone specific models and textures
        self.hood.dnaStore.resetPlaceNodes()
        self.hood.dnaStore.resetDNAGroups()
        self.hood.dnaStore.resetDNAVisGroups()
        self.hood.dnaStore.resetDNAVisGroupsAI()

    def removeLandmarkBlockNodes(self):
        """
        Since we are in the safe zone we do not need the suit_building_origins
        """
        assert(self.notify.debug("removeLandmarkBlockNodes()"))
        npc = self.geom.findAllMatches("**/suit_building_origin")
        for i in range(npc.getNumPaths()):
            npc.getPath(i).removeNode()
    
    # start state

    def enterStart(self):
        assert(self.notify.debug("enterStart()"))

    def exitStart(self):
        assert(self.notify.debug("exitStart()"))
        
    # playground state

    def enterPlayground(self, requestStatus):
        assert(self.notify.debug("enterPlayground(requestStatus="
                +str(requestStatus)+")"))
        self.acceptOnce(self.placeDoneEvent, self.handlePlaygroundDone)
        self.place=self.playgroundClass(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        self.place.enter(requestStatus)
        #self.hood.place = self.place
        base.cr.playGame.setPlace(self.place)

    def exitPlayground(self):
        assert(self.notify.debug("exitPlayground()"))
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place=None
        #self.hood.place = None
        base.cr.playGame.setPlace(self.place) 
   
    def handlePlaygroundDone(self):
        assert(self.notify.debug("handlePlaygroundDone()"))
        status=self.place.doneStatus
        if (ZoneUtil.getBranchZone(status["zoneId"]) == self.hood.hoodId and
            status["shardId"] == None):
            self.fsm.request("quietZone", [status])            
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)
    
    # toonInterior state

    def enterToonInterior(self, requestStatus):
        assert(self.notify.debug("enterToonInterior(requestStatus="
                +str(requestStatus)+")"))
        self.acceptOnce(self.placeDoneEvent, self.handleToonInteriorDone)
        self.place=ToonInterior.ToonInterior(self, 
                self.fsm.getStateNamed("toonInterior"), self.placeDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)

    def exitToonInterior(self):
        assert(self.notify.debug("exitToonInterior()"))
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place=None 
        base.cr.playGame.setPlace(self.place)
   
    def handleToonInteriorDone(self):
        assert(self.notify.debug("handleToonInteriorDone()"))
        status=self.place.doneStatus
        if (ZoneUtil.getBranchZone(status["zoneId"]) == self.hood.hoodId and
            status["shardId"] == None):
            self.fsm.request("quietZone", [status])            
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)

    # quietZone state

    def enterQuietZone(self, requestStatus):
        assert(self.notify.debug("enterQuietZone()"))
        self.quietZoneDoneEvent = "quietZoneDone"
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(
                self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        assert(self.notify.debug("exitQuietZone()"))
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData=None

    def handleQuietZoneDone(self):
        assert(self.notify.debug("handleQuietZoneDone()\n  base.cr.handlerArgs="
                +str(base.cr.handlerArgs)))
        # Change to the destination state:
        status=self.quietZoneStateData.getRequestStatus()
        if (status["where"] == "estate"):
            self.doneStatus = status
            messenger.send(self.doneEvent)
        else:
            self.fsm.request(status["where"], [status])
        

    # final state

    def enterFinal(self):
        assert(self.notify.debug("enterFinal()"))

    def exitFinal(self):
        assert(self.notify.debug("exitFinal()"))


    def createAnimatedProps(self, nodeList):
        assert(self.notify.debug("createAnimatedProps()"))
        self.animPropDict = {}
        for i in nodeList:
            # Get all the anim in the vis group
            animPropNodes = i.findAllMatches("**/animated_prop_*")
            numAnimPropNodes = animPropNodes.getNumPaths()
            for j in range(numAnimPropNodes):
                animPropNode = animPropNodes.getPath(j)

                if animPropNode.getName().startswith('animated_prop_generic'):
                    className = 'GenericAnimatedProp'
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
                className = 'GenericAnimatedProp'

                symbols = {}
                base.cr.importModule(symbols, 'toontown.hood', [className])

                classObj = getattr(symbols[className], className)
                interactivePropObj = classObj(interactivePropNode)
                # [gjeon] I think we can use animPropList to store interactive props
                animPropList = self.animPropDict.get(i)
                if animPropList is None:
                    animPropList = self.animPropDict.setdefault(i, [])                    
                animPropList.append(interactivePropObj)

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
            
    def enterGolfcourse( self, requestStatus ):
        """
        """
        #import pdb; pdb.set_trace()
        # Racetrack will grab this off of us
        #self.trackId = requestStatus[ 'trackId' ]
        #self.accept("golfOver",self.handleRaceOver)
        #self.accept("leavingGolf",self.handleLeftRace)

        base.transitions.fadeOut(t=0)

    def exitGolfcourse( self ):
        """
        """
        pass
        #del self.golfId

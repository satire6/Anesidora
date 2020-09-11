"""ToonInterior module: contains the ToonInterior class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from toontown.hood import ZoneUtil
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import NPCForceAcknowledge
from toontown.toon import HealthForceAcknowledge
class ToonInterior(Place.Place):
    """ToonInterior class"""

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("ToonInterior")

    # special methods

    def __init__(self, loader, parentFSMState, doneEvent):
        """
        ToonInterior constructor: create a play game ClassicFSM
        """
        Place.Place.__init__(self, loader, doneEvent)
        self.dnaFile="phase_7/models/modules/toon_interior"
        self.isInterior=1
        self.tfaDoneEvent = "tfaDoneEvent"
        self.hfaDoneEvent = "hfaDoneEvent"
        self.npcfaDoneEvent = "npcfaDoneEvent"
        # shared state
        self.fsm = ClassicFSM.ClassicFSM('ToonInterior',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['doorIn', 'teleportIn', 'tutorial',]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['sit', 'stickerBook', 'doorOut',
                                         'DFA', 'trialerFA',
                                         'teleportOut', 'quest',
                                         'purchase', 'phone','stopped', 'pet']),
                            State.State('sit',
                                        self.enterSit,
                                        self.exitSit,
                                        ['walk',]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA', 'trialerFA',
                                         'sit', 'doorOut',
                                         'teleportOut', 'quest',
                                         'purchase', 'phone', 'stopped',  'pet',
                                         ]),
                            # Trialer Force Acknowledge:
                            State.State('trialerFA',
                                        self.enterTrialerFA,
                                        self.exitTrialerFA,
                                        ['trialerFAReject', 'DFA']),
                            State.State('trialerFAReject',
                                        self.enterTrialerFAReject,
                                        self.exitTrialerFAReject,
                                        ['walk']),
                            # Download Force Acknowlege:
                            State.State('DFA',
                                        self.enterDFA,
                                        self.exitDFA,
                                        ['DFAReject', 'HFA', 'NPCFA', 'teleportOut', 
                                        'doorOut']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
                                        ['walk']),
                            # NPC Force Acknowledge:
                            State.State('NPCFA',
                                        self.enterNPCFA,
                                        self.exitNPCFA,
                                        ['NPCFAReject', 'HFA', 'teleportOut']),
                            State.State('NPCFAReject',
                                        self.enterNPCFAReject,
                                        self.exitNPCFAReject,
                                        ['walk']),
                            # Health Force Acknowledge
                            State.State('HFA',
                                        self.enterHFA,
                                        self.exitHFA,
                                        ['HFAReject', 'teleportOut', 'tunnelOut']),
                            State.State('HFAReject',
                                        self.enterHFAReject,
                                        self.exitHFAReject,
                                        ['walk']),
                            State.State('doorIn',
                                        self.enterDoorIn,
                                        self.exitDoorIn,
                                        ['walk']),
                            State.State('doorOut',
                                        self.enterDoorOut,
                                        self.exitDoorOut,
                                        ['walk']), # 'final'
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk']),
                            State.State('teleportOut',
                                        self.enterTeleportOut,
                                        self.exitTeleportOut,
                                        ['teleportIn']), # 'final'
                            State.State('quest',
                                        self.enterQuest,
                                        self.exitQuest,
                                        ['walk', 'doorOut',]),
                            State.State('tutorial',
                                        self.enterTutorial,
                                        self.exitTutorial,
                                        ['walk', 'quest',]),
                            State.State('purchase',
                                        self.enterPurchase,
                                        self.exitPurchase,
                                        ['walk', 'doorOut']),
                            State.State('pet',
                                        self.enterPet,
                                        self.exitPet,
                                        ['walk']),
                            State.State('phone',
                                        self.enterPhone,
                                        self.exitPhone,
                                        ['walk', 'doorOut']),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk', 'doorOut']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )
        self.parentFSMState = parentFSMState


    def load(self):
        assert(self.notify.debug("load()"))
        # Call up the chain
        Place.Place.load(self)

        self.parentFSMState.addChild(self.fsm)

    def unload(self):
        assert(self.notify.debug("unload()"))
        # Call up the chain
        Place.Place.unload(self)
        
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        del self.fsm
        #self.geom.removeNode()
        #del self.geom
        #self.ignoreAll()
        # Get rid of any references to models or textures from this safe zone
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enter(self, requestStatus):
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        self.zoneId = requestStatus["zoneId"]
        self.fsm.enterInitialState()
        # Let the safe zone manager know that we are here.
        messenger.send("enterToonInterior")
        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)
        # Play music
        volume = requestStatus.get('musicVolume', 0.7)
        base.playMusic(self.loader.activityMusic, looping = 1, volume = volume)

        #self.geom.reparentTo(render)

        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)
        # Request the state change:
        self.fsm.request(requestStatus["how"], [requestStatus])

    def exit(self):
        assert(self.notify.debug("exit()"))
        self.ignoreAll()
        # Let the safe zone manager know that we are leaving
        messenger.send("exitToonInterior")
        #self.geom.reparentTo(hidden)

        # Turn off the little red arrows.
        NametagGlobals.setMasterArrowsOn(0)

        # Stop music
        self.loader.activityMusic.stop()

    def setState(self, state):
        assert(self.notify.debug("setState(state="+str(state)+")"))
        self.fsm.request(state)

    def enterTutorial(self, requestStatus):
        self.fsm.request("walk")
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)
        globalClock.tick()
        base.transitions.irisIn()
        messenger.send("enterTutorialInterior")
        

    def exitTutorial(self):
        pass

    def doRequestLeave(self, requestStatus):
        # when it's time to leave, check their trialer status first
        self.fsm.request('trialerFA', [requestStatus])

    # walk state inherited from Place.py

    # sticker book state inherited from Place.py
        
    # doorIn/Out state inherited from Place.py

    # override DFA callback
    def enterDFACallback(self, requestStatus, doneStatus):
        """
        Download Force Acknowledge
        This function overrides Place.py because from the toon interior we need to
        if you have ridden the trolley before letting you teleprt out.
        """
        assert(self.notify.debug("enterDFACallback()"))
        self.dfa.exit()
        del self.dfa
        # Check the status from the dfa
        # If the download force acknowledge tells us the download is complete, then
        # we can enter the tunnel, otherwise for now we just stand there
        ds = doneStatus['mode']
        if (ds == 'complete'):
            # Allowed, check your quests
            # We no longer need the NPCFA with the new tutorial
            self.fsm.request("NPCFA", [requestStatus])
            # Skip straight to the HFA
            #self.fsm.request("HFA", [requestStatus])
        # Rejected
        elif (ds == 'incomplete'):
            self.fsm.request("DFAReject")
        else:
            # Some return code that is not handled
            self.notify.error("Unknown done status for DownloadForceAcknowledge: "
                              + `doneStatus`)

    # NPCFA state
            
    def enterNPCFA(self, requestStatus):
        """NPC Force Acknowledge"""
        assert(self.notify.debug("enterNPCFA()"))

        self.acceptOnce(self.npcfaDoneEvent, self.enterNPCFACallback, [requestStatus])
        self.npcfa = NPCForceAcknowledge.NPCForceAcknowledge(self.npcfaDoneEvent)
        self.npcfa.enter()
        
    def exitNPCFA(self):
        assert(self.notify.debug("exitNPCFA()"))
        self.ignore(self.npcfaDoneEvent)
            
    def enterNPCFACallback(self, requestStatus, doneStatus):
        assert(self.notify.debug("enterNPCFACallback()"))
        self.npcfa.exit()
        del self.npcfa
        # Check the status from the fda
        # If the download force acknowledge tells us the download is complete, then
        # we can enter the tunnel, otherwise for now we just stand there
        # Allowed, do the tunnel transition
        if (doneStatus["mode"] == "complete"):
            # Allowed, let them leave
            outHow={"teleportIn":"teleportOut", "tunnelIn":"tunnelOut", "doorIn":"doorOut"}
            self.fsm.request(outHow[requestStatus["how"]], [requestStatus])
        elif (doneStatus["mode"] == 'incomplete'):
            self.fsm.request("NPCFAReject")
        else:
            # Some return code that is not handled
            self.notify.error("Unknown done status for NPCForceAcknowledge: "
                              + `doneStatus`)

    # npca reject state

    def enterNPCFAReject(self):
        assert(self.notify.debug("enterNPCFAReject()"))
        # TODO: reject movie, turn toon around
        self.fsm.request("walk")
    
    def exitNPCFAReject(self):
        assert(self.notify.debug("exitNPCFAReject()"))


        # HFA state

    def enterHFA(self, requestStatus):
        """Hit Point Force Acknowledge"""
        assert(self.notify.debug("enterHFA()"))
        self.acceptOnce(self.hfaDoneEvent, self.enterHFACallback, [requestStatus])
        # Make sure we have enough HP to leave the safe zone
        # This enforces the so-called time out penalty
        self.hfa = HealthForceAcknowledge.HealthForceAcknowledge(self.hfaDoneEvent)
        self.hfa.enter(1)
        
    def exitHFA(self):
        assert(self.notify.debug("exitHFA()"))
        self.ignore(self.hfaDoneEvent)
            
    def enterHFACallback(self, requestStatus, doneStatus):
        assert(self.notify.debug("enterHFACallback()"))
        self.hfa.exit()
        del self.hfa
        # Check the status from the fda
        # If the download force acknowledge tells us the download is complete, then
        # we can enter the tunnel, otherwise for now we just stand there
        # Allowed, do the tunnel transition
        if (doneStatus["mode"] == "complete"):
            outHow={"teleportIn":"teleportOut", "tunnelIn":"tunnelOut", "doorIn":"doorOut"}
            self.fsm.request(outHow[requestStatus["how"]], [requestStatus])
        # Rejected
        elif (doneStatus["mode"] == 'incomplete'):
            self.fsm.request("HFAReject")
        else:
            # Some return code that is not handled
            self.notify.error("Unknown done status for HealthForceAcknowledge: "
                              + `doneStatus`)

    # hfa reject state

    def enterHFAReject(self):
        assert(self.notify.debug("enterHFAReject()"))
        # TODO: reject movie, turn toon around
        self.fsm.request("walk")
    
    def exitHFAReject(self):
        assert(self.notify.debug("exitHFAReject()"))


    # teleport in state

    def enterTeleportIn(self, requestStatus):
        # We want to set localToon to the starting position within the
        # interior, even if we are teleporting to an avatar here.
        # That way, if the teleport-to-avatar fails (for instance, if
        # the avatar has moved on), we'll at least be in a sensible
        # place.
        if ZoneUtil.isPetshop(self.zoneId):
            base.localAvatar.setPosHpr(0, 0, ToontownGlobals.FloorOffset,
                                       45.0, 0.0, 0.0)
        else:
            base.localAvatar.setPosHpr(2.5, 11.5, ToontownGlobals.FloorOffset,
                                       45.0, 0.0, 0.0)

        Place.Place.enterTeleportIn(self, requestStatus)

    # teleport out state

    def enterTeleportOut(self, requestStatus):
        Place.Place.enterTeleportOut(self, requestStatus,
                self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone(requestStatus="
                +str(requestStatus)+")"))
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        shardId = requestStatus["shardId"]
        if ((hoodId == self.loader.hood.id) and (zoneId == self.zoneId) and (shardId == None)):
            # If you are teleporting to somebody in this zone
            self.fsm.request("teleportIn", [requestStatus])
        else:
            # Different hood or zone, exit the zone
            if (hoodId == ToontownGlobals.MyEstate):
                self.getEstateZoneAndGoHome(requestStatus)
            else:
                self.doneStatus = requestStatus
                messenger.send(self.doneEvent)

    def goHomeFailed(self, task):
        # it took too long to hear back from the server,
        # or we tried going to a non-friends house
        self.notifyUserGoHomeFailed()
        #  ignore the setLocalEstateZone message
        self.ignore("setLocalEstateZone")
        self.doneStatus["avId"] =  -1
        self.doneStatus["zoneId"] =  self.getZoneId()
        self.fsm.request("teleportIn", [self.doneStatus])
        return Task.done

    def exitTeleportOut(self):
        Place.Place.exitTeleportOut(self)



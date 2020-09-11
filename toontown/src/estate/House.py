"""House module: contains the House class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class House(Place.Place):
    """House class"""

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("House")

    # special methods

    def __init__(self, loader, avId, parentFSMState, doneEvent):
        """
        House constructor: create a play game ClassicFSM
        """
        Place.Place.__init__(self, loader, doneEvent)
        self.id = ToontownGlobals.MyEstate
        self.ownersAvId = avId
        self.dnaFile="phase_7/models/modules/toon_interior"
        self.isInterior=1
        self.tfaDoneEvent = "tfaDoneEvent"
        self.oldStyle = None
        # shared state
        self.fsm = ClassicFSM.ClassicFSM('House',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['doorIn', 'teleportIn', 'tutorial',]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['sit', 'stickerBook', 'doorOut',
                                         'DFA', 'teleportOut', 'quest',
                                         'purchase', 'closet', 'banking', 'phone', 'stopped']),
                            State.State('sit',
                                        self.enterSit,
                                        self.exitSit,
                                        ['walk',]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA',
                                         'sit', 'doorOut',
                                         'teleportOut', 'quest',
                                         'purchase', 'closet', 'banking', 'phone', 'stopped',
                                         ]),
                            # Download Force Acknowlege:
                            State.State('DFA',
                                        self.enterDFA,
                                        self.exitDFA,
                                        ['DFAReject', 'teleportOut', 
                                        'doorOut']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
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
                            State.State('closet',
                                        self.enterCloset,
                                        self.exitCloset,
                                        ['walk',]),
                            State.State('banking',
                                        self.enterBanking,
                                        self.exitBanking,
                                        ['walk',]),
                            State.State('phone',
                                        self.enterPhone,
                                        self.exitPhone,
                                        ['walk',]),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk',]),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start', 'teleportIn'])],
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
        self.zoneId=requestStatus["zoneId"]
        self.fsm.enterInitialState()
        # Let the safe zone manager know that we are here.
        messenger.send("enterHouse")
        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)

        #self.geom.reparentTo(render)
        
        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)
        # Request the state change:
        self.fsm.request(requestStatus["how"], [requestStatus])

    def exit(self):
        assert(self.notify.debug("exit()"))
        self.ignoreAll()

        # Make sure our ClassicFSM goes into its final state
        # so the walkStateData cleans up its tasks
        if (hasattr(self, 'fsm')):
            self.fsm.requestFinalState()


        # Let the safe zone manager know that we are leaving
        messenger.send("exitHouse")
        #self.geom.reparentTo(hidden)

        # Turn off the little red arrows.
        NametagGlobals.setMasterArrowsOn(0)


    def setState(self, state):
        assert(self.notify.debug("setState(state="+str(state)+")"))
        if hasattr(self, 'fsm'):
            self.fsm.request(state)
    
    def getZoneId(self):
        """
        Returns the current zone ID.
        """
        return self.zoneId


    def enterTutorial(self, requestStatus):
        self.fsm.request("walk")
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)
        globalClock.tick()
        base.transitions.irisIn()
        messenger.send("enterTutorialInterior")
        

    def exitTutorial(self):
        pass

    # walk state inherited from Place.py

    # sticker book state inherited from Place.py
        
    # doorIn/Out state inherited from Place.py

    # teleport in state

    def enterTeleportIn(self, requestStatus):
        # We want to set localToon to the starting position within the
        # interior, even if we are teleporting to an avatar here.
        # That way, if the teleport-to-avatar fails (for instance, if
        # the avatar has moved on), we'll at least be in a sensible
        # place.
        base.localAvatar.setPosHpr(2.5, 11.5, ToontownGlobals.FloorOffset,
                                     45.0, 0.0, 0.0)

        Place.Place.enterTeleportIn(self, requestStatus)

    # teleport out state

    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug("enterTeleportOut()"))
        Place.Place.enterTeleportOut(self, requestStatus,
                self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone()"))
        # If we're teleporting from a safezone, we need to set the
        # activityFsm to the final state
        if (hasattr(self, 'fsm')):
            self.fsm.requestFinalState()
        self.notify.debug("House: teleportOutDone: requestStatus = %s" % requestStatus)
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        avId = requestStatus["avId"]
        shardId = requestStatus["shardId"]
        if ((hoodId == ToontownGlobals.MyEstate) and (zoneId == self.getZoneId())):
            self.fsm.request("teleportIn", [requestStatus])
        elif (hoodId == ToontownGlobals.MyEstate):
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            # Different hood or zone, exit the safe zone
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent, [self.doneStatus])

    def goHomeFailed(self, task):
        # it took to long to hear back from the server,
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

    # purchase state
    def enterPurchase(self):
        # this state just locks the toon down so he can't move
        Place.Place.enterPurchase(self)

    def exitPurchase(self):
        Place.Place.exitPurchase(self)

    # closet state
    def enterCloset(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.laffMeter.start()
        base.localAvatar.obscureMoveFurnitureButton(1)
        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepCloset)
        self.enablePeriodTimer()        

    def __handleFallingAsleepCloset(self, arg):
        if hasattr(self, "fsm"):
            #the place has been unloaded... ignore this request
            self.fsm.request("walk")
        # this message will make sure the clothes picking GUI goes away
        messenger.send("closetAsleep")
        base.localAvatar.forceGotoSleep()
                
    def exitCloset(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)
        base.localAvatar.stopSleepWatch()
        self.disablePeriodTimer()

    # banking state
    def enterBanking(self):
        # this state just locks the toon down so he can't move
        Place.Place.enterBanking(self)

    def exitBanking(self):
        Place.Place.exitBanking(self)



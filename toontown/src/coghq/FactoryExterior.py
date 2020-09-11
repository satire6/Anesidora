
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.building import Elevator
from pandac.PandaModules import *

class FactoryExterior(BattlePlace.BattlePlace):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("FactoryExterior")
    #notify.setDebug(True)
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        assert(self.notify.debug("__init__()"))
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = "elevatorDone"

    def load(self):
        self.fsm = ClassicFSM.ClassicFSM('FactoryExterior',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'tunnelIn', 'teleportIn',
                                         'doorIn',
                                         ]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['stickerBook', 'teleportOut',
                                         'tunnelOut', 'DFA', 'doorOut',
                                         'elevator', 'stopped',
                                         'WaitForBattle', 'battle',
                                         ]),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk', 'teleportOut', 'elevator'
                                         ]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA',
                                         'WaitForBattle', 'battle', 'elevator',
                                         ]),
                            State.State('WaitForBattle',
                                        self.enterWaitForBattle,
                                        self.exitWaitForBattle,
                                        ['battle', 'walk']),
                            State.State('battle',
                                        self.enterBattle,
                                        self.exitBattle,
                                        ['walk', 'teleportOut', 'died']),
                            # Download Force Acknowlege:
                            State.State('DFA',
                                        self.enterDFA,
                                        self.exitDFA,
                                        ['DFAReject', 'teleportOut', 'tunnelOut']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
                                        ['walk']),
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk',
                                         ]),
                            State.State('teleportOut',
                                        self.enterTeleportOut,
                                        self.exitTeleportOut,
                                        ['teleportIn', 'final',
                                         'WaitForBattle']),
                            State.State('doorIn',
                                        self.enterDoorIn,
                                        self.exitDoorIn,
                                        ['walk']),
                            State.State('doorOut',
                                        self.enterDoorOut,
                                        self.exitDoorOut,
                                        ['walk']),
                            State.State('died',
                                        self.enterDied,
                                        self.exitDied,
                                        ['quietZone']),
                            State.State('tunnelIn',
                                        self.enterTunnelIn,
                                        self.exitTunnelIn,
                                        ['walk']),
                            State.State('tunnelOut',
                                        self.enterTunnelOut,
                                        self.exitTunnelOut,
                                        ['final']),
                            State.State('elevator',
                                        self.enterElevator,
                                        self.exitElevator,
                                        ['walk', 'stopped']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )
        self.parentFSM.getStateNamed("factoryExterior").addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)

    def unload(self):
        self.parentFSM.getStateNamed("factoryExterior").removeChild(self.fsm)
        del self.fsm
        BattlePlace.BattlePlace.unload(self)        

    def enter(self, requestStatus):
        self.zoneId = requestStatus["zoneId"]
        # This will call load()
        BattlePlace.BattlePlace.enter(self)
        self.fsm.enterInitialState()
        # Play music
        base.playMusic(self.loader.music, looping = 1, volume = 0.8)
        self.loader.geom.reparentTo(render)
        self.nodeList = [self.loader.geom]
        # Turn the sky on
        self.loader.hood.startSky()

        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)
        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)
        # Add hooks for the linktunnels
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        how=requestStatus["how"]
        self.fsm.request(how, [requestStatus])

    def exit(self):
        # Turn the sky off
        self.loader.hood.stopSky()
        self.fsm.requestFinalState()
        # Stop music
        self.loader.music.stop()
        for node in self.tunnelOriginList:
            node.removeNode()
        del self.tunnelOriginList
        del self.nodeList
        # self.loader.geom.reparentTo(hidden)
        self.ignoreAll()
        BattlePlace.BattlePlace.exit(self)

    def enterTunnelOut(self, requestStatus):
        # Drop off the last two digits of the zoneId to make the
        # tunnel name.
        fromZoneId = self.zoneId - (self.zoneId % 100)
        tunnelName = base.cr.hoodMgr.makeLinkTunnelName(
            self.loader.hood.id, fromZoneId)
        requestStatus["tunnelName"] = tunnelName
        
        BattlePlace.BattlePlace.enterTunnelOut(self, requestStatus)

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))

        # In the FactoryExterior, we drop everyone to the same
        # location.  This is only a fallback in case the toon we
        # are teleporting to has moved.
        base.localAvatar.setPosHpr(-34, -350, 0, -28, 0, 0)

        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)
        
    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug("enterTeleportOut()"))
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone()"))
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        avId = requestStatus["avId"]
        shardId = requestStatus["shardId"]
        if ((hoodId == self.loader.hood.hoodId) and (zoneId == self.zoneId) and (shardId == None)):
            # If you are teleporting to somebody in this exterior
            # TODO: might need to set the new zone
            self.fsm.request("teleportIn", [requestStatus])
        elif (hoodId == ToontownGlobals.MyEstate):
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            # Different hood or zone, exit the safe zone
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def exitTeleportOut(self):
        assert(self.notify.debug("exitTeleportOut()"))
        BattlePlace.BattlePlace.exitTeleportOut(self)

    # elevator state
    # (For boarding a building elevator)
    def enterElevator(self, distElevator, skipDFABoard = 0):
        assert(self.notify.debug("enterElevator()"))
        
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed("elevator"),
                                          self.elevatorDoneEvent,
                                          distElevator)
        if skipDFABoard:
            self.elevator.skipDFABoard = 1
        #elevatorFSM is now on the DO
        distElevator.elevatorFSM=self.elevator
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        assert(self.notify.debug("exitElevator()"))
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        assert(self.notify.debug("detectedElevatorCollision()"))
        self.fsm.request("elevator", [distElevator])

    def handleElevatorDone(self, doneStatus):
        assert(self.notify.debug("handleElevatorDone()"))
        self.notify.debug("handling elevator done event")
        where = doneStatus['where']
        if (where == 'reject'):
            # If there has been a reject the Elevator should show an 
            # elevatorNotifier message and put the toon in the stopped state.
            # Don't request the walk state here. Let the the toon be stuck in the
            # stopped state till the player removes that message from his screen.
            # Removing the message will automatically put him in the walk state there.
            # Put the player in the walk state only if there is no elevator message.
            if hasattr(base.localAvatar, "elevatorNotifier") and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request("walk")
        elif (where == 'exit'):
            self.fsm.request("walk")
        elif (where == 'factoryInterior'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        elif (where == 'stageInterior'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + where +
                              " in handleElevatorDone")


from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.building import Elevator
from pandac.PandaModules import *
from toontown.coghq import CogHQExterior

class LawbotHQExterior(CogHQExterior.CogHQExterior):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("LawbotHQExterior")

    """
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        assert(self.notify.debug("__init__()"))
        CogHQExterior.CogHQExterior.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = "elevatorDone"
        self.fsm = ClassicFSM.ClassicFSM('LawbotHQExterior',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'tunnelIn', 'teleportIn',
                                         ]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['stickerBook', 'teleportOut',
                                         'tunnelOut', 'DFA',
                                         'elevator',
                                         'WaitForBattle', 'battle',
                                         ]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA',
                                         'WaitForBattle', 'battle',
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
                                        ['walk']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )

    def load(self):
        #self.parentFSM.getStateNamed("LawbotHQExterior").addChild(self.fsm)
        CogHQExterior.CogHQExterior.load(self)

    def unload(self):
        #self.parentFSM.getStateNamed("LawbotHQExterior").removeChild(self.fsm)
        CogHQExterior.CogHQExterior.unload(self)        

    def enter(self, requestStatus):
        self.zoneId = requestStatus["zoneId"]
        # This will call load()
        CogHQExterior.CogHQExterior.enter(self, requestStatus)
        # Play music
        base.playMusic(self.loader.music, looping = 1, volume = 0.8)
        self.loader.geom.reparentTo(render)
        self.nodeList = [self.loader.geom]
        # Turn the sky on
        self.loader.hood.startSky()
        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)
        # Add hooks for the linktunnels
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        how=requestStatus["how"]
        self.fsm.request(how, [requestStatus])

    def exit(self):
        CogHQExterior.CogHQExterior.exit(self)
        # Turn the sky off
        self.loader.hood.stopSky()
        # Stop music
        self.loader.music.stop()
        if hasattr(self, 'tunnelOriginList'):
            for node in self.tunnelOriginList:
                node.removeNode()
            del self.tunnelOriginList
        del self.nodeList
        # self.loader.geom.reparentTo(hidden)
        self.ignoreAll()
        

    def enterTunnelOut(self, requestStatus):
        # Drop off the last two digits of the zoneId to make the
        # tunnel name.
        fromZoneId = self.zoneId - (self.zoneId % 100)
        tunnelName = base.cr.hoodMgr.makeLinkTunnelName(
            self.loader.hood.id, fromZoneId)
        requestStatus["tunnelName"] = tunnelName
        
        CogHQExterior.CogHQExterior.enterTunnelOut(self, requestStatus)

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))

        # In the FactoryExterior, we drop everyone to the same
        # location.  This is only a fallback in case the toon we
        # are teleporting to has moved.
        base.localAvatar.setPosHpr(-0, -60, 10, -95, 0, 0)

        CogHQExterior.CogHQExterior.enterTeleportIn(self, requestStatus)
        
    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug("enterTeleportOut()"))
        CogHQExterior.CogHQExterior.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

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
        CogHQExterior.CogHQExterior.exitTeleportOut(self)

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
            self.fsm.request("walk")
        elif (where == 'exit'):
            self.fsm.request("walk")
        elif (where == 'stageInterior'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + where +
                              " in handleElevatorDone")
    """


from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *

class CogHQExterior(BattlePlace.BattlePlace):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CogHQExterior")
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        assert(self.notify.debug("__init__()"))
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM

        self.fsm = ClassicFSM.ClassicFSM('CogHQExterior',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'tunnelIn', 'teleportIn', 'doorIn',
                                         ]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['stickerBook', 'teleportOut',
                                         'tunnelOut', 'DFA',
                                         'doorOut', 'died', 'stopped',
                                         'WaitForBattle', 'battle',
                                         'squished', 'stopped',
                                         ]),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk', 'teleportOut', 'stickerBook',
                                         ]),
                            State.State('doorIn',
                                        self.enterDoorIn,
                                        self.exitDoorIn,
                                        ['walk', 'stopped']),
                            State.State('doorOut',
                                        self.enterDoorOut,
                                        self.exitDoorOut,
                                        ['walk', 'stopped']),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA',
                                         'WaitForBattle', 'battle',
                                         'tunnelOut', 'doorOut',
                                         'squished', 'died'
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
                            State.State('squished',
                                        self.enterSquished,
                                        self.exitSquished,
                                        ['walk', 'died', 'teleportOut',]),
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk', 'WaitForBattle', 'battle',
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
                                        ['walk', 'WaitForBattle', 'battle']),
                            State.State('tunnelOut',
                                        self.enterTunnelOut,
                                        self.exitTunnelOut,
                                        ['final']),
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
        self.parentFSM.getStateNamed("cogHQExterior").addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)

    def unload(self):
        self.parentFSM.getStateNamed("cogHQExterior").removeChild(self.fsm)
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

        # Turn on the animated props once since there is only one zone
        # for i in self.loader.nodeList:
        #    self.loader.enterAnimatedProps(i)

        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)

        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)

        # Add hooks for the linktunnels
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        how=requestStatus["how"]
        self.fsm.request(how, [requestStatus])

    def exit(self):
        self.fsm.requestFinalState()

        # Stop music
        self.loader.music.stop()
        for node in self.tunnelOriginList:
            node.removeNode()
        del self.tunnelOriginList
        if self.loader.geom:
            self.loader.geom.reparentTo(hidden)
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
        x,y,z,h,p,r = base.cr.hoodMgr.getPlaygroundCenterFromId(self.loader.hood.id)
        base.localAvatar.setPosHpr(render, x,y,z,h,p,r)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    def enterTeleportOut(self, requestStatus, callback=None):
        assert(self.notify.debug("enterTeleportOut()"))
        # If the request comes from a battle, let the battle handle
        # the teleport animation sequence, otherwise use the distributed
        # toon version
        if (requestStatus.has_key('battle')):
            self.__teleportOutDone(requestStatus)
        else:
            BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus,
                    self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone()"))

        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        avId = requestStatus["avId"]
        shardId = requestStatus["shardId"]
        if ((hoodId == self.loader.hood.hoodId) and (zoneId == self.loader.hood.hoodId) and (shardId == None)):
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

    def enterSquished(self):
        assert(CogHQExterior.notify.debug("enterSquished()"))
        # exitWalk hides the laffmeter, so start it here
        base.localAvatar.laffMeter.start()
        # Play the 'squish' animation
        base.localAvatar.b_setAnimState('Squish')
        # Put toon back in walk state after a couple seconds
        taskMgr.doMethodLater(2.0,
                              self.handleSquishDone,
                              base.localAvatar.uniqueName("finishSquishTask"))
        
    def handleSquishDone(self, extraArgs=[]):
        # put place back in walk state after squish is done
        base.cr.playGame.getPlace().setState("walk")
        
    def exitSquished(self):
        assert(CogHQExterior.notify.debug("exitSquished()"))
        taskMgr.remove(base.localAvatar.uniqueName("finishSquishTask"))
        base.localAvatar.laffMeter.stop()
    

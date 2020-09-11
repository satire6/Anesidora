
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.showbase import BulletinBoardWatcher
from pandac.PandaModules import *
from toontown.toon import Toon
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownBattleGlobals
from toontown.coghq import DistributedMint

class MintInterior(BattlePlace.BattlePlace):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("MintInterior")
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        assert(MintInterior.notify.debug("MintInterior()"))
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        # this is put on the loader by CashbotCogHQLoader.enterMintInterior
        self.zoneId = loader.mintId
        # any state that we might be in when someone beats the mint
        # needs to have a transition to teleportout
        self.fsm = ClassicFSM.ClassicFSM('MintInterior',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk',
                                         'teleportIn',
                                         'fallDown',
                                         ]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['push', 'sit', 'stickerBook', 
                                         'WaitForBattle', 'battle', 
                                         'died', 'teleportOut', 'squished',
                                         'DFA', 'fallDown', 'stopped'
                                         ]),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk', 'teleportOut', 'stickerBook',
                                         ]),
                            State.State('sit',
                                        self.enterSit,
                                        self.exitSit,
                                        ['walk', 'died', 'teleportOut',]),
                            State.State('push',
                                        self.enterPush,
                                        self.exitPush,
                                        ['walk', 'died', 'teleportOut',]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'battle', 'DFA',
                                        'WaitForBattle', 'died', 'teleportOut',
                                         ]),
                            # This needs a transition to teleportOut to allow
                            # the toon to leave after beating the mint.
                            # When localToon leaves the battle, battle gets
                            # a setMembers with no localToon, enables its
                            # collision sphere, collides with localToon, puts
                            # localToon in WaitForBattle.
                            State.State('WaitForBattle',
                                        self.enterWaitForBattle,
                                        self.exitWaitForBattle,
                                        ['battle', 'walk', 'died',
                                         'teleportOut',]),
                            State.State('battle',
                                        self.enterBattle,
                                        self.exitBattle,
                                        ['walk', 'teleportOut', 'died',]),
                            State.State('fallDown',
                                        self.enterFallDown,
                                        self.exitFallDown,
                                        ['walk', 'died', 'teleportOut',]),
                            State.State('squished',
                                        self.enterSquished,
                                        self.exitSquished,
                                        ['walk', 'died', 'teleportOut',]),
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk', 'teleportOut', 'quietZone', 'died',]),
                            State.State('teleportOut',
                                        self.enterTeleportOut,
                                        self.exitTeleportOut,
                                        ['teleportIn', 'FLA', 'quietZone',
                                         'WaitForBattle']),
                            # Download Force Acknowledge
                            State.State('DFA',
                                        self.enterDFA,
                                        self.exitDFA,
                                        ['DFAReject', 'teleportOut']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
                                        ['walk' 'teleportOut',]),
                            State.State('died',
                                        self.enterDied,
                                        self.exitDied,
                                        ['teleportOut']),
                            # Forced Leave Acknowledge
                            State.State('FLA',
                                        self.enterFLA,
                                        self.exitFLA,
                                        ['quietZone']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['teleportIn']),
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
        self.parentFSM.getStateNamed("mintInterior").addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)
        self.music = base.loadMusic('phase_9/audio/bgm/CHQ_FACT_bg.mid')

    def unload(self):
        self.parentFSM.getStateNamed("mintInterior").removeChild(self.fsm)
        del self.music
        del self.fsm
        del self.parentFSM
        BattlePlace.BattlePlace.unload(self)

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        base.transitions.fadeOut(t=0)

        # While we are here, we ignore invasion credit.
        base.localAvatar.inventory.setRespectInvasions(0)

        # Cheesy rendering effects are not allowed in mints.
        base.cr.forbidCheesyEffects(1)

        # wait until the mint and any distributed entities have been
        # created before moving on
        def commence(self=self):
            # Turn on the little red arrows.
            NametagGlobals.setMasterArrowsOn(1)
            self.fsm.request(requestStatus["how"], [requestStatus])
            base.playMusic(self.music, looping = 1, volume = 0.8)
            base.transitions.irisIn()
            mint = bboard.get(DistributedMint.DistributedMint.ReadyPost)
            self.loader.hood.spawnTitleText(mint.mintId, mint.floorNum)
        # as soon as the mint is ready, proceed
        self.mintReadyWatcher = BulletinBoardWatcher.BulletinBoardWatcher(
            'MintReady', DistributedMint.DistributedMint.ReadyPost, commence)

        self.mintDefeated = 0
        self.acceptOnce(DistributedMint.DistributedMint.WinEvent,
                        self.handleMintWinEvent)
        if __debug__ and 0:
            # make F10 simulate someone else winning the mint
            self.accept('f10',
                        lambda: messenger.send(
                DistributedMint.DistributedMint.WinEvent))

        self.confrontedBoss = 0
        def handleConfrontedBoss(self=self):
            self.confrontedBoss = 1
        self.acceptOnce('localToonConfrontedMintBoss', handleConfrontedBoss)

    def exit(self):
        # Turn off the little red arrows.
        NametagGlobals.setMasterArrowsOn(0)

        bboard.remove(DistributedMint.DistributedMint.ReadyPost)

        # Restore cheesy rendering effects.
        base.cr.forbidCheesyEffects(0)

        # Respect invasions again.
        base.localAvatar.inventory.setRespectInvasions(1)

        self.fsm.requestFinalState()
        self.loader.music.stop()
        self.music.stop()
        self.ignoreAll()
        del self.mintReadyWatcher

    # walk state inherited from BattlePlace.py
    # Override to turn off teleport
    def enterWalk(self, teleportIn=0):
        BattlePlace.BattlePlace.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    # push state inherited from Place.py
    # Override to turn off teleport
    def enterPush(self):
        BattlePlace.BattlePlace.enterPush(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    # waitForBattle state inherited from BattlePlace.py
    def enterWaitForBattle(self):
        MintInterior.notify.debug('enterWaitForBattle')
        BattlePlace.BattlePlace.enterWaitForBattle(self)
        # make sure we're under render, and make sure everyone else knows it
        if base.localAvatar.getParent() != render:
            base.localAvatar.wrtReparentTo(render)
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def exitWaitForBattle(self):
        MintInterior.notify.debug('exitWaitForBattle')
        BattlePlace.BattlePlace.exitWaitForBattle(self)

    # battle state inherited from BattlePlace.py
    # Override to turn off teleport and control music
    def enterBattle(self, event):
        MintInterior.notify.debug('enterBattle')
        self.music.stop()
        BattlePlace.BattlePlace.enterBattle(self, event)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    # Override to set bldg flag and creditMultiplier
    def enterTownBattle(self, event):
        # this assumes that our 'zoneId' is going to be set to the appropriate
        # faux-zone, and that we continue to use the faux-zone as the mint
        # ID
        mult = ToontownBattleGlobals.getMintCreditMultiplier(self.zoneId)
        base.localAvatar.inventory.setBattleCreditMultiplier(mult)
        self.loader.townBattle.enter(event, self.fsm.getStateNamed("battle"),
                                     bldg=1, creditMultiplier=mult)

    # Override to control our own music
    def exitBattle(self):
        MintInterior.notify.debug('exitBattle')
        BattlePlace.BattlePlace.exitBattle(self)
        self.loader.music.stop()
        base.playMusic(self.music, looping = 1, volume = 0.8)

    # sticker book state inherited from BattlePlace.py
    # Override to turn off teleport
    def enterStickerBook(self, page = None):
        BattlePlace.BattlePlace.enterStickerBook(self, page)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    # sit state inherited from BattlePlace.py
    # Override to turn off teleport
    def enterSit(self):
        BattlePlace.BattlePlace.enterSit(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterZone(self, zoneId):
        pass

    def enterTeleportOut(self, requestStatus):
        MintInterior.notify.debug('enterTeleportOut()')
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, 
                        self.__teleportOutDone)

    def __processLeaveRequest(self, requestStatus):
        hoodId = requestStatus["hoodId"]
        if (hoodId == ToontownGlobals.MyEstate):
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            # Different hood or zone, exit the safe zone
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def __teleportOutDone(self, requestStatus):
        MintInterior.notify.debug('__teleportOutDone()')
        messenger.send('leavingMint')
        messenger.send("localToonLeft")

        # we've played the teleport-out sequence; if we just got booted
        # out of the mint because the foreman was defeated, and we
        # were not in the battle, show a dialog to let the player know
        # what happened
        if self.mintDefeated and (not self.confrontedBoss):
            # Forced Leave Ack
            self.fsm.request('FLA', [requestStatus])
        else:
            self.__processLeaveRequest(requestStatus)
        
    def exitTeleportOut(self):
        MintInterior.notify.debug('exitTeleportOut()')
        BattlePlace.BattlePlace.exitTeleportOut(self)
         
    def handleMintWinEvent(self):
        """this handler is called when the mint has been defeated"""
        MintInterior.notify.debug('handleMintWinEvent')

        # if we're in the process of dying, ignore this
        if (base.cr.playGame.getPlace().fsm.getCurrentState().getName() ==
            'died'):
            return

        # update our flag
        self.mintDefeated = 1

        if 1:
            # go back to HQ
            zoneId = ZoneUtil.getHoodId(self.zoneId)
        else:
            # go back to the playground
            zoneId = ZoneUtil.getSafeZoneId(base.localAvatar.defaultZone)
        self.fsm.request('teleportOut', [{
            "loader": ZoneUtil.getLoaderName(zoneId),
            "where": ZoneUtil.getToonWhereName(zoneId),
            "how": "teleportIn",
            "hoodId": zoneId,
            "zoneId": zoneId,
            "shardId": None,
            "avId": -1,
            }])

    # died state
    def enterDied(self, requestStatus, callback = None):
        MintInterior.notify.debug('enterDied')
        def diedDone(requestStatus, self=self, callback=callback):
            if callback is not None:
                callback()
            messenger.send('leavingMint')
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
        BattlePlace.BattlePlace.enterDied(self, requestStatus, diedDone)

    # Forced Leave Ack state
    def enterFLA(self, requestStatus):
        MintInterior.notify.debug('enterFLA')
        # inform the player about why they got booted from the mint
        self.flaDialog = TTDialog.TTGlobalDialog(
            message = TTLocalizer.ForcedLeaveMintAckMsg,
            doneEvent = 'FLADone', style = TTDialog.Acknowledge,
            fadeScreen = 1,
            )
        def continueExit(self=self, requestStatus=requestStatus):
            self.__processLeaveRequest(requestStatus)
        self.accept('FLADone', continueExit)
        self.flaDialog.show()

    def exitFLA(self):
        MintInterior.notify.debug('exitFLA')
        if hasattr(self, 'flaDialog'):
            self.flaDialog.cleanup()
            del self.flaDialog

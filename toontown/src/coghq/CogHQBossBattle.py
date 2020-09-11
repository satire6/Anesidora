from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import BattlePlace
from toontown.suit import Suit
import math

class CogHQBossBattle(BattlePlace.BattlePlace):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CogHQBossBattle")
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        assert(self.notify.debug("__init__()"))
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM

        self.bossCog = None

        # This is only used for magic words.
        self.teleportInPosHpr = (0, 0, 0, 0, 0, 0)

        self.fsm = ClassicFSM.ClassicFSM('CogHQBossBattle',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'tunnelIn', 'teleportIn',
                                         'movie']),
                            State.State('battle',
                                        self.enterBattle,
                                        self.exitBattle,
                                        ['walk', 'died', 'movie']),
                            State.State('finalBattle',
                                        self.enterFinalBattle,
                                        self.exitFinalBattle,
                                        ['walk', 'stickerBook', 'teleportOut',
                                         'died',
                                         'tunnelOut', 'DFA', 'battle',
                                         'movie', 'ouch', 'crane',
                                         'WaitForBattle', 'squished'
                                         ]),
                            State.State('movie',
                                        self.enterMovie,
                                        self.exitMovie,
                                        ['walk', 'battle', 'finalBattle',
                                        'died', 'teleportOut']),
                            State.State('ouch',
                                        self.enterOuch,
                                        self.exitOuch,
                                        ['walk', 'battle', 'finalBattle',
                                        'died', 'crane']),
                            State.State('crane',
                                        self.enterCrane,
                                        self.exitCrane,
                                        ['walk', 'battle', 'finalBattle',
                                        'died', 'ouch', 'squished']),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['stickerBook', 'teleportOut',
                                         'died',
                                         'tunnelOut', 'DFA', 'battle',
                                         'movie', 'ouch', 'crane', 'finalBattle',
                                         'WaitForBattle', 
                                         ]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA', 'WaitForBattle',
                                         'movie', 'battle']),
                            State.State('WaitForBattle',
                                        self.enterWaitForBattle,
                                        self.exitWaitForBattle,
                                        ['battle', 'walk', 'movie']),
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
                                        ['teleportIn', 'final', 'WaitForBattle']),
                            State.State('died',
                                        self.enterDied,
                                        self.exitDied,
                                        ['final']),
                            State.State('tunnelIn',
                                        self.enterTunnelIn,
                                        self.exitTunnelIn,
                                        ['walk']),
                            State.State('tunnelOut',
                                        self.enterTunnelOut,
                                        self.exitTunnelOut,
                                        ['final']),
                            State.State('squished',
                                        self.enterSquished,
                                        self.exitSquished,
                                        ['finalBattle', 'crane', 'died', 'teleportOut',]),
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
        BattlePlace.BattlePlace.load(self)

        self.parentFSM.getStateNamed("cogHQBossBattle").addChild(self.fsm)
        self.townBattle = self.loader.townBattle
        for i in range(1, 3):
            Suit.loadSuits(i)

    def unload(self):
        BattlePlace.BattlePlace.unload(self)

        self.parentFSM.getStateNamed("cogHQBossBattle").removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()

        for i in range(1, 3):
            Suit.unloadSuits(i)

    def getTaskZoneId(self):
        # tell the task system that we're in a hood
        return base.cr.playGame.hood.id

    def enter(self, requestStatus, bossCog):
        self.zoneId = requestStatus["zoneId"]
        # This will call load()
        BattlePlace.BattlePlace.enter(self)
        self.fsm.enterInitialState()

        self.bossCog = bossCog
        if self.bossCog:
            self.bossCog.d_avatarEnter()

        # Don't play music here; the boss will play its own music
        # according to the state.

        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)

        # While we are here, we ignore invasion credit.
        base.localAvatar.inventory.setRespectInvasions(0)

        self.fsm.request(requestStatus["how"], [requestStatus])

    def exit(self):
        self.fsm.requestFinalState()        

        # Respect invasions again.
        base.localAvatar.inventory.setRespectInvasions(1)

        if self.bossCog:
            self.bossCog.d_avatarExit()

        self.bossCog = None

        BattlePlace.BattlePlace.exit(self)

    def enterBattle(self, event):
        assert(self.notify.debug("enterBattle()"))

        mult = 1
        if self.bossCog:
            mult = ToontownBattleGlobals.getBossBattleCreditMultiplier(self.bossCog.battleNumber)

        assert(self.notify.debug("creditMultiplier = %s" % (mult)))

        self.townBattle.enter(event, self.fsm.getStateNamed("battle"),
                              bldg = 1, creditMultiplier = mult)

        # Make sure the toon's anim state gets reset
        base.localAvatar.b_setAnimState('off', 1)
        base.localAvatar.setTeleportAvailable(0)
        # Disable leave to pay / set parent password
        base.localAvatar.cantLeaveGame = 1
        
    def exitBattle(self):
        assert(self.notify.debug("exitBattle()"))
        self.townBattle.exit()

    def enterFinalBattle(self):
        assert(self.notify.debug("enterFinalBattle()"))

        self.walkStateData.enter()
        self.walkStateData.fsm.request('walking')

        base.localAvatar.setTeleportAvailable(0)
        base.localAvatar.setTeleportAllowed(0)
        base.localAvatar.cantLeaveGame = 0
        
        # Put away the book
        base.localAvatar.book.hideButton()
        self.ignore(ToontownGlobals.StickerBookHotkey)
        self.ignore("enterStickerBook")
        self.ignore(ToontownGlobals.OptionsPageHotkey)
        
    def exitFinalBattle(self):
        assert(self.notify.debug("exitFinalBattle()"))
        self.walkStateData.exit()

        base.localAvatar.setTeleportAllowed(1)


    def enterMovie(self, requestStatus = None):
        assert(self.notify.debug("enterMovie()"))
        base.localAvatar.setTeleportAvailable(0)
        
    def exitMovie(self):
        assert(self.notify.debug("exitMovie()"))

    def enterOuch(self):
        assert(self.notify.debug("enterOuch()"))
        base.localAvatar.setTeleportAvailable(0)
        base.localAvatar.laffMeter.start()
        
    def exitOuch(self):
        assert(self.notify.debug("exitOuch()"))
        base.localAvatar.laffMeter.stop()

    def enterCrane(self):
        assert(self.notify.debug("enterCrane()"))
        base.localAvatar.setTeleportAvailable(0)
        base.localAvatar.laffMeter.start()
        base.localAvatar.collisionsOn()
        
    def exitCrane(self):
        assert(self.notify.debug("exitCrane()"))
        base.localAvatar.collisionsOff()
        base.localAvatar.laffMeter.stop()
        
    # walk state inherited from Place.py
    def enterWalk(self, teleportIn=0):
        BattlePlace.BattlePlace.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)
        
        # don't let them do a book teleport out
        base.localAvatar.setTeleportAllowed(0)
        # Put away the book
        base.localAvatar.book.hideButton()
        self.ignore(ToontownGlobals.StickerBookHotkey)
        self.ignore("enterStickerBook")
        self.ignore(ToontownGlobals.OptionsPageHotkey)

    def exitWalk(self):
        """Make sure to enable teleport for the toon."""
        BattlePlace.BattlePlace.exitWalk(self)
        base.localAvatar.setTeleportAllowed(1)

    # sticker book state inherited from Place.py
    def enterStickerBook(self, page = None):
        BattlePlace.BattlePlace.enterStickerBook(self, page)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    # sit state inherited from Place.py
    def enterSit(self):
        BattlePlace.BattlePlace.enterSit(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))

        base.localAvatar.detachNode()
        base.localAvatar.setPosHpr(*self.teleportInPosHpr)

        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug('enterTeleportOut()'))
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, 
                        self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        # Get out of here.
        hoodId = requestStatus["hoodId"]
        if hoodId == ToontownGlobals.MyEstate:
            # We are trying to go to an estate. This request might fail
            # if we are going to a toon's estate that we are not friends with.
            # So we don't want to tell the AI that we are leaving right away.
            # We will rely on the Place.Place.goHome function to do that if
            # the teleport to estate request is successful.
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def enterSquished(self):
        assert(self.notify.debug("enterSquished()"))
        # exitWalk hides the laffmeter, so start it here
        base.localAvatar.laffMeter.start()
        # Play the 'squish' animation
        base.localAvatar.b_setAnimState('Flattened')
        # Put toon back in walk state after a couple seconds
        #taskMgr.doMethodLater(2.0,
        #                      self.handleSquishDone,
        #                      base.localAvatar.uniqueName("finishSquishTask"))
        
    def handleSquishDone(self, extraArgs=[]):
        # put place back in walk state after squish is done
        base.cr.playGame.getPlace().setState("walk")
        
    def exitSquished(self):
        assert(self.notify.debug("exitSquished()"))
        taskMgr.remove(base.localAvatar.uniqueName("finishSquishTask"))
        base.localAvatar.laffMeter.stop()
    

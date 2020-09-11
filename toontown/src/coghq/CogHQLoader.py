
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import CogHQLobby
from toontown.hood import QuietZoneState
from toontown.hood import ZoneUtil
from toontown.town import TownBattle
from toontown.suit import Suit
from pandac.PandaModules import *

class CogHQLoader(StateData.StateData):

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CogHQLoader")

    def __init__(self, hood, parentFSMState, doneEvent):
        assert(self.notify.debug("__init__(hood="+str(hood)
                                 +", parentFSMState="+str(parentFSMState)
                                 +", doneEvent="+str(doneEvent)+")"))
        StateData.StateData.__init__(self, doneEvent)
        self.hood = hood
        self.parentFSMState = parentFSMState
        self.placeDoneEvent = "cogHQLoaderPlaceDone"
        self.townBattleDoneEvent = 'town-battle-done'
        self.fsm = ClassicFSM.ClassicFSM('CogHQLoader',
                           [State.State('start',
                                        None,
                                        None,
                                        ['quietZone',
                                         'cogHQExterior', # Tunnel from toon hood
                                         'cogHQBossBattle', # magic word ~bossBattle
                                         ]),
                            State.State('cogHQExterior',
                                        self.enterCogHQExterior,
                                        self.exitCogHQExterior,
                                        ['quietZone',
                                         'cogHQLobby', # Door transition
                                         ]),
                            State.State('cogHQLobby',
                                        self.enterCogHQLobby,
                                        self.exitCogHQLobby,
                                        ['quietZone',
                                         'cogHQExterior', # Front door
                                         'cogHQBossBattle', # Elevator to top
                                         ]),
                            State.State('cogHQBossBattle',
                                        self.enterCogHQBossBattle,
                                        self.exitCogHQBossBattle,
                                        ['quietZone',
                                         ]),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['cogHQExterior', 'cogHQLobby',
                                         'cogHQBossBattle', ]),
                            State.State('final',
                                        None,
                                        None,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )

    def load(self, zoneId):
        # Prepare the state machine
        self.parentFSMState.addChild(self.fsm)
        self.music = base.loadMusic(self.musicFile)
        self.battleMusic = base.loadMusic('phase_9/audio/bgm/encntr_suit_winning.mid')
        # Load the battle UI:
        self.townBattle = TownBattle.TownBattle(self.townBattleDoneEvent)
        self.townBattle.load()
        Suit.loadSuits(3)
        self.loadPlaceGeom(zoneId)

    def loadPlaceGeom(self, zoneId):
        # Override
        return

    def unloadPlaceGeom(self):
        # Override
        return

    def unload(self):
        assert(self.notify.debug("unload()"))
        self.unloadPlaceGeom()
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        del self.fsm
        self.townBattle.unload()
        self.townBattle.cleanup()
        del self.townBattle
        del self.battleMusic
        Suit.unloadSuits(3)
        Suit.unloadSkelDialog()
        del self.hood
        # Get rid of any references to models or textures from this cogHQ
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        self.fsm.request(requestStatus["where"], [requestStatus])

    def exit(self):
        self.ignoreAll()

    def enterQuietZone(self, requestStatus):
        self.quietZoneDoneEvent = "quietZoneDone"
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(
                self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData=None

    def handleQuietZoneDone(self):
        # Change to the destination state:
        status=self.quietZoneStateData.getRequestStatus()
        self.fsm.request(status["where"], [status])

    def enterPlace(self, requestStatus):
        self.acceptOnce(self.placeDoneEvent, self.placeDone)
        self.place = self.placeClass(self, self.fsm, self.placeDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)

    def exitPlace(self):
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)

    def placeDone(self):
        self.requestStatus=self.place.doneStatus
        assert(self.notify.debug("placeDone() doneStatus="+str(self.requestStatus)))
        status = self.place.doneStatus
        if ((status.get("shardId") == None) and self.isInThisHq(status)):
            # CogHQs use the same loader for all places in the hood.
            # Get rid of the old place geom
            self.unloadPlaceGeom()
            # And load the new one
            zoneId = status['zoneId']
            self.loadPlaceGeom(zoneId)
            self.fsm.request("quietZone", [status])            
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)

    def isInThisHq(self, status):
        # return true if we're going to a zone in this HQ hood
        if ZoneUtil.isDynamicZone(status['zoneId']):
            return status['hoodId'] == self.hood.hoodId
        else:
            return ZoneUtil.getHoodId(status["zoneId"]) == self.hood.hoodId

    def enterCogHQExterior(self, requestStatus):
        self.placeClass = self.getExteriorPlaceClass()
        self.enterPlace(requestStatus)
        self.hood.spawnTitleText(requestStatus['zoneId'])
        
    def exitCogHQExterior(self):
        taskMgr.remove("titleText")
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None


    def enterCogHQLobby(self, requestStatus):
        self.placeClass = CogHQLobby.CogHQLobby
        self.enterPlace(requestStatus)
        self.hood.spawnTitleText(requestStatus['zoneId'])
        
    def exitCogHQLobby(self):
        taskMgr.remove("titleText")
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None

    
    def enterCogHQBossBattle(self, requestStatus):
        self.placeClass = self.getBossPlaceClass()
        self.enterPlace(requestStatus)
        
    def exitCogHQBossBattle(self):
        self.exitPlace()
        self.placeClass = None



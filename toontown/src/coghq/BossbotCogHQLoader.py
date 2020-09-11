
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import CogHQLoader
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
from toontown.coghq import BossbotHQExterior
from toontown.coghq import BossbotHQBossBattle
from toontown.coghq import BossbotOfficeExterior
from toontown.coghq import CountryClubInterior
from pandac.PandaModules import DecalEffect, TextEncoder
import random

# Used to compensate for scaling of Cog tunnel sign's
# original aspect ratio of 1125x813 to a uniform ratio,
# scale z by factor of 0.7227
aspectSF = 0.7227

class BossbotCogHQLoader(CogHQLoader.CogHQLoader):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("BossbotCogHQLoader")
    #notify.setDebug(True)

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        
        self.fsm.addState(State.State('countryClubInterior',
                                      self.enterCountryClubInterior,
                                      self.exitCountryClubInterior,
                                      ['quietZone',
                                       'cogHQExterior', # Tunnel
                                       ]))
   
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('countryClubInterior')
          
        
        self.musicFile = random.choice(["phase_12/audio/bgm/Bossbot_Entry_v1.mid", "phase_12/audio/bgm/Bossbot_Entry_v2.mid", "phase_12/audio/bgm/Bossbot_Entry_v3.mid"])

        self.cogHQExteriorModelPath = "phase_12/models/bossbotHQ/CogGolfHub"
        self.factoryExteriorModelPath = "phase_11/models/lawbotHQ/LB_DA_Lobby"
        self.cogHQLobbyModelPath = "phase_12/models/bossbotHQ/CogGolfCourtyard"

        self.geom = None

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        # Load anims
        Toon.loadBossbotHQAnims()

    def unloadPlaceGeom(self):
        # Get rid of any old geom
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        CogHQLoader.CogHQLoader.unloadPlaceGeom(self)

    def loadPlaceGeom(self, zoneId):
        self.notify.info("loadPlaceGeom: %s" % zoneId)

        # We shoud not look at the last 2 digits to match against these constants
        zoneId = (zoneId - (zoneId %100))

        self.notify.debug("zoneId = %d ToontownGlobals.BossbotHQ=%d" % (zoneId,ToontownGlobals.BossbotHQ))
            
        if zoneId == ToontownGlobals.BossbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)
            
            # Rename the link tunnels so they will hook up properly
            gzLinkTunnel = self.geom.find("**/LinkTunnel1")
            gzLinkTunnel.setName("linktunnel_gz_17000_DNARoot")

            # put the signs on the tunnels
            self.makeSigns()

            # HACK: make tunnel_origin point straight out of tunnel
            top = self.geom.find("**/TunnelEntrance")
            origin = top.find("**/tunnel_origin")
            origin.setH(-33.33)

        elif zoneId == ToontownGlobals.BossbotLobby:
            self.notify.debug("cogHQLobbyModelPath = %s" % self.cogHQLobbyModelPath)
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)

        else:
            # Note: the factory interior has a dynamically allocated zone but
            # that is ok because we do not need to load any models - they all
            # get loaded by the distributed object
            self.notify.warning("loadPlaceGeom: unclassified zone %s" % zoneId)
            
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId)
    
    def makeSigns(self):
        # helper func
        def makeSign(topStr, signStr, textId):
            top = self.geom.find("**/" + topStr)
            sign = top.find("**/" + signStr)
            #sign.node().setEffect(DecalEffect.make())
            locator = top.find("**/sign_origin")
            signText = DirectGui.OnscreenText(
                text = TextEncoder.upper(TTLocalizer.GlobalStreetNames[textId][-1]),
                font = ToontownGlobals.getSuitFont(),
                scale = TTLocalizer.BCHQLmakeSign,
                fg = (0, 0, 0, 1), 
                parent = sign)
            signText.setPosHpr(locator, 0, -0.1, -0.25, 0, 0, 0)
            signText.setDepthWrite(0)
            
        makeSign("Gate_2", "Sign_6", 10700)
        makeSign("TunnelEntrance", "Sign_2", 1000)
        makeSign("Gate_3", "Sign_3", 10600)
        makeSign("Gate_4", "Sign_4", 10500)
        makeSign("GateHouse", "Sign_5", 10200)
       
    def unload(self):
        CogHQLoader.CogHQLoader.unload(self)
        # unload anims
        Toon.unloadSellbotHQAnims()

#    def enterFactoryInterior(self, requestStatus):
#        self.placeClass = FactoryInterior.FactoryInterior
#        self.enterPlace(requestStatus)
        
    def enterStageInterior(self, requestStatus):
        self.placeClass = StageInterior.StageInterior
        self.stageId = requestStatus['stageId']
        self.enterPlace(requestStatus)
        
#    def exitFactoryInterior(self):
#        self.exitPlace()
#        self.placeClass = None
        
    def exitStageInterior(self):
        self.exitPlace()
        self.placeClass = None

    def getExteriorPlaceClass(self):
        self.notify.debug("getExteriorPlaceClass")
        return BossbotHQExterior.BossbotHQExterior

    def getBossPlaceClass(self):
        self.notify.debug("getBossPlaceClass")
        return BossbotHQBossBattle.BossbotHQBossBattle
        
    def enterFactoryExterior(self, requestStatus):
        self.placeClass = BossbotOfficeExterior.BossbotOfficeExterior
        self.enterPlace(requestStatus)
        #self.hood.spawnTitleText(requestStatus['zoneId'])
        
    def exitFactoryExterior(self):
        taskMgr.remove("titleText")
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None

    def enterCogHQBossBattle(self, requestStatus):
        self.notify.debug("BossbotCogHQLoader.enterCogHQBossBattle")
        CogHQLoader.CogHQLoader.enterCogHQBossBattle(self, requestStatus)
        base.cr.forbidCheesyEffects(1)
        
    def exitCogHQBossBattle(self):
        self.notify.debug("BossbotCogHQLoader.exitCogHQBossBattle")
        CogHQLoader.CogHQLoader.exitCogHQBossBattle(self)
        base.cr.forbidCheesyEffects(0)        
        

    def enterCountryClubInterior(self, requestStatus):
        self.placeClass = CountryClubInterior.CountryClubInterior
        # MintInterior will grab this off of us
        self.notify.info('enterCountryClubInterior, requestStatus=%s' % requestStatus)
        self.countryClubId = requestStatus['countryClubId']
        self.enterPlace(requestStatus)
        # spawnTitleText is done by MintInterior once the mint shows up
        
    def exitCountryClubInterior(self):
        self.exitPlace()
        self.placeClass = None
        del self.countryClubId




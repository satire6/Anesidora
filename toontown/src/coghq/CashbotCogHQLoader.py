
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import CogHQLoader, MintInterior
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
import CashbotHQExterior
import CashbotHQBossBattle
from pandac.PandaModules import DecalEffect

class CashbotCogHQLoader(CogHQLoader.CogHQLoader):

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CashbotCogHQLoader")
    #notify.setDebug(True)

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)

        self.fsm.addState(State.State('mintInterior',
                                      self.enterMintInterior,
                                      self.exitMintInterior,
                                      ['quietZone',
                                       'cogHQExterior', # Tunnel
                                       ]))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('mintInterior')

        self.musicFile = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"

        self.cogHQExteriorModelPath = "phase_10/models/cogHQ/CashBotShippingStation"
        self.cogHQLobbyModelPath = "phase_10/models/cogHQ/VaultLobby"
        self.geom = None

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        # load anims
        Toon.loadCashbotHQAnims()

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

        if zoneId == ToontownGlobals.CashbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)

            # Rename the link tunnels so they will hook up properly
            ddLinkTunnel = self.geom.find("**/LinkTunnel1")
            ddLinkTunnel.setName("linktunnel_dl_9252_DNARoot")

            # Put a handy sign on the link tunnel
            locator = self.geom.find('**/sign_origin')
            backgroundGeom = self.geom.find('**/EntranceFrameFront')
            backgroundGeom.node().setEffect(DecalEffect.make())
            signText = DirectGui.OnscreenText(
                text = TTLocalizer.DonaldsDreamland[-1],
                font = ToontownGlobals.getSuitFont(),
                scale = 3,
                fg = (0.87, 0.87, 0.87, 1), 
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = backgroundGeom)
            signText.setPosHpr(locator, 0, 0, 0, 0, 0, 0)
            signText.setDepthWrite(0)

        elif zoneId == ToontownGlobals.CashbotLobby:
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)

        # Note: the factory interior has a dynamically allocated zone but
        # that is ok because we do not need to load any models - they all
        # get loaded by the distributed object
            
        else:
            self.notify.warning("loadPlaceGeom: unclassified zone %s" % zoneId)
            
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId)
    

    def unload(self):
        CogHQLoader.CogHQLoader.unload(self)
        # unload anims
        Toon.unloadCashbotHQAnims()

    def enterMintInterior(self, requestStatus):
        self.placeClass = MintInterior.MintInterior
        # MintInterior will grab this off of us
        self.mintId = requestStatus['mintId']
        self.enterPlace(requestStatus)
        # spawnTitleText is done by MintInterior once the mint shows up
        
    def exitMintInterior(self):
        self.exitPlace()
        self.placeClass = None
        del self.mintId

    def getExteriorPlaceClass(self):
        return CashbotHQExterior.CashbotHQExterior
    
    def getBossPlaceClass(self):
        return CashbotHQBossBattle.CashbotHQBossBattle

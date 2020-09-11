
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import CogHQLoader
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
import FactoryExterior
import FactoryInterior
import SellbotHQExterior
import SellbotHQBossBattle
from pandac.PandaModules import DecalEffect

# Used to compensate for scaling of Cog tunnel sign's
# original aspect ratio of 1125x813 to a uniform ratio,
# scale z by factor of 0.7227
aspectSF = 0.7227

class SellbotCogHQLoader(CogHQLoader.CogHQLoader):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("SellbotCogHQLoader")
    #notify.setDebug(True)

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        self.fsm.addState(State.State('factoryExterior',
                                      self.enterFactoryExterior,
                                      self.exitFactoryExterior,
                                      ['quietZone',
                                       'factoryInterior', # Elevator
                                       'cogHQExterior', # Tunnel
                                       ]))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('factoryExterior')
        self.fsm.addState(State.State('factoryInterior',
                                        self.enterFactoryInterior,
                                        self.exitFactoryInterior,
                                        ['quietZone',
                                         'factoryExterior', # Win bldg
                                         ]))
        for stateName in ['quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('factoryInterior')
        
        self.musicFile = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"

        self.cogHQExteriorModelPath = "phase_9/models/cogHQ/SellbotHQExterior"
        self.cogHQLobbyModelPath = "phase_9/models/cogHQ/SellbotHQLobby"
        self.factoryExteriorModelPath = "phase_9/models/cogHQ/SellbotFactoryExterior"
        self.geom = None

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        # Load anims
        Toon.loadSellbotHQAnims()

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
        
        if zoneId == ToontownGlobals.SellbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)

            # Rename the link tunnels so they will hook up properly
            dgLinkTunnel = self.geom.find("**/Tunnel1")
            dgLinkTunnel.setName("linktunnel_dg_5316_DNARoot")
            factoryLinkTunnel = self.geom.find("**/Tunnel2")
            factoryLinkTunnel.setName("linktunnel_sellhq_11200_DNARoot")

            # Put handy signs on the link tunnels
            cogSignModel = loader.loadModel(
                'phase_4/models/props/sign_sellBotHeadHQ')
            cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
            cogSignSF = 23

            # To Daisys Garden
            dgSign = cogSign.copyTo(dgLinkTunnel)
            dgSign.setPosHprScale(
                0.00, -291.5, 29,
                180.00, 0.00, 0.00,
                cogSignSF, cogSignSF, cogSignSF * aspectSF)
            dgSign.node().setEffect(DecalEffect.make())
            dgText = DirectGui.OnscreenText(
                text = TTLocalizer.DaisyGardens[-1],
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.3), scale = TTLocalizer.SCLdgSign,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = dgSign)
            dgText.setDepthWrite(0)

            # To Factory
            factorySign = cogSign.copyTo(factoryLinkTunnel)
            factorySign.setPosHprScale(
                148.625, -155, 27,
                -90.00, 0.00, 0.00,
                cogSignSF, cogSignSF, cogSignSF * aspectSF)
            # Make text a decal
            factorySign.node().setEffect(DecalEffect.make())
            factoryTypeText = DirectGui.OnscreenText(
                text = TTLocalizer.Sellbot,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.25), scale = .075,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = factorySign)
            factoryTypeText.setDepthWrite(0)
            factoryText = DirectGui.OnscreenText(
                text = TTLocalizer.Factory,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.34), scale = .12,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = factorySign)
            factoryText.setDepthWrite(0)

            doors = self.geom.find("**/doors")
            door0 = doors.find("**/door_0")
            door1 = doors.find("**/door_1")
            door2 = doors.find("**/door_2")
            door3 = doors.find("**/door_3")

            index = 0
            for door in [door0, door1, door2, door3]:
                doorFrame = door.find("**/doorDoubleFlat/+GeomNode")
                door.find("**/doorFrameHoleLeft").wrtReparentTo(doorFrame)
                door.find("**/doorFrameHoleRight").wrtReparentTo(doorFrame)
                doorFrame.node().setEffect(DecalEffect.make())
                index += 1
        elif zoneId == ToontownGlobals.SellbotFactoryExt:
            self.geom = loader.loadModel(self.factoryExteriorModelPath)
            factoryLinkTunnel = self.geom.find("**/tunnel_group2")
            factoryLinkTunnel.setName("linktunnel_sellhq_11000_DNARoot")
            factoryLinkTunnel.find("**/tunnel_sphere").setName("tunnel_trigger")

            # Put handy signs on the link tunnels
            cogSignModel = loader.loadModel(
                'phase_4/models/props/sign_sellBotHeadHQ')
            cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
            cogSignSF = 23
            elevatorSignSF = 15

            # To Daisys Garden
            hqSign = cogSign.copyTo(factoryLinkTunnel)
            hqSign.setPosHprScale(
                0.0, -353, 27.5,
                -180.00, 0.00, 0.00,
                cogSignSF, cogSignSF, cogSignSF * aspectSF)
            hqSign.node().setEffect(DecalEffect.make())
            hqTypeText = DirectGui.OnscreenText(
                text = TTLocalizer.Sellbot,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.25), scale = .075,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = hqSign)
            hqTypeText.setDepthWrite(0)
            hqText = DirectGui.OnscreenText(
                text = TTLocalizer.Headquarters,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.34), scale = 0.1,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = hqSign)
            hqText.setDepthWrite(0)

            # Factory Front Entrance
            frontDoor = self.geom.find("**/doorway1")
            fdSign = cogSign.copyTo(frontDoor)
            fdSign.setPosHprScale(
                62.74, -87.99, 17.26,
                2.72, 0.00, 0.00,
                elevatorSignSF, elevatorSignSF, elevatorSignSF * aspectSF)
            fdSign.node().setEffect(DecalEffect.make())
            fdTypeText = DirectGui.OnscreenText(
                text = TTLocalizer.Factory,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.25), scale = TTLocalizer.SCLfdSign,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = fdSign)
            fdTypeText.setDepthWrite(0)
            fdText = DirectGui.OnscreenText(
                text = TTLocalizer.SellbotFrontEntrance,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.34), scale = TTLocalizer.SCLdgSign,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = fdSign)
            fdText.setDepthWrite(0)

            # Factory Side Entrance
            sideDoor = self.geom.find("**/doorway2")
            sdSign = cogSign.copyTo(sideDoor)
            sdSign.setPosHprScale(
                -164.78, 26.28, 17.25,
                -89.89, 0.00, 0.00,
                elevatorSignSF, elevatorSignSF, elevatorSignSF * aspectSF)
            sdSign.node().setEffect(DecalEffect.make())
            sdTypeText = DirectGui.OnscreenText(
                text = TTLocalizer.Factory,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.25), scale = .075,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = sdSign)
            sdTypeText.setDepthWrite(0)
            sdText = DirectGui.OnscreenText(
                text = TTLocalizer.SellbotSideEntrance,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.34), scale = 0.1,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = sdSign)
            sdText.setDepthWrite(0)
        elif zoneId == ToontownGlobals.SellbotLobby:
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)

            front = self.geom.find("**/frontWall")
            front.node().setEffect(DecalEffect.make())
            
            door = self.geom.find("**/door_0")
            parent = door.getParent()
            door.wrtReparentTo(front)
            doorFrame = door.find("**/doorDoubleFlat/+GeomNode")
            door.find("**/doorFrameHoleLeft").wrtReparentTo(doorFrame)
            door.find("**/doorFrameHoleRight").wrtReparentTo(doorFrame)
            doorFrame.node().setEffect(DecalEffect.make())

            door.find("**/leftDoor").wrtReparentTo(parent)
            door.find("**/rightDoor").wrtReparentTo(parent)
        else:
            # Note: the factory interior has a dynamically allocated zone but
            # that is ok because we do not need to load any models - they all
            # get loaded by the distributed object
            self.notify.warning("loadPlaceGeom: unclassified zone %s" % zoneId)
            
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId)
    

    def unload(self):
        CogHQLoader.CogHQLoader.unload(self)
        # unload anims
        Toon.unloadSellbotHQAnims()


    def enterFactoryExterior(self, requestStatus):
        self.placeClass = FactoryExterior.FactoryExterior
        self.enterPlace(requestStatus)
        self.hood.spawnTitleText(requestStatus['zoneId'])
        
    def exitFactoryExterior(self):
        taskMgr.remove("titleText")
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None

    def enterFactoryInterior(self, requestStatus):
        self.placeClass = FactoryInterior.FactoryInterior
        self.enterPlace(requestStatus)
        
    def exitFactoryInterior(self):
        self.exitPlace()
        self.placeClass = None

    def getExteriorPlaceClass(self):
        return SellbotHQExterior.SellbotHQExterior

    def getBossPlaceClass(self):
        return SellbotHQBossBattle.SellbotHQBossBattle


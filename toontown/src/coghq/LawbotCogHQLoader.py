
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import CogHQLoader
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
import StageInterior
import LawbotHQExterior
import LawbotHQBossBattle
import LawbotOfficeExterior

# Used to compensate for scaling of Cog tunnel sign's
# original aspect ratio of 1125x813 to a uniform ratio,
# scale z by factor of 0.7227
aspectSF = 0.7227

class LawbotCogHQLoader(CogHQLoader.CogHQLoader):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("LawbotCogHQLoader")
    #notify.setDebug(True)

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        
        self.fsm.addState(State.State('stageInterior',
                                      self.enterStageInterior,
                                      self.exitStageInterior,
                                      ['quietZone',
                                       'cogHQExterior', # Tunnel
                                       ]))
        self.fsm.addState(State.State('factoryExterior',
                                      self.enterFactoryExterior,
                                      self.exitFactoryExterior,
                                      ['quietZone',
                                       'cogHQExterior', # Tunnel
                                       ]))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('stageInterior')
        for stateName in ['quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('factoryExterior')
        
        self.musicFile = "phase_11/audio/bgm/LB_courtyard.mid"

        self.cogHQExteriorModelPath = "phase_11/models/lawbotHQ/LawbotPlaza"
        #self.cogHQExteriorModelPath = "../../ttmodels.src/src/lawbotHQ/LawbotPlaza.mb"
        self.factoryExteriorModelPath = "phase_11/models/lawbotHQ/LB_DA_Lobby"
        #self.factoryExteriorModelPath = "../../ttmodels.src/src/lawbotHQ/LB_DA_Lobby.mb"
        self.cogHQLobbyModelPath = "phase_11/models/lawbotHQ/LB_CH_Lobby"
        #self.cogHQLobbyModelPath = "../../ttmodels.src/src/lawbotHQ/LB_CH_Lobby.mb"
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

        self.notify.debug("zoneId = %d ToontownGlobals.LawbotHQ=%d" % (zoneId,ToontownGlobals.LawbotHQ))
            
        if zoneId == ToontownGlobals.LawbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)

            # make sure the reflective floor renders properly
            ug = self.geom.find("**/underground")
            ug.setBin( "ground", -10)
            
            # Rename the link tunnels so they will hook up properly
            brLinkTunnel = self.geom.find("**/TunnelEntrance1")


            #RAU 
            brLinkTunnel.setName("linktunnel_br_3326_DNARoot")
            """
            factoryLinkTunnel = self.geom.find("**/Tunnel2")

            factoryLinkTunnel.ls()
            factoryLinkTunnel.setName("linktunnel_lawhq_13200_DNARoot")
            ##factoryLinkTunnel.setName("linktunnel_sellhq_11200_DNARoot")
 

            # Put handy signs on the link tunnels
            cogSignModel = loader.loadModel(
                'phase_4/models/props/sign_sellBotHeadHQ')
            cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
            cogSignSF = 23

            # To The Brrrgh
            dgSign = cogSign.copyTo(brLinkTunnel)
            dgSign.setPosHprScale(
                0.00, -291.5, 29,
                180.00, 0.00, 0.00,
                cogSignSF, cogSignSF, cogSignSF * aspectSF)
            dgSign.node().setEffect(DecalEffect.make())
            dgText = DirectGui.OnscreenText(
                text = TTLocalizer.TheBrrrgh[-1],
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.3), scale = 0.1,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = dgSign)
            dgText.setDepthWrite(0)

            # To Office
            factorySign = cogSign.copyTo(factoryLinkTunnel)
            factorySign.setPosHprScale(
                148.625, -155, 27,
                -90.00, 0.00, 0.00,
                cogSignSF, cogSignSF, cogSignSF * aspectSF)
            # Make text a decal
            factorySign.node().setEffect(DecalEffect.make())
            factoryTypeText = DirectGui.OnscreenText(
                text = TTLocalizer.Lawbot,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.25), scale = .075,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = factorySign)
            factoryTypeText.setDepthWrite(0)
            factoryText = DirectGui.OnscreenText(
                text = TTLocalizer.Office,
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
            """
            """
            # fix up the door node names
            door0 = self.geom.find("**/LB_DA_door_0")
            door0.setName("door_0")
            door1 = self.geom.find("**/LB_CR_door_1")
            door1.setName("door_1")
            door1.find("door_trigger_0").setName("door_trigger_1")
            door1.find("door_origin_0").setName("door_origin_1")
            """
            
        elif zoneId == ToontownGlobals.LawbotOfficeExt:
            self.geom = loader.loadModel(self.factoryExteriorModelPath)

            # make sure the reflective floor renders properly
            ug = self.geom.find("**/underground")
            ug.setBin( "ground", -10)

            """
            factoryLinkTunnel = self.geom.find("**/tunnel_group2")
            factoryLinkTunnel.setName("linktunnel_lawhq_13000_DNARoot")
            factoryLinkTunnel.find("**/tunnel_sphere").setName("tunnel_trigger")

            # Put handy signs on the link tunnels
            cogSignModel = loader.loadModel(
                'phase_4/models/props/sign_sellBotHeadHQ')
            cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
            cogSignSF = 23
            elevatorSignSF = 15

            # To Lawbot HQ
            hqSign = cogSign.copyTo(factoryLinkTunnel)
            hqSign.setPosHprScale(
                0.0, -353, 27.5,
                -180.00, 0.00, 0.00,
                cogSignSF, cogSignSF, cogSignSF * aspectSF)
            hqSign.node().setEffect(DecalEffect.make())
            hqTypeText = DirectGui.OnscreenText(
                text = TTLocalizer.Lawbot,
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
                text = TTLocalizer.Office,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.25), scale = .075,
                # required for DecalEffect (must be a GeomNode, not a TextNode)
                mayChange=False,
                parent = fdSign)
            fdTypeText.setDepthWrite(0)
            fdText = DirectGui.OnscreenText(
                text = TTLocalizer.SellbotFrontEntrance,
                font = ToontownGlobals.getSuitFont(),
                pos = (0,-0.34), scale = TTLocalizer.LCLdgSign,
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
                text = TTLocalizer.Office,
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
            """
        elif zoneId == ToontownGlobals.LawbotLobby:
            self.notify.debug("cogHQLobbyModelPath = %s" % self.cogHQLobbyModelPath)
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)

            # make sure the reflective floor renders properly
            ug = self.geom.find("**/underground")
            ug.setBin( "ground", -10)

            """
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
            """
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
        return LawbotHQExterior.LawbotHQExterior

    def getBossPlaceClass(self):
        self.notify.debug("getBossPlaceClass")
        return LawbotHQBossBattle.LawbotHQBossBattle
        
    def enterFactoryExterior(self, requestStatus):
        self.placeClass = LawbotOfficeExterior.LawbotOfficeExterior
        self.enterPlace(requestStatus)
        self.hood.spawnTitleText(requestStatus['zoneId'])
        
    def exitFactoryExterior(self):
        taskMgr.remove("titleText")
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None

    def enterCogHQBossBattle(self, requestStatus):
        self.notify.debug("LawbotCogHQLoader.enterCogHQBossBattle")
        CogHQLoader.CogHQLoader.enterCogHQBossBattle(self, requestStatus)
        base.cr.forbidCheesyEffects(1)
        
    def exitCogHQBossBattle(self):
        self.notify.debug("LawbotCogHQLoader.exitCogHQBossBattle")
        CogHQLoader.CogHQLoader.exitCogHQBossBattle(self)
        base.cr.forbidCheesyEffects(0)        
        




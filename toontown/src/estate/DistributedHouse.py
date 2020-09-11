from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from toontown.minigame.OrthoWalk import *
from string import *
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.toon import Toon
from direct.showbase import RandomNumGen
from toontown.toonbase import TTLocalizer
import random
from direct.showbase import PythonUtil
from toontown.hood import Place
import HouseGlobals
from toontown.building import ToonInteriorColors
from direct.showbase.MessengerGlobal import messenger

class DistributedHouse(DistributedObject.DistributedObject):
    """
    This is the house object on the client
    """
    notify = directNotify.newCategory("DistributedHouse")

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.houseType = None
        self.avId = -1
        self.ownerId = 0
        self.colorIndex = 0
        self.house = None
        self.name = ""
        self.namePlate = None
        self.nameText = None
        self.nametag = None
        self.floorMat = None
        self.matText = None
        self.randomGenerator = None
        self.housePosInd = 0
        self.house_loaded = 0

    def disable(self):
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.notify.debug("delete")
        self.unload()
        self.clearNametag()
        if self.namePlate:
            self.namePlate.removeNode()
            del self.namePlate
            self.namePlate = None
        if self.floorMat:
            self.floorMat.removeNode()
            del self.floorMat
            self.floorMat = None
        if self.house:
            self.house.removeNode()
            del self.house
        self.house_loaded = 0
        del self.randomGenerator
        DistributedObject.DistributedObject.delete(self)

    def clearNametag(self):
        if self.nametag != None:
            self.nametag.unmanage(base.marginManager)
            self.nametag.setAvatar(NodePath())
            self.nametag = None

    def load(self):        
        self.notify.debug("load")

        # Load the house once.  When we walk in a door, the house model will automatically
        # get hidden by the EstateLoader.  Only remove the house node on deletion
        if not self.house_loaded:
            if self.housePosInd == 1:
                houseModelIndex = base.config.GetInt('want-custom-house',HouseGlobals.HOUSE_DEFAULT)
            else:
                houseModelIndex = HouseGlobals.HOUSE_DEFAULT
            houseModelIndex = base.config.GetInt('want-custom-house-all',houseModelIndex)
            houseModel = self.cr.playGame.hood.loader.houseModels[houseModelIndex]
            self.house = houseModel.copyTo(self.cr.playGame.hood.loader.houseNode[self.housePosInd])
            self.house_loaded = 1

            # fill out the houseId2house dict in estateLoader
            self.cr.playGame.hood.loader.houseId2house[self.doId] = self.house

            # make it pretty
            if houseModelIndex == HouseGlobals.HOUSE_DEFAULT:
                self.__setHouseColor()

            # make it functional
            if houseModelIndex == HouseGlobals.HOUSE_DEFAULT:
                self.__setupDoor()
            else:
                pass
                self.__setupDoorCustom()

            messenger.send("houseLoaded-%d" % self.doId)

    def announceGenerate(self):
        assert(self.notify.debug("announceGenerate()"))
        DistributedObject.DistributedObject.announceGenerate(self)
        messenger.send("setBuilding-"+str(self.doId))

    def __setupDoor(self):
        self.notify.debug("setupDoor")
        self.dnaStore=self.cr.playGame.dnaStore
        doorModelName="door_double_round_ul" # hack  zzzzzzz
        # Switch leaning of the door:
        if doorModelName[-1:] == "r":
            doorModelName=doorModelName[:-1]+"l"
        else:
            doorModelName=doorModelName[:-1]+"r"
        door=self.dnaStore.findNode(doorModelName)
        # Determine where should we put the door:
        door_origin=self.house.find("**/door_origin")
        door_origin.setHpr(90,0,0)
        door_origin.setScale(.6,.6,.8)
        door_origin.setPos(door_origin, 0.5, 0, 0.0)
        doorNP=door.copyTo(door_origin)
        assert(not doorNP.isEmpty())
        assert(not door_origin.isEmpty())
        self.door_origin = door_origin
        self.randomGenerator=random.Random()
        self.randomGenerator.seed(self.doId)
        #houseColor = HouseGlobals.houseColors[self.housePosInd]
        houseColor = HouseGlobals.stairWood
        color = Vec4(houseColor[0], houseColor[1], houseColor[2], 1)
        #self.colors=ToonInteriorColors.colors[ToontownGlobals.MyEstate]
        #color=self.randomGenerator.choice(self.colors["TI_door"])
        DNADoor.setupDoor(doorNP,
                          door_origin, door_origin,
                          self.dnaStore,
                          str(self.doId), color)

        # put our name above the door
        # SDN: this might change to be on the mailbox
        self.__setupNamePlate()
        self.__setupFloorMat()
        self.__setupNametag()


    def __setupDoorCustom(self):
        """Setup the door for the new house types, e.g. tiki house."""
        self.randomGenerator=random.Random()
        self.randomGenerator.seed(self.doId)
        self.notify.debug("setupDoorCustom")
        self.dnaStore=self.cr.playGame.dnaStore
        door=self.house.find('**/door_0')
        door_origin=self.house.find("**/door_origin")

        door_origin.setHpr(90,0,0)
        door_origin.setScale(.6,.6,.8)

        doorNP = door

        assert(not doorNP.isEmpty())
        assert(not door_origin.isEmpty())
        self.door_origin = door_origin
        color = Vec4(1,1,1,1)

        #import pdb; pdb.set_trace()
        parent = door_origin
        rightDoor = door.find('**/rightDoor')
        rightDoor.setHpr(door_origin, Vec3(0,0,0))
        leftDoor = door.find('**/leftDoor')
        leftDoor.setHpr(door_origin, Vec3(0,0,0))

        doorTrigger = doorNP.find('**/door_*_trigger')
        doorTrigger.wrtReparentTo(door_origin)
        doorTrigger.node().setName("door_trigger_" + str(self.doId))

        self.__setupFloorMat(changeColor = False)
        self.__setupNametag()
        self.__setupNamePlateCustom()

    def __setupNamePlate(self):
        self.notify.debug("__setupNamePlate")

        # name plate above door
        if self.namePlate:
            self.namePlate.removeNode()
            del self.namePlate
            self.namePlate = None

        nameText = TextNode('nameText')
        r = self.randomGenerator.random()
        g = self.randomGenerator.random()
        b = self.randomGenerator.random()
        nameText.setTextColor(r,g,b,1)
        nameText.setAlign(nameText.ACenter)
        nameText.setFont(ToontownGlobals.getBuildingNametagFont())
        nameText.setShadowColor(0, 0, 0, 1)
        nameText.setBin('fixed')
        if TTLocalizer.BuildingNametagShadow:
            nameText.setShadow(*TTLocalizer.BuildingNametagShadow)
        nameText.setWordwrap(16.0)
        xScale = 1.0
        numLines = 0
        if (self.name == ""):
            # don't bother putting an empty string up
            return
        else:
            # make the name fit nicely on the floor mat
            houseName = TTLocalizer.AvatarsHouse % TTLocalizer.GetPossesive(self.name)

        nameText.setText(houseName)
        self.nameText = nameText

        # Since the text is wordwrapped, it may flow over more
        # than one line.  Try to adjust the scale and position of
        # the sign accordingly.
        textHeight = nameText.getHeight() - 2
        textWidth = nameText.getWidth()
        xScale = 1.0
        if textWidth > 16:
            xScale = 16.0 / textWidth

        sign_origin = self.house.find("**/sign_origin")
        pos = sign_origin.getPos()
        sign_origin.setPosHpr(pos[0],pos[1],pos[2]+.15*textHeight,90,0,0)
        self.namePlate = sign_origin.attachNewNode(self.nameText)
        self.namePlate.setDepthWrite(0)
        self.namePlate.setPos(0,-0.05,0)
        self.namePlate.setScale(xScale)

        return nameText

    def __setupFloorMat(self, changeColor = True):

        if self.floorMat:
            self.floorMat.removeNode()
            del self.floorMat
            self.floorMat = None

        mat = self.house.find("**/mat")
        if changeColor:
            mat.setColor(0.400, 0.357, 0.259, 1.000)

        color = HouseGlobals.houseColors[self.housePosInd]

        matText = TextNode('matText')
        matText.setTextColor(color[0], color[1], color[2], 1)
        matText.setAlign(matText.ACenter)
        matText.setFont(ToontownGlobals.getBuildingNametagFont())
        matText.setShadowColor(0, 0, 0, 1)
        matText.setBin('fixed')
        if TTLocalizer.BuildingNametagShadow:
            matText.setShadow(*TTLocalizer.BuildingNametagShadow)
        matText.setWordwrap(10.0)
        xScale = 1.0
        numLines = 0
        if (self.name == ""):
            # don't bother putting an empty string up
            return
        else:
            # make the name fit nicely on the floor mat
            houseName = TTLocalizer.AvatarsHouse % TTLocalizer.GetPossesive(self.name)

        matText.setText(houseName)
        self.matText = matText

        # Since the text is wordwrapped, it may flow over more
        # than one line.  Try to adjust the scale and position of
        # the sign accordingly.
        textHeight = matText.getHeight() - 2
        textWidth = matText.getWidth()
        xScale = 1.0
        if textWidth > 8:
            xScale = 8.0 / textWidth
        mat_origin = self.house.find("**/mat_origin")
        pos = mat_origin.getPos()
        mat_origin.setPosHpr(pos[0]-.15*textHeight,pos[1],pos[2],90,-90,0)
        self.floorMat = mat_origin.attachNewNode(self.matText)
        self.floorMat.setDepthWrite(0)
        self.floorMat.setPos(0,-.025,0)
        self.floorMat.setScale(.45*xScale)

    def __setupNametag(self):
        # set up the nametag
        if self.nametag:
            self.clearNametag()

        if (self.name == ""):
            houseName = ""
        else:
            houseName = TTLocalizer.AvatarsHouse % TTLocalizer.GetPossesive(self.name)
        self.nametag = NametagGroup()
        self.nametag.setFont(ToontownGlobals.getBuildingNametagFont())
        if TTLocalizer.BuildingNametagShadow:
            self.nametag.setShadow(*TTLocalizer.BuildingNametagShadow)
        self.nametag.setContents(Nametag.CName)
        self.nametag.setColorCode(NametagGroup.CCHouseBuilding)
        self.nametag.setActive(0)
        self.nametag.setAvatar(self.house)
        self.nametag.setObjectCode(self.doId)
        self.nametag.setName(houseName)
        self.nametag.manage(base.marginManager)

    def unload(self):
        self.notify.debug("unload")
        # Ignore all events we might have accepted
        self.ignoreAll()

    def setHouseReady(self):
        # the server has given us all the info we need to load the house
        self.notify.debug("setHouseReady")
        try:
            self.House_initialized
        except:
            self.House_initialized = 1
            self.load()

    def setHousePos(self, index):
        self.notify.debug("setHousePos")
        self.housePosInd = index
        self.__setHouseColor()

    def setHouseType(self, index):
        self.notify.debug("setHouseType")
        self.houseType = index

    def setFavoriteNum(self, index):
        self.notify.debug('setFavoriteNum')
        self.favoriteNum = index

    def __setHouseColor(self):
        if self.house:

            bwall = self.house.find("**/*back")
            rwall = self.house.find("**/*right")
            fwall = self.house.find("**/*front")
            lwall = self.house.find("**/*left")

            kd = .8
            color = HouseGlobals.houseColors[self.colorIndex]
            dark = (kd*color[0], kd*color[1], kd*color[2])
            if not bwall.isEmpty():
                bwall.setColor(color[0], color[1], color[2], 1)
            if not fwall.isEmpty():
                fwall.setColor(color[0], color[1], color[2], 1)
            if not rwall.isEmpty():
                rwall.setColor(dark[0], dark[1], dark[2], 1)
            if not lwall.isEmpty():
                lwall.setColor(dark[0], dark[1], dark[2], 1)

            # set attic color on pink, and yellow houses

            aColor = HouseGlobals.atticWood
            attic = self.house.find("**/attic")
            if not attic.isEmpty():
                attic.setColor(aColor[0], aColor[1], aColor[2], 1)

            # chimney
            color = HouseGlobals.houseColors2[self.colorIndex]
            chimneyList = self.house.findAllMatches("**/chim*")
            for chimney in chimneyList:
                chimney.setColor(color[0],color[1],color[2], 1)

    def setAvId(self, id):
        self.avId = id

    def setAvatarId(self, avId):
        self.notify.debug("setAvatarId = %s" % avId)
        self.ownerId = avId

    def getAvatarId(self):
        self.notify.debug("getAvatarId")
        return self.ownerId

    def setName(self, name):
        self.name = name
        # name plate has changed, so change the name
        if (self.nameText and
            self.nameText.getText() != self.name):
            if self.name == "":
                self.nameText.setText("")
            else:
                self.nameText.setText(self.name+"'s\n House")

    def getName(self):
        return self.name

    def b_setColor(self, colorInd):
        self.setColor(colorInd)
        self.d_setColor(colorInd)

    def d_setColor(self, colorInd):
        self.sendUpdate("setColor", [colorInd])

    def setColor(self, colorInd):
        self.colorIndex = colorInd
        if self.house:
            self.__setHouseColor()

    def getColor(self):
        return self.colorIndex

    def __setupNamePlateCustom(self):
        self.notify.debug("__setupNamePlateCustom")

        # name plate above door
        if self.namePlate:
            self.namePlate.removeNode()
            del self.namePlate
            self.namePlate = None

        nameText = TextNode('nameText')
        nameText.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
        nameText.setCardDecal(True)
        nameText.setCardColor(1.0, 1.0, 1.0, 0.0)

        r = self.randomGenerator.random()
        g = self.randomGenerator.random()
        b = self.randomGenerator.random()
        nameText.setTextColor(r,g,b,1)
        nameText.setAlign(nameText.ACenter)
        nameText.setFont(ToontownGlobals.getBuildingNametagFont())
        nameText.setShadowColor(0, 0, 0, 1)
        nameText.setBin('fixed')
        if TTLocalizer.BuildingNametagShadow:
            nameText.setShadow(*TTLocalizer.BuildingNametagShadow)
        nameText.setWordwrap(16.0)
        xScale = 1.0
        numLines = 0
        if (self.name == ""):
            # don't bother putting an empty string up
            return
        else:
            # make the name fit nicely on the floor mat
            houseName = TTLocalizer.AvatarsHouse % TTLocalizer.GetPossesive(self.name)

        nameText.setText(houseName)
        self.nameText = nameText

        # Since the text is wordwrapped, it may flow over more
        # than one line.  Try to adjust the scale and position of
        # the sign accordingly.
        textHeight = nameText.getHeight() - 2
        textWidth = nameText.getWidth()
        xScale = 1.0
        if textWidth > 16:
            xScale = 16.0 / textWidth

        sign_origin = self.house.find("**/sign_origin")
        #debugAxis = loader.loadModel("models/misc/xyzAxis")
        #debugAxis.reparentTo(sign_origin)
        #debugAxis.wrtReparentTo(render)
        pos = sign_origin.getPos()
        sign_origin.setPosHpr(pos[0],pos[1],pos[2]+.15*textHeight,90,0,0)
        self.namePlate = sign_origin.attachNewNode(self.nameText)
        self.namePlate.setDepthWrite(0)
        self.namePlate.setPos(0,-0.05,0)
        self.namePlate.setScale(xScale)

        return nameText

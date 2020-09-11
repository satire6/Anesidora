from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import math
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.toon import Toon
from direct.showbase import RandomNumGen
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
import random
import cPickle
import time
from direct.showbase import PythonUtil
from toontown.hood import Place
import Estate
import HouseGlobals
from toontown.estate import GardenGlobals
from toontown.estate import DistributedFlower
from toontown.estate import DistributedGagTree
from toontown.estate import DistributedStatuary
import GardenDropGame
import GardenProgressMeter
from toontown.estate import FlowerSellGUI
from toontown.toontowngui import TTDialog

class DistributedEstate(DistributedObject.DistributedObject):
    """
    This is the estate object on the client
    """
    notify = directNotify.newCategory("DistributedEstate")

    if __debug__:
        GardenGlobals.validateRecipes(notify)
        GardenGlobals.validatePlantAttributes(notify)

    def __init__(self, cr):
        assert(self.notify.debug("__init__"))
        DistributedObject.DistributedObject.__init__(self, cr)
        # keep track of closest house, so we can set it's color
        self.closestHouse = 0
        self.ground = None
        self.dayTrack = None
        self.sunTrack = None
        self.airplane = None
        self.flowerSellBox = None
        self.estateDoneEvent = "estateDone"

        self.load()
        
        # Initialize the camera and play the intro camera lerp track
        # The positions of the avatars must be calculated by this point
        self.initCamera()

        #testFlower = DistributedFlower.DistributedFlower()
        #testGagTree = DistributedGagTree.DistributedGagTree()
        #testStatuary = DistributedStatuary.DistributedStatuary()
        
        self.plotTable = []
        self.idList = [] #list of toon ids in this estate
        base.estate = self
        self.flowerGuiDoneEvent = "flowerGuiDone"        
        
    def disable(self):
        self.notify.debug("disable")
        self.__stopBirds()
        self.__stopCrickets()
        DistributedObject.DistributedObject.disable(self)
        self.ignore('enterFlowerSellBox')

    def delete(self):
        self.notify.debug("delete")
        self.unload()
        DistributedObject.DistributedObject.delete(self)

    def load(self):
        assert(self.notify.debug("load"))

        self.lt = base.localAvatar
       
        # Load a witch for Halloween
        newsManager = base.cr.newsManager

        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds):
                self.loadWitch()
            else:
                 self.loadAirplane()
                 
        self.loadFlowerSellBox()
        # load music
        #self.music = base.loadMusic(self.bgm)
        # Start music
        #base.playMusic(self.music, looping = 1, volume = 1)

        # set the clear color to green to make it appear more grassy
        self.oldClear = base.win.getClearColor()
        base.win.setClearColor(Vec4(0.09, 0.55, 0.21, 1.0))
        
    def unload(self):
        assert(self.notify.debug("unload"))

        # Ignore all events we might have accepted
        self.ignoreAll()

        # restore the clear color
        base.win.setClearColor(self.oldClear)
        
        # Kill tasks
        self.__killAirplaneTask() 
        self.__killDaytimeTask()
        self.__stopBirds()
        self.__stopCrickets()

        if self.dayTrack:
            self.dayTrack.pause()
            self.dayTrack = None

        self.__killSunTask()
        if self.sunTrack:
            self.sunTrack.pause()
            self.sunTrack = None

        #if (self.estateType and self.estateType == 0):
        # Hide the ground
        if self.ground:
            self.ground.removeNode()
            del self.ground
            
        if self.airplane:
            self.airplane.removeNode()
            del self.airplane
            self.airplane = None

        if self.flowerSellBox:
            self.flowerSellBox.removeNode()
            del self.flowerSellBox
            self.flowerSellBox = None


        # Stop music
        #self.music.stop()
        #del self.music

    def announceGenerate(self):
        assert(self.notify.debug("announceGenerate()"))
        DistributedObject.DistributedObject.announceGenerate(self)
        #self.startGame()
        self.accept('gardenGame', self.startGame)        
        
    def startGame(self):
        pass
        self.game = GardenDropGame.GardenDropGame()

    def loadAirplane(self):
        assert(self.notify.debug("loadAirplane"))
        self.airplane = loader.loadModel("phase_4/models/props/airplane.bam")
        self.airplane.setScale(4)
        self.airplane.setPos(0,0,1)
        #self.airplane.setBillboardPointEye()
        
        self.banner = self.airplane.find("**/*banner")
        bannerText = TextNode('bannerText')
        bannerText.setTextColor(1,0,0,1)
        bannerText.setAlign(bannerText.ACenter)
        bannerText.setFont(ToontownGlobals.getSignFont())
        bannerText.setText("Cog invasion!!!")
        self.bn = self.banner.attachNewNode(bannerText.generate())
        self.bn.setHpr(180,0,0)
        self.bn.setPos(-1.8,.1,0)
        self.bn.setScale(.35)
        self.banner.hide()

    # plane becomes a witch during halloween
    def loadWitch(self):
        if not self.airplane:
            self.airplane = loader.loadModel("phase_4/models/props/tt_m_prp_ext_flyingWitch.bam")
            
        def __replaceAirplane__():
            self.airplane.reparentTo(hidden)
            del self.airplane

            self.airplane = loader.loadModel("phase_4/models/props/tt_m_prp_ext_flyingWitch.bam")
            self.airplane.setScale(2)
            self.airplane.setPos(0,0,1)

            bannerText = TextNode('bannerText')
            bannerText.setTextColor(1,0,0,1)
            bannerText.setAlign(bannerText.ACenter)
            bannerText.setFont(ToontownGlobals.getSignFont())
            bannerText.setText("Happy halloween!!!")
            self.bn = self.airplane.attachNewNode(bannerText.generate())
            self.bn.setHpr(0,0,0)
            self.bn.setPos( 20.0, -.1, 0)
            self.bn.setScale(2.35)
        replacement = Sequence(
                LerpColorScaleInterval(
                    self.airplane,
                    0.1, Vec4(1, 1, 1, 0)
                ),
                Func(__replaceAirplane__),
                LerpColorScaleInterval(
                    self.airplane,
                    0.1, Vec4(1, 1, 1, 1)
                ),
        )
        
        replacement.start()
        
    def unloadWitch(self):
        def __replaceWitch__():
            self.airplane.reparentTo(hidden)
            del self.airplane
            del self.bn
            
            self.airplane = loader.loadModel("phase_4/models/props/airplane.bam")
            self.airplane.setScale(4)
            self.airplane.setPos(0,0,1)

            self.banner = self.airplane.find("**/*banner")
            bannerText = TextNode('bannerText')
            bannerText.setTextColor(1,0,0,1)
            bannerText.setAlign(bannerText.ACenter)
            bannerText.setFont(ToontownGlobals.getSignFont())
            bannerText.setText("Happy halloween!!!")
            self.bn = self.banner.attachNewNode(bannerText.generate())
            self.bn.setHpr(180,0,0)
            self.bn.setPos(-1.8,.1,0)
            self.bn.setScale(.35)
            self.banner.hide()

        replacement = Sequence(
                LerpColorScaleInterval(
                    self.airplane,
                    0.1, Vec4(1, 1, 1, 0)
                ),
                Func(__replaceWitch__),
                LerpColorScaleInterval(
                    self.airplane,
                    0.1, Vec4(1, 1, 1, 1)
                ),
        )
        
        replacement.start()
        
    def initCamera(self):
        # set up the camera
        initCamPos = VBase3(0, -10, 5)
        initCamHpr = VBase3(0, -10, 0)

    def setEstateType(self, index):
        self.estateType = index
        
    def setHouseInfo(self, houseInfo):
        self.notify.debug("setHouseInfo")
        houseType, housePos = cPickle.loads(houseInfo)
        self.loadEstate(houseType, housePos)

    def loadEstate(self, indexList, posList):
        self.notify.debug("loadEstate")
        self.houseType = indexList
        self.housePos = posList
        self.numHouses = len(self.houseType)
        self.house = [None] * self.numHouses

        
    def __startAirplaneTask(self):
        self.theta = 0
        self.phi = 0
        taskMgr.remove(self.taskName("estate-airplane"))
        taskMgr.add(self.airplaneFlyTask,
                    self.taskName("estate-airplane"))
        
    def __pauseAirplaneTask(self):
        # pause time
        pause = 45
        # reset the phi, so sin(phi) doesn't go below zero
        self.phi = 0
        # advance theta so it looks like we took off from a different than we landed
        # and mod it so it doesn't grow absurdly large
        self.airplane.hide()
        self.theta = (self.theta + 10) % 360
        taskMgr.remove(self.taskName("estate-airplane"))
        taskMgr.doMethodLater(pause, self.airplaneFlyTask,
                              self.taskName("estate-airplane"))
        
    def __killAirplaneTask(self):
        assert(self.notify.debug("__killAirplaneTask"))
        taskMgr.remove(self.taskName("estate-airplane"))
        
    def airplaneFlyTask(self, task):
        rad = 300.0
        amp = 80.0
        self.theta += .25
        self.phi += .005
        sinPhi = math.sin(self.phi)
        if (sinPhi <= 0):
            # stop the plane for a bit while it is low
            self.__pauseAirplaneTask()
            
        angle = math.pi * self.theta/180.0
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        z = amp * sinPhi
        self.airplane.reparentTo(render)
        self.airplane.setH(90+self.theta+180)
        self.airplane.setPos(x,y,z)
        return Task.cont
        
    def sendHouseColor(self, index, r,g,b,a):
        self.house[index].setColor(r,g,b,a)

    def setTreasureIds(self, doIds):
        self.flyingTreasureId = []
        for id in doIds:
            self.flyingTreasureId.append(id)

    def setDawnTime(self, ts):
        self.notify.debug("setDawnTime")
        self.dawnTime = ts
        # send a request to the server to get it's time
        self.sendUpdate("requestServerTime",[])
        
    def setServerTime(self, ts):
        self.notify.debug("setServerTime")
        # the server is telling us what time it has
        self.serverTime = ts

        # mark our the time on the client
        self.clientTime = time.time() % HouseGlobals.DAY_NIGHT_PERIOD

        # calculate the difference between the server and client clocks
        self.deltaTime = self.clientTime - self.serverTime

        # now that we know the deltaTime we can start the sun/moon and airplane tasks
        if base.dayNightEnabled:
            self.__initDaytimeTask()
            self.__initSunTask()
        self.__startAirplaneTask()
        
    def getDeltaTime(self):
        curTime = time.time() % HouseGlobals.DAY_NIGHT_PERIOD
        dawnTime = self.dawnTime
        dT = ((curTime - dawnTime) - self.deltaTime) % HouseGlobals.DAY_NIGHT_PERIOD
        print ("getDeltaTime = %s. curTime=%s. dawnTime=%s. serverTime=%s.  deltaTime=%s" % (dT,curTime,dawnTime,self.serverTime,self.deltaTime))
        return dT
        
    def __initDaytimeTask(self):
        # only call this fcn the first time, in order to pass the timestamp
        self.__killDaytimeTask()
        task = Task(self.__dayTimeTask)

        # figure out how far into the task we are (how far from dawn)
        dT = self.getDeltaTime()
        task.ts = dT
        taskMgr.add(task,
                    self.taskName("daytime"))

    def __killDaytimeTask(self):
        assert(self.notify.debug("__killDaytimeTask"))
        taskMgr.remove(self.taskName("daytime"))
        
    def __dayTimeTask(self, task):
        # a full day is from t=[0,HouseGlobals.DAY_NIGHT_PERIOD]
        taskName = self.taskName("daytime")
        track = Sequence(Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom,
                                                          HouseGlobals.HALF_DAY_PERIOD, Vec4(1,.6,.6,1)),
                                   LerpColorScaleInterval(base.cr.playGame.hood.sky,
                                                          HouseGlobals.HALF_DAY_PERIOD, Vec4(1,.8,.8,1)),
                                   ), # go to sunset
                         Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom,
                                                         HouseGlobals.HALF_NIGHT_PERIOD, Vec4(.2,.2,.5,1)),
                                  LerpColorScaleInterval(base.cr.playGame.hood.sky,
                                                         HouseGlobals.HALF_NIGHT_PERIOD, Vec4(.4,.4,.6,1)),
                                  ), # go to night
                         Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom,
                                                         HouseGlobals.HALF_NIGHT_PERIOD, Vec4(.6,.6,.8,1)),
                                  LerpColorScaleInterval(base.cr.playGame.hood.sky,
                                                         HouseGlobals.HALF_NIGHT_PERIOD, Vec4(.7,.7,.8,1)),
                                  ), # go to sunrise
                         Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom,
                                                         HouseGlobals.HALF_DAY_PERIOD, Vec4(1,1,1,1)),
                                  LerpColorScaleInterval(base.cr.playGame.hood.sky,
                                                         HouseGlobals.HALF_DAY_PERIOD, Vec4(1,1,1,1)),
                                  ),# go to day
                         Func(base.cr.playGame.hood.loader.geom.clearColorScale),
                         Func(base.cr.playGame.hood.sky.clearColorScale),
                         )
        
        if self.dayTrack:
            self.dayTrack.finish()
        self.dayTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
        print "ts=%s" % ts
        self.dayTrack.start(ts)
        taskMgr.doMethodLater(HouseGlobals.DAY_NIGHT_PERIOD-ts,
                              self.__dayTimeTask,
                              self.taskName("daytime"))
        return Task.done

    def __initSunTask(self):
        # only call this fcn the first time, in order to pass the timestamp
        self.__killSunTask()
        task = Task(self.__sunTask)
        dT = self.getDeltaTime()
        task.ts = dT
        taskMgr.add(task,
                    self.taskName("sunTask"))

    def __killSunTask(self):
        assert(self.notify.debug("__killSunTask"))
        taskMgr.remove(self.taskName("sunTask"))
        
    def __sunTask(self, task):
        sunMoonNode = base.cr.playGame.hood.loader.sunMoonNode
        sun = base.cr.playGame.hood.loader.sun
        h = 30 # the height of sun/moon
        halfPeriod = HouseGlobals.DAY_NIGHT_PERIOD / 2.0
        track = Sequence(Parallel(LerpHprInterval(sunMoonNode, HouseGlobals.HALF_DAY_PERIOD,
                                               Vec3(0, 0, 0)),
                               LerpColorScaleInterval(sun, HouseGlobals.HALF_DAY_PERIOD,
                                                      Vec4(1,1,.5,1))), # to sunset
                         Func(sun.clearColorScale),
                         Func(self.__stopBirds),
                         LerpHprInterval(sunMoonNode, .2,
                                         Vec3(0, -h-3, 0)),
                         LerpHprInterval(sunMoonNode, .1,
                                         Vec3(0, -h+2, 0)),
                         LerpHprInterval(sunMoonNode, .1,
                                         Vec3(0, -h-1.5, 0)),
                         LerpHprInterval(sunMoonNode, .1,
                                         Vec3(0, -h, 0)),  # to night
                         Func(self.notify.debug, "night"),
                         Wait(HouseGlobals.HALF_NIGHT_PERIOD-.5),
                         LerpHprInterval(sunMoonNode, HouseGlobals.HALF_NIGHT_PERIOD,
                                         Vec3(0, 0, 0)),   # to sunrise
                         Func(self.__startBirds),
                         LerpHprInterval(sunMoonNode, .2,
                                         Vec3(0, h+3, 0)),
                         LerpHprInterval(sunMoonNode, .1,
                                         Vec3(0, h-2, 0)),
                         LerpHprInterval(sunMoonNode, .1,
                                         Vec3(0, h+1.5, 0)),
                         LerpHprInterval(sunMoonNode, .1,
                                         Vec3(0, h, 0)),  # to day
                         Func(self.notify.debug, "day"),
                         Func(sunMoonNode.setHpr, 0, h, 0),
                         Wait(HouseGlobals.HALF_DAY_PERIOD-.5)
                         )
                      
        if self.sunTrack:
            self.sunTrack.finish()
        self.sunTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
            # we might have already passed the stopBirds/startBirds calls in the
            # interval.  explicitly call them
            if (ts > HouseGlobals.HALF_DAY_PERIOD and
                ts < (HouseGlobals.DAY_NIGHT_PERIOD - HouseGlobals.HALF_DAY_PERIOD)):
                self.__stopBirds()
                self.__startCrickets()
            else:
                self.__stopCrickets()
                self.__startBirds()
        print "ts(sun)=%s" % ts
        self.sunTrack.start(ts)
        taskMgr.doMethodLater(HouseGlobals.DAY_NIGHT_PERIOD-ts,
                              self.__sunTask,
                              self.taskName("sunTask"))
        
        return Task.done

    def __stopBirds(self):
        taskMgr.remove('estate-birds')

    def __startBirds(self):
        self.__stopBirds()
        taskMgr.doMethodLater(1, self.__birds, 'estate-birds')
        
    def __birds(self, task):
        base.playSfx(random.choice(base.cr.playGame.hood.loader.birdSound))
        t = (random.random() * 20.0) + 1
        taskMgr.doMethodLater(t, self.__birds, 'estate-birds')
        return Task.done

    def __stopCrickets(self):
        taskMgr.remove('estate-crickets')

    def __startCrickets(self):
        self.__stopCrickets()
        taskMgr.doMethodLater(1, self.__crickets, 'estate-crickets')
        
    def __crickets(self, task):
        sfx = random.choice(base.cr.playGame.hood.loader.cricketSound)
        track = Sequence(Func(base.playSfx, sfx),
                         Wait(1))
        track.play()
        t = (random.random() * 20.0) + 1
        taskMgr.doMethodLater(t, self.__crickets, 'estate-crickets')
        return Task.done
        
    def getLastEpochTimeStamp(self):
        return self.lastEpochTimeStamp
        
    def setLastEpochTimeStamp(self, ts):
        self.lastEpochTimeStamp = ts
        
    def getIdList(self):
        return self.idList
        
    def setIdList(self, idList):
        self.idList = idList
        
    def loadFlowerSellBox(self):
        assert(self.notify.debug("loadFlowerSellBox"))
        self.flowerSellBox = loader.loadModel("phase_5.5/models/estate/wheelbarrel.bam")
        self.flowerSellBox.setPos(-142.586, 4.353, 0.025)
        self.flowerSellBox.reparentTo(render)
        
        colNode = self.flowerSellBox.find('**/collision')
        colNode.setName('FlowerSellBox')

        self.accept('enterFlowerSellBox', self.__touchedFlowerSellBox)        
        
    def __touchedFlowerSellBox(self,entry):
        #self.notify.debug('%s' % entry)
        #popup the gui only if it's our wheelbarrow and we have stuff to sell
        if base.localAvatar.doId in self.idList:
            if len(base.localAvatar.flowerBasket.flowerList):
                self.popupFlowerGUI()

    def __handleSaleDone(self, sell = 0):
        self.ignore(self.flowerGuiDoneEvent)
        # Ask the AI to complete the sale
        self.sendUpdate("completeFlowerSale", [sell])
        self.ignore('stoppedAsleep')
        self.flowerGui.destroy()
        self.flowerGui = None    

    def popupFlowerGUI(self):
        assert self.notify.debug('popupFlowerGUI()')
        #self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.flowerGuiDoneEvent, self.__handleSaleDone)
        self.flowerGui = FlowerSellGUI.FlowerSellGUI(self.flowerGuiDoneEvent)
        self.accept('stoppedAsleep', self.__handleSaleDone)
        
    def closedAwardDialog(self, value):
        self.awardDialog.destroy()
        base.cr.playGame.getPlace().detectedGardenPlotDone()

    def awardedTrophy(self, avId):
        if base.localAvatar.doId == avId:
            base.cr.playGame.getPlace().detectedGardenPlotUse()
            msg = TTLocalizer.GardenTrophyAwarded % \
                  (len(base.localAvatar.getFlowerCollection()),
                   GardenGlobals.getNumberOfFlowerVarieties())
            self.awardDialog = TTDialog.TTDialog(
                style = TTDialog.Acknowledge,
                text = msg,
                command = self.closedAwardDialog
                )
                
    def setClouds(self, clouds):
        self.clouds = clouds
        base.cr.playGame.hood.loader.setCloudSwitch(clouds)
        
    def getClouds(self):
        if hasattr(self, "clouds"):
            return self.clouds
        else:
            return 0

    def cannonsOver(self, arg=None):
        # Let the user know the cannon game is over
        base.localAvatar.setSystemMessage(0, TTLocalizer.EstateCannonGameEnd)

    def gameTableOver(self, arg = None):
        # Let the user know that the game table rental is over.
        base.localAvatar.setSystemMessage(0, TTLocalizer.GameTableRentalEnd)

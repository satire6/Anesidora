import math
import random
from pandac.PandaModules import NodePath, Point3, VBase4, TextNode, Vec3, deg2Rad, \
     CollisionSegment, CollisionHandlerQueue, CollisionNode, BitMask32, SmoothMover
from direct.fsm import FSM
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import Sequence, ProjectileInterval, Parallel, \
     LerpHprInterval, ActorInterval, Func, Wait, SoundInterval, LerpPosHprInterval, \
     LerpScaleInterval
from direct.gui.DirectGui import DGG, DirectButton, DirectLabel, DirectWaitBar
from direct.task import Task
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.coghq import BanquetTableBase
from toontown.coghq import DinerStatusIndicator
from toontown.battle import MovieUtil


class DistributedBanquetTable(DistributedObject.DistributedObject, FSM.FSM, BanquetTableBase.BanquetTableBase):
    """ This class represents a banquet table and the associated chairs,
    The DistributedBossbotBoss creates several of these of these for the CEO
    battle scene. """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBanquetTable')
    rotationsPerSeatIndex = [90, 90, 0, 0, -90, -90, 180, 180]
    #rotationsPerSeatIndex = [0, 0, 0, 0, 0, 0, 0, 0]

    pitcherMinH = -360
    pitcherMaxH = 360
    rotateSpeed = 30    # degrees per second

    # The number of seconds it takes to move the power meter to
    # full the first time.
    waterPowerSpeed = base.config.GetDouble('water-power-speed', 15)

    # The exponent that controls the factor at which the power
    # meter speeds up, see getWaterPower()
    waterPowerExponent = base.config.GetDouble('water-power-exponent', 0.75)

    useNewAnimations = True

    # if true we use the up & down arrow keys to determine water power
    # if false we use how long control is held down
    TugOfWarControls = False
    OnlyUpArrow = True
    if OnlyUpArrow:
        BASELINE_KEY_RATE = 3 # above this key rate, power increases    
    else:
        BASELINE_KEY_RATE = 6 # above this key rate, power increases
    UPDATE_KEY_PRESS_RATE_TASK      = "BanquetTableUpdateKeyPressRateTask"    

    YELLOW_POWER_THRESHOLD = 0.75
    RED_POWER_THRESHOLD = 0.97
    
    def __init__(self, cr):
        """Create a new banquet table."""
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedBanquetTable')
        self.boss = None
        self.index = -1 # distinguishes us from the 13 tables in the scene
        self.diners = {}
        self.dinerStatus = {} # is the diner dead, hungry,  eating
        self.serviceLocs = {} # dummy nodepaths of where we want the food to be placed
        self.chairLocators = {} # top of the seat
        self.sitLocators = {} # point on the floor where sitting suit will be parented to
        self.activeIntervals = {}
        self.dinerStatusIndicators = {}
        self.preparedForPhaseFour= False
        self.avId = 0 # which toon is controlling us
        self.toon = None # the actual toon which should match up with self.avId
        self.pitcherSmoother = SmoothMover()
        self.pitcherSmoother.setSmoothMode(SmoothMover.SMOn)
        self.smoothStarted = 0
        self.__broadcastPeriod = 0.2
        # This number increments each time we change direction on the
        # crane controls.  It's used to update the animation
        # appropriately.
        self.changeSeq = 0
        self.lastChangeSeq = 0
        self.pitcherAdviceLabel = None

        self.fireLength = 250 # in feet, how far water fires
        self.fireTrack = None
        self.hitObject = None

        # stuff related to power bar
        self.setupPowerBar()
        self.aimStart = None
        
        self.toonPitcherPosition = Point3(0,-2,0)
        
        # can the local toon request control of this table
        self.allowLocalRequestControl = True
        self.fadeTrack = None
        self.grabTrack = None
        self.gotHitByBoss = False

        # these variables are used for calculation how fast the player is pressing the keys
        self.keyTTL = []
        self.keyRate = 0
        self.buttons = [0,1] # 0 means up arrow, 1 means down arrow
        self.lastPowerFired = 0

        # This is the sound effect currently looping for the pitcher
        # controls.
        self.moveSound = None

        self.releaseTrack = None
        
    def disable(self):
        """Remove us from active duty and store in the cache."""
        DistributedObject.DistributedObject.disable(self)
        taskMgr.remove(self.triggerName)
        taskMgr.remove(self.smoothName)
        taskMgr.remove(self.watchControlsName)
        taskMgr.remove(self.pitcherAdviceName)
        taskMgr.remove(self.posHprBroadcastName)
        taskMgr.remove(self.waterPowerTaskName)
        if self.releaseTrack:
            self.releaseTrack.finish()
            self.releaseTrack = None
        if self.fireTrack:
            self.fireTrack.finish()
            self.fireTrack = None
        self.cleanupIntervals()
        

    def delete(self):
        """Delete ourself from the world."""
        DistributedObject.DistributedObject.delete(self)
        self.boss = None
        self.ignoreAll()
        for indicator in self.dinerStatusIndicators.values():
            indicator.delete()
        self.dinerStatusIndicators = {}
        for diner in self.diners.values():
            diner.delete()
        self.diners = {}        
        self.powerBar.destroy()
        self.powerBar = None
        self.pitcherMoveSfx.stop()
        
        
    def announceGenerate(self):
        """Handle all required fields being filled in."""
        DistributedObject.DistributedObject.announceGenerate(self)
        self.loadAssets()
        self.smoothName = self.uniqueName('pitcherSmooth')
        self.pitcherAdviceName = self.uniqueName('pitcherAdvice')
        self.posHprBroadcastName = self.uniqueName('pitcherBroadcast')
        self.waterPowerTaskName = self.uniqueName('updateWaterPower')
        self.triggerName = self.uniqueName('trigger')
        self.watchControlsName = self.uniqueName('watchControls')
        
    ##### Messages To/From The Server #####

    def setBossCogId(self, bossCogId):
        """Handle receiving the CEO doId from the server."""
        self.bossCogId = bossCogId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated battles.
        self.boss = base.cr.doId2do[bossCogId]
        self.boss.setTable(self, self.index)

    def setIndex(self, index):
        """Handle receiving the index which identifies our side the server."""
        self.index = index
        # WARNING debug only, remove this
        #if (index == 0):
        #    base.bt = self

    def setState(self, state, avId, extraInfo):
        """Set the state as dictated by the AI."""
        self.gotHitByBoss = extraInfo
        if state == 'F':
            self.demand('Off')
        elif state == 'N':
            self.demand('On')
        elif state == 'I':
            self.demand('Inactive')
        elif state == 'R':
            self.demand('Free')
        elif state == 'C':
            self.demand('Controlled', avId)
        elif state == 'L':
            self.demand('Flat', avId)            
        else:
            self.notify.error("Invalid state from AI: %s" % (state))

    def setNumDiners(self, numDiners):
        """Set the number of diners as dictated by the AI."""
        self.numDiners = numDiners

    def setDinerInfo(self, hungryDurations, eatingDurations, dinerLevels):
        """Handle the AI telling us how long each suit will be hungry or eating."""
        self.dinerInfo = {}
        for i in xrange(len(hungryDurations)):
            hungryDur = hungryDurations[i]
            eatingDur = eatingDurations[i]
            dinerLevel = dinerLevels[i]
            self.dinerInfo[i] = (hungryDur, eatingDur, dinerLevel)
        
    ### loading assets ###

    def loadAssets(self):
        """Load and setup the assets for the banquet table and chairs."""
        # later on this will become a loadModel call
        self.tableGroup = loader.loadModel('phase_12/models/bossbotHQ/BanquetTableChairs')
        tableLocator = self.boss.geom.find('**/TableLocator_%d' % (self.index+1))
        if tableLocator.isEmpty():
            self.tableGroup.reparentTo(render)
            self.tableGroup.setPos(0,75,0)
        else:
            self.tableGroup.reparentTo(tableLocator)
        self.tableGeom = self.tableGroup.find('**/Geometry')
        self.setupDiners()
        self.setupChairCols()
        self.squirtSfx = loader.loadSfx('phase_4/audio/sfx/AA_squirt_seltzer_miss.mp3')
        self.hitBossSfx = loader.loadSfx('phase_5/audio/sfx/SA_watercooler_spray_only.mp3')
        self.hitBossSoundInterval = SoundInterval(self.hitBossSfx, node=self.boss,
                                                  volume = 1.0,
                                                  )
        self.serveFoodSfx = loader.loadSfx('phase_4/audio/sfx/MG_sfx_travel_game_bell_for_trolley.mp3')
        self.pitcherMoveSfx = base.loadSfx(
            "phase_4/audio/sfx/MG_cannon_adjust.mp3")
            #"phase_9/audio/sfx/CHQ_FACT_elevator_up_down.mp3")        

    def setupDiners(self):
        """Create the suits seated on the chairs."""
        for i in xrange(self.numDiners):
            newDiner = self.createDiner(i)
            self.diners[i] = newDiner
            self.dinerStatus[i] = self.HUNGRY

    def createDiner(self,i):
        """Create and return one diner sitting on the chair."""
        diner = Suit.Suit()
        diner.dna = SuitDNA.SuitDNA()
        #level = 8
        level = self.dinerInfo[i][2]
        level -= 4 # off by four somehow
        diner.dna.newSuitRandom(level = level, dept = 'c')
        diner.setDNA(diner.dna)        
        if self.useNewAnimations:
            diner.loop('sit', fromFrame = i)
        else:
            diner.pose('landing',0)
        locator = self.tableGroup.find('**/chair_%d' % (i +1))
        locatorScale = locator.getNetTransform().getScale()[0]
        correctHeadingNp = locator.attachNewNode('correctHeading')
        self.chairLocators[i] = correctHeadingNp
        #import pdb; pdb.set_trace()
        heading = self.rotationsPerSeatIndex[i]
        correctHeadingNp.setH(heading)
        sitLocator = correctHeadingNp.attachNewNode('sitLocator')
        base.sitLocator = sitLocator 
        pos = correctHeadingNp.getPos(render)
        if SuitDNA.getSuitBodyType(diner.dna.name) == 'c':
            sitLocator.setPos(0.5, 3.65, -3.75)
        else:
            sitLocator.setZ(-2.4)        
            sitLocator.setY(2.5)
            sitLocator.setX(0.5)
        self.sitLocators[i] = sitLocator
        # some fudging to make it look right
        diner.setScale(1.0/locatorScale)
        diner.reparentTo(sitLocator)            
        #diner.setZ(-5.5)

        # create the nodePath where we serve food to
        newLoc = NodePath('serviceLoc-%d-%d' % (self.index, i))
        newLoc.reparentTo(correctHeadingNp)
        newLoc.setPos(0, 3.0, 1)
        self.serviceLocs[i] = newLoc
        base.serviceLoc = newLoc

        # create the status indicator
        head = diner.find('**/joint_head')
        newIndicator = DinerStatusIndicator.DinerStatusIndicator(parent = head,
                                                                 pos = Point3(0,0,3.5),
                                                                 scale = 5.0)
        newIndicator.wrtReparentTo(diner)
        self.dinerStatusIndicators[i] = newIndicator
        return diner

    def setupChairCols(self):
        """Setup the chair collisions of all chairs."""        
        for i in xrange(self.numDiners):
            chairCol = self.tableGroup.find('**/collision_chair_%d' % (i +1))
            colName = 'ChairCol-%d-%d' % (self.index,i)
            chairCol.setTag('chairIndex',str(i))
            chairCol.setName(colName)
            chairCol.setCollideMask(ToontownGlobals.WallBitmask)
            self.accept('enter'+colName, self.touchedChair)

    def touchedChair(self, colEntry):
        """Handle the toon touching one of the chairs."""
        assert self.notify.debugStateCall(self)
        chairIndex = int( colEntry.getIntoNodePath().getTag('chairIndex'))
        if chairIndex in self.dinerStatus:
            status = self.dinerStatus[chairIndex]
            if status in (self.HUNGRY, self.ANGRY) :
                self.boss.localToonTouchedChair(self.index, chairIndex)

    def serveFood(self, food, chairIndex):
        """Display putting food in front of a toon."""
        assert self.notify.debugStateCall(self)        
        self.removeFoodModel(chairIndex)
        serviceLoc = self.serviceLocs.get(chairIndex)
        if (not food) or food.isEmpty():
            # food is not valid, load it from scratch and immediately place it
            foodModel = loader.loadModel('phase_12/models/bossbotHQ/canoffood')
            foodModel.setScale(ToontownGlobals.BossbotFoodModelScale)
            foodModel.reparentTo(serviceLoc)
        else:
            # create a interval of the food moving to the serviceLoc
            food.wrtReparentTo(serviceLoc)
            tray = food.find('**/tray')
            if not tray.isEmpty():
                tray.hide()
            ivalDuration = 1.5
            foodMoveIval = Parallel(
                SoundInterval( self.serveFoodSfx, node=food),
                ProjectileInterval( food, duration = ivalDuration, startPos = food.getPos(serviceLoc),
                                    endPos = serviceLoc.getPos(serviceLoc)),
                LerpHprInterval(food, ivalDuration, Point3(0,-360,0))
                )
            intervalName = "serveFood-%d-%d" % (self.index, chairIndex)
            foodMoveIval.start()
            self.activeIntervals[intervalName] = foodMoveIval

        #The AI will send b_setDinerStatus    
        #self.setDinerStatus( chairIndex, self.EATING)

    def setDinerStatus(self, chairIndex, status):
        """Set the diner status as dictated by the AI."""
        if chairIndex in self.dinerStatus:
            oldStatus = self.dinerStatus[chairIndex]
            self.dinerStatus[chairIndex] = status
            if oldStatus != status:
                if status == self.EATING:
                    self.changeDinerToEating(chairIndex)
                elif status == self.HUNGRY:
                    self.changeDinerToHungry(chairIndex)
                elif status == self.ANGRY:
                    self.changeDinerToAngry(chairIndex)
                elif status == self.DEAD:
                    self.changeDinerToDead(chairIndex)
                elif status == self.HIDDEN:
                    self.changeDinerToHidden(chairIndex)
                    
    def removeFoodModel(self, chairIndex):
        """Remove the food in front of any diner."""
        serviceLoc = self.serviceLocs.get(chairIndex)
        if serviceLoc:
            for i in xrange(serviceLoc.getNumChildren()):
                serviceLoc.getChild(0).removeNode()             
        
    def changeDinerToEating(self, chairIndex):
        """Change a diner to eating status."""
        assert self.notify.debugStateCall(self)
        #import pdb; pdb.set_trace()
        indicator = self.dinerStatusIndicators.get(chairIndex)
        eatingDuration = self.dinerInfo[chairIndex][1]
        if indicator:
            indicator.request('Eating', eatingDuration)
        diner = self.diners[chairIndex]
        #diner.loop('sit-eat-loop')
        intervalName = "eating-%d-%d" % (self.index, chairIndex)
        eatInTime = 32.0 / 24.0
        eatOutTime = 21.0 / 24.0
        eatLoopTime = 19 / 24.0
        #import pdb; pdb.set_trace()
        
        rightHand = diner.getRightHand()
        waitTime =5
        loopDuration = eatingDuration - eatInTime - eatOutTime - waitTime
        serviceLoc = self.serviceLocs[chairIndex]
        def foodAttach(self=self, diner=diner):
            foodModel = self.serviceLocs[chairIndex].getChild(0)
            foodModel.reparentTo( diner.getRightHand()),
            foodModel.setHpr( Point3(0,-94,0)),
            foodModel.setPos( Point3(-0.15,-0.7,-0.4)),
            scaleAdj = 1
            if SuitDNA.getSuitBodyType(diner.dna.name) == 'c':
               scaleAdj=0.6
               foodModel.setPos( Point3(0.1, -0.25, -0.31)),
            else:
               scaleAdj=0.8
               foodModel.setPos( Point3(-0.25, -0.85, -0.34)),
            oldScale = foodModel.getScale()
            newScale = oldScale * scaleAdj
            foodModel.setScale(newScale)

        def foodDetach(self=self, diner=diner):
            foodModel = diner.getRightHand().getChild(0)
            foodModel.reparentTo( serviceLoc),
            foodModel.setPosHpr( 0,0,0, 0,0,0),
            scaleAdj = 1
            if SuitDNA.getSuitBodyType(diner.dna.name) == 'c':
               scaleAdj=0.6
            else:
                scakeAdj = 0.8
            oldScale = foodModel.getScale()
            newScale = oldScale / scaleAdj
            foodModel.setScale(newScale)
            
        eatIval = Sequence(
            ActorInterval(diner, 'sit', duration = waitTime),
            ActorInterval(diner, 'sit-eat-in', startFrame=0, endFrame=6),
            Func(foodAttach),
            ActorInterval(diner, 'sit-eat-in', startFrame=6, endFrame=32),
            ActorInterval(diner, 'sit-eat-loop', duration=loopDuration, loop=1),
            ActorInterval(diner, 'sit-eat-out', startFrame=0, endFrame = 12),
            Func(foodDetach),
            ActorInterval(diner, 'sit-eat-out', startFrame=12, endFrame = 21),
            )
        eatIval.start()
        self.activeIntervals[intervalName] =eatIval  

    def changeDinerToHungry(self, chairIndex):
        """Change a diner to hungry."""
        intervalName = "eating-%d-%d" % (self.index, chairIndex)
        if intervalName in self.activeIntervals:
            self.activeIntervals[intervalName].finish()
        self.removeFoodModel(chairIndex)
        indicator = self.dinerStatusIndicators.get(chairIndex)
        if indicator:
            indicator.request('Hungry',self.dinerInfo[chairIndex][0])
        diner = self.diners[chairIndex]
        if random.choice([0,1]):
            diner.loop('sit-hungry-left')
        else:
            diner.loop('sit-hungry-right')

    def changeDinerToAngry(self, chairIndex):
        """Change a diner to angry."""
        self.removeFoodModel(chairIndex)
        indicator = self.dinerStatusIndicators.get(chairIndex)
        if indicator:
            indicator.request('Angry')
        diner = self.diners[chairIndex]
        diner.loop('sit-angry')

    def changeDinerToDead(self, chairIndex):
        """Change a diner to angry."""
        def removeDeathSuit(suit, deathSuit):
            if (not deathSuit.isEmpty()):
                deathSuit.detachNode()
                suit.cleanupLoseActor()
                
        self.removeFoodModel(chairIndex)
        indicator = self.dinerStatusIndicators.get(chairIndex)
        if indicator:
            indicator.request('Dead')
        diner = self.diners[chairIndex]
        deathSuit = diner
        locator = self.tableGroup.find('**/chair_%d' % (chairIndex +1))
        #diner.pose('neutral',0)
        #diner.setPos(0,0,0)
        #diner.reparentTo(self.chairLocators[chairIndex])
        deathSuit = diner.getLoseActor()
        ival = Sequence(
            Func(self.notify.debug,"before actorinterval sit-lose"),
            ActorInterval(diner, 'sit-lose'),
            Func(self.notify.debug,"before deathSuit.setHpr"),
            Func(deathSuit.setHpr, diner.getHpr()),
            Func(self.notify.debug,"before diner.hide"),
            Func(diner.hide),
            Func(self.notify.debug,"before deathSuit.reparentTo"),            
            Func(deathSuit.reparentTo, self.chairLocators[chairIndex]),
            Func(self.notify.debug,"befor ActorInterval lose"),
            ActorInterval(deathSuit, 'lose', duration = MovieUtil.SUIT_LOSE_DURATION),
            Func(self.notify.debug,"before remove deathsuit"),
            Func(removeDeathSuit, diner, deathSuit, name = 'remove-death-suit-%d-%d' % (chairIndex,self.index)),
            Func(self.notify.debug,"diner.stash"),
            Func(diner.stash),
            )
        spinningSound = base.loadSfx("phase_3.5/audio/sfx/Cog_Death.mp3")
        deathSound = base.loadSfx("phase_3.5/audio/sfx/ENC_cogfall_apart.mp3")
        deathSoundTrack = Sequence(
            Wait(0.8),
            SoundInterval(spinningSound, duration=1.2, startTime = 1.5, volume=0.2, node=deathSuit),
            SoundInterval(spinningSound, duration=3.0, startTime = 0.6, volume=0.8, node=deathSuit),
            SoundInterval(deathSound, volume = 0.32, node=deathSuit),
            )        
        intervalName = "dinerDie-%d-%d" % (self.index, chairIndex)
        deathIval = Parallel(ival, deathSoundTrack)
        deathIval.start()
        self.activeIntervals[intervalName] =deathIval        

    def changeDinerToHidden(self, chairIndex):
        """Change a diner to Hidden."""
        self.removeFoodModel(chairIndex)
        indicator = self.dinerStatusIndicators.get(chairIndex)
        if indicator:
            indicator.request('Inactive')
        diner = self.diners[chairIndex]
        diner.hide()

    def setAllDinersToSitNeutral(self):
        startFrame = 0
        for diner in self.diners.values():
            if not diner.isHidden():
                diner.loop('sit', fromFrame = startFrame)
                startFrame += 1
            
    ### Util code ###

    def cleanupIntervals(self):
        """Cleanup all intervals."""
        for interval in self.activeIntervals.values():
            interval.finish()
        self.activeIntervals = {}

    def clearInterval(self, name, finish=1):
        """ Clean up the specified Interval
        """
        if (self.activeIntervals.has_key(name)):
            ival = self.activeIntervals[name]
            if finish:
                ival.finish()
            else:
                ival.pause()
            if self.activeIntervals.has_key(name):
                del self.activeIntervals[name]
        else:
            self.notify.debug('interval: %s already cleared' % name)

    def finishInterval(self, name):
        """ Force the specified Interval to jump to the end
        """ 
        if (self.activeIntervals.has_key(name)):
            interval = self.activeIntervals[name]
            interval.finish()


    def getNotDeadInfo(self):
        """Return a list of (<table index>, <chair Index>, <suit level>) suits that are not dead."""
        notDeadList  = []
        for i in xrange(self.numDiners):
            if self.dinerStatus[i] != self.DEAD:
                notDeadList.append( (self.index, i, 12))
        return notDeadList
        
            

    def enterOn(self):
        """Handle entering the on state."""
        pass

    def exitOn(self):
        """Handle exiting the on state."""
        pass

    def enterInactive(self):
        """Handle entering the inactive state."""
        for chairIndex in xrange(self.numDiners):
            indicator = self.dinerStatusIndicators.get(chairIndex)
            if indicator:
                indicator.request('Inactive')
            self.removeFoodModel(chairIndex)
        pass

    def exitInactive(self):
        """Handle exiting the inactive state."""
        pass

    ### Water state, shooting water at the boss

    def enterFree(self):
        """Handle going to the free state. Free to be controlled by player"""
        self.resetPowerBar()
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None        
        self.prepareForPhaseFour()
        if self.avId == localAvatar.doId:
            # Five second timeout on grabbing the same tabke again.  Go
            # get a different table!
            self.tableGroup.setAlphaScale(0.3)
            self.tableGroup.setTransparency(1)
            taskMgr.doMethodLater(5, self.__allowDetect, self.triggerName)

            self.fadeTrack = Sequence(
                Func(self.tableGroup.setTransparency, 1),
                self.tableGroup.colorScaleInterval(0.2, VBase4(1,1,1,0.3)))
            self.fadeTrack.start()
            self.allowLocalRequestControl = False

        else:
            # Other players can grab this table immediately.
            self.allowLocalRequestControl = True            
            #self.trigger.unstash()
            #self.accept(self.triggerEvent, self.__hitTrigger)
            pass
        
        self.avId = 0


    def exitFree(self):
        """Handle exiting the free state."""
        pass

    def touchedTable(self, colEntry):
        """Handle the toon touching one of the tables."""
        assert self.notify.debugStateCall(self)
        tableIndex = int( colEntry.getIntoNodePath().getTag('tableIndex'))
        if self.state == 'Free' and self.avId == 0 and \
           self.allowLocalRequestControl:
            self.d_requestControl()
        #self.boss.localToonTouchedTable(self.tableIndex)
    

    def prepareForPhaseFour(self):
        """Set up geometry and collisions for phase four."""
        if not self.preparedForPhaseFour:
            # hide the chairs and chair collisions
            for i in xrange(8):
                chair = self.tableGroup.find('**/chair_%d' % (i +1))
                if not chair.isEmpty():
                    chair.hide()
                colChairs = self.tableGroup.findAllMatches('**/ChairCol*')
                for i in xrange(colChairs.getNumPaths()):
                    col = colChairs.getPath(i)
                    col.stash()
                colChairs = self.tableGroup.findAllMatches('**/collision_chair*')
                for i in xrange(colChairs.getNumPaths()):
                    col = colChairs.getPath(i)
                    col.stash()
            # make colliding against the table do something
            tableCol = self.tableGroup.find('**/collision_table')
            colName = 'TableCol-%d' % (self.index)
            tableCol.setTag('tableIndex',str(self.index))
            tableCol.setName(colName)
            tableCol.setCollideMask(ToontownGlobals.WallBitmask |
                                    ToontownGlobals.BanquetTableBitmask)
            self.accept('enter'+colName, self.touchedTable)            
            self.preparedForPhaseFour = True

            # create the water pitcher
            #self.waterPitcherModel = loader.loadModel('models/misc/xyzAxis')
            self.waterPitcherModel = loader.loadModel('phase_12/models/bossbotHQ/tt_m_ara_bhq_seltzerBottle')
            lampNode = self.tableGroup.find('**/lamp_med_5')
            pos = lampNode.getPos(self.tableGroup)
            lampNode.hide()
            bottleLocator = self.tableGroup.find('**/bottle_locator')
            pos = bottleLocator.getPos(self.tableGroup)
            self.waterPitcherNode = self.tableGroup.attachNewNode('pitcherNode')
            self.waterPitcherNode.setPos(pos)
            self.waterPitcherModel.reparentTo(self.waterPitcherNode)
            self.waterPitcherModel.ls()
            self.nozzle = self.waterPitcherModel.find('**/nozzle_tip')
            self.handLocator = self.waterPitcherModel.find('**/hand_locator')
            self.handPos = self.handLocator.getPos()
        
    def d_requestControl(self):
        """Tell AI our local toon is requesting control."""
        self.sendUpdate('requestControl')

    def d_requestFree(self, gotHitByBoss):
        """Tell AI our local toon is giving up control."""
        self.sendUpdate('requestFree', [gotHitByBoss])

    ### Controlled state ###
    def enterControlled(self, avId):
        """Handle entering the controlled state, with avId on the controls."""
        self.prepareForPhaseFour()
        self.avId = avId
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return
        self.toon = toon

        self.grabTrack = self.makeToonGrabInterval(toon)
        self.notify.debug('grabTrack=%s' % self.grabTrack)
        #self.pitcherCamPos = Point3(0,-self.toonPitcherPosition[1],2.5)
        #self.pitcherCamHpr = Point3(0,0,0)        
        self.pitcherCamPos = Point3(0, -50, 40)
        self.pitcherCamHpr = Point3(0, -21, 0)        


        if avId == localAvatar.doId:
            # The local toon is beginning to control the crane.
            #self.boss.toMovieMode()
            self.boss.toMovieMode() # temp until we get a collision on the table top
            self.__enableControlInterface()
            self.startPosHprBroadcast()
            self.grabTrack = Sequence(
                self.grabTrack,
                #Func(self.boss.toCraneMode),
                Func(camera.wrtReparentTo, localAvatar),
                LerpPosHprInterval(camera,1, self.pitcherCamPos, self.pitcherCamHpr),
                Func(self.boss.toCraneMode)
                )
            if self.TugOfWarControls:
                self.__spawnUpdateKeyPressRateTask()

            """
            camera.reparentTo(self.hinge)
            camera.setPosHpr(0, -20, -5, 0, -20, 0)
            self.tube.stash()

            localAvatar.setPosHpr(self.controls, 0, 0, 0, 0, 0, 0)
            localAvatar.sendCurrentPosition()

            self.__activatePhysics()
            self.__enableControlInterface()
            
            self.startShadow()
            """

            # If we get a message from the Place that we exited Crane
            # mode--for instance, because we got hit by flying
            # gears--then ask the AI to yield us up.
            self.accept('exitCrane', self.gotBossZapped) 

        else:
            self.startSmooth()
            toon.stopSmooth()
            #self.grabTrack = Sequence(self.grabTrack,
            #                          Func(toon.startSmooth))

        self.grabTrack.start()

    def exitControlled(self):
        """Handle exiting  the controlled state."""        
        self.ignore('exitCrane')        

        if self.grabTrack:
            self.grabTrack.finish()
            self.grabTrack = None

        nextState = self.getCurrentOrNextState()
        self.notify.debug('nextState=%s' % nextState)

        if nextState == 'Flat':
            place = base.cr.playGame.getPlace()
            #import pdb; pdb.set_trace()
            self.notify.debug('%s' % place.fsm)
            if self.avId == localAvatar.doId:
                self.__disableControlInterface()

        else:
            if self.toon and not self.toon.isDisabled():
                self.toon.loop('neutral')
                self.toon.startSmooth()

            self.releaseTrack = self.makeToonReleaseInterval(self.toon)
            #self.stopWatchJoystick()

            self.stopPosHprBroadcast()
            #self.stopShadow()
            self.stopSmooth()
            if self.avId == localAvatar.doId:
                # The local toon is no longer in control of the crane.
                    
                # do an immediate reparent to render, in case we get flattened next
                localAvatar.wrtReparentTo(render)
                self.__disableControlInterface()

                #self.__deactivatePhysics()
                #self.tube.unstash()

                camera.reparentTo(base.localAvatar)
                camera.setPos(base.localAvatar.cameraPositions[0][0])
                camera.setHpr(0, 0, 0)

                self.goToFinalBattle()
                self.safeBossToFinalBattleMode()
            else:
                toon = base.cr.doId2do.get(self.avId)
                if toon:
                    # do an immediate reparent to prevent perma flattened bug
                    toon.wrtReparentTo(render)                

            self.releaseTrack.start()

    def safeBossToFinalBattleMode(self):
        """Call boss.toFinalBattleMode if self.boss is valid."""
        if self.boss:
            self.boss.toFinalBattleMode()


    def goToFinalBattle(self):
        # This is a bit hacky.  Go back to finalBattle mode, but
        # only if we're still in crane mode.  (We might have been
        # zapped to 'ouch' mode by a hit.)
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                if place.fsm.getCurrentState().getName() == 'crane':
                    place.setState('finalBattle')
        

    def makeToonGrabInterval(self,toon):
        """Return an interval of the toon jumping to pitcher position."""
        toon.pose('leverNeutral', 0)
        toon.update()
        rightHandPos = toon.rightHand.getPos(toon)
        self.toonPitcherPosition = Point3(self.handPos[0]-rightHandPos[0], self.handPos[1]-rightHandPos[1], 0)
        destZScale = rightHandPos[2] / self.handPos[2] 
        grabIval = Sequence(
            Func(toon.wrtReparentTo, self.waterPitcherNode),
            Func(toon.loop, 'neutral'),
            Parallel(
               ActorInterval(toon, 'jump'),
               Sequence(
                  Wait(0.43),
                  Parallel(                
                     ProjectileInterval(toon, duration = 0.9,
                                   startPos = toon.getPos(self.waterPitcherNode),
                                   endPos = self.toonPitcherPosition),
                     LerpHprInterval(toon, 0.9, Point3(0,0,0)),
                     LerpScaleInterval(self.waterPitcherModel, 0.9, Point3(1,1,destZScale)),
                   ),
                 ),
               ),
            Func(toon.setPos, self.toonPitcherPosition),
            Func(toon.loop, 'leverNeutral'),           
            )
        return grabIval

    def makeToonReleaseInterval(self,toon):
        """Return an interval of the toon jumping to pitcher position."""
        temp1 = self.waterPitcherNode.attachNewNode('temp1')
        temp1.setPos(self.toonPitcherPosition)
        temp2 =  self.waterPitcherNode.attachNewNode('temp2')
        temp2.setPos(0,-10, -self.waterPitcherNode.getZ())
        startPos = temp1.getPos(render)
        endPos = temp2.getPos(render)
        temp1.removeNode()
        temp2.removeNode()

        def getSlideToPos(toon = toon):
            return render.getRelativePoint(toon, Point3(0, -10, 0))
        
        if self.gotHitByBoss:
            self.notify.debug('creating zap interval instead')
            grabIval = Sequence(
                Func(toon.loop, 'neutral'),
                Func(toon.wrtReparentTo, render),
                Parallel(
                   ActorInterval(toon, 'slip-backward'),
                   toon.posInterval(0.5, getSlideToPos, fluid = 1)
                   )
                )
        else:
            grabIval = Sequence(
                Func(toon.loop, 'neutral'),
                Func(toon.wrtReparentTo, render),
                Parallel(
                   ActorInterval(toon, 'jump'),
                   Sequence(
                      Wait(0.43),
                      ProjectileInterval(toon, duration = 0.9,
                                        startPos = startPos,
                                        endPos = endPos
                                      ),
                      ),
                   ),
                )
        
        return grabIval    

    ### Handle smoothing of distributed updates.  This is similar to
    ### code in DistributedSmoothNode, but streamlined for our
    ### purposes.

    def b_clearSmoothing(self):
        """Tell us and other clients to clear smoothing."""
        self.d_clearSmoothing()
        self.clearSmoothing()
        
    def d_clearSmoothing(self):
        """Tell other clients to clear smoothing."""
        self.sendUpdate("clearSmoothing", [0])

    def clearSmoothing(self, bogus = None):
        """Invalidate old position reports."""
        # Call this to invalidate all the old position reports
        # (e.g. just before popping to a new position).
        self.pitcherSmoother.clearPositions(1)

    def doSmoothTask(self, task):
        """
        This function updates the position of the node to its computed
        smoothed position.  This may be overridden by a derived class
        to specialize the behavior.
        """
        self.pitcherSmoother.computeAndApplySmoothHpr(self.waterPitcherNode)

        return Task.cont

    def startSmooth(self):
        """
        This function starts the task that ensures the node is
        positioned correctly every frame.  However, while the task is
        running, you won't be able to lerp the node or directly
        position it.
        """
        if not self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.reloadPosition()
            taskMgr.add(self.doSmoothTask, taskName)
            self.smoothStarted = 1

    def stopSmooth(self):
        """
        This function stops the task spawned by startSmooth(), and
        allows show code to move the node around directly.
        """
        if self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.forceToTruePosition()
            self.smoothStarted = 0


    def __enableControlInterface(self):
        """Enable the control interface."""
        gui = loader.loadModel("phase_3.5/models/gui/avatar_panel_gui")

        self.closeButton = DirectButton(
            image = (gui.find("**/CloseBtn_UP"),
                     gui.find("**/CloseBtn_DN"),
                     gui.find("**/CloseBtn_Rllvr"),
                     gui.find("**/CloseBtn_UP"),
                     ),
            relief = None,
            scale = 2,
            text = TTLocalizer.BossbotPitcherLeave,
            text_scale = 0.04,
            text_pos = (0, -0.07),
            text_fg = VBase4(1, 1, 1, 1),
            pos = (1.05, 0, -0.82),
            command = self.__exitPitcher,
            )
        
        self.accept('escape', self.__exitPitcher)

        self.accept('control', self.__controlPressed)
        self.accept('control-up', self.__controlReleased)
        self.accept('InputState-forward', self.__upArrow)
        self.accept('InputState-reverse', self.__downArrow)
        self.accept('InputState-turnLeft', self.__leftArrow)
        self.accept('InputState-turnRight', self.__rightArrow)
        self.accept('arrow_up', self.__upArrowKeyPressed)
        self.accept('arrow_down', self.__downArrowKeyPressed)

        taskMgr.add(self.__watchControls, self.watchControlsName)

        # In case they don't figure it out, hit them over the head
        # with it after a few seconds.
        taskMgr.doMethodLater(5, self.__displayPitcherAdvice,
                              self.pitcherAdviceName)
        #taskMgr.doMethodLater(10, self.__displayMagnetAdvice,
        #                      self.magnetAdviceName)

        # Up in the sky, it's hard to read what people are saying.
        #NametagGlobals.setOnscreenChatForced(1)

        self.arrowVert = 0
        self.arrowHorz = 0
        self.powerBar.show()

    def __disableControlInterface(self):
        """Disable the control interface."""
        #self.__turnOffMagnet()

        if self.closeButton:
            self.closeButton.destroy()
            self.closeButton = None

        self.__cleanupPitcherAdvice()
        #self.__cleanupMagnetAdvice()

        self.ignore('escape')
        self.ignore('control')
        self.ignore('control-up')
        self.ignore('InputState-forward')
        self.ignore('InputState-reverse')
        self.ignore('InputState-turnLeft')
        self.ignore('InputState-turnRight')
        self.ignore('arrow_up')
        self.ignore('arrow_down')

        self.arrowVert = 0
        self.arrowHorz = 0

        #NametagGlobals.setOnscreenChatForced(0)

        taskMgr.remove(self.watchControlsName)
        taskMgr.remove(self.waterPowerTaskName)        
        self.resetPowerBar()
        self.aimStart = None
        self.powerBar.hide()

        if self.TugOfWarControls:
            self.__killUpdateKeyPressRateTask()
            self.keyTTL=[]
        self.__setMoveSound(None)

    def __displayPitcherAdvice(self, task):
        """Display pitcher advice on the screen."""
        if self.pitcherAdviceLabel == None:
            self.pitcherAdviceLabel = DirectLabel(
                text = TTLocalizer.BossbotPitcherAdvice,
                text_fg = VBase4(1,1,1,1),
                text_align = TextNode.ACenter,
                relief = None,
                pos = (0, 0, 0.69),
                scale = 0.1)

    def __cleanupPitcherAdvice(self):
        """Remove pitcher advice from the screen."""
        if self.pitcherAdviceLabel:
            self.pitcherAdviceLabel.destroy()
            self.pitcherAdviceLabel = None
        taskMgr.remove(self.pitcherAdviceName)

    def showExiting(self):
        """Indicate that we've sent an exiting message to AI."""
        if self.closeButton:
            self.closeButton.destroy()
            self.closeButton = DirectLabel(
                relief = None,
                text = TTLocalizer.BossbotPitcherLeaving,
                pos = (1.05, 0, -0.88),
                text_pos = (0, 0),
                text_scale = 0.06,
                text_fg = VBase4(1, 1, 1, 1),
                )

        self.__cleanupPitcherAdvice()
        #self.__cleanupMagnetAdvice()
        

    def __exitPitcher(self):
        """Handle the toon clicking on exit button."""
        #import pdb; pdb.set_trace()
        self.showExiting()   
        self.d_requestFree(False)

    def __controlPressed(self):
        """Handle control key being pressed."""
        self.__cleanupPitcherAdvice()        
        if self.TugOfWarControls:
            if self.power:
                self.aimStart =1
                self.__endFireWater()
        else:
            if self.state == 'Controlled':
                self.__beginFireWater()

    def __controlReleased(self):
        """Handle control key being released."""
        if self.TugOfWarControls:
            pass
        else:
            if self.state == 'Controlled':
                self.__endFireWater()

    def __upArrow(self, pressed):
        """Handle up arrow key being pressed."""
        self.__incrementChangeSeq()
        self.__cleanupPitcherAdvice()
        if pressed:
            self.arrowVert = 1
        elif self.arrowVert > 0:
            self.arrowVert = 0

    def __downArrow(self, pressed):
        """Handle down arrow key being pressed."""
        self.__incrementChangeSeq()
        self.__cleanupPitcherAdvice()
        if pressed:
            self.arrowVert = -1
        elif self.arrowVert < 0:
            self.arrowVert = 0

    def __rightArrow(self, pressed):
        """Handle right arrow key being pressed."""
        self.__incrementChangeSeq()
        self.__cleanupPitcherAdvice()
        if pressed:
            self.arrowHorz = 1
        elif self.arrowHorz > 0:
            self.arrowHorz = 0

    def __leftArrow(self, pressed):
        """Handle left arrow key being pressed."""
        self.__incrementChangeSeq()
        self.__cleanupPitcherAdvice()
        if pressed:
            self.arrowHorz = -1
        elif self.arrowHorz < 0:
            self.arrowHorz = 0
        
    def __incrementChangeSeq(self):
        """Increment our change counter."""
        self.changeSeq = (self.changeSeq + 1) & 0xff

    def stopPosHprBroadcast(self):
        """Stop the pitcher rotation broadcast task."""
        taskName = self.posHprBroadcastName
        taskMgr.remove(taskName)

    def startPosHprBroadcast(self):
        """Start the pitcher rotation broadcast task."""
        taskName = self.posHprBroadcastName

        # Broadcast our initial position
        self.b_clearSmoothing()
        self.d_sendPitcherPos()

        # remove any old tasks
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self.__broadcastPeriod,
                              self.__posHprBroadcast, taskName)

    def __posHprBroadcast(self, task):
        """Periodically broadcast the pitcher rotation."""
        self.d_sendPitcherPos()
        taskName = self.posHprBroadcastName
        taskMgr.doMethodLater(self.__broadcastPeriod,
                              self.__posHprBroadcast, taskName)
        return Task.done


    def d_sendPitcherPos(self):
        """Send the pitcher rotation to the other clients."""
        timestamp = globalClockDelta.getFrameNetworkTime()

        self.sendUpdate('setPitcherPos', [
        self.changeSeq,  self.waterPitcherNode.getH(), timestamp])

    def setPitcherPos(self, changeSeq, h, timestamp):
        """Handle another client sending an update on the pitcher rotation."""
        #assert self.notify.debugStateCall(self)
        self.changeSeq = changeSeq
        if self.smoothStarted:
            now = globalClock.getFrameTime()
            local = globalClockDelta.networkToLocalTime(timestamp, now)

            #self.pitcherSmoother.setY(y)
            self.pitcherSmoother.setH(h)
            self.pitcherSmoother.setTimestamp(local)
            self.pitcherSmoother.markPosition()
        else:
            #self.crane.setY(y)
            self.waterPitcherNode.setH(h)

    def __watchControls(self, task):
        """Check the arrow key press and call move pitcher if needed."""
        if self.arrowHorz:
            self.__movePitcher(self.arrowHorz)
        else:
            pass
            self.__setMoveSound(None)
        return Task.cont

    def __movePitcher(self, xd):
        """Rotate the pitcher by the given xdelta."""
        dt = globalClock.getDt()

        h = self.waterPitcherNode.getH() - xd * self.rotateSpeed * dt
        h %= 360
        self.notify.debug('rotSpeed=%.2f curH=%.2f  xd =%.2f, dt = %.2f, h=%.2f' %
                          (self.rotateSpeed, self.waterPitcherNode.getH(), xd, dt,h))
        limitH = h
        self.waterPitcherNode.setH(limitH)
        if xd:
            self.__setMoveSound(self.pitcherMoveSfx)
        #self.__setMoveSound(self.craneMoveSfx)

    def reloadPosition(self):
        """reloadPosition(self)

        This function re-reads the position from the node itself and
        clears any old position reports for the node.  This should be
        used whenever show code bangs on the node position and expects
        it to stick.

        """
        self.pitcherSmoother.clearPositions(0)
        #self.pitcherSmoother.setPos(self.crane.getPos())
        self.pitcherSmoother.setHpr(self.waterPitcherNode.getHpr())
        self.pitcherSmoother.setPhonyTimestamp()


    def forceToTruePosition(self):
        """forceToTruePosition(self)

        This forces the node to reposition itself to its latest known
        position.  This may result in a pop as the node skips the last
        of its lerp points.

        """
        if self.pitcherSmoother.getLatestPosition():
            #self.pitcherSmoother.applySmoothPos(self.crane)
            self.pitcherSmoother.applySmoothHpr(self.waterPitcherNode)
        self.pitcherSmoother.clearPositions(1)


    # spray head extends from origin to target, holds,
    # then spray tail extends from origin to target
    def getSprayTrack(self,  color, origin, target, dScaleUp, dHold,
                      dScaleDown, horizScale = 1.0, vertScale = 1.0, parent = render):
        """Return an interval of water shooting out."""
        track = Sequence()
        SPRAY_LEN = 1.5

        # sprayRot
        #  |__ sprayScale
        #       |__ sprayProp

        sprayProp = MovieUtil.globalPropPool.getProp('spray')
        # make a parent node for the spray that will hold the scale
        sprayScale = hidden.attachNewNode('spray-parent')
        # the rotation must be on a separate node so that the
        # lerpScale doesn't muck with the rotation
        sprayRot = hidden.attachNewNode('spray-rotate')

        spray = sprayRot
        spray.setColor(color)
        if (color[3] < 1.0):
            spray.setTransparency(1)

        # show the spray
        def showSpray(sprayScale, sprayRot, sprayProp, origin, target, parent):
            if callable(origin):
                origin = origin()
            if callable(target):
                target = target()
            sprayRot.reparentTo(parent)
            sprayRot.clearMat()
            sprayScale.reparentTo(sprayRot)
            sprayScale.clearMat()
            sprayProp.reparentTo(sprayScale)
            sprayProp.clearMat()
            sprayRot.setPos(origin)
            sprayRot.lookAt(Point3(target))
        track.append(Func(showSpray, sprayScale, sprayRot, sprayProp,
                          origin, target, parent))

        # scale the spray up
        def calcTargetScale(target = target, origin = origin, horizScale = horizScale, vertScale = vertScale):
            if callable(target):
                target = target()
            if callable(origin):
                origin = origin()
            distance = Vec3(target - origin).length()
            yScale = distance / SPRAY_LEN
            #targetScale = Point3(yScale, yScale*horizScale, yScale*vertScale)
            targetScale = Point3(yScale*horizScale, yScale, yScale*vertScale)
            return targetScale
        track.append(LerpScaleInterval(sprayScale, dScaleUp, calcTargetScale, startScale=Point3(0.01, 0.01, 0.01)))
        track.append(Func(self.checkHitObject))

        # hold the spray
        track.append(Wait(dHold))

        # bring the back of the spray up to the front, using a scale

        # first we need to adjust the spray's parent node so that it
        # is positioned at the end of the spray
        def prepareToShrinkSpray(spray, sprayProp, origin, target):
            if callable(target):
                target = target()
            if callable(origin):
                origin = origin()
            #localSprayHeadPos = target - origin
            sprayProp.setPos(Point3(0., -SPRAY_LEN, 0.))
            spray.setPos(target)
        track.append(Func(prepareToShrinkSpray, spray, sprayProp,
                          origin, target))

        # shrink the spray down
        track.append(LerpScaleInterval(sprayScale, dScaleDown, Point3(0.01, 0.01, 0.01) ))

        # hide the spray
        def hideSpray(spray, sprayScale, sprayRot, sprayProp, propPool):
            sprayProp.detachNode()
            MovieUtil.removeProp(sprayProp)
            sprayRot.removeNode()
            sprayScale.removeNode()

        track.append(Func(hideSpray, spray, sprayScale, sprayRot,
                          sprayProp, MovieUtil.globalPropPool))
        #track.append(Func(battle.movie.clearRenderProp, sprayProp))

        return track

    def checkHitObject(self):
        """Check the object hit by the water spray."""
        if not self.hitObject:
            return
        if self.avId != base.localAvatar.doId:
            # we didn't fire this pitcher
            return
        
        tag = self.hitObject.getNetTag('pieCode')
        pieCode = int(tag)
        #print tag
        #print self.hitObject
        
        if pieCode == ToontownGlobals.PieCodeBossCog:
            # Make the local toon hear the sfx immediately, then tell the other clients
            self.hitBossSoundInterval.start()
            self.sendUpdate('waterHitBoss',[self.index])
            if self.TugOfWarControls:
                damage = 1
                if self.lastPowerFired < self.YELLOW_POWER_THRESHOLD:
                    damage =1
                elif self.lastPowerFired < self.RED_POWER_THRESHOLD:
                    damage =2
                else:
                    damage =3
                self.boss.d_hitBoss(damage)
            else:
                damage = 1
                if self.lastPowerFired < self.YELLOW_POWER_THRESHOLD:
                    damage =1
                elif self.lastPowerFired < self.RED_POWER_THRESHOLD:
                    damage =2
                else:
                    damage =3
                self.boss.d_hitBoss(damage)                
            # this gets done again when the AI sets boss damage, do it only once
            #self.boss.flashRed()
            #self.boss.doAnimate('hit', now=1)

    def waterHitBoss(self, tableIndex):
        """Handle another client telling us his water hit the boss."""
        if self.index == tableIndex:
            self.hitBossSoundInterval.start()
        

    def setupPowerBar(self):
        """Create the power bar for the water pitcher."""
        self.powerBar = DirectWaitBar(
            pos = (0.0, 0, -0.94),
            relief = DGG.SUNKEN,
            frameSize = (-2.0,2.0,-0.2,0.2),
            borderWidth = (0.02,0.02),
            scale = 0.25,
            range = 1,
            sortOrder = 50,
            frameColor = (0.5,0.5,0.5,0.5),
            barColor = (0.75,0.75,1.0,0.8),
            text = "",
            text_scale = 0.26,
            text_fg = (1, 1, 1, 1),
            text_align = TextNode.ACenter,
            text_pos = (0,-0.05),
            )
            
        self.power = 0
        self.powerBar['value'] = self.power
        self.powerBar.hide()        

    def resetPowerBar(self):
        """Bring the power and power bar to zero."""
        self.power = 0
        self.powerBar['value'] = self.power
        self.powerBar['text'] = ''
        self.keyTTL = []

    def __beginFireWater(self):
        """Handle player pressing control and starting the power meter."""        
        # The control key was pressed.
        if self.fireTrack and self.fireTrack.isPlaying():
            return        
        if self.aimStart != None:
            # This is probably just key-repeat.
            return
        if not self.state == 'Controlled':
            return
        if not self.avId == localAvatar.doId:
            return
        time = globalClock.getFrameTime()
        self.aimStart = time
        messenger.send('wakeup')
        taskMgr.add(self.__updateWaterPower, self.waterPowerTaskName)
    
    def __endFireWater(self):
        """Handle player releasing control and shooting the ball."""
        # The control key was released.  Fire the water.
        
        if self.aimStart == None:
            return
        if not self.state == 'Controlled':
            return        
        if not self.avId == localAvatar.doId:
            return
        #if not self.power:
        #    return
        taskMgr.remove(self.waterPowerTaskName)        
        messenger.send('wakeup')
        self.aimStart = None
        #self.sendSwingInfo()

        origin = self.nozzle.getPos(render)
        target = self.boss.getPos(render)
        angle = deg2Rad(self.waterPitcherNode.getH()+90)
        x = math.cos(angle)
        y = math.sin(angle)
        fireVector = Point3(x,y,0)
        if self.power <0.001:
            self.power =0.001
        self.lastPowerFired = self.power
        fireVector *= self.fireLength * self.power
        target = origin + fireVector
        segment = CollisionSegment(origin[0], origin[1], origin[2],
                                   target[0], target[1], target[2])
        fromObject = render.attachNewNode(CollisionNode('pitcherColNode'))
        fromObject.node().addSolid(segment)
        fromObject.node().setFromCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.CameraBitmask | ToontownGlobals.FloorBitmask)
        fromObject.node().setIntoCollideMask(BitMask32.allOff())        

        queue = CollisionHandlerQueue()
        base.cTrav.addCollider(fromObject, queue)
        base.cTrav.traverse(render)
        queue.sortEntries()
        self.hitObject = None
        if queue.getNumEntries():
            entry = queue.getEntry(0)
            target = entry.getSurfacePoint(render)
            self.hitObject = entry.getIntoNodePath()
        base.cTrav.removeCollider(fromObject)
        fromObject.removeNode()
        self.d_firingWater(origin, target)
        self.fireWater(origin, target)

        self.resetPowerBar()
        pass
        #self.__turnOffMagnet()
        

    def __updateWaterPower(self, task):
        """Change the value of the power meter."""
        if not self.powerBar:
            print "### no power bar!!!"
            return task.done

        newPower =  self.__getWaterPower(globalClock.getFrameTime())
        self.power = newPower
        self.powerBar['value'] = newPower
        #self.powerBar['text'] = TTLocalizer.GolfPowerBarText % {'power' : newPower}
        if self.power < self.YELLOW_POWER_THRESHOLD:
            self.powerBar['barColor'] =  VBase4(0.75,0.75,1.0,0.8)
        elif self.power < self.RED_POWER_THRESHOLD:
            self.powerBar['barColor'] = VBase4(1.0, 1.0, 0.0, 0.8)
        else:
            self.powerBar['barColor'] = VBase4(1.0, 0.0, 0.0, 0.8)        
        return task.cont

    def __getWaterPower(self, time):
        """Return a value between 0 and 1 to indicate golf power."""
        elapsed = max(time - self.aimStart, 0.0)
        t = elapsed / self.waterPowerSpeed
        exponent = self.waterPowerExponent
        if t > 1:
            t = t % 1
        power = 1 - math.pow(1-t, exponent)
        if power > 1.0:
            power = 1.0 
        return power

    def d_firingWater(self, origin, target):
        """Tell the other clients we are firing."""
        self.sendUpdate('firingWater', [ origin[0], origin[1], origin[2], \
                                           target[0], target[1], target[2]])

    def firingWater(self, startX, startY, startZ, endX, endY, endZ):
        """Another client is firing the water."""
        assert self.notify.debugStateCall(self)
        origin = Point3(startX,startY, startZ)
        target = Point3(endX, endY, endZ)
        self.fireWater(origin, target)

    def fireWater(self, origin, target):
        """Code common to a toon firing water locally or from another client."""
        color = VBase4(0.75, 0.75, 1, 0.8)        
        dScaleUp = 0.1
        dHold = 0.3
        dScaleDown = 0.1
        horizScale = 0.1
        vertScale = 0.1        
        sprayTrack = self.getSprayTrack(color, origin, target, dScaleUp,
                                       dHold, dScaleDown, horizScale,
                                       vertScale)
        
        duration = self.squirtSfx.length()
        if sprayTrack.getDuration() < duration:
            duration = sprayTrack.getDuration()
        soundTrack = SoundInterval(self.squirtSfx, node =self.waterPitcherModel,
                                   duration = duration)
        self.fireTrack = Parallel(
            sprayTrack,
            soundTrack
            )
        
        self.fireTrack.start()

    def getPos(self, wrt = render):
        """Return the position of the table."""
        return self.tableGroup.getPos(wrt)

    def getLocator(self):
        """Returns the table locator."""
        return self.tableGroup


    def enterFlat(self, avId):
        """Handle going to the flattened state."""
        self.prepareForPhaseFour()
        self.resetPowerBar()
        self.notify.debug('enterFlat %d' % self.index)
        if self.avId:
            toon = base.cr.doId2do.get(self.avId)
            if toon:
                toon.wrtReparentTo(render)
                toon.setZ(0)
        self.tableGroup.setScale(1, 1, 0.01)
        if self.avId and self.avId == localAvatar.doId:            
            localAvatar.b_squish(ToontownGlobals.BossCogDamageLevels
                                 [ToontownGlobals.BossCogMoveAttack])
            

    def exitFlat(self):
        """Handle exiting the flattened state."""
        self.tableGroup.setScale(1.0)
        if self.avId:
            toon = base.cr.doId2do.get(self.avId)
            if toon:
                if toon == localAvatar:
                    self.boss.toCraneMode()
                    toon.b_setAnimState('neutral')
                toon.setAnimState('neutral')
                toon.loop('leverNeutral')

    def __allowDetect(self, task):
        if self.fadeTrack:
            self.fadeTrack.finish()
        self.fadeTrack = Sequence(
            self.tableGroup.colorScaleInterval(0.2, VBase4(1,1,1,1)),
            Func(self.tableGroup.clearColorScale),
            Func(self.tableGroup.clearTransparency))
        self.fadeTrack.start()

        self.allowLocalRequestControl = True

    def gotBossZapped(self):
        """Handle the local toon getting hit by a ranged attack."""       
        self.showExiting()   
        self.d_requestFree(True)

    def __upArrowKeyPressed(self):
        """Handle up arrow being pressed down."""
        if self.TugOfWarControls:
            self.__pressHandler(0)

    def __downArrowKeyPressed(self):
        """Handle down arrow being pressed down."""
        if self.TugOfWarControls:
            self.__pressHandler(1)

    def __pressHandler(self, index):
        """Handle the up or down arrow key being pressed."""
        if index == self.buttons[0]:
            self.keyTTL.insert(0, 1.0)
            if not self.OnlyUpArrow:
                self.buttons.reverse()
                        
        
    def __spawnUpdateKeyPressRateTask(self):
        taskMgr.remove(self.taskName(self.UPDATE_KEY_PRESS_RATE_TASK))
        taskMgr.doMethodLater(.1,
                              self.__updateKeyPressRateTask,
                              self.taskName(self.UPDATE_KEY_PRESS_RATE_TASK))

    def __killUpdateKeyPressRateTask(self):
        taskMgr.remove(self.taskName(self.UPDATE_KEY_PRESS_RATE_TASK))
 

    def __updateKeyPressRateTask(self, task):
        if not self.state in ('Controlled'):
            return Task.done
        
        # decrement times to live for each key press entry in keyTTL
        for i in range(len(self.keyTTL)):
            self.keyTTL[i] -= .1

        # prune all times to live that are <= 0
        for i in range(len(self.keyTTL)):
            if self.keyTTL[i] <= 0:
                a = self.keyTTL[0:i]
                del self.keyTTL
                self.keyTTL = a
                break

        self.keyRate = len(self.keyTTL)

        # update the power bar
        keyRateDiff = self.keyRate - self.BASELINE_KEY_RATE
        diffPower = keyRateDiff / 300.0
        if self.power < 1 and diffPower >0:
            diffPower = diffPower * math.pow((1 -self.power), 1.25)
        newPower = self.power + diffPower
        if newPower > 1:
            newPower =1
        elif newPower <0:
            newPower = 0
        self.notify.debug('diffPower=%.2f keyRate = %d, newPower=%.2f' % (diffPower, self.keyRate, newPower))
        self.power = newPower
        self.powerBar['value'] = newPower        

        if self.power < self.YELLOW_POWER_THRESHOLD:
            self.powerBar['barColor'] =  VBase4(0.75,0.75,1.0,0.8)
        elif self.power < self.RED_POWER_THRESHOLD:
            self.powerBar['barColor'] = VBase4(1.0, 1.0, 0.0, 0.8)
        else:
            self.powerBar['barColor'] = VBase4(1.0, 0.0, 0.0, 0.8)
            
        self.__spawnUpdateKeyPressRateTask()
        return Task.done

    def __setMoveSound(self, sfx):
        # Starts looping the indicated sound effect, or stops it.
        if sfx != self.moveSound:
            if self.moveSound:
                self.moveSound.stop()
            self.moveSound = sfx
            if self.moveSound:
                base.playSfx(self.moveSound, looping=1, volume = 0.5)

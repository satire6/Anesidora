import math
import random
import GenericAnimatedProp
from direct.actor import Actor
from direct.interval.IntervalGlobal import Sequence, ActorInterval,Wait, Func, SoundInterval, Parallel
from direct.fsm import FSM
from direct.showbase.PythonUtil import weightedChoice
from pandac.PandaModules import TextNode, Vec3
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil


def clearPythonIvals(ival):
    """Recursive function to clear all python ivals."""
    if hasattr(ival, 'function'):
        ival.function = None
    if hasattr(ival, 'pythonIvals'):
        for oneIval in ival.pythonIvals:
            clearPythonIvals(oneIval)
        ival.pythonIvals = []

class InteractiveAnimatedProp(GenericAnimatedProp.GenericAnimatedProp, FSM.FSM):
    """We need much more functionality than GenericAnimatedProp to
    make interactive props behave correctly in battle.
    """

    # these definitions need to be overridden by the subclasses
    ZoneToIdles = {}
    ZoneToIdleIntoFightAnims = {}
    ZoneToFightAnims = {}
    ZoneToVictoryAnims = {}
    ZoneToSadAnims = {}

    IdlePauseTime = base.config.GetFloat('prop-idle-pause-time',0.0)

    HpTextGenerator = TextNode("HpTextGenerator")
    BattleCheerText =  "+"


    def __init__(self, node, holidayId = -1):
        # ok the ttc hydrant is repeated in donalds dock
        # so we have to figure out the zone id  based on the node name zone number
        FSM.FSM.__init__(self,"InteractiveProp-%s"%str(node))
        self.holidayId = holidayId
        self.numIdles = 0
        self.numFightAnims = 0
        self.idleInterval = None
        self.battleCheerInterval = None
        self.sadInterval = None
        self.victoryInterval = None
        self.lastIdleAnimName = ''
        self.lastIdleTime = 0
        self.curIval = None
        self.okToStartNextAnim = False
        cellIndexStr = node.getTag("DNACellIndex")
        self.cellIndex = ord(cellIndexStr)
        self.origAnimNameToSound = {}
        self.lastPlayingAnimPhase = 0 # which was the last idle anim playing
        self.buildingsMakingMeSad = set()
        GenericAnimatedProp.GenericAnimatedProp.__init__(self, node)

    def delete(self):
        """Handle going to a different street or to the playground."""
        # exit contains our clean up code
        self.exit()
        GenericAnimatedProp.GenericAnimatedProp.delete(self)
        self.idleInterval = None
        self.battleCheerInterval = None
        self.sadInterval = None
        self.victoryInterval = None
        pass        

    def getCellIndex(self):
        """Returns the battle cell index, -1 if it's not associated with any."""
        return self.cellIndex

    def playBattleCheerAnim(self):
        """Loop the battle cheer animation."""
        self.node.loop("battleCheer")

        
    def setupActor(self, node):
        """Setup the animation/s for our actor."""
        if self.hoodId in self.ZoneToIdles:
            self.numIdles = len(self.ZoneToIdles[self.hoodId])
        if self.hoodId in self.ZoneToFightAnims:
            self.numFightAnims = len(self.ZoneToFightAnims[self.hoodId])
        self.idleInterval = None
        anim = node.getTag('DNAAnim')
        self.trashcan = Actor.Actor(node, copy = 0)
        self.trashcan.reparentTo(node)
        animDict = {}
        animDict['anim'] = "%s/%s"%(self.path,anim)
        
        for i in xrange(self.numIdles):
            baseAnim = self.ZoneToIdles[self.hoodId][i]
            if isinstance(baseAnim, tuple):
                baseAnim=baseAnim[0]                
            animStr = self.path + '/' + baseAnim
            animKey = "idle%d" % i
            animDict[animKey] = animStr
            # lets check settle anim
            settleName = self.getSettleName(i)
            if settleName:
                settleStr = self.path + '/' + settleName
                settleKey = "settle%d"  % i
                animDict[settleKey] = settleStr                
            
        for i in xrange(self.numFightAnims):
            animStr = self.path + '/' + self.ZoneToFightAnims[self.hoodId][i]
            animKey = "fight%d" % i
            animDict[animKey] = animStr
        if self.hoodId in self.ZoneToIdleIntoFightAnims:
            animStr = self.path + '/' + self.ZoneToIdleIntoFightAnims[self.hoodId]
            animKey = "idleIntoFight"
            animDict[animKey] = animStr
        if self.hoodId in self.ZoneToIdleIntoFightAnims:
            animStr = self.path + '/' + self.ZoneToVictoryAnims[self.hoodId]
            animKey = "victory"
            animDict[animKey] = animStr
        if self.hoodId in self.ZoneToSadAnims:
            animStr = self.path + '/' + self.ZoneToSadAnims[self.hoodId]
            animKey = "sad"
            animDict[animKey] = animStr   
            
        self.trashcan.loadAnims(animDict)
        self.trashcan.pose('anim', 0)
        self.node = self.trashcan
        self.idleInterval = self.createIdleInterval()
        self.battleCheerInterval = self.createBattleCheerInterval()
        self.victoryInterval = self.createVictoryInterval()
        self.sadInterval = self.createSadInterval()
        
    def createIdleInterval(self):
        """Returns an interval that we use when w're just idling."""
        result = Sequence()
        if self.numIdles >= 3:
            numberOfAnimsAbove2 = self.numIdles - 2
            for rareIdle in xrange( 2, self.numIdles):
                for i in xrange(2):
                    result.append(ActorInterval( self.node, 'idle0'))
                    result.append(Wait(self.IdlePauseTime))
                    result.append(ActorInterval( self.node, 'idle1'))
                    result.append(Wait(self.IdlePauseTime))
                result.append(ActorInterval(self.node, 'idle%d' % rareIdle))
                result.append(Wait(self.IdlePauseTime))
        else:
            for i in xrange(self.numIdles):
                result.append(ActorInterval(self.node, "idle%d" % i))
        self.notify.debug("idle interval=%s" % result)                    
        return result

    def createBattleCheerText(self):
        """Create the text node to parent above the prop when he plays fight boost."""
        # Set the font
        self.HpTextGenerator.setFont(ToontownGlobals.getSignFont())
        
        # Show  the text
        self.HpTextGenerator.setText(self.BattleCheerText)
            
        # No shadow
        self.HpTextGenerator.clearShadow()

        # Center the number
        self.HpTextGenerator.setAlign(TextNode.ACenter)
        
        # Blue copied from DistributedSuitBase.showHPText
        r = 0
        g = 0
        b = 1
        a = 1

        self.HpTextGenerator.setTextColor(r, g, b, a)
                
        self.hpTextNode = self.HpTextGenerator.generate()
                
        # Put the hpText over the head of the avatar
        self.hpText = self.node.attachNewNode(self.hpTextNode)
        self.hpText.setScale(1)
        # Make sure it is a billboard
        self.hpText.setBillboardPointEye()
        # Render it after other things in the scene.
        self.hpText.setBin('fixed', 100)

        # Initial position ... Center of the body... the "tan tien"
        self.hpText.setPos( 0, 0, 4)
        self.hpText.hide()


    def createBattleCheerInterval(self):
        """Create a looping interval that the prop plays when buffing battles."""
        result=Sequence()
        for i in xrange(self.numFightAnims):
            animKey = "fight%d" % i
            animAndSoundIval = self.createAnimAndSoundIval(animKey)
            origAnimName = self.node.getAnimFilename(animKey).split('/')[-1]
            if self.hasOverrideIval(origAnimName):
                result.append(self.getOverrideIval(origAnimName))
            elif self.hasSpecialIval(origAnimName):
                result.append(Parallel(
                    animAndSoundIval,
                    self.getSpecialIval(origAnimName))
                              )
            else:
                result.append(animAndSoundIval)

        self.createBattleCheerText()
        battleCheerTextIval = Sequence(Func(self.hpText.show),
                                       self.hpText.posInterval(duration=4.0, pos = Vec3(0,0,7), startPos=(0,0,3)),
                                       Func(self.hpText.hide),
                                       )
                                            
        ivalWithText = Parallel( battleCheerTextIval,
                                 result)
        return ivalWithText

    def createSadInterval(self):
        """Create a looping interval that the prop plays when buffing battles."""
        result=Sequence()
        if self.hoodId in self.ZoneToSadAnims:
            result = self.createAnimAndSoundIval('sad')
        return result    

    def hasSpecialIval(self, origAnimName):
        """Returns true if for a given animation, it needs to play with a special interval."""
        # overriden by 'fightBoost' for mailbox interactive props'
        return False

    def getSpecialIval(self, origAnimName):
        """Returns an Interval if for a given animation, it needs to play with a special interval."""
        # overriden by 'fightBoost' for mailbox interactive props'
        return Sequence()

    def hasOverrideIval(self, origAnimName):
        """Returns true if for a given animation, it needs to play more than just an actor interval.

        If you have an override ival, code it to have the special ival if needed.
        """
        # overriden by 'fightBoost' for mailbox interactive props'
        return False

    def getOverrideIval(self, origAnimName):
        """Returns an Interval if for a given animation, it needs to play more than just an actor interval."""
        # overriden by 'fightBoost' for mailbox interactive props'
        return Sequence()      

    def createVictoryInterval(self):
        """Create a victory interval that the prop plays when toons win battles."""
        result=Sequence()
        if self.hoodId in self.ZoneToVictoryAnims:
            animAndSoundIval = self.createAnimAndSoundIval("victory")
            result.append(animAndSoundIval)
        return result    
        
    def enter(self):
        """Don't animate if props helping in battle is not turned on."""
        GenericAnimatedProp.GenericAnimatedProp.enter(self)
        if base.config.GetBool('props-buff-battles', True):
            self.notify.debug("props buff battles is true")
            # even if props-buff-battles is true we need to make sure the buff holiday is running
            # and since each holiday is prop specific, deal with it on the sub class
            if base.cr.newsManager.isHolidayRunning(self.holidayId):
                self.notify.debug("holiday is running, doing idle interval")
                self.node.stop()
                self.node.pose('idle0', 0 )
                if base.config.GetBool("interactive-prop-random-idles", 1):
                    self.requestIdleOrSad()
                else:
                    self.idleInterval.loop()
                pass
            else:
                # dont animate or do anything else
                self.notify.debug("holiday is NOT running, doing nothing")
                self.node.stop()
                self.node.pose('idle0', 0 )
        else:
            # dont animate or do anything else
            self.notify.debug("props do not buff battles")
            self.node.stop()
            self.node.pose('idle0', 0 )

    def exit(self):
        """Stop showing the prop."""
        assert self.notify.debugStateCall(self)
        self.okToStartNextAnim = False
        self.notify.debug("%s %d okToStartNextAnim=%s" % (self, self.visId,self.okToStartNextAnim))
        GenericAnimatedProp.GenericAnimatedProp.exit(self)
        self.request('Off')

    def requestIdleOrSad(self):
        """Go to sad if there's nearby cog buildings, doIdleAnim otherwise."""
        if not hasattr(self, 'node') or not self.node:
            self.notify.warning("requestIdleOrSad  returning hasattr(self,'node')=%s" % hasattr(self,'node'))
            return 
        if self.buildingsMakingMeSad:
            self.request("Sad")
        else:
            self.request("DoIdleAnim")

    def enterDoIdleAnim(self):
        """Start playing the appropriate animation."""
        self.notify.debug("enterDoIdleAnim numIdels=%d" % self.numIdles)
        self.okToStartNextAnim = True
        self.notify.debug("%s %d okToStartNextAnim=%s" % (self, self.visId,self.okToStartNextAnim))
        self.startNextIdleAnim()
        
    def exitDoIdleAnim(self):
        """Stop the currently playing animation."""
        self.notify.debug("exitDoIdlesAnim numIdles=%d" % self.numIdles)
        self.okToStartNextAnim = False
        self.notify.debug("%s %d okToStartNextAnim=%s" % (self, self.visId,self.okToStartNextAnim))
        self.calcLastIdleFrame()
        self.clearCurIval()

    def calcLastIdleFrame(self):
        """Store the currently playing idle information for a smooth transition."""
        if self.curIval and self.curIval.ivals:
            firstIval = self.curIval.ivals[0]
            # hmmm I want to test if it's ActorInterval, but I dont want to create another one
            if isinstance(firstIval, ActorInterval):
                self.lastIdleFrame = firstIval.getCurrentFrame()
                self.lastIdleAnimName = firstIval.animName
            elif isinstance(firstIval, Parallel):
                for testIval in firstIval.ivals:
                    if  isinstance(firstIval, ActorInterval):
                        self.lastIdleTime = testIval.getT()
                        self.lastIdleAnimName = testIval.animName
                        break

    def chooseIdleAnimToRun(self):
        """Returns a weighted number between 0 and self.numIdles, inclusive"""
        # e.g. if self.numIdles is 2, we have a 4/7 chance of picking 2
        # a 2/7 chance of picking 1
        # and a 1/7 chance of picking 0
        assert self.notify.debugStateCall(self)
        result = self.numIdles -1
        if base.config.GetBool('randomize-interactive-idles', True):
            pairs = []
            for i in xrange(self.numIdles):
                # actually we want idle2 to have a lower chance of occcurring
                # as it's the niftier idle compared to idle1 and idle0
                reversedChance = self.numIdles - i -1
                pairs.append(( math.pow(2,reversedChance) , i))
            sum = math.pow(2,self.numIdles) - 1
            result = weightedChoice(pairs, sum=sum)
            self.notify.debug("chooseAnimToRun numIdles=%s pairs=%s result=%s" %
                              (self.numIdles,pairs,result))
        else:
            # this makes debugging a heck of a lot easier
            # takes a really long time for AwesomeIdles to play
            result = self.lastPlayingAnimPhase + 1
            if result >= len(self.ZoneToIdles[self.hoodId]):
                result = 0 
        return result


    def startNextIdleAnim(self):
        """Start up the next anim sequence."""
        self.notify.debug("startNextAnim self.okToStartNextAnim=%s" % self.okToStartNextAnim)
        if not hasattr(self, 'node') or not self.node:
            self.notify.warning("startNextIdleAnim returning hasattr(self,'node')=%s" % hasattr(self,'node'))
            return
        self.curIval = None
        if self.okToStartNextAnim:
            self.notify.debug("got pass okToStartNextAnim")
            whichAnim = self.chooseIdleAnimToRun()
            if self.visId == localAvatar.zoneId:
                self.notify.debug("whichAnim=%s" % whichAnim)
                if __dev__:
                    self.notify.info("whichAnim=%s %s" % (whichAnim, self.getOrigIdleAnimName(whichAnim)))
            self.lastPlayingAnimPhase = whichAnim # merely for debugging
            self.curIval = self.createIdleAnimSequence(whichAnim)
            self.notify.debug("starting curIval of length %s" % self.curIval.getDuration())
            self.curIval.start()
        else:
            self.curIval = Wait(10) # just so we dont crash in exitIdleAnim
            self.notify.debug("false self.okToStartNextAnim=%s" %self.okToStartNextAnim)

    def createIdleAnimAndSoundInterval(self, whichIdleAnim, startingTime=0):
        """Return an interval which has the idle anim and sound, or just the anim as appropriate."""
        animIval = self.node.actorInterval("idle%d" % whichIdleAnim , startTime=startingTime)
        animIvalDuration = animIval.getDuration()
        origAnimName = self.ZoneToIdles[self.hoodId][whichIdleAnim]
        if isinstance(origAnimName , tuple):
           origAnimName = origAnimName[0]
        soundIval = self.createSoundInterval( origAnimName, animIvalDuration)
        soundIvalDuration = soundIval.getDuration()
        if self.hasSpecialIval(origAnimName):
            # used for debugging fightBoost isn't really an idle anim
            specialIval = self.getSpecialIval(origAnimName)
            idleAnimAndSound = Parallel( animIval, soundIval, specialIval)
        else:
            idleAnimAndSound = Parallel( animIval, soundIval)
        return idleAnimAndSound

    def createIdleAnimSequence(self, whichIdleAnim):
        """Return a sequence which plays an anims, waits the right time, then starts next one."""
        dummyResult = Sequence(Wait(self.IdlePauseTime))
        if not hasattr(self, 'node') or not self.node:
            self.notify.warning("createIdleAnimSequence returning dummyResult hasattr(self,'node')=%s" % hasattr(self,'node'))
            return dummyResult
        idleAnimAndSound = self.createIdleAnimAndSoundInterval(whichIdleAnim)            
        result = Sequence( idleAnimAndSound,
                           Wait(self.IdlePauseTime),
                           Func(self.startNextIdleAnim)
                           )
        if isinstance(self.ZoneToIdles[self.hoodId][whichIdleAnim] , tuple) and \
           len(self.ZoneToIdles[self.hoodId][whichIdleAnim]) > 2:
            # animation, minNumberOfLoops, maxNumberOfLoops, settleAnim, minPauseTime, maxPauseTime
            info = self.ZoneToIdles[self.hoodId][whichIdleAnim]
            origAnimName = info[0]
            minLoop = info[1]
            maxLoop = info[2]
            settleAnim = info[3]
            minPauseTime = info[4]
            maxPauseTime = info[5]
            assert( minLoop <= maxLoop)
            assert( minPauseTime <= maxPauseTime)
            numberOfLoops = random.randrange(minLoop, maxLoop+1)
            pauseTime = random.randrange(minPauseTime, maxPauseTime+1)
            result = Sequence()
            for i in xrange(numberOfLoops):
                result.append(idleAnimAndSound)
            if self.getSettleName(whichIdleAnim):
                result.append(self.node.actorInterval('settle%d' % whichIdleAnim))
            result.append(Wait(pauseTime))
            result.append(Func(self.startNextIdleAnim))                        
        
        # self.notify.debug("createAnimSequence %s" % result)
        return result

    def gotoFaceoff(self):
        """Request the face off state, so only the prop makes fsm requests."""
        self.notify.debugStateCall(self)
        if base.cr.newsManager.isHolidayRunning(self.holidayId):
            self.request("Faceoff")
        else:
            self.notify.debug("not going to faceoff because holiday %d is not running" %self.holidayId)            

    def gotoBattleCheer(self):
        """Request the battle cheer state, so only the prop makes fsm requests."""
        self.notify.debugStateCall(self)
        if base.cr.newsManager.isHolidayRunning(self.holidayId):
            self.request("BattleCheer")
        else:
            self.notify.debug("not going to battleCheer because holiday %d is not running" %self.holidayId)

    def gotoIdle(self):
        """Request the idle state, so only the prop makes fsm requests."""
        self.notify.debugStateCall(self)
        if base.cr.newsManager.isHolidayRunning(self.holidayId):
            self.request("DoIdleAnim")
        else:
            self.notify.debug("not going to idle because holiday %d is not running" %self.holidayId)

    def gotoVictory(self):
        """Request the battle cheer state, so only the prop makes fsm requests."""
        self.notify.debugStateCall(self)
        if base.cr.newsManager.isHolidayRunning(self.holidayId):
            self.request("Victory")
        else:
            self.notify.debug("not going to victory because holiday %d is not running" %self.holidayId)

    def gotoSad(self, buildingDoId):
        """Request the sad state, so only the prop makes fsm requests."""
        self.notify.debugStateCall(self)
        self.buildingsMakingMeSad.add(buildingDoId)
        if base.cr.newsManager.isHolidayRunning(self.holidayId):
            self.request("Sad")
        else:
            self.notify.debug("not going to sad because holiday %d is not running" %self.holidayId)

    def buildingLiberated(self,buildingDoId):
        """We got informed that a building has been tooned, go to idle if possible."""
        self.buildingsMakingMeSad.discard(buildingDoId)
        if not self.buildingsMakingMeSad:
            self.gotoIdle()
    
    def enterFaceoff(self):
        """Finish the last idle animation, then play idleIntoFight, then request battleCheer."""
        self.notify.debugStateCall(self)
        self.curIval = self.createFaceoffInterval()
        self.curIval.start()

    def exitFaceoff(self):
        """Exit the faceoff state, nothing for now."""
        # we must pause to avoid calling the func to go to battle cheer
        self.notify.debugStateCall(self)
        self.curIval.pause()
        self.curIval = None
        pass    

    def calcWhichIdleAnim(self, animName):
        """Given an anim name, which index does it correspond to."""
        result = 0        
        info = self.ZoneToIdles[self.hoodId]
        for index, curInfo in enumerate(info):
            if isinstance(curInfo, tuple):
                if curInfo[0] == animName:
                    result = index
                    break
            elif isinstance(curInfo, str):
                if curInfo == animName:
                    result = index
                    breal
        return result
                

    def createFaceoffInterval(self):
        """Creat an interval the finishes the last idle animation, then play idleIntoFight, then request battleCheer."""
        result = Sequence()
        if self.lastIdleAnimName:
            whichIdleAnim = self.calcWhichIdleAnim(self.lastIdleAnimName)
            animAndSound = self.createIdleAnimAndSoundInterval(whichIdleAnim, self.lastIdleTime)
            result.append(animAndSound)
        idleIntoFightIval = self.createAnimAndSoundIval("idleIntoFight")
        result.append(idleIntoFightIval)
        result.append(Func(self.gotoBattleCheer))
        return result
        
        
    def enterBattleCheer(self):
        """Loop ourself in the battle cheer interval."""
        self.notify.debugStateCall(self)
        self.curIval = self.battleCheerInterval
        self.curIval.loop()

    def exitBattleCheer(self):
        """Stop looping  ourself in the battle cheer interval."""
        self.notify.debugStateCall(self)
        self.curIval.finish()
        self.curIval = None

    def enterVictory(self):
        """Loop ourself in the victory interval."""
        self.notify.debugStateCall(self)
        self.curIval = self.victoryInterval
        self.curIval.loop()

    def exitVictory(self):
        """Stop looping ourself in the victory interval."""
        self.notify.debugStateCall(self)
        self.curIval.finish()
        self.curIval = None

    def enterSad(self):
        """Loop ourself in the sad interval."""
        self.notify.debugStateCall(self)
        self.curIval = self.sadInterval
        if self.curIval:
            self.curIval.loop()

    def exitSad(self):
        """Stop looping ourself in the sad interval."""
        self.notify.debugStateCall(self)
        self.curIval.finish()
        self.curIval = None
            
    def getSettleName(self, whichIdleAnim):
        """Checks if the settle anim is defined in self.ZoneToIdles, then returns that."""
        result = None
        if isinstance(self.ZoneToIdles[self.hoodId][whichIdleAnim] , tuple) and \
           len(self.ZoneToIdles[self.hoodId][whichIdleAnim]) > 3:
            result = self.ZoneToIdles[self.hoodId][whichIdleAnim][3]
        return result

    def getOrigIdleAnimName(self, whichIdleAnim):
        """Returns the original anim name for the Nth idle anim."""
        result = None
        if isinstance(self.ZoneToIdles[self.hoodId][whichIdleAnim] , tuple) :
            result = self.ZoneToIdles[self.hoodId][whichIdleAnim][0]
        else:
            result = self.ZoneToIdles[self.hoodId][whichIdleAnim]
        return result

    def createAnimAndSoundIval(self, animKey):
        """Return an interval for the anim animKey  and sound, or just the anim as appropriate."""
        animIval = self.node.actorInterval(animKey)
        animIvalDuration = animIval.getDuration()
        origAnimName = self.node.getAnimFilename(animKey)
        soundIval = self.createSoundInterval( origAnimName, animIvalDuration)
        soundIvalDuration = soundIval.getDuration()
        printFunc = Func(self.printAnimIfClose, animKey)
        if self.hasSpecialIval(origAnimName):
            # used in mailbox with pie delivery
            specialIval = self.getSpecialIval(origAnimName)
            idleAnimAndSound = Parallel( animIval, soundIval, specialIval)
            if base.config.GetBool("interactive-prop-info", False):
                idleAnimAndSound.append(printFunc)
        else:
            idleAnimAndSound = Parallel( animIval, soundIval)
            if base.config.GetBool("interactive-prop-info", False):
                idleAnimAndSound.append(printFunc)
        return idleAnimAndSound

    def printAnimIfClose(self,animKey):
        if base.config.GetBool("interactive-prop-info", False):
            try:
                animName = self.node.getAnimFilename(animKey)
                baseAnimName = animName.split('/')[-1]
                if localAvatar.zoneId == self.visId:
                    self.notify.info("playing %s" % baseAnimName)
            except Exception,e:
                self.notify.warning("Unknown error in printAnimIfClose, giving up:\n%s" % str(e))

    def clearCurIval(self):
        """Finish the current ival, then break garbage cycles."""
        if self.curIval:
            self.curIval.finish()
        clearPythonIvals(self.curIval)
        self.curIval = None

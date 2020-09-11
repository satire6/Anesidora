"""DistributedSuit module: contains the DistributedSuit class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.directtools.DirectGeometry import CLAMP
from direct.controls.ControlManager import CollisionHandlerRayStart
from direct.task import Task
from otp.otpbase import OTPGlobals
from otp.avatar import DistributedAvatar
import Suit
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import TTLocalizer
from toontown.battle import DistributedBattle
from direct.fsm import ClassicFSM
from direct.fsm import State
import SuitTimings
import SuitBase
import DistributedSuitPlanner
import SuitDNA
from direct.directnotify import DirectNotifyGlobal
import SuitDialog
from toontown.battle import BattleProps
import math
import copy




class DistributedSuitBase(DistributedAvatar.DistributedAvatar, Suit.Suit,
                          SuitBase.SuitBase):
    """
    DistributedSuit class:  a 'bad guy' which exists on each client's
     machine and helps direct the Suits which exist on the server.  This
     is the object that each individual player interacts with when
     initiating combat.  This guy has all of the attributes of a
     DistributedSuitAI object, plus some more such as collision info
    
    Attributes:
       Derived plus...
       DistributedSuit_initialized (integer), flag indicating if this
           suit has been properly initialized
       fsm, the state machine that this client suit will use, this
           includes states of detecting collisions with toons and
           entering battles
       dna, dna created for the suit, sent to us from the server
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitBase')

    def __init__(self, cr):
        try:
            self.DistributedSuitBase_initialized
            return
        except:
            self.DistributedSuitBase_initialized = 1
            
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        Suit.Suit.__init__(self)
        SuitBase.SuitBase.__init__(self)
        self.activeShadow = 0
        self.virtual = 0 #the red glowing effect

        # collision junk
        #
        self.battleDetectName = None
        
        self.cRay            = None
        self.cRayNode        = None
        self.cRayNodePath    = None
        self.cRayBitMask     = None
        self.lifter          = None
        self.cTrav           = None

        # our reference to the local hood's suit planner, the doId of
        # it is sent to us from the server side suit
        self.sp = None

        # Initialize this for setState() calls - child classes will
        # likely redefine this
        self.fsm = None

        # propellers for flying into and out of the streets
        self.prop = None
        self.propInSound = None
        self.propOutSound = None

        # make sure to hide the suit when first created, it is not yet
        # placed in the right location, so if its current location happens
        # to be on the street, we don't want it visible
        self.reparentTo(hidden)
        self.loop('neutral')
        
        # number of times to reanimate into a skeleCog
        self.skeleRevives = 0
        # keep track of how many times we have reanimated
        self.maxSkeleRevives = 0
        # if we were in the holiday when we started a silly surge, in case holiday ends in middle of battle
        self.sillySurgeText = False
        
        # use this for displaying hp bonus text
        self.interactivePropTrackBonus = -1
        
    def setVirtual(self, virtual):
        pass
        
    def getVirtual(self):
        return 0
        
    def setSkeleRevives(self, num):
        if num == None:
            num = 0
        self.skeleRevives = num
        if num > self.maxSkeleRevives:
            self.maxSkeleRevives = num
        if self.getSkeleRevives() > 0:
            nameInfo = TTLocalizer.SuitBaseNameWithLevel % {"name": self.name  ,
                                                            "dept":  self.getStyleDept(),
                                                            "level": ("%s%s" % (self.getActualLevel(), TTLocalizer.SkeleRevivePostFix)),}
            self.setDisplayName( nameInfo )
        else:
            nameInfo = TTLocalizer.SuitBaseNameWithLevel % {"name":  self.name,
                                                            "dept":  self.getStyleDept(),
                                                            "level": self.getActualLevel(),}
            self.setDisplayName( nameInfo )
            
        
    def getSkeleRevives(self):
        return self.skeleRevives

    def getMaxSkeleRevives(self):
        return self.maxSkeleRevives

    def generate(self):
        """
        This method is called when the DistributedObject is
        reintroduced to the world, either for the first
        time or from the cache.
        """
        assert(self.notify.debug("DistributedSuit %d: generating" %
                               self.getDoId()))
        DistributedAvatar.DistributedAvatar.generate(self)

    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        self.notify.debug("DistributedSuit %d: disabling" % self.getDoId())
        self.ignoreAll()
        self.__removeCollisionData()
        self.cleanupLoseActor()
        self.stop()
        taskMgr.remove(self.uniqueName('blink-task'))
        DistributedAvatar.DistributedAvatar.disable(self)
 
    def delete(self):
        """
        This method is called when the DistributedObject is
        permanently removed from the world and deleted from
        the cache.
        """
        try:
            self.DistributedSuitBase_deleted
        except:
            self.DistributedSuitBase_deleted = 1
            self.notify.debug("DistributedSuit %d: deleting" % self.getDoId())

            del self.dna
            del self.sp

            DistributedAvatar.DistributedAvatar.delete(self)
            Suit.Suit.delete(self)
            SuitBase.SuitBase.delete(self)

    # We need to force the Suit version of these to be called, otherwise
    # we get the generic Avatar version which is undefined
    def setDNAString(self, dnaString):
        Suit.Suit.setDNAString(self, dnaString)

    def setDNA(self, dna):
        Suit.Suit.setDNA(self, dna)

    def getHP(self):
        return self.currHP

    def setHP(self, hp):
        """
        Function:    set the current health of this suit, this can
                     be called during battle and at initialization
        Parameters:  hp, value to set health to
        """
        if hp > self.maxHP:
            self.currHP = self.maxHP
        else:
            self.currHP = hp
        return None

    def getDialogueArray(self, *args):
        # Force the right inheritance chain to be called
        return Suit.Suit.getDialogueArray(self, *args)

    def __removeCollisionData(self):
        """
        clean up the suit's various collision data such
        as the battle detection sphere, the ground collision
        ray, and the lifter
        """
        # make sure to remove any raycast information
        #
        self.enableRaycast(0)

        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None

        self.lifter = None

        self.cTrav = None

    def setHeight(self, height):
        # We want to make sure we get the specialized one.
        Suit.Suit.setHeight(self, height)

    def getRadius(self):
        # We want to make sure we get the specialized one.
        return Suit.Suit.getRadius(self)

    def setLevelDist(self, level):
        """
        level is the new level (int) of the suit.
        
        The distributed function to be called when the
        server side suit changes level
        """
        if self.notify.getDebug():
            self.notify.debug("Got level %d from server for suit %d" % \
                               (level, self.getDoId()))
        self.setLevel(level)

    def attachPropeller(self):
        """
        attach a propeller to this suit, used when the suit
        is going into it's flying animation
        """
        if self.prop == None:
            self.prop = BattleProps.globalPropPool.getProp('propeller')
        if self.propInSound == None:
            self.propInSound = base.loadSfx("phase_5/audio/sfx/ENC_propeller_in.mp3")
        if self.propOutSound == None:
            self.propOutSound = base.loadSfx("phase_5/audio/sfx/ENC_propeller_out.mp3")
        head = self.find("**/joint_head")
        self.prop.reparentTo(head)

    def detachPropeller(self):
        """
        remove the propeller from a suit if it has one, this
        is used after a suit is done with its flying anim
        """
        if self.prop:
            self.prop.removeNode()
            self.prop = None
        if self.propInSound:
            self.propInSound = None
        if self.propOutSound:
            self.propOutSound = None

    def beginSupaFlyMove(self, pos, moveIn, trackName):
        """
        beginSupaFlyMove(self, Point3 pos, bool moveIn, string trackName)

        Returns an interval that will animate the suit either up into
        the sky or back down to the ground, based on moveIn.

        pos is the point on the street over which the animation takes
        place.
        """
        skyPos = Point3(pos)

        # calculate a point in the sky based on how fast a suit walks
        # and how long it has been determined that flying away should take
        #
        if moveIn:
            skyPos.setZ(pos.getZ() + (SuitTimings.fromSky *
                                      ToontownGlobals.SuitWalkSpeed))
        else:
            skyPos.setZ(pos.getZ() + (SuitTimings.toSky *
                                      ToontownGlobals.SuitWalkSpeed))

        # calculate some times used to manipulate the suit's landing
        # animation
        #
        groundF = 28
        dur = self.getDuration('landing')
        fr = self.getFrameRate('landing')
        
        # length of time in animation spent in the air
        animTimeInAir = groundF/fr
        # length of time in animation spent impacting and reacting to
        # the ground
        impactLength = dur - animTimeInAir
        # the frame at which the suit touches the ground
        timeTillLanding = SuitTimings.fromSky - impactLength
        # time suit spends playing the flying portion of the landing anim
        waitTime = timeTillLanding - animTimeInAir

        # now create info for the propeller's animation
        #
        if self.prop == None:
            self.prop = BattleProps.globalPropPool.getProp('propeller')
        propDur = self.prop.getDuration('propeller')
        lastSpinFrame = 8
        fr = self.prop.getFrameRate('propeller')
        # time from beginning of anim at which propeller plays its spin
        spinTime = lastSpinFrame/fr
        # time from beginning of anim at which propeller starts to close
        openTime = (lastSpinFrame + 1) / fr

        if moveIn:
            # if we are moving into the neighborhood from the sky, move
            # down from above (skyPos) the first waypoint in the suit's
            # current path (pos), first create an interval that will
            # move the suit over time, then create a function interval
            # to set the suit's animation to a single frame (the first)
            # of the landing animation, then create a wait interval to
            # wait for the suit to get closer to the ground, then create
            # an actor interval to play the landing animation so it ends
            # when the suit touches the ground, and lastly create a
            # function interval to make sure the suit goes into it's
            # walk animation once it lands
            #

            # create the lerp intervals that will go in the first track,
            # also reparent the suit's shadow to render and set the
            # position of it below the suit on the ground
            #
            lerpPosTrack = Sequence(
                self.posInterval(timeTillLanding, pos, startPos=skyPos),
                Wait(impactLength),
                )


            shadowScale = self.dropShadow.getScale()
            
            # create a scale interval for the suit's shadow so it scales
            # up as the suit gets closer to the ground
            #
            # keep Z scale at 1. so that lifter doesn't go crazy-go-nuts and set Z to infinity
            shadowTrack = Sequence(
                Func(self.dropShadow.reparentTo, render),
                Func(self.dropShadow.setPos, pos),
                self.dropShadow.scaleInterval(timeTillLanding, self.scale,
                                              startScale = Vec3(0.01, 0.01, 1.)),
                Func(self.dropShadow.reparentTo, self.getShadowJoint()),
                Func(self.dropShadow.setPos, 0, 0, 0),
                Func(self.dropShadow.setScale, shadowScale),
                )

            fadeInTrack = Sequence(
                Func(self.setTransparency, 1),
                self.colorScaleInterval(1, colorScale = VBase4(1, 1, 1, 1),
                                        startColorScale = VBase4(1, 1, 1, 0)),
                Func(self.clearColorScale),
                Func(self.clearTransparency),
                )

            # now create the suit animation intervals that will go in the
            # second track
            #
            animTrack = Sequence(
                Func(self.pose, 'landing', 0),
                Wait(waitTime),
                ActorInterval(self, 'landing', duration = dur),
                Func(self.loop, 'walk'),
                )

            # now create the propeller animation intervals that will go in
            # the third and final track
            #
            self.attachPropeller()
            propTrack = Parallel(
                SoundInterval(self.propInSound, duration = waitTime + dur,
                              node = self),
                Sequence(ActorInterval(self.prop, 'propeller',
                                       constrainedLoop = 1,
                                       duration = waitTime + spinTime,
                                       startTime = 0.0,
                                       endTime = spinTime),
                         ActorInterval(self.prop, 'propeller',
                                       duration = propDur - openTime,
                                       startTime = openTime),
                         Func(self.detachPropeller),
                         ),
                )

            return Parallel(lerpPosTrack,
                            shadowTrack,
                            fadeInTrack,
                            animTrack,
                            propTrack,
                            name = self.taskName('trackName')
                            )
        else:
            # move to the sky, move vertically from the current
            # position to some location in the sky, also reparent the
            # suit's shadow to render and set the position of it below
            # the suit on the ground
            #
            lerpPosTrack = Sequence(
                Wait(impactLength),
                LerpPosInterval(self, timeTillLanding, skyPos,
                                startPos=pos),
                )

            # create a scale interval for the suit's shadow so it scales
            # down as the suit gets further from the ground
            #
            # keep Z scale at 1. so that lifter doesn't go crazy-go-nuts and set Z to infinity
            shadowTrack = Sequence(
                Func(self.dropShadow.reparentTo, render),
                Func(self.dropShadow.setPos, pos),
                self.dropShadow.scaleInterval(timeTillLanding, Vec3(0.01, 0.01, 1.),
                                              startScale = self.scale),
                Func(self.dropShadow.reparentTo, self.getShadowJoint()),
                Func(self.dropShadow.setPos, 0, 0, 0),
                )

            fadeOutTrack = Sequence(
                Func(self.setTransparency, 1),
                self.colorScaleInterval(1, colorScale = VBase4(1, 1, 1, 0),
                                        startColorScale = VBase4(1, 1, 1, 1)),
                Func(self.clearColorScale),
                Func(self.clearTransparency),
                Func(self.reparentTo, hidden),
                )
                

            # create the suit animation intervals which will go into
            # a second track
            #
            actInt = ActorInterval(self, 'landing', loop = 0,
                                   startTime = dur,
                                   endTime = 0.0)

            # now create the propeller animation intervals that will go in
            # the third and final track
            #
            self.attachPropeller()
            self.prop.hide()
            propTrack = Parallel(
                SoundInterval(self.propOutSound, duration = waitTime + dur,
                              node = self),
                Sequence(Func(self.prop.show),
                         ActorInterval(self.prop, 'propeller',
                                       endTime = openTime,
                                       startTime = propDur),
                         ActorInterval(self.prop, 'propeller',
                                       constrainedLoop = 1,
                                       duration = propDur - openTime,
                                       startTime = spinTime,
                                       endTime = 0.0),
                         Func(self.detachPropeller),
                         ),
                )

            return Parallel(ParallelEndTogether(lerpPosTrack,
                                                shadowTrack,
                                                fadeOutTrack),
                            actInt,
                            propTrack,
                            name = self.taskName('trackName')
                            )

    def enableBattleDetect(self, name, handler):
        if self.collTube:
            # We recreate the sphere node every time we switch states
            # to force the collision event to be regenerated even if
            # the avatar was already within the suit's bubble.
            self.battleDetectName = self.taskName(name)
            self.collNode = CollisionNode(self.battleDetectName)
            self.collNode.addSolid(self.collTube)
            self.collNodePath = self.attachNewNode(self.collNode)
            self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
            self.accept("enter" + self.battleDetectName, handler)

        return Task.done

    def disableBattleDetect(self):
        if self.battleDetectName:
            self.ignore("enter" + self.battleDetectName)
            self.battleDetectName = None
        if self.collNodePath:
            self.collNodePath.removeNode()
            self.collNodePath = None

    def enableRaycast(self, enable=1):
        """
        enable/disable raycast, useful for when we know
        when the suit will change elevations
        """
        if (not self.cTrav
                or not hasattr(self, "cRayNode")
                or not self.cRayNode):
            return

        self.cTrav.removeCollider(self.cRayNodePath)
        if enable:
            if self.notify.getDebug():
                self.notify.debug("enabling raycast")
            self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        else:
            if self.notify.getDebug():
                self.notify.debug("disabling raycast")

    # setBrushOff
    def b_setBrushOff(self, index):
        # Local
        self.setBrushOff(index)
        # Distributed
        self.d_setBrushOff(index)

    def d_setBrushOff(self, index):
        self.sendUpdate("setBrushOff", [index])

    def setBrushOff(self, index):
        self.setChatAbsolute(SuitDialog.getBrushOffText(self.getStyleName(), index),
                             CFSpeech | CFTimeout)

    def initializeBodyCollisions(self, collIdStr):
        """
        set up collision information for this cog,
        only do once when creating the cog
        """
        DistributedAvatar.DistributedAvatar.initializeBodyCollisions(self, collIdStr)

        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)        

        # Set up the collison ray
        # This is a ray cast from your head down to detect floor polygons
        # and is only turned on during specific parts of the suit's path
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode(self.taskName("cRay"))
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())

        # set up floor collision mechanism
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        self.lifter.setReach(6.0)

        # Limit our rate-of-fall with the lifter.
        self.lifter.setMaxVelocity(8.0)
        self.lifter.addCollider(self.cRayNodePath, self)

        # now use the standard collision traverser to handle updating
        # collision info
        self.cTrav = base.cTrav

    def disableBodyCollisions(self):
        self.disableBattleDetect()
        self.enableRaycast(0)
        if self.cRayNodePath:
            self.cRayNodePath.removeNode()
        del self.cRayNode
        del self.cRay
        del self.lifter

    def denyBattle(self):
        self.notify.debug('denyBattle()')

        # Deny the local toon's request for battle.  This is only sent
        # directly to a toon who requested the battle; other toons in
        # the zone don't see this message.
        
        place = self.cr.playGame.getPlace()
        if place.fsm.getCurrentState().getName() == 'WaitForBattle':
            place.setState('walk')
        self.resumePath(self.pathState)

    def makePathTrack(self, nodePath, posPoints, velocity, name):
        track = Sequence(name = name)
        assert len(posPoints) > 1
        restOfPosPoints = posPoints[1:]
        for pointIndex in range(len(posPoints) - 1):
            startPoint = posPoints[pointIndex]
            endPoint = posPoints[pointIndex + 1]
            # Face the endpoint
            track.append(
                Func(nodePath.headsUp,
                     endPoint[0], endPoint[1], endPoint[2])
                )
            # Calculate the amount of time we should spend walking
            distance = Vec3(endPoint - startPoint).length()
            duration = distance / velocity

            # Walk to the end point
            track.append(
                LerpPosInterval(nodePath, duration=duration,
                                pos=Point3(endPoint),
                                startPos=Point3(startPoint))
                )
        return track

    def setState(self, state):
        if (self.fsm == None):
            return 0
        # check to make sure we aren't going into the state we are already
        # in, this is useful so we don't go into the Off state when already
        # in the off state, which will result in the stopping of a currently
        # playing track
        #
        if (self.fsm.getCurrentState().getName() == state):
            assert(self.notify.debug("State change ignored, already in " +
                                   "state" + str(state)))
            return 0
        return self.fsm.request(state)

    # Specific State functions

    ##### Off state #####

    def subclassManagesParent(self):
        # factory suits are parented under other nodes, and the
        # parent info doesn't need to be distributed
        return 0

    def enterOff(self, *args):
        assert self.notify.debug('enterOff()')
        self.hideNametag3d()
        self.hideNametag2d()
        if not self.subclassManagesParent():
            self.setParent(ToontownGlobals.SPHidden)

    def exitOff(self):
        if not self.subclassManagesParent():
            self.setParent(ToontownGlobals.SPRender)
        self.showNametag3d()
        self.showNametag2d()
        self.loop('neutral', 0)

    ##### Battle state #####

    def enterBattle(self):
        # Join a battle object and let it take over control of the suit
        assert self.notify.debug('DistributedSuit: entering a Battle')
        self.loop('neutral', 0)
        self.disableBattleDetect()
        self.corpMedallion.hide()
        self.healthBar.show()
        # make sure health bar updates current suit condition
        if self.currHP < self.maxHP:
            self.updateHealthBar(0, 1)
            
    def exitBattle(self):
        self.healthBar.hide()
        self.corpMedallion.show()
        self.currHP = self.maxHP
        self.interactivePropTrackBonus = -1
    ##### WaitForBattle state #####

    def enterWaitForBattle(self):
        self.loop('neutral', 0)

    def exitWaitForBattle(self):
        pass

    def setSkelecog(self, flag):
        SuitBase.SuitBase.setSkelecog(self, flag)
        if flag:
            Suit.Suit.makeSkeleton(self)

    def showHpText(self, number, bonus=0, scale=1, attackTrack =-1):
        if self.HpTextEnabled and not self.ghostMode:           
            # We don't show zero change.
            if number != 0:
                # Get rid of the number if it is already there.
                if self.hpText:
                    self.hideHpText()
                # Set the font
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                # Show both negative and positive signs
                if number < 0:
                    self.HpTextGenerator.setText(str(number))
                    # If we're doing the Silly Holiday word additions
                    if base.cr.newsManager.isHolidayRunning(ToontownGlobals.SILLY_SURGE_HOLIDAY):
                        self.sillySurgeText = True
                        absNum = abs(number)
                        if absNum > 0 and absNum <= 10:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[1])
                        elif absNum > 10 and absNum <= 20:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[2])                           
                        elif absNum > 20 and absNum <= 30:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[3])  
                        elif absNum > 30 and absNum <= 40:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[4])  
                        elif absNum > 40 and absNum <= 50:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[5])  
                        elif absNum > 50 and absNum <= 60:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[6])  
                        elif absNum > 60 and absNum <= 70:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[7])  
                        elif absNum > 70 and absNum <= 80:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[8])  
                        elif absNum > 80 and absNum <= 90:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[9])  
                        elif absNum > 90 and absNum <= 100:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[10])  
                        elif absNum > 100 and absNum <= 110:
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[11])
                        else: # greater than 110
                            self.HpTextGenerator.setText(str(number) + "\n" + TTLocalizer.SillySurgeTerms[12])
                    
                    # check for interactive prop gag track bonus
                    if self.interactivePropTrackBonus > -1 and self.interactivePropTrackBonus == attackTrack:
                        self.sillySurgeText = True
                        if attackTrack in TTLocalizer.InteractivePropTrackBonusTerms:
                            self.HpTextGenerator.setText(str(number) + "\n" +
                                                         TTLocalizer.InteractivePropTrackBonusTerms[attackTrack])
                else:
                    self.HpTextGenerator.setText("+" + str(number))
                # No shadow
                self.HpTextGenerator.clearShadow()
                # Put a shadow on there
                #self.HpTextGenerator.setShadow(0.05, 0.05)
                #self.HpTextGenerator.setShadowColor(0, 0, 0, 1)
                # Center the number
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                # Red for negative, green for positive, yellow for bonus
                if bonus == 1:
                    r = 1.0
                    g = 1.0
                    b = 0
                    a = 1
                elif bonus == 2:
                    r = 1.0
                    g = 0.5
                    b = 0
                    a = 1
                elif number < 0:
                    r = 0.9
                    g = 0
                    b = 0
                    a = 1
                    # if we have a track bonus, for now make it blue
                    if self.interactivePropTrackBonus > -1 and self.interactivePropTrackBonus == attackTrack:
                        r = 0
                        g = 0
                        b = 1
                        a = 1
                else:
                    r = 0
                    g = 0.9
                    b = 0
                    a = 1
                    
                self.HpTextGenerator.setTextColor(r, g, b, a)

                self.hpTextNode = self.HpTextGenerator.generate()
                
                # Put the hpText over the head of the avatar
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                # Make sure it is a billboard
                self.hpText.setBillboardPointEye()
                # Render it after other things in the scene.
                self.hpText.setBin('fixed', 100)
                if self.sillySurgeText:               
                    self.nametag3d.setDepthTest(0)
                    self.nametag3d.setBin('fixed', 99)
                
                # Initial position ... Center of the body... the "tan tien"
                self.hpText.setPos(0, 0, self.height/2)
                seq = Task.sequence(
                    # Fly the number out of the character
                    self.hpText.lerpPos(Point3(0, 0, self.height + 1.5),
                                            1.0,
                                            blendType = 'easeOut'),
                    # Wait 2 seconds
                    Task.pause(0.85),
                    # Fade the number
                    self.hpText.lerpColor(Vec4(r, g, b, a),
                                              Vec4(r, g, b, 0),
                                              0.1),
                    # Get rid of the number
                    Task.Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName("hpText"))
        else:
            # Just play the sound effect.
            # TODO: Put in the sound effect!
            pass

    def hideHpTextTask(self, task):
        self.hideHpText()
        # If we're doing the Silly Holiday word additions
        if self.sillySurgeText:
            self.nametag3d.clearDepthTest()
            self.nametag3d.clearBin()
            self.sillySurgeText = False
        return Task.done            


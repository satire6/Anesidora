"""MazeSuit module: contains the CogThief class"""
import math
from pandac.PandaModules import CollisionSphere, CollisionNode, Point3, CollisionTube, \
     Vec3, rad2Deg
from direct.showbase.DirectObject import DirectObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import Parallel, SoundInterval, \
     Sequence, Func, LerpScaleInterval
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.minigame import CogThiefGameGlobals
from toontown.battle.BattleProps import globalPropPool
from toontown.battle.BattleSounds  import globalBattleSoundCache

CTGG = CogThiefGameGlobals
class CogThief(DirectObject):
    """This represents a single cog thief in the cog thief game"""
    notify = directNotify.newCategory("CogThief")
    DefaultSpeedWalkAnim = 4.
    CollisionRadius = 1.25
    MaxFriendsVisible = 4
    Infinity = 100000.0 # just a really big number
    SeparationDistance = 6.0
    MinUrgency = 0.5
    MaxUrgency = 0.75   
    
    def __init__(self, cogIndex, suitType, game, cogSpeed):
        self.cogIndex = cogIndex
        self.suitType = suitType
        self.game = game
        self.cogSpeed = cogSpeed
        suit = Suit.Suit()
        d = SuitDNA.SuitDNA()
        d.newSuit(suitType)
        suit.setDNA(d)
        # cache the walk anim
        suit.pose('walk', 0)
        self.suit = suit
        self.goal = CTGG.NoGoal
        self.goalId = CTGG.InvalidGoalId
        self.lastLocalTimeStampFromAI = 0
        self.lastPosFromAI = Point3(0,0,0)
        self.lastThinkTime = 0
        self.doneAdjust = False
        self.barrel = CTGG.NoBarrelCarried
        self.signalledAtReturnPos = False
        self.defaultPlayRate = 1.0
        self.netTimeSentToStartByHit = 0

        # steering loosely based on boid code game programming gems #1
        # "Portions Copyright (C) Steven Woodcock, 2000"
        self.velocity = Vec3(0,0,0)
        self.oldVelocity = Vec3(0,0,0)
        self.acceleration = Vec3(0,0,0)
        self.bodyLength = self.CollisionRadius *2
        # Desired distance from closest neighbor when flying.
        self.cruiseDistance = 2 * self.bodyLength
        self.maxVelocity = self.cogSpeed
        # Maximum magnitude of acceleration as a fraction of maxSpeed.
        self.maxAcceleration = 5.0
        self.perceptionRange = 6;
        self.notify.debug('cogSpeed=%s' % self.cogSpeed)

        self.kaboomSound = loader.loadSfx("phase_4/audio/sfx/MG_cannon_fire_alt.mp3")
        self.kaboom = loader.loadModel('phase_4/models/minigames/ice_game_kaboom')
        self.kaboom.setScale(2.0)
        self.kaboom.setBillboardPointEye()
        self.kaboom.hide()
        self.kaboomTrack = None

        splatName = 'splat-creampie'
        self.splat = globalPropPool.getProp(splatName)
        self.splat.setBillboardPointEye()
        self.splatType = globalPropPool.getPropType(splatName)

        self.pieHitSound = globalBattleSoundCache.getSound('AA_wholepie_only.mp3')

        
    def destroy(self):
        self.ignoreAll()
        self.suit.delete()
        self.game = None
        
    def uniqueName(self, baseStr):
        return baseStr + '-' + str(self.game.doId)

    def handleEnterSphere(self, collEntry):
        """Handle the suit colliding with localToon."""
        #assert self.notify.debugStateCall(self)
        intoNp =  collEntry.getIntoNodePath()
        self.notify.debug('handleEnterSphere suit %d hit %s' %
                          (self.cogIndex,intoNp))
        if self.game: 
            self.game.handleEnterSphere(collEntry)


    def gameStart(self, gameStartTime):
        self.gameStartTime = gameStartTime
        
        self.initCollisions()
        self.startWalkAnim()

    def gameEnd(self):
        self.moveIval.pause()
        del self.moveIval
        
        self.shutdownCollisions()

        # keep the suits from walking in place
        self.suit.loop('neutral')

    def initCollisions(self):
        # Make a sphere, give it a unique name, and parent it
        # to the suit.
        self.collSphere = CollisionSphere(0, 0, 0, 1.25)
        # Make he sphere intangible
        self.collSphere.setTangible(1)
        name = "CogThiefSphere-%d" % self.cogIndex
        self.collSphereName = self.uniqueName(name)
        self.collNode = CollisionNode(self.collSphereName)
        self.collNode.setIntoCollideMask(CTGG.BarrelBitmask |
                                         ToontownGlobals.WallBitmask )
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.suit.attachNewNode(self.collNode)
        #self.collNodePath.hide()

        # Add a hook looking for collisions with localToon
        self.accept('enter' + self.collSphereName,
                    self.handleEnterSphere)

        # we need a taller collision tube to collide against for pie
        self.pieCollSphere = CollisionTube(0, 0, 0, 0, 0, 4, self.CollisionRadius)
        # Make he sphere intangible
        self.pieCollSphere.setTangible(1)
        name = "CogThiefPieSphere-%d" % self.cogIndex
        self.pieCollSphereName = self.uniqueName(name)
        self.pieCollNode = CollisionNode(self.pieCollSphereName)
        self.pieCollNode.setIntoCollideMask(ToontownGlobals.PieBitmask )
        self.pieCollNode.addSolid(self.pieCollSphere)
        self.pieCollNodePath = self.suit.attachNewNode(self.pieCollNode)        
        #self.pieCollNodePath.show()

        # Add a hook looking for collisions with localToon
        #self.accept('enter' + self.pieCollSphereName,
        #            self.handleEnter)        

    def shutdownCollisions(self):
        self.ignore(self.uniqueName('enter' + self.collSphereName))
        
        del self.collSphere
        self.collNodePath.removeNode()
        del self.collNodePath
        del self.collNode

    def updateGoal(self, timestamp, inResponseClientStamp, goalType, goalId, pos):
        """Update our goal and position."""
        assert self.notify.debugStateCall(self)
        self.notify.debug('self.netTimeSentToStartByHit =%s' % self.netTimeSentToStartByHit )
        if not self.game:
            self.notify.debug('updateGoal self.game is None, just returning')
            return
        if not self.suit:
            self.notify.debug('updateGoal self.suit is None, just returning')
            return
        if self.goal == CTGG.NoGoal:
            self.startWalkAnim()

        if goalType == CTGG.NoGoal:
            self.notify.debug('updateGoal setting position to %s' % pos)
            self.suit.setPos(pos)

        self.lastThinkTime = 0
        self.velocity = Vec3(0,0,0)
        self.oldVelocity = Vec3(0,0,0)
        self.acceleration = Vec3(0,0,0)

        if goalType == CTGG.RunAwayGoal:
            #import pdb; pdb.set_trace()
            pass
        
        if inResponseClientStamp < self.netTimeSentToStartByHit and \
           self.goal == CTGG.NoGoal and \
           goalType == CTGG.RunAwayGoal:
            #import pdb; pdb.set_trace()
            self.notify.warning('ignoring newGoal %s as cog %d was recently hit responsetime=%s hitTime=%s' %
                                (CTGG.GoalStr[goalType], self.cogIndex,
                                 inResponseClientStamp, self.netTimeSentToStartByHit))
        else:
            self.lastLocalTimeStampFromAI = globalClockDelta.networkToLocalTime(timestamp, bits=32)
            self.goal = goalType
            self.goalId = goalId
            self.lastPosFromAI = pos
            self.doneAdjust = False
        self.signalledAtReturnPos = False
        # TODO move the suit to where we expect him to be given the time difference

        
    def startWalkAnim(self):
        if self.suit:
            self.suit.loop('walk')
            speed = self.cogSpeed # float(MazeData.CELL_WIDTH) / self.cellWalkDuration
            self.defaultPlayRate = float(self.cogSpeed / self.DefaultSpeedWalkAnim)
            self.suit.setPlayRate( self.defaultPlayRate, 'walk')
        
    def think(self):
        """Calculate where we should go."""
        if self.goal == CTGG.ToonGoal:
            self.thinkAboutCatchingToon()
        elif self.goal == CTGG.BarrelGoal:
            self.thinkAboutGettingBarrel()
        elif self.goal == CTGG.RunAwayGoal:
            self.thinkAboutRunAway()

    def thinkAboutCatchingToon(self):
        if not self.game:
            return

        av = self.game.getAvatar(self.goalId)        
        if av:
            if not self.lastThinkTime:
                self.lastThinkTime = globalClock.getFrameTime()
            diffTime = globalClock.getFrameTime() - self.lastThinkTime            
            avPos = av.getPos()            
            myPos = self.suit.getPos()

            if not self.doneAdjust:            
                myPos = self.lastPosFromAI
                self.notify.debug('thinkAboutCatchingToon not doneAdjust setting pos %s'
                                  % myPos)
                self.doneAdjust = True
                                  
            self.suit.setPos(myPos)
            
            if self.game.isToonPlayingHitTrack(self.goalId):
                # do nothing, just look at toon
                self.suit.headsUp(av)
                self.velocity = Vec3(0,0,0)
                self.oldVelocity = Vec3(0,0,0)
                self.acceleration = Vec3(0,0,0)
            else:
                self.commonMove()
            
            newPos = self.suit.getPos()
            self.adjustPlayRate(newPos, myPos, diffTime)
            
        self.lastThinkTime = globalClock.getFrameTime()

    def convertNetworkStampToGameTime(self, timestamp):
        """Convert a network timestamp to game time."""
        localStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
        gameTime = self.game.local2GameTime(localStamp)
        return gameTime
        

    def respondToToonHit(self, timestamp):
        """The toon hit us, react appropriately."""
        assert self.notify.debugStateCall(self)
        localStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
        # using 1.0 sec as fudge
        #if localStamp > self.lastLocalTimeStampFromAI:
        if self.netTimeSentToStartByHit < timestamp:
            self.clearGoal()
            self.showKaboom()
            # move him to his starting postion
            startPos = CTGG.CogStartingPositions[self.cogIndex]
            oldPos = self.suit.getPos()
            self.suit.setPos(startPos)
            if self.netTimeSentToStartByHit < timestamp:
                self.netTimeSentToStartByHit = timestamp
        else:
            self.notify.debug('localStamp = %s, lastLocalTimeStampFromAI=%s, ignoring respondToToonHit' % (localStamp, self.lastLocalTimeStampFromAI))
        self.notify.debug('respondToToonHit self.netTimeSentToStartByHit = %s' % self.netTimeSentToStartByHit)

    def clearGoal(self):
        """Clear goal and goal id."""
        self.goal = CTGG.NoGoal
        self.goalId = CTGG.InvalidGoalId

    def thinkAboutGettingBarrel(self):
        """Go for  a barrel."""
        if not self.game:
            return
        
        if not hasattr(self.game, 'barrels'):
            return
        if not self.goalId in xrange(len(self.game.barrels)):
            return

        if not self.lastThinkTime:
            self.lastThinkTime = globalClock.getFrameTime()
        diffTime = globalClock.getFrameTime() - self.lastThinkTime
        barrel = self.game.barrels[self.goalId]
        barrelPos = barrel.getPos()
        myPos = self.suit.getPos() 
        if not self.doneAdjust:            
            myPos = self.lastPosFromAI
            self.notify.debug('thinkAboutGettingBarrel not doneAdjust setting position to %s' % myPos)            
            self.suit.setPos(myPos)
            """
            diffTime = globalClock.getFrameTime()- self.lastLocalTimeStampFromAI
            self.notify.debug('doing adjust, diffTime = %s' % diffTime)
            if diffTime < 0:
                # it just looks really weird when it moves backwards
                diffTime = 0
                self.notify.debug('forcing diffTime to %s' % diffTime)
            """
            self.doneAdjust = True            
        displacement = barrelPos - myPos
        distanceToToon = displacement.length()
        #self.notify.debug('diffTime = %s' % diffTime)
        self.suit.headsUp(barrel)
        lengthTravelled = diffTime  * self.cogSpeed
        #self.notify.debug('lengthTravelled = %s' % lengthTravelled)
        # don't overshoot our target
        if lengthTravelled > distanceToToon:
            lengthTravelled = distanceToToon
            #self.notify.debug('overshooting lengthTravelled = %s' % lengthTravelled)
        displacement.normalize()
        dirVector = displacement
        dirVector *= lengthTravelled
        newPos = myPos + dirVector
        # always keep them grounded
        newPos.setZ(0)
        self.suit.setPos(newPos)
        self.adjustPlayRate(newPos, myPos, diffTime)
            
        self.lastThinkTime = globalClock.getFrameTime()

    def stopWalking(self, timestamp):
        """Stop the cog from walking."""
        localStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
        if localStamp > self.lastLocalTimeStampFromAI:
            self.suit.loop('neutral')
            self.clearGoal()

    def thinkAboutRunAway(self):
        """Go for  a barrel."""
        if not self.game:
            return
        if not self.lastThinkTime:
            self.lastThinkTime = globalClock.getFrameTime()
        diffTime = globalClock.getFrameTime() - self.lastThinkTime

        returnPos = CTGG.CogReturnPositions[self.goalId]
        myPos = self.suit.getPos() 
        if not self.doneAdjust:
            myPos = self.lastPosFromAI
            self.suit.setPos(myPos)
            """
            diffTime = globalClock.getFrameTime()- self.lastLocalTimeStampFromAI
            self.notify.debug('run away doing adjust, diffTime = %s' % diffTime)
            if diffTime < 0:
                # it just looks really weird when it moves backwards
                diffTime = 0
                self.notify.debug('forcing diffTime to %s' % diffTime)
            """
            self.doneAdjust = True            
        displacement = returnPos - myPos
        distanceToToon = displacement.length()
        #self.notify.debug('diffTime = %s' % diffTime)
        tempNp = render.attachNewNode('tempRet')
        tempNp.setPos(returnPos)
        self.suit.headsUp(tempNp)
        tempNp.removeNode()
        lengthTravelled = diffTime  * self.cogSpeed
        #self.notify.debug('lengthTravelled = %s' % lengthTravelled)
        # don't overshoot our target
        if lengthTravelled > distanceToToon:
            lengthTravelled = distanceToToon
            #self.notify.debug('overshooting lengthTravelled = %s' % lengthTravelled)
        displacement.normalize()
        dirVector = displacement
        dirVector *= lengthTravelled
        newPos = myPos + dirVector
        # always keep them grounded
        newPos.setZ(0)
        self.suit.setPos(newPos)
        self.adjustPlayRate(newPos, myPos, diffTime)        

        if (self.suit.getPos() - returnPos).length() < 0.0001:
            if not self.signalledAtReturnPos and self.barrel >= 0:
                # tell the AI we're at return Pos
                self.game.sendCogAtReturnPos(self.cogIndex, self.barrel)
                self.signalledAtReturnPos = True

        self.lastThinkTime = globalClock.getFrameTime()


    def makeCogCarryBarrel(self, timestamp, inResponseClientStamp,  barrelModel, barrelIndex, cogPos):
        """Handle the AI telling us the barrel is attached to a cog."""
        #assert self.notify.debugStateCall(self)
        if not self.game:
            return
        localTimeStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
        # TODO validate time?
        self.lastLocalTimeStampFromAI = localTimeStamp
        inResponseGameTime = self.convertNetworkStampToGameTime(inResponseClientStamp)

        self.notify.debug('inResponseGameTime =%s timeSentToStart=%s' %
                          (inResponseGameTime, self.netTimeSentToStartByHit))
        if inResponseClientStamp  < self.netTimeSentToStartByHit and \
           self.goal == CTGG.NoGoal:
            self.notify.warning('ignoring makeCogCarrybarrel')            
        else:
            barrelModel.setPos(0,-1.0,1.5)
            barrelModel.reparentTo(self.suit)
            self.suit.setPos(cogPos)
            self.barrel = barrelIndex


    def makeCogDropBarrel(self, timestamp, inResponseClientStamp, barrelModel, barrelIndex, barrelPos):
        """Handle the AI telling us the barrel is attached to a cog."""
        #assert self.notify.debugStateCall(self)
        localTimeStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
        # TODO validate time?
        self.lastLocalTimeStampFromAI = localTimeStamp


        barrelModel.reparentTo(render )
        barrelModel.setPos(barrelPos)

        self.barrel = CTGG.NoBarrelCarried

        #
        #self.suit.setPos(cogPos)

    def respondToPieHit(self, timestamp):
        """The toon hit us, react appropriately."""
        assert self.notify.debugStateCall(self)
        localStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
        # argh using 1.0 sec as fudge
        #if localStamp  > self.lastLocalTimeStampFromAI:
        if self.netTimeSentToStartByHit < timestamp:
            self.clearGoal()
            self.showSplat()
            # move him to his starting postion
            startPos = CTGG.CogStartingPositions[self.cogIndex]
            oldPos = self.suit.getPos()
            self.suit.setPos(startPos)
            if self.netTimeSentToStartByHit < timestamp:
                self.netTimeSentToStartByHit = timestamp
        else:
            self.notify.debug('localStamp = %s, lastLocalTimeStampFromAI=%s, ignoring respondToPieHit' % (localStamp, self.lastLocalTimeStampFromAI))
            self.notify.debug('respondToPieHit self.netTimeSentToStartByHit = %s' % self.netTimeSentToStartByHit)    

    def cleanup(self):
        """Do whatever is necessary to cleanup properly."""
        self.clearGoal()
        self.ignoreAll()
        self.suit.delete()
        if self.kaboomTrack and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.suit = None
        self.game = None
                    

    def adjustPlayRate(self, newPos, oldPos, diffTime):
        """Adjust animation rate based on how far he's moved."""
        # lets slowdown playrate if they're not moving much
        lengthTravelled = (newPos - oldPos).length()
        if diffTime:
            speed = lengthTravelled / diffTime
        else:
            speed = self.cogSpeed
        rateMult = speed / self.cogSpeed
        newRate = rateMult * self.defaultPlayRate
        self.suit.setPlayRate( newRate, 'walk')

    def commonMove(self):
        """Move the cog thief. Common for all 3 behaviors """
        if not self.lastThinkTime:
                self.lastThinkTime = globalClock.getFrameTime()        
        dt = globalClock.getFrameTime() - self.lastThinkTime

        # Step 1:  Update our position.
        # Update our position based on the velocity
        # vector we computed last time around.

        self.oldpos = self.suit.getPos();     # save off our previous position

        pos = self.suit.getPos()
        pos += self.velocity * dt;      # apply velocities.
        self.suit.setPos(pos)

        # Step 2:  SeeFriends.
        # Determine if we can see any of our flockmates.

        self.seeFriends();

        acc = Vec3(0,0,0)

        # well first off we want to move to our target
        self.accumulate(acc, self.getTargetVector())

        # Step 3:  Flocking behavior.
        # Do we see any of our flockmates?  If yes, it's time to implement
        # the first Three Rules (they don't matter if we can't see anybody)
   
        if self.numFlockmatesSeen > 0:
            #if hasattr(base,'doDebug') and base.doDebug:
            #    import pdb; pdb.set_trace()
            keepDistanceVector = self.keepDistance()
            oldAcc = Vec3(acc)
            self.accumulate(acc, keepDistanceVector )
            if self.cogIndex == 0:
                #self.notify.debug('oldAcc=%s, keepDist=%s newAcc=%s' %
                #                  (oldAcc,keepDistanceVector, acc))
                pass
            
            

        # Step 8:  Constrain acceleration
        # If our acceleration change is more than we allow, constrain it

        if (acc.length() > self.maxAcceleration) :
            # definitely too much...constrain to maximum change
            acc.normalize()
            acc *= self.maxAcceleration


        # Step 9:  Implementation.
        # Here's where we apply our newly computed acceleration vector
        # to create a new velocity vector to use next update cycle.

        self.oldVelocity = self.velocity;     # save off our previous velocity

        # now add in the acceleration

        self.velocity += acc;

        # Step 10:  constraint Y velocity changes.
        # Attempt to restrict flight straight up/down by damping out Y axis velocity.
        # This isn't strictly necessary, but does lead to more realistic looking flight.

        # Step 11:  Constrain our speed.
        # If we're moving faster than we're allowed to move, constrain our velocity.
        if self.velocity.length() > self.maxVelocity:
            self.velocity.normalize()
            self.velocity *= self.maxVelocity

        # Step 12:  Compute roll/pitch/yaw.
        # Compute our orientation after all this speed adjustment nonsense.
        # bah no need, we turn on a dime towards our velocity
        forwardVec = Vec3(1,0,0)
        heading = rad2Deg(math.atan2(self.velocity[1], self.velocity[0]))
        heading -= 90
        self.suit.setH( heading)
 

    def getTargetVector(self):
        """Return a vector to my goal."""
        targetPos = Point3(0,0,0)
        if self.goal == CTGG.ToonGoal:
            av = self.game.getAvatar(self.goalId)        
            if av:
                targetPos = av.getPos()
        elif self.goal == CTGG.BarrelGoal:
            barrel = self.game.barrels[self.goalId]
            targetPos = barrel.getPos()
        elif self.goal == CTGG.RunAwayGoal:
            targetPos = CTGG.CogReturnPositions[self.goalId]
        targetPos.setZ(0)
        myPos = self.suit.getPos()
        diff = targetPos - myPos
        if diff.length() > 1.0:
            diff.normalize()
            diff *= 1.0

        return diff

    def accumulate(self, accumulator,  valueToAdd):
        """Return the magnitude of the accumulated vector."""

        accumulator += valueToAdd;
        
        return accumulator.length()


    def seeFriends(self):
        """Determines which flockmates a given flock boid can see."""
        # clear the existing visibility list of any holdover from last round

        self.clearVisibleList();        

        for cogIndex in self.game.cogInfo.keys():
            if cogIndex == self.cogIndex:
                continue

            if self.sameGoal(cogIndex):
                dist = self.canISee(cogIndex)
                if dist != self.Infinity:
                    self.addToVisibleList(cogIndex)
                    if dist < self.distToNearestFlockmate:
                        self.nearestFlockmate = cogIndex
                        self.distToNearestFlockmate = dist

        return self.numFlockmatesSeen

    def clearVisibleList(self):
        """Clears the visibility list and associated fields."""
        self.visibleFriendsList = []
        self.numFlockmatesSeen = 0
        self.nearestFlockmate = None
        self.distToNearestFlockmate = self.Infinity

    def addToVisibleList(self, cogIndex):
        """Add the cog to the visible list."""
        # test:  do we see enough buddies already?
        if self.numFlockmatesSeen < self.MaxFriendsVisible:
            #nope--we can add to this one to the list
            self.visibleFriendsList.append(cogIndex)
            self.numFlockmatesSeen += 1
            if self.cogIndex ==0:
                #self.notify.debug('self.numFlockmatesSeen = %s' % self.numFlockmatesSeen)
                pass
            


    def canISee(self, cogIndex):
        """Return distance if I can see the other cog, infinity otherwise"""

        if self.cogIndex == cogIndex:
            # well we should never see ourself
            return self.Infinity

        cogThief = self.game.getCogThief(cogIndex)
        distance = self.suit.getDistance(cogThief.suit)

        if distance < self.perceptionRange:
            #self.notify.debug('%s can see %s' % (self.cogIndex, cogIndex))
            return distance

        # fell through; can not see it
        return self.Infinity

    def sameGoal(self, cogIndex):
        """Return true if we have the same goal."""
        cogThief = self.game.getCogThief(cogIndex)
        result = (cogThief.goalId == self.goalId) and (cogThief.goal == self.goal)
        return result
        
    def keepDistance(self):
        """Generates a vector for a flock boid to maintain his
        desired separation distance from the nearest flockmate he sees.
        """
        ratio = self.distToNearestFlockmate / self.SeparationDistance;
        nearestThief = self.game.getCogThief(self.nearestFlockmate)
        change = nearestThief.suit.getPos() - self.suit.getPos()

        if ratio < self.MinUrgency:
            ratio = self.MinUrgency
        if ratio > self.MaxUrgency:
            ratio = self.MaxUrgency

            
        # test:  are we too close to our nearest flockmate?
        if self.distToNearestFlockmate < self.SeparationDistance:
            #self.notify.debug('%d is too close to %d' % (self.cogIndex, self.nearestFlockmate))

            # too close...move away from our neighbor
            change.normalize()
            change *= -(1-ratio) # the close we are the more we are pushed away
        elif self.distToNearestFlockmate > self.SeparationDistance:
            # too far away move towards our neighbor
            change.normalize()
            change *= ratio
        else:
            # in the UNLIKELY event we're exactly the right distance away, do nothing
            change = Vec3(0,0,0)

        return change

    def showKaboom(self):
        """Show the kaboom graphic and sound."""
        if self.kaboomTrack and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.kaboom.reparentTo(render)
        self.kaboom.setPos(self.suit.getPos())
        self.kaboom.setZ(3)

        self.kaboomTrack = Parallel(
            SoundInterval(self.kaboomSound, volume=0.5),
            Sequence(
               Func(self.kaboom.showThrough),
               LerpScaleInterval(self.kaboom, duration=0.5, scale =Point3(10,10,10),
                                 startScale = Point3(1,1,1),
                              blendType='easeOut'),
               Func(self.kaboom.hide),
               )
            )
        self.kaboomTrack.start()


    def showSplat(self):
        """Show the splat graphic and sound."""
        if self.kaboomTrack and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.splat.reparentTo(render)
        self.splat.setPos(self.suit.getPos())
        self.splat.setZ(3)

        self.kaboomTrack = Parallel(
            SoundInterval(self.pieHitSound, volume=1.0),
            Sequence(
               Func(self.splat.showThrough),
               LerpScaleInterval(self.splat, duration=0.5, scale =1.75,
                              startScale = Point3(0.1,0.1,0.1), blendType='easeOut'),
               Func(self.splat.hide),
               )
            )
        self.kaboomTrack.start()

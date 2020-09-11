import random
from pandac.PandaModules import VBase3, Point3
from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, Track, \
     LerpPosInterval, ProjectileInterval, SoundInterval, ActorInterval
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import DistributedBattleFinal
from toontown.suit import SuitTimings
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps

# attack properties table
class DistributedBattleDiners(DistributedBattleFinal.DistributedBattleFinal):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleDiners')
                    
    def __init__(self, cr):
        """Create the diners battle."""
        DistributedBattleFinal.DistributedBattleFinal.__init__(self, cr) 
        self.initialReservesJoiningDone = False

        #debug only remove this
        base.dbw = self

    def announceGenerate(self):
        DistributedBattleFinal.DistributedBattleFinal.announceGenerate(self)
        self.moveSuitsToInitialPos()

    def showSuitsJoining(self, suits, ts, name, callback):
        """Show the diners joining the battle, handle initial case too."""
        if len(suits) == 0 and not self.initialReservesJoiningDone:
            # this is a valid case, avoid the assert
            self.initialReservesJoiningDone = True;
            self.doInitialSuitsJoining(ts, name, callback)
            return
        self.showSuitsFalling(suits, ts, name, callback)

    def doInitialSuitsJoining(self, ts, name, callback):
        done = Func(callback)
        if (self.hasLocalToon()):
            # Parent the camera to the battle and position it to watch the
            # suits join.
            camera.reparentTo(self)

            # Choose either a left or a right view at random.
            if random.choice([0, 1]):
                camera.setPosHpr(20, -4, 7, 60, 0, 0)
            else:
                camera.setPosHpr(-20, -4, 7, -60, 0, 0)
        track = Sequence(Wait(0.5), done, name = name)
        track.start(ts)
        self.storeInterval(track, name)

    def moveSuitsToInitialPos(self):
        """Force the inital suits to be in the right spot."""
        battlePts = self.suitPoints[len(self.suitPendingPoints)-1]
        for i in xrange(len(self.suits)):
            suit = self.suits[i]
            suit.reparentTo(self)
            destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            suit.setPos(destPos)
            suit.setHpr(destHpr)
            #self.suits[i].setPos(self.bossCog,battlePts[i][0])
            #self.suits[i].setH(battlePts[i][1])

    def showSuitsFalling(self, suits, ts, name, callback):
        assert(len(suits) > 0)

        if self.bossCog == None:
            # Hmm, no boss cog?  Maybe not generated yet.
            return

        suitTrack = Parallel()

        delay = 0
        for suit in suits:
            """
            This is done by the AI now.
            if self.battleNumber == 2:
                # Battle 2 features skelecogs only.
                suit.makeSkeleton()
                suit.corpMedallion.hide()
                suit.healthBar.show()
                """

            suit.setState('Battle')
            #RAU lawbot boss battle hack, 
            if suit.dna.dept == 'l':
                suit.reparentTo(self.bossCog)
                suit.setPos(0, 0, 0)
            
            #suit.setScale(3.8 / suit.height)

            # Move all suits into position
            if suit in self.joiningSuits:
                i = len(self.pendingSuits) + self.joiningSuits.index(suit)
                destPos, h = self.suitPendingPoints[i]
                destHpr = VBase3(h, 0, 0)
            else:
                destPos, destHpr = self.getActorPosHpr(suit, self.suits)

            startPos = destPos + Point3(0,0,(SuitTimings.fromSky *
                                      ToontownGlobals.SuitWalkSpeed))
            self.notify.debug('startPos for %s = %s' % (suit, startPos))
            suit.reparentTo(self)
            suit.setPos(startPos)            
            suit.headsUp(self)                

            moveIval = Sequence()
            chairInfo = self.bossCog.claimOneChair()
            if chairInfo:
                moveIval = self.createDinerMoveIval(suit,destPos, chairInfo)
                
            suitTrack.append(Track(
                (delay, Sequence(moveIval,
                                 Func(suit.loop, 'neutral')))
                ))
            delay += 1

        if (self.hasLocalToon()):
            # Parent the camera to the battle and position it to watch the
            # suits join.
            camera.reparentTo(self)

            # Choose a back angle to see the diners flying to their battle position
            self.notify.debug('self.battleSide =%s' % self.battleSide)
            camHeading = -20
            camX = -4
            if self.battleSide == 0:
                camHeading = 20
                camX = 4
            camera.setPosHpr(camX, -15, 7, camHeading, 0, 0)


        done = Func(callback)
        track = Sequence(suitTrack, done,
                         name = name)
        track.start(ts)
        self.storeInterval(track, name)

    def createDinerMoveIval(self, suit, destPos, chairInfo):
        """Return an interval of a diner moving to his destPos."""
        # adapted from  suit.beginSupaFlyMovie

        # calculate some times used to manipulate the suit's landing
        # animation
        #
        dur = suit.getDuration('landing')
        fr = suit.getFrameRate('landing')

        landingDur = dur
        
        totalDur = 7.3
        # length of time in animation spent in the air
        animTimeInAir = totalDur - dur
        flyingDur = animTimeInAir
        
        # length of time in animation spent impacting and reacting to
        # the ground
        impactLength = dur - animTimeInAir        
        
        tableIndex = chairInfo[0]
        chairIndex = chairInfo[1]
        table = self.bossCog.tables[tableIndex]
        chairLocator = table.chairLocators[chairIndex]
        chairPos = chairLocator.getPos(self)
        chairHpr = chairLocator.getHpr(self)
        suit.setPos(chairPos)
        table.setDinerStatus(chairIndex, table.HIDDEN)
        suit.setHpr(chairHpr)
        wayPoint = (chairPos + destPos) / 2.0
        wayPoint.setZ(wayPoint.getZ() + 20)

        moveIval = Sequence(
            Func(suit.headsUp, self),
            Func(suit.pose, 'landing', 0),
            ProjectileInterval(suit, duration = flyingDur, startPos = chairPos,
                               endPos = destPos, gravityMult=0.25),
            ActorInterval(suit, 'landing'),
            )
        

        # now create info for the propeller's animation
        #
        if suit.prop == None:
            suit.prop = BattleProps.globalPropPool.getProp('propeller')
        propDur = suit.prop.getDuration('propeller')
        lastSpinFrame = 8
        fr = suit.prop.getFrameRate('propeller')
        # time from beginning of anim at which propeller plays its spin
        spinTime = lastSpinFrame/fr
        # time from beginning of anim at which propeller starts to close
        openTime = (lastSpinFrame + 1) / fr

        # now create the propeller animation intervals that will go in
        # the third and final track
        #
        suit.attachPropeller()
        propTrack = Parallel(
            SoundInterval(suit.propInSound, duration = flyingDur,
                          node = suit),
            Sequence(ActorInterval(suit.prop, 'propeller',
                                   constrainedLoop = 1,
                                   duration = flyingDur+1,
                                   startTime = 0.0,
                                   endTime = spinTime),
                     ActorInterval(suit.prop, 'propeller',
                                   duration = landingDur,
                                   startTime = openTime),
                     Func(suit.detachPropeller),
                     ),
                )

        result = Parallel(moveIval,
                          propTrack,
                          )
        return result
                

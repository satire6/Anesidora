import random
from pandac.PandaModules import VBase3, Point3
from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, Track
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import DistributedBattleFinal
from toontown.suit import SuitTimings
from toontown.toonbase import ToontownGlobals

# attack properties table
class DistributedBattleWaiters(DistributedBattleFinal.DistributedBattleFinal):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleWaiters')
                    
    def __init__(self, cr):
        """Create the waiters battle."""
        DistributedBattleFinal.DistributedBattleFinal.__init__(self, cr) 
        self.initialReservesJoiningDone = False

        #debug only remove this
        base.dbw = self

    def announceGenerate(self):
        DistributedBattleFinal.DistributedBattleFinal.announceGenerate(self)
        for suit in self.suits:
            suit.makeWaiter()
        self.moveSuitsToInitialPos()

    def showSuitsJoining(self, suits, ts, name, callback):
        """Show the waiters joining the battle, handle initial case too."""
        assert self.notify.debugStateCall(self)
        if len(suits) == 0 and not self.initialReservesJoiningDone:
            # this is a valid case, avoid the assert
            self.initialReservesJoiningDone = True;
            self.doInitialSuitsJoining(ts, name, callback)
            return
        self.showSuitsFalling(suits, ts, name, callback)

    def doInitialSuitsJoining(self, ts, name, callback):
        assert self.notify.debugStateCall(self)
        done = Func(callback)
        if (self.hasLocalToon()):
            # Parent the camera to the battle and position it to watch the
            # suits join.
            self.notify.debug('parenting camera to distributed battle waiters')
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
        #import pdb; pdb.set_trace()
        battlePts = self.suitPoints[len(self.suitPendingPoints)-1]
        for i in xrange(len(self.suits)):
            suit = self.suits[i]
            suit.reparentTo(self)
            destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            suit.setPos(destPos)
            suit.setHpr(destHpr)

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
            suit.makeWaiter()
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

            flyIval = suit.beginSupaFlyMove(destPos, True,'flyIn')
            suitTrack.append(Track(
                #(delay, self.createAdjustInterval(suit, destPos, destHpr)),
                (delay, Sequence(flyIval,
                                 Func(suit.loop, 'neutral')))
                ))
            delay += 1

        if (self.hasLocalToon()):
            # Parent the camera to the battle and position it to watch the
            # suits join.
            camera.reparentTo(self)

            # Choose either a left or a right view at random.
            if random.choice([0, 1]):
                camera.setPosHpr(20, -4, 7, 60, 0, 0)
            else:
                camera.setPosHpr(-20, -4, 7, -60, 0, 0)

        done = Func(callback)
        track = Sequence( suitTrack,  done,
                         name = name)
        track.start(ts)
        self.storeInterval(track, name)

    def enterWaitForInput(self, ts=0):
        """Wait for input from the toons."""
        DistributedBattleFinal.DistributedBattleFinal.enterWaitForInput(self,ts)
        if self.hasLocalToon():
            camera.reparentTo(self)

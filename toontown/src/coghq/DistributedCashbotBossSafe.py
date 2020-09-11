from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
import DistributedCashbotBossObject

class DistributedCashbotBossSafe(DistributedCashbotBossObject.DistributedCashbotBossObject):

    """ This is a safe sitting around in the Cashbot CFO final battle
    room.  It's used as a prop for toons to pick up and throw at the
    CFO's head.  Also, the special safe with self.index == 0
    represents the safe that the CFO uses to put on his own head as a
    safety helmet from time to time. """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossSafe')

    grabPos = (0, 0, -8.2)

    # What happens to the crane and its cable when this object is picked up?
    craneFrictionCoef = 0.20
    craneSlideSpeed = 11
    craneRotateSpeed = 16

    # A safe remains under physical control of whichever client
    # last dropped it, even after it stops moving.  This allows
    # goons to push safes out of the way.
    wantsWatchDrift = 0

    def __init__(self, cr):
        DistributedCashbotBossObject.DistributedCashbotBossObject.__init__(self, cr)
        NodePath.__init__(self, 'object')
        self.index = None

        self.flyToMagnetSfx = loader.loadSfx('phase_5/audio/sfx/TL_rake_throw_only.mp3')
        self.hitMagnetSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_safe.mp3')
        # We want these sfx's to overlap just a smidge for effect.
        self.toMagnetSoundInterval = Parallel(
            SoundInterval(self.flyToMagnetSfx, duration = ToontownGlobals.CashbotBossToMagnetTime, node = self),
            Sequence(Wait(ToontownGlobals.CashbotBossToMagnetTime - 0.02),
                     SoundInterval(self.hitMagnetSfx, duration = 1.0, node = self)))
        self.hitFloorSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_bigweight_miss.mp3')
        self.hitFloorSoundInterval = SoundInterval(
            self.hitFloorSfx, node = self)

    def announceGenerate(self):
        DistributedCashbotBossObject.DistributedCashbotBossObject.announceGenerate(self)
        self.name = 'safe-%s' % (self.doId)
        self.setName(self.name)

        self.boss.safe.copyTo(self)
        self.shadow = self.find('**/shadow')

        self.collisionNode.setName('safe')
        cs = CollisionSphere(0, 0, 4, 4)
        self.collisionNode.addSolid(cs)

        if self.index == 0:
            # If this is safe 0, it's the safe that the CFO uses when
            # he wants to put on his own helmet.  This one can't be
            # picked up by magnets, and it doesn't stick around for
            # any length of time when it's knocked off his head--it
            # just falls through the floor and resets.
            
            self.collisionNode.setIntoCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.WallBitmask)
            self.collisionNode.setFromCollideMask(ToontownGlobals.PieBitmask)

        assert(not self.boss.safes.has_key(self.index))
        self.boss.safes[self.index] = self

        self.setupPhysics('safe')
        self.resetToInitialPosition()

    def disable(self):
        assert(self.boss.safes.get(self.index) == self)
        del self.boss.safes[self.index]
        DistributedCashbotBossObject.DistributedCashbotBossObject.disable(self)

    def hideShadows(self):
        self.shadow.hide()

    def showShadows(self):
        self.shadow.show()

    def getMinImpact(self):
        # This method returns the minimum impact, in feet per second,
        # with which the object should hit the boss before we bother
        # to tell the server.
        if self.boss.heldObject:
            return ToontownGlobals.CashbotBossSafeKnockImpact
        else:
            return ToontownGlobals.CashbotBossSafeNewImpact

    def doHitGoon(self, goon):
        # Dropping a safe on a goon always destroys the goon.
        goon.b_destroyGoon()

    def resetToInitialPosition(self):
        posHpr = ToontownGlobals.CashbotBossSafePosHprs[self.index]
        self.setPosHpr(*posHpr)
        self.physicsObject.setVelocity(0, 0, 0)

    def fellOut(self):
        # The safe fell out of the world.  Reset it back to its
        # original position.

        self.deactivatePhysics()
        self.d_requestInitial()


    ##### Messages To/From The Server #####

    def setIndex(self, index):
        self.index = index

    def setObjectState(self, state, avId, craneId):
        if state == 'I':
            self.demand('Initial')
        else:
            DistributedCashbotBossObject.DistributedCashbotBossObject.setObjectState(self, state, avId, craneId)

    def d_requestInitial(self):
        self.sendUpdate('requestInitial')

    ### FSM States ###

    def enterInitial(self):
        self.resetToInitialPosition()
        self.showShadows()

        if self.index == 0:
            # The special "helmet-only" safe goes away completely when
            # it's in Initial mode.
            self.stash()

    def exitInitial(self):
        if self.index == 0:
            self.unstash()

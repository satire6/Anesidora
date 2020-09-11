from pandac.PandaModules import *
from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import NPCToons
from toontown.toonbase import TTLocalizer
from direct.distributed import DistributedObject
from toontown.quest import QuestParser

class DistributedNPCBlocker(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        # Make collision sphere wide enough to block a tunnel
        self.cSphereNodePath.setScale(4.5, 1.0, 6.0)
        self.isLocalToon = 1
        self.movie = None

    def announceGenerate(self):
        #self.nametag.unmanage(base.marginManager)
        DistributedNPCToonBase.announceGenerate(self)
        
    def initToonState(self):
        # We'll make all NPC toons loop their neutral cycle by
        # default.  Normally this is sent from the AI, but because the
        # server sometimes loses updates that immediately follow the
        # generate, we might lose that message.
        self.setAnimState("neutral", 0.9, None, None)
        # Set the Blocker's position and orientation
        posh = NPCToons.BlockerPositions[self.name]
        self.setPos(posh[0])
        self.setH(posh[1])

    def disable(self):
        if hasattr(self, 'movie') and self.movie:
            self.movie.cleanup()
            del self.movie
            if (self.isLocalToon == 1):
                base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        # Lock down the avatar for purchase mode
        base.cr.playGame.getPlace().fsm.request('quest', [self])
        # Tell the server
        self.sendUpdate("avatarEnter", [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')

    def resetBlocker(self):
        assert self.notify.debug('resetBlocker')
        # Make blocker non-collideable
        self.cSphereNode.setCollideMask(BitMask32())
        if hasattr(self, 'movie') and self.movie:
            self.movie.cleanup()
            self.movie = None
        self.startLookAround()
        # Reset the NPC back to original pos hpr in case he had to
        # turn all the way around to talk to the toon
        # TODO: make this a lerp
        self.clearMat()
        # If we are the local toon and we have simply taken too long
        # to read through the chat balloons, just free us
        if (self.isLocalToon == 1):
            base.localAvatar.posCamera(0, 0)
            self.freeAvatar()
            self.isLocalToon = 0

    def setMovie(self, mode, npcId, avId, timestamp):
        """
        This is a message from the AI describing a movie between this NPC
        and a Toon that has approached us. 
        """
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)

        self.npcId = npcId

        # See if this is the local toon
        self.isLocalToon = (avId == base.localAvatar.doId)

        if (mode == NPCToons.BLOCKER_MOVIE_CLEAR):
            assert self.notify.debug('BLOCKER_MOVIE_CLEAR')
            return

        elif (mode == NPCToons.BLOCKER_MOVIE_START):
            assert self.notify.debug('BLOCKER_MOVIE_PLAY')
            self.movie = QuestParser.NPCMoviePlayer("tutorial_blocker", 
                                                base.localAvatar, self)
            self.movie.play()

        elif (mode == NPCToons.BLOCKER_MOVIE_TIMEOUT):
            assert self.notify.debug('BLOCKER_MOVIE_TIMEOUT')
            return

        return

    def finishMovie(self, av, isLocalToon, elapsedTime):
        """
        Final cleanup for a movie that has finished
        """
        self.resetBlocker()

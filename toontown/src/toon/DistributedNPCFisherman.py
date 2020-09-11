from pandac.PandaModules import *
from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.fishing import FishSellGUI
from direct.task.Task import Task

class DistributedNPCFisherman(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.fishGui = None
            
    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupFishGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.fishGui:
            self.fishGui.destroy()
            self.fishGui = None
        self.av = None
        if (self.isLocalToon):
            base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedNPCToonBase.generate(self)
        self.fishGuiDoneEvent = "fishGuiDone"
        
    def announceGenerate(self):
        DistributedNPCToonBase.announceGenerate(self)
        
    def initToonState(self):
        # announceGenerate in DistributedNPCToonBase tries to
        # parent the toon to a node called npc_origin_N.  For now
        # this node doesn't exist for the fisherman, so we will have
        # to create our own node, and then call the base class function
        self.setAnimState("neutral", 1.05, None, None)
        # Make sure you look under stashed nodes as well, since street
        # visibility might have stashed the zone this origin is under
        npcOrigin = self.cr.playGame.hood.loader.geom.find("**/npc_fisherman_origin_%s;+s" % self.posIndex)
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning("announceGenerate: Could not find npc_fisherman_origin_" + str(self.posIndex))

    def getCollSphereRadius(self):
        """
        Override DistributedNPCToonBase here to spec a smaller radius
        """
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        # Lock down the avatar for purchase mode
        base.cr.playGame.getPlace().fsm.request('purchase')
        # Tell the server
        self.sendUpdate("avatarEnter", [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def setupAvatars(self, av):
        """
        Prepare avatars for the quest movie
        """
        # Ignore avatars now to prevent unnecessary requestInteractions when we know
        # this npc is busy right now. If another toon did manage to request interaction
        # before we starting ignoring, he will get a freeAvatar message from the server
        self.ignoreAvatars()
        # Make us face each other
        # Actually this looks funny for the fishermen
        # av.headsUp(self, 0, 0, 0)
        # self.headsUp(av, 0, 0, 0)
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def resetFisherman(self):
        assert self.notify.debug('resetFisherman')
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupFishGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.fishGui:
            self.fishGui.destroy()
            self.fishGui = None
            
        self.show()
        self.startLookAround()
        self.detectAvatars()
        # Reset the NPC back to original pos hpr in case he had to
        # turn all the way around to talk to the toon
        # TODO: make this a lerp
        self.clearMat()
        # If we are the local toon and we have simply taken too long
        # to read through the chat balloons, just free us
        if (self.isLocalToon):
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        """
        This is a message from the AI describing a movie between this NPC
        and a Toon that has approached us. 
        """
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp

        self.npcId = npcId

        # See if this is the local toon
        self.isLocalToon = (avId == base.localAvatar.doId)
            
        assert(self.notify.debug("setMovie: %s %s %s %s" %
                          (mode, avId, timeStamp, self.isLocalToon)))

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == NPCToons.SELL_MOVIE_CLEAR):
            assert self.notify.debug('SELL_MOVIE_CLEAR')
            return

        if (mode == NPCToons.SELL_MOVIE_TIMEOUT):
            assert self.notify.debug('SELL_MOVIE_TIMEOUT')
            # In case the GUI hasn't popped up yet
            taskMgr.remove(self.uniqueName('lerpCamera'))
            # Stop listening for the GUI
            if (self.isLocalToon):
                self.ignore(self.fishGuiDoneEvent)
                # hide the popupInfo
                if self.popupInfo:
                    self.popupInfo.reparentTo(hidden)
                if self.fishGui:
                    self.fishGui.destroy()
                    self.fishGui = None

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                 CFSpeech | CFTimeout)
            self.resetFisherman()

        elif (mode == NPCToons.SELL_MOVIE_START):
            assert self.notify.debug('SELL_MOVIE_START')
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning("Avatar %d not found in doId" % (avId))
                return
            else:
                self.accept(self.av.uniqueName('disable'),
                            self.__handleUnexpectedExit)

            self.setupAvatars(self.av)

            if (self.isLocalToon):
                camera.wrtReparentTo(render)
                camera.lerpPosHpr(-5, 9, base.localAvatar.getHeight()-0.5,
                                  -150, -2, 0,
                                  1,
                                  other=self,
                                  blendType="easeOut",
                                  task=self.uniqueName('lerpCamera'))

            if (self.isLocalToon):
                taskMgr.doMethodLater(1.0, self.popupFishGUI,
                                      self.uniqueName('popupFishGUI'))
            
        elif (mode == NPCToons.SELL_MOVIE_COMPLETE):
            assert self.notify.debug('SELL_MOVIE_COMPLETE')
            # this is necessary to not show marketing message on test
            chatStr = TTLocalizer.STOREOWNER_THANKSFISH
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetFisherman()

        elif (mode == NPCToons.SELL_MOVIE_TROPHY):
            assert self.notify.debug('SELL_MOVIE_TROPHY')

            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning("Avatar %d not found in doId" % (avId))
                return
            else:
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.STOREOWNER_TROPHY % (numFish, totalNumFish),
                                     CFSpeech | CFTimeout)
            self.resetFisherman()

        elif (mode == NPCToons.SELL_MOVIE_NOFISH):
            assert self.notify.debug('SELL_MOVIE_NOFISH')
            chatStr = TTLocalizer.STOREOWNER_NOFISH
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetFisherman()

        elif (mode == NPCToons.SELL_MOVIE_NO_MONEY):
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            self.resetFisherman()

        return

    def __handleSaleDone(self, sell):
        self.ignore(self.fishGuiDoneEvent)
        # Ask the AI to complete the sale
        self.sendUpdate("completeSale", [sell])
        self.fishGui.destroy()
        self.fishGui = None
        
    def popupFishGUI(self, task):
        assert self.notify.debug('popupFishGUI()')
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.fishGuiDoneEvent, self.__handleSaleDone)
        self.fishGui = FishSellGUI.FishSellGUI(self.fishGuiDoneEvent)
        
        

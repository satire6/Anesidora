from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.minigame import ClerkPurchase 
from toontown.shtiker.PurchaseManagerConstants import *
import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel

class DistributedNPCClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchase = None
        self.isLocalToon = 0
        self.av = None
        self.purchaseDoneEvent = 'purchaseDone'
            
    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None
        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def allowedToEnter(self):
        """Check if the local toon is allowed to enter."""
        if base.cr.isPaid():
            return True
        place = base.cr.playGame.getPlace()
        myHoodId = ZoneUtil.getCanonicalHoodId(place.zoneId)
        if  myHoodId in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ):
            # trialer going to TTC/Estate/Goofy Speedway, let them through
            return True
        return False

    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')
            
    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        if self.allowedToEnter():
            # Lock down the avatar for purchase mode
            base.cr.playGame.getPlace().fsm.request('purchase')
            # Tell the server
            self.sendUpdate("avatarEnter", [])
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='otherGags',
                                                  doneFunc=self.handleOkTeaser)

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetClerk(self):
        assert self.notify.debug('resetClerk')
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None
        # Reset the NPC back to original pos hpr in case he had to
        # turn all the way around to talk to the toon
        # TODO: make this a lerp
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()
        # If we are the local toon and we have simply taken too long
        # to read through the chat balloons, just free us
        if (self.isLocalToon):
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, timestamp):
        """
        This is a message from the AI describing a movie between this NPC
        and a Toon that has approached us. 
        """
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp

        # See if this is the local toon
        self.isLocalToon = (avId == base.localAvatar.doId)
            
        assert(self.notify.debug("setMovie: %s %s %s %s" %
                          (mode, avId, timeStamp, self.isLocalToon)))

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == NPCToons.PURCHASE_MOVIE_CLEAR):
            assert self.notify.debug('PURCHASE_MOVIE_CLEAR')
            return

        if (mode == NPCToons.PURCHASE_MOVIE_TIMEOUT):
            assert self.notify.debug('PURCHASE_MOVIE_TIMEOUT')
            # In case the GUI hasn't popped up yet
            taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
            taskMgr.remove(self.uniqueName('lerpCamera'))
            # Stop listening for the GUI
            if (self.isLocalToon):
                self.ignore(self.purchaseDoneEvent)
            # See if a button was pressed first
            if self.purchase:
                self.__handlePurchaseDone()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                                CFSpeech | CFTimeout)
            self.resetClerk()

        elif (mode == NPCToons.PURCHASE_MOVIE_START):
            assert self.notify.debug('PURCHASE_MOVIE_START')
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
                camera.lerpPosHpr(-5, 9, self.getHeight()-0.5, -150, -2, 0, 1,
                                  other=self,
                                  blendType="easeOut",
                                  task=self.uniqueName('lerpCamera'))

            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING,
                                                CFSpeech | CFTimeout)
            if (self.isLocalToon):
                taskMgr.doMethodLater(1.0, self.popupPurchaseGUI,
                                       self.uniqueName('popupPurchaseGUI'))
            
        elif (mode == NPCToons.PURCHASE_MOVIE_COMPLETE):
            assert self.notify.debug('PURCHASE_MOVIE_COMPLETE')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                                CFSpeech | CFTimeout)
            self.resetClerk()

        elif (mode == NPCToons.PURCHASE_MOVIE_NO_MONEY):
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NEEDJELLYBEANS,
                                                CFSpeech | CFTimeout)
            self.resetClerk()

        return

    def popupPurchaseGUI(self, task):
        assert self.notify.debug('popupPurchaseGUI()')
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.purchaseDoneEvent, self.__handlePurchaseDone)
        self.accept('boughtGag', self.__handleBoughtGag)
        self.purchase = ClerkPurchase.ClerkPurchase(base.localAvatar,
                                self.remain, self.purchaseDoneEvent)
        self.purchase.load()
        self.purchase.enter()
        return Task.done

    def __handleBoughtGag(self):
        # Send each gag purchase to the AI as we go.
        self.d_setInventory(base.localAvatar.inventory.makeNetString(),
                            base.localAvatar.getMoney(), 0)

    def __handlePurchaseDone(self):
        """
        This is the callback from the Purchase object
        Cleanup the gui and send the message to the AI
        """
        assert self.notify.debug('handlePurchaseDone()')
        #print "handlepurchasedone"
        self.ignore('boughtGag')
        self.d_setInventory(base.localAvatar.inventory.makeNetString(),
                            base.localAvatar.getMoney(), 1)
        #print "handlepurchasedone, set inventory"
        self.purchase.exit()
        self.purchase.unload()
        self.purchase = None


    def d_setInventory(self, invString, money, done):
        # Report our inventory to the server
        self.sendUpdate('setInventory', [invString, money, done])

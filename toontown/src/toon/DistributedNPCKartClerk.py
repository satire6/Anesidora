##########################################################################
# Module: DistributedNPCKartClerk.py
#   (Based on Distributed NPCPetclerk.py)
# Date: 4/24/05
# Author: shaskell
##########################################################################

#from pandac.PandaModules import *
from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.racing.KartShopGui import *
from toontown.racing.KartShopGlobals import * 

class DistributedNPCKartClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.kartShopGui = None
            
    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupKartShopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        #TODO: what is this?
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.kartShopGui:
            self.kartShopGui.destroy()
            self.kartShopGui = None
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

        
    def getCollSphereRadius(self):
        """
        Override DistributedNPCToonBase here to spec a smaller radius
        """
        return 2.25

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

    def resetKartShopClerk(self):
        assert self.notify.debug('resetKartShopClerk')
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupKartShopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.kartShopGui:
            self.kartShopGui.destroy()
            self.kartShopGui = None
            
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

    def ignoreEventDict(self):
        for event in KartShopGlobals.EVENTDICT:
            self.ignore(event)
            
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
                self.ignoreEventDict()
                # hide the popupInfo
                if self.popupInfo:
                    self.popupInfo.reparentTo(hidden)
                if self.kartShopGui:
                    self.kartShopGui.destroy()
                    self.kartShopGui = None

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                 CFSpeech | CFTimeout)
            self.resetKartShopClerk()

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
                taskMgr.doMethodLater(1.0, self.popupKartShopGUI,
                                      self.uniqueName('popupKartShopGUI'))

        #Player made at least one successful purchase    
        elif (mode == NPCToons.SELL_MOVIE_COMPLETE):
            assert self.notify.debug('SELL_MOVIE_COMPLETE')
            #TODO: change this appropriately
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                 CFSpeech | CFTimeout)
            self.resetKartShopClerk()

        #Player canceled with no purchas
        elif (mode == NPCToons.SELL_MOVIE_PETCANCELED):
            assert self.notify.debug('SELL_MOVIE_PETCANCELED')
            #TODO: change this appropriately
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                 CFSpeech | CFTimeout)
            self.resetKartShopClerk()


        elif (mode == NPCToons.SELL_MOVIE_NO_MONEY):
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            #TODO: change this appropriately
            self.resetKartShopClerk()

        return

 #        self.sendUpdate("petAdopted", [whichPet, nameIndex])

    def __handleBuyKart(self, kartID): 
              #base.localAvatar.requestKartDNAFieldUpdate( KartDNA.bodyType, kartID )
               #base.localAvatar.requestKartDNAFieldUpdate( KartDNA.bodyColor, getDefaultColor() )
        self.sendUpdate("buyKart", [kartID])
                    
    def __handleBuyAccessory(self, accID):
        #base.localAvatar.requestAddOwnedAccessory(accID )
        self.sendUpdate("buyAccessory", [accID])
        
    def __handleGuiDone(self, bTimedOut=False):
        self.ignoreAll()
        if hasattr(self, 'kartShopGui') and self.kartShopGui != None:
                self.kartShopGui.destroy()
                self.kartShopGui = None
        #TODO: Need this?
        if not bTimedOut:
            self.sendUpdate("transactionDone")
        
    def popupKartShopGUI(self, task):
        assert self.notify.debug('popupKartShopGUI()')
        self.setChatAbsolute('', CFSpeech)
        
        self.accept( KartShopGlobals.EVENTDICT["buyAccessory"], self.__handleBuyAccessory )
        self.accept( KartShopGlobals.EVENTDICT["buyKart"], self.__handleBuyKart )
        self.acceptOnce(  KartShopGlobals.EVENTDICT[ 'guiDone' ], self.__handleGuiDone )
                                
        self.kartShopGui = KartShopGuiMgr(KartShopGlobals.EVENTDICT)


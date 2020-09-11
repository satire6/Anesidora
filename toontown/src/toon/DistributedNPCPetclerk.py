from pandac.PandaModules import *
from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.pets import PetshopGUI
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel

class DistributedNPCPetclerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.petshopGui = None
        self.petSeeds = None
        self.waitingForPetSeeds = False
            
    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPetshopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.petshopGui:
            self.petshopGui.destroy()
            self.petshopGui = None
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
        self.eventDict = {}
        self.eventDict['guiDone']  = "guiDone"
        self.eventDict['petAdopted']  = "petAdopted"
        self.eventDict['petReturned']  = "petReturned"
        self.eventDict['fishSold']  = "fishSold"
        
    def getCollSphereRadius(self):
        """
        Override DistributedNPCToonBase here to spec a smaller radius
        """
        return 4.0

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
            self.dialog = TeaserPanel.TeaserPanel(pageName='tricks',
                                                  doneFunc=self.handleOkTeaser)            

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetPetshopClerk(self):
        assert self.notify.debug('resetPetshopClerk')
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPetshopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.petshopGui:
            self.petshopGui.destroy()
            self.petshopGui = None
            
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

        self.petSeeds = None
        self.waitingForPetSeeds = False
        
        return Task.done

    def ignoreEventDict(self):
        for event in self.eventDict.values():
            self.ignore(event)
            
    def setPetSeeds(self, petSeeds):
        self.petSeeds = petSeeds
        if self.waitingForPetSeeds:
            self.waitingForPetSeeds = False
            self.popupPetshopGUI(None)  #re-call this now that we have the petseeds
    
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
                if self.petshopGui:
                    self.petshopGui.destroy()
                    self.petshopGui = None

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                 CFSpeech | CFTimeout)
            self.resetPetshopClerk()

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
                taskMgr.doMethodLater(1.0, self.popupPetshopGUI,
                                      self.uniqueName('popupPetshopGUI'))
            
        elif (mode == NPCToons.SELL_MOVIE_COMPLETE):
            assert self.notify.debug('SELL_MOVIE_COMPLETE')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_THANKSFISH_PETSHOP,
                                 CFSpeech | CFTimeout)
            self.resetPetshopClerk()

        elif (mode == NPCToons.SELL_MOVIE_PETRETURNED):
            assert self.notify.debug('SELL_MOVIE_PETRETURNED')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_PETRETURNED,
                                 CFSpeech | CFTimeout)
            self.resetPetshopClerk()

        elif (mode == NPCToons.SELL_MOVIE_PETADOPTED):
            assert self.notify.debug('SELL_MOVIE_PETADOPTED')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_PETADOPTED,
                                 CFSpeech | CFTimeout)
            self.resetPetshopClerk()

        elif (mode == NPCToons.SELL_MOVIE_PETCANCELED):
            assert self.notify.debug('SELL_MOVIE_PETCANCELED')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_PETCANCELED,
                                 CFSpeech | CFTimeout)
            self.resetPetshopClerk()

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
            self.resetPetshopClerk()

        elif (mode == NPCToons.SELL_MOVIE_NOFISH):
            assert self.notify.debug('SELL_MOVIE_NOFISH')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NOFISH,
                                 CFSpeech | CFTimeout)
            self.resetPetshopClerk()

        elif (mode == NPCToons.SELL_MOVIE_NO_MONEY):
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            self.resetPetshopClerk()

        return

    def __handlePetAdopted(self, whichPet, nameIndex):
        #the pet adopted message automatically handles returning the
        #current pet, so we need to do this here too
        base.cr.removePetFromFriendsMap()
        
        self.ignore(self.eventDict['petAdopted'])
        self.sendUpdate("petAdopted", [whichPet, nameIndex])

    def __handlePetReturned(self):
        base.cr.removePetFromFriendsMap()
        self.ignore(self.eventDict['petReturned'])
        self.sendUpdate("petReturned")

    def __handleFishSold(self):
        self.ignore(self.eventDict['fishSold'])
        # Ask the AI to complete the sale
        self.sendUpdate("fishSold")

    def __handleGUIDone(self, bTimedOut=False):
        self.ignore(self.eventDict['guiDone'])
        self.petshopGui.destroy()
        self.petshopGui = None
        if not bTimedOut:
            self.sendUpdate("transactionDone")
        
    def popupPetshopGUI(self, task):
        if not self.petSeeds:
            self.waitingForPetSeeds = True
            return
            
        #print "popupPetshopGui"
        assert self.notify.debug('popupPetshopGUI()')
        self.setChatAbsolute('', CFSpeech)
        
        self.acceptOnce(self.eventDict['guiDone'], self.__handleGUIDone)
        self.acceptOnce(self.eventDict['petAdopted'], self.__handlePetAdopted)
        self.acceptOnce(self.eventDict['petReturned'], self.__handlePetReturned)
        self.acceptOnce(self.eventDict['fishSold'], self.__handleFishSold)
        
        self.petshopGui = PetshopGUI.PetshopGUI(self.eventDict, self.petSeeds)
        
        

#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: Client side of a party person, an NPC who stands near the party hat
#          and can send you to the party grounds to plan your party
#-------------------------------------------------------------------------------

from DistributedNPCToonBase import DistributedNPCToonBase
from direct.distributed.DistributedObject import DistributedObject
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from direct.task.Task import Task
from direct.distributed import ClockDelta
from pandac.PandaModules import CFSpeech, CFTimeout, Point3
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.parties import PartyGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TeaserPanel

class DistributedNPCPartyPerson(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isInteractingWithLocalToon = 0
        self.av = None
        self.button = None
        self.askGui = None
        self.teaserDialog = None

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupAskGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        self.av = None
        if (self.isInteractingWithLocalToon):
            base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def delete(self):
        if self.askGui:
            self.ignore(self.planPartyQuestionGuiDoneEvent)
            self.askGui.cleanup()
            del self.askGui

        DistributedNPCToonBase.delete(self)
        
    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedNPCToonBase.generate(self)
        
    def announceGenerate(self):
        DistributedNPCToonBase.announceGenerate(self)
        
        # Make sure you look under stashed nodes as well, since street
        # visibility might have stashed the zone this origin is under
        
        self.planPartyQuestionGuiDoneEvent = "planPartyQuestionDone"

        self.askGui = TTDialog.TTGlobalDialog(
            dialogName = self.uniqueName("askGui"),
            doneEvent = self.planPartyQuestionGuiDoneEvent,
            message = TTLocalizer.PartyDoYouWantToPlan,
            style = TTDialog.YesNo,
            okButtonText = OTPLocalizer.DialogYes,
            cancelButtonText = OTPLocalizer.DialogNo,
        )
        self.askGui.hide()        
        
    def initToonState(self):
        # announceGenerate in DistributedNPCToonBase tries to
        # parent the toon to a node called npc_origin_N.  For now
        # this node doesn't exist for the party person, so we will have
        # to create our own node, and then call the base class function
        self.setAnimState("neutral", 1.05, None, None)
        if self.posIndex%2==0:
            side = "left"
        else:
            side = "right"
        npcOrigin = self.cr.playGame.hood.loader.geom.find("**/party_person_%s;+s" % side)
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning("announceGenerate: Could not find party_person_%s" % side )

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
        # This is used to keep the avatar in one place apparently
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

    def resetPartyPerson(self):
        assert self.notify.debug('resetPartyPerson')
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupAskGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.askGui:
            self.askGui.hide()

        self.show()
        self.startLookAround()
        self.detectAvatars()
        # Reset the NPC back to original pos hpr in case he had to
        # turn all the way around to talk to the toon
        # TODO: make this a lerp
        self.clearMat()
        # If we are the local toon and we have simply taken too long
        # to read through the chat balloons, just free us
        if self.isInteractingWithLocalToon:
            if hasattr(self, "teaserDialog") and not self.teaserDialog:
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
        self.isInteractingWithLocalToon = (avId == base.localAvatar.doId)
            
        assert(self.notify.debug("setMovie: %s %s %s %s" %
                          (mode, avId, timeStamp, self.isInteractingWithLocalToon)))

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if mode == NPCToons.PARTY_MOVIE_CLEAR:
            assert self.notify.debug('PARTY_MOVIE_CLEAR')
            return

        # It's been a long time since we heard anything
        if mode == NPCToons.PARTY_MOVIE_TIMEOUT:
            assert self.notify.debug('PARTY_MOVIE_TIMEOUT')
            # In case the GUI hasn't popped up yet
            taskMgr.remove(self.uniqueName('lerpCamera'))
            # Stop listening for the GUI
            if self.isInteractingWithLocalToon:
                self.ignore(self.planPartyQuestionGuiDoneEvent)
                if self.askGui:
                    self.askGui.hide()
                    self.ignore(self.planPartyQuestionGuiDoneEvent)

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                 CFSpeech | CFTimeout)
            self.resetPartyPerson()

        # Ask the toon if they want to plan a party (assuming it's the local toon)
        elif mode == NPCToons.PARTY_MOVIE_START:
            assert self.notify.debug('PARTY_MOVIE_START')
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning("Avatar %d not found in doId" % (avId))
                return
            else:
                self.accept(self.av.uniqueName('disable'),
                            self.__handleUnexpectedExit)

            self.setupAvatars(self.av)

            if self.isInteractingWithLocalToon:
                camera.wrtReparentTo(render)
                camera.lerpPosHpr(-5, 9, base.localAvatar.getHeight()-0.5,
                                  -150, -2, 0,
                                  1,
                                  other=self,
                                  blendType="easeOut",
                                  task=self.uniqueName('lerpCamera'))
                taskMgr.doMethodLater(1.0, self.popupAskGUI,
                                      self.uniqueName('popupAskGUI'))
            else:
                self.setChatAbsolute(TTLocalizer.PartyDoYouWantToPlan, CFSpeech | CFTimeout)
        # They want to plan a party!
        elif mode == NPCToons.PARTY_MOVIE_COMPLETE:
            assert self.notify.debug('PARTY_MOVIE_COMPLETE')
            # this is necessary to not show marketing message on test
            chatStr = TTLocalizer.PartyPlannerOnYourWay
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
            
            if self.isInteractingWithLocalToon:
                base.localAvatar.aboutToPlanParty = True
                base.cr.partyManager.setPartyPlannerStyle(self.style)
                base.cr.partyManager.setPartyPlannerName(self.name)
                base.localAvatar.creatingNewPartyWithMagicWord = False
                loaderId = "safeZoneLoader"
                whereId = "party"
                hoodId, zoneId = extraArgs
                avId = -1
                place = base.cr.playGame.getPlace()
                requestStatus = {"loader": loaderId,
                                            "where": whereId,
                                            "how": "teleportIn",
                                            "hoodId": hoodId, 
                                            "zoneId": zoneId, 
                                            "shardId": None,
                                            "avId": avId}
                # we need to do a requestLeave to make sure phase 13 is downloaded
                place.requestLeave(requestStatus)

        # They decided not to plan a party this time
        elif mode == NPCToons.PARTY_MOVIE_MAYBENEXTTIME:
            assert self.notify.debug('PARTY_MOVIE_MAYBENEXTTIME')

            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning("Avatar %d not found in doId" % (avId))
                return
            else:
                self.setChatAbsolute(TTLocalizer.PartyPlannerMaybeNextTime, CFSpeech | CFTimeout)
            self.resetPartyPerson()

        # They're already hosting too many parties
        elif mode == NPCToons.PARTY_MOVIE_ALREADYHOSTING:
            assert self.notify.debug('PARTY_MOVIE_ALREADYHOSTING')
            chatStr = TTLocalizer.PartyPlannerHostingTooMany
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
            
        elif mode == NPCToons.PARTY_MOVIE_ONLYPAID:
            assert self.notify.debug('PARTY_MOVIE_ONLYPAID')
            chatStr = TTLocalizer.PartyPlannerOnlyPaid
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()

        elif mode == NPCToons.PARTY_MOVIE_COMINGSOON:
            assert self.notify.debug('PARTY_MOVIE_COMINGSOON')
            chatStr = TTLocalizer.PartyPlannerNpcComingSoon
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
        elif mode == NPCToons.PARTY_MOVIE_MINCOST:
            assert self.notify.debug('PARTY_MOVIE_MINCOST')
            chatStr = TTLocalizer.PartyPlannerNpcMinCost % PartyGlobals.MinimumPartyCost
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()               

        return

    def __handleAskDone(self):
        self.ignore(self.planPartyQuestionGuiDoneEvent)
        doneStatus = self.askGui.doneStatus
        if doneStatus == "ok":
            wantsToPlan = 1
            if (localAvatar.getGameAccess() != ToontownGlobals.AccessFull):
                wantsToPlan = 0
                place = base.cr.playGame.getPlace()
                if place:
                    place.fsm.request('stopped', force = 1)
                self.teaserDialog = TeaserPanel.TeaserPanel(pageName='parties', doneFunc = self.handleOkTeaser)
        else:
            wantsToPlan = 0
        self.sendUpdate("answer", [wantsToPlan])
        self.askGui.hide()
        
    def popupAskGUI(self, task):
        assert self.notify.debug('popupAskGUI()')
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.planPartyQuestionGuiDoneEvent, self.__handleAskDone)        
        self.askGui.show()
        
    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.teaserDialog.destroy()
        del self.teaserDialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

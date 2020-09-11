from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.quest import QuestParser
from toontown.quest import QuestChoiceGui
from toontown.quest import TrackChoiceGui
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel

ChoiceTimeout = 20

class DistributedNPCSpecialQuestGiver(DistributedNPCToonBase):

    def __init__(self, cr):
        assert self.notify.debug("__init__")
        DistributedNPCToonBase.__init__(self, cr)
        self.curQuestMovie = None
        self.questChoiceGui = None
        self.trackChoiceGui = None
        
    def announceGenerate(self):
        self.setAnimState("neutral", 0.9, None, None)
        
        npcOrigin = self.cr.playGame.hood.loader.geom.find("**/npc_origin_" + `self.posIndex`)
        
         # Now he's no longer parented to render, but no one minds.
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning("announceGenerate: Could not find npc_origin_" + str(self.posIndex))

        DistributedNPCToonBase.announceGenerate(self)
            
    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        # if there are situations where a quest movie should be able to stick around
        # after the NPC is deleted, this will need to change
        if self.curQuestMovie:
            curQuestMovie = self.curQuestMovie
            # do this here in case we get deleted in the call to movie.cleanup()
            self.curQuestMovie = None
            curQuestMovie.timeout(fFinish = 1)
            curQuestMovie.cleanup()

    def disable(self):
        self.cleanupMovie()
        DistributedNPCToonBase.disable(self)

    def cleanupMovie(self):        
        self.clearChat()
        # Kill any quest choice guis that may be active
        self.ignore("chooseQuest")
        if self.questChoiceGui:
            self.questChoiceGui.destroy()
            self.questChoiceGui = None
        # Kill any movies that may be playing 
        self.ignore(self.uniqueName("doneChatPage"))
        if self.curQuestMovie:
            self.curQuestMovie.timeout(fFinish = 1)
            self.curQuestMovie.cleanup()
            self.curQuestMovie = None
        # Kill any track choice guis that may be active
        if self.trackChoiceGui:
            self.trackChoiceGui.destroy()
            self.trackChoiceGui = None
            
    def allowedToTalk(self):
        """Check if the local toon is allowed to talk to this NPC."""
        if base.cr.isPaid():
            return True
        place = base.cr.playGame.getPlace()
        myHoodId = ZoneUtil.getCanonicalHoodId(place.zoneId)
        # if we're in the estate we should use place.id
        if hasattr(place, 'id'):
            myHoodId = place.id
        if  myHoodId in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ToontownGlobals.Tutorial
            ):
            return True
        return False
            
    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        if self.allowedToTalk():
            # Lock down the avatar for quest mode
            base.cr.playGame.getPlace().fsm.request('quest', [self])
            # Tell the server
            self.sendUpdate("avatarEnter", [])
            # make sure this NPCs chat balloon is visible above all others for th elocekd down avatar
            self.nametag3d.setDepthTest(0)
            self.nametag3d.setBin('fixed', 0)
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='quests',
                                                  doneFunc=self.handleOkTeaser)        

    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def finishMovie(self, av, isLocalToon, elapsedTime):
        """
        Final cleanup for a movie that has finished
        """
        self.cleanupMovie()
        av.startLookAround()
        self.startLookAround()
        self.detectAvatars()
        # Reset the NPC back to original pos hpr in case he had to
        # turn all the way around to talk to the toon
        # TODO: make this a lerp
        self.clearMat()
        if isLocalToon:
            taskMgr.remove(self.uniqueName("lerpCamera"))
            # Go back into walk mode
            base.localAvatar.posCamera(0,0)
            base.cr.playGame.getPlace().setState("walk")
            # Tell the AI we are done now
            self.sendUpdate("setMovieDone", [])
            # set the name tag back to normal rendering
            self.nametag3d.clearDepthTest()
            self.nametag3d.clearBin()

    def setupCamera(self, mode):
        camera.wrtReparentTo(render)
        if ((mode == NPCToons.QUEST_MOVIE_QUEST_CHOICE) or
            (mode == NPCToons.QUEST_MOVIE_TRACK_CHOICE)):
            camera.lerpPosHpr(5, 9, self.getHeight()-0.5, 155, -2, 0, 1,
                              other=self,
                              blendType="easeOut",
                              task=self.uniqueName("lerpCamera"))
        else:
            camera.lerpPosHpr(-5, 9, self.getHeight()-0.5, -150, -2, 0, 1,
                              other=self,
                              blendType="easeOut",
                              task=self.uniqueName("lerpCamera"))
        

    def setMovie(self, mode, npcId, avId, quests, timestamp):
        """
        This is a message from the AI describing a movie between this NPC
        and a Toon that has approached us. 
        """
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)

        # See if this is the local toon
        isLocalToon = (avId == base.localAvatar.doId)
            
        assert(self.notify.debug("setMovie: %s %s %s %s %s %s" %
                                 (mode, npcId, avId, quests, timeStamp, isLocalToon)))

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == NPCToons.QUEST_MOVIE_CLEAR):
            assert self.notify.debug("setMovie: movie cleared")
            self.cleanupMovie()
            return

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == NPCToons.QUEST_MOVIE_TIMEOUT):
            assert self.notify.debug("setMovie: movie timeout")
            self.cleanupMovie()
            # If we are the local toon and we have simply taken too long
            # to read through the chat balloons, just free us
            if isLocalToon:
                self.freeAvatar()
            # Act like we finished the chat pages by setting the page number to -1
            self.setPageNumber(0,-1)
            self.clearChat()
            self.startLookAround()
            self.detectAvatars()
            return
                
        av = base.cr.doId2do.get(avId)
        if av is None:
            self.notify.warning("Avatar %d not found in doId" % (avId))
            return

        # Reject is simpler, so lets get that out of the way
        if (mode == NPCToons.QUEST_MOVIE_REJECT):
            rejectString = Quests.chooseQuestDialogReject()
            rejectString = Quests.fillInQuestNames(rejectString, avName = av.name)
            # No need for page chat here, just setChatAbsolute
            self.setChatAbsolute(rejectString, CFSpeech | CFTimeout)
            if isLocalToon:
                # Go back into walk mode
                base.localAvatar.posCamera(0,0)
                base.cr.playGame.getPlace().setState("walk")
            return

        # Reject is simpler, so lets get that out of the way
        if (mode == NPCToons.QUEST_MOVIE_TIER_NOT_DONE):
            rejectString = Quests.chooseQuestDialogTierNotDone()
            rejectString = Quests.fillInQuestNames(rejectString, avName = av.name)
            # No need for page chat here, just setChatAbsolute
            self.setChatAbsolute(rejectString, CFSpeech | CFTimeout)
            if isLocalToon:
                # Go back into walk mode
                base.localAvatar.posCamera(0,0)
                base.cr.playGame.getPlace().setState("walk")
            return

        self.setupAvatars(av)
            
        fullString = ""
        toNpcId = None
        if (mode == NPCToons.QUEST_MOVIE_COMPLETE):
            questId, rewardId, toNpcId = quests

            # Try out the new quest script system
            scriptId = "quest_complete_" + str(questId)
            if QuestParser.questDefined(scriptId):
                self.curQuestMovie = QuestParser.NPCMoviePlayer(scriptId, av, self)
                self.curQuestMovie.play()
                return

            if isLocalToon:
                self.setupCamera(mode)
            greetingString = Quests.chooseQuestDialog(questId, Quests.GREETING)
            if greetingString:
                fullString += greetingString + "\a"
            fullString += Quests.chooseQuestDialog(questId, Quests.COMPLETE) + "\a"
            if rewardId:
                fullString += Quests.getReward(rewardId).getString()
            leavingString = Quests.chooseQuestDialog(questId, Quests.LEAVING)
            if leavingString:
                fullString += "\a" + leavingString
            
        elif (mode == NPCToons.QUEST_MOVIE_QUEST_CHOICE_CANCEL):
            fullString = TTLocalizer.QuestMovieQuestChoiceCancel
            
        elif (mode == NPCToons.QUEST_MOVIE_TRACK_CHOICE_CANCEL):
            fullString = TTLocalizer.QuestMovieTrackChoiceCancel
            
        elif (mode == NPCToons.QUEST_MOVIE_INCOMPLETE):
            questId, completeStatus, toNpcId = quests

            # Try out the new quest script system
            scriptId = "quest_incomplete_" + str(questId)
            if QuestParser.questDefined(scriptId):
                if self.curQuestMovie:
                    self.curQuestMovie.timeout()
                    self.curQuestMovie.cleanup()
                    self.curQuestMovie = None
                self.curQuestMovie = QuestParser.NPCMoviePlayer(scriptId, av, self)
                self.curQuestMovie.play()
                return

            if isLocalToon:
                self.setupCamera(mode)
            greetingString = Quests.chooseQuestDialog(questId, Quests.GREETING)
            if greetingString:
                fullString += greetingString + "\a"

            fullString += Quests.chooseQuestDialog(questId, completeStatus)
            leavingString = Quests.chooseQuestDialog(questId, Quests.LEAVING)
            if leavingString:
                fullString += "\a" + leavingString
            
        elif (mode == NPCToons.QUEST_MOVIE_ASSIGN):
            questId, rewardId, toNpcId = quests

            # Try out the new quest script system
            scriptId = "quest_assign_" + str(questId)
            if QuestParser.questDefined(scriptId):
                if self.curQuestMovie:
                    self.curQuestMovie.timeout()
                    self.curQuestMovie.cleanup()
                    self.curQuestMovie = None
                self.curQuestMovie = QuestParser.NPCMoviePlayer(scriptId, av, self)
                self.curQuestMovie.play()
                return

            if isLocalToon:
                self.setupCamera(mode)
            #greetingString = Quests.chooseQuestDialog(questId, Quests.GREETING)
            #if greetingString:
            #    fullString += greetingString + "\a"
            fullString += Quests.chooseQuestDialog(questId, Quests.QUEST)
            leavingString = Quests.chooseQuestDialog(questId, Quests.LEAVING)
            if leavingString:
                fullString += "\a" + leavingString

        elif (mode == NPCToons.QUEST_MOVIE_QUEST_CHOICE):
            # Quest choice movie
            if isLocalToon:
                self.setupCamera(mode)
            assert self.notify.debug("QUEST_MOVIE_QUEST_CHOICE: %s" % quests)
            self.setChatAbsolute(TTLocalizer.QuestMovieQuestChoice, CFSpeech)
            if isLocalToon:
                self.acceptOnce("chooseQuest", self.sendChooseQuest)
                self.questChoiceGui = QuestChoiceGui.QuestChoiceGui()
                self.questChoiceGui.setQuests(quests, npcId, ChoiceTimeout)
            return

        elif (mode == NPCToons.QUEST_MOVIE_TRACK_CHOICE):
            # If this is a TrackChoiceQuest, complete simply means we are at the
            # avatar that will allow us to chose. If the localToon cancels the
            # choice, we are not really complete yet
            # In this case, the quests are really the track choices
            if isLocalToon:
                self.setupCamera(mode)
            tracks = quests
            assert self.notify.debug("QUEST_MOVIE_TRACK_CHOICE: %s" % tracks)
            self.setChatAbsolute(TTLocalizer.QuestMovieTrackChoice, CFSpeech)
            if isLocalToon:
                self.acceptOnce("chooseTrack", self.sendChooseTrack)
                self.trackChoiceGui = TrackChoiceGui.TrackChoiceGui(tracks, ChoiceTimeout)
            return

        fullString = Quests.fillInQuestNames(fullString,
                                             avName = av.name,
                                             fromNpcId = npcId,
                                             toNpcId = toNpcId)

        self.acceptOnce(self.uniqueName("doneChatPage"),
                        self.finishMovie, extraArgs = [av, isLocalToon])
        self.setPageChat(avId, 0, fullString, 1)

    def sendChooseQuest(self, questId):
        """
        This is the callback from the questChoiceGui event
        Cleanup the gui and send the message with our choice to the AI
        """
        if self.questChoiceGui:
            self.questChoiceGui.destroy()
            self.questChoiceGui = None
        self.sendUpdate("chooseQuest", [questId])

    def sendChooseTrack(self, trackId):
        """
        This is the callback from the trackChoiceGui event
        Cleanup the gui and send the message with our choice to the AI
        """
        if self.trackChoiceGui:
            self.trackChoiceGui.destroy()
            self.trackChoiceGui = None
        self.sendUpdate("chooseTrack", [trackId])

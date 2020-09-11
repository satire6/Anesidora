
from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.quest import Quests

class DistributedNPCSpecialQuestGiverAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, questCallback=None, hq=0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        # Am I a hq toon? Maybe this should be a subclass?
        self.hq = hq
        # Am I part of the tutorial?
        self.tutorial = 0
        # Initialize the pendingAvId to None in case we get any rogue messages
        self.pendingAvId = None

    def getTutorial(self):
        return self.tutorial

    def setTutorial(self, val):
        # If you are in the tutorial you have no timeouts
        self.tutorial = val

    def getHq(self):
        return self.hq
        
    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        # this avatar has come within range
        self.notify.debug("avatar enter " + str(avId))
        # Let the quest manager figure out what to do from here on
        self.air.questManager.requestInteract(avId, self)
        DistributedNPCToonBaseAI.avatarEnter(self)

    def chooseQuest(self, questId, quest = None):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("chooseQuest: avatar %s choseQuest %s" % (avId, questId))

        # Sanity check, this should not happen
        if (not self.pendingAvId):
            self.notify.warning("chooseQuest: not expecting an answer from any avatar: %s" % (avId))
            return
        if (self.pendingAvId != avId):
            self.notify.warning("chooseQuest: not expecting an answer from this avatar: %s" % (avId))
            return

        # See if the avatar cancelled
        if questId == 0:
            # Clear the pendings
            self.pendingAvId = None
            self.pendingQuests = None
            # Tell the quest manager this avatar cancelled
            self.air.questManager.avatarCancelled(avId)
            # Tell the avatar goodbye then allow him to finish the movie
            self.cancelChoseQuest(avId)
            return

        # See if the avatar chose any of the quests offered
        for quest in self.pendingQuests:
            if (questId == quest[0]):
                # Clear the pendings
                self.pendingAvId = None
                self.pendingQuests = None
                # Let the quest manager figure out what to do from here on
                self.air.questManager.avatarChoseQuest(avId, self, *quest)
                return
                
        self.air.questManager.avatarChoseQuest(avId, self, *quest)

        # If we got here, something is wrong, handle it gracefully
        self.notify.warning("chooseQuest: avatar: %s chose a quest not offered: %s" % (avId, questId))
        # Clear the pendings
        self.pendingAvId = None
        self.pendingQuests = None
        return

    def chooseTrack(self, trackId):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("chooseTrack: avatar %s choseTrack %s" % (avId, trackId))

        if (not self.pendingAvId):
            self.notify.warning("chooseTrack: not expecting an answer from any avatar: %s" % (avId))
            return
        if (self.pendingAvId != avId):
            self.notify.warning("chooseTrack: not expecting an answer from this avatar: %s" % (avId))
            return

        # See if the avatar cancelled
        if trackId == -1:
            # Clear the pendings
            self.pendingAvId = None
            self.pendingTracks = None
            self.pendingTrackQuest = None
            # Tell the quest manager this avatar cancelled
            self.air.questManager.avatarCancelled(avId)
            # Tell the avatar goodbye then allow him to finish the movie
            self.cancelChoseTrack(avId)
            return

        # See if the avatar chose any of the tracks offered
        for track in self.pendingTracks:
            if (trackId == track):
                # Let the quest manager figure out what to do from here on
                self.air.questManager.avatarChoseTrack(avId, self, self.pendingTrackQuest, trackId)
                # Clear the pendings
                self.pendingAvId = None
                self.pendingTracks = None
                self.pendingTrackQuest = None
                return

        # If we got here, something is wrong, handle it gracefully
        self.notify.warning("chooseTrack: avatar: %s chose a track not offered: %s" % (avId, trackId))
        # Clear the pendings
        self.pendingAvId = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        return


    def sendTimeoutMovie(self, task):
        # Clear the movie
        self.pendingAvId = None
        self.pendingQuests = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_TIMEOUT,
                                     self.npcId, self.busy, [],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        self.busy = 0
        return Task.done

    def sendClearMovie(self, task):
        # Clear the movie
        self.pendingAvId = None
        self.pendingQuests = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        self.busy = 0
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_CLEAR,
                                     self.npcId, 0, [],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def rejectAvatar(self, avId):
        self.busy = avId
        # Send a movie to reject the avatar with time stamp
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_REJECT,
                                     self.npcId, avId, [],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # No timeout here because we do not wait for the toon to click on rejects
        # Just send a clear after a pause
        #
        # We actually need a longer pause here - people need to read the text before
        # clearMovie wipes it -grw
        if not self.tutorial:
            taskMgr.doMethodLater(5.5, self.sendClearMovie, self.uniqueName("clearMovie"))
        return
        
    def rejectAvatarTierNotDone(self, avId):
        self.busy = avId
        # Send a movie to reject the avatar with time stamp
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_TIER_NOT_DONE,
                                     self.npcId, avId, [],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # No timeout here because we do not wait for the toon to click on rejects
        # Just send a clear after a pause
        #
        # We actually need a longer pause here - people need to read the text before
        # clearMovie wipes it -grw
        if not self.tutorial:
            taskMgr.doMethodLater(5.5, self.sendClearMovie, self.uniqueName("clearMovie"))
        return

    def completeQuest(self, avId, questId, rewardId):
        self.busy = avId
        # nextQuestId will be the npc for the next visiting quest (visitNpcId)
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_COMPLETE,
                                     self.npcId, avId, [questId, rewardId, 0],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def incompleteQuest(self, avId, questId, completeStatus, toNpcId):
        self.busy = avId
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_INCOMPLETE,
                                     self.npcId, avId, [questId, completeStatus, toNpcId],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def assignQuest(self, avId, questId, rewardId, toNpcId):
        self.busy = avId
        # Call the quest callback now. We could wait until the movie
        # is over, but I don't think we need to.
        if self.questCallback:
            self.questCallback()
        #print "assignQuest", avId
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_ASSIGN,
                                     self.npcId, avId, [questId, rewardId, toNpcId],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def presentQuestChoice(self, avId, quests):
        self.busy = avId
        self.pendingAvId = avId
        self.pendingQuests = quests
        flatQuests = []
        for quest in quests:
            flatQuests.extend(quest)
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_QUEST_CHOICE,
                                     self.npcId, avId, flatQuests,
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def presentTrackChoice(self, avId, questId, tracks):
        self.busy = avId
        self.pendingAvId = avId
        self.pendingTracks = tracks
        self.pendingTrackQuest = questId
        # Send a movie to present the choice to the avatar
        # Instead of quests, we send the trackIds
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_TRACK_CHOICE,
                                     self.npcId, avId, tracks,
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def cancelChoseQuest(self, avId):
        self.busy = avId
        # Send a movie to present the choice to the avatar
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_QUEST_CHOICE_CANCEL,
                                     self.npcId, avId, [],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def cancelChoseTrack(self, avId):
        self.busy = avId
        self.sendUpdate("setMovie", [NPCToons.QUEST_MOVIE_TRACK_CHOICE_CANCEL,
                                     self.npcId, avId, [],
                                     ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        return

    def setMovieDone(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("setMovieDone busy: %s avId: %s" % (self.busy, avId))
        if self.busy == avId:
            # Kill all pending doLaters that will clear the movie 
            taskMgr.remove(self.uniqueName("clearMovie"))
            self.sendClearMovie(None)
        elif self.busy:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCToonAI.setMovieDone busy with %s' % (self.busy))
            self.notify.warning("somebody called setMovieDone that I was not busy with! avId: %s" % avId)

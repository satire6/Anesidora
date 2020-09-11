#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: AI component that manages which toons are currently dancing, who entered
#          and exited the dance floor, and broadcasts dance moves to all clients.
#-------------------------------------------------------------------------------
import random
from direct.task.Task import Task

from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties import PartyGlobals
from random import randint

class DistributedPartyJukeboxActivityBaseAI(DistributedPartyActivityAI):
    notify = directNotify.newCategory("DistributedPartyJukeboxActivityAI")
    
    def __init__(self, air, partyDoId, x, y, h, actId, phaseToMusicData):
        self.notify.debug("Intializing.")
        DistributedPartyActivityAI.__init__(self,
                                            air,
                                            partyDoId,
                                            x, y, h,
                                            actId,
                                            PartyGlobals.ActivityTypes.Continuous
                                            )
    
        # Holds the list of songs requested by each avatar.
        # Format: { toonId : (phase, filename), ... }
        self.phaseToMusicData = phaseToMusicData
        self.toonIdToSongData = {}
        # Holds the queue of songs to be played by avatarId
        self.toonIdQueue = []
        
        self.songPlaying = False
        self.songTimerTask = None
        
        self.timeoutTask = None
        
        # listen for fireworks show starting and stopping
        self.accept( PartyGlobals.FireworksStartedEvent, self.__handleFireworksStarted )
        self.accept( PartyGlobals.FireworksFinishedEvent, self.__handleFireworksFinished )

        # this ensure the first song we hear is one of the new ones
        self.randomSongPhase = 13
        
    def delete(self):
        self.ignoreAll()
        self.__stopTimeout()
        DistributedPartyActivityAI.delete(self)
        
    def generate(self):
        DistributedPartyActivityAI.generate(self)
        self.__playNextSong()
        
    # Distributed (clsend airecv)
    def toonJoinRequest(self):    
        """
        Gets from client when a toon requests to use the jukebox.
        only one toon can use the jukebox.
        """
        senderId = self.air.getAvatarIdFromSender()
        self.notify.debug("Request enter %s" % senderId)
        if senderId not in self.toonIds:
            joined = (len(self.toonIds) == 0)
            if self.party.isInActivity(senderId):
                joined = False
            self.__startTimeout(PartyGlobals.JUKEBOX_TIMEOUT)
            self.sendToonJoinResponse(senderId, joined)
        #TODO: Add suspicious behavior case?
        
    # Distributed (clsend airecv)
    def toonExitRequest(self):
        """
        Sent from client when toon using the jukebox wishes to stop using the
        jukebox.
        """
        senderId = self.air.getAvatarIdFromSender()
        self.notify.debug("Request exit %s" % senderId)
        if senderId in self.toonIds:
            self.sendToonExitResponse(senderId, True)
        else:
            self.sendToonExitResponse(senderId, False)
        
    def toonExitResponse(self, senderId, exited):
        if exited:
            self.__stopTimeout()
        DistributedPartyActivityAI.sendToonExitResponse(self, senderId, exited)
        
#===============================================================================
# Song addition, playing, etc.
#===============================================================================
  
    # Distributed (clsend airecv)
    def queuedSongsRequest(self):
        senderId = self.air.getAvatarIdFromSender()
        
        songInfoList = []
        index = -1
        for i in range(len(self.toonIdQueue)):
            toonId = self.toonIdQueue[i]
            if toonId == senderId:
                index = i
            songInfoList.append(self.toonIdToSongData[toonId])
        self.d_queuedSongsResponse(senderId, songInfoList, index)

    # Distributed
    def d_queuedSongsResponse(self, senderId, songInfoList, index):
        self.sendUpdateToAvatarId(senderId,
                                  "queuedSongsResponse",
                                  [songInfoList, index])
        
    # Distributed (clsend airecv)
    def setNextSong(self, nextSongInfo):
        """
        Called by client when adding or replacing a song in the queue.
        """
        phase = PartyGlobals.sanitizePhase(nextSongInfo[0])
        filename = nextSongInfo[1]
        self.notify.debug("setNextSong %d/%s" % (phase, filename))
        
        senderId = self.air.getAvatarIdFromSender()
        data = self.getMusicData(phase, filename)
        if data:
            self.toonIdToSongData[senderId] = (phase, filename)
            if senderId not in self.toonIdQueue:
                self.toonIdQueue.append(senderId)
            self.d_setSongInQueue(senderId, nextSongInfo)
    
    # Distributed (required broadcast ram)  
    def d_setSongPlaying(self, phase, filename, toonId=0):
        self.sendUpdate("setSongPlaying", [(phase, filename), toonId])
    
    # Distributed
    def d_setSongInQueue(self, toonId, songInfo):
        self.sendUpdateToAvatarId(toonId, "setSongInQueue", [songInfo])
            
#===============================================================================
# Host Toon only
#===============================================================================
   
    # Distributed (clsend airecv)
    def moveHostSongToTopRequest(self):
        self.notify.debug("moveHostSongToTopRequest")
        senderId = self.air.getAvatarIdFromSender()
        # TODO: Check to see if senderId is in fact party host
        if senderId in self.toonIdQueue:
            self.b_moveHostSongToTop(senderId)
        
    def moveHostSongToTop(self, hostId):
        self.toonIdQueue.remove(hostId)
        self.toonIdQueue.insert(0, hostId)
    
    def d_moveHostSongToTop(self, hostId):
        self.notify.debug("d_moveHostSongToTop")
        self.sendUpdateToAvatarId(hostId, "moveHostSongToTop", [])
        
    def b_moveHostSongToTop(self, hostId):
        self.moveHostSongToTop(hostId)
        self.d_moveHostSongToTop(hostId)
    
#===============================================================================
# Song scheduling
#===============================================================================

    def __playNextSong(self):
        self.notify.debug("__playNextSong")
        """
        Pops song out of the queue, broadcasts new song to all clients,
        and schedules next play task.
        """
        self.songPlaying = False
        toonId = 0
        # Play the next song in the queue
        if len(self.toonIdQueue) > 0:
            toonId = self.toonIdQueue[0]
            songInfo = self.toonIdToSongData.get(toonId, None)
            del self.toonIdToSongData[toonId]
            self.toonIdQueue.remove(toonId)
            
        # No song in the queue? Pick a random song!
        else:
            songInfo = self.getRandomMusicInfo(self.randomSongPhase)
            # every other random song is one of the new party songs
            self.randomSongPhase = -1
            self.notify.debug("random songInfo=%s" % str(songInfo))
            
        if songInfo is not None:
            phase = songInfo[0]
            filename = songInfo[1]
            data = self.getMusicData(phase, filename)
            if data:
                self.notify.debug("Playing song: %s, %s" % (phase, filename))
                self.d_setSongPlaying(phase, filename, toonId)
                self.__startTimerForNextSong(self.__getTimeUntilNextSong(data[1]))
                self.songPlaying = True
        
    def __getTimeUntilNextSong(self, duration):
        return (PartyGlobals.getMusicRepeatTimes(duration) * duration) + PartyGlobals.MUSIC_GAP
        
    def __playNextSongTask(self, task):
        self.__playNextSong()
        return Task.done
    
    def __startTimerForNextSong(self, seconds):
        self.notify.debug("Playing next song in %d seconds." % seconds)
        self.__stopTimerForNextSong()
        self.songTimerTask = taskMgr.doMethodLater(seconds,
                                                   self.__playNextSongTask,
                                                   self.taskName("playNextSong"))
    
    def __stopTimerForNextSong(self):
        if self.songTimerTask != None:
            taskMgr.remove(self.songTimerTask)
            self.songTimerTask = None
    
#===============================================================================
# Timeout
#===============================================================================

    def __startTimeout(self, timeLimit):
        """
        Sets the timeout counter running.  If __stopTimeout() is not
        called before the time expires, we'll exit the avatar.  This
        prevents avatars from hanging out in the jukebox all day.
        """
        self.__stopTimeout()
        self.timeoutTask = taskMgr.doMethodLater(timeLimit,
                                                 self.__handleTimeoutTask,
                                                 self.taskName("timeout"))

    def __stopTimeout(self):
        """
        Stops a previously-set timeout from expiring.
        """
        if self.timeoutTask != None:
            taskMgr.remove(self.timeoutTask)
            self.timeoutTask = None

    def __handleTimeoutTask(self, task):
        """
        Called when a timeout expires, this kicks the toon out of the jukebox.
        """
        self.notify.debug('Timeout expired!')
        if len(self.toonIds) > 0:
            self.toonExitResponse(self.toonIds[0], True)
        return Task.done


    def getRandomMusicInfo(self, phase=13):
        if phase == -1:
            # Get random phase
            keys = self.phaseToMusicData.keys()
            # bias random music towards the new party songs
            keys += [13,13,13,]
            phase = random.choice(keys) # this is random.choice

        # From that phase, get random filename
        values = self.phaseToMusicData[phase].keys()
        filename = values[randint(0, len(values) - 1)]

        return (phase, filename)


    def getMusicData(self, phase, filename):
        data = []
        phase = PartyGlobals.sanitizePhase(phase)
        phase = self.phaseToMusicData.get(phase)
        if phase:
            data = phase.get(filename, [])
        return data    
    
#===============================================================================
# React to fireworks show
#===============================================================================
    
    def __handleFireworksStarted(self):
        self.notify.debug("__handleFireworksStarted")
        self.__stopTimerForNextSong()
        self.d_setSongPlaying(0, "", 0)
    
    def __handleFireworksFinished(self):
        self.notify.debug("__handleFireworksFinished")
        self.__playNextSong()


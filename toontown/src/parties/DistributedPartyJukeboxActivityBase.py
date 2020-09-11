#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: Party Jukebox Activity places a jukebox in the party and controls
#          playback of all the music. Music scheduling is handled on the AI side.
#
# Bug Fixes:
# 1. Fixed occasasion where it can throw an exception on an unloaded GUI:
#    Toon walks to the jukebox, and the Jukebox GUI pops up.
#    Toon adds a song, the "Add Song" button is disabled while the request is sent to the server.
#    While the server is processing the request, the Toon closes the Jukebox GUI, which is unloaded from the client.
#    When the response comes back, the client expects a GUI to be loaded so that it can enable the "Add Song" button again.
#    Solution:
#        make sure that self.gui.isLoaded() is in check first before doing
#        server response operations.
#-------------------------------------------------------------------------------

from direct.actor.Actor import Actor
from direct.task.Task import Task

from pandac.PandaModules import *

from otp.otpbase.OTPBase import OTPBase

from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

from toontown.parties.DistributedPartyActivity import DistributedPartyActivity
from toontown.parties.PartyGlobals import ActivityIds, ActivityTypes, JUKEBOX_TIMEOUT
from toontown.parties.PartyGlobals import getMusicRepeatTimes, MUSIC_PATH,  sanitizePhase
from toontown.parties.JukeboxGui import JukeboxGui

class DistributedPartyJukeboxActivityBase(DistributedPartyActivity):
    notify = directNotify.newCategory("DistributedPartyJukeboxActivityBase")
    
    def __init__(self, cr, actId, phaseToMusicData):
        DistributedPartyActivity.__init__(self,
                                          cr,
                                          actId,
                                          ActivityTypes.Continuous
                                          )
        self.phaseToMusicData = phaseToMusicData
        self.jukebox = None
        self.gui = None
        
        self.tunes = []
        self.music = None
        # Data is tuple (phase, filename)
        self.currentSongData = None
        
        self.localQueuedSongInfo = None
        self.localQueuedSongListItem = None

    def generateInit(self):
        self.gui = JukeboxGui(self.phaseToMusicData)
    
    def load(self):
        DistributedPartyActivity.load(self)
        
        # Load Jukebox actor
        self.jukebox = Actor("phase_13/models/parties/jukebox_model",
                             {"dance": "phase_13/models/parties/jukebox_dance"}
                             )
        self.jukebox.reparentTo(self.root)
        
        # Create collision area for jukebox
        self.collNode = CollisionNode(self.getCollisionName())
        self.collNode.setCollideMask(ToontownGlobals.CameraBitmask | ToontownGlobals.WallBitmask)
        
        collTube = CollisionTube(0, 0, 0, 0.0, 0.0, 4.25, 2.25)
        collTube.setTangible(1)
        self.collNode.addSolid(collTube)
        self.collNodePath = self.jukebox.attachNewNode(self.collNode)

        self.sign.setPos(-5.0, 0, 0)
        
        self.activate()
    
    def unload(self):
        DistributedPartyActivity.unload(self)
        
        self.gui.unload()
        
        if self.music is not None:
            self.music.stop()
        
        self.jukebox.stop()
        self.jukebox.delete()
        self.jukebox = None
        
        self.ignoreAll()
        
    def getCollisionName(self):
        return self.uniqueName("jukeboxCollision")
    
    def activate(self):
        self.accept("enter" + self.getCollisionName(),
                    self.__handleEnterCollision)
    
#===============================================================================
# Enter/Exit Jukebox
#===============================================================================

    def __handleEnterCollision(self, collisionEntry):    
        if base.cr.playGame.getPlace().fsm.getCurrentState().getName() == "walk":
            base.cr.playGame.getPlace().fsm.request("activity")
            self.d_toonJoinRequest()
    
    def joinRequestDenied(self, reason):
        DistributedPartyActivity.joinRequestDenied(self, reason)
        self.showMessage(TTLocalizer.PartyJukeboxOccupied)
    
    # Distributed (broadcast ram)
    def handleToonJoined(self, toonId):
        """
        Toon requested to use the jukebox and the request has been granted.
        """
        toon = base.cr.doId2do.get(toonId)
        if toon:
            self.jukebox.lookAt(base.cr.doId2do[toonId])
            self.jukebox.setHpr(self.jukebox.getH() + 180.0, 0, 0)
        
        if toonId == base.localAvatar.doId:
            self.__localUseJukebox()
    
    def handleToonExited(self, toonId):
        """
        Typically called when toon times out.
        """
        if toonId == base.localAvatar.doId and self.gui.isLoaded():
            self.__deactivateGui()

    def handleToonDisabled(self, toonId):
        """
        A toon dropped unexpectedly from the game. Handle it!
        """
        self.notify.warning("handleToonDisabled no implementation yet" )              
    
    def __localUseJukebox(self):
        """
        Sets the local toon to use the jukebox, including activating the GUI and
        changing the client into the appropriate state.
        """
        base.localAvatar.disableAvatarControls()
        base.localAvatar.stopPosHprBroadcast()
        
        self.__activateGui()
        
        self.accept(JukeboxGui.CLOSE_EVENT, self.__handleGuiClose)
        
        # We are locking exiting now in case the AI times the toon out of the Jukebox.
        taskMgr.doMethodLater(
            0.5,
            self.__localToonWillExitTask,
            self.uniqueName("toonWillExitJukeboxOnTimeout"),
            extraArgs=None
            )
        
        self.accept(JukeboxGui.ADD_SONG_CLICK_EVENT, self.__handleQueueSong)
        if self.isUserHost():
            self.accept(JukeboxGui.MOVE_TO_TOP_CLICK_EVENT, self.__handleMoveSongToTop)
    
    def __localToonWillExitTask(self, task):
        self.localToonExiting()
        return Task.done
        
    def __activateGui(self):
        self.gui.enable(timer=JUKEBOX_TIMEOUT)
        self.gui.disableAddSongButton()
        if self.currentSongData is not None:
            self.gui.setSongCurrentlyPlaying(self.currentSongData[0],
                                             self.currentSongData[1])
        self.d_queuedSongsRequest()
        
    def __deactivateGui(self):
        self.ignore(JukeboxGui.CLOSE_EVENT)
        self.ignore(JukeboxGui.SONG_SELECT_EVENT)
        self.ignore(JukeboxGui.MOVE_TO_TOP_CLICK_EVENT)
        
        base.cr.playGame.getPlace().setState("walk")
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.enableAvatarControls()
        
        self.gui.unload()
        self.__localClearQueuedSong()
        
    def isUserHost(self):
        """
        Checks if the localAvatar is the host of the party
        Returns
            true if localAvatar is the host of the party
        """
        return (self.party.partyInfo.hostId == base.localAvatar.doId)
        
    # Distributed (clsend airecv)
    def d_queuedSongsRequest(self):
        self.sendUpdate("queuedSongsRequest")
        
    # Distributed (only sender receives this response)
    def queuedSongsResponse(self, songInfoList, index):
        """
        Gets a list of songs and adds them to the queue.
        Called when the toon first interacts with the jukebox.
        
        Parameters:
            songInfoList is the list of songs
            index is the item # on the list for a song previously queued by the player.
        """
        if self.gui.isLoaded():
            for i in range(len(songInfoList)):
                songInfo = songInfoList[i]
                
                self.__addSongToQueue(songInfo,
                                      isLocalQueue=(index >=0 and i == index))
        
        
            self.gui.enableAddSongButton()
        
    def __handleGuiClose(self):
        """
        Closes Jukebox GUI, cleans up event handlers, and sets client state to normal.
        Typically triggered when the player clicks the close
        button in the jukebox, which fires CLOSE_EVENT.
        """
        self.__deactivateGui()
        self.d_toonExitDemand()
        
#===============================================================================
# Queueing songs
#===============================================================================

    def __handleQueueSong(self, name, values):
        """
        Requests to queue a song.
        Triggered when the localAvatar clicks the "Add/Replace Song button".
        """
        self.d_setNextSong(values[0], values[1])
        
    # Distributed (clsend airecv)
    def d_setNextSong(self, phase, filename):
        self.sendUpdate("setNextSong", [(phase, filename)])
        
    # Distributed (sender only gets it back)
    def setSongInQueue(self, songInfo):
        if self.gui.isLoaded():
            phase = sanitizePhase(songInfo[0])
            filename = songInfo[1]
            data = self.getMusicData(phase, filename)
            
            if data:
                if self.localQueuedSongListItem is not None:
                    self.localQueuedSongListItem["text"] = data[0]
                else:
                    self.__addSongToQueue(songInfo,
                                          isLocalQueue=True)
                    
    def __addSongToQueue(self, songInfo, isLocalQueue=False):
        """
        Adds a song to the queue. If it's the localAvatar's queued song, then
        it marks it.
        
        Parameters:
            songInfo is a list of phase and data
            isLocalQueue is flag marking whether this is the localAvatar's queued song
        """
        isHost = (isLocalQueue and self.isUserHost())
        
        data = self.getMusicData(sanitizePhase(songInfo[0]), songInfo[1])
        if data:
            listItem = self.gui.addSongToQueue(data[0],
                                               highlight=isLocalQueue,
                                               moveToTopButton=isHost)
            if isLocalQueue:
                self.localQueuedSongInfo = songInfo
                self.localQueuedSongListItem = listItem
                
    def __localClearQueuedSong(self):
        """
        Clears the queued song records.
        """
        self.localQueuedSongInfo = None
        self.localQueuedSongListItem = None
        
#===============================================================================
# Music Playback
#===============================================================================

    def __play(self, phase, filename, length):
        """
        Plays some music!
        """
        assert self.notify.debugStateCall(self)
        self.music = base.loadMusic((MUSIC_PATH + "%s") % (phase, filename))
        if self.music:
            if self.__checkPartyValidity() and hasattr(base.cr.playGame.getPlace().loader, "music") and base.cr.playGame.getPlace().loader.music:
                base.cr.playGame.getPlace().loader.music.stop()
            base.resetMusic.play()
            self.music.setTime(0.0)
            self.music.setLoopCount(getMusicRepeatTimes(length))
            self.music.play()
            jukeboxAnimControl = self.jukebox.getAnimControl("dance")
            if not jukeboxAnimControl.isPlaying():
                self.jukebox.loop("dance")
            self.currentSongData = (phase, filename)
            
    def __stop(self):
        """
        Stops animations and and clears GUI.
        """
        self.jukebox.stop()
        self.currentSongData = None
        
        if self.music:
            self.music.stop()
            
        if self.gui.isLoaded():
            self.gui.clearSongCurrentlyPlaying()
    
    # Distributed (broadcast ram)  
    def setSongPlaying(self, songInfo, toonId):
        """
        Sets the song from the AI to play in the client.
        Parameters:
            songInfo is a list with two items: phase and filename
        """
        
        phase = sanitizePhase(songInfo[0])
        filename = songInfo[1]
        assert(self.notify.debug("setSongPlaying phase_%d/%s" % (phase, filename)))
        
        # setSongPlaying sends empty filename if songs have stop playing
        # in order for the client to clean up.
        if not filename:
            self.__stop()
            return
        
        data = self.getMusicData(phase, filename)
        if data:
            self.__play(phase, filename, data[1])
            self.setSignNote(data[0])
            
            # Update the gui if it's active:
            if self.gui.isLoaded():
                item = self.gui.popSongFromQueue()
                self.gui.setSongCurrentlyPlaying(phase, filename)
                
                if item == self.localQueuedSongListItem:
                    self.__localClearQueuedSong()

        if toonId == localAvatar.doId:
            localAvatar.setSystemMessage(0, TTLocalizer.PartyJukeboxNowPlaying)
                
#===============================================================================
# Host only: Push his/her queued song to the top of the playlist.
#===============================================================================

    def __handleMoveSongToTop(self):
        """
        Requests to move the localAvatar's queued song to top.
        It is triggered when the user clicks on the "moveToTopButton" on the GUI.
        This is only enabled for the host of the party.
        """
        if self.isUserHost() and self.localQueuedSongListItem is not None:
            self.d_moveHostSongToTopRequest()
    
    # Distributed (clsend airecv)
    def d_moveHostSongToTopRequest(self):
        self.notify.debug("d_moveHostSongToTopRequest")
        self.sendUpdate("moveHostSongToTopRequest")
        
    # Distributed (only host gets it)
    def moveHostSongToTop(self):
        self.notify.debug("moveHostSongToTop")
        if self.gui.isLoaded():
            self.gui.pushQueuedItemToTop(self.localQueuedSongListItem)
    

    def getMusicData(self, phase, filename):
        data = []
        phase = sanitizePhase(phase)
        phase = self.phaseToMusicData.get(phase)
        if phase:
            data = phase.get(filename, [])
        return data    
        
        
    def __checkPartyValidity(self):
        """ Function that checks the validity of a street,
        it's loader and the geometry"""
        if hasattr(base.cr.playGame, "getPlace") and base.cr.playGame.getPlace() and \
        hasattr(base.cr.playGame.getPlace(), "loader") and base.cr.playGame.getPlace().loader:
            return True
        else:
            return False

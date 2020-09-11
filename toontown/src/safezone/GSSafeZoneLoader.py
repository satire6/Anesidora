##########################################################################
# Module: GSSafeZoneLoader.py
# Purpose: This module oversees the construction of the Goofy Speedway
# safe zone loader object.
#
# Date: 6/10/05
# Author: jjtaylor (jjtaylor@schellgames.com)
# Note: Modification of original GSLoader.py
##########################################################################

##########################################################################
# Panda/Direct Import Modules
##########################################################################
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from pandac.PandaModules import *

##########################################################################
# Toontwon Import Modules
##########################################################################
from toontown.hood import ZoneUtil
from toontown.launcher import DownloadForceAcknowledge
from toontown.safezone.SafeZoneLoader import SafeZoneLoader
from toontown.safezone.GSPlayground import GSPlayground
from toontown.effects.CarSmoke import CarSmoke
from toontown.toonbase import ToontownGlobals


##########################################################################
# Python Import Modules
##########################################################################
import random
if( __debug__ ):
    import pdb

class GSSafeZoneLoader( SafeZoneLoader ):
    """
    Purpose: The GSSafeZoneLoader Class provides.. yadda yadda
    """

    def __init__( self, hood, parentFSM, doneEvent ):
        """
        """

        # Initialize Super Class
        SafeZoneLoader.__init__( self, hood, parentFSM, doneEvent )     

        # Initialize Instance Variables
        self.musicFile = "phase_6/audio/bgm/GS_SZ.mid"
        self.activityMusicFile = "phase_6/audio/bgm/GS_KartShop.mid"
        self.dnaFile = "phase_6/dna/goofy_speedway_sz.dna"
        self.safeZoneStorageDNAFile = "phase_6/dna/storage_GS_sz.dna"

        # Override Super Class FSM
        del self.fsm
        self.fsm = ClassicFSM.ClassicFSM('SafeZoneLoader',
                              [State.State('start',
                                           self.enterStart,
                                           self.exitStart,
                                           ['quietZone',
                                            'playground',
                                            'toonInterior',]),
                               State.State('playground',
                                           self.enterPlayground,
                                           self.exitPlayground,
                                           ['quietZone', 'racetrack' ]),
                               State.State('toonInterior',
                                           self.enterToonInterior,
                                           self.exitToonInterior,
                                           ['quietZone']),
                               State.State('quietZone',
                                           self.enterQuietZone,
                                           self.exitQuietZone,
                                           ['playground', 'toonInterior', 'racetrack' ]),
                               State.State('racetrack',
                                           self.enterRacetrack,
                                           self.exitRacetrack,
                                           ['quietZone', 'playground']),
                               State.State('final',
                                           self.enterFinal,
                                           self.exitFinal,
                                           ['start'])],
                              # Initial State
                              'start',
                              # Final State
                              'final', )                              
        self.smoke = None

    def load( self ):
        """
        """


        SafeZoneLoader.load( self )                
        
        if base.cr.newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if ToontownGlobals.CRASHED_LEADERBOARD in holidayIds:
                self.startSmokeEffect()                
                
        self.birdSound = map( base.loadSfx, [ 'phase_4/audio/sfx/SZ_TC_bird1.mp3',
                                              'phase_4/audio/sfx/SZ_TC_bird2.mp3',
                                              'phase_4/audio/sfx/SZ_TC_bird3.mp3' ] )

    def unload( self ):
        """
        """
        del self.birdSound                
        
        if self.smoke != None:        
            self.stopSmokeEffect()             
            
        SafeZoneLoader.unload( self )

    def enterPlayground( self, requestStatus ):
        """
        """
        self.playgroundClass = GSPlayground
        SafeZoneLoader.enterPlayground( self, requestStatus )

        # self.hood.spawnTitleText( requestStatus[ 'zoneId' ] )

    def exitPlayground( self ):
        """
        """

        taskMgr.remove( 'titleText' )
        self.hood.hideTitleText()
        SafeZoneLoader.exitPlayground( self )
        self.playgroundClass = None

    def handlePlaygroundDone( self ):
        assert( self.notify.debug( "handlePlaygroundDone()" ) )
        status = self.place.doneStatus
        if( self.enteringARace( status ) and status.get( 'shardId' ) == None ):
            # GIVE THIS A WHIRL
            zoneId = status[ 'zoneId' ]
            self.fsm.request( 'quietZone', [ status ] )
        elif (ZoneUtil.getBranchZone(status["zoneId"]) == self.hood.hoodId and
            # Going to Kart Shop
            status["shardId"] == None):
            self.fsm.request("quietZone", [status])            
        else:
            self.doneStatus = status
            messenger.send( self.doneEvent )

    def enteringARace( self, status ):
        if( not status[ 'where' ] == 'racetrack' ):
            return 0
        if( ZoneUtil.isDynamicZone( status[ 'zoneId' ] ) ):
            return status[ 'hoodId' ] == self.hood.hoodId
        else:
            return ZoneUtil.getHoodId( status[ 'zoneId' ] ) == self.hood.hoodId

    def enterRacetrack( self, requestStatus ):
        """
        """

        # Racetrack will grab this off of us
        self.trackId = requestStatus[ 'trackId' ]
        self.accept("raceOver",self.handleRaceOver)
        self.accept("leavingRace",self.handleLeftRace)

        base.transitions.fadeOut(t=0)

    def exitRacetrack( self ):
        """
        """
        del self.trackId

    def handleRaceOver(self):
        print "you done!!"

    def handleLeftRace(self):
        req={"loader":"safeZoneLoader","where":"playground","how":"teleportIn"
             ,"zoneId":8000,"hoodId":8000,"shardId":None}
        self.fsm.request("quietZone",[req])        
                
    def startSmokeEffect(self):           
        if base.config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            leaderBoard = self.geom.find("**/*crashed*")      
            locator = leaderBoard.find("**/*locator_smoke*")
            if locator != None:          
                self.smoke = CarSmoke(locator)            
                self.smoke.start()                 
                        
    def stopSmokeEffect(self):   
        if base.config.GetBool('want-crashedLeaderBoard-Smoke', 1):         
            if self.smoke != None:
                self.smoke.stop()        
                self.smoke.destroy()                
                self.smoke = None

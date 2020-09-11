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
from direct.gui import DirectGui
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from pandac.PandaModules import *

##########################################################################
# Toontwon Import Modules
##########################################################################
from toontown.hood import ZoneUtil
from toontown.launcher import DownloadForceAcknowledge
from toontown.safezone.SafeZoneLoader import SafeZoneLoader
from toontown.safezone.GZPlayground import GZPlayground
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

##########################################################################
# Python Import Modules
##########################################################################
import random
if( __debug__ ):
    import pdb

class GZSafeZoneLoader( SafeZoneLoader ):
    """
    Purpose: The GZSafeZoneLoader Class provides.. yadda yadda
    """

    def __init__( self, hood, parentFSM, doneEvent ):
        """
        """
        # Initialize Super Class
        SafeZoneLoader.__init__( self, hood, parentFSM, doneEvent )     

        # Initialize Instance Variables
        self.musicFile = "phase_6/audio/bgm/GZ_SZ.mid"
        self.activityMusicFile = "phase_6/audio/bgm/GS_KartShop.mid"
        self.dnaFile = "phase_6/dna/golf_zone_sz.dna"
        self.safeZoneStorageDNAFile = "phase_6/dna/storage_GZ_sz.dna"

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
                                           ['quietZone', 'golfcourse' ]),
                               State.State('toonInterior',
                                           self.enterToonInterior,
                                           self.exitToonInterior,
                                           ['quietZone']),
                               State.State('quietZone',
                                           self.enterQuietZone,
                                           self.exitQuietZone,
                                           ['playground', 'toonInterior', 'golfcourse' ]),
                               State.State('golfcourse',
                                           self.enterGolfCourse,
                                           self.exitGolfCourse,
                                           ['quietZone', 'playground']),
                               State.State('final',
                                           self.enterFinal,
                                           self.exitFinal,
                                           ['start'])],
                              # Initial State
                              'start',
                              # Final State
                              'final', )

    def load( self ):
        """
        """


        SafeZoneLoader.load( self )
        self.birdSound = map( base.loadSfx, [ 'phase_4/audio/sfx/SZ_TC_bird1.mp3',
                                              'phase_4/audio/sfx/SZ_TC_bird2.mp3',
                                              'phase_4/audio/sfx/SZ_TC_bird3.mp3' ] )

    def unload( self ):
        """
        """
        del self.birdSound
        SafeZoneLoader.unload( self )

    def enterPlayground( self, requestStatus ):
        """
        """
        self.playgroundClass = GZPlayground
        SafeZoneLoader.enterPlayground( self, requestStatus )

        # add the bbhq sign
        top = self.geom.find("**/linktunnel_bosshq_10000_DNARoot")
        sign = top.find("**/Sign_5")
        sign.node().setEffect(DecalEffect.make())
        locator = top.find("**/sign_origin")
        signText = DirectGui.OnscreenText(
            text = TextEncoder.upper(TTLocalizer.BossbotHQ[-1]),
            font = ToontownGlobals.getSuitFont(),
            scale = TTLocalizer.GSZLbossbotSignScale,
            fg = (0, 0, 0, 1), 
            # required for DecalEffect (must be a GeomNode, not a TextNode)
            mayChange=False,
            parent = sign)
        signText.setPosHpr(locator, 0, 0, -0.3, 0, 0, 0)
        signText.setDepthWrite(0)
        
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
        if( self.enteringAGolfCourse( status ) and status.get( 'shardId' ) == None ):
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
        if( not status[ 'where' ] == 'golfcourse' ):
            return 0
        if( ZoneUtil.isDynamicZone( status[ 'zoneId' ] ) ):
            return status[ 'hoodId' ] == self.hood.hoodId
        else:
            return ZoneUtil.getHoodId( status[ 'zoneId' ] ) == self.hood.hoodId

    def enteringAGolfCourse( self, status ):
        if( not status[ 'where' ] == 'golfcourse' ):
            return 0
        if( ZoneUtil.isDynamicZone( status[ 'zoneId' ] ) ):
            return status[ 'hoodId' ] == self.hood.hoodId
        else:
            return ZoneUtil.getHoodId( status[ 'zoneId' ] ) == self.hood.hoodId        

    def enterGolfCourse( self, requestStatus ):
        """
        """

        # GolfCourse will grab this off of us
        if requestStatus.has_key('curseId'):
            self.golfCourseId = requestStatus[ 'courseId' ]
        else:
            self.golfCourseId = 0

        self.accept("raceOver",self.handleRaceOver)
        self.accept("leavingGolf", self.handleLeftGolf)

        base.transitions.irisOut(t=0.2)

    def exitGolfCourse( self ):
        """
        """
        del self.golfCourseId

    def handleRaceOver(self):
        print "you done!!"

    def handleLeftGolf(self):
        req={"loader":"safeZoneLoader","where":"playground","how":"teleportIn"
             ,"zoneId":17000,"hoodId":17000,"shardId":None}
        self.fsm.request("quietZone",[req])

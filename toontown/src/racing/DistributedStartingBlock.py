from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.building.ElevatorConstants import *
from toontown.building.ElevatorUtils import *
from toontown.building import DistributedElevatorExt
from toontown.building import DistributedElevator
from toontown.toonbase import ToontownGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.gui import DirectGui
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from direct.distributed import DistributedObject

from direct.distributed import DistributedSmoothNode

from direct.actor import Actor
from direct.fsm.FSM import FSM
from direct.showbase import PythonUtil
from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.racing.Kart import Kart
from toontown.racing.KartShopGlobals import KartGlobals
from toontown.racing import RaceGlobals
from toontown.toontowngui.TTDialog import TTGlobalDialog
from toontown.toontowngui.TeaserPanel import TeaserPanel

if( __debug__ ):
    import pdb

##########################################################################
# Temporary Class for Working with DistributedRacePad
# Modeling startblock after Pond->FishingSpot relationship so the
# startblocks can be placed via the level editor. Also going this route
# since kart viewing (Big Boy-esque) area will have more than 4 starting
# blocks and this can be changed easily in the level editor. Starting
# blocks will be props.
#
# Using temp class so that the current startingblock implementation isn't
# broken so that you can still get to the race instances.
##########################################################################
class DistributedStartingBlock( DistributedObject.DistributedObject, FSM ):
    """
    Purpose: MUST ADD COMMENTS HERE.
    """
    
    ######################################################################
    # Class Variables
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory( "DistributedStartingBlock" )

    sphereRadius = 1.5
    id = 0
    
    cameraPos = Point3(0, -23, 10)
    cameraHpr = Point3(0, -10, 0)
    
    SFX_BaseDir = "phase_6/audio/sfx/"
    SFX_KartAppear = SFX_BaseDir + "KART_Appear.mp3"

    defaultTransitions = { 'Off'        : [ 'EnterMovie' ],
                           'EnterMovie' : [ 'Off', 'Waiting', 'ExitMovie' ],
                           'Waiting'    : [ 'ExitMovie', 'Off' ],
                           'ExitMovie'  : [ 'Off', 'ExitMovie' ] }
    
    def __init__( self, cr ):
        """
        comment
        """
        
        # Initialize the Super Class
        DistributedObject.DistributedObject.__init__( self, cr )
        FSM.__init__( self, "staringBlock_%s_FSM" % ( DistributedStartingBlock.id ) )
        
        # Initialize Instance Variables
        self.avId = 0
        self.av = None
        self.lastAvId = 0
        self.avatar = None
        self.kartPad = None
        self.collNode = None
        self.movieNode = None
        self.movieTrack = None
        self.collSphere = None
        self.collNodePath = None
        self.localToonKarting = 0
        self.kartNode = None
        self.kart = None
        self.holeActor = None
        self.exitRequested = False

        if( __debug__ ):
            # FOR LOD TESTING - should really move this to a config_variable.
            self.testLOD = False
        
        self.id = DistributedStartingBlock.id
        DistributedStartingBlock.id += 1
        
    def disable( self ):
        """
        Comment
        """
        FSM.cleanup( self )
        #self.notify.debugStateCall( self )
        self.ignore( self.uniqueName( 'enterStartingBlockSphere' ) )
        self.ignore("stoppedAsleep")
        self.setOccupied( 0 )
        self.avId = 0
        self.nodePath.detachNode()
        self.kartPad = None
        if self.holeActor:
            self.holeActor.cleanup()
            self.holeActor = None
        
        # Call Super Class Disable Routine
        DistributedObject.DistributedObject.disable( self )
   
    def delete( self ):
        """
        comment
        """
        #self.notify.debugStateCall( self )
        #if( __debug__ ):
            #self.smiley.remove()
            #self.smiley2.remove()

        if( hasattr( self, 'dialog' ) ):
            if(not self.dialog.removed()):
                self.dialog.ignoreAll()
                if(not self.dialog.isEmpty()):
                    self.dialog.cleanup()
                del self.dialog

        self.finishMovie()

        if( hasattr( self, 'cancelButton' ) ):
            self.cancelButton.destroy()
            del self.cancelButton
            
        del self.kartPad
        if( self.nodePath ):
            self.nodePath.removeNode()
            del self.nodePath
   
        # Call Super Class Delete Method
        DistributedObject.DistributedObject.delete( self )
   
    def generateInit( self ):
        """
        comment
        """
        self.notify.debugStateCall( self )
        DistributedObject.DistributedObject.generateInit(self)
        
        # Create a NodePath to represent the spot itself. It gets
        # repositioned according to setPosHpr.
        self.nodePath = NodePath( self.uniqueName( 'StartingBlock' ) )
        
        # Make a collision sphere to detect when an avatar enters the
        # kart block.
        self.collSphere = CollisionSphere( 0, 0, 0, self.sphereRadius )
        
        # Make sure the sphere is intangible initially.
        self.collSphere.setTangible( 0 )
        self.collNode = CollisionNode( self.uniqueName( 'StartingBlockSphere' ) )
        self.collNode.setCollideMask( ToontownGlobals.WallBitmask )
        self.collNode.addSolid( self.collSphere )
        self.collNodePath = self.nodePath.attachNewNode( self.collNode )
        #self.collNodePath.show()
   
    def announceGenerate( self ):
        """
        Comment
        """
        self.notify.debugStateCall( self )
        DistributedObject.DistributedObject.announceGenerate(self)

        # The posHpr has been set at this point, thus reparent to render
        # and accept the collision sphere event.
        #if( __debug__ ):
        #    self.smiley = loader.loadModel( "models/misc/smiley" )
        #    self.smiley.setScale( 0.25 )
        #    self.smiley.setColorScale( 1, 0, 0, 1 )
        #    self.smiley.reparentTo( self.nodePath )
        self.nodePath.reparentTo( render )
        self.accept( self.uniqueName( 'enterStartingBlockSphere' ), self.__handleEnterSphere )

        if( __debug__ ):
            if self.testLOD:
                self.__generateKartAppearTrack()

    def setPadDoId( self, padDoId ):
        """
        comment
        """
        self.notify.debugStateCall( self )
        
        # Create Reference to Pad and add the block to the
        # Pad's references as well.
        self.kartPad = base.cr.doId2do.get( padDoId )
        self.kartPad.addStartingBlock( self )
   
    def setPosHpr( self, x, y, z, h, p, r ):
        """
        """
        self.notify.debugStateCall( self )
        
        self.nodePath.setPosHpr( x, y, z, h+180, 0, 0 )
 
    def setPadLocationId( self, padLocationId ):
        """
        """
        self.notify.debugStateCall( self )
        
        # Generate a new node on the nodepath.
        self.movieNode = self.nodePath.attachNewNode( self.uniqueName( 'MovieNode' ) )
        self.exitMovieNode = self.movieNode
           
        if( padLocationId % 2 ):
            # padLocation is on the right-side, thus the view node should
            # be placed on the right-side.
            self.movieNode.setPosHpr( 3.0, 0, 0, 90.0, 0, 0 )
             
        else:
            # otherwise its on the left-side.
            self.movieNode.setPosHpr( -3.0, 0, 0, -90.0, 0, 0 )

        #if( __debug__ ):
        #    self.smiley2 = loader.loadModel( "models/misc/smiley" )
        #    self.smiley2.setScale( 0.2 )
        #    self.smiley2.setColorScale( 0, 1, 0, 1 )
        #    self.smiley2.reparentTo( self.movieNode )
 
    def setActive( self, isTangible ):
        """
        Comment:
        """
        self.collSphere.setTangible( isTangible )
 
    def __handleEnterSphere( self, collEntry ):
        """
        comment
        """
        assert  self.notify.debug( "__handleEnterSphere" ) 
        
        # Protect against the same toon from re-entering the sphere
        # immediately after exiting. It is most likely a mistake on the
        # toon's part.
        if( base.localAvatar.doId == self.lastAvId and \
            globalClock.getFrameCount() <= self.lastFrame + 1 ):
            self.notify.debug( "Ignoring duplicate entry for avatar." )
            return
        
        # Only toons with hp > 0 and own a kart may enter the sphere.
        if( ( base.localAvatar.hp > 0 ) ):
            def handleEnterRequest( self = self ):
                self.ignore("stoppedAsleep")
                if hasattr(self.dialog, 'doneStatus') and (self.dialog.doneStatus == 'ok'):
                    self.d_requestEnter(base.cr.isPaid())
                else:
                    if self.cr and not self.isDisabled():
                        self.cr.playGame.getPlace().setState( "walk" )
                    else:
                        self.notify.warning("Warning! Object has already been disabled.")
                    
                self.dialog.ignoreAll()
                self.dialog.cleanup()
                del self.dialog
                
            # take the localToon out of walk mode
            self.cr.playGame.getPlace().fsm.request('stopped')

            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleEnterRequest)

            # A dialog box should prompt the toon for action, to either
            # enter a race or ignore it.
            doneEvent = 'enterRequest|dialog'
            if( self.kartPad.isPractice() ):
                msg = TTLocalizer.StartingBlock_EnterPractice
            else:
                raceName = TTLocalizer.KartRace_RaceNames[ self.kartPad.trackType ]
                numTickets = RaceGlobals.getEntryFee( self.kartPad.trackId, self.kartPad.trackType )
                msg = TTLocalizer.StartingBlock_EnterNonPractice % ( raceName, numTickets )

            self.dialog = TTGlobalDialog( msg, doneEvent, 4 )
            self.dialog.accept( doneEvent, handleEnterRequest )

            #self.d_requestEnter()
   
    ######################################################################
    # Distributed Methods
    ######################################################################
    def d_movieFinished( self ):
        """
        """
        self.notify.debugStateCall( self )
        self.sendUpdate( "movieFinished", [] )
        
    def d_requestEnter( self, paid ):
        """
        """
        self.notify.debugStateCall( self )
        self.sendUpdate( "requestEnter", [paid] )
        
    def d_requestExit( self ):
        """
        """
        self.notify.debugStateCall( self )
        self.exitRequested = True
        self.hideGui()
        self.sendUpdate( "requestExit", [] )
        
    def rejectEnter( self, errCode ):
        """
        """
        self.notify.debugStateCall( self )
        def handleTicketError( self = self ):
            self.ignore("stoppedAsleep")
            self.dialog.ignoreAll()
            self.dialog.cleanup()
            del self.dialog
            self.cr.playGame.getPlace().setState( "walk" )

        doneEvent = 'errorCode|dialog'
        if( errCode == KartGlobals.ERROR_CODE.eTickets ):
            msg = TTLocalizer.StartingBlock_NotEnoughTickets            
            self.dialog = TTGlobalDialog( msg, doneEvent, 2 )
            self.dialog.accept( doneEvent, handleTicketError )
            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleTicketError)
        elif( errCode == KartGlobals.ERROR_CODE.eBoardOver ):
            msg = TTLocalizer.StartingBlock_NoBoard
            self.dialog = TTGlobalDialog( msg, doneEvent, 2 )
            self.dialog.accept( doneEvent, handleTicketError ) 
            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleTicketError)
        elif( errCode == KartGlobals.ERROR_CODE.eNoKart ):
            msg = TTLocalizer.StartingBlock_NoKart
            self.dialog = TTGlobalDialog( msg, doneEvent, 2 )
            self.dialog.accept( doneEvent, handleTicketError )
            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleTicketError)
        elif( errCode == KartGlobals.ERROR_CODE.eOccupied ):
            msg = TTLocalizer.StartingBlock_Occupied
            self.dialog = TTGlobalDialog( msg, doneEvent, 2 )
            self.dialog.accept( doneEvent, handleTicketError )
            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleTicketError)
        elif( errCode == KartGlobals.ERROR_CODE.eTrackClosed ):
            msg = TTLocalizer.StartingBlock_TrackClosed
            self.dialog = TTGlobalDialog( msg, doneEvent, 2 )
            self.dialog.accept( doneEvent, handleTicketError )
            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleTicketError)
        elif( errCode == KartGlobals.ERROR_CODE.eUnpaid ):
            self.dialog = TeaserPanel( pageName="karting", doneFunc=handleTicketError )
        else:
            self.cr.playGame.getPlace().setState( "walk" )

    def finishMovie(self):
        if self.movieTrack:
            self.movieTrack.finish()
            self.movieTrack = None
            
    def setOccupied( self, avId ):
        """
        """
        
        self.notify.debug("%d setOccupied: %d" %(self.doId, avId))
        
        # Check if there is a current avatar in the spot.
        if( self.av != None ):

            # make sure any movies playing are done
            self.finishMovie()

            if( not self.av.isEmpty() and not self.av.isDisabled() ):
                self.av.loop( 'neutral' )
                self.av.setParent( ToontownGlobals.SPRender )
                self.av.startSmooth()
                
            # make sure any movies playing are done
            self.finishMovie()

            if self.kart:
                self.kart.delete()
                self.kart = None
                
            # remove the kart node
            if self.kartNode:
                self.kartNode.removeNode()
                self.kartNode = None
            
            self.placedAvatar = 0
            self.ignore( self.av.uniqueName( "disable" ) )
            self.av = None

        assert self.kart == None
            
        # Store avatar and frame information
        wasLocalToon = self.localToonKarting
        self.lastAvId = self.avId
        self.lastFrame = globalClock.getFrameCount()
        
        # Update new information
        self.avId = avId
        self.localToonKarting = 0
        
        if( self.avId == 0 ):
            # The Kart Block is now available.
            self.collSphere.setTangible( 0 )
            self.request( "Off" )
        else:
            # The Kart block is now occupied; no one else may be here.
            self.collSphere.setTangible( 1 )
            av = self.cr.doId2do.get( self.avId )
            self.placedAvatar = 0
            
            if( self.avId == base.localAvatar.doId ):
                self.localToonKarting = 1

            if( av != None ):
                self.av = av
                self.av.stopSmooth()
                self.placedAvatar = 0

                self.acceptOnce( self.av.uniqueName( "disable" ), self.__avatarGone )
                
                # Create a kart node
                self.kartNode = render.attachNewNode( self.av.uniqueName( 'KartNode' ) )
                self.kartNode.setPosHpr( self.nodePath.getPos( render ),
                                         self.nodePath.getHpr( render ) )

                # Create the kart
                assert self.kart == None
                self.kart = Kart()
                self.kart.baseScale = 1.6
                self.kart.setDNA( self.av.getKartDNA() )

                # Generate the actual kart.
                self.kart.generateKart()
                self.kart.resetGeomPos()

                # Parent the Avatar to the kart block.
                self.av.wrtReparentTo( self.nodePath )
                self.av.setAnimState( 'neutral', 1.0 )
                if not self.localToonKarting:
                        av.stopSmooth()
                        self.__placeAvatar()
                self.avParent = av.getParent()
            else:
                self.notify.warning( "Unknown avatar %d in kart block %d " % ( self.avId, self.doId ) )
                # make sure we don't try to play any movies here, but
                # let the next setOccupied (to 0 hopefully) reset
                # the starting block
                self.avId = 0
   
        # If the local toon was involved but is no longer, restore
        # walk mode.  We do this down here, after we have twiddled
        # with the tangible flag, so that the toon must walk out and
        # walk back in again in order to generate the enter event
        # again.
        if wasLocalToon and not self.localToonKarting:
            # Reset to walk mode, but not if we're exiting all the way
            # out (and our place is already gone).
            place = base.cr.playGame.getPlace()
            if place:
                # check to see if the toon requested the exit, or was booted
                if self.exitRequested:
                    place.setState('walk')
                else:
                    # the toon was booted off the block
                    def handleDialogOK( self = self ):
                        self.ignore("stoppedAsleep")
                        place.setState( "walk" )
                        self.dialog.ignoreAll()
                        self.dialog.cleanup()
                        del self.dialog

                    doneEvent = 'kickedOutDialog'
                    msg = TTLocalizer.StartingBlock_KickSoloRacer
                    self.dialog = TTGlobalDialog( msg, doneEvent, style = 1 )
                    self.dialog.accept( doneEvent, handleDialogOK )

                    # make dialog go away if they fall asleep while stopped
                    self.accept("stoppedAsleep", handleDialogOK)


    def __avatarGone( self ):
        self.notify.debugStateCall( self )
        
        # Called when the avatar in the kart block vanishes. The AI will
        # call setOccupied( 0 ) as well, but the client calls it first
        # just to be on the safe side, so that it doesn't try to access a
        # non-existent avatar.
        self.setOccupied( 0 )
        
    def __placeAvatar( self ):
        self.notify.debugStateCall( self )
        
        # Places the avatar at the Kart Block, mainly for the
        # benefit of those who did not observe the EnterMovie.
        if( not self.placedAvatar ):
            self.placedAvatar = 1
            self.av.setPosHpr( 0, 0, 0, 0, 0, 0 )
 
    def setMovie( self, mode ):
        """
        """
        self.notify.debugStateCall( self )
        if( self.avId == 0 ):
            return

        # make sure to finish any currently playing movie
        self.finishMovie()
        
        if( mode == 0 ):
            pass
        elif( mode == KartGlobals.ENTER_MOVIE ):
            self.request( "EnterMovie" )
        elif( mode == KartGlobals.EXIT_MOVIE ):
            self.request( "ExitMovie" )
        else:
            pass
        
    def makeGui( self ):
        self.notify.debugStateCall( self )
        
        # Check if the timer exists, if so then the gui has been
        # made.
        if( hasattr( self, 'cancelButton' ) ):
            return
        fishGui = loader.loadModel( "phase_4/models/gui/fishingGui" )
        self.cancelButton = DirectGui.DirectButton(
            relief = None,
            scale = (0.67),
            pos = (1.16,0,-0.9),
            #pos = (0,0,0),
            text = ("", TTLocalizer.FishingExit, TTLocalizer.FishingExit),
            text_align = TextNode.ACenter,
            text_fg = Vec4(1,1,1,1),
            text_shadow = Vec4(0,0,0,1),
            text_pos=(0.0, -0.12),
            textMayChange = 0,
            text_scale = 0.1,
            image = ( fishGui.find("**/exit_buttonUp") ,
                      fishGui.find("**/exit_buttonDown"),
                      fishGui.find("**/exit_buttonRollover") ),
            text_font = ToontownGlobals.getInterfaceFont(),
            command = self.d_requestExit,
            #pressEffect = False,
            )
        self.cancelButton.hide()
        

            
    def showGui( self ):
        """
        """
        self.notify.debugStateCall( self )

        # hack to make sure we don't show the exit button
        # during the 'WaitBoarding' state on race starting blocks
        if hasattr(self.kartPad, 'state'):
            if not self.kartPad.state == 'WaitCountdown':
                return
            
        self.cancelButton.show()
        
    def hideGui( self ):
        self.notify.debugStateCall( self )
        if( not hasattr( self, 'cancelButton' ) ):
            return
       
        self.cancelButton.hide()
 
    def generateToonMoveTrack( self ):
        """
        """
        hpr = self.movieNode.getHpr( render )
        heading = PythonUtil.fitDestAngle2Src( self.av.getH( render ), hpr[ 0 ] )
        hpr.setX( heading )
        
        self.av.setAnimState( 'run', 1.0 )
        toonTrack = Sequence(
            Wait( 0.5 ),
            Parallel( LerpPosInterval( self.av, 1.,
                                       Point3( self.movieNode.getX(self.avParent),
                                               self.movieNode.getY(self.avParent),
                                               0 )),
                                       #other = self.nodePath ),
                      LerpHprInterval( self.av, 1.,
                                       hpr = hpr,
                                       other = render ) ),
            Func( self.av.loop, 'neutral' ),
            )
        return toonTrack
 
    def generateKartAppearTrack( self ):
        """
        """
        if( not self.av ):
            # Obtain the toon's kart
            if not self.kartNode:
                self.kartNode = render.attachNewNode( str(self) + 'kartNode' )
                self.kartNode.setPosHpr( self.nodePath.getPos( render ), self.nodePath.getHpr( render ) )
            self.kart.setScale( 0.85 )
            self.kart.reparentTo( self.kartNode )
            return Parallel()
        
        self.kart.setScale( 0.1 )
        
        kartTrack = Parallel(
            Sequence( ActorInterval( self.av, "feedPet" ),
                      Func( self.av.loop, 'neutral' ) ),
            Sequence( Func( self.kart.setActiveShadow, False ),
                      Func( self.kart.reparentTo, self.av.rightHand ),
                      #Func( self.kart.setPos, .1, 0, .2 ),
                      Wait( 2.1 ),
                      Func( self.kart.wrtReparentTo, render ),
                      Func( self.kart.setShear, 0, 0, 0),
                      Parallel( LerpHprInterval( self.kart,
                                                 hpr = self.kartNode.getHpr( render ),
                                                 duration = 1.2 ),
                                ProjectileInterval( self.kart,
                                                    endPos = self.kartNode.getPos( render ),
                                                    duration = 1.2,
                                                    gravityMult = 0.45 ) ),
                      Wait( 0.2 ),
                      Func( self.kart.setActiveShadow, True ),
                      # Must be a cleaner way to do this.
                      Sequence( LerpScaleInterval( self.kart,
                                                   scale = Point3( 1.1, 1.1, .1),
                                                   duration = 0.2),
                                LerpScaleInterval( self.kart,
                                                   scale = Point3( .9, .9, .1 ),
                                                   duration = 0.1 ),
                                LerpScaleInterval( self.kart,
                                                   scale = Point3( 1., 1., .1 ),
                                                   duration = 0.1 ),
                                LerpScaleInterval( self.kart,
                                                   scale = Point3( 1., 1., 1.1 ),
                                                   duration = 0.2 ),
                                LerpScaleInterval( self.kart,
                                                   scale = Point3( 1., 1., .9 ),
                                                   duration = 0.1 ),
                                LerpScaleInterval( self.kart,
                                                   scale = Point3( 1., 1., 1. ),
                                                   duration = 0.1 ),
                                Func( self.kart.wrtReparentTo, self.kartNode ) ) ) )
        return kartTrack

    def generateToonJumpTrack( self ):
        """
        """
        # Maintain a reference to Parent and Scale of avatar in case they
        # exit from the kart.
        base.sb = self
        def getToonJumpTrack( av, kart ):

            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = kart.toonNode[0]):
                dest = node.getPos(av.getParent())
                return dest

            def getJumpHpr(av = av, node = kart.toonNode[0]):
                hpr = node.getHpr(av.getParent())
                return hpr
            
            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                   Wait( 0.43 ),
                   Parallel( LerpHprInterval( av,
                                              hpr = getJumpHpr,
                                              duration = .9 ),
                             ProjectileInterval( av,
                                                 endPos = getJumpDest,
                                                 duration = .9 )
                             ),
                   )
                )
            return toonJumpTrack

        def getToonSitTrack( av ):
            toonSitTrack = Sequence(

                ActorInterval( av, 'sit-start' ),
                Func( av.loop, 'sit' )
                )
            return toonSitTrack

        toonJumpTrack = getToonJumpTrack( self.av, self.kart )
        toonSitTrack = getToonSitTrack( self.av )
        
        jumpTrack = Sequence(
            Parallel(
                toonJumpTrack,
                Sequence( Wait(1),
                          toonSitTrack,
                          ),
                ),
            #Func( self.av.setPosHpr, 0, 0, 0, 0, 0, 0 ),
            Func( self.av.setPosHpr, 0, .45, -.25, 0, 0, 0 ),
            Func( self.av.reparentTo, self.kart.toonSeat ),
            #Func( self.av.setScale, self.kart.accGeomScale/self.kart.baseScale ),
            #toonSitTrack,
            #Func( self.av.wrtReparentTo, self.kart.rotateNode )
            )
        
        return jumpTrack
 
    def generateToonReverseJumpTrack( self ):
        """
        """
        def getToonJumpTrack( av, destNode ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = destNode):
                dest = node.getPos(av.getParent())
                return dest

            def getJumpHpr(av = av, node = destNode):
                hpr = node.getHpr(av.getParent())
                return hpr
            
            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                  Wait( 0.1), #43 ),
                  Parallel( LerpHprInterval( av,
                                             hpr = getJumpHpr,
                                             duration = .9 ),
                            ProjectileInterval( av,
                                                endPos = getJumpDest,
                                                duration = .9 ) )
                  )
                )  
            return toonJumpTrack

        toonJumpTrack = getToonJumpTrack( self.av, self.exitMovieNode )
        jumpTrack = Sequence(
            toonJumpTrack,
            Func( self.av.loop, 'neutral' ),
            Func( self.av.reparentTo, render ),
            Func( self.av.setPosHpr, self.exitMovieNode, 0,0,0,0,0,0 ),
            )
        return jumpTrack

    def generateCameraMoveTrack( self ):
        """
        """
        self.cPos = camera.getPos( self.av )
        self.cHpr = camera.getHpr( self.av )
        
        camera.wrtReparentTo( self.nodePath )
        cameraTrack = LerpPosHprInterval(
            camera, 1.5, self.cameraPos, self.cameraHpr )
        return cameraTrack

    def generateCameraReturnMoveTrack( self ):
        cameraTrack = Sequence(
            Func( camera.wrtReparentTo, self.av ),
            LerpPosHprInterval( camera,
                                1.5,
                                self.cPos,
                                self.cHpr ) )
        return cameraTrack
    
    def generateKartDisappearTrack( self ):
        def getHoleTrack( hole, holeParent ):
            holeTrack = Sequence(
                Wait( .2 ),
                Func( hole.setBin, 'shadow', 0 ),
                Func( hole.setDepthTest, 0 ),
                Func( hole.setDepthWrite, 0 ),
                Func( hole.reparentTo, holeParent ),
                Func( hole.setPos, holeParent, Point3( 0, 0.0, -.6 ) ),
                ActorInterval( hole, 'hole', startTime=3.4, endTime=3.1 ),
                Wait( 0.4 ),
                ActorInterval( hole, 'hole', startTime=3.1, endTime=3.4 ) )
            return holeTrack

        def getKartShrinkTrack( kart ):
            pos = kart.getPos()
            pos.addZ( -1. )
            kartTrack = Sequence(
                LerpScaleInterval( kart,
                                   scale = Point3( 1., 1., .9 ),
                                   duration = 0.1 ),
                LerpScaleInterval( kart,
                                   scale = Point3( 1., 1., 1.1 ),
                                   duration = 0.1 ),
                LerpScaleInterval( kart,
                                   scale = Point3( 1., 1., .1 ),
                                   duration = 0.2 ),
                LerpScaleInterval( kart,
                                   scale = Point3( .9, .9, .1 ),
                                   duration = 0.1 ),
                LerpScaleInterval( kart,
                                   scale = Point3( 1.1, 1.1, .1 ),
                                   duration = 0.1 ),
                LerpScaleInterval( kart,
                                   scale = Point3( .1, .1, .1 ),
                                   duration = 0.2 ),
                Wait( 0.2 ),
                LerpPosInterval( kart,
                                 pos = pos,
                                 duration = 0.2 ),
                Func( kart.hide ),
                )
            return kartTrack           

        if not self.holeActor:
            self.holeActor = Actor.Actor('phase_3.5/models/props/portal-mod',
                                         {'hole': 'phase_3.5/models/props/portal-chan'})
        holeTrack = getHoleTrack( self.holeActor, self.kartNode )
        shrinkTrack = getKartShrinkTrack( self.kart )
        
        kartTrack = Parallel(
            shrinkTrack,
            holeTrack )
            
        return kartTrack
    
    
    ######################################################################
    # State Transitions
    ######################################################################
    def enterOff( self ):
        """
        """
        self.notify.debug( "%d enterOff: Entering the Off State."  % self.doId)
        self.hideGui()
        
    def exitOff( self ):
        """
        """
        self.notify.debug( "%d exitOff: Exiting the Off State." % self.doId )
        
    def enterEnterMovie( self ):
        """
        """
        #pdb.set_trace()
        self.notify.debug( "%d enterEnterMovie: Entering the Enter Movie State." % self.doId)
        
        # Obtain the Enter Movie Tracks
        toonTrack = self.generateToonMoveTrack()
        kartTrack = self.generateKartAppearTrack()
        jumpTrack = self.generateToonJumpTrack()
        name = self.av.uniqueName( "EnterRaceTrack" )
        
        if( (self.av is not None) and ( self.localToonKarting ) ):    
            kartAppearSfx = base.loadSfx(self.SFX_KartAppear)
            cameraTrack = self.generateCameraMoveTrack()
            engineStartTrack = self.kart.generateEngineStartTrack()
            self.finishMovie()
            self.movieTrack = Sequence(
                Parallel( cameraTrack,
                          toonTrack,
                          ),
                Parallel(
                    SoundInterval(kartAppearSfx),
                    Sequence(
                        kartTrack,
                        jumpTrack,
                        engineStartTrack,
                        Func( self.makeGui ),
                        Func( self.showGui ),
                        Func( self.request, "Waiting" ),
                        Func( self.d_movieFinished )
                        ),
                    ),
                name = name,
                autoFinish = 1
                )
            self.exitRequested = False
        else:
            self.finishMovie()
            self.movieTrack = Sequence(
                toonTrack,
                kartTrack,
                jumpTrack,
                name = name,
                autoFinish = 1,
                )

        self.movieTrack.start()
 
    def exitEnterMovie( self ):
        """
        """
        self.notify.debug( "%d exitEnterMovie: Exiting the Enter Movie State." % self.doId )
        
    def enterWaiting( self ):
        """
        """
        self.notify.debug( "%d enterWaiting: Entering the Waiting State." % self.doId )
        
    def exitWaiting( self ):
        """
        """
        self.notify.debug( "%d exitWaiting: Exiting the Waiting State." % self.doId )

    def enterExitMovie( self ):
        """
        """
        self.notify.debug( "%d enterExitMovie: Entering the Exit Movie State." % self.doId )

        # this should be hidden by now... but just in case.
        self.hideGui()
        
        jumpTrack = self.generateToonReverseJumpTrack()
        kartTrack = self.generateKartDisappearTrack()
        self.finishMovie()
        self.movieTrack = Sequence( Func(self.kart.kartLoopSfx.stop),
                                    jumpTrack,
                                    kartTrack,
                                    name = self.av.uniqueName( "ExitRaceTrack" ),
                                    autoFinish = 1 )
        if( (self.av is not None) and ( self.localToonKarting ) ):
            cameraTrack = self.generateCameraReturnMoveTrack()
            self.movieTrack.append( cameraTrack )
            self.movieTrack.append( Func(self.d_movieFinished) )
            
        self.movieTrack.start()
   
    def exitExitMovie( self ):
        """
        """
        self.notify.debug( "%d exitExitMovie: Exiting the Exit Movie State." % self.doId )
        #Moved up to SetOccupied
        #CHECK: IS THIS OKAY?
        #self.kartNode.removeNode()
        #del self.kartNode
           

    def doExitToRaceTrack( self ):
        self.hideGui()
        self.finishMovie()
        
        # obtain old block position and the new position to move to.
        oldBlockPos = self.kartNode.getPos( render )
        self.kartNode.setPos( self.kartNode, 0, 40, 0 )
        newBlockPos = self.kartNode.getPos( render )
        oldBlockScale = self.kartNode.getScale()

        # up kart lod
        self.kart.LODnode.setSwitch( 0, 60, 0 )

        # Set the old pos back
        self.kartNode.setPos( render, oldBlockPos )

        blockLerpIval = LerpPosInterval( self.kartNode,
                                         pos = newBlockPos,
                                         duration = 2.0 )
        scaleLerpIval = LerpScaleInterval( self.kartNode,
                                           scale = oldBlockScale*.2,
                                           duration = 2.0 )
        engineStopTrack = self.kart.generateEngineStopTrack(2)
        
        self.finishMovie()
        self.movieTrack = Parallel()
        if( self.av == base.localAvatar ):
            # If we are the local avatar, then iris out.
            self.movieTrack.insert( 0, Func( base.transitions.irisOut, 1.5, 0 ) )
            self.movieTrack.append(engineStopTrack),
            taskMgr.doMethodLater(1.6, self.bulkLoad, "loadIt", extraArgs=[])

        self.movieTrack.append(
            Sequence(
                Parallel( blockLerpIval,
                          scaleLerpIval,
                          ),
                Func( self.kartNode.hide ),
                Func( self.kartNode.setPos, render, oldBlockPos ),
                Func( self.kartNode.setScale, oldBlockScale ),
            ))

        self.movieTrack.start()

    def bulkLoad(self):
        base.loader.beginBulkLoad("atRace", TTLocalizer.StartingBlock_Loading, 60, 1, TTLocalizer.TIP_KARTING)

class DistributedViewingBlock( DistributedStartingBlock ):
    """
    Derived from the starting block to provide specific movies for the
    Viewing pads.    """

    ######################################################################
    # Class Variables
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory( "DistributedViewingBlock" )
    #notify.setInfo(True)
    sphereRadius = 6

    #cameraPos = Point3(-23, 0, 10)
    #cameraHpr = Point3(90, -10, 0)

    def __init__( self, cr ):
        """
        Comment
        """

        # Initialize the Super Class
        DistributedStartingBlock.__init__( self, cr )

        # Initialize Instance Variables
        self.timer = None

    def delete( self ):
        """
        """

        if( self.timer is not None ):
            self.timer.destroy()
            del self.timer

        # Perform the Super Class Delete Call
        DistributedStartingBlock.delete( self )

    def generateInit( self ):
        """
        comment
        """
        self.notify.debugStateCall( self )
        # skip over DistributedStartingBlock, since this method is
        # a cut-and-paste of DistributedStartingBlock.generateInit
        DistributedObject.DistributedObject.generateInit(self)
        
        # Create a NodePath to represent the spot itself. It gets
        # repositioned according to setPosHpr.
        self.nodePath = NodePath( self.uniqueName( 'StartingBlock' ) )
        
        # Make a collision sphere to detect when an avatar enters the
        # kart block.
        self.collSphere = CollisionSphere( -1, 6.75, -1, self.sphereRadius )
        
        # Make sure the sphere is intangible initially.
        self.collSphere.setTangible( 0 )
        self.collNode = CollisionNode( self.uniqueName( 'StartingBlockSphere' ) )
        self.collNode.setCollideMask( ToontownGlobals.WallBitmask )
        self.collNode.addSolid( self.collSphere )
        self.collNodePath = self.nodePath.attachNewNode( self.collNode )

    def announceGenerate( self ):
        """
        Comment
        """
        self.notify.debugStateCall( self )
        # skip over DistributedStartingBlock, since this method is
        # a cut-and-paste of DistributedStartingBlock.announceGenerate
        DistributedObject.DistributedObject.announceGenerate(self)
        
        # The posHpr has been set at this point, thus reparent to render
        # and accept the collision sphere event.
        #if( __debug__ ):
        #    self.smiley = loader.loadModel( "models/misc/smiley" )
        #    self.smiley.setScale( 0.25 )
        #    self.smiley.setColorScale( 1, 0, 0, 1 )
        #    self.smiley.reparentTo( self.nodePath )
        self.nodePath.reparentTo( render )
        self.accept( self.uniqueName( 'enterStartingBlockSphere' ), self.__handleEnterSphere )

        if( __debug__ ):
            if self.testLOD:
                self.__generateKartAppearTrack()

    def setPadLocationId( self, padLocationId ):
        """
        Comment:
        """

        self.notify.debugStateCall( self )

        # Generate a new node on the nodepath.
        self.movieNode = self.nodePath.attachNewNode( self.uniqueName( 'MovieNode' ) )
        self.exitMovieNode = self.nodePath.attachNewNode( self.uniqueName( 'ExitMovieNode' ) )

        if( padLocationId %2 ):
            # padLocation is on the right-side, thus the view node should
            # be placed on the right-side.
            self.movieNode.setPosHpr( 0, 6.5, 0, 0, 0, 0 )
        else:
            # otherwise its on the left-side.
            self.movieNode.setPosHpr( 0, -6.5, 0, 0, 0, 0 )
            
        self.exitMovieNode.setPosHpr( 3, 6.5, 0, 270, 0, 0 )

        #if( __debug__ ):
        #    self.smiley3 = loader.loadModel( "models/misc/smiley" )
        #    self.smiley3.setScale( 0.2 )
        #    self.smiley3.setColorScale( 1, 1, 0, 1 )
        #    self.smiley3.reparentTo( self.exitMovieNode )
 
        #    self.smiley2 = loader.loadModel( "models/misc/smiley" )
        #    self.smiley2.setScale( 0.2 )
        #    self.smiley2.setColorScale( 0, 1, 0, 1 )
        #    self.smiley2.reparentTo( self.movieNode )

        self.collNodePath.reparentTo( self.movieNode )
        #if ( __debug__):
        #    self.collNodePath.show()

    def __handleEnterSphere( self, collEntry ):
        """
        comment
        """
        assert  self.notify.debug( "__handleEnterSphere" ) 
        
        # Protect against the same toon from re-entering the sphere
        # immediately after exiting. It is most likely a mistake on the
        # toon's part.
        if( base.localAvatar.doId == self.lastAvId and \
            globalClock.getFrameCount() <= self.lastFrame + 1 ):
            self.notify.debug( "Ignoring duplicate entry for avatar." )
            return
        
        # Only toons with hp > 0 and own a kart may enter the sphere.
        if( ( base.localAvatar.hp > 0 ) ):
            def handleEnterRequest( self = self ):
                self.ignore("stoppedAsleep")
                if hasattr(self.dialog, 'doneStatus') and (self.dialog.doneStatus == 'ok'):
                    self.d_requestEnter(base.cr.isPaid())
                else:
                    self.cr.playGame.getPlace().setState( "walk" )
                    
                self.dialog.ignoreAll()
                self.dialog.cleanup()
                del self.dialog
                
            # take the localToon out of walk mode
            self.cr.playGame.getPlace().fsm.request('stopped')

            # make dialog go away if they fall asleep while stopped
            self.accept("stoppedAsleep", handleEnterRequest)

            # A dialog box should prompt the toon for action, to either
            # enter a race or ignore it.
            doneEvent = 'enterRequest|dialog'
            msg = TTLocalizer.StartingBlock_EnterShowPad
            self.dialog = TTGlobalDialog( msg, doneEvent, 4 )
            self.dialog.accept( doneEvent, handleEnterRequest )

            #self.d_requestEnter()

    def generateCameraMoveTrack( self ):
        """
        """
        self.cPos = camera.getPos( self.av )
        self.cHpr = camera.getHpr( self.av )

        cameraPos = Point3(23, -10, 7)
        cameraHpr = Point3(65, -10, 0)
        
        camera.wrtReparentTo( self.nodePath )
        cameraTrack = LerpPosHprInterval(
            camera, 1.5, cameraPos, cameraHpr )
        return cameraTrack

    def makeGui( self ):
        self.notify.debugStateCall( self )

        if( self.timer is not None ):
            return

        # TEMPORARY TOONTOWN TIMER FOR TIME UNTIL RACE LAUNCH
        self.timer = ToontownTimer()
        self.timer.setScale( 0.3 )
        self.timer.setPos( 1.16, 0, -.73 )
        self.timer.hide()

        # Make Super Class GUI
        DistributedStartingBlock.makeGui( self )

    def showGui( self ):
        self.notify.debugStateCall( self )

        # Show Timer and Super class gui
        self.timer.show()
        DistributedStartingBlock.showGui( self )

    def hideGui( self ):
        self.notify.debugStateCall( self )

        if( not hasattr( self, "timer" ) or self.timer is None ):
            return

        self.timer.reset()
        self.timer.hide()

        DistributedStartingBlock.hideGui( self )

    def countdown( self ):
        countdownTime = KartGlobals.COUNTDOWN_TIME - globalClockDelta.localElapsedTime( self.kartPad.getTimestamp( self.avId ) )
        self.timer.countdown( countdownTime )

    def enterEnterMovie( self ):
        """
        """
        #pdb.set_trace()
        self.notify.debug( "%d enterEnterMovie: Entering the Enter Movie State." % self.doId )
        
        # Obtain the toon's kart.
        pos = self.nodePath.getPos( render )
        hpr = self.nodePath.getHpr( render )

        pos.addZ( 1.7) #1.5 )
        hpr.addX(270)
        self.kartNode.setPosHpr( pos, hpr )
        
        # Obtain the Enter Movie Tracks
        toonTrack = self.generateToonMoveTrack()
        kartTrack = self.generateKartAppearTrack()
        jumpTrack = self.generateToonJumpTrack()
        name = self.av.uniqueName( "EnterRaceTrack" )
        
        if( (self.av is not None) and ( self.localToonKarting ) ):    
            cameraTrack = self.generateCameraMoveTrack()
            self.finishMovie()
            self.movieTrack = Sequence(
                Parallel( cameraTrack,
                          Sequence(),
                          ),
                kartTrack,
                jumpTrack,
                Func( self.makeGui ),
                Func( self.showGui ),
                Func( self.countdown ),
                Func( self.request, "Waiting" ),
                Func( self.d_movieFinished ),
                name = name,
                autoFinish = 1
                )
        else:
            self.finishMovie()
            self.movieTrack = Sequence(
                toonTrack,
                kartTrack,
                jumpTrack,
                name = name,
                autoFinish = 1,
                )

        self.movieTrack.start()

        # never show the dialog on viewing pads
        self.exitRequested = True
 

    


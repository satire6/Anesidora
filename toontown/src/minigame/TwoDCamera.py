"""TwoDCamera module: contains the TwoDCamera class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.minigame import ToonBlitzGlobals
import math

class TwoDCamera(DistributedObject.DistributedObject):
    """The TwoDCamera class controls the camera for a 2D Scroller game.
       The constructor takes a camera and it controls that camera."""
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDCamera')
    
    def __init__(self, camera):
        self.notify.debug('Constructing TwoDCamera with %s' %camera)
        self.camera = camera        
        self.cameraSideView = ToonBlitzGlobals.CameraStartingPosition
        self.threeQuarterOffset = 2
        self.changeFacingInterval = None
        self.ivalControllingCamera = False
        self.accept('avatarOrientationChanged', self.setupChangeFacingInterval)

    def onstage(self):
        self.camera.reparentTo(render)
        p = self.cameraSideView
        self.camera.setPosHpr(render, p[0], p[1], p[2], p[3], p[4], p[5])
        self.camera.setX(render, base.localAvatar.getX(render) + self.threeQuarterOffset)
        
    def destroy(self):
        self.ignore('avatarOrientationChanged')
        p = self.cameraSideView
        self.camera.setPosHpr(render, p[0], p[1], p[2], p[3], p[4], p[5])
        
    def update(self):
        """
        This function is called every frame in the local toon task.
        This function handles setting the the camera to the correct position 
        during the game.
        Set the camera to the 3/4 position and move it if the toon's heading changes.
        Control the camera only if the camera interval is not controlling it already.
        When the avatar changes its facing,the camera interval controls the camera 
        to place on a new three-quarter position.
        """
        if not self.ivalControllingCamera:
            camX = base.localAvatar.getX(render) - (math.sin(base.localAvatar.getH(render) * math.pi/180) * self.threeQuarterOffset)
            self.camera.setX(render, camX)
    
    def clearChangeFacingInterval(self):
        """Cleanup the toon change facing interval."""
        if self.changeFacingInterval:
            self.changeFacingInterval.pause()
            del self.changeFacingInterval
        self.changeFacingInterval = None

    def setupChangeFacingInterval(self, newHeading):
        """
        Start an interval that quickly pans the camera when he changes facing.
        Call this function only when you are sure that the toon is changing the facing.
        """
        self.clearChangeFacingInterval()
        self.newHeading = newHeading
        self.changeFacingInterval = LerpFunc(self.myLerpPos, duration = 5.0)#, blendType = 'easeOut')        
        self.changeFacingInterval.start()
        
    def myLerpPos(self, t):
        """
        This is used instead of a regular LerpPosInterval because if I use a 
        regular LerpPosInterval the camera jerks when the interval gives up 
        control of the camera.
        """
        self.ivalControllingCamera = True
        finalCamX = base.localAvatar.getX(render) - (math.sin(self.newHeading * math.pi/180) * self.threeQuarterOffset)
        diffX = finalCamX - self.camera.getX(render)            
        self.camera.setX(render, self.camera.getX(render) + diffX * t)
                
        if (math.fabs(self.camera.getX(render) - finalCamX) < 0.01): # In order to avoid floating point error
            self.notify.debug('giving up camera control')
            self.camera.setX(render, finalCamX)
            self.ivalControllingCamera = False
            self.clearChangeFacingInterval()
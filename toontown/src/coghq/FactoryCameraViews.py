from pandac.PandaModules import *
from direct.showbase.PythonUtil import Functor
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal

class FactoryCameraViews:
    notify = DirectNotifyGlobal.directNotify.newCategory('FactoryCameraViews')

    def __init__(self, factory):
        self.factory = factory
        # add a few useful views for the factory
        av = base.localAvatar

        self.currentCamPos = None

        self.views = [["signatureRoomView",
                       # Look down at the signature room from the button balcony
                       (Point3(0.,-14.8419799805,13.212685585), # pos
                        Point3(0.,-13.9563484192,12.749215126), # fwd
                        Point3(0.0,1.5,15.75),                  # up
                        Point3(0.0,1.5,-3.9375),                # down
                        1),
                       ["localToonLeftBattle"],  # regenerate view on battle done
                       ],
                      ["lookoutTrigger",
                       # Look at the whole signature room from the lookout balcony
                       (Point3(0,-17.7,28.8), # pos
                        Point3(0,10,0), # fwd
                        Point3(0.0,1.5,15.75),                  # up
                        Point3(0.0,1.5,-3.9375),                # down
                        1),
                       [],
                       ],
                      ["moleFieldView",
                       # Look at a bigger portion of mole field 
                       (Point3(0,-17.7,28.8), # pos
                        Point3(0,10,0), # fwd
                        Point3(0.0,1.5,15.75),                  # up
                        Point3(0.0,1.5,-3.9375),                # down
                        1),
                       [],
                       ],
                      ]
        
        camHeight = av.getClampedAvatarHeight()

        for i in range(len(self.views)):
            camPos = self.views[i][1]
            av.auxCameraPositions.append(camPos)
            factory.accept("enter" + self.views[i][0],
                           Functor(self.switchCamPos, i))
            # camera can also switch specified events
            for msg in self.views[i][2]:
                factory.accept(msg, self.checkCamPos)
            
        
    def delete(self):
        # stop listening for enter/exit events
        for i in range(len(self.views)):
            base.localAvatar.auxCameraPositions.remove(self.views[i][1])
            self.factory.ignore("enter" + self.views[i][0])
            self.factory.ignore("exit" + self.views[i][0])
            for msg in self.views[i][2]:
                self.factory.ignore(msg)
        # reset the camera position
        base.localAvatar.resetCameraPosition()

        del self.views

    def switchCamPos(self, viewIndex, colEntry=None):
        # switch to old view when done
        av = base.localAvatar
        prevView = av.cameraIndex

        self.currentCamPos = viewIndex
        
        # listen for exit event
        av.accept("exit" + self.views[viewIndex][0],
                  Functor(self.prevCamPos, prevView))

        self.notify.info('auto-switching to camera position %s' % viewIndex)
        av.setCameraSettings(self.views[viewIndex][1])
        
    def prevCamPos(self, index, colEntry=None):
        av = base.localAvatar
        if len(av.cameraPositions) > index:
            av.setCameraPositionByIndex(index)

        self.currentCamPos = None

    def checkCamPos(self):
        # Sets the camera position if it should be set.
        if self.currentCamPos != None:
            av = base.localAvatar
            viewIndex = self.currentCamPos
            self.notify.info('returning to camera position %s' % viewIndex)
            av.setCameraSettings(self.views[viewIndex][1])
            


from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShadowPlacer import ShadowPlacer
from otp.otpbase import OTPGlobals

# This global variable will be set true or false according to whether
# all avatar's drop shadows should be made visible, by the
# TimeOfDayManager (which currently manages projected shadows).
# Always change its state via this function, instead of monkeying with
# it directly.
globalDropShadowFlag = 1
def setGlobalDropShadowFlag(flag):
    global globalDropShadowFlag
    if flag != globalDropShadowFlag:
        globalDropShadowFlag = flag
        messenger.send('globalDropShadowFlagChanged')

# A similar trick to control the global gray level of the drop shadows.
globalDropShadowGrayLevel = 0.5
def setGlobalDropShadowGrayLevel(grayLevel):
    global globalDropShadowGrayLevel
    if grayLevel != globalDropShadowGrayLevel:
        globalDropShadowGrayLevel = grayLevel
        messenger.send('globalDropShadowGrayLevelChanged')

# I made this inherit from DirectObject so that non-distributed things can cast shadows

class ShadowCaster: 

    notify = DirectNotifyGlobal.directNotify.newCategory("ShadowCaster")
    #notify.setDebug(1)
    
    def __init__(self, squareShadow = False):
        assert self.notify.debugStateCall(self)
        # some shadow initialization stuff
        if squareShadow:
            self.shadowFileName = "phase_3/models/props/square_drop_shadow"
        else:
            self.shadowFileName = "phase_3/models/props/drop_shadow"

        self.dropShadow = None
        self.shadowPlacer = None
        self.activeShadow = 0
        self.wantsActive = 1
        self.storedActiveState = 0

        # Only create these hooks if we're running a game that cares
        # about them.
        if hasattr(base,"wantDynamicShadows") and base.wantDynamicShadows:
            messenger.accept('globalDropShadowFlagChanged', self, self.__globalDropShadowFlagChanged)
            messenger.accept('globalDropShadowGrayLevelChanged', self, self.__globalDropShadowGrayLevelChanged)

    def delete(self):
        assert self.notify.debugStateCall(self)

        # Only remove these hooks if we're running a game that cares
        # about them.
        if hasattr(base,"wantDynamicShadows") and base.wantDynamicShadows:
            messenger.ignore('globalDropShadowFlagChanged', self)
            messenger.ignore('globalDropShadowGrayLevelChanged', self)
        self.deleteDropShadow()
        self.shadowJoint = None

    def initializeDropShadow(self, hasGeomNode=True):
        """
        Load up and arrange the drop shadow
        """
        assert self.notify.debugStateCall(self)
        # First, protect this function from being called twice by
        # removing the old ones first.
        self.deleteDropShadow()

        # This will be used by the shadow system to identify things
        # that might want to have projected shadows drawn.
        if hasGeomNode:
            self.getGeomNode().setTag('cam', 'caster')

        # make the object float above the shadow slightly
        # not necessarily a good idea for all avatars
        #self.getGeomNode().setZ(0.025)

        # load and prep the drop shadow
        dropShadow = loader.loadModel(self.shadowFileName)
        dropShadow.setScale(0.4) # Slightly smaller to compensate for billboard
        
        dropShadow.flattenMedium()
        dropShadow.setBillboardAxis(2) # slide the shadow towards the camera
        dropShadow.setColor(0.0, 0.0, 0.0, globalDropShadowGrayLevel, 1) # override of 1 to prevent avatar.setColor() from affecting shadows.
        self.shadowPlacer = ShadowPlacer(
            base.shadowTrav, dropShadow,
            OTPGlobals.WallBitmask, OTPGlobals.FloorBitmask)
        self.dropShadow = dropShadow
        if not globalDropShadowFlag:
            self.dropShadow.hide()
        if self.getShadowJoint():
            dropShadow.reparentTo(self.getShadowJoint())
        else:
            self.dropShadow.hide()
        
        # Set the state of the shadow placers (in case someone set the
        # value before now):
        self.setActiveShadow(self.wantsActive)
        
        self.__globalDropShadowFlagChanged()
        self.__globalDropShadowGrayLevelChanged()

    def update(self):
        """This method is meant to be overriden."""
        # Toontown doesn't have self.update() for all shadowcasters
        # but initializeDropShadow calls it, so this prevents a crash.
        pass

    def deleteDropShadow(self):
        """
        Lose the drop shadows
        """
        assert self.notify.debugStateCall(self)
        if self.shadowPlacer:
            self.shadowPlacer.delete()
            self.shadowPlacer = None

        if self.dropShadow:
            self.dropShadow.removeNode()
            self.dropShadow = None

    def setActiveShadow(self, isActive=1):
        """
        Turn the shadow placement on or off.
        """
        assert self.notify.debugStateCall(self)

        isActive = isActive and self.wantsActive
        if(not globalDropShadowFlag):
            self.storedActiveState = isActive
        # changed logic to prevent crash (test remark 13203) - grw
        if self.shadowPlacer != None:
            isActive = isActive and globalDropShadowFlag
            if self.activeShadow != isActive:
                self.activeShadow = isActive
                if isActive:
                    self.shadowPlacer.on()
                else:
                    self.shadowPlacer.off()


    def setShadowHeight(self, shadowHeight):
        """
        Places the shadow at a particular height below the avatar (in
        effect, asserting that the avatar is shadowHeight feet above
        the ground).

        This is only useful when the active shadow is disabled via
        setActiveShadow(0).
        """
        assert self.notify.debugStateCall(self)
        if self.dropShadow:
            self.dropShadow.setZ(-shadowHeight)

    def getShadowJoint(self):
        assert self.notify.debugStateCall(self)
        if hasattr(self, "shadowJoint"):
            return self.shadowJoint
        shadowJoint = self.find('**/attachShadow')
        if shadowJoint.isEmpty():
            # We make a fresh NodePath that refers to the same node as
            # self, rather than assigning self directly--this will
            # prevent a cyclic Python reference.
            self.shadowJoint = NodePath(self)
        else:
            self.shadowJoint = shadowJoint
        return self.shadowJoint

    def hideShadow(self):
        assert self.notify.debugStateCall(self)
        self.dropShadow.hide()

    def showShadow(self):
        assert self.notify.debugStateCall(self)
        if not globalDropShadowFlag:
            self.dropShadow.hide()
        else:
            self.dropShadow.show()
    
    def __globalDropShadowFlagChanged(self):
        if (self.dropShadow != None):
            if(globalDropShadowFlag == 0):
                if(self.activeShadow == 1):
                    self.storedActiveState = 1
                    self.setActiveShadow(0)
            elif(self.activeShadow == 0):
                self.setActiveShadow(1)
            self.showShadow()
            
    def __globalDropShadowGrayLevelChanged(self):
        if (self.dropShadow != None):
            self.dropShadow.setColor(0.0, 0.0, 0.0, globalDropShadowGrayLevel, 1)

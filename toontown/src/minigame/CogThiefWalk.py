"""CofThiefWalk state module: contains the walk state which is used by
   Cog Thief minigame."""

from toontown.safezone import Walk

class CogThiefWalk(Walk.Walk):
    """Walk state class"""

    # create a notify category
    notify = directNotify.newCategory("CogThiefWalk")

    def __init__(self, doneEvent):
        """__init__(self, string)
        Walk state constructor
        """
        Walk.Walk.__init__(self, doneEvent)


    def enter(self, slowWalk = 0):
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.startBlink()
        #base.localAvatar.attachCamera()
        # this must be called *after* attachCamera()
        #base.localAvatar.startUpdateSmartCamera()
        #base.localAvatar.setNameVisible(0)
        base.localAvatar.showName()
        base.localAvatar.collisionsOn()
        base.localAvatar.startGlitchKiller()
        base.localAvatar.enableAvatarControls()
        
    def exit(self):
        # Go to our final state explicitly
        self.fsm.request('off')
        self.ignore("control")
        base.localAvatar.disableAvatarControls()
        #base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.stopBlink()
        #base.localAvatar.detachCamera()
        base.localAvatar.stopGlitchKiller()
        base.localAvatar.collisionsOff()
        base.localAvatar.controlManager.placeOnFloor()

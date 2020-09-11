"""FactoryLevelMgr module: contains the FactoryLevelMgr class"""

from otp.level import LevelMgr
import FactoryUtil
from direct.showbase.PythonUtil import Functor
from toontown.toonbase import ToontownGlobals

class FactoryLevelMgr(LevelMgr.LevelMgr):
    """This class manages editable factory attributes"""
    InterestingLocations = [
        (
        # double staircase
        ((-866, -272, -40), -101),
        # stomper room
        ((-662, -242, 7.5), 0),
        # warehouse
        ((-20, -180, 20), 0),
        # left elevator
        ((-249, 258, 111), 0),
        # right elevator
        ((318, 241, 115), -16),
        # vista view of factory from left elevator
        ((-251, 241, 109), -180),
        # top of right silo
        ((296, 292, 703), 56),
        # platform jumping room
        ((-740, 122, 28), 90),
        # paint mixer room
        ((210, -270, 38), -90),
        ),
        (
        ((20,21,0),0),
        ((3,404,39),-16),
        ((-496,358,5),0),
        ),
        ]

    def __init__(self, level, entId):
        LevelMgr.LevelMgr.__init__(self, level, entId)

        if base.config.GetBool('want-factory-lifter', 0):
            self.toonLifter = FactoryUtil.ToonLifter('f3')

        if __debug__:
            """
            # interesting places
            self.ipPlacer = FactoryUtil.CyclePlacer(
                FactoryLevelMgr.InterestingLocations[self.level.factoryId],
                'f4-up')
                """

            # ouch button
            self.ouchButton = FactoryUtil.Ouch('f6',
                                               Functor(self.level.b_setOuch,3))

        self.callSetters('farPlaneDistance')
        self.geom.reparentTo(render)

        # Render the semi-transparent oil room floor early, before various other game objects.
        # Otherwise shadows and traps won't draw on this floor.
        oilRoomOil = self.geom.find("**/oilroom/room/geometry_oilroom/*oil")
        oilRoomFloor = self.geom.find("**/oilroom/room/geometry_oilroom/*platform")
        if oilRoomOil and not oilRoomOil.isEmpty() and oilRoomFloor and not oilRoomFloor.isEmpty():
            oilRoomOil.setBin("background", 10)
            oilRoomFloor.setBin("background", 11)

    def destroy(self):
        if __debug__:
            #self.ipPlacer.destroy()
            #del self.ipPlacer
            self.ouchButton.destroy()
            del self.ouchButton
                
        if hasattr(self, 'toonLifter'):
            self.toonLifter.destroy()
            del self.toonLifter

        LevelMgr.LevelMgr.destroy(self)

    def setFarPlaneDistance(self, farPlaneDistance):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear,
                                farPlaneDistance)

    if __dev__:
        def setWantDoors(self, wantDoors):
            self.wantDoors = wantDoors
            messenger.send('wantDoorsChanged')

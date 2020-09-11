""" DistributedSuitPlannerAI module:  contains the SuitPlannerAI class which
    handles management of all suits within a single neighborhood."""

from pandac.PandaModules import *
from direct.distributed import DistributedObject
import SuitPlannerBase
from toontown.toonbase import ToontownGlobals

class DistributedSuitPlanner( DistributedObject.DistributedObject,
                              SuitPlannerBase.SuitPlannerBase ):
    """
    /////////////////////////////////////////////////////////////////////////
    //
    // SuitPlanner class:  The client side version of the suit planner.
    //                     This version has less functionality than the
    //                     server side, but some functionality is common
    //                     between the two
    // Attributes:
    //
    /////////////////////////////////////////////////////////////////////////
    """

    def __init__( self, cr ):

        # initialize some values that we will be using
        #
        DistributedObject.DistributedObject.__init__( self, cr )
        SuitPlannerBase.SuitPlannerBase.__init__( self )
        self.suitList = []
        self.buildingList = [0, 0, 0, 0]
        self.pathViz = None
        return None

    def generate( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject is
        //              reintroduced to the world, either for the first
        //              time or from the cache.
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.notify.info("DistributedSuitPlanner %d: generating" %
                         self.getDoId())
        DistributedObject.DistributedObject.generate( self )
        # register with the cr
        base.cr.currSuitPlanner = self

    def disable( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject is
        //              removed to the world
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.notify.info("DistributedSuitPlanner %d: disabling" %
                         self.getDoId())
        self.hidePaths()
        DistributedObject.DistributedObject.disable( self )
        # unregister with the cr
        base.cr.currSuitPlanner = None


    #
    # the following functions let client objects query the state of the suit world
    #
    
    def d_suitListQuery(self):
        self.sendUpdate('suitListQuery')

    def suitListResponse(self, suitList):
        self.suitList = suitList
        # let anyone know that might care
        messenger.send('suitListResponse')

    def d_buildingListQuery(self):
        self.sendUpdate('buildingListQuery')
        
    def buildingListResponse(self, buildingList):
        self.buildingList = buildingList
        # let anyone know that might care
        messenger.send('buildingListResponse')

    def hidePaths(self):
        # Hides the visualization created by a previous call to
        # showPaths(), below.
        if self.pathViz:
            self.pathViz.detachNode()
            self.pathViz = None
    
    def showPaths(self):
        # Draw a visualization of the suit paths at runtime for the
        # user's convenience.
        
        self.hidePaths()
        vizNode = GeomNode(self.uniqueName('PathViz'))
        lines = LineSegs()
        self.pathViz = render.attachNewNode(vizNode)
        points = self.frontdoorPointList + self.sidedoorPointList + self.cogHQDoorPointList + self.streetPointList
        while len(points) > 0:
            self.__doShowPoints(vizNode, lines, None, points)

        # Also create an unused collision sphere to show each battle
        # cell.
        cnode = CollisionNode('battleCells')
        cnode.setCollideMask(BitMask32.allOff())
        for zoneId, cellPos in self.battlePosDict.items():
            cnode.addSolid(CollisionSphere(cellPos, 9))

            text = "%s" % (zoneId)
            self.__makePathVizText(text, cellPos[0], cellPos[1], cellPos[2] + 9,
                                   (1, 1, 1, 1))

        self.pathViz.attachNewNode(cnode).show()

    def __doShowPoints(self, vizNode, lines, p, points):
        if p == None:
            # Choose a new point at random.  We arbitrarily take the
            # last one on the list.
            pi = len(points) - 1
            if pi < 0:
                return
            p = points[pi]
            del points[pi]
        else:
            # Remove the indicated point from the list.
            if p not in points:
                # We've already visited this point, and presumably
                # already drawn the edge.
                return
            
            pi = points.index(p)
            del points[pi]

        # Draw a label for the point.
        text = "%s" % (p.getIndex())
        pos = p.getPos()

        if (p.getPointType() == DNASuitPoint.FRONTDOORPOINT):
            color = (1, 0, 0, 1)            
        elif (p.getPointType() == DNASuitPoint.SIDEDOORPOINT):
            color = (0, 0, 1, 1)            
        else:
            color = (0, 1, 0, 1)            

        self.__makePathVizText(text, pos[0], pos[1], pos[2], color)

        # Draw a line to each connected point, and recurse.
        adjacent = self.dnaStore.getAdjacentPoints(p)
        numPoints = adjacent.getNumPoints()
        for i in range(numPoints):
            qi = adjacent.getPointIndex(i)
            q = self.dnaStore.getSuitPointWithIndex(qi)

            pp = p.getPos()
            qp = q.getPos()

            # Get an intermediate point between p and q.
            v = Vec3(qp - pp)
            v.normalize()
            c = v.cross(Vec3.up())
            p1a = pp + v * 2 + c * 0.5
            p1b = pp + v * 3
            p1c = pp + v * 2 - c * 0.5
            
            lines.reset()
            lines.moveTo(pp)
            lines.drawTo(qp)

            # Draw an arrowhead showing direction of travel.
            lines.moveTo(p1a)
            lines.drawTo(p1b)
            lines.drawTo(p1c)
            
            lines.create(vizNode, 0)
            self.__doShowPoints(vizNode, lines, q, points)

    def __makePathVizText(self, text, x, y, z, color):
        if not hasattr(self, "debugTextNode"):
            self.debugTextNode = TextNode('debugTextNode')
            self.debugTextNode.setAlign(TextNode.ACenter)
            self.debugTextNode.setFont(ToontownGlobals.getSignFont())
        self.debugTextNode.setTextColor(*color)
        self.debugTextNode.setText(text)
        np = self.pathViz.attachNewNode(self.debugTextNode.generate())
        np.setPos(x, y, z + 1)
        np.setScale(1.0)
        np.setBillboardPointEye(2)

        # Use MDual transparency so we can read the numbers through a
        # semitransparent bubble (e.g. a battle bubble)
        np.node().setAttrib(TransparencyAttrib.make(TransparencyAttrib.MDual), 2)

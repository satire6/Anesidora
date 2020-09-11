import math
import direct

from pandac.PandaModules import BitMask32
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import CollisionTraverser

from otp.otpbase import OTPGlobals

from otp.navigation.NavUtil import QuadTree


class AreaMapper(object):
    def __init__(self,environment):
        '''
        Create a map of the free space in a given area.
        '''
        self.csRadius = 1
        self.csHeight = 2
        self.avatarRadius = 1.4
        self.cs = CollisionSphere(0,0,0,1)

        self.csNode = CollisionNode("AreaMapperCollisionSphere")
        self.csNode.setFromCollideMask(OTPGlobals.WallBitmask)
        self.csNode.setIntoCollideMask(BitMask32.allOff())
        self.csNode.addSolid(self.cs)

        self.environment = environment

        self.csNodePath = self.environment.getTop().attachNewNode(self.csNode)

        self.floorRay = CollisionRay()
        self.floorRay.setDirection(0,0,-1)
        self.floorRay.setOrigin(0,0,0)

        self.floorRayNode = CollisionNode("AreaMapperFloorRay")
        self.floorRayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
        self.floorRayNode.setIntoCollideMask(BitMask32.allOff())
        self.floorRayNode.addSolid(self.floorRay)

        self.floorRayNodePath = self.environment.getTop().attachNewNode(self.floorRayNode)

        self.chq = CollisionHandlerQueue()
        self.traverser = CollisionTraverser()

        self.startX = 0
        self.startY = 0
        self.startZ = 0

        self.frontierSquares = {(0,0):1}
        self.frontierSquaresQueue = [(0,0)]
        self.walkableSquares = {(0,0):1}
        self.blockedSquares = {}

        self.setSquareSize(2)
        self.startAtPlayerSpawn()

        self.visGeom = None
        self.visGN = None
        self.visNodePath = None

        self.triVertexLookup = {}
        self.triList = []

        self.minX = 500
        self.maxX = -500
        self.minY = 500
        self.maxY = -500

        self.quadTree = QuadTree(width=1024)
        self.squares = []

        self.runDiscovery(100000)

        self._subdivide()

        #self._fixZValues()

        self.csNodePath.removeNode()
        self.floorRayNodePath.removeNode()
        

##     def _unstashEnvironment(self):
##         # Would be nice if we could just do this  :(
##         #for np in self.environment.findAllMatches("**/+CollisionNode;+s"):
##         #    np.unstash()
##         b = self.environment.builder
##         for s in b.sections.values():
##             s.unstash()
##         for o in b.largeObjects.values():
##             o.unstash()

    def setStart(self,x,y):
        self.startX = x
        self.startY = y
        self.startZ = self.findFloor(x,y)

    def startAtLocalAvatar(self):
        startPos = localAvatar.getPos(self.environment)
        self.setStart(startPos.getX(),startPos.getY())

    def startAtPlayerSpawn(self):
        # XXX Bleugh, this is really pirates-specific.  Nasty.
        for spawnPt in self.environment.world.getAllPlayerSpawnPts():
            parentDoId = self.environment.world.uidMgr.getDoId(spawnPt[1])
            if parentDoId == self.environment.doId:
                # Sweet, we found a spawn point for this grid's gamearea.  Use it!

                z = self.findFloor(spawnPt[0][0], spawnPt[0][1])
                if not self.isSphereBlocked(spawnPt[0][0], spawnPt[0][1], z):
                    self.setStart(spawnPt[0][0], spawnPt[0][1])
                    return

        raise "No player spawn points found for the given game area!  D:"


    def setSquareSize(self,size):
        self.squareSize = size
        self.csRadius = math.sqrt(2*(self.squareSize*self.squareSize/4)) + self.avatarRadius
        self.csNodePath.setScale(self.environment,self.csRadius,self.csRadius,self.csRadius)
        self.csHeight = self.csRadius*2


    def findFloor(self,x,y):
        self.floorRayNodePath.setPos(self.environment,x,y,50000)

        self.chq.clearEntries()

        self.traverser.clearColliders()
        self.traverser.addCollider(self.floorRayNodePath, self.chq)
        self.traverser.traverse(self.environment)

        highestZ = -50000

        for e in self.chq.getEntries():
            assert e.hasInto()
            assert e.getInto().isTangible()
            assert e.hasSurfacePoint()

            z = e.getSurfacePoint(self.environment).getZ()

            if z > highestZ:
                highestZ = z

        return highestZ
    

    def isSphereBlocked(self,x,y,z):
        if z < self.csHeight:
            return True
    
        self.csNodePath.setPos(self.environment,x,y,z)

        self.chq.clearEntries()

        self.traverser.clearColliders()
        self.traverser.addCollider(self.csNodePath, self.chq)
        self.traverser.traverse(self.environment)

        for entry in self.chq.getEntries():
            if entry.hasInto():
                if entry.getInto().isTangible():
                    return True
            
        return False


    def _neighbors(self,x,y):
        return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

    def _explore(self,p):
        x,y = p
        x1 = self.startX + self.squareSize*x
        y1 = self.startY + self.squareSize*y
        z1 = self.findFloor(x1,y1)
        if self.isSphereBlocked(x1,y1,z1+self.csHeight):
            self.blockedSquares[p] = z1
            return
        else:
            self.walkableSquares[p] = z1
            self.quadTree.fill(x,y)
            for n in self._neighbors(x,y):
                if not (n in self.frontierSquares or n in self.walkableSquares or n in self.blockedSquares):
                    self.frontierSquares[n] = 1
                    self.frontierSquaresQueue.append(n)


    def _exploreFrontier(self):
        if len(self.frontierSquaresQueue) == 0:
            assert len(self.frontierSquares.keys()) == 0
            return 0
        else:
            qlen = len(self.frontierSquaresQueue)
            for i in xrange(qlen):
                p = self.frontierSquaresQueue.pop(0)
                del self.frontierSquares[p]
                self._explore(p)
            return qlen



    def runDiscovery(self,maxSquares):
        print "Discovering walkable space (this will take 30-60 seconds)..."
        #self._unstashEnvironment()
        squaresExplored = 1

        self.walkableSquares[(0,0)] = self.findFloor(self.startX,self.startY)

        while (squaresExplored < maxSquares) and (len(self.frontierSquaresQueue) > 0):
            squaresExplored += self._exploreFrontier()
    

##     def visualize(self):
##         gFormat = GeomVertexFormat.getV3cp()
##         self.vertexData = GeomVertexData("OMGVERTEXDATA", gFormat, Geom.UHDynamic)
##         self.vertexWriter = GeomVertexWriter(self.vertexData, "vertex")
##         self.colorWriter = GeomVertexWriter(self.vertexData, "color")

##         numVerts = 0

##         for xa,ya,xb,yb in self.squares:
##             x1 = self.startX + self.squareSize*(xa) - self.squareSize*0.5
##             y1 = self.startY + self.squareSize*(ya) - self.squareSize*0.5

##             x2 = self.startX + self.squareSize*(xb) + self.squareSize*0.5
##             y2 = self.startY + self.squareSize*(yb) + self.squareSize*0.5

##             self.vertexWriter.addData3f(x1,y1,self.findFloor(x1,y1)+0.1)
##             self.colorWriter.addData4f(0.0, 1.0, 0.0, 0.5)

##             self.vertexWriter.addData3f(x2,y1,self.findFloor(x2,y1)+0.1)
##             self.colorWriter.addData4f(0.0, 1.0, 0.0, 0.5)

##             self.vertexWriter.addData3f(x2,y2,self.findFloor(x2,y2)+0.1)
##             self.colorWriter.addData4f(0.0, 1.0, 0.0, 0.5)

##             self.vertexWriter.addData3f(x1,y2,self.findFloor(x1,y2)+0.1)
##             self.colorWriter.addData4f(0.0, 1.0, 0.0, 0.5)

##             numVerts += 4

##         print "NUMVERTS: ", numVerts

##         self.pointVis = GeomLinestrips(Geom.UHStatic)

##         for i in xrange(numVerts/4):
##             self.pointVis.addVertex(i*4)
##             self.pointVis.addVertex(i*4+1)
##             self.pointVis.addVertex(i*4+2)
##             self.pointVis.addVertex(i*4+3)
##             self.pointVis.addVertex(i*4)
##             self.pointVis.closePrimitive()

        
##         self.visGeom = Geom(self.vertexData)
##         self.visGeom.addPrimitive(self.pointVis)

##         self.visGN = GeomNode("NavigationGridVis")
##         self.visGN.addGeom(self.visGeom)

##         self.visNodePath = self.environment.attachNewNode(self.visGN)

##         self.visNodePath.setTwoSided(True)
##         self.visNodePath.setRenderModeThickness(4)
##         #self.visNodePath.setTransparency(1)


    # ---------- Begin Triangulation Code ------------


##     def _addTriVertex(self,x,y):
##         '''
##         lookup[(x,y)] is a reference to the vert located to the UPPER-LEFT of grid square (x,y)
##         '''
##         if (x,y) not in self.gridCoordToVertexId:
##             vId = self.vertexCounter
##             self.vertexCounter += 1

##             self.gridCoordToVertexId[(x,y)] = vId
            
##             x1 = self.startX + self.squareSize*x - (0.5 * self.squareSize)
##             y1 = self.startY + self.squareSize*y - (0.5 * self.squareSize)
##             z1 = self.findFloor(x1,y1)
##             self.vertexIdToXYZ[vId] = (x1,y1,z1)

##             self.vertexToTris[vId] = []

##         return self.gridCoordToVertexId[(x,y)]


##     def _triangulateGridSquare(self,x,y,left=True):
##         a = self._addTriVertex(x,y)
##         b = self._addTriVertex(x+1,y)
##         c = self._addTriVertex(x+1,y+1)
##         d = self._addTriVertex(x,y+1)

##         if x < self.minX:
##             self.minX = x
##         if x > self.maxX:
##             self.maxX = x
##         if y < self.minY:
##             self.minY = y
##         if y > self.maxY:
##             self.maxY = y


##         if left:
##             self.triToVertices[self.triCounter] = [a,b,d]
##             self.triToAngles[self.triCounter] = [90,45,45]
        
##             self.triToVertices[self.triCounter+1] = [b,c,d]
##             self.triToAngles[self.triCounter+1] = [45,90,45]

##             self.vertexToTris[a].append(self.triCounter)
##             self.vertexToTris[b].append(self.triCounter)
##             self.vertexToTris[b].append(self.triCounter+1)
##             self.vertexToTris[c].append(self.triCounter+1)
##             self.vertexToTris[d].append(self.triCounter)
##             self.vertexToTris[d].append(self.triCounter+1)
##         else:
##             self.triToVertices[self.triCounter] = [a,b,c]
##             self.triToAngles[self.triCounter] = [45,90,45]
        
##             self.triToVertices[self.triCounter+1] = [a,c,d]
##             self.triToAngles[self.triCounter+1] = [45,45,90]

##             self.vertexToTris[a].append(self.triCounter)
##             self.vertexToTris[a].append(self.triCounter+1)
##             self.vertexToTris[b].append(self.triCounter)
##             self.vertexToTris[c].append(self.triCounter)
##             self.vertexToTris[c].append(self.triCounter+1)
##             self.vertexToTris[d].append(self.triCounter+1)

##         self.triCounter += 2
    
    
##     def countCruft(self):
##         count = 0
##         for s in self.squares:
##             if (s[0] == s[2]) and (s[1] == s[3]):
##                 x = s[0]
##                 y = s[1]
##                 numNeighbors = 0
##                 for (x1,y1) in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
##                     if (x1,y1) in self.walkableSquares:
##                         numNeighbors += 1
##                 if numNeighbors < 3:
##                     count += 1
##         return count

##     def killCruft(self):
##         for i in xrange(len(self.squares)):
##             s = self.squares[i]
##             if (s[0] == s[2]) and (s[1] == s[3]):
##                 x = s[0]
##                 y = s[1]
##                 numNeighbors = 0
##                 for (x1,y1) in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
##                     if (x1,y1) in self.walkableSquares:
##                         numNeighbors += 1
##                 if numNeighbors < 3:
##                     self.squares[i] = None

##         self.squares = [s for s in self.squares if s != None]


    def _addVertexByGridCoords(self,x,y):
        '''
        lookup[(x,y)] is a reference to the vert located at (-0.5,-0.5) from grid square (x,y)
        '''
        if (x,y) not in self.gridCoordToVertexId:
            vId = self.vertexCounter
            self.vertexCounter += 1

            self.gridCoordToVertexId[(x,y)] = vId
            
            x1 = self.startX + self.squareSize*x - (0.5 * self.squareSize)
            y1 = self.startY + self.squareSize*y - (0.5 * self.squareSize)
            z1 = self.findFloor(x1,y1)
            self.vertexIdToXYZ[vId] = (x1,y1,z1)

            self.vertToPolys[vId] = []

        return self.gridCoordToVertexId[(x,y)]

    
    def _addOpenSquare(self, gridX1, gridY1, gridX2, gridY2):
        curSpot = [gridX1,gridY1]

        verts = []
        angles = []

        while curSpot[0] <= gridX2:
            verts.append(self._addVertexByGridCoords(curSpot[0],curSpot[1]))
            if curSpot[0] == gridX1:
                angles.append(90)
            else:
                angles.append(180)
            self.vertToPolys[verts[-1]].append(self.polyCounter)
            curSpot[0] += 1

        while curSpot[1] <= gridY2:
            verts.append(self._addVertexByGridCoords(curSpot[0],curSpot[1]))
            if curSpot[1] == gridY1:
                angles.append(90)
            else:
                angles.append(180)
            self.vertToPolys[verts[-1]].append(self.polyCounter)
            curSpot[1] += 1

        while curSpot[0] > gridX1:
            verts.append(self._addVertexByGridCoords(curSpot[0],curSpot[1]))
            if curSpot[0] == gridX2+1:
                angles.append(90)
            else:
                angles.append(180)
            self.vertToPolys[verts[-1]].append(self.polyCounter)
            curSpot[0] -= 1

        while curSpot[1] > gridY1:
            if curSpot[1] == gridY2+1:
                angles.append(90)
            else:
                angles.append(180)
            verts.append(self._addVertexByGridCoords(curSpot[0],curSpot[1]))
            self.vertToPolys[verts[-1]].append(self.polyCounter)
            curSpot[1] -= 1


        self.polyToVerts[self.polyCounter] = verts
        self.polyToAngles[self.polyCounter] = angles
        self.polyCounter += 1

        

    def _subdivide(self):
        print "Growing squares..."
        self.vertexCounter = 0
        self.polyCounter = 0

        self.gridCoordToVertexId = {}
        self.vertexIdToXYZ = {}

        self.polyToVerts = {}
        self.polyToAngles = {}
        self.vertToPolys = {}

        self.squares = self.quadTree.squarify()

        for (gridX1,gridY1,gridX2,gridY2) in self.squares:
            self._addOpenSquare(gridX1,gridY1,gridX2,gridY2)


##     def _fixZValues(self):
##         print "Fixing Z values..."
##         for k in self.vertexIdToXYZ.keys():
##             v = self.vertexIdToXYZ[k]

##             self.vertexIdToXYZ[k] = (v[0],v[1],self.findFloor(v[0],v[1]))

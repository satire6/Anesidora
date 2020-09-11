import math
import bisect
import cPickle as pickle
import string
import time
import os
import StringIO

# File I/O stuff
import direct
from pandac.PandaModules import VirtualFileSystem
from pandac.PandaModules import Filename
from pandac.PandaModules import DSearchPath

# Visualization stuff
from pandac.PandaModules import GeomVertexFormat
from pandac.PandaModules import GeomVertexData
from pandac.PandaModules import GeomVertexWriter
from pandac.PandaModules import GeomLinestrips
from pandac.PandaModules import Geom
from pandac.PandaModules import GeomNode

from otp.navigation.NavUtil import PriQueue
from otp.navigation.NavUtil import FIFOCache

from libotp import PathTable

# Node locator collision stuff
from pandac.PandaModules import BitMask32
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionPolygon
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import CollisionTraverser

from otp.otpbase import OTPGlobals

class NavMesh(object):

    notify = directNotify.newCategory("NavMesh")
    
    def __init__(self, filepath=None, filename=None):
        if filename is not None:
            self._initFromFilename(filepath,filename)
        
    
    def initFromPolyData(self, polyToVerts, vertToPolys, polyToAngles, vertexCoords, environmentHash):
        '''
        Initialize the mesh from a set of polygons.

        polyToVerts:     Dictionary mapping a polygon ID to a set of N vertex IDs
        vertToPolys:     Dictionary mapping a vertex ID to a set of poly IDs (of every poly that includes it)
        polyToAngles:    Dictionary mapping a polygon ID to a set of N angles (in vertex order)
        vertexCoords:    Dictionary mapping a vertex ID to the coordinates of the vertex in worldspace
        environmentHash: Hash value derived from the same collision geometry as the other arguments.  See AreaMapper.getEnvironmentHash().
        '''
        self.polyToVerts = polyToVerts
        self.vertToPolys = vertToPolys
        self.polyToAngles = polyToAngles
        self.vertexCoords = vertexCoords
        self.environmentHash = environmentHash

        self.connectionLookup = {}
        
        self.connections = []

        self._discoverInitialConnectivity()        

        self.optimizeMesh()


    def visualize(self, parentNodePath, highlightVerts = [], pathVerts = [], visitedVerts = []):
        '''
        XXX Should move this into a product-specific class.
        '''
        gFormat = GeomVertexFormat.getV3cp()
        self.visVertexData = GeomVertexData("OMGVERTEXDATA2", gFormat, Geom.UHDynamic)
        self.visVertexWriter = GeomVertexWriter(self.visVertexData, "vertex")
        self.visVertexColorWriter = GeomVertexWriter(self.visVertexData, "color")

        vertToWriterIndex = {}
        currIndex = 0

        for v in self.vertexCoords.keys():
            vertToWriterIndex[v] = currIndex
            x = self.vertexCoords[v][0]
            y = self.vertexCoords[v][1]
            z = self.vertexCoords[v][2]
            self.visVertexWriter.addData3f(x,y,z+0.5)
            if v in highlightVerts:
                self.visVertexColorWriter.addData4f(1.0, 0.0, 0.0, 1.0)
            elif v in visitedVerts:
                self.visVertexColorWriter.addData4f(0.0, 0.0, 1.0, 1.0)
            else:
                self.visVertexColorWriter.addData4f(1.0, 1.0, 0.0, 1.0)
            currIndex += 1

        pathOffsetIntoIndex = currIndex
        
        for v in pathVerts:
            self.visVertexWriter.addData3f(v[0],v[1],v[2]+0.5)
            self.visVertexColorWriter.addData4f(0.0, 1.0, 0.0, 1.0)
            currIndex += 1

        lines = GeomLinestrips(Geom.UHStatic)

        for p in self.polyToVerts.keys():
            for v in self.polyToVerts[p]:
                lines.addVertex(vertToWriterIndex[v])
            lines.addVertex(vertToWriterIndex[self.polyToVerts[p][0]])
            lines.closePrimitive()

        if len(pathVerts) > 0:
            for i in xrange(len(pathVerts)):
                lines.addVertex(pathOffsetIntoIndex+i)
            lines.closePrimitive()

        self.visGeom = Geom(self.visVertexData)
        self.visGeom.addPrimitive(lines)

        self.visGN = GeomNode("NavMeshVis")
        self.visGN.addGeom(self.visGeom)

        self.visNodePath = parentNodePath.attachNewNode(self.visGN)

        self.visNodePath.setTwoSided(True)
        


    def _discoverInitialConnectivity(self):
        print "Building initial connectivity graph..."
        for pId in self.polyToVerts.keys():
            verts = self.polyToVerts[pId]

            numVerts = len(verts)
            candidates = []
            neighborPolys = []

            for v in verts:
                candidates += [p for p in self.vertToPolys[v] if (p not in candidates) and (p != pId)]

            for vNum in xrange(numVerts):
                neighbor = [p for p in candidates if ((verts[vNum] in self.polyToVerts[p]) and \
                                                      (verts[(vNum+1)%numVerts] in self.polyToVerts[p]))]
                if len(neighbor) == 0:
                    neighborPolys.append(None)
                elif len(neighbor) == 1:
                    neighborPolys.append(neighbor[0])
                else:
                    raise "Two neighbors found for the same edge?!?!"

            self.connectionLookup[pId] = neighborPolys


    # --------- Begin stitching code ---------

    def _attemptToMergePolys(self, polyA, polyB):
        newVerts = []
        newAngles = []
        newConnections = []
        
        vertsA = self.polyToVerts[polyA]
        vertsB = self.polyToVerts[polyB]

        lenA = len(vertsA)
        lenB = len(vertsB)

        anglesA = self.polyToAngles[polyA]
        anglesB = self.polyToAngles[polyB]
        

        sharedVerts = [v for v in vertsA if (v in vertsB)]

        locA = 0

        while vertsA[locA] not in sharedVerts:
            locA += 1

        while vertsA[locA] in sharedVerts:
            locA = (locA - 1) % lenA

        locA = (locA + 1) % lenA

        CCWmost = vertsA[locA]
        CCWmostLocA = locA

        while vertsA[locA] in sharedVerts:
            locA = (locA + 1) % lenA

        locA = (locA - 1) % lenA

        CWmost = vertsA[locA]
        CWmostLocA = locA


        # Convexity Check.
        # Verify that removing the edge preserves convexity and bail out if not.

        locA = 0
        locB = 0
        while vertsA[locA] != CCWmost:
            locA += 1
        while vertsB[locB] != CCWmost:
            locB += 1
        CCWmostAngleSum = anglesA[locA] + anglesB[locB]
        CCWmostLocB = locB
        if CCWmostAngleSum > 180:
            return False

        locA = 0
        locB = 0
        while vertsA[locA] != CWmost:
            locA += 1
        while vertsB[locB] != CWmost:
            locB += 1
        CWmostAngleSum = anglesA[locA] + anglesB[locB]
        if CWmostAngleSum > 180:
            return False

        # We've found the CW-most vert of the shared edge.
        # Now walk A clockwise until we hit the CCW-most vert of the shared edge.

        newVerts.append(CWmost)
        newAngles.append(CWmostAngleSum)
        newConnections.append(self.connectionLookup[polyA][locA])
        locA = (locA + 1) % lenA

        while vertsA[locA] != CCWmost:
            newVerts.append(vertsA[locA])
            newAngles.append(anglesA[locA])
            newConnections.append(self.connectionLookup[polyA][locA])
            locA = (locA + 1) % lenA

        # Now we've hit the CCW-most vert of the shared edge.
        # Walk B clockwise until we get back to the CW-most vert of the shared edge.

        locB = CCWmostLocB

        newVerts.append(CCWmost)
        newAngles.append(CCWmostAngleSum)
        neighbor = self.connectionLookup[polyB][locB]
        newConnections.append(neighbor)
        if neighbor is not None:
            for i in xrange(len(self.connectionLookup[neighbor])):
                if self.connectionLookup[neighbor][i] == polyB:
                    self.connectionLookup[neighbor][i] = polyA
        
        locB = (locB + 1) % lenB

        while vertsB[locB] != CWmost:
            newVerts.append(vertsB[locB])
            newAngles.append(anglesB[locB])
            neighbor = self.connectionLookup[polyB][locB]
            newConnections.append(neighbor)
            if neighbor is not None:
                for i in xrange(len(self.connectionLookup[neighbor])):
                    if self.connectionLookup[neighbor][i] == polyB:
                        self.connectionLookup[neighbor][i] = polyA            
            locB = (locB + 1) % lenB

        # We've added every vertex, its proper angle, and connectivity info
        # to the new polygon.  Now replace A with the new guy and remove B.

        self.polyToVerts[polyA] = newVerts
        self.polyToAngles[polyA] = newAngles
        self.connectionLookup[polyA] = newConnections

        # Make sure we have vertex->poly pointers for all the new verts we added to A.
        for v in newVerts:
            if polyA not in self.vertToPolys[v]:
                self.vertToPolys[v].append(polyA)

        # Clean up all of B's old vertices.
        for v in vertsB:
            self.vertToPolys[v].remove(polyB)
            if len(self.vertToPolys[v]) == 0:
                # No one's using this vertex anymore, remove it
                del self.vertToPolys[v]
                del self.vertexCoords[v]

        del self.polyToVerts[polyB]
        del self.polyToAngles[polyB]
        del self.connectionLookup[polyB]

        return True


    def _attemptToGrowPoly(self, pId):
        for neighbor in self.connectionLookup.get(pId,[]):
            if (neighbor is not None) and self._attemptToMergePolys(pId,neighbor):
                return True
        return False


    def _growEachPolyOnce(self):
        grewAtLeastOne = False
        
        for pId in self.connectionLookup.keys():
            if self._attemptToGrowPoly(pId):
                grewAtLeastOne = True

        return grewAtLeastOne


    def optimizeMesh(self):
        '''
        Takes a mesh that is already functionally complete and optimizes it for better performance.
        Reduces poly count and cuts out redundant vertices.
        Also compacts the polygon IDs into a contiguous range from 0 to N.
        No need to do the same for vertex IDs yet.
        '''
        '''print "Stitching polygons: %s -> " % (len(self.polyToVerts)),
        orig = len(self.polyToVerts)
        numPasses = 1
        while self._growEachPolyOnce():
            print "%s -> " % (len(self.polyToVerts)),
            numPasses += 1
        print "Done!\nPoly count reduced to %0.1f%% of original." % (len(self.polyToVerts)/float(orig)*100.0)'''

        self._pruneExtraVerts()

        self._compactPolyIds()

        self.numNodes = len(self.connections)

        biggest = 0
        biggestPoly = -1
        for p in self.polyToVerts:
            if len(self.polyToVerts[p]) > biggest:
                biggest = len(self.polyToVerts[p])
                biggestPoly = p

        print "Most verts in a single poly: ", biggest
        assert biggest < 256


    def _cleanPoly(self, polyId):
        verts = self.polyToVerts[polyId]
        angles = self.polyToAngles[polyId]
        neighbors = self.connectionLookup[polyId]
        numVerts = len(verts)

        newVerts = []
        newAngles = []
        newNeighbors = []

        for i in xrange(numVerts):
            if (angles[i] != 180) or \
               (len(self.vertToPolys.get(verts[i],[])) > 2) or \
               (neighbors[i] != neighbors[(i-1)%numVerts]):
                # Keep vertex
                newVerts.append(verts[i])
                newAngles.append(angles[i])
                newNeighbors.append(neighbors[i])
            else:
                # Remove vertex, this will happen twice so pop it
                self.vertToPolys.pop(verts[i],None)
                self.vertexCoords.pop(verts[i],None)

        if len(verts) != len(newVerts):
            self.polyToVerts[polyId] = newVerts
            self.polyToAngles[polyId] = newAngles
            self.connectionLookup[polyId] = newNeighbors

        assert len(newVerts) < 256
        

    def _pruneExtraVerts(self):
        print "Pruning extra vertices..."
        print "Starting verts: %s" % len(self.vertToPolys)
        for polyId in self.connectionLookup.keys():
            self._cleanPoly(polyId)
        print "Ending verts: %s" % len(self.vertToPolys)


    def _compactPolyIds(self):
        polyList = self.polyToVerts.keys()
        polyList.sort()

        oldToNewId = {None:None}

        newPolyToVerts = {}
        newPolyToAngles = {}
        self.connections = []

        currId = 0

        for oldId in polyList:
            oldToNewId[oldId] = currId
            self.connections.append([])
            currId += 1

        for oldId in polyList:
            newPolyToVerts[oldToNewId[oldId]] = self.polyToVerts[oldId]
            newPolyToAngles[oldToNewId[oldId]] = self.polyToAngles[oldId]
            #self.connections[oldToNewId[oldId]] = []
            for edgeNum in xrange(len(self.connectionLookup[oldId])):
                self.connections[oldToNewId[oldId]].append( oldToNewId[self.connectionLookup[oldId][edgeNum]] )

        self.polyToVerts = newPolyToVerts
        self.polyToAngles = newPolyToAngles
        del self.connectionLookup


    # --------- Begin pathfinding code ---------

    def _findCentroid(self, polyId):
        verts = self.polyToVerts[polyId]
        numVerts = len(verts)
        x = 0
        y = 0
        z = 0
        for v in verts:
            x += self.vertexCoords[v][0]
            y += self.vertexCoords[v][1]
            z += self.vertexCoords[v][2]

        x /= numVerts
        y /= numVerts
        z /= numVerts

        return (x,y,z)


##     def _estimateDistanceBetweenPolys(self, polyA, polyB):
##         centroidA = self._findCentroid(polyA)
##         centroidB = self._findCentroid(polyB)

##         dx = centroidA[0] - centroidB[0]
##         dy = centroidA[1] - centroidB[1]
##         dz = centroidA[2] - centroidB[2]

##         return math.sqrt(dx*dx + dy*dy + dz*dz)


    def _walkToNeighbor(self, currPoly, neighborPoly):
        currVerts = self.polyToVerts[currPoly]
        neighborVerts = self.polyToVerts[neighborPoly]

        lenCurr = len(currVerts)

        sharedVerts = [v for v in currVerts if (v in neighborVerts)]

        loc = 0

        while currVerts[loc] not in sharedVerts:
            loc += 1

        while currVerts[loc] in sharedVerts:
            loc = (loc - 1) % lenCurr

        loc = (loc + 1) % lenCurr

        CCWmost = currVerts[loc]
        CCWmostLoc = loc

        while currVerts[loc] in sharedVerts:
            loc = (loc + 1) % lenCurr

        loc = (loc - 1) % lenCurr

        CWmost = currVerts[loc]

        CCWmostCoords = self.vertexCoords[CCWmost]
        CWmostCoords = self.vertexCoords[CWmost]

        # For now, walk to the midpoint of the connecting edge

        departingEdge = CCWmostLoc # Don't need this with goal->start search

        neighborsEdge = 0
        while self.connections[neighborPoly][neighborsEdge] != currPoly:
            neighborsEdge += 1

        return (neighborsEdge,
                ((CWmostCoords[0] + CCWmostCoords[0])/2.0,
                 (CWmostCoords[1] + CCWmostCoords[1])/2.0,
                 (CWmostCoords[2] + CCWmostCoords[2])/2.0))
        

##     def _remakePath(self,walkBack,currNode):
##         if currNode in walkBack:
##             p = self._remakePath(walkBack,walkBack[currNode])
##             return p + [currNode,]
##         return [currNode,]
        

##     def findRoute(self, startNode, goalNode):
##         '''
##         So much love for A*.
##         '''
##         nodeToF = {}
##         nodeToG = {}
##         nodeToH = {}

##         walkBack = {}

##         #nodeToEntryPoint = {}
##         self.nodeToEntryPoint[startNode] = self._findCentroid(startNode)

##         nodeToG[startNode] = 0
##         nodeToH[startNode] = self._estimateDistanceBetweenPolys(startNode,goalNode)
##         nodeToF[startNode] = nodeToG[startNode] + nodeToH[startNode]
        
##         closedSet = {}
##         openSet = {}
##         openQueue = PriQueue() # Priority = F score

##         openSet[startNode] = 1
##         openQueue.push((nodeToF[startNode],startNode))

##         goalPoint = self._findCentroid(goalNode)

##         while len(openSet) > 0:
##             f,currNode = openQueue.pop(0)
##             del openSet[currNode]

##             self.aStarWasHere[currNode] = 1
            
##             if currNode == goalNode:
##                 return self._remakePath(walkBack,currNode)

##             closedSet[currNode] = 1

##             currPoint = self.nodeToEntryPoint[currNode]

##             for neighbor in self.connections[currNode]:
##                 if (neighbor is not None) and (neighbor not in closedSet):
##                     departingEdge,newEntryPoint = self._walkToNeighbor(currNode,currPoint,neighbor)
##                     newG = nodeToG[currNode] + math.sqrt((newEntryPoint[0] - currPoint[0])**2 + \
##                                                          (newEntryPoint[1] - currPoint[1])**2 + \
##                                                          (newEntryPoint[2] - currPoint[2])**2)
##                     gotHereFasterThanBefore = False
                    
##                     if neighbor not in openSet:
##                         openSet[neighbor] = 1
##                         gotHereFasterThanBefore = True
##                     elif newG < nodeToG[neighbor]:
##                         openQueue.remove((nodeToF[neighbor],neighbor))
##                         gotHereFasterThanBefore = True

##                     if gotHereFasterThanBefore:
##                         walkBack[neighbor] = currNode
##                         self.nodeToEntryPoint[neighbor] = newEntryPoint
##                         nodeToH[neighbor] = math.sqrt((goalPoint[0] - newEntryPoint[0])**2 + \
##                                                       (goalPoint[1] - newEntryPoint[1])**2 + \
##                                                       (goalPoint[2] - newEntryPoint[2])**2)
##                         nodeToG[neighbor] = newG
##                         nodeToF[neighbor] = nodeToG[neighbor] + nodeToH[neighbor]
##                         openQueue.push((nodeToF[neighbor],neighbor))

##         raise "No path found!  D:"
                        

    def _findAllRoutesToGoal(self, goalNode):
        '''
        Find the shortest path from ALL start nodes to the given goal node.  (Djikstra)
        
        After running, self.pathData[startNode][goalNode] == outgoing edge from startNode to the next node
        for the given value of goalNode and ALL values of startNode.
        '''
        nodeToG = {}
        
        walkBack = {}

        nodeDeparturePoint = {}
        nodeDeparturePoint[goalNode] = self._findCentroid(goalNode)

        nodeToG[goalNode] = 0
        
        closedSet = {}
        openSet = {}
        openQueue = PriQueue()

        openSet[goalNode] = 1
        openQueue.push((nodeToG[goalNode],goalNode))

        walkBack[goalNode] = (0,goalNode)

        while len(openSet) > 0:
            f,currNode = openQueue.pop(0)
            del openSet[currNode]

            closedSet[currNode] = 1

            currPoint = nodeDeparturePoint[currNode]

            for neighbor in self.connections[currNode]:
                if (neighbor is not None) and (neighbor not in closedSet):
                    neighborsEdge,newPoint = self._walkToNeighbor(currNode,neighbor)
                    newG = nodeToG[currNode] + math.sqrt((newPoint[0] - currPoint[0])**2 + \
                                                         (newPoint[1] - currPoint[1])**2 + \
                                                         (newPoint[2] - currPoint[2])**2)
                    gotHereFasterThanBefore = False
                    
                    if neighbor not in openSet:
                        openSet[neighbor] = 1
                        gotHereFasterThanBefore = True
                    elif newG < nodeToG[neighbor]:
                        openQueue.remove((nodeToG[neighbor],neighbor))
                        gotHereFasterThanBefore = True

                    if gotHereFasterThanBefore:
                        walkBack[neighbor] = (neighborsEdge,currNode)
                        nodeDeparturePoint[neighbor] = newPoint
                        nodeToG[neighbor] = newG
                        openQueue.push((nodeToG[neighbor],neighbor))


        for startNode in xrange(len(self.connections)):
            departingEdge = walkBack[startNode][0]

            assert self.pathData[startNode][goalNode] is None

            self.pathData[startNode][goalNode] = departingEdge


    def generatePathData(self,rowRange=None):
        '''
        Entry point for path preprocessing.
        Solves all pairs shortest path for this mesh.
        Stores the result in self.pathData.
        SLOW.  Expect 8-10 minutes on Port Royal alone.

        Currently runs Djikstra on every possible start node.
        There are faster approaches for APSP, but...
        '''
        if rowRange is None:
            rowRange = (0,self.numNodes)

        self.initPathData()

        for goalNode in xrange(rowRange[0],rowRange[1]):
            self._findAllRoutesToGoal(goalNode)


    def createPathTable(self):
        '''
        Takes a 2D array self.pathData and changes it in place.
        Each row is changed into a run-length encoded string.
        Then, feeds the data into a new PathTable instance.
        '''
        for row in self.pathData:
            for val in row:
                if val == None:
                    raise "Incomplete path data!"

        shortestPathLookup = self.pathData

        self.pathData = []

        # Run-Length Encode the whole thing!
        for start in xrange(self.numNodes):
            row = []
            lastVal = None
            nodesInRow = 0
            for goal in xrange(self.numNodes):
                val = shortestPathLookup[start][goal]
                if val != lastVal:
                    row.append([goal,val])
                    lastVal = val
                    nodesInRow += 1
                else:
                    nodesInRow += 1

            assert nodesInRow == self.numNodes

            stringsRow = []

            # Convert row to a bytestring to save space
            for item in row:
                assert item[0] < 65536
                assert item[1] < 256

                stringsRow.append(chr(item[0]/256) + chr(item[0]%256) + chr(item[1]))
                
                assert len(stringsRow[-1]) == 3

            rowString = string.join(stringsRow,"")
                
            self.pathData.append(rowString)

        self.pathTable = PathTable(self.pathData, self.connections)
            

    def printPathData(self):
        '''
        Outputs the pickled path table to stdout.
        '''
        import sys
        sys.stdout.write(pickle.dumps(self.pathData,protocol=0))
        

    def initPathData(self):
        self.pathData = []

        for i in xrange(self.numNodes):
            self.pathData.append([None,]*self.numNodes)

        
    def addPaths(self, partialData):
        for i in xrange(len(partialData)):
            for j in xrange(len(partialData[i])):
                if partialData[i][j] is not None:
                    assert self.pathData[i][j] is None
                    self.pathData[i][j] = partialData[i][j]


##     def pathTableLookup(self, startNode, goalNode):
##         '''
##         Look up the equivalent of pathData[goalNode][startNode] in our run-length encoded data.
##         '''
##         if startNode >= self.numNodes or goalNode >= self.numNodes:
##             raise "Invalid node ID.  Must be less than self.numNodes (%s)." % self.numNodes

##         str = self.pathData[startNode]

##         pos = 0

##         while (pos < len(str)) and (256*ord(str[pos]) + ord(str[pos+1]) <= goalNode):
##             #print pos, ": ",256*ord(str[pos]) + ord(str[pos+1])
##             pos += 3

##         pos -= 3

##         return ord(str[pos+2])            


    def findRoute(self, startNode, goalNode):
        '''
        Returns the node-by-node route from startNode to goalNode.
        '''
        return self.pathTable.findRoute(startNode, goalNode)
    

    def makeNodeLocator(self, environment):
        meshNode = CollisionNode("NavMeshNodeLocator")
        meshNode.setFromCollideMask(BitMask32.allOff())
        meshNode.setIntoCollideMask(OTPGlobals.PathFindingBitmask)

        self.polyHashToPID = {}

        for pId in self.polyToAngles:
            vertCount = 0
            corners = []
            for angle in self.polyToAngles[pId]:
                if angle != 180:
                    # It's a corner
                    corners.append(vertCount)
                vertCount += 1

            # XXX this code only works for square nodes at present
            # Unfortunately we can only make triangle or square CollisionPolygons on the fly
            assert len(corners) == 4

            #import pdb
            #pdb.set_trace()

            verts = []

            for vert in corners:
                verts.append((self.vertexCoords[self.polyToVerts[pId][vert]][0],
                              self.vertexCoords[self.polyToVerts[pId][vert]][1],
                              0))
                

            #import pdb
            #pdb.set_trace()
            
            poly = CollisionPolygon(verts[0], verts[1], verts[2], verts[3])

            assert poly not in self.polyHashToPID

            self.polyHashToPID[poly] = pId

            meshNode.addSolid(poly)

        ray = CollisionRay()
        ray.setDirection(0,0,-1)
        ray.setOrigin(0,0,0)

        rayNode = CollisionNode("NavMeshRay")
        rayNode.setFromCollideMask(OTPGlobals.PathFindingBitmask)
        rayNode.setIntoCollideMask(BitMask32.allOff())
        rayNode.addSolid(ray)

        self.meshNodePath = environment.attachNewNode(meshNode)
        self.rayNodePath = environment.attachNewNode(rayNode)

        self.meshNodePath.setTwoSided(True)

        self.chq = CollisionHandlerQueue()
        self.traverser = CollisionTraverser()
        self.traverser.addCollider(self.rayNodePath, self.chq)


    def findNodeFromPos(self, environment, x, y):
        self.rayNodePath.setPos(environment, x, y, 50000)
        self.chq.clearEntries()

        self.traverser.traverse(self.meshNodePath)

        if self.chq.getNumEntries() != 1:
            self.notify.warning("No node found at position: %s, %s in %s" % (x, y, environment))
            return 0

        e = self.chq.getEntry(0)

        assert e.hasInto()
        if not e.hasInto():
            self.notify.warning("No into found for collision %s" % (e))
            

        pId = self.polyHashToPID[e.getInto()]

        return pId
        

    # --------- Begin long-term storage code ---------

    def writeToFile(self, filename, storePathTable=True):
        '''
        Output the contents of this mesh to the file specified.
        Saving to a file lets us avoid doing expensive precomputation every time a mesh instance is required.
        '''
        if self.environmentHash is None:
            raise "Attempted write to file without valid environment hash!"

        if storePathTable and not self.pathData:
            raise "Attempted to write empty pathData.  Call NavMesh.generatePathTable() first!"
        
        f = open(filename,'wb')

        if storePathTable:
            pickle.dump([self.environmentHash,
                         self.polyToVerts,
                         self.polyToAngles,
                         self.vertexCoords,
                         self.connections,
                         self.pathData],
                        f,
                        protocol=2)
            f.close()
            self.pathData = None
        else:
            pickle.dump([self.environmentHash,
                         self.polyToVerts,
                         self.polyToAngles,
                         self.vertexCoords,
                         self.connections,
                         None],
                        f,
                        protocol=2)
            f.close()            

        print "Successfully wrote to file %s." % filename


    def _initFromString(self, str):
        contents = pickle.loads(str)

        self.environmentHash = contents[0]
        self.polyToVerts = contents[1]
        self.polyToAngles = contents[2]
        self.vertexCoords = contents[3]
        self.connections = contents[4]
        self.pathData = contents[5]

        if self.pathData is not None:
            self.pathTable = PathTable(self.pathData, self.connections)
            self.pathData = None

        self.numNodes = len(self.connections)
        

    def _initFromFilename(self, filepath, filename):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename(filename)
        searchPath = DSearchPath()
        #searchPath.appendDirectory(Filename('.'))
        #searchPath.appendDirectory(Filename('etc'))
        #searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('~')))
        #searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$HOME')))
        searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars(filepath)))

        found = vfs.resolveFilename(filename,searchPath)

        if not found:
            raise IOError, "File not found!"

        str = vfs.readFile(filename,1)

        self._initFromString(str)


    def checkHash(self, envHash):
        '''
        "Does this mesh represent the environment I think it does?"
        If this check fails, the mesh is out of date (or being used with the wrong environment).
        In either case, whoever generated this instance should discard it and create a new mesh from scratch.
        '''
        return envHash == self.environmentHash



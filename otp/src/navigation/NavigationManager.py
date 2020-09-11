import string
import md5
import subprocess
import cPickle as pickle
import time
import os

from otp.navigation.AreaMapper import AreaMapper
from otp.navigation.NavMesh import NavMesh
from otp.otpbase import OTPGlobals
from pandac.PandaModules import BitMask32
from direct.directnotify import DirectNotifyGlobal


class NavigationManager(object):
    notify = DirectNotifyGlobal.directNotify.newCategory("NavigationManager")
    '''
    "The pathfinding class."

    * Offers fast pathfinding based on navigation meshes.  No waypoints necessary!
    * Auto-generates navigaton meshes and stores them to disk for future use.
    * Detects changes in the collision geometry of your environment and builds a new mesh automatically.
    * Precomputes all optimal paths for your environment and stores them alongside the navmesh on disk.


    Example Usage:

    from pirates.world.LocationConstants import LocationIds
    nm = NavigationManager("c:\\cygwin\\home\\ian\\trunk\\otp\\src\\navigation\\",
                           {LocationIds.PORT_ROYAL_ISLAND:"port_royal"})
    pr = simbase.air.doFind("Port Royal")
    nm.addEnvironment(pr)
    # XXX incomplete!  more to come


    Current Limitations:

    * Not finished!
    * AreaMapper assumes no vertical (Z-axis) overlap in walkable space.  Multi-level structures will
      not be properly explored--only the uppermost floor is found.
    * NavMesh itself is not impacted by Z-axis overlap, so if you want to use this pathfinding system
      with your 20-story building, just figure out how to write an AreaMapper for it!
    
    '''
    def __init__(self, navFilePath, envIdToFilename):
        self.navFilePath = navFilePath
        self.usePathTables = True

        self.envIdToFilename = envIdToFilename

        self.meshes = {}


    def _getEnvironmentId(self, env):
        '''
        Given an environment object, returns a unique ID that is constant from session to session.
        Override with the appropriate calls for your product.
        '''
        return env.getUniqueId()


    def _getEnvironmentHash(self, env):
        '''
        Accepts an environment object and returns the MD5 hash of a string representing all collision geometry therein.
        This value should change whenever the layout of your collisions changes.
        Use to determine whether derived data still reflects reality.

        Base method assumes env is a NodePath, but you can override this to handle whatever you like.
        '''
        allCNs = env.findAllMatches('**/+CollisionNode')
        monsterData = []

        for np in allCNs:
            #monsterData.append( str(np) )
            #monsterData.append( str(np.getTransform(env)) )
            #monsterData.append( str(np.getCollideMask()) )
            monsterData.append("cn")
            
            node = np.node()

            if node.getIntoCollideMask() & OTPGlobals.WallBitmask != BitMask32.allOff():
                for i in xrange(node.getNumSolids()):
                    s = node.getSolid(i)
                    
                    monsterData.append( str(s) )
                    
        monsterData = string.join(monsterData, "")
    
        hash = md5.new(monsterData)

        return hash.digest()


    def addEnvironment(self, env, performHashCheck=True):
        '''
        "Enable navigation for the specified environment."
        On startup, call this for each area that needs to support navigation.

        The NavigationManager will read in all existing data for your environment.

        If data files do not exist or are out of sync due to a change in the collision geometry,
        we compute them and write them out to the path specified in self.navFilePath.
        '''
        id = self._getEnvironmentId(env)
        hash = self._getEnvironmentHash(env)
        filename = self.envIdToFilename[id]

        if self.usePathTables:
            filename += ".nav"
        else:
            filename += ".msh"

        try:
            newMesh = NavMesh(filepath = self.navFilePath,
                              filename = filename)
            if not newMesh.checkHash(hash):
                if performHashCheck:
                    assert self.notify.warning("Hash check failed on %s!" % (filename))
                    newMesh = None
                else:
                    assert self.notify.warning("Hash check failed on %s, ignoring." % (filename))
        except IOError:
            assert self.notify.warning("Error reading file %s." % (filename))
            newMesh = None


        if newMesh is None:
            assert self.notify.debug("--------- Recomputing navigation data for %s(%s). ---------" % (self.envIdToFilename[id],id))

            assert self.notify.debug("Holding this process hostage for a few minutes.  Go make a sandwich.")

            assert self.notify.debug("Editing environments and want to avoid this wait in the future?")

            assert self.notify.debug("Set 'use-path-finding 1' in your prc file.")

            t0 = time.time()

            mapper = AreaMapper(env)
            newMesh = NavMesh()
            newMesh.initFromPolyData(mapper.polyToVerts,mapper.vertToPolys,mapper.polyToAngles,mapper.vertexIdToXYZ,hash)
            newMesh.writeToFile(self.navFilePath+self.envIdToFilename[id]+".msh",storePathTable=False)

            assert self.notify.debug("Generating path table (this could take almost an hour)...")


            t1 = time.time()

            if config.GetBool("want-parallel-pathgen", False):

                numProcs = 8
                rowsPerProc = newMesh.numNodes / numProcs
                procs = []
                rowsLeft = newMesh.numNodes

                assert self.notify.debug("Farming rows out to %s slaves:" % numProcs)

                for i in xrange(numProcs):
                    if rowsLeft < rowsPerProc*2:
                        assert i == numProcs-1
                        todo = rowsLeft
                    else:
                        todo = rowsPerProc

                    rowsLeft -= todo
                    
                    args = pickle.dumps([self.navFilePath,
                                         self.envIdToFilename[id]+".msh",
                                         i*rowsPerProc,
                                         i*rowsPerProc + todo],
                                        protocol=0)

                    assert self.notify.debug("(%s, %s)" % (i*rowsPerProc, i*rowsPerProc + todo))

                    os.chdir(os.path.expandvars("$OTP/src/navigation"))

                    proc = subprocess.Popen("python APSPSlave.py",
                                            stdout=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    proc.stdin.write(args)
                    proc.stdin.flush()
                    proc.stdin.close()
                    procs.append(proc)

                assert rowsLeft == 0

                newMesh.initPathData()

                for proc in procs:
                    res = proc.stdout.read()
                    partialTable = pickle.loads(res)
                    newMesh.addPaths(partialTable)

            else:
                newMesh.generatePathData()

            newMesh.createPathTable()
                
            t2 = time.time()
                
            assert self.notify.debug("Done!  Pathfinding time: %0.3f seconds" % (t2-t1))

            assert self.notify.debug("Total preprocessing time: %0.3f seconds" % (t2-t0))

            newMesh.writeToFile(self.navFilePath+self.envIdToFilename[id]+".nav",storePathTable=True)

            if not newMesh.checkHash(hash):
                raise "Hash check still failed after we regenerated the NavMesh!  Something is seriously wrong!"
            
        # Mesh is now accurate, we're good to go.
        self.meshes[id] = newMesh
        

def gogogo():
    from pandac.PandaModules import Filename
    from pirates.world.LocationConstants import LocationIds

    navpath = os.path.expandvars(config.GetString("navdata-path","$OTP/src/navigation/"))
    
    simbase.nm = NavigationManager(navpath,
                                   {LocationIds.PORT_ROYAL_ISLAND:'port_royal'})
    pr = simbase.air.doFind("Port Royal")
    simbase.nm.addEnvironment(pr)

def randomlookups():
    import random
    import time
    mesh = simbase.air.navMgr.meshes.values()[0]

    assert self.notify.debug("Timing lookups...")

    routeList = []

    for i in xrange(1000000):
        routeList.append((random.randint(0,mesh.numNodes-1),random.randint(0,mesh.numNodes-1)))

    t1 = time.time()

    for i in routeList:
        #mesh.pathTableLookup(random.randint(0,mesh.numNodes-1),random.randint(0,mesh.numNodes-1))
        route = mesh.findRoute(i[0],i[1])

    #for i in xrange(mesh.numNodes-1):
    #    for j in xrange(mesh.numNodes-1):
    #        val = mesh.pathTableLookup(j,i)

    t2 = time.time()

    assert self.notify.debug("Time: %0.3f seconds" % (t2-t1))
    assert self.notify.debug("Paths per second: %0.3f" % (1000000/(t2-t1)))


def routelookups():
    import time
    mesh = simbase.nm.meshes.values()[0]
    assert self.notify.debug("Timing lookups...")

    t1 = time.time()

    i = 0

    for i in xrange(mesh.numNodes):
        for j in xrange(mesh.numNodes):
            route = mesh.pathTable.findRoute(i,j)

    t2 = time.time()

    assert self.notify.debug("Time: %0.3f" % (t2-t1))

    assert self.notify.debug("Lookups per second: %0.1f" % (mesh.numNodes**2 / (t2-t1)))


def intersectiontest():
    import random
    import time

    s = set()
    t = set()

    for i in xrange(0,2500):
        s.add(i)
    for i in xrange(2000,4000):
        t.add(i)

    t1 = time.time()

    for i in xrange(1000000):
        s.intersection(t)

    t2 = time.time()

    assert self.notify.debug("Intersection time: %0.3f" % (t2-t1))
    assert self.notify.debug("Intersects per second: %0.1f" % (1000000 / (t2-t1)))
    

def addtest():
    import time

    s = set()

    t1 = time.time()

    for i in xrange(1000000):
        s.add(i)

    t2 = time.time()

    assert self.notify.debug("Add time: %0.3f" % (t2-t1))
    assert self.notify.debug("Adds per second: %0.1f" % (1000000 / (t2-t1)))
    

def findNodeTest():
    import time

    mesh = simbase.nm.meshes.values()[0]
    pr = simbase.air.doFind("Port Royal")

    mesh.makeNodeLocator(pr)

    t1 = time.time()

    for i in xrange(10000):
        pId = mesh.findNodeFromPos(pr, 0.5, 0.5)

    t2 = time.time()

    assert self.notify.debug("Find time: %0.3f" % (t2-t1))
    assert self.notify.debug("Finds per second: %0.1f" % (10000 / (t2-t1)))

"""PartyLoader module: contains the PartyLoader class"""
import math
import random

from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State

from pandac.PandaModules import *
from pandac.PandaModules import NodePath

from toontown.toonbase.ToontownGlobals import *
from toontown.safezone import SafeZoneLoader

from toontown.parties import Party
from toontown.parties.PartyGlobals import FireworksStartedEvent, FireworksFinishedEvent

class PartyLoader(SafeZoneLoader.SafeZoneLoader):
    notify = DirectNotifyGlobal.directNotify.newCategory("PartyLoader")
    
    
    def __init__(self, hood, parentFSM, doneEvent):
        """
        PartyLoader constructor: create a play game ClassicFSM
        """
        assert(self.notify.debug("__init__()"))
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)

        # override the fsm to be more meaningful to parties
        del self.fsm
        self.fsm = ClassicFSM.ClassicFSM('PartyLoader',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['quietZone', 'party', 'planning']),
                            State.State('party',
                                        self.enterParty,
                                        self.exitParty,
                                        ['quietZone']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['planning', 'party']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )
        self.musicFile = "phase_13/audio/bgm/party_original_theme.mid"
        self.activityMusicFile = "phase_13/audio/bgm/party_waltz_dance.mid"
        self.dnaFile = "phase_13/dna/party_sz.dna"
        # There is no safe zone specific DNA Storage for the party
        self.safeZoneStorageDNAFile = None
        
        self.cloudSwitch = 0
        
        self.id = PartyHood
        self.partyOwnerId = None
        self.branchZone = None        
        self.partyDoneEvent = "partyDone"
        self.barrel = None
        self.clouds = []
        self.cloudTrack = None
        self.sunMoonNode = None
        self.fsm.enterInitialState()
        
    def load(self):
        # set the clear color to green to make it appear more grassy
        self.oldClear = base.win.getClearColor()
        base.win.setClearColor(Vec4(0.47, 0.69, 0.3, 1.0))
        
        assert(self.notify.debug("load()"))
        SafeZoneLoader.SafeZoneLoader.load(self)
        # create music and sound effects
        self.underwaterSound = base.loadSfx('phase_4/audio/sfx/AV_ambient_water.mp3')
        self.swimSound = base.loadSfx('phase_4/audio/sfx/AV_swim_single_stroke.mp3')
        self.submergeSound = base.loadSfx('phase_5.5/audio/sfx/AV_jump_in_water.mp3')
        self.birdSound=map(base.loadSfx, [
                'phase_4/audio/sfx/SZ_TC_bird1.mp3',
                'phase_4/audio/sfx/SZ_TC_bird2.mp3',
                'phase_4/audio/sfx/SZ_TC_bird3.mp3'])
        # SDN: use birds as a place holder for crickets for now
        self.cricketSound=map(base.loadSfx, [
                'phase_4/audio/sfx/SZ_TC_bird1.mp3',
                'phase_4/audio/sfx/SZ_TC_bird2.mp3',
                'phase_4/audio/sfx/SZ_TC_bird3.mp3'])
        
    def unload(self):
        assert(self.notify.debug("unload()"))
        self.ignoreAll()
        
        # restore the clear color
        base.win.setClearColor(self.oldClear)
        
        # remove ourselves from the current party
        if base.cr.partyManager:
            # partyManager can become None in case on an AI reset
            base.cr.partyManager.leaveParty()
        
        self.partyOwnerId = None
        self.partyZoneId = None
        if self.place:
            self.place.exit()
            self.place.unload()
            del self.place
        del self.underwaterSound
        del self.swimSound
        del self.submergeSound
        del self.birdSound
        del self.cricketSound
        
        self.__cleanupCloudFadeInterval()

        if self.sunMoonNode:
            self.sunMoonNode.removeNode()
            del self.sunMoonNode
            self.sunMoonNode = None
        if self.clouds:
            for cloud in self.clouds:
                cloud[0].removeNode()
                #cloud[0].destroy()
                del cloud[1]
            del self.clouds
        if self.barrel:
            self.barrel.removeNode()
        SafeZoneLoader.SafeZoneLoader.unload(self)
        
    def loadClouds(self):
        # load up the cloud platforms
        self.loadCloudPlatforms()
        if base.cloudPlatformsEnabled and 0:
            self.setCloudSwitch(1)
            pass
        if self.cloudSwitch:
            self.setCloudSwitch(self.cloudSwitch)
        

    def enter(self, requestStatus):
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        self.partyOwnerId = requestStatus.get("ownerId", base.localAvatar.doId) 
        base.localAvatar.inParty = 1
        
        self.accept(FireworksStartedEvent, self.__handleFireworksStarted)
        self.accept(FireworksFinishedEvent, self.__handleFireworksFinished)
        
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        assert(self.notify.debug("exit()"))
        self.ignoreAll()
        base.cr.cache.flush()
        base.localAvatar.stopChat()
        base.localAvatar.inParty = 0
        
        self.ignore(FireworksStartedEvent)
        self.ignore(FireworksFinishedEvent)
        
        SafeZoneLoader.SafeZoneLoader.exit(self)

    def createSafeZone(self, dnaFile):
        assert(self.notify.debug("createParty()"))
        SafeZoneLoader.SafeZoneLoader.createSafeZone(self,dnaFile)
        parent = self.geom.getParent()
        geom = self.geom
        n = NodePath("PartyGroundRoot")
        n.reparentTo(parent)
        geom.reparentTo(n)
        geom.setPos(-10.0, 0.0, 0.0)
        self.geom = n

        # load the sun and moon
        self.loadSunMoon()

    def loadSunMoon(self):
        self.sun = loader.loadModel("phase_4/models/props/sun.bam")
        self.moon = loader.loadModel("phase_5.5/models/props/moon.bam")
        # create a new node to hold the sun and moon. just set the pitch according to daytime
        self.sunMoonNode = self.geom.attachNewNode("sunMoon")
        self.sunMoonNode.setPosHpr(0,0,0,0,0,0)
        if self.sun:
            self.sun.reparentTo(self.sunMoonNode)
            self.sun.setY(270)
            self.sun.setScale(2)
            self.sun.setBillboardPointEye()
        if self.moon:
            #self.moon.setP(180)
            self.moon.reparentTo(self.sunMoonNode)
            self.moon.setY(-270)
            self.moon.setScale(15)
            self.moon.setBillboardPointEye()

        # start out at day time
        self.sunMoonNode.setP(30)

    # start state
    # Defined in SafeZoneLoader.py
    
    # party state 
    
    def enterParty(self, requestStatus):
        self.notify.debug("enterParty: requestStatus = %s" % requestStatus)
        ownerId = requestStatus.get("ownerId")
        if ownerId:
            self.partyOwnerId = ownerId 
        zoneId = requestStatus["zoneId"]
        self.notify.debug("enterParty, ownerId = %s, zoneId = %s" % (self.partyOwnerId, zoneId))
        self.accept(self.partyDoneEvent, self.handlePartyDone)
        self.place = Party.Party(self, self.partyOwnerId, zoneId,
                                   self.fsm.getStateNamed("party"), self.partyDoneEvent)
        base.cr.playGame.setPlace(self.place)
        self.place.load()
        self.place.enter(requestStatus)
        self.partyZoneId = zoneId

    def exitParty(self):
        self.notify.debug("exitParty")
        self.ignore(self.partyDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place) 
        base.cr.cache.flush()
        
    def handlePartyDone(self, doneStatus=None):
        PartyLoader.notify.debug("handlePartyDone doneStatus = %s" % doneStatus)
        if not doneStatus:
            doneStatus = self.place.getDoneStatus()

        how = doneStatus["how"]
        shardId = doneStatus["shardId"]
        hoodId = doneStatus["hoodId"]
        zoneId = doneStatus["zoneId"]
        avId = doneStatus.get("avId", -1)
        ownerId = doneStatus.get("ownerId", -1)
        # If we're switching shards, or exiting the party,
        # we need to back out one more level.
        
        self.notify.debug("hoodId = %s, avId = %s" % (hoodId,avId))
        self.doneStatus = doneStatus
        messenger.send(self.doneEvent)


    # quietZone state
    # Defined in SafeZoneLoader.py

    # SDN: check whether using SafeZoneLoaders function works here
    def handleQuietZoneDone(self):
        status=self.quietZoneStateData.getRequestStatus()
        assert(self.notify.debug("handleQuietZoneDone()\n  status="
                +str(status)))
        # Change to the destination state:
        self.fsm.request(status["where"], [status])

    # final state
    # Defined in SafeZoneLoader.py
    
    # utility functions
    def atMyParty(self):
        # True if localToon is the owner of this party
        if self.partyOwnerId != None:
            if self.partyOwnerId == base.localAvatar.getDoId():
                return 1
            else:
                return 0
        else:
            self.notify.warning("We aren't in an party")

            
    def startCloudPlatforms(self):
        assert(self.notify.debug("startClouds"))
        return
        if len(self.clouds):
            self.cloudTrack = self.__cloudTrack()
            self.cloudTrack.loop()
        
    def stopCloudPlatforms(self):
        assert(self.notify.debug("stopClouds"))
        if self.cloudTrack:
            self.cloudTrack.pause()
            del self.cloudTrack
            self.cloudTrack = None

    def __cloudTrack(self):
        track = Parallel()
        for cloud in self.clouds:
            axis = cloud[1]
            pos = cloud[0].getPos(render)
            newPos = pos + axis * 30
            reversePos = pos - axis * 30
            track.append(Sequence(LerpPosInterval(cloud[0], 10,
                                                  newPos),
                                  (LerpPosInterval(cloud[0], 20,
                                                   reversePos)),
                                  (LerpPosInterval(cloud[0], 10,
                                                   pos))))
        return track

    def debugGeom(self, decomposed):
        print 'numPrimitives = %d' % decomposed.getNumPrimitives()
        
        for primIndex in range(decomposed.getNumPrimitives()):
            prim = decomposed.getPrimitive(primIndex)
            print 'prim = %s' % prim
            print 'isIndexed = %d' % prim.isIndexed()            
            print 'prim.getNumPrimitives = %d' % prim.getNumPrimitives()

            #import pdb; pdb.set_trace()            
            for basicPrim in range(prim.getNumPrimitives()):
                pass
                print '%d start=%d' % (basicPrim, prim.getPrimitiveStart(basicPrim))
                print '%d end=%d' % (basicPrim, prim.getPrimitiveEnd(basicPrim))



    def loadCloud( self, version, radius, zOffset):
        self.notify.debug( 'loadOnePlatform version=%d' % version)

        # load the model
        cloud  = NodePath("cloud-%d%d" % (radius, version))
        cloudModel = loader.loadModel("phase_5.5/models/estate/bumper_cloud")        
        cc = cloudModel.copyTo(cloud)

        # rename the collision polys
        colCube = cc.find("**/collision")
        colCube.setName("cloudSphere-0")

        # position and scale this cloud
        dTheta = 2.0 * math.pi / self.numClouds
        cloud.reparentTo(self.cloudOrigin)
        axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]        
        cloud.setPos(radius * math.cos(version * dTheta),
                     radius * math.sin(version * dTheta),
                     4 * random.random() + zOffset)
        cloud.setScale(4.0)
        cloud.setTag("number", "%d%d" % (radius, version))

        self.clouds.append([cloud, random.choice(axes)])    


    def loadSkyCollision(self):
        """
        Put a collision plane in the sky so he doesn't fly too high up
        """
        plane = CollisionPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 200)))
        plane.setTangible(0)
        planeNode = CollisionNode("sky_collision") # Previously part of the cloudSpere.
        planeNode.addSolid(plane)
        self.cloudOrigin.attachNewNode(planeNode)

        
    def loadCloudPlatforms(self):      
        self.cloudOrigin = self.geom.attachNewNode("cloudOrigin")
        self.cloudOrigin.setZ(30)

        self.loadSkyCollision()
        
        self.numClouds = 12

        # bottom clouds
        for i in range(self.numClouds):
            self.loadCloud(i, 50, 0)

        # middle clouds
        for i in range(self.numClouds):
            self.loadCloud(i, 70, 30)

        # top clouds
        for i in range(self.numClouds):
            self.loadCloud(i, 30, 60)
            
        self.cloudOrigin.stash()
        
    def __cleanupCloudFadeInterval(self):
        if hasattr(self, "cloudFadeInterval"):
            self.cloudFadeInterval.pause()
            self.cloudFadeInterval = None
            
    def fadeClouds(self):
        self.__cleanupCloudFadeInterval()
            
        self.cloudOrigin.setTransparency(1)
        self.cloudFadeInterval = self.cloudOrigin.colorInterval(
            0.5,
            Vec4(1, 1, 1, int(self.cloudOrigin.isStashed())),
            blendType="easeIn")
        
        if self.cloudOrigin.isStashed():
            self.cloudOrigin.setColor(Vec4(1, 1, 1, 0))
            self.setCloudSwitch(1)
        else:
            self.cloudFadeInterval = Sequence(self.cloudFadeInterval,
                                              Func(self.setCloudSwitch, 0),
                                              Func(self.cloudOrigin.setTransparency, 0))
            
        self.cloudFadeInterval.start()
            
    def setCloudSwitch(self, on):
        self.cloudSwitch = on
        if hasattr(self, "cloudOrigin"):
            if on:
                self.cloudOrigin.unstash()
            else:
                self.cloudOrigin.stash()
                
    def _clearDayChangeInterval(self):
        if hasattr(self, "dayChangeInterval"):
            self.dayChangeInterval.pause()
            self.dayChangeInterval = None
            
    def switchToNight(self):
        self._clearDayChangeInterval()
        self.dayChangeInterval = Sequence(
            self.sunMoonNode.hprInterval(
                5.0,
                Point3(0, -30, 0),
                blendType="easeInOut"
                ),
            Func(base.win.setClearColor, Vec4(0.15, 0.22, 0.14, 1.0))
            )
        self.dayChangeInterval.start()
        
    def switchToDay(self):
        self.dayChangeInterval = Sequence(
            Func(base.win.setClearColor, Vec4(0.47, 0.69, 0.3, 1.0)),
            self.sunMoonNode.hprInterval(
                5.0,
                Point3(0, 30, 0),
                blendType="easeInOut"
                ),
            )
        self.dayChangeInterval.start()
                
    def __handleFireworksStarted(self):
        """
        Hide the clouds during the fireworks show
        """
        assert( self.notify.debug("__handleFireworksStarted") )
        self.sunMoonNode.hide()
        #self.switchToNight()
        #self.music.stop()
    
    def __handleFireworksFinished(self):
        """
        Show the clouds after the fireworks show is over
        """
        assert( self.notify.debug("__handleFireworksFinished") )
        self.sunMoonNode.show()
        #self.switchToDay()
        #base.cr.playGame.getPlace().playMusic()

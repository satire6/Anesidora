from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
import DistributedSuitBase
from direct.task.Task import Task
import random
from toontown.toonbase import ToontownGlobals
from otp.level import LevelConstants
from toontown.distributed.DelayDeletable import DelayDeletable

class DistributedFactorySuit(DistributedSuitBase.DistributedSuitBase,
                             DelayDeletable):

    notify = DirectNotifyGlobal.directNotify.newCategory(
                                        'DistributedFactorySuit')

    def __init__(self, cr):
        """__init__(cr)"""
        try:
            self.DistributedSuit_initialized
        except:
            self.DistributedSuit_initialized = 1
            DistributedSuitBase.DistributedSuitBase.__init__(self, cr)

            # Set up the DistributedSuit state machine
            self.fsm = ClassicFSM.ClassicFSM(
                'DistributedSuit',
                [State.State('Off',
                             self.enterOff,
                             self.exitOff,
                             ['Walk',
                              'Battle']),
                 State.State('Walk',
                             self.enterWalk,
                             self.exitWalk,
                             ['WaitForBattle',
                              'Battle',
                              'Chase']
                             ),
                 State.State('Chase',
                             self.enterChase,
                             self.exitChase,
                             ['WaitForBattle',
                              'Battle',
                              'Return',
                              ]
                             ),
                 State.State('Return',
                             self.enterReturn,
                             self.exitReturn,
                             ['WaitForBattle',
                              'Battle',
                              'Walk']
                             ),
                 State.State('Battle',
                             self.enterBattle,
                             self.exitBattle,
                             ['Walk',
                              'Chase',
                              'Return',]),
                 State.State('WaitForBattle',
                             self.enterWaitForBattle,
                             self.exitWaitForBattle,
                             ['Battle']),
                 ],
                        # Initial state
                        'Off',
                        # Final state
                        'Off',
                       )
            self.path = None
            self.walkTrack = None
            self.chaseTrack = None
            self.returnTrack = None
            self.fsm.enterInitialState()
            self.chasing = 0
            self.paused = 0
            self.pauseTime = 0
            self.velocity = 3
            self.factoryRequest = None
            
        return None

    def generate(self):
        DistributedSuitBase.DistributedSuitBase.generate(self)

    def setLevelDoId(self, levelDoId):
        self.notify.debug("setLevelDoId(%s)" % (levelDoId))
        self.levelDoId = levelDoId

    def setCogId(self, cogId):
        self.cogId = cogId
    def setReserve(self, reserve):
        self.reserve = reserve

    def denyBattle(self):
        # make this a warning so we see it in the logs
        self.notify.warning('denyBattle()')
        
        place = self.cr.playGame.getPlace()
        if place.fsm.getCurrentState().getName() == 'WaitForBattle':
            place.setState('walk')

    def doReparent(self):
        """the reparent may be delayed if our parent hasn't been created
        yet"""
        self.notify.debug("Suit requesting reparenting")
        if not hasattr(self,'factory'):
            self.notify.warning('no factory, get Redmond to look at DistributedFactorySuit.announceGenerate()')
        self.factory.requestReparent(self, self.spec['parentEntId'])
        # set the path the suit walks on
        if self.pathEntId:
            self.factory.setEntityCreateCallback(self.pathEntId,
                                                 self.setPath)
        else:
            self.setPath()

    def setCogSpec(self, spec):
        self.spec = spec
        self.setPos(spec['pos'])
        self.setH(spec['h'])
        self.originalPos = spec['pos']
        self.escapePos = spec['pos']
        self.pathEntId = spec['path']
        self.behavior = spec['behavior']
        self.skeleton = spec['skeleton']
        self.revives = spec.get('revives')
        self.boss = spec['boss']
        # the AI now sets this, it's a required field
        #if self.skeleton:
        #    self.makeSkeleton()
        if self.reserve:
            self.reparentTo(hidden)
        else:
            self.doReparent()

    def comeOutOfReserve(self):
        self.doReparent()

    def getCogSpec(self, cogId):
        if self.reserve:
            return self.factory.getReserveCogSpec(cogId)
        else:
            return self.factory.getCogSpec(cogId)

    def announceGenerate(self):
        self.notify.debug("announceGenerate %s" % self.doId)

        #print "%s: originalPos = %s" % (self.doId, self.originalPos)
        #self.setState('Walk')
        # Since Cogs are not entities, we need to jump through some
        # hoops here. We need to wait until the factory has been generated,
        # then we need to wait until the factory has had a chance to set
        # itself up.
        def onFactoryGenerate(factoryList, self=self):
            self.factory = factoryList[0]
            def onFactoryReady(self=self):
                self.notify.debug("factory ready, read spec")
                spec = self.getCogSpec(self.cogId)
                self.setCogSpec(spec)
                self.factoryRequest = None
            # we can't get the parent node for the cog
            # until the factory's levelMgr has been created
            self.factory.setEntityCreateCallback(LevelConstants.LevelMgrEntId,
                                                 onFactoryReady)
        self.factoryRequest = self.cr.relatedObjectMgr.requestObjects(
            [self.levelDoId], onFactoryGenerate)


        DistributedSuitBase.DistributedSuitBase.announceGenerate(self)
        
    def disable(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject
        //              is removed from active duty and stored in a cache.
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.ignoreAll()
        if self.factoryRequest is not None:
            self.cr.relatedObjectMgr.abortRequest(self.factoryRequest)
            self.factoryRequest = None
        self.notify.debug("DistributedSuit %d: disabling" % self.getDoId())
        self.setState('Off')

        # remove walk track
        if self.walkTrack:
            del self.walkTrack
            self.walkTrack = None
            
        DistributedSuitBase.DistributedSuitBase.disable(self)
        taskMgr.remove(self.taskName('returnTask'))
        taskMgr.remove(self.taskName('checkStray'))
        taskMgr.remove(self.taskName('chaseTask'))
        return

    def delete(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject is
        //              permanently removed from the world and deleted from
        //              the cache.
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        try:
            self.DistributedSuit_deleted
        except:
            self.DistributedSuit_deleted = 1
            self.notify.debug("DistributedSuit %d: deleting" % self.getDoId())

            del self.fsm
            DistributedSuitBase.DistributedSuitBase.delete(self)

    def d_requestBattle(self, pos, hpr):
        """d_requestBattle(toonId)
        """
        # Make sure the local toon can't continue to run around (and
        # potentially start battles with other suits!)
        self.cr.playGame.getPlace().setState('WaitForBattle')

        # lock the factory visibility to the suit's zone
        self.factory.lockVisibility(
            zoneNum=self.factory.getEntityZoneEntId(self.spec['parentEntId']))

        self.sendUpdate('requestBattle', [pos[0], pos[1], pos[2],
                                          hpr[0], hpr[1], hpr[2]])

    def handleBattleBlockerCollision(self):
        """ This function is used the the BattleBlockerEntity to indirectly
        call __handleToonCollision when a toon tries to cross the battle
        blocker collision geom """
        self.__handleToonCollision(None)

        
    def __handleToonCollision(self, collEntry):
        """
        /////////////////////////////////////////////////////////////
        // Function:    This function is the callback for any
        //              collision events that the collision sphere
        //              for this bad guy might receive
        // Parameters:  collEntry, the collision entry object
        // Changes:     None
        /////////////////////////////////////////////////////////////
        """
        if collEntry:
            if collEntry.getFromNodePath().getParent().getKey() != localAvatar.getKey():
                return

        # Hack: Sellbot Warehouse has Cogs standing above the player. Prevent the Cogs'
        # big collision spheres from abducting the player.
        if hasattr(self, 'factory') and hasattr(self.factory, 'lastToonZone'):
            factoryZone = self.factory.lastToonZone
            unitsBelow = self.getPos(render)[2] - base.localAvatar.getPos(render)[2]
            if factoryZone == 24 and unitsBelow > 10.0:
                self.notify.warning('Ignoring toon collision in %d from %f below.' 
                    % (factoryZone, unitsBelow))
                return
                
        if not base.localAvatar.wantBattles:
            return

        toonId = base.localAvatar.getDoId()
        self.notify.debug('Distributed suit %d: requesting a Battle with toon: %d' %
                          (self.doId, toonId))
        self.d_requestBattle(self.getPos(), self.getHpr())

        # the suit on this machine only will go into wait for battle while it
        # is waiting for word back from the server about our battle request
        #
        self.setState('WaitForBattle')

        return None

    def setPath(self):
        self.notify.debug("setPath %s" % self.doId)
        # if a path is not defined, then the suit won't walk
        if self.pathEntId != None:
            # set up the walk heirarchy
            #          parent
            #           |
            #          path
            #           |
            #          idealPathNode
            #           |
            #          suit
            # The idealPathNode exactly follows the path described
            # in the path entity.  If the suit has strayed far enough off the
            # path, he will head back towards the idealPathNode as it
            # is lerped around the path.  As he is heading back, he will
            # course correct several times so he rejoins the path in sync
            # with the idealPathNode's movement.
            parent = self.factory.entities.get(self.spec['parentEntId'])
            self.path = self.factory.entities.get(self.pathEntId)
            assert parent != None
            assert self.path != None
            self.idealPathNode = self.path.attachNewNode("idealPath")
            self.reparentTo(self.idealPathNode)
            self.setPos(0,0,0)
            self.path.reparentTo(parent)

            # make path track
            self.walkTrack = self.path.makePathTrack(self.idealPathNode, self.velocity,
                                                     self.uniqueName("suitWalk"))
            
            
        # Finally we can enter the walk state
        self.setState('Walk')

    def initializeBodyCollisions(self, collIdStr):
        DistributedSuitBase.DistributedSuitBase.initializeBodyCollisions(self, collIdStr)

        # setup a sphere for discovering a nearby toon
        self.sSphere = CollisionSphere(0.0, 0.0, 0.0, 15)
        name = self.uniqueName("toonSphere")
        self.sSphereNode = CollisionNode(name)
        self.sSphereNode.addSolid(self.sSphere)
        self.sSphereNodePath=self.attachNewNode(self.sSphereNode)
        self.sSphereNodePath.hide()
        self.sSphereBitMask = ToontownGlobals.WallBitmask
        self.sSphereNode.setCollideMask(self.sSphereBitMask)
        self.sSphere.setTangible(0)
        self.accept("enter" + name, self.__handleToonCollision)

    def enableBattleDetect(self, name, handler):
        DistributedSuitBase.DistributedSuitBase.enableBattleDetect(self,name,handler)
        self.lookForToon(1)

    def disableBattleDetect(self):
        DistributedSuitBase.DistributedSuitBase.disableBattleDetect(self)
        self.lookForToon(0)
        
    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    # Defined in DistributedSuitBase.py

    def subclassManagesParent(self):
        return 1

    ########## Walk state and detect toon functions  ###########

    def enterWalk(self, ts=0):
        self.enableBattleDetect('walk', self.__handleToonCollision)
        # create the walk track if we have a path
        if self.path:
            if self.walkTrack:
                self.walkTrack.loop()
                self.walkTrack.pause()
                if self.paused:
                    self.walkTrack.setT(self.pauseTime)
                else:
                    self.walkTrack.setT(ts)
                self.walkTrack.resume()
            self.loop('walk', 0)
            self.paused = 0
        else:
            # Just stand here waiting for a toon to approach.
            self.loop('neutral', 0)
            
    def exitWalk(self):
        self.disableBattleDetect()
        if self.walkTrack:
            self.pauseTime = self.walkTrack.pause()
            self.paused = 1
        return

    def lookForToon(self, on=1):
        if self.behavior in ['chase']:
            if on:
                self.accept(self.uniqueName("entertoonSphere"), self.__handleToonAlert)
            else:
                self.ignore(self.uniqueName("entertoonSphere"))
            
    def __handleToonAlert(self, collEntry):
        # TODO: check toonpos against the FOV of the suit
        self.notify.debug("%s: ahah!  i saw you" % self.doId)
        # check the z's, make sure they are the same
        toonZ = base.localAvatar.getZ(render)
        suitZ = self.getZ(render)
        dZ = abs(toonZ-suitZ)
        # check if toon is on this floor
        # (assume space between floor and ceiling is at least 8 feet)
        if dZ < 8.0:
            self.sendUpdate("setAlert", [base.localAvatar.doId])

    # Needed by DistributedSuitBase.denyBattle
    def resumePath(self, state):
        # go back to walk state
        self.setState('Walk')
        
    ########## Chase state and check stray functions ##########
    

    def enterChase(self):
        self.enableBattleDetect('walk', self.__handleToonCollision)
        self.startChaseTime = globalClock.getFrameTime()
        # Start checking if we've strayed too far (or too long)
        self.startCheckStrayTask(1)
        self.startChaseTask()
        
    def exitChase(self):
        self.disableBattleDetect()
        taskMgr.remove(self.taskName('chaseTask'))
        # Stop the chase track
        if self.chaseTrack:
            self.chaseTrack.pause()
            del self.chaseTrack
            self.chaseTrack = None
        self.chasing = 0
        # Stop checking if we've strayed
        self.startCheckStrayTask(0)

    def setConfrontToon(self, avId):
        self.notify.debug('DistributedFactorySuit.setConfrontToon %d' % avId)
        self.chasing = avId
        self.setState("Chase")

    def startChaseTask(self, delay=0):
        self.notify.debug('DistributedFactorySuit.startChaseTask delay=%s' % delay)
        taskMgr.remove(self.taskName('chaseTask'))
        taskMgr.doMethodLater(delay,
                              self.chaseTask,
                              self.taskName('chaseTask'))

    def chaseTask(self, task):
        # Chase an avatar around
        if not self.chasing:
            return Task.done
        
        # make sure avatar exists
        av = base.cr.doId2do.get(self.chasing, None)
        if not av:
            self.notify.warning("avatar %s isn't here to chase" % self.chasing)
            return Task.done

        # check how long we've been chasing
        if (globalClock.getFrameTime() - self.startChaseTime > 3.0):
            self.setReturn()
            return Task.done
        
        toonPos = av.getPos(self.getParent())
        suitPos = self.getPos()
        distance = Vec3(suitPos-toonPos).length()
        
        # chase this toon
        if self.chaseTrack:
            self.chaseTrack.pause()
            del self.chaseTrack
            self.chaseTrack = None
            
        import random
        rand1 = .5
        rand2 = .5
        rand3 = .5
        # randomize the position a bit, so cogs don't stack up
        targetPos = Vec3(toonPos[0] + (4.0 * (rand1 - .5)),
                         toonPos[1] + (4.0 * (rand2 - .5)),
                         suitPos[2])
        track = Sequence(Func(self.headsUp,
                              targetPos[0],targetPos[1],targetPos[2]),
                         Func(self.loop, 'walk', 0))
        chaseSpeed = 4.0
        duration = distance / chaseSpeed
        track.extend([LerpPosInterval(self, duration=duration,
                                      pos = Point3(targetPos),
                                      startPos = Point3(suitPos)),
                      ])
        self.chaseTrack = track
        self.chaseTrack.start()

        # course correct every second
        self.startChaseTask(1.0)
    
    def startCheckStrayTask(self, on=1):
        taskMgr.remove(self.taskName("checkStray"))
        if on:
            taskMgr.add(self.checkStrayTask,
                        self.taskName("checkStray"))
            
    def checkStrayTask(self, task):
        curPos = self.getPos()
        distance = Vec3(curPos - self.originalPos).length()
        if distance > 10.0:
            self.sendUpdate("setStrayed", [])
            

    ############# Return state ##############
            
    def enterReturn(self):
        # Return the cog to it's starting position

        # specifically disable looking for toons on the way back
        # but it is ok to battle them if we actually bump into them
        self.enableBattleDetect('walk', self.__handleToonCollision)
        self.lookForToon(0)
        #if not self.chasing:
        #    return

        # return to where we should be
        self.startReturnTask()


    def exitReturn(self):
        self.disableBattleDetect()
        taskMgr.remove(self.taskName("checkStray"))
        taskMgr.remove(self.taskName('returnTask'))
        if self.returnTrack:
            self.returnTrack.pause()
            self.returnTrack = None

    def setReturn(self):
        # put suit in walk state if not already in walk state
        self.notify.debug('DistributedFactorySuit.setReturn')
        self.setState('Return')

    def startReturnTask(self, delay=0):
        taskMgr.remove(self.taskName('returnTask'))
        taskMgr.doMethodLater(delay,
                              self.returnTask,
                              self.taskName('returnTask'))
        
    def returnTask(self, task):
        # return to parent node, which is the idealPathNode
        # first, do a straight reparent to our original parent
        self.factory.requestReparent(self, self.spec['parentEntId'])

        # if we are on a path, or just the original pos
        # if it is a static suit
        if self.returnTrack:
            self.returnTrack.pause()
            self.returnTrack = None

        # find where to head back to
        if self.path:
            # head back to our parent, the idealPathNode
            targetPos = VBase3(0,0,0)
        else:
            # head to the origin
            targetPos = self.originalPos
            
        track = Sequence(Func(self.headsUp, 
                              targetPos[0],
                              targetPos[1],
                              targetPos[2]),
                         Func(self.loop, 'walk', 0))
        curPos = self.getPos()
        distance = Vec3(curPos - targetPos).length()
        duration = distance / 3.0
        track.append(LerpPosInterval(self, duration=duration,
                                     pos = Point3(targetPos),
                                     startPos = Point3(curPos)))
        track.append(Func(self.returnDone))
        self.returnTrack = track
        self.returnTrack.start()

    def returnDone(self):
        assert self.notify.debug("returnDone")
        # Reset hpr
        self.setHpr(self.spec['h'],0,0)
        self.setState("Walk")
        # Return to neutral animation if not on a path
        if not self.path:
            self.loop('neutral')
        
    def setActive(self, active):
        # suit is being put into action by AI, or it is being
        # told to take a break.  The initial active position is
        # given by self.originalPos.  The position the suit goes
        # to take a break is self.escapePos

        if active:
            # put into walk state
            self.setState('Walk')
        else:
            # put into off state
            self.setState('Off')
            
    def disableBattleDetect(self):
        if self.battleDetectName:
            self.ignore("enter" + self.battleDetectName)
            self.battleDetectName = None
        if self.collNodePath:
            self.collNodePath.removeNode()
            self.collNodePath = None
            
    def disableBodyCollisions(self):
        self.disableBattleDetect()
        self.enableRaycast(0)
        if self.cRayNodePath:
            self.cRayNodePath.removeNode()
        if hasattr(self, "cRayNode"):
            del self.cRayNode
        if hasattr(self, "cRay"):
            del self.cRay
        if hasattr(self, "lifter"):
            del self.lifter
            
    def removeCollisions(self):
        """
        clean up the suit's various collision data such
        as the battle detection sphere, the ground collision
        ray, and the lifter
        """
        # make sure to remove any raycast information
        #
        self.enableRaycast(0)
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.lifter = None
        self.cTrav = None
        
    def setVirtual(self, isVirtual = 1):
        self.virtual = isVirtual
        if self.virtual:
            actorNode = self.find("**/__Actor_modelRoot")
            actorCollection = actorNode.findAllMatches("*")
            parts = ()
            for thingIndex in range(0,actorCollection.getNumPaths()):
                thing = actorCollection[thingIndex]
                if thing.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                    thing.setColorScale(1.0,0.0,0.0,1.0)
                    thing.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                    thing.setDepthWrite(False)
                    thing.setBin('fixed', 1)

        
    def getVirtual(self):
        return self.virtual
        
    ##### Battle state #####

    # Defined in DistributedSuitBase.py

    ##### WaitForBattle state #####

    # Defined in DistributedSuitBase.py

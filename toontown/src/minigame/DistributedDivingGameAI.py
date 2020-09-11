"""DistributedDivingGameAI module: contains the DistributedDivingGameAI class"""

from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.actor import Actor
import DivingGameGlobals
#import DistributedSharkAI
import random
import random
import types

class DistributedDivingGameAI(DistributedMinigameAI):
    
    fishProportions = []
    
    # Fish proportions 
    for i in range(6):
        fishProportions.append([])
    
    n = 100
    
    # proportions work as such, divide up from 0-1 between them all.  When
    # that spawner spawns, it does random.random, and the area in range it touches
    # will determine the type of fish that spawns.
    # right now, all zones have the same type.  
    # it would be kind of cool if each zone had different fish, so maybe people
    # won't see nurse sharks until they get to Daisy's Garden or something like that
    
    # clownfish, pbj-fish, bear-acuda, balloonfish, nurse shark, piano Tuna
    # n means no chance of spawning
    
    # toon town central
    fishProportions[0]
    fishProportions[0].append(([0,.8], [.8, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[0].append(([0,.8], [.8, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[0].append(([0,.7], [.7, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[0].append(([0,.7], [.7, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[0].append(([0, .5], [.5, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[0].append(([n, .5], [.5, 1],[n, n],[n, n],[n, n],[n, n]))
    #self.fishProportions[0].append(([0,1], [n, n],[n, n],[n, n],[n, n],[n, n]))
    #self.fishProportions[0].append(([n, n], [0, 1],[n, n],[n, n],[n, n],[n, n]))
    #self.fishProportions[0].append(([n,n], [n, n],[0 , 1],[n, n],[n, n],[n, n]))
    #self.fishProportions[0].append(([n,n], [n, n],[n, n],[0, 1],[n, n],[n, n]))
    #self.fishProportions[0].append(([n,n], [n, n],[n, n],[n, n],[0, 1],[n, n]))
    #self.fishProportions[0].append(([n,n], [n, n],[n, n],[n, n],[n, n],[0, 1]))

    # donald's dock, first sight of the piano tuna
    fishProportions[1]
    fishProportions[1].append(([0,.8], [.8, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[1].append(([0,.8], [.8, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[1].append(([0,.7], [.7, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[1].append(([0,.7], [.7, .9],[n, n],[n, n],[n, n],[.9, 1]))
    fishProportions[1].append(([0, .4], [.4, .8],[n, n],[n, n],[n, n],[.8, 1]))
    fishProportions[1].append(([n, .3], [.3, .6],[n, n],[n, n],[n, n],[.6, 1]))
   
    # daisy gardens, first sight of the balloonfish
    fishProportions[2]
    fishProportions[2].append(([0,.7], [.7, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[2].append(([0,.6], [.6, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[2].append(([0,.6], [.6, .8],[n, n],[.8, 1],[n, n],[n, n]))
    fishProportions[2].append(([0,.5], [.5, .7],[n, n],[.7, .9],[n, n],[.9, 1]))
    fishProportions[2].append(([0, .2], [.2, .4],[n, n],[.4, .75],[n, n],[.75, 1]))
    fishProportions[2].append(([n, .2], [.2, .6],[n, n],[.6, .8],[n, n],[.8, 1]))
    
    # minnie melody land, first sight of the nurse shark
    fishProportions[3]
    fishProportions[3].append(([0,.7], [.7, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[3].append(([0,.6], [.6, 1],[n, n],[n, n],[n, n],[n, n]))
    fishProportions[3].append(([0,.6], [.6, .8],[n, n],[.95, 1],[n, n],[n, n]))
    fishProportions[3].append(([0,.5], [.5, .7],[n, n],[.7, .85],[.9, .95],[.95, 1]))
    fishProportions[3].append(([0, .2], [.2, .4],[n, n],[.4, .75],[.75, .85],[.85, 1]))
    fishProportions[3].append(([n, .2], [.2, .6],[n, n],[.6, .8],[n, n],[.8, 1]))
    
    # the brrrgh, might be nice for the frozen fish to appear,
    # but for now, it just has a lot more piano tuna
    fishProportions[4]
    fishProportions[4].append(([0,.7], [.7, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[4].append(([0,.45], [.45, .9],[n, n],[.9, 1],[n, n],[n, n]))
    fishProportions[4].append(([0,.2], [.2, .5],[n, n],[.5, .95],[.95, 1],[n, n]))
    fishProportions[4].append(([0,.1], [.1, .3],[n, n],[.3, .75],[.75, .8],[.8, 1]))
    fishProportions[4].append(([n, n], [0, .15],[n, n],[.15, .4],[n, n],[.4, 1]))
    fishProportions[4].append(([n, n], [n, n],[n, n],[0, .4],[n, n],[.6, 1]))
    
    # donald's dreamland
    fishProportions[5]
    fishProportions[5].append(([0,.7], [.7, .9],[.9, 1],[n, n],[n, n],[n, n]))
    fishProportions[5].append(([0,.45], [.45, .9],[n, n],[.9, 1],[n, n],[n, n]))
    fishProportions[5].append(([0,.2], [.2, .5],[n, n],[.5, .95],[.95, 1],[n, n]))
    fishProportions[5].append(([0,.1], [.1, .3],[n, n],[.3, .75],[.75, .8],[.8, 1]))
    fishProportions[5].append(([n, n], [0, .15],[n, n],[.15, .4],[n, n],[.4, 1]))
    fishProportions[5].append(([n, n], [n, n],[n, n],[0, .4],[n, n],[.6, 1]))
    
    # difficulty pattern for the AI, 
    # time between spawns
    # types of spawns
    # reward modifier
            
    difficultyPatternsAI = {
        ToontownGlobals.ToontownCentral:
        [ 3.5, fishProportions[0], 1.5
          ],
        ToontownGlobals.DonaldsDock:
        [ 3.0, fishProportions[1], 1.8
          ],
        ToontownGlobals.DaisyGardens:
        [ 2.5, fishProportions[2], 2.1
          ],
        ToontownGlobals.MinniesMelodyland:
        [ 2.0, fishProportions[3], 2.4
          ],
        ToontownGlobals.TheBrrrgh:
        [ 2.0, fishProportions[4], 2.7
          ],
        ToontownGlobals.DonaldsDreamland:
        [ 1.5, fishProportions[5], 3.0
          ],
        }

    def __init__(self, air, minigameId):
        try:
            self.DistributedDivingGameAI_initialized
        except:
            self.DistributedDivingGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedDivingGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['swimming']),
                                    State.State('swimming',
                                                self.enterSwimming,
                                                self.exitSwimming,
                                                ['cleanup']),
                                    State.State('cleanup',
                                                self.enterCleanup,
                                                self.exitCleanup,
                                                ['inactive']),
                                    ],
                                   # Initial State
                                   'inactive',
                                   # Final State
                                   'inactive',
                                   )

            # Add our game ClassicFSM to the framework ClassicFSM
            self.addChildGameFSM(self.gameFSM)

            #self.__timeBase = globalClock.getRealTime()
            self.__timeBase = globalClockDelta.localToNetworkTime(globalClock.getRealTime())

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")        
        self.sendUpdate("setTrolleyZone", [self.trolleyZone])
        #self.shark=DistributedSharkAI.DistributedSharkAI(self.air,self.doId)
        #self.shark.generateWithRequired(self.zoneId)
        

        # reset scores
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0
            

        self.SPAWNTIME = self.difficultyPatternsAI[self.getSafezoneId()][0]
        self.proportion = self.difficultyPatternsAI[self.getSafezoneId()][1]
        self.REWARDMOD = self.difficultyPatternsAI[self.getSafezoneId()][2]
        
        DistributedMinigameAI.setGameReady(self)
        self.spawnings = []
        
        # note, there is a bit of randomness to spawn numbers
        for i in range(DivingGameGlobals.NUM_SPAWNERS):
            self.spawnings.append(Sequence(Func(self.spawnFish,i),Wait(self.SPAWNTIME+random.random()),Func(self.spawnFish,i),Wait(self.SPAWNTIME-.5+random.random())))
            self.spawnings[i].loop()    
        

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        DistributedMinigameAI.setGameStart(self, timestamp)
        self.gameFSM.request('swimming')
        
        self.scoreTracking = {}

        for avId in self.scoreDict.keys():
            self.scoreTracking[avId] = [0,0,0,0,0] #0fishhits, 1crabhits, 2treasure catches, 3treasure drops, 4treasure Recoveries

    # called from the client
    # says that a crab is done moving, AI should tell the client's
    # how the crab should next move
    def getCrabMoving(self, crabId, crabX, dir):
        timestamp = globalClockDelta.getFrameNetworkTime()
        
        # pseudo random numbers
        rand1 = int(random.random()*10)
        rand2 = int(random.random()*10)
        
        self.sendUpdate("setCrabMoving", [crabId, timestamp, rand1, rand2, crabX, dir])
        
    # called from the client
    # says a toon has reached the boat with a treasure
    # AI calls to increment score, along with a new spot for the treasure to spawn
    def treasureRecovered(self):
        if not hasattr(self, "scoreTracking"):
            return
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'DivingGameAI.treasureRecovered: invalid avId')
            return
        timestamp = globalClockDelta.getFrameNetworkTime()
        newSpot = int(random.random() * 30)
        
        self.scoreTracking[avId][4] += 1
        
        # increment scores in AI
        for someAvId in self.scoreDict.keys():
            if someAvId == avId:#reward to carrier
                self.scoreDict[avId] += 10 * (self.REWARDMOD * 0.25)
                    
            self.scoreDict[someAvId] += 10 * ((self.REWARDMOD * 0.75)/ float(len(self.scoreDict.keys())))
            
        self.sendUpdate("incrementScore", [avId, newSpot, timestamp])
        
    def hasScoreMult(self):
        return 0
        
    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        taskMgr.remove(self.taskName("gameTimer"))
        
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        self.gameFSM.request('cleanup')
        DistributedMinigameAI.gameOver(self)
        trackingString = "MiniGame Stats : Diving Game"
        trackingString += ("\nDistrict:%s" % (self.getSafezoneId()))
        for avId in self.scoreTracking.keys():
            trackingString = trackingString + ("\navId:%s fishHits:%s crabHits:%s treasureCatches:%s treasureDrops:%s treasureRecoveries:%s Score: %s" % (avId, self.scoreTracking[avId][0],self.scoreTracking[avId][1],self.scoreTracking[avId][2],self.scoreTracking[avId][3],self.scoreTracking[avId][4], self.scoreDict[avId]))
        #print trackingString
        self.air.writeServerEvent("MiniGame Stats", None, trackingString)        
        #print self.scoreTracking
        #import pdb; pdb.set_trace()        

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def getTimeBase(self):
        return self.__timeBase

    def enterSwimming(self):
        self.notify.debug("enterSwimming")
        
        duration = 65.
        
        taskMgr.doMethodLater(duration,
                              self.timerExpired,
                              self.taskName("gameTimer"))
                                  
        #def enterPlay(self):
        #self.notify.debug("enterPlay")

        
        # Start the game timer
        #if not config.GetBool('endless-cannon-game', 0):
            #taskMgr.doMethodLater(CannonGameGlobals.GameTime,
                                  #self.timerExpired,
                                  #self.taskName("gameTimer"))

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        #print "time to kick everyone out"
        
        # make sure players get at least 5
        for avId in self.scoreDict.keys():
            if self.scoreDict[avId] < 5:
                self.scoreDict[avId] = 5
            
            
        self.gameOver()
        return Task.done
        
    def exitSwimming(self):
        for i in range(DivingGameGlobals.NUM_SPAWNERS):
            self.spawnings[i].pause()

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        # call this when the game is done
        # clean things up in this class
        for i in range(DivingGameGlobals.NUM_SPAWNERS):
            self.spawnings[i].finish()
            
        del self.spawnings
        
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
    
    # called by a client when they try to pick up a treasure
    # tells all the clients that a certain Avid picked it up
    def pickupTreasure(self, chestId):
        if not hasattr(self, "scoreTracking"):
            return        
        timestamp = globalClockDelta.getFrameNetworkTime()
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'DivingGameAI.pickupTreasure: invalid avId')
            return
        #self.shark.followDude(avId)
        self.scoreTracking[avId][2] += 1
        self.sendUpdate("setTreasureGrabbed", [avId, chestId])
    
    # figures out what fish to spawn, and informs the clients to spawn it
    def spawnFish(self, spawnerId):
        timestamp = globalClockDelta.getFrameNetworkTime()
        
        props = self.proportion[spawnerId]
        num = random.random()
        
        for i in range(len(props)):
            prop = props[i]
            low = prop[0]
            high = prop[1]
            if num > low and num <= high:
                offset = int(10*random.random())
                self.sendUpdate("fishSpawn", [timestamp, i, spawnerId, offset])
                return
    
    # simplified handleFishCollision
    def handleCrabCollision(self, avId, status):
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'DivingGameAI.handleCrabCollision: invalid avId')
            return
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate("setTreasureDropped", [avId, timestamp])
        self.scoreTracking[avId][1] += 1
        if status == 'normal' or status == 'treasure':
            timestamp = globalClockDelta.getFrameNetworkTime()
            self.sendUpdate("performCrabCollision", [avId, timestamp])
            if status == 'treasure':
                self.scoreTracking[avId][3] += 1
    
    # called from client when a player collides with a fish
    # also drops treasure
    def handleFishCollision(self, avId, spawnId, spawnerId, status):
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'DivingGameAI.handleFishCollision: invalid avId')
            return
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate("setTreasureDropped", [avId, timestamp]) # returns the treasure to render, and freezes avId
        
        # with this part commented out, now we make it that a person who
        # is frozen in the water from a collision, will still manage to 
        # block oncoming fish.  Thus creating floating walls.  This might
        # help people on teamwork.
        
        # in perform***Collision, it will only freeze the player if they are in
        # normal or treasure
        
        #if status == 'normal' or status == 'treasure':
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.scoreTracking[avId][0] += 1
        if status == 'treasure':
            self.scoreTracking[avId][3] += 1
        self.sendUpdate("performFishCollision", [avId, spawnId, spawnerId, timestamp])
        


from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.ClockDelta import NetworkTimePrecision
import random
from direct.task.Task import Task

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.directutil import Mopath
from toontown.toonbase import ToontownGlobals
from direct.actor import Actor

# This class is more accurately a train TRACK, it handles many trains moving
# across sequentially

class Train(DirectObject): 

    notify = directNotify.newCategory('Train')
    #notify.setDebug(True)

    nameId = 0
    Sfx_TrainPass = 'phase_10/audio/sfx/CBHQ_TRAIN_pass.mp3'
    Sfx_TrainStopStart = 'phase_10/audio/sfx/CBHQ_TRAIN_stopstart.mp3'
    LocomotiveFile = 'phase_10/models/cogHQ/CashBotLocomotive'
    CarFiles = ['phase_10/models/cogHQ/CashBotBoxCar',
                'phase_10/models/cogHQ/CashBotTankCar',
                'phase_10/models/cogHQ/CashBotFlatCar'
                ]
    CarLength = 88

    # this indicates the longest a train will take to cross the track
    MarkDelta = 15 #seconds

    def __init__(self, trackStartPos, trackEndPos, trackNum, numTotalTracks):
        self.trackStartPos = trackStartPos
        self.trackEndPos = trackEndPos
        self.numCars = len(self.CarFiles)

        # load up the models for the locomotive and the cars
        self.locomotive = loader.loadModel(self.LocomotiveFile)
        self.cars = []

        self.trainPassingSfx = base.loadSfx(self.Sfx_TrainPass)
        self.trainStopStartSfx = base.loadSfx(self.Sfx_TrainStopStart)

        self.trainId = trackNum

        # flip the models if the tracks run the opposite direction
        self.bFlipped = False
        if (trackStartPos[0] < trackEndPos[0]):
            self.locomotive.setHpr(180, 0, 0)
            self.bFlipped = True

        self.collNodeName = 'CollNode-%s' % self.trainId

        # get initial start time
        self.firstMark = (self.MarkDelta / numTotalTracks) * trackNum
        currentTime = self.__networkTimeInSeconds()
        currentRun = int((currentTime - self.firstMark) / self.MarkDelta)
        self.lastMark = (currentRun * self.MarkDelta) + self.firstMark

        # start a run
        self.doNextRun(True)
        self.hide()

    def hide(self):
        if self.locomotive:
            self.locomotive.reparentTo(hidden)

    def show(self):
        if self.locomotive:
            self.locomotive.reparentTo(render)

    def __networkTimeInSeconds(self):
        time = globalClockDelta.getRealNetworkTime(bits=32) / NetworkTimePrecision
        return time
            
    # this gets a new set of cars, sets up a lerp track for the
    # next run and starts the run

    # A) first time through - get the last start time and start the interval in the middle
    # B) the last run started less than MarkDelta ago - start a new run sometime in the future
    # C) the last run started more than MarkDelta ago - start a new run in the middle 
    
    def doNextRun(self, bFirstRun=False):
        if self.locomotive:
            if bFirstRun:
                # make sure to start this one at the previous mark
                nextMark = self.lastMark
            else:
                nextMark = self.lastMark + self.MarkDelta
                self.nextRun.finish()

            self.notify.debug("Next mark %s" % nextMark)
            currentTime = self.__networkTimeInSeconds()

            # positive=not ready yet, negative=we're late
            timeTillNextMark = nextMark - currentTime

            self.notify.debug("Time diff %s" % timeTillNextMark)

            #the next run starts at the next multiple of self.MarkDelta
            runNumber = int((nextMark-self.firstMark) / self.MarkDelta)

            # set up next Run Interval
            S = random.getstate()
            random.seed(self.trainId + runNumber)
            self.nextRun = self.__getNextRun()
            random.setstate(S)

            self.__startNextRun(timeTillNextMark)
            self.lastMark = nextMark
        return Task.done

    def __startNextRun(self, timeTillMark):
        if self.locomotive:
            self.__disableCollisions()
            if timeTillMark > 0:
                self.nextRun = Sequence(Wait(timeTillMark), self.nextRun)
                self.nextRun.start()
            else:
                #we're late!
                self.nextRun.start(-1*timeTillMark)
            self.__enableCollisions()

        return Task.done

    # clean up the self.cars array
    def __cleanupCars(self):
        # remove the cars from the last run
        self.__disableCollisions()
        for car in self.cars:
            car.removeNode()
        self.cars = []

    # set up the self.cars array with a random set of cars and
    # parent them to the locomotive
    def __getCars(self):
        self.__cleanupCars()
        numCarsThisRun = random.randrange(1, 10)
        for nCar in range(numCarsThisRun):
            carType = random.randrange(0, self.numCars)
            car = loader.loadModel(self.CarFiles[carType])
            car.reparentTo(self.locomotive)
            car.setPos(self.CarLength*(nCar+1), 0, 0)
            self.cars.append(car)

    def __showStart(self):
        self.notify.debug("Starting train %s at %s." % (self.trainId,self.__networkTimeInSeconds()))
            
    # set up a Lerp track for the upcoming run.  The final task
    # is a call to doNextRun.  It is up to doNextRun to determine
    # if another run should be made
    def __getNextRun(self):
        self.__getCars()
        trainShouldStop = random.randrange(0, 4)
        nextRun = Sequence(Func(self.__showStart))
        if trainShouldStop is 0:
            waitTime = 3 #this is how long the delay is in the effect
            totalTime = random.randrange(4, (self.MarkDelta-waitTime)/2)
            sfxStopTime = 4.3 #this is where the train stops in the effect
            halfway = (self.trackStartPos + self.trackEndPos) / 2
            halfway.setX(150)
            nextRun.append( \
                Parallel(
                    Sequence(
                        Wait(totalTime-sfxStopTime),
                        SoundInterval(self.trainStopStartSfx, volume = 0.5),
                        ),
                    Sequence(
                        LerpPosInterval(self.locomotive, totalTime, halfway, self.trackStartPos, blendType = "easeInOut"),
                        WaitInterval(waitTime),
                        LerpPosInterval(self.locomotive, totalTime, self.trackEndPos, halfway, blendType = "easeIn"),
                        )
                    )
                )
        else:
            totalTime = random.randrange(6, self.MarkDelta-1)
            #match up the middle of the run time to the middle of the sfx time
            sfxTime = 7
            sfxStartTime = (totalTime/2) - (sfxTime/2)
            if self.bFlipped:
                sfxStartTime -= 1
            else:
                sfxStartTime += 1
            nextRun.append( \
                Parallel(
                    Sequence(
                        Wait(sfxStartTime),
                        SoundInterval(self.trainPassingSfx, volume = 0.5),
                        ),
                    LerpPosInterval(self.locomotive, totalTime, self.trackEndPos, self.trackStartPos),
                    )
                )

        nextRun.append( Func(self.doNextRun) )

        return nextRun

    def delete(self):
        self.__cleanupCars()
        self.locomotive.removeNode()
        self.locomotive = None
        self.nextRun.finish()
        self.nextRun = None
        del self.trainPassingSfx
        del self.trainStopStartSfx

    def uniqueName(self, name):
        Train.nameId += 1
        return (name + '-%d' % Train.nameId)

    def __enableCollisions(self):
        # find the collision nodes in the locomotive and cars
        allColls = self.locomotive.findAllMatches('**/+CollisionNode')
        for car in self.cars:
            carColls = car.findAllMatches('**/+CollisionNode')
            allColls += carColls

        #rename these based off the trainId
        for collNode in allColls:
            collNode.setName(self.collNodeName)
            collNode.setCollideMask(ToontownGlobals.WallBitmask)

        self.accept('enter' + self.collNodeName, self.__handleCollisionSphereEnter)

    def __disableCollisions(self):
        # stop listening for toons.
        self.ignore('enter' + self.collNodeName)
        #self.collisionNode.setCollideMask(BitMask32(0))
    
    def __handleCollisionSphereEnter(self, collEntry=None):
        # Response for the train hitting a toon
        assert(self.notify.debug("Entering collision sphere..."))
        base.localAvatar.b_squish(10)

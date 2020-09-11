from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.golf import DistributedGolfHoleAI
from pandac.PandaModules import *
from direct.fsm.FSM import FSM
from toontown.ai.ToonBarrier import *
from toontown.golf import GolfGlobals


# At one time golf course holds a single set of golfers and a single hole. 

# It is reponsible for changing the hole and holding all between hole data
# including links to the avatars. It does not hold golf balls or run the game
# that is handled by the golfHole

# This class is largely based off of the minigame framework

# Codes to indicate avatar state
INITIAL = 0
EXITED = 1
EXPECTED = 2
JOINED = 3
READY = 4
ONHOLE = 5
BALLIN = 6

JOIN_TIMEOUT = 30
READY_TIMEOUT = 30
EXIT_TIMEOUT = 30
REWARD_TIMEOUT = 30


class DistributedGolfCourseAI(DistributedObjectAI.DistributedObjectAI, FSM):
    notify = directNotify.newCategory("DistributedGolfCourseAI")
    defaultTransitions = {
        'Off'                : [ 'WaitJoin',],
        'WaitJoin'           : [ 'WaitReadyCourse', 'Cleanup'],
        'WaitReadyCourse'    : [ 'WaitReadyHole', 'Cleanup'],
        'WaitReadyHole'      : [ 'PlayHole', 'Cleanup', "WaitLeaveHole", 'WaitReward'],
        'PlayHole'           : [ 'PlayHole', 'WaitLeaveHole', 'Cleanup' , 'WaitReward'],
        'WaitLeaveHole'      : [ 'WaitReadyHole', 'WaitLeaveCourse', 'Cleanup', 'WaitReward'],
        'WaitReward'         : [ 'WaitLeaveCourse', 'Cleanup', 'WaitLeaveHole'],
        'WaitLeaveCourse'    : [ 'Cleanup', ],
        'Cleanup'            : [ 'Off' ],
    }
    
    def __init__(self, zoneId, avIds, courseId, preferredHoleId = None):
        FSM.__init__( self, "GolfCourse_%s_FSM" % ( zoneId ) )
        DistributedObjectAI.DistributedObjectAI.__init__(self, simbase.air)
        self.notify.debug("GOLF COURSE: init")
        self.zoneId = zoneId
        self.currentHole = None
        #self.currentHole = DistributedGolfHoleAI.DistributedGolfHoleAI(self.zoneId, golfCourse = self)
        #self.currentHole.generateWithRequired(self.zoneId)

        # avatars that will play the game
        self.avIdList = []
        self.avStateDict = {}
        
        self.addExpectedGolfers(avIds)
        self.courseId = courseId
        self.preferredHoleId = preferredHoleId
        self.courseInfo = GolfGlobals.CourseInfo[self.courseId]
        self.numHoles = self.courseInfo['numHoles']
        self.holeIds = self.calcHolesToUse()
        self.notify.debug('self.holeIds = %s' % self.holeIds)
        self.numHolesPlayed = 0
        self.curHoleIndex = 0

        self.trophyListLen = 0
        self.courseBestListLen = 0
        self.holeBestListLen = 0
        self.cupListLen = 0

        self.scores = {} # scores of each toon
        self.aimTimes = {} # total aim times of each toon
        self.startingHistory = {} # the golf history of the toons before the course starts
        self.endingHistory = {} # the golf history of the toons after the course ends
        self.startingHoleBest = {}  
        self.endingHoleBest = {}
        self.startingCourseBest = {}
        self.endingCourseBest = {}
        self.startingCups = {}
        self.endingCups = {}
        self.initHistory()
        self.newTrophies = {} # when they finish the course, the new trophies each toon receives
        self.newHoleBest = {} # when they finish the course, the new hole best each toon receives
        self.newCourseBest = {} # when they finish the course, the new course besteach toon receives
        self.newCups = {}
        self.drivingToons = [] # list of toons who can cheat and drive the ball
        
        self.__barrier = None
        self.winnerByTieBreak = 0

    def initHistory(self):
        """Make a copy of the avatars golf history for us to manipulate."""
        for avId in self.avIdList:
            av = simbase.air.doId2do.get(avId)
            if av:
                history = av.getGolfHistory()
                self.startingHistory[avId] = history[:]
                self.endingHistory[avId] = history[:]
                holeBest = av.getGolfHoleBest()
                self.startingHoleBest[avId] = holeBest[:]
                self.endingHoleBest[avId] = holeBest[:]
                courseBest = av.getGolfCourseBest()
                self.startingCourseBest[avId] = courseBest[:]
                self.endingCourseBest[avId] = courseBest[:]
        
    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)
        
        # WARNING remove this line or else it will leak
        # simbase.golfCourse = self

        self.grabGolfers()

    def delete(self):
        self.notify.debug("GOLF COURSE: delete: deleting AI GolfCourse object")
        if hasattr(self, 'rewardBarrier'):
            self.rewardBarrier.cleanup()
            del self.rewardBarrier
        if self.currentHole:
            self.notify.debug('calling requestDelete on hole %d' % self.currentHole.doId)
            self.currentHole.requestDelete()
            self.currentHole = None

        self.ignoreAll()
        # tell GolfManagerAI to remove us
        # TODO figure out why the import doesn't work at the top of the file
        from toontown.golf import GolfManagerAI
        GolfManagerAI.GolfManagerAI().removeCourse(self)
        if self.__barrier:
            self.__barrier.cleanup()
            self.__barrier = None
        DistributedObjectAI.DistributedObjectAI.delete(self)

        
    def load(self):
        self.b_setCourseReady()
        self.request('WaitReadyCourse')
        
    def getZoneId(self):
        return self.zoneId
        
    def addExpectedGolfers(self, avIdList):
        self.notify.debug("Sending %s to course %s" % (avIdList, self.zoneId))
        for avId in avIdList:
            golfer = simbase.air.doId2do.get(avId)
            if golfer:
                if avId not in self.avIdList:
                    self.avIdList.append(avId)
                    self.avStateDict[avId] = INITIAL
                    #if self.isGenerated():
                    #    golfer.sendUpdate("sendToGolfCourse", [self.zoneId])
                elif self.avStateDict[avId] == EXITED:
                    if self.isGenerated():
                        #golfer.sendUpdate("sendToGolfCourse", [self.zoneId])
                        pass
                else:
                    self.notify.warning("GOLF COURSE: trying to grab golfer %s that is already on the course" % (avId))
        
    def grabGolfers(self):
        for avId in self.avIdList:
            golfer = simbase.air.doId2do.get(avId)
            if golfer:
                if self.avStateDict[avId] == INITIAL:
                    #golfer.sendUpdate("sendToGolfCourse", [self.zoneId])
                    self.avStateDict[avId] = EXPECTED
        self.request('WaitJoin')
        
        
    def getGolferIds(self):
        return self.avIdList
        
    def checkGolferPlaying(self, avId):
        if self.avStateDict[avId] == ONHOLE:
            return 1
        else:
            return 0
            
        
    def b_setCourseReady(self):
        self.setCourseReady()
        self.d_setCourseReady()

    def d_setCourseReady(self):
        self.notify.debug("GOLF COURSE: Sending setCourseReady")
        self.sendUpdate("setCourseReady", [self.numHoles, self.holeIds, self.calcCoursePar()])

    def setCourseReady(self):
        """
        This method gets called when all avatars have joined
        """
        self.notify.debug("GOLF COURSE: setCourseReady: golf course ready with avatars: %s" %
                          self.avIdList)
        self.trophyListLen = 0
        self.courseBestListLen = 0
        self.holeBestListLen = 0
        self.cupListLen = 0
        self.normalExit = 1

    def d_setPlayHole(self):
        """
        Tells the distributed golf course that play is about to begin
        """
        self.notify.debug("GOLF COURSE: setPlayHole: play on golf hole about to start")
        self.sendUpdate("setPlayHole", [])
        
    def b_setCourseExit(self):
        self.d_setCourseExit()
        self.setCourseExit()

    def d_setCourseExit(self):
        self.notify.debug("GOLF COURSE: Sending setGameExit")
        self.sendUpdate("setCourseExit", [])

    def setCourseExit(self):
        """
        This method gets called when it's time for avatars to exit the golf course
        """
        self.notify.debug("GOLF COURSE: setGameExit")
        
    def handleExitedAvatar(self, avId):
        """
        An avatar bailed out because he lost his connection or quit
        unexpectedly.
        We have decided when this happens, we will continue wihtout them
        """
        # TODO: what if they have all exited already?
        self.notify.warning("GOLF COURSE: handleExitedAvatar: avatar id exited: " +
                            str(avId))
        self.avStateDict[avId] = EXITED

        # Let the clients know that one of them has dropped
        self.sendUpdate("avExited", [avId])

        if self.currentHole and not self.haveAllGolfersExited():
            # if the guy who dropped was taking his turn, we need to move to the next guy
            self.currentHole.avatarDropped(avId)

        if self.haveAllGolfersExited():
            self.setCourseAbort()
        else:
            # we need to move to next hole if the guy who dropped was the only one who hasn't sunk a ball
            if self.isCurHoleDone():
                if self.isPlayingLastHole():
                    if self.state not in ["WaitReward", "WaitReadyHole"]:
                        self.safeDemand('WaitReward')
                else:
                    self.notify.debug('allBalls are in holes, calling holeOver')
                    self.holeOver()

        # remove the avId from any ToonBarriers waiting on it
        if hasattr(self, 'rewardBarrier'):
            if self.rewardBarrier:
                self.rewardBarrier.clear(avId)
        if hasattr(self, '__barrier'):
            if self.__barrier:
                self.__.clear(avId)                
            
        
    def startNextHole(self):
        self.notify.debugStateCall(self)
        holeId = self.holeIds[self.numHolesPlayed]
        self.currentHole = DistributedGolfHoleAI.DistributedGolfHoleAI(self.zoneId, golfCourse = self, holeId = holeId)
        self.currentHole.generateWithRequired(self.zoneId)
        self.d_setCurHoleDoId(self.currentHole.doId)
        self.safeDemand('WaitReadyHole')
        
    def holeOver(self):
        """
        Called from the hole to let the course know to start the next hole
        """
        self.notify.debug("GOLF COURSE: holeOver")
        self.numHolesPlayed += 1
        if self.numHolesPlayed < self.numHoles:
            self.b_setCurHoleIndex(self.numHolesPlayed)
        self.safeDemand('WaitLeaveHole')

    def setCourseAbort(self):
        """
        This gets called in the case of an unexpected abort
        """
        self.notify.debug("GOLF COURSE: setGameAbort")
        self.normalExit = 0
        self.sendUpdate("setCourseAbort", [0])
        # only transition to cleanup after we've sent the gameAbort msg
        self.safeDemand("Cleanup")
        
        

        
#######################################################################################
### FSM FUNCTIONS
#######################################################################################

    def enterOff(self):
        self.notify.debug("GOLF COURSE: enterOff")
        
    def exitOff(self):
        self.notify.debug("GOLF COURSE: exitOff")
        
    def enterWaitJoin(self):
        """
        This state waits for all of the clients to join.
        see setAvatarJoined
        """
        self.notify.debug("GOLF COURSE: enterWaitJoin")
        for avId in self.avIdList:
            self.avStateDict[avId] = EXPECTED
            # listen for this avatar's exit event
            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            self.handleExitedAvatar, extraArgs=[avId])
    
        def allAvatarsJoined(self=self):
            self.notify.debug("GOLF COURSE: all avatars joined")
            # Everybody is here, wait for them to ready the course
            
            # wait for clients to be ready
            self.load()
            
    
        def handleTimeout(avIds, self=self):
            self.notify.debug("GOLF COURSE: timed out waiting for clients %s "
                              "to join" % avIds)
            for avId in self.avStateDict:
                if not self.avStateDict[avId] == JOINED:
                    #kick player
                    self.handleExitedAvatar(avId)
            if self.haveAllGolfersExited():
                self.setCourseAbort()
            else:
                self.load()
    
        self.__barrier = ToonBarrier(
            'waitClientsJoin',
            self.uniqueName('waitClientsJoin'),
            self.avIdList, JOIN_TIMEOUT,
            allAvatarsJoined, handleTimeout)
    
        # at this point, it's not possible for any avatars to have
        # already joined

    def exitWaitJoin(self):
        self.notify.debugStateCall(self)
        self.__barrier.cleanup()
        self.__barrier = None
        
    def setAvatarJoined(self):
        """
        This is a distributed update that gets called from the clients
        when this distributed object is created on their machine. Each time
        we hear that a single avatar has joined, we check to see if they
        have all joined.
        """
        # check to make sure this message is still relevant
        #if (self.state !=
        #    'WaitJoin'):
        #    self.notify.debug("GOLF COURSE: Ignoring setAvatarJoined message")
        #    return
    
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("GOLF COURSE: setAvatarJoined: avatar id joined: " +
                          str(avId))
        self.avStateDict[avId] = JOINED
        self.notify.debug("GOLF COURSE: setAvatarJoined: new states: " +
                          str(self.avStateDict))

        if hasattr(self,"_DistributedGolfCourseAI__barrier") and self._DistributedGolfCourseAI__barrier:
            self.__barrier.clear(avId)
        else:
            self.notify.warning("setAvatarJoined avId=%d but barrier is invalid" % avId)
        
    def exitFrameworkWaitClientsJoin(self):
        self.__barrier.cleanup()
        del self.__barrier
        
    def enterWaitReadyCourse(self):
        """
        This state waits for all of the clients to be ready.
        see setAvatarReady
        """
        self.notify.debug("GOLF COURSE: enterWaitReadyCourse")

        def allAvatarsInCourse(self=self):
            self.notify.debug("GOLF COURSE: all avatars ready course")
            # Everybody is here, start the game
            # prepopulate the scores with zeros
            for avId in self.avIdList:
                blankScoreList = [0] * self.numHoles
                self.scores[avId] = blankScoreList
                self.aimTimes[avId] = 0
            self.notify.debug('self.scores = %s' % self.scores)
            self.startNextHole() 

        def handleTimeout(avIds, self=self):
            self.notify.debug("GOLF COURSE: Course timed out waiting for clients %s "
                              "to report 'ready'" % avIds)
            if self.haveAllGolfersExited():
                self.setCourseAbort()
            else:
                allAvatarsInCourse()           

        self.__barrier = ToonBarrier(
            'WaitReadyCourse',
            self.uniqueName('WaitReadyCourse'),
            self.avIdList, READY_TIMEOUT,
            allAvatarsInCourse, handleTimeout)
            
        

        # some clients may already be ready
        for avId in self.avStateDict.keys():
            if self.avStateDict[avId] == READY:
                self.__barrier.clear(avId)
                
    def setAvatarReadyCourse(self):
        """
        This is a distributed update that gets called from the clients
        when they are ready. Usually this means they have finished reading
        the rules panel. Each time we hear that a single avatar is ready,
        we check to see if they are all ready. If they are all ready, we
        send a ??? to actually start playing the golf round.
        """
        # check to make sure this message is still relevant
        # note that it's possible for one client to report 'joined' and
        # 'ready' before another client has even reported 'joined'
        #if (self.state not in
        #    ['WaitJoin', 'WaitReadyCourse']):
        #    self.notify.debug("GOLF COURSE: Ignoring setAvatarReadyCourse message")
        #    return
        
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("GOLF COURSE: setAvatarReadyCourse: avatar id ready: " +
                          str(avId))
        self.avStateDict[avId] = READY
        self.notify.debug("GOLF COURSE: setAvatarReadyCourse: new avId states: " +
                          str(self.avStateDict))

        # if we're in the waitClientsReady state, update the barrier;
        # otherwise, just having set this avatar's stateDict entry is
        # sufficient (the barrier will be updated accordingly when we
        # enter the waitClientsReady state)
        if (self.state ==
            'WaitReadyCourse'):
            self.__barrier.clear(avId)
            
    def exitWaitReadyCourse(self):
        self.notify.debugStateCall(self)
        self.__barrier.cleanup()
        self.__barrier = None
        
    def enterWaitReadyHole(self):
        self.notify.debug("GOLF COURSE: enterWaitReadyHole")

        def allAvatarsInHole(self=self):
            self.notify.debug("GOLF COURSE: all avatars ready hole")
            # Everybody is here, start the game
            if self.safeDemand('PlayHole'):
                self.d_setPlayHole()

        def handleTimeout(avIds, self=self):
            self.notify.debug("GOLF COURSE: Hole timed out waiting for clients %s "
                              "to report 'ready'" % avIds)
            if self.haveAllGolfersExited():
                self.setCourseAbort()
            else:
                if self.safeDemand('PlayHole'):
                    self.d_setPlayHole()
                
                
        stillPlaying = self.getStillPlayingAvIds()

        self.__barrier = ToonBarrier(
            'WaitReadyHole',
            self.uniqueName('WaitReadyHole'),
            stillPlaying, READY_TIMEOUT,
            allAvatarsInHole, handleTimeout)
            

        # some clients may already be ready
        for avId in self.avStateDict.keys():
            if self.avStateDict[avId] == ONHOLE:
                self.__barrier.clear(avId)
                
    def exitWaitReadyHole(self):
        self.notify.debugStateCall(self)
        if hasattr(self, "__barrier"):
            self.__barrier.cleanup()
            self.__barrier = None
                

    def getStillPlayingAvIds(self):
        """Return a list of av ids are still playing and have not been disconnected."""
        retval = []
        for avId in self.avIdList:
            av = simbase.air.doId2do.get(avId)
            if av:
                if self.avStateDict.has_key(avId) and not \
                   self.avStateDict[avId] == EXITED:                    
                    retval.append(avId)
        return retval

                
    def avatarReadyHole(self, avId):
        """
        This is a distributed update that gets called from the clients
        when they are ready. Usually this means they have finished reading
        the rules panel. Each time we hear that a single avatar is ready,
        we check to see if they are all ready. If they are all ready, we
        send a ??? to actually start playing the golf round.
        """
        # check to make sure this message is still relevant
        # note that it's possible for one client to report 'joined' and
        # 'ready' before another client has even reported 'joined'
        if (self.state not in
            ['WaitJoin', 'WaitReadyCourse', 'WaitReadyHole']):
            self.notify.debug("GOLF COURSE: Ignoring setAvatarReadyHole message")
            return
        
        #avId = self.air.getAvatarIdFromSender()
        self.notify.debug("GOLF COURSE: setAvatarReadyHole: avatar id ready: " +
                          str(avId))
        self.avStateDict[avId] = ONHOLE
        self.notify.debug("GOLF COURSE: setAvatarReadyHole: new avId states: " +
                          str(self.avStateDict))

        # if we're in the waitClientsReady state, update the barrier;
        # otherwise, just having set this avatar's stateDict entry is
        # sufficient (the barrier will be updated accordingly when we
        # enter the waitClientsReady state)
        if (self.state ==
            'WaitReadyHole'):
            self.__barrier.clear(avId)



    def enterPlayHole(self):
        self.notify.debug("GOLF COURSE: enterPlayHole")
        if self.currentHole and not self.currentHole.playStarted:
            self.currentHole.startPlay()
        pass
        
    def exitPlayHole(self):
        self.notify.debug("GOLF COURSE: exitPlayHole")
        pass

    def enterWaitLeaveHole(self):
        """We are finished with our current hole, figure out what to do next."""
        self.notify.debugStateCall(self)
        self.notify.debug('calling requestDelete on hole %d' % self.currentHole.doId)
        self.currentHole.requestDelete()
        self.currentHole = None
        if self.numHolesPlayed >= self.numHoles:
            # we've played all the holes
            #self.safeDemand('WaitReward')
            pass
        else:
            self.startNextHole()
        pass
    
    def exitWaitLeaveHole(self):
        pass

    def enterWaitReward(self):
        """Done playing all the holes, display a reward movie on the client."""
        # TODO calculate any trophy rewards, send those to the client
        self.updateHistoryForCourseComplete()
        self.awardTrophies()
        self.awardCups()
        self.awardHoleBest()
        self.awardCourseBest()
        self.recordHoleInOne()
        self.recordCourseUnderPar()
        
        trophiesList = []
        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            if avId in self.newTrophies:
                oneTrophyList = self.newTrophies[avId]
                trophiesList.append(oneTrophyList)
            else:
                # probably a disconnected player, just us an empty list
                trophiesList.append([])
        while len(trophiesList) < GolfGlobals.MAX_PLAYERS_PER_HOLE:
            # toon.dc expects 4 lists
            trophiesList.append([])

        holeBestList = []
        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            if avId in self.newHoleBest:
                oneTrophyList = self.newHoleBest[avId]
                holeBestList.append(oneTrophyList)
            else:
                # probably a disconnected player, just us an empty list
                holeBestList.append([])
        while len(holeBestList) < GolfGlobals.MAX_PLAYERS_PER_HOLE:
            # toon.dc expects 4 lists
            holeBestList.append([])

        courseBestList = []
        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            if avId in self.newCourseBest:
                oneTrophyList = self.newCourseBest[avId]
                courseBestList.append(oneTrophyList)
            else:
                # probably a disconnected player, just us an empty list
                courseBestList.append([])
        while len(courseBestList) < GolfGlobals.MAX_PLAYERS_PER_HOLE:
            # toon.dc expects 4 lists
            courseBestList.append([])

        cupList = []
        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            if avId in self.newCups:
                oneCupList = self.newCups[avId]
                cupList.append(oneCupList)
                self.cupListLen = self.cupListLen + 1
            else:
                # probably a disconnected player, just us an empty list
                cupList.append([])
        while len(cupList) < GolfGlobals.MAX_PLAYERS_PER_HOLE:
            # toon.dc expects 4 lists
            cupList.append([]) 

        REWARD_TIMEOUT = (self.trophyListLen + self.holeBestListLen + self.courseBestListLen + self.cupListLen) * 5 + 19
        # the extra 15 seconds are for: 8 seconds of rankings and 7 as a buffer

        # send total aim times too
        aimTimesList = [0] *4
        aimIndex = 0
        stillPlaying = self.getStillPlayingAvIds()
        for avId in self.avIdList:
            if avId in stillPlaying:
                aimTime = 0
                if avId in self.aimTimes:
                    aimTime = self.aimTimes[avId]
                aimTimesList[aimIndex] = aimTime
            aimIndex += 1

        self.sendUpdate('setReward', [trophiesList, self.rankings, \
                                      holeBestList, courseBestList, cupList,
                                      self.winnerByTieBreak, aimTimesList[0],
                                      aimTimesList[1], aimTimesList[2], aimTimesList[3]] )

        def allAvatarsRewarded(self=self):
            self.notify.debug("GOLF COURSE: all avatars rewarded")
            # Everybody is here, leave the golf course
            #self.safeDemand('WaitLeaveCourse')
            self.rewardDone()
    
        def handleRewardTimeout(avIds, self=self):
            self.notify.debug("GOLF COURSE: timed out waiting for clients %s "
                              "to finish reward" % avIds)
            # self.setCourseAbort()
            #self.safeDemand('WaitLeaveCourse')
            self.rewardDone()

        stillPlaying = self.getStillPlayingAvIds()
        self.rewardBarrier = ToonBarrier(
            'waitReward',
            self.uniqueName('waitReward'),
            stillPlaying, REWARD_TIMEOUT,
            allAvatarsRewarded, handleRewardTimeout)

    def exitWaitReward(self):
        """Handle exiting the WaitReward state."""
        pass
    
    def enterWaitLeaveCourse(self):
        self.notify.debugStateCall(self)

        # TODO we should be calling self.courseFinished()
        self.setCourseAbort()
        pass

    def exitWaitLeaveCourse(self):
        pass
        
    def enterCleanup(self):
        self.notify.debug("GOLF COURSE: enterCleanup")

        #delete myself
        self.requestDelete()
        pass

    def exitCleanup(self):
        self.notify.debug("GOLF COURSE: exitCleanup")
        pass
    

#######################################################################################
### END FSM FUNCTIONS
#######################################################################################

    def isCurHoleDone(self):
        """Returns true if the current hole is finished."""
        retval = False
        if self.areAllBallsInHole():
            #if all the balls are in the hole we're done
            retval = True
        else:
            # if everyone is exited or Ball in we're done
            retval = True
            for state in self.avStateDict.values():
                if not (state == BALLIN or state == EXITED):
                    retval = False
                    break
        return retval
        
    def areAllBallsInHole(self):
        """Return true if everyone's ball is in the hole."""
        self.notify.debug('areAllBallsInHole, self.avStateDict=%s' % self.avStateDict)
        allBallsInHole = True
        for state in self.avStateDict.values():
            if state != BALLIN:
                allBallsInHole = False
        return allBallsInHole

    def isPlayingLastHole(self):
        """Return true if we are currently playing the last hole in the course."""
        retval = (self.numHoles - self.numHolesPlayed == 1)
        return retval

    def setBallIn(self, avId):
        self.notify.debug('setBallIn %d' % avId)
        if self.avStateDict[avId] == BALLIN:
            # we've already process this ball going in, just return
            self.notify.debug('setBallIn already in BALLIN state, just returning')
            return
        self.avStateDict[avId] = BALLIN
        self.updateHistoryForBallIn(avId)
        if self.isCurHoleDone():
            if self.isPlayingLastHole():
                if self.state != "WaitReward":
                    self.safeDemand('WaitReward')
            else:
                self.notify.debug('allBalls are in holes, calling holeOver')
                self.holeOver()

    def updateHistoryForBallIn(self, avId):
        """Update our history on anything that is hole dependent."""
        if self.currentHole == None:
            return
        holeId = self.currentHole.holeId
        holeInfo = GolfGlobals.HoleInfo[holeId]
        par = holeInfo['par']
        holeIndex = self.numHolesPlayed
        if holeIndex >= self.numHoles:
            self.notify.warning('updateHistoryForBallIn invalid holeIndex %d' % holeIndex)
            holeIndex = self.numHoles -1
        elif holeIndex < 0:
            self.notify.warning('updateHistoryForBallIn invalid holeIndex %d' % holeIndex)
            holeIndex = 0
        strokes = self.scores[avId][holeIndex]
        self.notify.debug('self.scores = %s' % self.scores)
        diff = strokes - par

        # check for hole in one
        if strokes == 1:
            self.incrementEndingHistory(avId, GolfGlobals.HoleInOneShots)

        # now do eagle, birdie, par
        if diff <= -2:
            self.incrementEndingHistory(avId, GolfGlobals.EagleOrBetterShots)
        if diff <= -1:
            self.incrementEndingHistory(avId, GolfGlobals.BirdieOrBetterShots)
        if diff <= 0:
            self.endingHistory[avId][GolfGlobals.ParOrBetterShots] += 1

        # check our personal best
        if strokes < self.endingHoleBest[avId][holeId] or \
           self.endingHoleBest[avId][holeId] == 0:
            self.endingHoleBest[avId][holeId] = strokes
            

    def incrementEndingHistory(self, avId, historyIndex):
        """Safely increment the golf ending history for an avatar."""
        if self.endingHistory.has_key(avId) and \
           GolfGlobals.TrophyRequirements.has_key(historyIndex):
            maximumAmount = GolfGlobals.TrophyRequirements[historyIndex][-1]
            if self.endingHistory[avId][historyIndex] < maximumAmount:
                self.endingHistory[avId][historyIndex] += 1
                
    
    def getCourseId(self):
        """Return the courseId of this course."""
        return self.courseId
    

    def abortCurrentHole(self):
        """Abort the current hole being played, and go to the next hole."""
        holeId = self.currentHole.holeId
        holeDoId = self.currentHole.doId
        self.currentHole.finishHole()
        return holeId, holeDoId
        
    def calcHolesToUse(self):
        """Return the list of holes to use in our course.

        If this is changed, update client version too.
        """
        retval = []

        if simbase.air.config.GetBool('golf-course-randomized', 1):
            retval = self.calcHolesToUseRandomized(self.courseId)
            self.notify.debug("randomized courses!")
            for x in range(len(retval)):
                self.notify.debug("Hole is: %s" % retval[x])
        else:
            validHoles = self.calcUniqueHoles(self.courseId)
            if self.preferredHoleId in validHoles:
                retval.append(self.preferredHoleId)
            while len(retval) < self.numHoles:
                for holeId in GolfGlobals.CourseInfo[self.courseId]['holeIds']:
                    if type(holeId) == type(0):
                        retval.append(holeId)
                    elif type(holeId) == type(()):
                        retval.append(holeId[0])
                    else:
                        self.notify.warning('cant handle %s' % self.holeId)
                    if len(retval) >= self.numHoles:
                        break;
        
        return retval
        
    def incrementScore(self, avId):
        self.notify.debug('incrementScore self.scores=%s avId=%s' % (self.scores, avId))
        self.scores[avId][self.numHolesPlayed] += 1
        self.notify.debug('after increment self.score=%s' % self.scores)
        self.sendScores()
        
    def sendScores(self):
        self.notify.debug('sendScores self.scores = %s' % self.scores)
        scorelist = []
        for avId in self.avIdList:
            for score in self.scores[avId]:
                scorelist.append(score)
        self.sendUpdate('setScores', [scorelist])
        self.notify.debug('sendScores end self.scores = %s' % self.scores)

    def getCurHoleIndex(self):
        return self.curHoleIndex

    def b_setCurHoleIndex(self, holeIndex):
        self.setCurHoleIndex(holeIndex)
        self.d_setCurHoleIndex(holeIndex)

    def d_setCurHoleIndex(self, holeIndex):
        self.sendUpdate('setCurHoleIndex', [holeIndex])

    def setCurHoleIndex(self, holeIndex):
        self.curHoleIndex = holeIndex


    def setDoneReward(self):
        """
        Clear the avatar from the reward barrier since he is done with the reward movie.
        """
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('got rewardDone from %d' % avId)
        if hasattr(self, 'rewardBarrier'):
            self.rewardBarrier.clear(avId)
        self.sendUpdate("setCourseAbort", [avId])

    def rewardDone(self):
        """All clients have confirmed done with the reward movie. do proper cleanup."""
        # we didn't delete the hole, so we don't see grayspace for the reward movie
        # now go ahead and delete
        self.notify.debug('rewardDone')
        self.holeOver()
        self.safeDemand('WaitLeaveCourse')

    def updateHistoryForCourseComplete(self):
        """Update the histories for finishing a course."""
        self.calcRankings()
        stillPlaying = self.getStillPlayingAvIds()

        for avId in stillPlaying:
            # he definitely completed a course
            self.incrementEndingHistory(avId, GolfGlobals.CoursesCompleted)
            # check if he's under course par
            coursePar = self.calcCoursePar()
            totalScore = self.getTotalScore(avId)
            if totalScore < coursePar:
                self.incrementEndingHistory(avId, GolfGlobals.CoursesUnderPar)
            # check if it's a multiplayer win
            if len(stillPlaying) > 1:
                self.incrementEndingHistory(avId, GolfGlobals.MultiPlayerCoursesCompleted)
                if self.rankingsById[avId] == 1:                    
                    # check for course zero, one or two wins
                    if self.courseId == 0:
                        self.incrementEndingHistory(avId, GolfGlobals.CourseZeroWins)
                    elif self.courseId == 1:
                        self.incrementEndingHistory(avId, GolfGlobals.CourseOneWins)
                    elif self.courseId == 2:
                        self.incrementEndingHistory(avId, GolfGlobals.CourseTwoWins)
                    else:
                        self.notify.warning('unhandled case, self.courseId=%s' % self.courseId)
            # check for our personal best 
            if totalScore < self.endingCourseBest[avId][self.courseId] or \
               self.endingCourseBest[avId][self.courseId] == 0:
                self.endingCourseBest[avId][self.courseId] = totalScore
        

    def calcRankings(self):
        """Calculate the rankings of the avatars still playing.

        -1 represents not ranked, 1 is 1st, 2 is 2nd, two 1st places are possible.
        Sets self.rankings and self.rankingsById
        8/29/2007 too much collusion. randomly choose winner if tied for 1st
        9/14/2007 use aim time as tie breaker
        """        
        stillPlaying = self.getStillPlayingAvIds()
        self.rankings = []
        totalScores = []

        # get the total scores for each player, disconnected players get a high score
        for avId in self.avIdList:
            aimTime = 0
            if avId in self.aimTimes:
                aimTime = self.aimTimes[avId]
            if avId in stillPlaying:
                totalScores.append( (avId,self.getTotalScore(avId),aimTime) )
            else:
                totalScores.append( (avId,255,aimTime) )
        
        def scoreCompareNoTime(tupleA, tupleB):
            if tupleA[1] > tupleB[1]:
                return 1
            elif tupleA[1] == tupleB[1]:
                return 0
            else:
                return -1

        def scoreCompareWithTime(tupleA, tupleB):
            if tupleA[1] > tupleB[1]:
                return 1
            elif tupleA[1] == tupleB[1]:
                if tupleA[2] > tupleB[2]:
                    return 1
                elif tupleA[2] == tupleB[2]:
                    return 0
                else:
                    return -1
            else:
                return -1            

        # sort it by score, make sure the avId gets sorted too
        if GolfGlobals.TIME_TIE_BREAKER:
            totalScores.sort( scoreCompareWithTime)
        else:
            totalScores.sort( scoreCompareNoTime)

        # calculate the rank, handle 2 1st place winners
        curRank = 0
        oldScore = 0
        oldTime = 0
        self.rankingsById = {}
        # calculate rankings, including time if the option is turned on
        for scoreTuple in totalScores:
            time = scoreTuple[2]
            score = scoreTuple[1]
            avId = scoreTuple[0]
            if score > oldScore or \
               (GolfGlobals.TIME_TIE_BREAKER and score == oldScore and time > oldTime):
                curRank += 1
                oldScore = score
                oldTime = time
            self.rankingsById[avId] = curRank

        # calculate which toons had the exact same number of strokes for 1st
        tiedForFirst = []
        tempRank = 0
        oldScore =0;
        oldTime = 0
        for scoreTuple in totalScores:
            time = scoreTuple[2]
            score = scoreTuple[1]
            avId = scoreTuple[0]
            if score > oldScore:
                tempRank += 1
                oldScore = score
                oldTime = time                
            if tempRank == 1:
                tiedForFirst.append(avId)

        for avId in self.avIdList:
            if avId in stillPlaying:
                self.rankings.append(self.rankingsById[avId])
            else:
                self.rankings.append(-1)

        # randomly choose winner if tied for 1st
        if (len(tiedForFirst) >= 2) and not GolfGlobals.TIME_TIE_BREAKER:
            winnerAvId = random.choice(tiedForFirst)
            winnerIndex = self.avIdList.index(winnerAvId)
            self.winnerByTieBreak = winnerAvId
            for index in xrange(len(self.rankings)):
                if (self.rankings[index] > 0) and (index != winnerIndex) :
                    self.rankings[index] += 1
            for avId in self.rankingsById:
                if (self.rankingsById[avId] > 0) and (avId != winnerAvId):
                    self.rankingsById[avId] += 1
        elif len(tiedForFirst) >= 2:
            winnerAvId = totalScores[0][0]
            self.winnerByTieBreak = winnerAvId

           
            
    def awardTrophies(self):
        """Award the trophies. Also update self.newTrophies."""
        stillPlaying = self.getStillPlayingAvIds()
        for avId in stillPlaying:
            av = simbase.air.doId2do.get(avId)
            if av:
                oldHistory = self.startingHistory[avId]
                endingHistory = self.endingHistory[avId]
                oldTrophies = GolfGlobals.calcTrophyListFromHistory(oldHistory)
                endingTrophies = GolfGlobals.calcTrophyListFromHistory(endingHistory)
                av.b_setGolfHistory(endingHistory)
                
                # now figure out which trophies he just got
                newTrophies = []
                for index in xrange(len(oldTrophies)):
                    if not oldTrophies[index] and endingTrophies[index]:
                        self.notify.debug('New Trophy %d' % index)
                        self.air.writeServerEvent("golf_trophy", avId, "%s" % (index))
                        newTrophies.append(True)
                        self.trophyListLen = self.trophyListLen + 1
                    else:
                        newTrophies.append(False)
                self.newTrophies[avId] = newTrophies

    def awardCups(self):
        """Award the cups and laff boost. Also update self.newCups."""
        stillPlaying = self.getStillPlayingAvIds()
        for avId in stillPlaying:
            av = simbase.air.doId2do.get(avId)
            if av:
                oldHistory = self.startingHistory[avId]
                endingHistory = self.endingHistory[avId]
                oldCups = GolfGlobals.calcCupListFromHistory(oldHistory)
                endingCups = GolfGlobals.calcCupListFromHistory(endingHistory)
                
                # now figure out which trophies he just got
                newCups = []
                for index in xrange(len(oldCups)):
                    if not oldCups[index] and endingCups[index]:
                        self.notify.debug('New Trophy %d' % index)
                        newCups.append(True)
                        self.air.writeServerEvent("golf_cup", avId, "%s" % (index))
                        newMaxHp = av.getMaxHp() + 1
                        av.b_setMaxHp(newMaxHp)
                        # Also, give them a full heal
                        av.toonUp(newMaxHp)
                    else:
                        newCups.append(False)

                self.newCups[avId] = newCups

    def awardHoleBest(self):
        """Award the personal best in goles. Also update self.newHoleBest."""
        stillPlaying = self.getStillPlayingAvIds()
        for avId in stillPlaying:
            av = simbase.air.doId2do.get(avId)
            if av:
                oldHoleBest = self.startingHoleBest[avId]
                endingHoleBest = self.endingHoleBest[avId]
                av.b_setGolfHoleBest(endingHoleBest)
                
                # now figure out which trophies he just got
                newHoleBest = []

                longestHoleBestList = 0
                
                for index in xrange(len(oldHoleBest)):
                    if endingHoleBest[index] < oldHoleBest[index]:
                        self.notify.debug('New HoleBest %d' % index)
                        newHoleBest.append(True)
                        longestHoleBestList = longestHoleBestList + 1
                    else:
                        newHoleBest.append(False)

                if( longestHoleBestList > self.holeBestListLen):
                    self.holeBestListLen = longestHoleBestList
                self.newHoleBest[avId] = newHoleBest

    def awardCourseBest(self):
        """Award the personal best in goles. Also update self.newCourseBest."""
        stillPlaying = self.getStillPlayingAvIds()
        for avId in stillPlaying:
            av = simbase.air.doId2do.get(avId)
            if av:
                oldCourseBest = self.startingCourseBest[avId]
                endingCourseBest = self.endingCourseBest[avId]
                av.b_setGolfCourseBest(endingCourseBest)
                
                # now figure out which trophies he just got
                newCourseBest = []

                longestCourseBestList = 0
                
                for index in xrange(len(oldCourseBest)):
                    if endingCourseBest[index] < oldCourseBest[index]:
                        self.notify.debug('New CourseBest %d' % index)
                        newCourseBest.append(True)
                        longestCourseBestList = longestCourseBestList + 1
                    else:
                        newCourseBest.append(False)

                if(longestCourseBestList > self.courseBestListLen):
                    self.courseBestListLen = longestCourseBestList
                self.newCourseBest[avId] = newCourseBest                     

    def haveAllGolfersExited(self):
        """Returns true if all the golfers are gone"""
        retval = True
        for avId in self.avStateDict:
            if not self.avStateDict[avId] == EXITED:
                retval = False
                break
        return retval
                
        
    def getCurHoleDoId(self):
        """Return the DoId of the current hole."""
        retval = 0
        if self.currentHole:
            retval = self.currentHole.doId
        return retval

    def d_setCurHoleDoId(self, curHoleDoId):
        """Send the current hole doId to the client."""
        self.sendUpdate('setCurHoleDoId', [curHoleDoId])

    def calcCoursePar(self):
        """Return the par for the course."""
        retval = 0
        for holeId in self.holeIds:
            holeInfo = GolfGlobals.HoleInfo[holeId]
            retval += holeInfo['par']
        return retval

    def getTotalScore(self, avId):
        """Return the total golf score for an avatar."""
        retval = 0
        if self.scores.has_key(avId):
            for holeScore in self.scores[avId]:
                retval += holeScore
        return retval

    def getCurHoleScore(self, avId):
        """Return the current hole score for an avatar."""
        retval = 0
        if avId in self.scores and self.numHolesPlayed < len(self.scores[avId]):
            retval = self.scores[avId][self.numHolesPlayed]
        return retval

    def toggleDrivePermission(self, avId):
        """Toggle the drive cheat for this toon. Returns true id driving was turned on."""
        if avId in self.drivingToons:
            self.drivingToons.remove(avId)
            self.sendUpdate('changeDrivePermission', [avId,0])
            retval = False
            pass
        else:
            self.drivingToons.append(avId)
            self.sendUpdate('changeDrivePermission', [avId,1])
            retval =True
        return retval

    def safeDemand(self, newState):
        """Demand the new state only if we're not in Cleanup and its safe.
        Returns true if the demand was done."""
        doingDemand = False
        if self.state == 'Cleanup':
            # deliberately do nothing
            pass
        else:            
            if self.state in self.defaultTransitions:
                if newState in self.defaultTransitions[self.state]:
                    self.demand(newState)
                    doingDemand = True
            elif self.state == None:
                # we are in the middle of the transition, demand and pray it works
                self.demand(newState)
                doingDemand = True
            if not doingDemand:
                self.notify.warning('doId=%d ignoring demand from %s to %s' % (self.doId,self.state, newState))
        return doingDemand

    def setAvatarExited(self):
        """Handle a client telling us a toon fell asleep."""
        avId = self.air.getAvatarIdFromSender()
        self.handleExitedAvatar(avId)

    def createChoicesList(self, courseId, possibleHoles):
        """Return a weighted list of hole choices."""
        retval = []
        # assuming all input is correct
        holeIds = GolfGlobals.CourseInfo[courseId]['holeIds']
        for holeOrTuple in holeIds:
            if type(holeOrTuple) == type(()):
                # if its a tuple, the first Id is hole, 2nd is its weight
                holeId = holeOrTuple[0]
                weight = holeOrTuple[1]
            elif type(holeOrTuple) == type(0):                
                holeId = holeOrTuple
                weight =1
            else:
                self.notify.warning('cant handle %s' %holeOrTuple)
                continue
            if holeId in possibleHoles:
                retval += [holeId]*weight
        return retval                                

    def calcUniqueHoles(self, courseId):
        """Return a set of the unique holes used in this course."""
        uniqueHoles = set()
        for holeOrTuple in GolfGlobals.CourseInfo[courseId]['holeIds']:
            if type(holeOrTuple) == type(()):
                uniqueHoles.add(holeOrTuple[0])
            elif type(holeOrTuple) == type(0):
                uniqueHoles.add(holeOrTuple)
            else:
                self.notify.warning('cant handle %s' %holeOrTuple)
        return uniqueHoles

    def calcHolesToUseRandomized(self,courseId):
        """Randomizes which golf holes to use for each course."""
        retval = []
        numHoles = GolfGlobals.CourseInfo[courseId]['numHoles']
        uniqueHoles = self.calcUniqueHoles(courseId)        

        curHolesChosen = set()
        while len(retval) < numHoles:
            if uniqueHoles == curHolesChosen:
                curHolesChosen = set()
            possibleHoles = uniqueHoles - curHolesChosen
            choicesList = self.createChoicesList( courseId, possibleHoles)
            if not (self.preferredHoleId == None) and \
               self.preferredHoleId in choicesList and \
               self.preferredHoleId not in curHolesChosen:
                holeChosen = self.preferredHoleId
            else:            
                holeChosen = random.choice(choicesList)
            retval.append(holeChosen)
            curHolesChosen.add(holeChosen)
        return retval

    def recordHoleInOne(self):
        """Write to the server log hole in ones the players got."""
        stillPlaying = self.getStillPlayingAvIds()
        for avId in stillPlaying:
            scoreList = self.scores[avId]
            for holeIndex in xrange(len(scoreList)):
                strokes = scoreList[holeIndex]
                if strokes == 1:
                    holeId = self.holeIds[holeIndex]
                    self.air.writeServerEvent("golf_ace", avId, "%d|%d|%s" % (self.courseId, holeId, stillPlaying))

    def recordCourseUnderPar(self):
        """Write to the server log hole if they are course under par."""
        coursePar = self.calcCoursePar()
        stillPlaying = self.getStillPlayingAvIds()
        for avId in stillPlaying:
            totalScore = self.getTotalScore(avId)            
            netScore = totalScore - coursePar
            if netScore < 0:
                self.air.writeServerEvent("golf_underPar", avId, "%d|%d|%s" % (self.courseId, netScore, stillPlaying))

    def addAimTime(self, avId, aimTime):
        """Add to the aim time of a toom."""
        if avId in self.aimTimes:
            self.aimTimes[avId] += aimTime
            

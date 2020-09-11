import random

HILL_MOLE = 0
HILL_BOMB = 1
HILL_WHACKED = 2
HILL_COGWHACKED = 3

class MoleFieldBase:
    WHACKED = 1
    

   
    MoveUpTimeMax = 1
    MoveUpTimeMultiplier = 0.95
    MoveUpTimeMin = 0.5

    StayUpTimeMax = 7
    StayUpTimeMultiplier = 0.95
    StayUpTimeMin = 3

    MoveDownTimeMax = 1
    MoveDownTimeMultiplier = 0.95
    MoveDownTimeMin = 0.5

    TimeBetweenPopupMax = 1.5
    TimeBetweenPopupMultiplier = 0.95
    TimeBetweenPopupMin = 0.25    

    #GameDuration = 180
    #GameDuration = 60
    #MolesWhackedTarget = 100
    #MolesWhackedTarget = 7

    DamageOnFailure = 20
    
    # use this random generator whenever you calculate a random value for
    # the barrel that must be independently the same on the client and AI.
    # Use for one calculation and then discard.
    def getRng(self):
        return random.Random(self.entId * self.level.doId)

        
    def scheduleMoles(self):
        """Schedule the moles going up and down."""
        self.schedule = []
        totalTime = 0
        curMoveUpTime = self.MoveUpTimeMax # number of seconds it takes for the mole to move up
        curMoveDownTime = self.MoveDownTimeMax # number of seconds it takes for the mole to move down
        curTimeBetweenPopup = self.TimeBetweenPopupMax # how long before another mole pops up
        curStayUpTime = self.StayUpTimeMax  # how long does the mole stay up
        curTime = 3
        eligibleMoles = range(self.numMoles)
        self.getRng().shuffle(eligibleMoles)
        usedMoles = []
        self.notify.debug('eligibleMoles=%s' % eligibleMoles)
        self.endingTime = 0
        randOb = random.Random(self.entId * self.level.doId)
        while self.endingTime < self.GameDuration:
            # choose a mole
            if len(eligibleMoles) == 0:
                eligibleMoles = usedMoles
                self.getRng().shuffle(usedMoles)
                usedMoles = []
                self.notify.debug('eligibleMoles=%s' % eligibleMoles)
            moleIndex = eligibleMoles[0]
            eligibleMoles.remove(moleIndex)
            usedMoles.append(moleIndex)
            moleType = randOb.choice([HILL_MOLE, HILL_MOLE, HILL_MOLE, HILL_BOMB])
            self.schedule.append((curTime, moleIndex, curMoveUpTime, curStayUpTime, curMoveDownTime, moleType))
            curTime += curTimeBetweenPopup
            
            curMoveUpTime = self.calcNextMoveUpTime(curTime, curMoveUpTime)
            curStayUpTime = self.calcNextStayUpTime(curTime, curStayUpTime)
            curMoveDownTime = self.calcNextMoveDownTime(curTime, curMoveDownTime)
            curTimeBetweenPopup = self.calcNextTimeBetweenPopup(curTime, curTimeBetweenPopup)
            self.endingTime = curTime + curMoveUpTime + curStayUpTime + curMoveDownTime

        # remove the last entry in the schedule, since it goes over the game duration
        self.schedule.pop()
        self.endingTime = self.schedule[-1][0] + self.schedule[-1][2] + \
                          self.schedule[-1][3] + self.schedule[-1][4]
        

        self.notify.debug('schedule length = %d, endingTime=%f' % (len(self.schedule), self.endingTime))

    def calcNextMoveUpTime(self, curTime, curMoveUpTime):
        """Calculate how long it takes for the next mole to move up."""
        # we pass curTime in case we want it fairly flat at the start,
        # then quickly ramp up
        newMoveUpTime = curMoveUpTime * self.MoveUpTimeMultiplier
        if newMoveUpTime < self.MoveDownTimeMin:
            newMoveUpTime =  self.MoveDownTimeMin
        return newMoveUpTime

    def calcNextStayUpTime(self, curTime, curStayUpTime):
        """Calculate how long it takes for the next mole to stay up."""
        # we pass curTime in case we want it fairly flat at the start,
        # then quickly ramp up
        newStayUpTime = curStayUpTime * self.StayUpTimeMultiplier
        if newStayUpTime < self.StayUpTimeMin:
            newStayUpTime = self.StayUpTimeMin
        return newStayUpTime

    def calcNextMoveDownTime(self, curTime, curMoveDownTime):
        """Calculate how long it takes for the next mole to move down."""
        # we pass curTime in case we want it fairly flat at the start,
        # then quickly ramp up
        newMoveDownTime = curMoveDownTime * self.MoveDownTimeMultiplier
        if newMoveDownTime < self.MoveDownTimeMin:
            newMoveDownTime = self.MoveDownTimeMin
        return newMoveDownTime

    def calcNextTimeBetweenPopup(self, curTime, curTimeBetweenPopup):
        """Calculate how long it takes for the next mole to pop up."""
        # we pass curTime in case we want it fairly flat at the start,
        # then quickly ramp up
        newTimeBetweenPopup = curTimeBetweenPopup * self.TimeBetweenPopupMultiplier
        if newTimeBetweenPopup < self.TimeBetweenPopupMin:
            newTimeBetweenPopup = self.TimeBetweenPopupMin
        return newTimeBetweenPopup
    

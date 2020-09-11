"""PetGoalMgr.py"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from direct.showbase.PythonUtil import randFloat, lerp
from toontown.pets import PetConstants
import random

class PetGoalMgr(DirectObject.DirectObject):
    """This class handles short- and long-term goals of the pet (PetGoals).
    For instance, if a pet wants to make his owner happy, he needs to get
    close to his owner, then do a trick once he's there, and keep doing
    tricks until his owner is happy. This multi-step goal can be encapsulated
    in a PetGoal."""
    notify = DirectNotifyGlobal.directNotify.newCategory("PetGoalMgr")
    
    def __init__(self, pet):
        self.pet = pet
        # quick-access 'list' of all goals
        self.goals = {}
        self._hasTrickGoal = False
        self.primaryGoal = None
        # timestamp of primary goal start
        self.primaryStartT = 0
        if __dev__:
            self.pscSetup = PStatCollector('App:Show code:petThink:UpdatePriorities:Setup')
            self.pscFindPrimary = PStatCollector('App:Show code:petThink:UpdatePriorities:FindPrimary')
            self.pscSetPrimary = PStatCollector('App:Show code:petThink:UpdatePriorities:SetPrimary')

    def destroy(self):
        if __dev__:
            del self.pscSetup
            del self.pscFindPrimary
            del self.pscSetPrimary
        goals = self.goals.keys()
        for goal in goals:
            self.removeGoal(goal)
            goal.destroy()
        del self.goals

    def hasTrickGoal(self):
        return self._hasTrickGoal
    def _setHasTrickGoal(self, hasTrickGoal):
        self._hasTrickGoal = hasTrickGoal

    def addGoal(self, goal):
        assert not goal in self.goals
        self.goals[goal] = None
        goal.setGoalMgr(self)
    def removeGoal(self, goal):
        assert goal in self.goals
        if self.primaryGoal == goal:
            self._setPrimaryGoal(None)
            # don't choose a new primary goal right now, we'll be
            # updating our priorities soon enough, and we don't want
            # to bog down if we're removing many goals in succession
        goal.clearGoalMgr()
        del self.goals[goal]

    def updatePriorities(self):
        if len(self.goals) == 0:
            return

        if __dev__:
            self.pscSetup.start()
        if self.primaryGoal is None:
            highestPriority = -99999.
            candidates = []
        else:
            # init highestPriority to our current primaryGoal
            highestPriority = self.primaryGoal.getPriority()
            candidates = [self.primaryGoal]
            # bump up its priority based on how new it is
            decayDur = PetConstants.PrimaryGoalDecayDur
            priFactor = PetConstants.PrimaryGoalScale
            elapsed = min(decayDur,
                          globalClock.getFrameTime() - self.primaryStartT)
            highestPriority *= lerp(priFactor, 1., elapsed / decayDur)
        if __dev__:
            self.pscSetup.stop()

        if __dev__:
            self.pscFindPrimary.start()
        for goal in self.goals:
            thisPri = goal.getPriority()
            if thisPri >= highestPriority:
                if thisPri > highestPriority:
                    highestPriority = thisPri
                    candidates = [goal]
                else:
                    candidates.append(goal)
        if __dev__:
            self.pscFindPrimary.stop()

        if __dev__:
            self.pscSetPrimary.start()
        newPrimary = random.choice(candidates)
        if self.primaryGoal != newPrimary:
            self.pet.notify.debug(
                'new goal: %s, priority=%s' % (newPrimary.__class__.__name__,
                                               highestPriority))
            self._setPrimaryGoal(newPrimary)
        if __dev__:
            self.pscSetPrimary.stop()

    def _setPrimaryGoal(self, goal):
        if self.primaryGoal == goal:
            return
        if self.primaryGoal is not None:
            self.primaryGoal.fsm.request('background')
        self.primaryGoal = goal
        self.primaryStartT = globalClock.getFrameTime()
        if goal is not None:
            goal.fsm.request('foreground')

    def _handlePrimaryGoalDone(self):
        self._setPrimaryGoal(None)

    def __repr__(self):
        string = '%s' % self.__class__.__name__
        string += '\n Primary: %s' % self.primaryGoal
        goalPairs = []
        for goal in self.goals:
            goalPairs.append((goal.getPriority(), goal))
        goalPairs.sort()
        goalPairs.reverse()
        for goalPair in goalPairs:
            string += '\n  %s' % goalPair[1]
        return string

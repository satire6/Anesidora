"""RingTrack module: contains the RingTrack class"""

"""
ringTracks are meant to be used in the ring minigame. They define a
periodic sequence of changes in a 2D position. The 2D position varies
within the range [-1..1,-1..1]

ringTracks comprise a series of ring 'actions'. (see RingAction.py) Each
action specifies a particular movement of the ring. Each action in a
ringTrack has a duration, in the range (0..1). The duration specifies the
fraction of time taken by the action wrt the entire track length.
The sum of the durations of all of a track's actions must be <= 1. If
the sum of the durations is less than 1, any time t that is greater than
the sum will be evaluated as the end of the last action.
"""

from direct.directnotify import DirectNotifyGlobal
import RingAction

class RingTrack:
    notify = DirectNotifyGlobal.directNotify.newCategory("RingTrack")

    def __init__(self, actions, actionDurations=None, reverseFlag=0):
        # if no durations specified, give each action an equal timeslice
        if actionDurations == None:
            actionDurations = [1. / float(len(actions))] * len(actions)

        assert(len(actions) == len(actionDurations))

        # check that the action durations sum to 1.
        sum = 0.
        for duration in actionDurations:
            sum += duration
        if sum != 1.:
            self.notify.warning("action lengths do not sum to 1.; sum=" + \
                                str(sum))
        
        self.actions = actions
        self.actionDurations = actionDurations
        self.reverseFlag = reverseFlag

    def eval(self, t):
        """eval(self, float:[0..1])
        Evaluates a ringTrack at a normalized (0..1) time t
        returns a normalized (x,y) pair
        """
        t = float(t)
        assert(t >= 0. and t <= 1.)

        # reverse the time value if appropriate
        if self.reverseFlag:
            t = 1. - t

        # start time of current 'action'
        actionStart = 0.
        # run through actions, see which one we're currently in
        for action,duration in zip(self.actions,self.actionDurations):
            actionEnd = actionStart + duration
            if t < actionEnd:
                # calculate the normalized time within the action
                actionT = (t - actionStart) / duration
                # return the current position of the action
                return action.eval(actionT)
            else:
                actionStart = actionEnd

        if t == actionStart:
            self.notify.debug("time value is at end of ring track: " + \
                              str(t) + " == " + str(actionStart))
        else:
            self.notify.debug("time value is beyond end of ring track: " + \
                         str(t) + " > " + str(actionStart))

        # return final result of final action
        lastAction = self.actions[len(self.actions)-1]
        return lastAction.eval(1.)

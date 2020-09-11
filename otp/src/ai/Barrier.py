""" Barrier.py: contains the Barrier class: utility class for AI objects that must wait for a message from each of a list of Avatars """

from otp.ai.AIBase import *
from direct.task import Task
from direct.showbase import DirectObject
import random

class Barrier(DirectObject.DirectObject):
    notify = directNotify.newCategory('Barrier')
    
    def __init__(self, name, uniqueName, avIdList, timeout,
                 clearedFunc = None, timeoutFunc = None,
                 doneFunc = None):
        """
        name: a context name that should be used in common with the
              client code.
        uniqueName: should be a unique name for this Barrier, used
                    for timeout doLater
        avIdList: list of avatars from which we'll expect responses
        timeout: how long to wait before giving up
        clearedFunc: func to call when all avatars have cleared the barrier;
                     takes no arguments
        timeoutFunc: func to call when the timeout has expired;
                     takes list of avIds of avatars that did not
                     clear the barrier
        doneFunc:    func to call when the the barrier is complete for
                     either reason; takes list of avIds of avatars that
                     successfully cleared the barrier

        Call Barrier.clear(avId) when you get a response from
        each avatar.

        If you need to have additional parameters passed to your
        callback funcs, see PythonUtil.Functor
        """
        self.name = name
        self.uniqueName = uniqueName + '-Barrier'
        self.avIdList = avIdList[:]
        self.pendingAvatars = self.avIdList[:]
        self.timeout = timeout
        self.clearedFunc = clearedFunc
        self.timeoutFunc = timeoutFunc
        self.doneFunc = doneFunc

        if len(self.pendingAvatars) == 0:
            # If we are initialized with an empty list of avatars to
            # wait for, we consider ourselves cleared immediately.
            self.notify.debug(
                '%s: barrier with empty list' % (self.uniqueName))
            self.active = 0
            if self.clearedFunc:
                self.clearedFunc()
            if self.doneFunc:
                self.doneFunc(self.avIdList)
            return

        # choose a name for the timeout task
        self.taskName = self.uniqueName + '-Timeout'
        # this shouldn't be necessary, and it's kind of ugly;
        # in any case, it's better than bringing down the AI server
        # with an assert
        origTaskName = self.taskName
        while taskMgr.hasTaskNamed(self.taskName):
            self.taskName = origTaskName + '-' + str(random.randint(0, 10000))

        # start the timeout
        taskMgr.doMethodLater(self.timeout,
                              self.__timerExpired,
                              self.taskName)

        # Hang hooks for each avatar to disappear.
        for avId in self.avIdList:
            event = simbase.air.getAvatarExitEvent(avId)
            self.acceptOnce(event, self.__handleUnexpectedExit, extraArgs=[avId])

        self.notify.debug(
            '%s: expecting responses from %s within %s seconds' %
            (self.uniqueName, self.avIdList, self.timeout))

        self.active = 1

    def cleanup(self):
        """
        call this if you're abandoning the barrier condition and
        discarding this object
        """
        if self.active:
            taskMgr.remove(self.taskName)
            self.active = 0
        self.ignoreAll()

    def clear(self, avId):
        if not (avId in self.pendingAvatars):
            self.notify.warning(
                "%s: tried to clear %s, who was not listed." %
                (self.uniqueName, avId))
            return

        self.notify.debug('%s: clearing avatar %s' % (self.uniqueName, avId))
        self.pendingAvatars.remove(avId)
        if len(self.pendingAvatars) == 0:
            self.notify.debug(
                '%s: barrier cleared by %s' % (self.uniqueName, self.avIdList))
            self.cleanup()
            if self.clearedFunc:
                self.clearedFunc()
            if self.doneFunc:
                self.doneFunc(self.avIdList)

    def isActive(self):
        return self.active

    def getPendingAvatars(self):
        return self.pendingAvatars[:]

    def __timerExpired(self, task):
        self.notify.warning(
            '%s: timeout expired; responses not received from %s' %
            (self.uniqueName, self.pendingAvatars))
        self.cleanup()
        # report which avatars have not responded
        if self.timeoutFunc:
            self.timeoutFunc(self.pendingAvatars[:])
        if self.doneFunc:
            clearedAvIds = self.avIdList[:]
            for avId in self.pendingAvatars:
                clearedAvIds.remove(avId)
            self.doneFunc(clearedAvIds)

        return Task.done

    def __handleUnexpectedExit(self, avId):
        if avId not in self.avIdList:
            return

        self.avIdList.remove(avId)
        if avId in self.pendingAvatars:
            self.clear(avId)

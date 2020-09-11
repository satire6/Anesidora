from direct.distributed import DistributedObjectAI
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.golf import DistributedGolfCourseAI
from pandac.PandaModules import *

# This map is only used for support of the magic word ~golf hole
RequestHole = {}

def GolfManagerAI(): #singleton
    if not hasattr(simbase, 'golf'):
        simbase.golf = __GolfManagerAI()
    return simbase.golf

class __GolfManagerAI(DirectObject.DirectObject):
    notify = directNotify.newCategory("GolfManagerAI")
    def __init__(self):
        DirectObject.DirectObject.__init__(self)
        self.courseList = []
        
    def delete(self):
        DirectObject.DirectObject.delete(self)

    def readyGolfCourse(self, avIds, courseId = 0):
        self.notify.debug('readyGolfCourse avIds=%s courseId=%d' %
                          (avIds, courseId))
        golfZone = simbase.air.allocateZone()

        preferredHoleId = None
        for avId in avIds:
            if avId in RequestHole:
                preferredHoleId = RequestHole[avId][0]
        
        newCourse = DistributedGolfCourseAI.DistributedGolfCourseAI(golfZone, avIds, courseId, preferredHoleId)
        newCourse.generateWithRequired(golfZone)
        
        self.courseList.append(newCourse)
        newCourse.addExpectedGolfers(avIds)
        
        golfZone = newCourse.getZoneId()
        self.notify.debug('%s' %  self)
        self.notify.debug('returning %d' % golfZone)
        return golfZone

    def findGolfCourse(self, avId):
        """Return the DistributedGolfCourseAI that contains avId. Return None if not found."""
        retval = None

        for course in self.courseList:
            if avId in course.avIdList:
                retval = course
                break

        return retval

    def removeCourse(self, course):
        """Remove the course from the courseList."""
        if course in self.courseList:
            for avId in course.avIdList:
                if avId in RequestHole:
                    if not RequestHole[avId][1]:
                        del RequestHole[avId]
            self.courseList.remove(course)
        

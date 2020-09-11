"""Trajectory module: contains the Trajectory class"""

from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from math import *

class Trajectory:
    # represents the flight (or a portion of the flight) of a projectile

    # Notify category for trajectories
    notify = DirectNotifyGlobal.directNotify.newCategory("Trajectory")

    # for simplicity, we'll assume that gravity is the only
    # force acting on the projectile during flight.
    # g = 9.8 m/s^2 = 32 ft/s^2
    gravity = 32.0

    # again for simplicity, we'll assume that all projectiles (toons)
    # have the same collision radius
    __radius = 2.0

    # the projectile's velocity is constant in the X and Y directions.
    # the projectile's motion in the Z (up) direction is parabolic
    # due to the constant force of gravity, which acts in the -Z direction
    # with constant force

    def __init__(self, startTime, startPos, startVel, gravMult = 1.0):
        self.setStartTime(startTime)
        self.setStartPos(startPos)
        self.setStartVel(startVel)
        self.setGravityMult(gravMult)

    # these can be changed at any time; the Trajectory is stateless.
    def setStartTime(self, t):
        self.__startTime = t

    def setStartPos(self, sp):
        self.__startPos = sp

    def setStartVel(self, sv):
        self.__startVel = sv

    def setGravityMult(self, mult):
        self.__zAcc = mult * -Trajectory.gravity

    def getStartTime(self):
        return self.__startTime

    def __str__(self):
        return 'startTime: %s, startPos: %s, startVel: %s, zAcc: %s' % (
            self.__startTime, repr(self.__startPos),
            repr(self.__startVel), self.__zAcc)

    def __calcTimeOfHighestPoint(self):
        """__calcTimeOfHighestPoint(self)
        returns the time of the highest point of the projectile's
        trajectory
        """

        # the highest point of the trajectory is reached when the
        # Z velocity is equal to zero

        # for constant acceleration:
        # v = v_0 + (a*t)
        # so, we know v, v_0, and a, so solve for t
        # 0 = v_0 + (a*t)
        # a*t = -v_0
        # t = -(v_0 / a)
        t = -self.__startVel[2] / self.__zAcc

        # if t is negative, the projectile starts at its highest point
        if t < 0:
            t = 0

        return t + self.__startTime

    def calcTimeOfImpactOnPlane(self, height = 0):
        """calcTimeOfImpactOnPlane(self, float)
        uses the quadratic formula to calculate the projectile's
        time of impact on a horizontal surface at a given height
        ignores cases where projectile punches up through the
        plane
        """

        # quadratic equation: at^2 + bt + c = 0
        # quadratic formula:  t = [-b +/- sqrt(b^2 - 4ac)] / 2a

        # position equation with constant acceleration:
        # p(t) = p_0 + (v_0 * t) + (0.5 * a * t^2)

        # get our parameters
        a = self.__zAcc * 0.5
        b = self.__startVel[2]
        c = self.__startPos[2] - height

        # calculate the determinant (b^2 - 4ac)
        D = (b * b) - (4.0 * a * c)

        if D < 0:
            # the projectile never reaches the height specified
            # return an invalid time
            return -1.0
        elif D == 0:
            # if determinant is zero, there is only one root
            t = (-b) / (2.0 * a)
        else:
            # otherwise, only return the larger root
            # This is on the assumption that we only care about
            # collisions where the projectile has negative
            # Z velocity
            t = (-b - sqrt(D)) / (2.0 * a)

            ## # otherwise we could do something like this
            ## sqrtD = sqrt(D)
            ## t1 = (-b - sqrtD) / (2.0 * a)
            ## t2 = (-b + sqrtD) / (2.0 * a)
            ## if t2 < 0:
            ##     t = t1
            ## else:
            ##     t = min(t1, t2)

        # if t is negative, the projectile starts below the plane and descends (??)
        if t < 0:
            return -1.0

        return t + self.__startTime


    def calcZ(self, t):
        """calcZ(self, float)
        returns z-coordinate of projectile at a given point in time
        """
        tt = t - self.__startTime
        return self.__startPos[2] + (self.__startVel[2] * tt) + (0.5 * self.__zAcc * tt * tt)

    def __reachesHeight(self, height):
        """__reachesHeight(self, float)
        returns non-zero if the projectile reaches the given height
        """
        if self.calcZ(self.__calcTimeOfHighestPoint()) < height:
            return 0
        return 1

    def getPos(self, t):
        """getPos(self, float)
        Returns the position of the projectile at time 't'
        """
        tt = t - self.__startTime
        return Point3(self.__startPos[0] + (self.__startVel[0] * tt),
                      self.__startPos[1] + (self.__startVel[1] * tt),
                      self.calcZ(t))

    def getVel(self, t):
        """getVel(self, float)
        Returns the velocity of the projectile at time 't'
        """
        tt = t - self.__startTime
        return Vec3(self.__startVel[0],
                    self.__startVel[1],
                    self.__startVel[2] + (self.__zAcc * tt))

    def getStartTime(self):
        return self.__startTime

    def checkCollisionWithGround(self, height = 0):
        return self.calcTimeOfImpactOnPlane(height)

    def checkCollisionWithDisc(self, discCenter, discRadius):
        """checkCollisionWithDisc(self, Point3, float)
        check for collision with a horizontal disc, with negative Z velocity
        returns time of impact
        if no collision, time will be negative
        """
        # does the trajectory ever reach the height of the disc?
        if self.__reachesHeight(discCenter[2]) == 0:
            return -1.0

        # when is the projectile at the height of the disc (and descending)?
        t_atDiscHeight = self.calcTimeOfImpactOnPlane(discCenter[2])

        if t_atDiscHeight < 0:
            return -1.0

        # what is the projectile's position at that moment?
        p_atDiscHeight = self.getPos(t_atDiscHeight)

        # check that position against the disc
        # use pythagorean theorem to get distance in flat 2D plane between
        # projectile's X,Y position and the disc center's X,Y position
        offset_x = p_atDiscHeight[0] - discCenter[0]
        offset_y = p_atDiscHeight[1] - discCenter[1]
        # leave it squared, we're only comparing distances, we can compare
        # squared distances just as well
        offset_from_center_SQUARED = (offset_x * offset_x) + (offset_y * offset_y)

        # what is the maximum offset at which the projectile can be from the
        # center of the disc, and still be considered to collide with the disc?
        max_offset = discRadius
        max_offset_SQUARED = max_offset * max_offset

        if offset_from_center_SQUARED < max_offset_SQUARED:
            # we've got a collision
            return t_atDiscHeight
        else:
            # no collision
            return -1.0

    def calcEnterAndLeaveCylinderXY(self, cylBottomCenter, cylRadius):
        """calcEnterAndLeaveTimesOverCylinder(self, Point3, float)
        returns two time values, representing the times when the trajectory
        will enter and leave the area occupied by the cylinder on the X,Y plane
        if the trajectory never intersects the cylinder in X and Y, returns -1, -1
        if the trajectory only intersects the cylinder at one time (t), returns t, t
        """
        # calculate points where trajectory intersects the cylinder in the X,Y plane
        # (trajectory is a straight line in X,Y plane)

        # Real-Time Rendering, p.296
        # intersection of circle and ray
        # ray: f(t) = o + td
        # circle: f(p) = ||p - v|| - r = 0
        # v=circle center, r=circle radius, o=ray origin, d=unit direction vector
        # intersection of circle and ray:
        # t = -b +/- sqrt(b^2 - c)
        #   where b = d*(o-v), c = (o-v)*(o-v)-r^2
        v = Vec2(cylBottomCenter[0], cylBottomCenter[1])
        ##r = cylRadius
        o = Vec2(self.__startPos[0], self.__startPos[1])
        d = Vec2(self.__startVel[0], self.__startVel[1])
        d.normalize()
        b = d.dot(o - v)
        c = (o - v).dot(o - v) - (cylRadius * cylRadius)

        # if b^2 - c < 0, no intersection
        # if == 0, ray just grazes circle; ignore
        bsmc = (b * b) - c
        if bsmc <= 0.0:
            return -1.0, -1.0

        ##self.notify.debug("trajectory passes through tower in X,Y")

        # otherwise, find two values of t where ray intersects circle
        sqrt_bsmc = sqrt(bsmc)
        t1 = -b - sqrt_bsmc # entering the cylinder's (X,Y) region
        t2 = -b + sqrt_bsmc # leaving the cylinder's (X,Y) region

        if t1 > t2:
            self.notify.debug("calcEnterAndLeaveCylinderXY: t1 > t2??")

        # adjust the time values for our velocity; they are based on unit velocity
        mag = Vec2(self.__startVel[0], self.__startVel[1]).length()
        t1 = t1 / mag
        t2 = t2 / mag

        return t1 + self.__startTime, t2 + self.__startTime

    def checkCollisionWithCylinderSides(self, cylBottomCenter, cylRadius, cylHeight):
        """checkCollisionWithCylinderSides(self, Point3, float, float)
        check for collision with the sides of a cylinder
        returns time of impact
        if no collision, time will be negative
        """
        # does the trajectory ever reach the height of the cylinder bottom?
        if self.__reachesHeight(cylBottomCenter[2]) == 0:
            return -1.0

        # calc times of entering and leaving the cylinder's space in the X,Y plane
        t1, t2 = self.calcEnterAndLeaveCylinderXY(cylBottomCenter, cylRadius)

        # calculate points
        p1 = self.getPos(t1)
        p2 = self.getPos(t2)

        ##self.notify.debug("points: " + str(p1) + ", " + str(p2))

        # if both points are above the cylinder, reject
        cylTopHeight = cylBottomCenter[2] + cylHeight
        if p1[2] > cylTopHeight and p2[2] > cylTopHeight:
            return -1.0

        # if p1 is a hit, accept
        if p1[2] < cylTopHeight and p1[2] > cylBottomCenter[2]:
            # make sure the collision happens after launch
            if t1 > self.__startTime:
                return t1

        # this code works for checking against cylinder top; we don't want it, though
##         # otherwise, projectile hits top of cylinder
##         t_cylTop = self.calcTimeOfImpactOnPlane(cylTopHeight)

##         if t_cylTop < t1:
##             self.notify.debug("checkCollisionWithCylinder: projectile hits cylinder top plane before it reaches cylinder?")
##             return -1.0
##         elif t_cylTop > t2:
##             self.notify.debug("checkCollisionWithCylinder: projectile hits cylinder top plane after it passes cylinder?")
##             return -1.0

##         return t_cylTop

        return -1.0

    def checkCollisionWithProjectile(self, projectile):
        """checkCollisionWithProjectile(self, Projectile)
        check for collision with another Projectile's trajectory
        returns time of impact
        if no collision, time will be negative
        """
        # TODO

        # calculate intersection of trajectories in X,Y plane
        # if there's an intersection, compare heights at that point
        return -1.0


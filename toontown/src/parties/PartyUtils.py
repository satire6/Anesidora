#-------------------------------------------------------------------------------
# Contact: Rob Gordon, Edmundo Ruiz, Shawn Patton (Schell Games)
# Created: Sep 2008
#
# Purpose: Utility functions for parties.
#-------------------------------------------------------------------------------
import math
import time
import datetime

from direct.directnotify import DirectNotifyGlobal
from direct.interval.LerpInterval import LerpFunc

from pandac.PandaModules import Vec3

from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownTimer import ToontownTimer

from toontown.parties import PartyGlobals

notify = DirectNotifyGlobal.directNotify.newCategory("PartyUtils")

def getNewToontownTimer():
    """Returns a new instance of a Toontown Timer that has the look for party activities."""
    timer = ToontownTimer()
    timer.hide()
    timer.posInTopRightCorner()
    timer.setColor(1, 1, 1, 0.75)
    
    return timer

def getPartyActivityIcon(activityIconsModel, activityName):
    """
    Finds and returns the proper activity's icon. If it can't find it, it returns
    the clock icon with a warning.
    
    Parameters
        activityIconsModel the loaded activity icons texture card model
        activityName the name of the activity
        
    Returns
        activity icon NodePath
    """
    icon = activityIconsModel.find("**/%sIcon" % activityName)
    if icon.isEmpty():
        icon = activityIconsModel.find("**/PartyClockIcon")
        notify.warning("Couldn't find %sIcon in %s, using PartyClockIcon" %
                        (activityName, activityIconsModel.getName())
                        )
        
    return icon

def arcPosInterval( duration, object, pos, arcHeight, other ):
        startPos = object.getPos()
        endPos = object.getParent().getRelativePoint( other, pos )
        startX = startPos.getX()
        startY = startPos.getY()
        startZ = startPos.getZ()
        dx = endPos.getX() - startPos.getX()
        dy = endPos.getY() - startPos.getY()
        dz = endPos.getZ() - startPos.getZ()
        def setArcPos( t ):
            newX = startX + dx*t
            newY = startY + dy*t
            newZ = startZ + dz*t + arcHeight*(-(2.0*t - 1.0)**2 + 1.0) # parabola
            object.setPos( newX, newY, newZ )

        return LerpFunc( setArcPos, duration=duration )

def formatDate( year, month, day ):
    """
    year: year in datetime format (1-9999)
    month: month in datetime format (1-12)
    day: day of the month in datetime format (1-number of days in given month
         and year)
    
    returns a string
    """
    monthString = TTLocalizer.DateOfBirthEntryMonths[month-1]
    return TTLocalizer.PartyDateFormat % { 'mm':monthString, 'dd':day, 'yyyy':year }

def truncateTextOfLabelBasedOnWidth(directGuiObject, textToTruncate, maxWidth):
    # This implementation is much much faster than the previous one,
    # a 20 party list took longer than 2 minutes to come up
    #width = directGuiObject.getWidth()
    text0 = directGuiObject.component("text0")
    tempNode = text0.textNode
    currentText = textToTruncate[:]
    scale = text0.getScale()[0]
    width = tempNode.calcWidth(currentText) * scale
    while width > maxWidth:
        currentText = currentText[:-1]
        width = tempNode.calcWidth(currentText) * scale
    directGuiObject["text"] = currentText
    if directGuiObject["text"] != textToTruncate:
        directGuiObject["text"] = "%s..."%directGuiObject["text"]

def truncateTextOfLabelBasedOnMaxLetters(directGuiObject, textToTruncate, maxLetters):
    # the frameSize for the host name is way bigger now, it's faster just to base it on num letters
    curStr = directGuiObject["text"]
    if maxLetters < len(curStr):
        curStr = curStr[:maxLetters]
        curStr += "..."
        directGuiObject["text"] = curStr

def scaleTextOfGuiObjectBasedOnWidth(directGuiObject, textToScale, maxWidth):
    width = directGuiObject.getWidth()
    scale = 0.01
    while width > maxWidth:
        directGuiObject["text_scale"] = scale
        directGuiObject.resetFrameSize()
        width = directGuiObject.getWidth()
        scale += 0.005

def formatTime( hour, minute ):
    """
    hour: hours in datetime format (0-23)
    minute: minutes in datetime format (0-59)
    
    returns a string
    """
    meridiemString = TTLocalizer.PartyTimeFormatMeridiemAM
    if hour == 0:
        hour = 12 
    elif hour > 11:
        meridiemString = TTLocalizer.PartyTimeFormatMeridiemPM
    if  hour > 12:
        hour -= 12
    return TTLocalizer.PartyTimeFormat % ( hour, minute, meridiemString )

SecondsInOneDay = 60 * 60 * 24 # 60 seconds per minute, 60 minutes per hour, 24 hours

def getTimeDeltaInSeconds(td):
    """From the passed in timedelta, return the normalized seconds (possible negative."""
    result = (td.days * SecondsInOneDay)  + td.seconds + (td.microseconds / 1000000.0)
    return result

def formatDateTime(dateTimeToShow, inLocalTime=False ):
    # If inLocalTime is True return the formatted datetime with respect to the
    # users local time
    if inLocalTime:
        curServerTime = base.cr.toontownTimeManager.getCurServerDateTime()
        ltime = time.localtime()
        localTime = datetime.datetime(
            year=ltime.tm_year,
            month=ltime.tm_mon,
            day=ltime.tm_mday,
            hour=ltime.tm_hour,
            minute=ltime.tm_min,
            second = ltime.tm_sec
        )
        naiveServerTime = curServerTime.replace(tzinfo=None)
        newTimeDelta = localTime - naiveServerTime
        localDifference = getTimeDeltaInSeconds(newTimeDelta)
        dateTimeToShow = dateTimeToShow + datetime.timedelta(seconds=localDifference)
        return "%s %s" % (formatDate(dateTimeToShow.year, dateTimeToShow.month, dateTimeToShow.day), formatTime(dateTimeToShow.hour, dateTimeToShow.minute))    
    else:
        return "%s %s" % (formatDate(dateTimeToShow.year, dateTimeToShow.month, dateTimeToShow.day), formatTime(dateTimeToShow.hour, dateTimeToShow.minute))    

def convertDistanceToPartyGrid(d, index):
    """
    Converts d from Panda space to party grid space. We use party grid
    space when storing party activity location information in the Uberdog
    database or when sending it across the wire.
    index is 0 for x values, 1 for y values since we're dealing with non-square
    grid squares
    
    Returns converted d 
    """
    return int((d - PartyGlobals.PartyGridToPandaOffset[index])/PartyGlobals.PartyGridUnitLength[index])
    
def convertDistanceFromPartyGrid(d, index):
    """
    Converts d from Party Grid space to Panda space.
    index is 0 for x values, 1 for y values since we're dealing with non-square
    grid squares
   
    Returns converted d
    """
    return d*PartyGlobals.PartyGridUnitLength[index] + PartyGlobals.PartyGridToPandaOffset[index] + PartyGlobals.PartyGridUnitLength[index]/2.0
    
def convertDegreesToPartyGrid( h ):
    """
    Returns h in party grid space, converted from Panda space (in degrees)
    """
    # clamp to [0-360]
    while h < 0.0:
        h = h + 360.0
    h = h % 360.0
    return int(h/PartyGlobals.PartyGridHeadingConverter)

def convertDegreesFromPartyGrid( h ):
    """
    Returns h in Panda space (in degrees), converted from party grid space.
    """
    return h*PartyGlobals.PartyGridHeadingConverter

def getCenterPosFromGridSize(x, y, gridsize):
    """
    Given an x,y in Panda space and a party object grid size, returns the center x,y in Panda space.
    Used for centering an even-sized object in Panda space, because normally the x,y coords are 
    centered within a grid square; for even-sized objects the center is between two grid squares.
    """
    if gridsize[0] % 2 == 0:
        xMod = PartyGlobals.PartyGridUnitLength[0]/2.0
    else:
        xMod = 0
    if gridsize[1] % 2 == 0:
        yMod = PartyGlobals.PartyGridUnitLength[1]/2.0
    else:
        yMod = 0
    return x + xMod, y + yMod
    
#===============================================================================
# Math Helpers
#===============================================================================

def toRadians(angle):
    return angle*math.pi/180.0

def toDegrees(angle):
    return angle*180.0/math.pi

# assuming that rotation and angle are radians
def calcVelocity(rotation, angle, initialVelocity = 1.0):
    horizVel = initialVelocity * math.cos(angle)
    xVel = horizVel * -math.sin(rotation)
    yVel = horizVel * math.cos(rotation)
    zVel = initialVelocity * math.sin(angle)
    
    return Vec3(xVel, yVel, zVel)

class LineSegment:
    """
    Used for calculating intersections between two line segments.
    """
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        
    def isIntersecting( self, line, compare=None ):
        x1 = self.pt1.getX()
        x2 = self.pt2.getX()
        x3 = line.pt1.getX()
        x4 = line.pt2.getX()
        y1 = self.pt1.getY()
        y2 = self.pt2.getY()
        y3 = line.pt1.getY()
        y4 = line.pt2.getY()
        
        top1 = (x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)
        top2 = (x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)
        bot  = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        
        if bot == 0.0:
            return False
        
        u1 = top1/bot
        u2 = top2/bot

        if compare is None:
            return (0 <= u1 and u1 <= 1) and (0 <= u2 and u2 <= 1)
        elif compare == "segment-ray":
            return (0 <= u1 and u1 <= 1) and (0 <= u2)
        elif compare == "ray-ray":
            return (0 <= u1) and (0 <= u2)
        elif compare == "ray-segment":
            return (0 <= u1) and (0 <= u2 and u2 <= 1)


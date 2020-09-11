import time
from datetime import datetime, timedelta
import pytz
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class ToontownTimeManager(DistributedObject.DistributedObject):
    """
    A class to keep track of toontown time. Toontown time is essentially the
    server time, and matches the time zone and daylight savings changes.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownTimeManager")

    ClockFormat = '%I:%M:%S %p' # uses am or pm
    #ClockFormat = '%H:%M:%S' # military time
    formatStr= "%Y-%m-%d %H:%M:%S" 

    def __init__(self, serverTimeUponLogin=0, clientTimeUponLogin=0,
                 globalClockRealTimeUponLogin=0):
        """Construct ourself. Default values are at 1970"""
        # TODO: Perhaps the AI and UD should have their own version of this class? SG-SLWP
        try:
            self.serverTimeZoneString = base.config.GetString('server-timezone',TTLocalizer.TimeZone)
        except:
            try:
                self.serverTimeZoneString = simbase.config.GetString('server-timezone',TTLocalizer.TimeZone)
            except:
                notify.error("ToontownTimeManager does not have access to base or simbase.")
        self.serverTimeZone = pytz.timezone(self.serverTimeZoneString)
        self.updateLoginTimes(serverTimeUponLogin, clientTimeUponLogin,
                              globalClockRealTimeUponLogin)
        self.debugSecondsAdded = 0

    def updateLoginTimes(self, serverTimeUponLogin, clientTimeUponLogin,
                 globalClockRealTimeUponLogin):
        """Update our fields to the new data"""
        # import calendar
        # test transition from EDT to EST
        # gmtime = calendar.timegm((2008, 11, 2, 5, 55, 0, 0, 0)) # equal to 12:59 am EDT
        # test transition from EST to EDT
        # gmtime = calendar.timegm((2009, 3, 8, 6, 55, 0, 0, 0)) # equal to 1:55 am EST
        # self.debugServerTime = gmTime
        # self.serverTimeUponLogin = debugServerTime
        # serverTimeUponLogin is in UTC!!!
        self.serverTimeUponLogin = serverTimeUponLogin
        self.clientTimeUponLogin = clientTimeUponLogin
        self.globalClockRealTimeUponLogin = globalClockRealTimeUponLogin
        naiveTime = datetime.utcfromtimestamp(
            self.serverTimeUponLogin)
        self.utcServerDateTime = naiveTime.replace(tzinfo = pytz.utc)
        self.serverDateTime = datetime.fromtimestamp(
            self.serverTimeUponLogin, self.serverTimeZone)

    def getCurServerDateTime(self):
        """Return the current datetime object of the server."""
        secondsPassed = globalClock.getRealTime() - self.globalClockRealTimeUponLogin + \
                        self.debugSecondsAdded
        curDateTime = self.serverTimeZone.normalize(
            self.serverDateTime + timedelta(seconds=secondsPassed))
        return curDateTime

    def getCurServerDateTimeForComparison(self):
        """Return the current UNnormalized datetime object of the server."""
        # PartyInfo.startTime is in PST, this force the return value to always be in PST
        secondsPassed = globalClock.getRealTime() - self.globalClockRealTimeUponLogin + \
                        self.debugSecondsAdded
        curDateTime = self.serverDateTime + timedelta(seconds=secondsPassed)
        curDateTime = curDateTime.replace(tzinfo = self.serverTimeZone)
        return curDateTime    

    def getCurServerTimeStr(self):
        """Return a string representation of the current server time."""
        curDateTime = self.getCurServerDateTime()
        result = curDateTime.strftime(self.ClockFormat)
        if result[0] == '0':
            result = result [1:]
        return result

    def setDebugSecondsAdded(self, moreSeconds):
        """Add more seconds to simulate more time passing."""
        self.debugSecondsAdded = moreSeconds

    def debugTest(self):
        """Print debug function results testing dst."""
        startTime = datetime.today()
        serverTzInfo = self.serverTimeZone
        startTime = startTime.replace(tzinfo=serverTzInfo)
        self.notify.info('startTime = %s' % startTime)
        serverTime = self.getCurServerDateTime()
        self.notify.info("serverTime = %s" % serverTime)
        result = startTime <= serverTime
        self.notify.info("start < serverTime %s" % result)
        startTime1MinAgo = startTime + timedelta(minutes = -1)
        self.notify.info('startTime1MinAgo = %s' % startTime1MinAgo)
        result2 = startTime1MinAgo <= serverTime
        self.notify.info("startTime1MinAgo < serverTime %s" % result2)
        serverTimeForComparison = self.getCurServerDateTimeForComparison()
        self.notify.info("serverTimeForComparison = %s" % serverTimeForComparison)
        result3 = startTime1MinAgo <= serverTimeForComparison
        self.notify.info("startTime1MinAgo < serverTimeForComparison %s" % result3)

    def convertStrToToontownTime(self, dateStr):
        """Converts a date string and returns a last logged in time, any errors returns current server time."""
        curDateTime = self.getCurServerDateTime()
        try:
            # warning time.mktime was giving a different result in published build vs
            # what I was seeing in my local dev environment, it was ahead by 1 hour
            # interpretation of the -1 for dst flag was different
            curDateTime = datetime.fromtimestamp(time.mktime(time.strptime(dateStr, self.formatStr)), self.serverTimeZone)
            curDateTime = self.serverTimeZone.normalize(curDateTime)
        except:
            self.notify.warning("error parsing date string=%s" % dateStr)
            pass
        result= curDateTime
        return result

    def convertUtcStrToToontownTime(self, dateStr):
        """Converts a utc date string and returns toontown time, any errors returns current server time."""
        curDateTime = self.getCurServerDateTime()
        try:
            # we changed implementation since time.mktime is giving a incorrect result in published build            
            timeTuple = time.strptime(dateStr, self.formatStr)
            utcDateTime = datetime(timeTuple[0], timeTuple[1], timeTuple[2],
                                   timeTuple[3], timeTuple[4], timeTuple[5],
                                   timeTuple[6], pytz.utc)
            curDateTime = utcDateTime.astimezone(self.serverTimeZone)
            curDateTime= self.serverTimeZone.normalize(curDateTime)
        except:
            self.notify.warning("error parsing date string=%s" % dateStr)
            pass
        result= curDateTime
        return result    

        
                         

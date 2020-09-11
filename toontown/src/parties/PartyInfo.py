# python imports
from datetime import datetime

# panda imports
from direct.directnotify import DirectNotifyGlobal

# toontown imports
from toontown.parties.PartyGlobals import InviteTheme
from toontown.parties.DecorBase import DecorBase
from toontown.parties.ActivityBase import ActivityBase

class PartyInfoBase:
    """
    Python friendly representation of a single party.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("PartyInfoBase")
    
    def __init__(self, partyId, hostId,
                 startYear, startMonth, startDay, startHour, startMinute,
                 endYear, endMonth, endDay, endHour, endMinute,
                 isPrivate,
                 inviteTheme,
                 activityList,
                 decors,
                 status):
        """Construct the party info."""
        self.partyId = partyId
        self.hostId = hostId
        
        self.startTime = datetime(startYear, startMonth, startDay, startHour, startMinute)
        self.endTime = datetime(endYear, endMonth, endDay, endHour, endMinute)
        self.isPrivate = isPrivate
        self.inviteTheme = inviteTheme
        self.activityList = []
        for oneItem in activityList:
            newActivity = ActivityBase(
                oneItem[0], # activityID
                oneItem[1], # x position
                oneItem[2], # y position
                oneItem[3], # heading
            )
            self.activityList.append(newActivity)
        self.decors = []
        for oneItem in decors:
            newDecor = DecorBase(
                oneItem[0], # decoration ID
                oneItem[1], # x position
                oneItem[2], # y position
                oneItem[3], # heading
            )
            self.decors.append(newDecor)
        self.status = status # see PartyGlobals.PartyStatus

    def getActivityIds(self):
        activities = []
        for activityBase in self.activityList:
            activities.append(activityBase.activityId)
        return activities

    def __str__(self):
        """Return a useful string representation of this object."""
        string = "partyId=%d " % self.partyId
        string += "hostId=%d " % self.hostId
        string += "start=%s " % self.startTime
        string += "end=%s " % self.endTime
        string += "isPrivate=%s " % self.isPrivate
        string += "inviteTheme=%s " % InviteTheme.getString(self.inviteTheme)
        string += "activityList=%s " % self.activityList
        string += "decors=%s " % self.decors
        string += "status=%s" % self.status
        string += "\n" # I need a line break to read the debug output easier
        return string

    def __repr__(self):
        """Return a string used in debugging."""
        return self.__str__()

class PartyInfo (PartyInfoBase):
    """
    Client side representation of party information, note the use of base.cr
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("PartyInfo")
    
    def __init__(self, partyId, hostId,
                 startYear, startMonth, startDay, startHour, startMinute,
                 endYear, endMonth, endDay, endHour, endMinute,
                 isPrivate,
                 inviteTheme,
                 activityList,
                 decors,
                 status):
        """Construct the party info."""
        PartyInfoBase.__init__(self, partyId, hostId,
                 startYear, startMonth, startDay, startHour, startMinute,
                 endYear, endMonth, endDay, endHour, endMinute,
                 isPrivate,
                 inviteTheme,
                 activityList,
                 decors,
                 status)
        # make the start and end times timezone aware to facilitate
        # direct comparisons with getCurServerDateTime
        serverTzInfo = base.cr.toontownTimeManager.serverTimeZone
        self.startTime = self.startTime.replace(tzinfo=serverTzInfo)
        self.endTime = self.endTime.replace(tzinfo=serverTzInfo)

class PartyInfoAI (PartyInfoBase):
    """
    AI side representation of party information, note the use of simbase.air
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("PartyInfo")
    
    def __init__(self, partyId, hostId,
                 startYear, startMonth, startDay, startHour, startMinute,
                 endYear, endMonth, endDay, endHour, endMinute,
                 isPrivate,
                 inviteTheme,
                 activityList,
                 decors,
                 status):
        """Construct the party info."""
        PartyInfoBase.__init__(self, partyId, hostId,
                 startYear, startMonth, startDay, startHour, startMinute,
                 endYear, endMonth, endDay, endHour, endMinute,
                 isPrivate,
                 inviteTheme,
                 activityList,
                 decors,
                 status)
        # make the start and end times timezone aware to facilitate
        # direct comparisons with getCurServerDateTime

        serverTzInfo = simbase.air.toontownTimeManager.serverTimeZone
        self.startTime = self.startTime.replace(tzinfo=serverTzInfo)
        self.endTime =  self.endTime.replace(tzinfo=serverTzInfo)    

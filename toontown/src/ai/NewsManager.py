from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import SuitBattleGlobals
from toontown.toonbase import TTLocalizer
import HolidayDecorator
import HalloweenHolidayDecorator
import CrashedLeaderBoardDecorator
from direct.interval.IntervalGlobal import *
import calendar
from copy import deepcopy

decorationHolidays = [ToontownGlobals.WINTER_DECORATIONS, ToontownGlobals.HALLOWEEN_PROPS, ToontownGlobals.HALLOWEEN_COSTUMES, ToontownGlobals.CRASHED_LEADERBOARD,]

# These holidays cause the 'promotional' speedchat menu to show up;
# only one of these should be active at a time!
# If we want to support multiple simultaneously, we'll have to figure out a
# different way of putting the menus into the SpeedChat menu. Currently
# there's a hidden menu that's always in the SpeedChat, waiting for one of
# these holidays to come along, at which point it populates itself with
# phrases and becomes visible. We *could* add a menu for every possible
# holiday, but that seems inefficient. We could also dynamically insert the
# menus, but we don't have a robust method of inserting menus and items
# into the SpeedChat beyond inserting at a specific index.
promotionalSpeedChatHolidays = [ToontownGlobals.ELECTION_PROMOTION]

class NewsManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("NewsManager")
    
    neverDisable = 1

    YearlyHolidayType = 1
    OncelyHolidayType = 2
    RelativelyHolidayType = 3
    OncelyMultipleStartHolidayType = 4

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.population = 0
        self.invading = 0
        # This is the current holiday Id just for decorations
        # Only one decoration holiday is active at a time
        self.decorationHolidayIds = []
        self.holidayDecorator = None
        # This dictionary keeps track of all active holidays
        # Multiple holidays may be active (i.e. decorations and fireworks)
        self.holidayIdList = []

        # Attach myself to the cr so others can access
        base.cr.newsManager = self

        # Reset battle mult in case localToon just switched districts
        base.localAvatar.inventory.setInvasionCreditMultiplier(1)

        self.weeklyCalendarHolidays = []

    def delete(self):
        self.cr.newsManager = None
        if self.holidayDecorator:
            self.holidayDecorator.exit()
        DistributedObject.DistributedObject.delete(self)

    def setPopulation(self, population):
        self.population = population
        messenger.send("newPopulation", [population])

    def getPopulation(self):
        return population
        
    def sendSystemMessage(self, message, style):
        base.localAvatar.setSystemMessage(style, message)
        
    def setInvasionStatus(self, msgType, cogType, numRemaining, skeleton):
        # Let the player know the status of any cog invasion taking place
        self.notify.info("setInvasionStatus: msgType: %s cogType: %s, numRemaining: %s, skeleton: %s" %
                         (msgType, cogType, numRemaining, skeleton))

        cogName = SuitBattleGlobals.SuitAttributes[cogType]['name']
        cogNameP = SuitBattleGlobals.SuitAttributes[cogType]['pluralname']

        if skeleton:
            cogName = TTLocalizer.Skeleton
            cogNameP = TTLocalizer.SkeletonP
            
        if msgType == ToontownGlobals.SuitInvasionBegin:
            msg1 = TTLocalizer.SuitInvasionBegin1
            msg2 = TTLocalizer.SuitInvasionBegin2 % cogNameP
            # Now are invading
            self.invading = 1
        elif msgType == ToontownGlobals.SuitInvasionUpdate:
            msg1 = TTLocalizer.SuitInvasionUpdate1 % numRemaining
            msg2 = TTLocalizer.SuitInvasionUpdate2 % cogNameP
            # Still invading
            self.invading = 1
        elif msgType == ToontownGlobals.SuitInvasionEnd:
            msg1 = TTLocalizer.SuitInvasionEnd1 % cogName
            msg2 = TTLocalizer.SuitInvasionEnd2
            # No longer invading
            self.invading = 0
        elif msgType == ToontownGlobals.SuitInvasionBulletin:
            msg1 = TTLocalizer.SuitInvasionBulletin1
            msg2 = TTLocalizer.SuitInvasionBulletin2 % cogNameP
            # Still invading
            self.invading = 1
        else:
            self.notify.warning("setInvasionStatus: invalid msgType: %s" % (msgType))
            return

        # Update our local display of skill credit to take the invasion
        # multiplier into account. The actual math and credit is given
        # on the AI, this is just to inform the player
        # TODO: this is slightly out of sync because this will get updated
        # as soon as the invasion is over, whereas the AI multiplier will
        # not, it is only updated at the start of each battle. Nobody should
        # complain since the error is in the favor of the Toons (we show less
        # than you might actually get)
        if self.invading:
            mult = ToontownBattleGlobals.getInvasionMultiplier()
        else:
            mult = 1
        base.localAvatar.inventory.setInvasionCreditMultiplier(mult)
        
        # TODO: this gets stomped at load time
        Sequence(
            Wait(1.0),
            Func(base.localAvatar.setSystemMessage, 0, msg1),
            Wait(5.0),
            Func(base.localAvatar.setSystemMessage, 0, msg2),
            name = 'newsManagerWait',
            autoPause = 1,
            ).start()
        return

    def getInvading(self):
        return self.invading

    def startHoliday(self, holidayId):
        if holidayId not in self.holidayIdList:
            self.notify.info("setHolidayId: Starting Holiday %s" % (holidayId))
            self.holidayIdList.append(holidayId)
            if holidayId in decorationHolidays:
                self.decorationHolidayIds.append(holidayId)
                if (hasattr(base.cr.playGame, 'dnaStore') and
                    hasattr(base.cr.playGame, 'hood') and
                    hasattr(base.cr.playGame.hood, 'loader')):
                    # Put up decorations
                    if holidayId == ToontownGlobals.HALLOWEEN_COSTUMES:
                        self.holidayDecorator = HalloweenHolidayDecorator.HalloweenHolidayDecorator()                        
                    elif holidayId == ToontownGlobals.CRASHED_LEADERBOARD:                    
                        self.holidayDecorator = CrashedLeaderBoardDecorator.CrashedLeaderBoardDecorator()
                    else:
                        self.holidayDecorator = HolidayDecorator.HolidayDecorator()
                    self.holidayDecorator.decorate()
                    messenger.send("decorator-holiday-%d-starting" % holidayId)
            elif holidayId in promotionalSpeedChatHolidays:
                if hasattr(base, 'TTSCPromotionalMenu'):
                    base.TTSCPromotionalMenu.startHoliday(holidayId)
            elif holidayId == ToontownGlobals.MORE_XP_HOLIDAY:
                self.setMoreXpHolidayStart()
            elif holidayId == ToontownGlobals.JELLYBEAN_DAY:
                self.setJellybeanDayStart()
            elif holidayId == ToontownGlobals.CIRCUIT_RACING_EVENT:
                self.setGrandPrixWeekendStart()
            elif holidayId == ToontownGlobals.HYDRANT_ZERO_HOLIDAY:
                self.setHydrantZeroHolidayStart()
            elif holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addAprilToonsMenu()   
            elif holidayId == ToontownGlobals.WINTER_CAROLING:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addCarolMenu()
            elif holidayId == ToontownGlobals.VALENTINES_DAY:
                messenger.send('ValentinesDayStart')
                base.localAvatar.setSystemMessage(0, TTLocalizer.ValentinesDayStart)
            elif holidayId == ToontownGlobals.SILLY_CHATTER_ONE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseOneMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_TWO:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseTwoMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_THREE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseThreeMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FOUR:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseFourMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FIVE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addSillyPhaseFiveMenu()
            elif holidayId == ToontownGlobals.VICTORY_PARTY_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.addVictoryPartiesMenu()
    
    def endHoliday(self, holidayId):
        if holidayId in self.holidayIdList:
            self.notify.info("setHolidayId: Ending Holiday %s" % (holidayId))
            self.holidayIdList.remove(holidayId)
            if holidayId in self.decorationHolidayIds:
                self.decorationHolidayIds.remove(holidayId)
                # Current holiday is over, remove decorations
                if (hasattr(base.cr.playGame, 'dnaStore') and
                    hasattr(base.cr.playGame, 'hood') and
                    hasattr(base.cr.playGame.hood, 'loader')):
                    if holidayId == ToontownGlobals.HALLOWEEN_COSTUMES:
                        self.holidayDecorator = HalloweenHolidayDecorator.HalloweenHolidayDecorator()                        
                    elif holidayId == ToontownGlobals.CRASHED_LEADERBOARD:                    
                        self.holidayDecorator = CrashedLeaderBoardDecorator.CrashedLeaderBoardDecorator()
                    else:
                        self.holidayDecorator = HolidayDecorator.HolidayDecorator()
                    self.holidayDecorator.undecorate()
                    messenger.send("decorator-holiday-%d-ending" % holidayId)
            elif holidayId in promotionalSpeedChatHolidays:
                if hasattr(base, 'TTSCPromotionalMenu'):
                    base.TTSCPromotionalMenu.endHoliday(holidayId)
            elif holidayId == ToontownGlobals.MORE_XP_HOLIDAY:
                self.setMoreXpHolidayEnd()
            elif holidayId == ToontownGlobals.JELLYBEAN_DAY:
                self.setJellybeanDayEnd()
            elif holidayId == ToontownGlobals.CIRCUIT_RACING_EVENT:
                self.setGrandPrixWeekendEnd()
            elif holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:            
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeAprilToonsMenu() 
            elif holidayId == ToontownGlobals.WINTER_CAROLING:            
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeCarolMenu()
            elif holidayId == ToontownGlobals.VALENTINES_DAY:
                messenger.send('ValentinesDayStop')
                base.localAvatar.setSystemMessage(0, TTLocalizer.ValentinesDayEnd)      
            elif holidayId == ToontownGlobals.SILLY_CHATTER_ONE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseOneMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_TWO:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseTwoMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_THREE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseThreeMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FOUR:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseFourMenu()
            elif holidayId == ToontownGlobals.SILLY_CHATTER_FIVE:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeSillyPhaseFiveMenu()
            elif holidayId == ToontownGlobals.VICTORY_PARTY_HOLIDAY:
                if hasattr(base, 'localAvatar') and base.localAvatar and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
                    base.localAvatar.chatMgr.chatInputSpeedChat.removeVictoryPartiesMenu()

    def setHolidayIdList(self, holidayIdList):
        def isEnding(id):
            return id not in holidayIdList
        def isStarting(id):
            return id not in self.holidayIdList
        # Which holidays are ending?
        toEnd = filter(isEnding, self.holidayIdList)
        for endingHolidayId in toEnd:
            self.endHoliday(endingHolidayId)
        # Which holidays are starting?
        toStart = filter(isStarting, holidayIdList)
        for startingHolidayId in toStart:
            self.startHoliday(startingHolidayId)
        messenger.send("setHolidayIdList", [holidayIdList])

    def getDecorationHolidayId(self):
        return self.decorationHolidayIds

    def getHolidayIdList(self):
        return self.holidayIdList

    def setBingoWin(self, zoneId):
        base.localAvatar.setSystemMessage(0, "Bingo congrats!")
        
    def setBingoStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoStart)
        
    def setBingoOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoOngoing)
        
    def setBingoEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.FishBingoEnd)
        
    def setCircuitRaceStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceStart)
        
    def setCircuitRaceOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceOngoing)
        
    def setCircuitRaceEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.CircuitRaceEnd)

    def setTrolleyHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayStart)
        
    def setTrolleyHolidayOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayOngoing)

    def setTrolleyHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyHolidayEnd)

    def setTrolleyWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyWeekendStart)

    def setTrolleyWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.TrolleyWeekendEnd)

    def setRoamingTrialerWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendStart)
        base.roamingTrialers = True
        
    def setRoamingTrialerWeekendOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendOngoing)
        base.roamingTrialers = True
        
    def setRoamingTrialerWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.RoamingTrialerWeekendEnd)        
        base.roamingTrialers = False

    def setMoreXpHolidayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayStart)
        
    def setMoreXpHolidayOngoing(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayOngoing)
        
    def setMoreXpHolidayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.MoreXpHolidayEnd)

    def setJellybeanDayStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanDayHolidayStart)

    def setJellybeanDayEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.JellybeanDayHolidayEnd)

    def setGrandPrixWeekendStart(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GrandPrixWeekendHolidayStart )

    def setGrandPrixWeekendEnd(self):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GrandPrixWeekendHolidayEnd)

    def setHydrantZeroHolidayStart(self):
        messenger.send("HydrantZeroIsRunning", [True])
        
        
    def holidayNotify(self):
        # this function is used to notify players just logging in of which Silly Saturday event is going
        for id in self.holidayIdList:
            if id == 19:
                self.setBingoOngoing()
            elif id == 20:
                self.setCircuitRaceOngoing()
            elif id == 21:
                self.setTrolleyHolidayOngoing()
            elif id == 22:
                self.setRoamingTrialerWeekendOngoing()

    def setWeeklyCalendarHolidays(self, weeklyCalendarHolidays):
        """Handle the AI server telling us which weekly holidays to display."""
        self.weeklyCalendarHolidays = weeklyCalendarHolidays

    def getHolidaysForWeekday(self, day):
        """Return a list of weekly holiday ids that match the given day of the week."""
        result = []
        for item in self.weeklyCalendarHolidays:
            if item[1] == day:
                result.append(item[0])
        return result

    def setYearlyCalendarHolidays(self, yearlyCalendarHolidays):
        """Handle the AI server telling us which yearly holidays to display."""
        self.yearlyCalendarHolidays = yearlyCalendarHolidays

    def getYearlyHolidaysForDate(self, theDate):
        """Return the yearly holidays which start or stop on the given date."""
        result = []
        for item in self.yearlyCalendarHolidays:
            if item[1][0] == theDate.month and item[1][1] == theDate.day:
                # holiday starts on this date
                newItem =  [self.YearlyHolidayType] + list(item) 
                result.append(tuple(newItem))
                continue
            if item[2][0] == theDate.month and item[2][1] == theDate.day:
                # holiday ends on this date
                newItem = [self.YearlyHolidayType] + list(item)  
                result.append(tuple(newItem))
        return result

    def setMultipleStartHolidays(self, multipleStartHolidays):
        """Handle the AI server telling us which oncely holidays to display."""
        # oncely differs from yearly holidays in that they have a fixed year
        #import pdb; pdb.set_trace()
        self.multipleStartHolidays = multipleStartHolidays

    def getMultipleStartHolidaysForDate(self, theDate):
        """Return the multiple start holidays which start or stop on the given date."""
        result = []
        for theHoliday in self.multipleStartHolidays:
            times = theHoliday[1:]
            tempTimes = times[0] # weird why it's we'd have to do this, investigate dc definition when we have time
            for startAndStopTimes in tempTimes:
                startTime = startAndStopTimes[0]
                endTime = startAndStopTimes[1]
                if startTime[0] == theDate.year and startTime[1] == theDate.month and \
                   startTime[2] == theDate.day:
                    # holiday starts on this date
                    # We fake the calendarGuiDay and say this is a oncely holiday
                    fakeOncelyHoliday = [theHoliday[0], startTime, endTime]
                    newItem = [self.OncelyMultipleStartHolidayType]+ fakeOncelyHoliday 
                    result.append(tuple(newItem))
                    continue
                if endTime[0] == theDate.year and endTime[1] == theDate.month and \
                    endTime[2] == theDate.day:
                     # holiday ends on this date
                     fakeOncelyHoliday = [theHoliday[0], startTime, endTime]
                     newItem =  [self.OncelyMultipleStartHolidayType] + fakeOncelyHoliday
                     result.append(tuple(newItem))
        return result        

    def setOncelyCalendarHolidays(self, oncelyCalendarHolidays):
        """Handle the AI server telling us which oncely holidays to display."""
        # oncely differs from yearly holidays in that they have a fixed year
        self.oncelyCalendarHolidays = oncelyCalendarHolidays
           

    def getOncelyHolidaysForDate(self, theDate):
        """Return the oncely holidays which start or stop on the given date."""
        result = []
        for item in self.oncelyCalendarHolidays:
            if item[1][0] == theDate.year and item[1][1] == theDate.month and \
               item[1][2] == theDate.day:
                # holiday starts on this date
                newItem = [self.OncelyHolidayType]+ list(item) 
                result.append(tuple(newItem))
                continue
            if item[2][0] == theDate.year and item[2][1] == theDate.month and \
               item[2][2] == theDate.day:
                # holiday ends on this date
                newItem =  [self.OncelyHolidayType] + list(item)
                result.append(tuple(newItem))
        return result
    
    def setRelativelyCalendarHolidays(self, relativelyCalendarHolidays):
        """Handle the AI server telling us which relatively holidays to display."""
        self.relativelyCalendarHolidays = relativelyCalendarHolidays

    def getRelativelyHolidaysForDate(self, theDate):
        """Return the relatively holidays which start or stop on the given date."""
        result = []
        self.weekDaysInMonth = []                       # A matrix of the number of times a weekday repeats in a month
        self.numDaysCorMatrix = [(28,0), (29, 1),
                            (30, 2), (31, 3)]           # A matrix of the number of weekdays that repeat one extra
                                                        # time based on the number of days in the month. For instance
                                                        # in a month with 31 days, the first two week days occur
                                                        # one more time than the other days.
        for i in range(7):                              # The minimum number of times a day repeats in a month
            self.weekDaysInMonth.append((i,4))
            
        for holidayItem in self.relativelyCalendarHolidays:
            item = deepcopy(holidayItem)
            newItem = []
            newItem.append(item[0])
            i = 1
            while(i<len(item)):
                sRepNum = item[i][1]
                sWeekday = item[i][2]
                eWeekday = item[i+1][2]
                while(1):
                    eRepNum = item[i+1][1]
                    self.initRepMatrix(theDate.year, item[i][0])
                    while(self.weekDaysInMonth[sWeekday][1] < sRepNum):
                        sRepNum -= 1
                    sDay = self.dayForWeekday(theDate.year, item[i][0], sWeekday, sRepNum)
                    
                    self.initRepMatrix(theDate.year, item[i+1][0])
                    while(self.weekDaysInMonth[eWeekday][1] < eRepNum):
                        eRepNum -= 1
                    nDay = self.dayForWeekday(theDate.year, item[i+1][0], eWeekday, eRepNum)
                    if(((nDay>sDay) and (item[i+1][0] == item[i][0]) \
                        and ((item[i+1][1] - item[i][1]) <= (nDay-sDay+abs(eWeekday-sWeekday))/7))
                        or (item[i+1][0] != item[i][0])):
                        break                    
                    
                    # Handles the case when the end weekday is less than the start
                    if(self.weekDaysInMonth[eWeekday][1] > eRepNum):
                        eRepNum += 1
                    else:
                        item[i+1][0] += 1
                        item[i+1][1] = 1
                newItem.append([item[i][0], sDay, item[i][3], item[i][4], item[i][5]])
                newItem.append([item[i+1][0], nDay, item[i+1][3], item[i+1][4], item[i+1][5]])
                i += 2
            if item[1][0] == theDate.month and \
                newItem[1][1] == theDate.day:
                # holiday starts on this date
                nItem = [self.RelativelyHolidayType]+ list(newItem)
                result.append(tuple(nItem))
                continue

            if item[2][0] == theDate.month and \
                newItem[2][1] == theDate.day:
                # holiday ends on this date
                nItem =  [self.RelativelyHolidayType] + list(newItem)
                result.append(tuple(nItem))
        return result
    
    ############################################################
    # Method: dayForWeekday(month, weekday, repNum)
    # Returns the day for a given weekday that has repeated
    # repNum times for that month
    ############################################################
    def dayForWeekday(self, year, month, weekday, repNum):
        monthDays = calendar.monthcalendar(year, month)
        if(monthDays[0][weekday] == 0):
            repNum += 1
        return monthDays[(repNum-1)][weekday]
    
    ############################################################
    # Method: initRepMatrix
    # Initialize the number of times weekdays get
    # repeated in a month method.
    ############################################################
    def initRepMatrix(self, year, month):

        for i in range(7):
            self.weekDaysInMonth[i] = (i,4)

        startingWeekDay, numDays = calendar.monthrange(year, month)
        if(startingWeekDay>6):
            import pdb;pdb.set_trace()

        for i in range(4):
            if(numDays == self.numDaysCorMatrix[i][0]):
                break

        for j in range(self.numDaysCorMatrix[i][1]):                                               # At this point we have a matrix of the weekdays and
            self.weekDaysInMonth[startingWeekDay] = (self.weekDaysInMonth[startingWeekDay][0],
                                                     self.weekDaysInMonth[startingWeekDay][1]+1)   # the number of times they repeat for the current month
            startingWeekDay = (startingWeekDay+1)%7

    def isHolidayRunning(self, holidayId):
        """Return True if a holiday is currently running."""
        # WARNING this will not properly handle holidays with delayed ends, like april fools
        # and vampire mickey
        result = holidayId in self.holidayIdList
        return result
        

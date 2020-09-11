"""CalendarGuiDay module: contains the CalendarGuiDay class"""
import datetime
import time
from pandac.PandaModules import TextNode, Vec3, Vec4, PlaneNode, Plane, \
     Point3
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton, \
     DirectScrolledList, DGG
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.parties.PartyInfo import PartyInfo
from toontown.parties import PartyGlobals
from toontown.ai.NewsManager import NewsManager
from toontown.toon import GMUtils

def myStrftime( myTime):
    """Return a better time string without the leading zero"""
    result = ""
    result = myTime.strftime("%I")
    if result[0] == '0':
        result = result[1:]
    result += myTime.strftime(":%M %p")
    return result

class CalendarGuiDay(DirectFrame):
    """A class to represent the gui for one day in the month.
    Do not put references to the shtiker page or book,  so this
    class may be extended later."""

    notify = directNotify.newCategory("CalendarGuiDay")
    ScrollListTextSize = 0.03
    
    def __init__(self, parent, myDate, startDate, dayClickCallback=None, onlyFutureDaysClickable=False):
        """Construct ourself."""
        self.origParent = parent
        self.startDate = startDate
        self.myDate = myDate
        self.dayClickCallback = dayClickCallback
        # If true, only allow clicks on days in the future
        self.onlyFutureDaysClickable = onlyFutureDaysClickable  
        DirectFrame.__init__(self, parent =parent)

        self.timedEvents = []
        self.partiesInvitedToToday = []
        self.hostedPartiesToday = []
        self.yearlyHolidaysToday = [] # either ending or starting today

        self.showMarkers = base.config.GetBool('show-calendar-markers',0)

        self.filter = ToontownGlobals.CalendarFilterShowAll
        
        self.load()
        # self.createDummyLocators()
        self.createGuiObjects()
        self.update()

    def createDummyLocators(self):
        """Put some programming locators until we get the real art assets."""
        self.dayButtonLocator = self.attachNewNode('dayButtonLocator')
        self.dayButtonLocator.setX(0.1)
        self.dayButtonLocator.setZ(-0.05)     
        self.numberLocator = self.attachNewNode('numberLocator')
        self.numberLocator.setX(0.09)
        self.scrollLocator = self.attachNewNode('scrollLocator')
        self.selectedLocator = self.attachNewNode('selectedLocator')
        self.selectedLocator.setX(0.11)
        self.selectedLocator.setZ(-0.06)

    def load(self):
        """Load the assets, and make sure locators are there."""
        dayAsset = loader.loadModel('phase_4/models/parties/tt_m_gui_sbk_calendar_box')
        dayAsset.reparentTo(self)
        self.dayButtonLocator = self.find('**/loc_origin')
        self.numberLocator = self.find('**/loc_number')
        self.scrollLocator = self.find('**/loc_topLeftList')
        self.selectedLocator = self.find('**/loc_origin')
        self.todayBox = self.find('**/boxToday')
        self.todayBox.hide()
        self.selectedFrame= self.find('**/boxHover')
        self.selectedFrame.hide()
        self.defaultBox = self.find('**/boxBlank')
        self.scrollBottomRightLocator = self.find('**/loc_bottomRightList')
        self.scrollDownLocator = self.find('**/loc_scrollDown')
        self.attachMarker(self.scrollDownLocator)
        
        self.scrollUpLocator = self.find('**/loc_scrollUp')
        self.attachMarker(self.scrollUpLocator)

    def attachMarker(self, parent, scale=0.005, color = (1,0,0)):
        """Attach a marker to the parent to aid in visual debugging."""
        if self.showMarkers:
            marker = loader.loadModel("phase_3/models/misc/sphere")
            marker.reparentTo(parent)
            marker.setScale(scale)
            marker.setColor(*color)        
 
    def createGuiObjects(self):
        """Create the other gui objects in the month, assumes we have proper locators."""
        # we create an invisible button so the day can be clicked on
        self.dayButton = DirectButton(
            parent = self.dayButtonLocator,
            image = self.selectedFrame,
            relief = None,
            command = self.__clickedOnDay,
            # next three settings are for debug
            pressEffect = 1,
            rolloverSound = None,
            clickSound = None
            )

        self.numberWidget =  DirectLabel(
            parent = self.numberLocator,
            relief = None,
            text = str(self.myDate.day),
            text_scale = 0.04,
            text_align = TextNode.ACenter,
            text_font = ToontownGlobals.getInterfaceFont(),
            text_fg = Vec4(110/255.0, 126/255.0, 255/255.0 ,1),
            )

        self.attachMarker(self.numberLocator)

        self.listXorigin = 0
        self.listFrameSizeX =self.scrollBottomRightLocator.getX() -  self.scrollLocator.getX()
        self.scrollHeight = self.scrollLocator.getZ() -  self.scrollBottomRightLocator.getZ() 
        self.listZorigin = self.scrollBottomRightLocator.getZ()
        self.listFrameSizeZ =self.scrollLocator.getZ() - self.scrollBottomRightLocator.getZ()  
        self.arrowButtonXScale = 1
        self.arrowButtonZScale = 1
        self.itemFrameXorigin = 0
        self.itemFrameZorigin = 0
        self.buttonXstart = self.itemFrameXorigin + 0.21
        self.gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        buttonOffSet = -0.01

        # these settings put the arrow buttons on the top
        incButtonPos = (0.0,0,0)
        decButtonPos = (0.0,0,0)

        # these settings put the arrow buttons on the right side
        # incButtonPos = (self.buttonXstart,0,self.listZorigin - buttonOffSet)
        # decButtonPos = (self.buttonXstart, 0, self.listZorigin + self.listFrameSizeZ + buttonOffSet)
        itemFrameMinZ = self.listZorigin
        itemFrameMaxZ = self.listZorigin + self.listFrameSizeZ
           
        arrowUp = self.find("**/downScroll_up")
        arrowDown = self.find("**/downScroll_down")
        arrowHover = self.find("**/downScroll_hover")
        
        self.scrollList = DirectScrolledList(
            parent = self.scrollLocator,
            relief = None,
            pos = (0,0,0),
            # inc and dec are DirectButtons
            # incButton is on the bottom of page, decButton is on the top!
            incButton_image = (arrowUp,
                               arrowDown,
                               arrowHover,
                               arrowUp,
                               ),
            incButton_relief = None,
            incButton_scale = (self.arrowButtonXScale,1,self.arrowButtonZScale),
            incButton_pos = incButtonPos,

            # Make the disabled button fade out
            incButton_image3_color = Vec4(1,1,1,0.2),
            decButton_image = (arrowUp,
                               arrowDown,
                               arrowHover,
                               arrowUp,
                               ),
            decButton_relief = None,
            decButton_scale = (self.arrowButtonXScale,1,-self.arrowButtonZScale),

            decButton_pos = decButtonPos,
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1,1,1,0.2),

            # itemFrame is a DirectFrame, shift it down a bit to match top left scroll
            itemFrame_pos = (self.itemFrameXorigin,0,-0.03),
           
            # each item is a button with text on it
            numItemsVisible = 4,
            
            # so we select the day when we click on a scroll button
            incButtonCallback = self.scrollButtonPressed,
            decButtonCallback = self.scrollButtonPressed,
            )
        # make sure the arrow buttons appear over item frame
        itemFrameParent = self.scrollList.itemFrame.getParent()
        self.scrollList.incButton.reparentTo(self.scrollDownLocator)
        self.scrollList.decButton.reparentTo(self.scrollUpLocator)

        arrowUp.removeNode()
        arrowDown.removeNode()
        arrowHover.removeNode()

        # Set up a clipping plane to truncate names that would extend
        # off the right end of the scrolled list.
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.23, 0, 0)))
        clipNP = self.scrollList.component('itemFrame').attachNewNode(clipper)
        self.scrollList.component('itemFrame').setClipPlane(clipNP)

    def scrollButtonPressed(self):
        """Select the current day when the scroll button is pressed."""
        self.__clickedOnDay()

    def adjustForMonth(self):
        """Darken us if we are not in the same month as startDate."""
        # make us glow if are equal to the serverDate
        curServerDate = base.cr.toontownTimeManager.getCurServerDateTime()
        
        if self.onlyFutureDaysClickable:
            if self.myDate.year < curServerDate.year or \
               ( self.myDate.year == curServerDate.year and self.myDate.month < curServerDate.month ) or \
               ( self.myDate.year == curServerDate.year and self.myDate.month == curServerDate.month and self.myDate.day < curServerDate.day ):
                self.numberWidget.setColorScale(0.5,0.5,0.5,0.5)
                self.numberWidget['state'] = DirectGuiGlobals.DISABLED
            else:
                self.numberWidget.setColorScale(1,1,1,1)
        if self.myDate.month != self.startDate.month:
            self.setColorScale(0.75, 0.75, 0.75, 1.0)
            if self.dayClickCallback is not None:
                self.numberWidget['state'] = DirectGuiGlobals.DISABLED
        else:
            self.setColorScale(1,1,1,1)
            
        if self.myDate.date() == curServerDate.date():
            self.defaultBox.hide()
            self.todayBox.show()
        else:
            self.defaultBox.show()
            self.todayBox.hide()
        
    def destroy( self ):
        if self.dayClickCallback is not None:
            self.numberWidget.destroy()
        self.dayClickCallback = None
        self.notify.debug('desroying %s' % self.myDate)
        try:
            for item in self.scrollList['items']:
                if hasattr(item, "description") and item.description and hasattr(item.description,'destroy'):
                    self.notify.debug('desroying description of item %s' % item)
                    item.unbind(DGG.ENTER)
                    item.unbind(DGG.EXIT)
                    item.description.destroy()
        except e:
            self.notify.debug('pass %s' % self.myDate)
            # an empty scroll list will come to this point
            pass
        self.scrollList.removeAndDestroyAllItems()

        self.scrollList.destroy()
        self.dayButton.destroy()
        DirectFrame.destroy( self )
                                       
    def addWeeklyHolidays(self):
        """Add weekly holidays to our scroll list."""
        if not (self.filter == ToontownGlobals.CalendarFilterShowAll or \
                self.filter == ToontownGlobals.CalendarFilterShowOnlyHolidays):            
            return
        if base.cr.newsManager:
            holidays = base.cr.newsManager.getHolidaysForWeekday(self.myDate.weekday())
            holidayName = ""
            holidayDesc = ""
            for holidayId in holidays:
                if holidayId in TTLocalizer.HolidayNamesInCalendar:
                    holidayName = TTLocalizer.HolidayNamesInCalendar[holidayId][0]
                    holidayDesc = TTLocalizer.HolidayNamesInCalendar[holidayId][1]
                else:
                    holidayName = TTLocalizer.UnknownHoliday % holidayId

                self.addTitleAndDescToScrollList(holidayName, holidayDesc)
            self.scrollList.refresh()

        if base.config.GetBool('calendar-test-items',0):
            # add test items just so we see scroll list arrows
            if self.myDate.date() + datetime.timedelta(days=-1) == base.cr.toontownTimeManager.getCurServerDateTime().date():
                testItems = ("1:00 AM Party", "2:00 AM CEO", "11:15 AM Party",
                             "5:30 PM CJ", "11:00 PM Party", "Really Really Long String")
                for text in testItems:
                    newItem = DirectLabel(
                        relief = None,
                        text = text,
                        text_scale = self.ScrollListTextSize,
                        text_align = TextNode.ALeft,)

                    self.scrollList.addItem(newItem)
            if self.myDate.date() + datetime.timedelta(days=-2) == base.cr.toontownTimeManager.getCurServerDateTime().date():
                testItems = ("1:00 AM Party", "3:00 AM CFO", "11:00 AM Party",)
                textSize = self.ScrollListTextSize
                for text in testItems:
                    newItem = DirectLabel(
                        relief = None,
                        text = text,
                        text_scale = textSize,
                        text_align = TextNode.ALeft,)

                    self.scrollList.addItem(newItem)
        

    def updateArrowButtons(self):
        """If we don't have anything in out scroll list, hide the arrow buttons."""
        numItems = 0
        try:
            numItems = len(self.scrollList['items'])
        except e:
            numItems = 0
        if numItems <= self.scrollList.numItemsVisible:
            self.scrollList.incButton.hide()
            self.scrollList.decButton.hide()
        else:
            self.scrollList.incButton.show()
            self.scrollList.decButton.show()            
    
    def collectTimedEvents(self):
        """Sort by time the events in my day."""
        # possible events would be yearly holidays,
        # oncely holidays and relatively holidays
        # parties
        # and in the future planned boss battle raids
        self.timedEvents = []
        if (self.filter == ToontownGlobals.CalendarFilterShowAll or \
            self.filter == ToontownGlobals.CalendarFilterShowOnlyParties):            
            for party in localAvatar.partiesInvitedTo:
                #if self.myDate.month == 9 and self.myDate.day == 1:
                #    import pdb; pdb.set_trace()
                if party.startTime.date() == self.myDate.date():
                    self.partiesInvitedToToday.append(party)
                    self.timedEvents.append((party.startTime.time(), party))
            for party in localAvatar.hostedParties:
                if party.startTime.date() == self.myDate.date():
                    self.hostedPartiesToday.append(party)
                    self.timedEvents.append((party.startTime.time(), party))
                
        if base.cr.newsManager and (self.filter == ToontownGlobals.CalendarFilterShowAll or \
                self.filter == ToontownGlobals.CalendarFilterShowOnlyHolidays): 
            yearlyHolidays = base.cr.newsManager.getYearlyHolidaysForDate(self.myDate)
            for holiday in yearlyHolidays:
                holidayId = holiday[1]
                holidayStart = holiday[2]
                holidayEnd = holiday[3]
                holidayType = holiday[0]
                if holidayStart[0] == self.myDate.month and \
                   holidayStart[1] == self.myDate.day:
                    myTime = datetime.time(holidayStart[2], holidayStart[3])
                elif holidayEnd[0] == self.myDate.month and \
                   holidayEnd[1] == self.myDate.day:
                    myTime = datetime.time(holidayEnd[2], holidayEnd[3])
                else:
                    self.notify.error('holiday is not today %s' % holiday)
                self.timedEvents.append((myTime, holiday))

            oncelyHolidays = base.cr.newsManager.getOncelyHolidaysForDate(self.myDate)
            for holiday in oncelyHolidays:
                holidayId = holiday[1]
                holidayStart = holiday[2]
                holidayEnd = holiday[3]
                holidayType = holiday[0]
                if holidayStart[0] == self.myDate.year and \
                   holidayStart[1] == self.myDate.month and \
                   holidayStart[2] == self.myDate.day:
                    myTime = datetime.time(holidayStart[3], holidayStart[4])
                elif holidayEnd[0] == self.myDate.year and \
                   holidayEnd[1] == self.myDate.month and \
                   holidayEnd[2] == self.myDate.day:
                    myTime = datetime.time(holidayEnd[3], holidayEnd[4])
                else:
                    self.notify.error('holiday is not today %s' % holiday)
                self.timedEvents.append((myTime, holiday))

            multipleStartHolidays = base.cr.newsManager.getMultipleStartHolidaysForDate(self.myDate)
            for holiday in multipleStartHolidays:
                holidayId = holiday[1]
                holidayStart = holiday[2]
                holidayEnd = holiday[3]
                holidayType = holiday[0]
                if holidayStart[0] == self.myDate.year and \
                   holidayStart[1] == self.myDate.month and \
                   holidayStart[2] == self.myDate.day:
                    myTime = datetime.time(holidayStart[3], holidayStart[4])
                elif holidayEnd[0] == self.myDate.year and \
                   holidayEnd[1] == self.myDate.month and \
                   holidayEnd[2] == self.myDate.day:
                    myTime = datetime.time(holidayEnd[3], holidayEnd[4])
                else:
                    self.notify.error('holiday is not today %s' % holiday)
                self.timedEvents.append((myTime, holiday))

            relativelyHolidays = base.cr.newsManager.getRelativelyHolidaysForDate(self.myDate)
            for holiday in relativelyHolidays:
                holidayId = holiday[1]
                holidayStart = holiday[2]
                holidayEnd = holiday[3]
                holidayType = holiday[0]
                if holidayStart[0] == self.myDate.month and \
                   holidayStart[1] == self.myDate.day:
                    myTime = datetime.time(holidayStart[2], holidayStart[3])
                elif holidayEnd[0] == self.myDate.month and \
                   holidayEnd[1] == self.myDate.day:
                    myTime = datetime.time(holidayEnd[2], holidayEnd[3])
                else:
                    self.notify.error('holiday is not today %s' % holiday)
                self.timedEvents.append((myTime, holiday))

        # sort timedEvents
        def timedEventCompare(te1, te2):
            if te1[0] < te2[0]:
                return -1
            elif te1[0] == te2[0]:
                return 0
            else:
                return 1
        self.timedEvents.sort( cmp = timedEventCompare)

        # now add them to the scroll list
        for timedEvent in self.timedEvents:
            if isinstance(timedEvent[1], PartyInfo):
                self.addPartyToScrollList(timedEvent[1])
            elif isinstance(timedEvent[1], tuple) and timedEvent[1][0] == NewsManager.YearlyHolidayType:
                self.addYearlyHolidayToScrollList(timedEvent[1])
            elif isinstance(timedEvent[1], tuple) and timedEvent[1][0] == NewsManager.OncelyHolidayType:
                self.addOncelyHolidayToScrollList(timedEvent[1])
            elif isinstance(timedEvent[1], tuple) and timedEvent[1][0] == NewsManager.OncelyMultipleStartHolidayType:
                self.addOncelyMultipleStartHolidayToScrollList(timedEvent[1])
            elif isinstance(timedEvent[1], tuple) and timedEvent[1][0] == NewsManager.RelativelyHolidayType:
                self.addRelativelyHolidayToScrollList(timedEvent[1])


        
    def addYearlyHolidayToScrollList(self, holiday):
        """Add a yearly holiday to the scroll list. Could be start date or end date"""
        # first figure out if it ends on the same day
        holidayId = holiday[1]
        holidayStart = holiday[2]
        holidayEnd = holiday[3]
        holidayType = holiday[0]
        holidayText = ""
        startTime = datetime.time(holidayStart[2], holidayStart[3])
        endTime =  datetime.time(holidayEnd[2], holidayEnd[3])
        startDate = datetime.date( self.myDate.year, holidayStart[0], holidayStart[1])
        endDate = datetime.date( self.myDate.year,holidayEnd[0], holidayEnd[1])
        if endDate < startDate:
            endDate = datetime.date(endDate.year+1, endDate.month, endDate.day)
        if holidayId in TTLocalizer.HolidayNamesInCalendar:
            holidayName = TTLocalizer.HolidayNamesInCalendar[holidayId][0]
            holidayDesc = TTLocalizer.HolidayNamesInCalendar[holidayId][1]
        else:
            holidayName = TTLocalizer.UnknownHoliday % holidayId
            holidayDesc = TTLocalizer.UnknownHoliday % holidayId
        
        if holidayStart[0] == holidayEnd[0] and \
           holidayStart[1] == holidayEnd[1]:
            # end of holiday is on the same day
            holidayText = myStrftime(startTime)
            holidayText += " " + holidayName
            holidayDesc += " " + TTLocalizer.CalendarEndsAt  + myStrftime(endTime) 
        elif self.myDate.month == holidayStart[0] and \
             self.myDate.day == holidayStart[1]:
            holidayText = myStrftime(startTime) 
            holidayText += " " + holidayName
            holidayDesc = holidayName + ". " + holidayDesc
            holidayDesc += " " + TTLocalizer.CalendarEndsAt + endDate.strftime(TTLocalizer.HolidayFormat) + myStrftime(endTime)
        elif self.myDate.month == holidayEnd[0] and \
             self.myDate.day == holidayEnd[1]:
            holidayText = myStrftime(endTime) 
            holidayText += " " + TTLocalizer.CalendarEndDash + holidayName
            holidayDesc = TTLocalizer.CalendarEndOf + holidayName
            holidayDesc += ". " + TTLocalizer.CalendarStartedOn + startDate.strftime(TTLocalizer.HolidayFormat) + myStrftime(startTime) 

        else:
            self.notify.error('unhandled case')

        self.addTitleAndDescToScrollList(holidayText, holidayDesc)

    def addOncelyHolidayToScrollList(self, holiday):
        """Add a oncely holiday to the scroll list. Could be start date or end date"""
        # first figure out if it ends on the same day
        holidayId = holiday[1]
        holidayStart = holiday[2]
        holidayEnd = holiday[3]
        holidayType = holiday[0]
        holidayText = ""
        startTime = datetime.time(holidayStart[3], holidayStart[4])
        endTime =  datetime.time(holidayEnd[3], holidayEnd[4])
        startDate = datetime.date( holidayStart[0], holidayStart[1], holidayStart[2])
        endDate = datetime.date( holidayStart[0], holidayEnd[1], holidayEnd[2])
        if endDate < startDate:
            endDate = datetime.date(endDate.year+1, endDate.month, endDate.day)
        if holidayId in TTLocalizer.HolidayNamesInCalendar:
            holidayName = TTLocalizer.HolidayNamesInCalendar[holidayId][0]
            holidayDesc = TTLocalizer.HolidayNamesInCalendar[holidayId][1]
        else:
            holidayName = TTLocalizer.UnknownHoliday % holidayId
            holidayDesc = ""
        
        if holidayStart[1] == holidayEnd[1] and \
           holidayStart[2] == holidayEnd[2]:
            # end of holiday is on the same day
            holidayText = myStrftime(startTime) 
            holidayText += " " + holidayName
            holidayDesc = holidayName + ". " + holidayDesc
            holidayDesc += " " + TTLocalizer.CalendarEndsAt  + myStrftime(endTime)
        elif self.myDate.year == holidayStart[0] and \
             self.myDate.month == holidayStart[1] and \
             self.myDate.day == holidayStart[2]:
            holidayText = myStrftime(startTime) 
            holidayText += " " + holidayName
            holidayDesc = holidayName + ". " + holidayDesc
            holidayDesc += " " + TTLocalizer.CalendarEndsAt + endDate.strftime(TTLocalizer.HolidayFormat) + myStrftime(endTime)
        elif self.myDate.year == holidayEnd[0] and \
             self.myDate.month == holidayEnd[1] and \
             self.myDate.day == holidayEnd[2]:
            holidayText = myStrftime(endTime) 
            holidayText += " " + TTLocalizer.CalendarEndDash + holidayName
            holidayDesc = TTLocalizer.CalendarEndOf + holidayName
            holidayDesc += ". " + TTLocalizer.CalendarStartedOn + startDate.strftime(TTLocalizer.HolidayFormat) + myStrftime(startTime)

        else:
            self.notify.error('unhandled case')

        self.addTitleAndDescToScrollList(holidayText, holidayDesc)

    def addOncelyMultipleStartHolidayToScrollList(self, holiday):
        """Add a multiple start holiday to the scroll list. Could be start date or end date"""
        # I can't think of anything different we'd do from addOncely, so just call that
        self.addOncelyHolidayToScrollList(holiday)
        
        
    def addRelativelyHolidayToScrollList(self, holiday):
        """Add a relatively holiday to the scroll list. Could be start date or end date"""
        # first figure out if it ends on the same day
        holidayId = holiday[1]
        holidayStart = holiday[2]
        holidayEnd = holiday[3]
        holidayType = holiday[0]
        holidayText = ""
        startTime = datetime.time(holidayStart[2], holidayStart[3])
        endTime =  datetime.time(holidayEnd[2], holidayEnd[3])
        startDate = datetime.date( self.myDate.year, holidayStart[0], holidayStart[1])
        endDate = datetime.date( self.myDate.year,holidayEnd[0], holidayEnd[1])
        if endDate < startDate:
            endDate.year +=1
        if holidayId in TTLocalizer.HolidayNamesInCalendar:
            holidayName = TTLocalizer.HolidayNamesInCalendar[holidayId][0]
            holidayDesc = TTLocalizer.HolidayNamesInCalendar[holidayId][1]
        else:
            holidayName = TTLocalizer.UnknownHoliday % holidayId
            holidayDesc = ""

        if holidayStart[0] == holidayEnd[0] and \
           holidayStart[1] == holidayEnd[1]:
            # end of holiday is on the same day
            holidayText = myStrftime(startTime)
            holidayText += " " + holidayName
            holidayDesc += " " + TTLocalizer.CalendarEndsAt  + myStrftime(endTime)
        elif self.myDate.month == holidayStart[0] and \
             self.myDate.day == holidayStart[1]:
            holidayText = myStrftime(startTime)
            holidayText += " " + holidayName
            holidayDesc = holidayName + ". " + holidayDesc
            holidayDesc += " " + TTLocalizer.CalendarEndsAt + endDate.strftime(TTLocalizer.HolidayFormat) + myStrftime(endTime)
        elif self.myDate.month == holidayEnd[0] and \
             self.myDate.day == holidayEnd[1]:
            holidayText = myStrftime(endTime)
            holidayText += " " + TTLocalizer.CalendarEndDash + holidayName
            holidayDesc = TTLocalizer.CalendarEndOf + holidayName
            holidayDesc += ". " + TTLocalizer.CalendarStartedOn + startDate.strftime(TTLocalizer.HolidayFormat) + myStrftime(startTime)

        else:
            self.notify.error('unhandled case')

        self.addTitleAndDescToScrollList(holidayText, holidayDesc)
            
        
    def addTitleAndDescToScrollList(self, title, desc):
        """Add a text title and popup description to the scrollList."""
        textSize = self.ScrollListTextSize
        descTextSize = 0.05
        newItem = DirectButton(
            relief = None,
            text = title,
            text_scale = textSize,
            text_align = TextNode.ALeft,
            rolloverSound = None,
            clickSound = None,
            pressEffect = 0,
            command = self.__clickedOnScrollItem,
            )

        # lower tool tip a little
        scrollItemHeight = newItem.getHeight()

        descUnderItemZAdjust = (scrollItemHeight * descTextSize/textSize)
        descUnderItemZAdjust = max( 0.0534, descUnderItemZAdjust) # ensure minimum height
        descUnderItemZAdjust = -descUnderItemZAdjust
        # self.notify.debug('scrollItemHeight of %s = %f' % (title, scrollItemHeight))
        descZAdjust = descUnderItemZAdjust
        # self.notify.debug('descUnderItemZAdjust of %s = %f' % (title, descUnderItemZAdjust))

        newItem.description = DirectLabel(
            parent = newItem,
            pos = (0.115, 0, descZAdjust),
            text = '',
            text_wordwrap = 15,
            pad= (0.02,0.02),
            text_scale = descTextSize,
            text_align = TextNode.ACenter,
            textMayChange = 0,
            )
        # if we set text here, it really slows down changing the month
        # do it when we first enter the scroll item instead
        newItem.description.checkedHeight = False
        
        # # workaround to stop getting clipped by plane node
        newItem.description.setBin('gui-popup', 0)
        newItem.description.hide()

        newItem.bind(DGG.ENTER, self.enteredTextItem, extraArgs = [ newItem,desc, descUnderItemZAdjust])
        newItem.bind(DGG.EXIT, self.exitedTextItem, extraArgs = [newItem])

        self.scrollList.addItem(newItem)

    def exitedTextItem(self, newItem, mousepos):
        newItem.description.hide()

    def enteredTextItem(self, newItem, descText, descUnderItemZAdjust, mousePos):
        # compute if we go over edge, then adjust if needed
        if not newItem.description.checkedHeight:
            newItem.description.checkedHeight = True

            newItem.description['text'] = descText
            bounds = newItem.description.getBounds()
            descHeight = newItem.description.getHeight()
            # lets see if we go down too far
            scrollItemHeight = newItem.getHeight()
            descOverItemZAdjust = descHeight - (scrollItemHeight / 2.0)
            descZPos = self.getPos(aspect2d)[2] + descUnderItemZAdjust -descHeight
            if descZPos < -1.0:
                newItem.description.setZ(descOverItemZAdjust)

            descWidth = newItem.description.getWidth()
            brightFrame = loader.loadModel('phase_4/models/parties/tt_m_gui_sbk_calendar_popUp_bg')
            newItem.description['geom']=brightFrame
            newItem.description['geom_scale'] = (descWidth , 1, descHeight)

            descGeomZ = (bounds[2] - bounds[3]) / 2.0
            descGeomZ += bounds[3]
            # self.notify.debug('descGeomZ=%s' % descGeomZ)
            newItem.description['geom_pos'] = (0 , 0, descGeomZ)
            # self.notify.debug('descWidth=%s descHeight=%s' % (descWidth, descHeight))

        newItem.description.show()

    def addPartyToScrollList(self, party):
        """Add a party to the scroll list."""
        textSize = self.ScrollListTextSize
        descTextSize = 0.05
        partyTitle = myStrftime(party.startTime)
        partyTitle = partyTitle + " " + TTLocalizer.EventsPageCalendarTabParty

        textSize = self.ScrollListTextSize
        descTextSize = 0.05
        newItem = DirectButton(
            relief = None,
            text = partyTitle,
            text_scale = textSize,
            text_align = TextNode.ALeft,
            rolloverSound = None,
            clickSound = None,
            pressEffect = 0,
            command = self.__clickedOnScrollItem,
        )

        # lower tool tip a little
        scrollItemHeight = newItem.getHeight()

        descUnderItemZAdjust = (scrollItemHeight * descTextSize/textSize)
        descUnderItemZAdjust = max( 0.0534, descUnderItemZAdjust) # ensure minimum height
        descUnderItemZAdjust = -descUnderItemZAdjust
        # self.notify.debug('scrollItemHeight of %s = %f' % (title, scrollItemHeight))
        descZAdjust = descUnderItemZAdjust
        # self.notify.debug('descUnderItemZAdjust of %s = %f' % (title, descUnderItemZAdjust))
        self.scrollList.addItem(newItem)
        
        newItem.description = MiniInviteVisual(newItem, party)
        # # workaround to stop getting clipped by plane node
        newItem.description.setBin('gui-popup', 0)
        newItem.description.hide()

        newItem.bind(DGG.ENTER, self.enteredTextItem, extraArgs = [ newItem, newItem.description, descUnderItemZAdjust])
        newItem.bind(DGG.EXIT, self.exitedTextItem, extraArgs = [newItem])

        

    def __clickedOnScrollItem(self):
        """Handle the user clicking on a scroll item."""
        self.__clickedOnDay()

    def __clickedOnDay(self):
        """Handle user clicking on us a day square."""
        acceptClick = True
        if self.onlyFutureDaysClickable:
            curServerDate = base.cr.toontownTimeManager.getCurServerDateTime()
            if self.myDate.date() < curServerDate.date():
                acceptClick = False

        if not acceptClick:
            return
            
        if self.dayClickCallback:
            self.dayClickCallback(self)
        self.notify.debug('we got clicked on %s' % self.myDate.date())
        
        # tell the calendarGuiMonth
        messenger.send('clickedOnDay',  [self.myDate.date()])

    def updateSelected(self, selected):
        # note set multiplier to 1.0 if we don't want to pop selected days
        multiplier = 1.1
        if selected:
            self.selectedFrame.show()
            self.setScale(multiplier)
            self.setPos( -0.01,0,0.01)
            grandParent = self.origParent.getParent()
            self.origParent.reparentTo(grandParent)
        else:
            self.selectedFrame.hide()
            self.setScale(1.0)
            self.setPos(0,0,0)

    def changeDate(self, startDate, myDate):
        """Change the date that we are displaying."""
        self.startDate = startDate
        self.myDate = myDate   
        self.scrollList.removeAndDestroyAllItems()
        self.update()

    def update(self):
        """Fill in the day with the proper contents."""
        self.numberWidget['text']  = str(self.myDate.day)
        self.adjustForMonth()
        self.addWeeklyHolidays()
        self.collectTimedEvents()
        self.updateArrowButtons()

    def changeFilter(self, filter):
        """Change our fliter, update scroll items if needed."""
        oldFilter = self.filter
        self.filter = filter
        if self.filter != oldFilter:
            self.scrollList.removeAndDestroyAllItems()
            self.update()
            

class MiniInviteVisual(DirectFrame):
    
    def __init__(self, parent, partyInfo):
        DirectFrame.__init__(self, parent, pos = (0.1,0,-0.018))
        self.checkedHeight = True # Hack... we don't have height
        self.partyInfo = partyInfo
        self.parent = parent
        self.inviteBackgrounds = loader.loadModel("phase_4/models/parties/partyStickerbook")
        backgrounds = ["calendar_popup_birthday", "calendar_popup_fun", "calendar_popup_cupcake", "tt_t_gui_sbk_calendar_popup_racing", "tt_t_gui_sbk_calendar_popup_valentine1", "tt_t_gui_sbk_calendar_popup_victoryParty"]            
        self.background = DirectFrame(
            parent = self,
            relief = None,
            geom = self.inviteBackgrounds.find("**/%s"%backgrounds[self.partyInfo.inviteTheme]),
            scale = (0.7, 1.0, 0.23),
            pos = (0.0, 0.0, -0.1),
        )
        self.whosePartyLabel = DirectLabel(
            parent = self,
            relief = None,
            pos = (0.07, 0.0, -0.04),
            text=" ",
            text_scale = 0.04,
            text_wordwrap = 8,
            textMayChange=True,
        )
        self.whenTextLabel = DirectLabel(
            parent = self,
            relief = None,
            text = " ",
            pos = (0.07, 0.0, -0.13),
            text_scale = 0.04,
            textMayChange=True,
        )
        self.partyStatusLabel = DirectLabel(
            parent = self,
            relief = None,
            text = " ",
            pos = (0.07, 0.0, -0.175),
            text_scale = 0.04,
            textMayChange=True,
        )

    def show(self):
        # we do this weirdness so it doesn't get clipped by the PlaneNode
        self.reparentTo(self.parent)
        self.setPos(0.1,0,-0.018)
        newParent = self.parent.getParent().getParent()
        self.wrtReparentTo(newParent)
        if self.whosePartyLabel["text"] == " ":
            host = base.cr.identifyAvatar(self.partyInfo.hostId)
            if host:
                name = host.getName()
                if GMUtils.testGMIdentity(name):
                    name = GMUtils.handleGMName(name)
                self.whosePartyLabel["text"] = name
        if self.whenTextLabel["text"] == " ":
            time = myStrftime(self.partyInfo.startTime) 
            self.whenTextLabel["text"] = time
        if self.partyStatusLabel["text"] == " ":
            if self.partyInfo.status == PartyGlobals.PartyStatus.Cancelled:
                self.partyStatusLabel["text"] = TTLocalizer.CalendarPartyCancelled
            elif self.partyInfo.status == PartyGlobals.PartyStatus.Finished:
                self.partyStatusLabel["text"] = TTLocalizer.CalendarPartyFinished
            elif self.partyInfo.status == PartyGlobals.PartyStatus.Started:
                self.partyStatusLabel["text"] = TTLocalizer.CalendarPartyGo
            elif self.partyInfo.status == PartyGlobals.PartyStatus.NeverStarted:
                self.partyStatusLabel["text"] = TTLocalizer.CalendarPartyNeverStarted
            else:
                self.partyStatusLabel["text"] = TTLocalizer.CalendarPartyGetReady
        DirectFrame.show(self)

    def destroy(self):
        del self.checkedHeight
        del self.partyInfo
        del self.parent
        del self.background
        del self.whosePartyLabel
        del self.whenTextLabel
        del self.partyStatusLabel
        DirectFrame.destroy(self)


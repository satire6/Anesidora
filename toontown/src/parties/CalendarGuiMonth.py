"""CalendarGuiMonth module: contains the CalendarGuiMonth class"""
import calendar
from datetime import timedelta, datetime
from pandac.PandaModules import Vec4, TextNode
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton, DirectScrolledList, DGG
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.parties.CalendarGuiDay import CalendarGuiDay

class CalendarGuiMonth(DirectFrame):
    """A class to represent the gui for one month.
    Do not put references to the shtiker page or book,  so this
    class may be extended later."""

    notify = directNotify.newCategory("CalendarGuiMonth")

    def __init__(self, parent, startingDateTime, scale=1.0, pos = (0, 0, -0.1),
                 dayClickCallback=None, onlyFutureDaysClickable=False):
        """Construct ourself."""
        self.startDate = startingDateTime
        self.curDate = startingDateTime
        self.dayClickCallback = dayClickCallback
        self.onlyFutureDaysClickable = onlyFutureDaysClickable
        # sticker book is shifted up by 0.1, so default pos counteracts that
        # as the gui was made assuming 0,0 is center of the screen
        DirectFrame.__init__(self, parent=parent, scale=scale, pos = pos)

        # for debugging, show red dots for locators
        self.showMarkers = base.config.GetBool('show-calendar-markers',0)
        
        # WARNING debug only, remove this or else we leak
        # base.cgm = self

        # self.createDummyLocators()
        self.load()
        self.createGuiObjects()
        self.lastSelectedDate = None
        self.accept('clickedOnDay', self.clickedOnDay)
        

    def createDummyLocators(self):
        """Put some programming locators until we get the real art assets."""
        self.monthLocator = self.attachNewNode('monthLocator')
        self.monthLocator.setZ(0.6)

        self.weekDayLocators = []
        for i in xrange(7):
            self.weekDayLocators.append( self.attachNewNode('weekDayLocator-%d'%i))
            self.weekDayLocators[i].setZ(0.5)
            self.weekDayLocators[i].setX( i*(0.24) + -0.75)

        dayTopLeftX = -0.8
        dayTopLeftZ = 0.4
        self.dayLocators =[]        
        for row in xrange(6):
            oneWeek = []
            for col in xrange(7):
                newDayLoc = self.attachNewNode('dayLocator-row-%d-col-%d' %
                                               (row,col))
                newDayLoc.setX( col *0.24 + dayTopLeftX)
                newDayLoc.setZ( row * -0.18 + dayTopLeftZ)
                oneWeek.append(newDayLoc)
            self.dayLocators.append(oneWeek)

        self.monthLeftLocator = self.attachNewNode('monthLeft')
        self.monthLeftLocator.setPos(-0.3, 0,0.65)

        self.monthRightLocator = self.attachNewNode('monthRight')
        self.monthRightLocator.setPos(0.3, 0, 0.65)

    def attachMarker(self, parent, scale=0.01, color = (1,0,0)):
        """Attach a marker to the parent to aid in visual debugging."""
        if self.showMarkers:
            marker = loader.loadModel("phase_3/models/misc/sphere")
            marker.reparentTo(parent)
            marker.setScale(scale)
            marker.setColor(*color)                     

    def load(self):
        """Load our assets, make sure we have correct locators."""
        monthAsset = loader.loadModel('phase_4/models/parties/tt_m_gui_sbk_calendar')
        monthAsset.reparentTo(self)
        self.monthLocator = self.find('**/locator_month/locator_month')
        self.attachMarker(self.monthLocator)
        
        self.weekDayLocators = []
        for weekday in ('sun','mon','tue','wed','thu','fri','sat'):        
            weekDayLoc = self.find('**/loc_%s' % weekday)
            self.weekDayLocators.append(weekDayLoc)
            self.attachMarker(weekDayLoc)

        self.dayLocators =[]        
        for row in xrange(6):
            oneWeek = []
            for col in xrange(7):
                newDayLoc = self.find('**/loc_box_%s_%s' % (row, col))
                oneWeek.append(newDayLoc)
            self.dayLocators.append(oneWeek)

        
        self.monthLeftLocator = self.find('**/locator_month_arrowL')
        self.monthRightLocator = self.find('**/locator_month_arrowR')

        self.filterLocator = self.find('**/locator_filter')
        self.filterLocatorArrowUp = self.find('**/locator_filter_arrowTop')
        self.filterLocatorArrowDown = self.find('**/locator_filter_arrowBottom')

        self.yearLocator = self.attachNewNode("yearLocator")
        self.yearLocator.setPos(self.monthLocator, 0,0,-0.03)
        
    def createGuiObjects(self):
        """Create the other gui objects in the month, assumes we have proper locators."""
        self.monthLabel =  DirectLabel(
            parent = self.monthLocator,
            relief = None,
            text = TTLocalizer.Months[self.startDate.month],
            text_scale = 0.075,
            text_font = ToontownGlobals.getMinnieFont(),
            text_fg = (40/255.0, 140/255.0, 246/255.0, 1.0),
            )
        self.yearLabel =  DirectLabel(
            parent = self.yearLocator,
            relief = None,
            text = str(self.startDate.year),
            text_scale = 0.03,
            text_font = ToontownGlobals.getMinnieFont(),
            #text_fg = (40/255.0, 140/255.0, 246/255.0, 1.0),
            text_fg = (140/255.0, 140/255.0, 246/255.0, 1.0),
            )

        self.weekdayLabels = []
        for posIndex in xrange(7):
            # Sunday is the usual first day of the week, but
            # self.startDate.weekDay() reports 0 for Monday
            adjustedNameIndex = (posIndex-1) % 7
            self.weekdayLabels.append( DirectLabel(
                parent = self.weekDayLocators[posIndex],
                relief = None,
                text = TTLocalizer.DayNamesAbbrev[adjustedNameIndex],
                text_font = ToontownGlobals.getInterfaceFont(),
                text_fg = (255/255.0, 146/255.0, 113/255.0, 1.0),
                text_scale = 0.05))
        self.createGuiDays()

        arrowUp = self.find("**/month_arrowR_up")
        arrowDown = self.find("**/month_arrowR_down")
        arrowHover = self.find("**/month_arrowR_hover")
        self.monthLeftArrow = DirectButton(
            parent = self.monthLeftLocator,
            relief = None,
            image = (arrowUp,
                     arrowDown,
                     arrowHover,
                     arrowUp,
                     ),            
            # make the disabled color more transparent
            image3_color = Vec4(1, 1, 1, 0.5),
            scale = (-1.0, 1.0, 1.0),  # make the arrow point left
            #pos = (0.25, 0, buttonbase_ycoord - textRowHeight * 4),
            command = self.__doMonthLeft,
            )
        if self.onlyFutureDaysClickable:
            self.monthLeftArrow.hide()
        self.monthRightArrow = DirectButton(
            parent = self.monthRightLocator,
            relief = None,
            image = (arrowUp,
                     arrowDown,
                     arrowHover,
                     arrowUp,
                     ),                
            # make the disabled color more transparent
            image3_color = Vec4(1, 1, 1, 0.5),
            #pos = (0.65, 0, buttonbase_ycoord - textRowHeight * 4),
            command = self.__doMonthRight,
            )
        

        def makeLabel(itemName, itemNum, *extraArgs):
           
            return DirectLabel(text = itemName,
                               frameColor = (0,0,0,0),
                               #scale = 0.1,
                                #relief = DGG.RAISED,
                                #frameSize = (-3.5, 3.5, -0.2, 0.8),
                                text_scale = 0.04)

        gui = loader.loadModel('phase_4/models/parties/tt_m_gui_sbk_calendar_box')
        arrowUp = gui.find("**/downScroll_up")
        arrowDown = gui.find("**/downScroll_down")
        arrowHover = gui.find("**/downScroll_hover")

        filterLocatorUpPos = self.filterLocatorArrowUp.getPos(self.filterLocator)
        filterLocatorDownPos = self.filterLocatorArrowDown.getPos(self.filterLocator)
        self.filterList = DirectScrolledList(
            parent = self.filterLocator,
            relief = None,
            pos = (0,0,0), #(0.65, 0, 0.7),
            image = None, #DGG.getDefaultDialogGeom(),
            text_scale = 0.025,            
            incButton_image = (arrowUp,
                               arrowDown,
                               arrowHover,
                               arrowUp,
                               ),            
            incButton_relief = None,
            incButton_pos = filterLocatorDownPos, #(0.0, 0.0, -0.035),
            # Make the disabled button fade out
            incButton_image3_color = Vec4(1,1,1,0.2),
            incButtonCallback = self.filterChanged,
            # Same for the decrement button
            decButton_image = (arrowUp,
                               arrowDown,
                               arrowHover,
                               arrowUp,
                               ),  
            decButton_relief = None,
            decButton_pos = filterLocatorUpPos, #(0.0, 0.0, 0.07),
            decButton_scale = (1,1,-1),
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1,1,1,0.2),
            decButtonCallback = self.filterChanged,
            # each item is a button with text on it
            numItemsVisible = 1,
            itemMakeFunction = makeLabel,
            # note ordering is very important, should match ToontownGlobals
            items = [TTLocalizer.CalendarShowAll, TTLocalizer.CalendarShowOnlyHolidays, TTLocalizer.CalendarShowOnlyParties,],
            # itemFrame is a DirectFrame
            itemFrame_frameSize = (-.2, .2, -.02, .05),
            itemFrame_frameColor = (0,0,0,0),
            )
        gui.removeNode()
        

    def getTopLeftDate(self):
        """Return the top left date. Will probably be a date in the previous month."""
        # for the current month figure out how many days
        # we subtract to get to Sunday
        firstOfTheMonth = self.curDate.replace(day=1)
        daysAwayFromSunday = (firstOfTheMonth.weekday() -6) % 7        
        topLeftDate = firstOfTheMonth + timedelta(days = -daysAwayFromSunday)
        return topLeftDate

    def createGuiDays(self):
        """Create the day guis for the whole month."""
        topLeftDate = self.getTopLeftDate()
        curDate = topLeftDate
        self.guiDays = []
        for row in self.dayLocators:
            for oneLocator in row:
                self.guiDays.append(
                    CalendarGuiDay(oneLocator, curDate, self.curDate, self.dayClickCallback, self.onlyFutureDaysClickable)
                )
                curDate += timedelta(days = 1)

    def changeDateForGuiDays(self):
        """Change the date for all our gui days.

        This should be much faster then our current tearing down and loading up again.
        """
        topLeftDate = self.getTopLeftDate()
        guiDayDate = topLeftDate
        for guiDay in self.guiDays:
            guiDay.changeDate(self.curDate, guiDayDate)
            guiDayDate += timedelta(days = 1)
                
    def changeMonth(self, monthChange):
        """Change the month we are displaying."""
        # monthChange should be able to handle bigger values now
        if monthChange != 0:
            # if it's March 1, make sure we dont skip February going back 31 days
            newMonth = self.curDate.month + monthChange
            newYear = self.curDate.year
            # make sure we have a valid month 1..12
            while newMonth > 12:
                newYear += 1
                newMonth -= 12
            while newMonth < 1:
                if newYear - 1 > 1899:
                    newMonth += 12
                    newYear -= 1
                else:
                    newMonth += 1
            self.curDate = datetime(
                newYear, newMonth, 1,
                self.curDate.time().hour, self.curDate.time().minute, self.curDate.time().second,
                self.curDate.time().microsecond, self.curDate.tzinfo)
                
        self.monthLabel['text'] = TTLocalizer.Months[self.curDate.month],
        self.yearLabel['text'] = str(self.curDate.year),
        startTime = globalClock.getRealTime()
        self.changeDateForGuiDays()
        endTime = globalClock.getRealTime()
        self.notify.debug('changeDate took %f seconds' % (endTime - startTime))
        # if we have a selected date, it probably changed box        
        self.updateSelectedDate()
        if self.onlyFutureDaysClickable and (newMonth == self.startDate.month and newYear == self.startDate.year):
            self.monthLeftArrow.hide()
    
    def __doMonthLeft(self):
        """Handle left month arrrow being pressed."""
        self.changeMonth(-1)

    def __doMonthRight(self):
        """Handle right month arrow being pressed."""
        self.monthLeftArrow.show()
        self.changeMonth(1)
        
    def destroy(self):
        """Clean ourself up."""
        self.ignoreAll()
        # these 2 lines get rid of party planner leaks
        self.dayClickCallback = None
        self.monthLeftArrow.destroy()
        self.monthRightArrow.destroy()
        for day in self.guiDays:
            if day is not None:
                day.destroy()
            day = None
        self.filterList.destroy()
        DirectFrame.destroy(self)
    
    def clickedOnDay(self, dayDate):
        """Handle one of our child day squares getting clicked on."""
        self.lastSelectedDate = dayDate
        self.updateSelectedDate()

    def updateSelectedDate(self):
        if self.lastSelectedDate:
            for oneGuiDay in self.guiDays:
                if oneGuiDay.myDate.date() == self.lastSelectedDate:
                    oneGuiDay.updateSelected(True)
                else:
                    oneGuiDay.updateSelected(False)

    def clearSelectedDay(self):
        for oneGuiDay in self.guiDays:
            oneGuiDay.updateSelected(False)

    def filterChanged(self):
        """Refresh our days since the filter has changed."""
        newFilter = self.filterList.getSelectedIndex()
        for guiDay in self.guiDays:
            guiDay.changeFilter(newFilter)

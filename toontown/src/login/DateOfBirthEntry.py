
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

class DateOfBirthEntry(DirectFrame):
    def __init__(self, showDay=1,
                 firstYear=1900, defaultAge=10, curYear=None,
                 monthHandler=None, yearHandler=None, dayHandler=None,
                 dateObject=None, parent=aspect2d, **kw):
        if dateObject:
            self.dateObject=dateObject
        else:
            self.dateObject=base.cr.dateObject

        self.showDay = showDay
        self.firstYear = firstYear
        self.defaultAge = defaultAge
        # we'll set the user handlers after we've set everything up
        self.setMonthHandler(None)
        self.setYearHandler(None)
        self.setDayHandler(None)

        # Merge keyword options with default options
        optiondefs = {}
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, relief = None)
        self.initialiseoptions(DateOfBirthEntry)        
        
        # for scroll list buttons
        gui = loader.loadModel("phase_3/models/gui/month_year_gui")

        # vars that are the same across all controls
        bS = 14
        normalColor = (0.9,0.6,0.1,1)
        downColor = (0.2,0.6,1,1)
        overColor = (1,1,0,1)
        disabledColor = (0.5,0.5,0.5,1)
        incButtonPos = (1.75, 0,-0.1)
        decButtonPos = (1.75,0,0.6)
        itemFrameScale = 0.8
        imagePos = (0.5, 0, 0.25)
        imageScale = 12

        # positions of the controls, left-to-right
        w = 4
        posTable = (
            (-0.75, 0, 0),
            (-0.75+w, 0, 0),
            (-0.75+(w*2), 0, 0),
            )

        self.months = TTLocalizer.DateOfBirthEntryMonths
        self.monthControl = DirectScrolledList(
            parent = self,
            relief = None,
            items = self.months,
            image = gui.find("**/month-yearPanel"),
            image_scale = imageScale,
            image_pos = imagePos,
            # inc and dec are DirectButtons
            incButton_image = gui.find("**/smallVerticalArrow"),
            incButton_relief = None,
            incButton_scale = (bS,bS,-bS),
            incButton_pos = incButtonPos,
            incButton_image0_color = normalColor,
            incButton_image1_color = downColor,
            incButton_image2_color = overColor,
            incButton_image3_color = disabledColor,
            decButton_image = gui.find("**/smallVerticalArrow"),
            decButton_relief = None,
            decButton_scale = (bS,bS,bS),
            decButton_pos = decButtonPos,
            decButton_image0_color = normalColor,
            decButton_image1_color = downColor,
            decButton_image2_color = overColor,
            decButton_image3_color = disabledColor,
            pos = posTable[0],
            # itemFrame is a DirectFrame used to hold all the items
            itemFrame_pos = (0,0,0),
            itemFrame_scale = itemFrameScale,
            itemFrame_relief = None,
            #itemFrame_frameSize = (-0.1,0.1,-0.1,0.1),
            #itemFrame_frameColor = mcolor,  
            #itemFrame_borderWidth = (0.01, 0.01),
            )

        # set to empty by default
        self.days = range(1,31+1)
        strDays = map(str, self.days)
        self.dayControl = DirectScrolledList(
            parent = self,
            relief = None,
            items = strDays,
            image = gui.find("**/month-yearPanel"),
            image_scale = imageScale,
            image_pos = imagePos,
            # inc and dec are DirectButtons
            # note: these buttons are switched, to reverse the order
            # of the items
            incButton_image = gui.find("**/smallVerticalArrow"),
            incButton_relief = None,
            incButton_scale = (bS,bS,bS),
            incButton_pos = decButtonPos,
            incButton_image0_color = normalColor,
            incButton_image1_color = downColor,
            incButton_image2_color = overColor,
            incButton_image3_color = disabledColor,
            decButton_image = gui.find("**/smallVerticalArrow"),
            decButton_relief = None,
            decButton_scale = (bS,bS,-bS),
            decButton_pos = incButtonPos,
            decButton_image0_color = normalColor,
            decButton_image1_color = downColor,
            decButton_image2_color = overColor,
            decButton_image3_color = disabledColor,
            pos = posTable[1],
            # itemFrame is a DirectFrame used to hold all the items
            itemFrame_pos = (0,0,0),
            itemFrame_scale = itemFrameScale,
            itemFrame_relief = None,
            #itemFrame_frameSize = (-0.1,0.1,-0.1,0.1),
            #itemFrame_frameColor = mcolor,  
            #itemFrame_borderWidth = (0.01, 0.01),
            )
        # this has to be set before we do anything that triggers
        # the day control update function (i.e., use our own API
        # to set the current month/year)
        self.lastChosenDay = self.getDay()

        if curYear == None:
            curYear = self.dateObject.getYear()
        self.years = range(self.firstYear, curYear+1)
        # reverse the list so that the up button increments the year
        self.years.reverse()
        # convert the list of integers to strings
        strYears = map(str, self.years)
        self.yearControl = DirectScrolledList(
            parent = self,
            items = strYears,
            relief = None,
            image = gui.find("**/month-yearPanel"),
            image_scale = imageScale,
            image_pos = imagePos,
            # inc and dec are DirectButtons
            incButton_image = gui.find("**/smallVerticalArrow"),
            incButton_relief = None,
            incButton_scale = (bS,bS,-bS),
            incButton_pos = incButtonPos,
            incButton_image0_color = normalColor,
            incButton_image1_color = downColor,
            incButton_image2_color = overColor,
            incButton_image3_color = disabledColor,
            decButton_image = gui.find("**/smallVerticalArrow"),
            decButton_relief = None,
            decButton_scale = (bS,bS,bS),
            decButton_pos = decButtonPos,
            decButton_image0_color = normalColor,
            decButton_image1_color = downColor,
            decButton_image2_color = overColor,
            decButton_image3_color = disabledColor,
            pos = posTable[2],
            # itemFrame is a DirectFrame used to hold all the items
            itemFrame_pos = (0,0,0),
            itemFrame_scale = itemFrameScale,
            itemFrame_relief = None,
            #itemFrame_frameSize = (-0.1,0.1,-0.1,0.1),
            #itemFrame_frameColor = mcolor,  
            #itemFrame_borderWidth = (0.01, 0.01),
            )
        # start on default age
        self.setYear(curYear-self.defaultAge)

        if not self.showDay:
            # hide the day control and move the year control over
            self.dayControl.hide()
            self.yearControl.setPos(posTable[1])

        # make sure to set these last, so they don't get called
        # during construction
        self.monthControl['command'] = self.__handleMonth
        self.yearControl['command'] = self.__handleYear
        self.dayControl['command'] = self.__handleDay

        # make sure to set these last, so the client doesn't get
        # spurious callbacks
        self.setMonthHandler(monthHandler)
        self.setYearHandler(yearHandler)
        self.setDayHandler(dayHandler)

        gui.removeNode()

    def destroy(self):
        del self.monthHandler
        del self.dayHandler
        del self.yearHandler
        DirectFrame.destroy(self)

    def getMonth(self):
        """ returns int, 1..12 """
        month = self.monthControl.getSelectedText() # Jan/Feb/...
        return self.months.index(month)+1 # 1..12

    def getDay(self):
        """ returns int """
        return int(self.dayControl.getSelectedText())

    def getYear(self):
        """ returns int """
        return int(self.yearControl.getSelectedText())

    def setMonth(self, month):
        """ month: int, 1..12 """
        if month in [1,2,3,4,5,6,7,8,9,10,11,12]:
            self.monthControl.scrollTo(month-1)
        else:
            print ("month not found in list: %s" % (month))
            self.monthControl.scrollTo(0)
        self.__updateDaysInMonth()
        
    def setDay(self, day):
        """ day: int """
        if day in self.days:
            self.dayControl.scrollTo(self.days.index(day))
        else:
            print ("day not found in list: %s" % (day))
            self.dayControl.scrollTo(0)

    def setYear(self, year):
        """ year: int """
        if year in self.years:
            self.yearControl.scrollTo(self.years.index(year))
        else:
            print ("year not found in list: %s" % (year))
            self.yearControl.scrollTo(0)
        self.__updateDaysInMonth()

    def getAge(self):
        """ returns int years """
        return self.dateObject.getAge(self.getMonth(), self.getYear())

    def setMonthHandler(self, handler):
        self.monthHandler = handler

    def setDayHandler(self, handler):
        self.dayHandler = handler

    def setYearHandler(self, handler):
        self.yearHandler = handler

    def __handleMonth(self):
        #print 'handleMonth'
        self.__updateDaysInMonth()
        if self.monthHandler:
            self.monthHandler(self.getMonth())

    def __handleDay(self):
        #print 'handleDay'
        self.lastChosenDay = self.getDay()
        if self.dayHandler:
            self.dayHandler(self.getDay())

    def __handleYear(self):
        #print 'handleYear'
        self.__updateDaysInMonth()
        if self.yearHandler:
            self.yearHandler(self.getYear())

    def __updateDaysInMonth(self):
        """ update the day control to reflect the number of days
        in the month specified by the month and year controls
        """
        # preserve the 'last chosen day' value
        lastChosenDay = self.lastChosenDay

        oldNumDays = len(self.days)
        numDays = self.dateObject.getNumDaysInMonth(month=self.getMonth(),
                                                    year=self.getYear())
        self.days = range(1,numDays+1)

        self.__updateDayControlLength(oldNumDays, numDays)

        # attempt to set the day to the last day the user chose
        # if there are too few days in the month, choose the
        # last day of the month
        day = lastChosenDay
        if not day in self.days:
            day = self.days[-1]

        self.setDay(day)

        # restore the 'last chosen day' value
        self.lastChosenDay = lastChosenDay

    def __updateDayControlLength(self, oldDays, newDays):
        if oldDays > newDays:
            # remove some days
            for day in range(oldDays, newDays, -1):
                self.dayControl.removeItem(self.dayControl['items'][day-1])
        elif oldDays < newDays:
            # add some days
            for day in range(oldDays+1, newDays+1):
                self.dayControl.addItem(str(day))
        assert(len(self.dayControl['items']) == newDays)

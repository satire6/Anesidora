import time

class DateObject:
    """ default Date object; uses local clock """

    def getYear(self):
        """ returns int """
        return time.localtime(time.time())[0]
    def getMonth(self):
        """ returns int, 1..12 """
        return time.localtime(time.time())[1]
    def getDay(self):
        """ returns int, 1.. """
        return time.localtime(time.time())[2]

    def getDetailedAge(self, dobMonth, dobYear, dobDay=None,
                       curMonth=None, curYear=None, curDay=None):
        """ returns (int years, int months) """
        if curMonth is None:
            curMonth = self.getMonth()
        if curYear is None:
            curYear = self.getYear()
        if curDay is None:
            curDay = self.getDay()

        # perform calculations in months
        curMonths = (curYear * 12) + (curMonth - 1)
        dobMonths = (dobYear * 12) + (dobMonth - 1)

        if dobMonth == curMonth:
            # if we were not given a day of birth, we count
            # being in the birth month as counting for a month
            # towards the age

            # if we were given a day of birth, and we are not
            # yet at that day of the month, don't count the
            # current month towards the age
            if dobDay is not None:
                if dobDay > curDay:
                    curMonths -= 1

        ageMonths = curMonths - dobMonths
        return (int(ageMonths / 12), (ageMonths % 12))

    def getAge(self, dobMonth, dobYear, dobDay=None,
               curMonth=None, curYear=None, curDay=None):
        """ returns int years """
        return self.getDetailedAge(dobMonth, dobYear, dobDay=dobDay,
                                   curMonth=curMonth, curYear=curYear,
                                   curDay=curDay)[0]

    def getNumDaysInMonth(self, month = None, year = None):
        """Returns the number of days in the month.
        
        If any of the arguments are missing (month or year) the
        current month/year is assumed."""
    
        def isLeapYear(year):
            """Returns 1 if year is a leap year, zero otherwise."""
            if year%4 == 0:
                if year%100 == 0:
                    if year%400 == 0:
                        return 1
                    else:
                        return 0
                else:
                    return 1
            else:
                return 0

        if month is None:
            m = self.getMonth()
        else:
            m = month

        if year is None:
            y = self.getYear()
        else:
            y = year
    
        if m == 2:
            if isLeapYear(y):
                return 29
            else:
                return 28
        elif m in (1, 3, 5, 7, 8, 10, 12):
            return 31
        else:
            return 30

import DateObject

class TTDateObject(DateObject.DateObject):
    """ Toontown date object; uses the account server date """
    def __init__(self, accountServerDate):
        self.accountServerDate=accountServerDate

    def getYear(self):
        """ returns int """
        return self.accountServerDate.getYear()
    def getMonth(self):
        """ returns int, 1..12 """
        return self.accountServerDate.getMonth()
    def getDay(self):
        """ returns int, 1.. """
        return self.accountServerDate.getDay()

    def getDetailedAge(self, dobMonth, dobYear, dobDay=None,
                       curMonth=None, curYear=None, curDay=None):
        """ returns (int years, int months) """
        return DateObject.DateObject.getDetailedAge(
            self,
            dobMonth, dobYear, dobDay,
            curMonth = self.getMonth(),
            curYear = self.getYear(),
            curDay = self.getDay(),
            )

    def getAge(self, dobMonth, dobYear, dobDay=None,
               curMonth=None, curYear=None, curDay=None):
        """ returns int years """
        return TTDateObject.getDetailedAge(
            self,
            dobMonth, dobYear, dobDay=dobDay,
            curMonth=curMonth, curYear=curYear, curDay=curDay)[0]

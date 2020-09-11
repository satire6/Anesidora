"""AccountServerDate.py: contains the AccountServerDate class """

from pandac.PandaModules import *
from otp.login.HTTPUtil import *
from direct.directnotify import DirectNotifyGlobal
from otp.login import TTAccount
import DateObject
import TTDateObject
import time

class AccountServerDate:
    """ This class gets the current date from the account server,
    in order to protect against incorrect client clock settings.
    It exposes the current month and year.

    Since the account server is located in one particular time zone,
    and clients are potentially in any time zone, this class subtracts
    a day or two from the account server's date in order to ensure that
    we don't move on to a new month/year before every time zone is in
    that new month/year.
    """
    notify = \
           DirectNotifyGlobal.directNotify.newCategory("AccountServerDate")

    def __init__(self):
        self.__grabbed = 0

    # this is used by the cr in error msgs
    def getServer(self):
        return TTAccount.getAccountServer().cStr()
    
    def grabDate(self, force=0):
        """ might throw a TTAccountException """
        if self.__grabbed and not force:
            self.notify.debug('using cached account server date')
            return
        
        if (base.cr.accountOldAuth or
            base.config.GetBool('use-local-date', 0)):
            self.__useLocalClock()
            return
        
        url = URLSpec(self.getServer())
        url.setPath('/getDate.php')
        self.notify.debug('grabbing account server date from %s' %
                          url.cStr())
            
        response = getHTTPResponse(url, http)
        
        # make sure we got a valid response
        if response[0] != 'ACCOUNT SERVER DATE':
            self.notify.debug('invalid response header')
            raise UnexpectedResponse, \
                  "unexpected response, response=%s" % response

        # grab the date
        try:
            epoch = int(response[1])
        except ValueError, e:
            self.notify.debug(str(e))
            raise UnexpectedResponse, \
                  "unexpected response, response=%s" % response

        # since we're now dealing with birth-days, we need a precise day
        # value. Just use Pacific time for now; the rest of the world
        # can deal.
        """
        # pull the date back a few days, to ensure that we don't move
        # on to a new month/year until all time zones are in the
        # new month/year
        epoch -= 2 * 24*60*60
        """

        timeTuple = time.gmtime(epoch)
        self.year = timeTuple[0]
        self.month = timeTuple[1]
        self.day = timeTuple[2]

        # replace the local-clock dateObject on the cr with one
        # that will ask us for the current date
        base.cr.dateObject = TTDateObject.TTDateObject(self)

        self.__grabbed = 1

    def __useLocalClock(self):
        # just store the local date
        self.month = base.cr.dateObject.getMonth()
        self.year = base.cr.dateObject.getYear()
        self.day = base.cr.dateObject.getDay()

    def getMonth(self):
        return self.month
    def getYear(self):
        return self.year
    def getDay(self):
        return self.day

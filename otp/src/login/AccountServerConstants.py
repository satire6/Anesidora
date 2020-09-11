"""AccountServerConstants.py: contains the AccountServerConstants class """

from pandac.PandaModules import *
from RemoteValueSet import *
from direct.directnotify import DirectNotifyGlobal
import TTAccount
import HTTPUtil

class AccountServerConstants(RemoteValueSet):
    notify = \
           DirectNotifyGlobal.directNotify.newCategory("AccountServerConstants")

    def __init__(self, cr):
        """ might throw a TTAccountException """
        self.expectedConstants = [
            'minNameLength',
            'minPwLength',
            'allowNewAccounts',
            'freeTrialPeriodInDays',
            'priceFirstMonth',
            'pricePerMonth',
            'customerServicePhoneNumber',
            'creditCardUpFront',
            ]
        # if in dev env with no account server, constants will be set to
        # an arbitrary string. If a constant needs to be something more
        # specific, set it here
        # rurbino the minPw and minName used to be zero, that sounds bad and upped it to 1
        self.defaults = {
            'minNameLength': '1',
            'minPwLength': '1',
            'allowNewAccounts': '1',
            'creditCardUpFront': '0',
            'priceFirstMonth': '9.95',
            'pricePerMonth': '9.95',
            }

        # do not query server for AccountConstants (US is no - will query)
        noquery = 1
#
# rest deprecated because all production functionality should have moved to website
# (only used for customer service number for the US)

        if cr.productName == 'DisneyOnline-US':
            if base.config.GetBool('tt-specific-login',0):
                # the new website does not have constants.php, don't try to query it
                pass
            else:
                noquery = 0

        if (cr.accountOldAuth or
            base.config.GetBool('default-server-constants', noquery)):
            self.notify.debug('setting defaults, not using account server constants')

            # fake it; create and populate a 'dict' object
            self.dict = {}

            # user is running in dev env, with no account server
            # set some defaults
            for constantName in self.expectedConstants:
                self.dict[constantName] = 'DEFAULT'
            # some constants need to be something more specific
            self.dict.update(self.defaults)
            return
        
        url = URLSpec(AccountServerConstants.getServer())
        url.setPath('/constants.php')
        self.notify.debug('grabbing account server constants from %s' %
                          url.cStr())

        RemoteValueSet.__init__(self, url, cr.http,
                                expectedHeader='ACCOUNT SERVER CONSTANTS',
                                expectedFields=self.expectedConstants,)

    # override the accessors so we can warn about undeclared constants
    def getBool(self, name):
        return self.__getConstant(name, RemoteValueSet.getBool)
    def getInt(self, name):
        return self.__getConstant(name, RemoteValueSet.getInt)
    def getFloat(self, name):
        return self.__getConstant(name, RemoteValueSet.getFloat)
    def getString(self, name):
        return self.__getConstant(name, RemoteValueSet.getString)

    def __getConstant(self, constantName, accessor):
        if not constantName in self.expectedConstants:
            self.notify.warning(
                "requested constant '%s' not in expected constant list; "
                "if it's a new constant, add it to the list" %
                constantName)
        return accessor(self, constantName)

    # this is used by the tcr in error msgs
    @staticmethod
    def getServer():
        return TTAccount.getAccountServer().cStr()
    @staticmethod
    def getServerURL():
        return TTAccount.getAccountServer()

"""TTAccount.py is for communicating with account servers"""

from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil
from otp.otpbase import OTPLocalizer
import HTTPUtil
import RemoteValueSet
import copy

accountServer = ''
accountServer = launcher.getAccountServer()
print "TTAccount: accountServer from launcher: ", (accountServer)
        
configAccountServer = base.config.GetString('account-server', '')
if configAccountServer:
    accountServer = configAccountServer
    print "TTAccount: overriding accountServer from config: ", (accountServer)

if not accountServer:
    accountServer = "https://toontown.go.com"
    print "TTAccount: default accountServer: ", (accountServer)

accountServer = URLSpec(accountServer, 1)

def getAccountServer():
    return accountServer

# TTAccount only raises HTTPUtil exceptions; rename the base
# exception for easy/handsome client exception catching
TTAccountException = HTTPUtil.HTTPUtilException

class TTAccount:
    notify = DirectNotifyGlobal.directNotify.newCategory("TTAccount")
    
    def __init__(self, cr):
        self.cr = cr
        self.response = None

    """
    UNLESS OTHERWISE SPECIFIED,
    these functions return None on success,
    return an error string on 'normal' failure,
    and raise a TTAccountException on connection problem, bad response, etc.
    """

    def createAccount(self, loginName, password, data):
        """
        Ask the account server to create a new account.
        see talk() for list of required fields in 'data' dict
        see above for return values
        """
        return self.talk('create',
                         data=self.__makeLoginDict(loginName, password, data))

    def authorize(self, loginName, password):
        """
        Ask the account server to give us a play token.
        see above for return values
        """
        return self.talk('play', data=self.__makeLoginDict(loginName, password))
    
    def createBilling(self, loginName, password, data):
        """
        Start paying using a credit card.
        see talk() for list of required fields in 'data' dict
        see above for return values
        """
        return self.talk('purchase',
                         data=self.__makeLoginDict(loginName, password, data))

    def setParentPassword(self, loginName, password, parentPassword):
        """
        set the parent password
        see above for return values
        """
        return self.talk(
            'setParentPassword',
            data=self.__makeLoginDict(loginName, password,
                                      {'parentPassword': parentPassword}))

    def supportsParentPassword(self):
        """Returns true if authenticateParentPassword is implemented
        and meaningful for this type of account system."""
        return 1

    def authenticateParentPassword(self, loginName,
                                   password, parentPassword):
        """
        try to authenticate the parent password
        NOTE: this does not actually set any state on the account,
        it just tests a parent password
        returns (int success, string error)
        you will get:
        (1, None) --> success, password cleared
        (0, None) --> failure, password did not clear
        (0, '<some message>') --> failure, but not due to bad password,
                                  error msg explains what the problem is
        this function will never intentionally raise an exception
        """
        try:
            errorMsg = self.talk(
                'authenticateParentPassword',
                data=self.__makeLoginDict(loginName, parentPassword))
            if not errorMsg:
                return (1, None)
            
            # we got an error message; check to see if it's the
            # 'wrong password' error
            if self.response.getInt('errorCode') in (5, 72):
                return (0, None)

            # some other error, pass it back
            return (0, errorMsg)
        except TTAccountException, e:
            # connection error, bad response, etc.
            # pass it back
            return (0, str(e))

    def supportsAuthenticateDelete(self):
        """ Returns true if authenticateDelete is implemented
        for this type of account system """
        return 1

    def authenticateDelete(self, loginName, password):
        """
        authenticate the deletion of a toon
        password can be either the login or parent password
        NOTE: this does not actually set any state on the account,
        it just authenticates the password
        returns (int success, string error)
        you will get:
        (1, None) --> success, password cleared
        (0, None) --> failure, password did not clear
        (0, '<some message>') --> failure, but not due to bad password,
                                  error msg explains what the problem is
        this function will never intentionally raise an exception
        """
        try:
            errorMsg = self.talk(
                'authenticateDelete',
                data=self.__makeLoginDict(loginName, password))
            if not errorMsg:
                return (1, None)
            
            # we got an error message; check to see if it's the
            # 'wrong password' error
            if self.response.getInt('errorCode') in (5, 72):
                return (0, None)

            # some other error, pass it back
            return (0, errorMsg)
        except TTAccountException, e:
            # connection error, bad response, etc.
            # pass it back
            return (0, str(e))
    
    def enableSecretFriends(self, loginName, password,
                            parentPassword, enable=1):
        """
        attempt to enable secret friends
        returns (int success, string error)
        you will get:
        (1, None) --> success, password cleared, operation gperformed
        (0, None) --> failure, password did not clear, operation not performed
        (0, '<some message>') --> failure, but not due to bad password,
                                  error msg explains what the problem is
        this function will never intentionally raise an exception
        """
        try:
            errorMsg = self.talk(
                'setSecretChat',
                data=self.__makeLoginDict(loginName, parentPassword,
                                          {'chat': base.cr.secretChatAllowed,
                                           'secretsNeedParentPassword': base.cr.secretChatNeedsParentPassword}
                                          )
                )
            if not errorMsg:
                return (1, None)
            
            # we got an error message; check to see if it's the
            # 'wrong password' error
            if self.response.getInt('errorCode') in (5, 72):
                return (0, None)

            # some other error, pass it back
            return (0, errorMsg)
        except TTAccountException, e:
            # connection error, bad response, etc.
            # pass it back
            return (0, str(e))
    
    def changePassword(self, loginName, password, newPassword):
        """
        change password to newPassword
        see above for return values
        """
        return self.talk(
            'purchase',
            data=self.__makeLoginDict(loginName, password,
                                      {'newPassword': newPassword}))

    def requestPwdReminder(self, email=None, acctName=None):
        """
        request an email with the password(s)
        will be sent to the parent/billing email address

        pass email OR acctName
        see above for return values
        """
        assert acctName or email
        assert not (acctName and email)
        data = {}
        if email is not None:
            data['email'] = email
        else:
            data['accountName'] = acctName
        return self.talk('forgotPassword', data)
    
    def cancelAccount(self, loginName, password):
        """
        Stop paying.
        see above for return values
        """
        return self.talk('cancel',
                         data=self.__makeLoginDict(loginName, password))

    def getAccountData(self, loginName, password):
        """
        retrieves account fields for a specific account
        all field values are strings

        on success, account data is available in self.accountData dictionary
        see above for return values
        """
        errorMsg = self.talk(
            'get',
            data=self.__makeLoginDict(loginName, password))
        # if there was an error msg from the server, return it
        if errorMsg:
            self.notify.warning('getAccountData error: %s' % errorMsg)
            return errorMsg

        # TODO: check that we got all the expected fields

        # if there's an error field, print it out
        if self.response.hasKey('errorMsg'):
            self.notify.warning("error field is: '%s'" %
                                self.response.getString('errorMsg'))

        # make an independent copy of the raw result dictionary
        self.accountData = copy.deepcopy(self.response)

        fieldNameMap = {
            'em': 'email',
            'l1': 'addr1',
            'l2': 'addr2',
            'l3': 'addr3',
            }

        # rename some fields
        dict = self.accountData.dict
        for fieldName in dict.keys():
            if fieldNameMap.has_key(fieldName):
                dict[fieldNameMap[fieldName]] = dict[fieldName]
                del dict[fieldName]

        return None

    def getLastErrorMsg(self, forceCustServNum=0):
        """ call this function if you need to show the customer
        service # unconditionally on all errors, or if you
        have a threshold condition beyond which the CS # should
        always be included.

        For error codes >= 100, we always add the CS #. It might
        be simpler for the server to add it, but that would waste
        bandwidth.
        """
        assert self.response.hasKey('errorCode')
        assert self.response.hasKey('errorMsg')
        errCode = self.response.getInt('errorCode')

        if errCode < 100:
            # these are 'user-fixable' problems
            # don't show customer service number if
            # suppress flag is true
            msg = self.response.getString('errorMsg')
            if forceCustServNum:
                # put up an 'if you need help, call...' msg
                msg += (' ' + OTPLocalizer.TTAccountCustomerServiceHelp %
                        self.cr.accountServerConstants.getString('customerServicePhoneNumber'))
        elif errCode < 200:
            # these are non-user fixable, but it's useful
            # for the user to see what the error is
            msg = self.response.getString('errorMsg')
            msg += (' ' + OTPLocalizer.TTAccountCustomerServiceHelp %
                    self.cr.accountServerConstants.getString('customerServicePhoneNumber'))
        elif errCode >= 500:
            # these are non-user fixable, and there's no
            # useful information that we can give to the user
            msg = OTPLocalizer.TTAccountIntractibleError
            msg += (' ' + OTPLocalizer.TTAccountCallCustomerService %
                    self.cr.accountServerConstants.getString('customerServicePhoneNumber'))
        else:
            # don't know what this range of errors is all about...
            # log a warning...
            self.notify.warning("unknown error code class: %s: %s" %
                                (self.response.getInt('errorCode'),
                                 self.response.getString('errorMsg')))
            # and pass on the server's error msg, with the Cust. Serv. #
            msg = self.response.getString('errorMsg')
            msg += (' ' + OTPLocalizer.TTAccountCallCustomerService %
                    self.cr.accountServerConstants.getString('customerServicePhoneNumber'))

        return msg

    def __makeLoginDict(self, loginName, password, data=None):
        """ many of the TTAccount API functions accept
        a login and password separately from the dict
        of data fields; this function puts the login
        and password into a dict, the way talk() wants
        it """
        dict = {
            'accountName': loginName,
            'password': password
            }
        if data:
            dict.update(data)
        return dict

    def makeLoginDict(self, loginName, password, data=None):
        return self.__makeLoginDict(loginName, password,data)

    def talk(self, operation, data={}):
        """
        A utility function used by other members of this class.
        returns:
          None: no error
          string: user error msg (bad password...)
        raises TTAccountException on connection failure, etc.
        """
        self.notify.debug("TTAccount.talk()")

        # ensure that data contains nothing but strings
        for key in data.keys():
            data[key] = str(data[key])

        # assert that 'data' contains all the required data
        if operation in ('play', 'get', 'cancel',
                         'authenticateParentPassword',
                         'authenticateDelete',
                         'authenticateParentPasswordNewStyle',
                         'authenticateDeleteNewStyle'):
            assert PythonUtil.contains(
                data.keys(),
                ('accountName',
                 'password'))
        elif operation == 'authenticateParentUsernameAndPassword':
            assert PythonUtil.contains(
                data.keys(),
                ('accountName',
                 'parentUsername',
                 'parentPasswordNewStyle',
                 'userid'))
        elif operation == 'forgotPassword':
            assert data.has_key('accountName') or data.has_key('email')
        elif operation == 'setParentPassword':
            assert PythonUtil.contains(
                data.keys(),
                ('accountName',
                 'password',
                 'parentPassword',))
        elif operation == 'setSecretChat':
            assert PythonUtil.contains(
                data.keys(),
                ('accountName',
                 'password',
                 'chat',))
        elif operation == 'create':
            assert PythonUtil.contains(
                data.keys(),
                ('accountName',
                 'password',
                 #'dobYear',
                 #'dobMonth',
                 #'dobDay',
                 #'email',
                 #'referrer',
                 ))
        elif operation == 'purchase':
            # is this a password change or a purchase op?
            if data.has_key('newPassword'):
                assert PythonUtil.contains(
                    data.keys(),
                    ('accountName',
                     'password'))
            else:
                assert PythonUtil.contains(
                    data.keys(),
                    ('accountName',
                     'password',
                     'email', 
                     #'dobMonth',
                     #'dobYear',
                     'ccType',
                     'ccNumber',
                     'ccMonth',
                     'ccYear',
                     'nameOnCard',
                     'addr1',
                     'addr2',
                     'city',
                     'state',
                     'country',
                     'zip'))
        else:
            self.notify.error('Internal TTAccount error: need to add '
                              '\'required data\' checking for %s operation' %
                              operation)

        # map operations to php pages
        op2Php = {
            'play': 'play',
            'get': 'get',
            'cancel': 'cancel',
            'create': 'create',
            'purchase': 'purchase',
            'setParentPassword': 'setSecrets',
            'authenticateParentPassword': 'authenticateChat',
            'authenticateDelete': 'authDelete',
            'setSecretChat': 'setChat',
            'forgotPassword': 'forgotPw',
            # these last 3 are exclusive to the redesigned web site
            'authenticateParentPasswordNewStyle' : 'api/authChat',
            'authenticateParentUsernameAndPassword' : 'api/authParentChat',
            'authenticateDeleteNewStyle' : 'api/authDelete',
            }

        newWebOperations = ('authenticateParentPasswordNewStyle',
                          'authenticateParentUsernameAndPassword',
                          'authenticateDeleteNewStyle')
        url = URLSpec(getAccountServer())
        if operation in newWebOperations :

            url.setPath('/%s' % (op2Php[operation]))            
        else:
            url.setPath('/%s.php' % (op2Php[operation]))
        body = ''

        if data.has_key('accountName'):
            if operation not in newWebOperations:
                # name is put on url for documentation only
                url.setQuery('n=%s' % (URLSpec.quote(data['accountName'])))

        serverFields = {
            # map: local field name --> server field name
            'accountName': 'n',    # accountName
            'password': 'p',       # accountPassword
            'parentPassword': 'sp',# parent password
            'newPassword': 'np',   # new password for password change
            'chat': 'chat',        # chat enable flag
            'email': 'em',         # email address
            'dobYear': 'doby',     # date of birth year
            'dobMonth': 'dobm',    # date of birth month
            'dobDay': 'dobd',      # date of birth day
            'ccNumber': 'ccn',     # credit card number
            'ccMonth': 'ccm',      # credit card expiration month (1==January)
            'ccYear': 'ccy',       # credit card expiration year
            'nameOnCard': 'noc',   # NameOnCard, the credit card owner
            'addr1': 'l1',         # Address line 1
            'addr2': 'l2',         # Address line 2
            'addr3': 'l3',         # Address line 3
            'city': 'city',        # Billing address city
            'state': 'state',      # Billing address state
            'country': 'country',  # Billing address country code
            'zip': 'zip',          # Billing address zip/postal code
            'referrer': 'ref',     # referrer code
            'secretsNeedParentPassword': 'secretsNeedsParentPassword',     # restricted secret chat
            'parentPasswordNewStyle' : 'pp',
            'parentUsername' : 'pu',
            'userid' : 'userid',
            }
        ignoredFields = ('ccType',)

        # add all of the fields in 'data' to the HTTP body

        # populate a map of serverField:value pairs so that we
        # can add the fields in alphabetical order
        outBoundFields = {}
        for fieldName in data.keys():
            if not serverFields.has_key(fieldName):
                if not fieldName in ignoredFields:
                    # unknown field name
                    self.notify.error(
                        'unknown data field: %s' % fieldName)
            else:
                outBoundFields[serverFields[fieldName]] = data[fieldName]

        # add the fields to the body in alphabetical order
        orderedFields = outBoundFields.keys()
        orderedFields.sort()
        for fieldName in orderedFields:
            if len(body):
                body += '&'
            body += "%s=%s" % (
                fieldName,
                URLSpec.quotePlus(outBoundFields[fieldName]))

        self.notify.debug("url="+url.cStr())
        # important: the body may contain the password; only print in debug env
        self.notify.debug("body="+body)

        if operation in ('get',):
            expectedHeader = 'ACCOUNT INFO'
        elif operation in ('play', 'cancel', 'create', 'purchase',
                           'setParentPassword', 'setSecretChat',
                           'authenticateParentPassword',
                           'authenticateDelete',
                           'forgotPassword',
                           'authenticateParentPasswordNewStyle',
                           'authenticateParentUsernameAndPassword',
                           'authenticateDeleteNewStyle',):
            expectedHeader = 'ACCOUNT SERVER RESPONSE'
        else:
            self.notify.error('Internal TTAccount error: need to set '
                              'expected response header for \'%s\' operation' %
                              operation)

        # In certain circumstances in which the Disney proxy fails to
        # contact the server, it seems to report a successful
        # connection and simply returns a bogus response.
        # Make sure to check for the proper header in the response.
        self.response = RemoteValueSet.RemoteValueSet(
            url, self.cr.http, body=body, expectedHeader=expectedHeader)
        self.notify.debug("    self.response="+str(self.response))

        # was there an error?
        if self.response.hasKey('errorCode'):
            errorCode = self.response.getInt('errorCode')

            self.notify.info('account server error code: %s' % errorCode)

            # if free time has expired, set it on the cr
            if errorCode == 10:
                self.cr.freeTimeExpiresAt = 0

        # if there's an error message in the response,
        # pass it back
        if self.response.hasKey('errorMsg'):
            # add the customer service # for error messages that
            # should always have the #
            return self.getLastErrorMsg()

        # grab some info out of the response for easy access
        if operation in ('get', 'forgotPassword', 'authenticateDelete',
                         'play', 'cancel', 'create', 'purchase',
                         'setParentPassword', 'authenticateParentPassword',
                         'authenticateParentPasswordNewStyle',
                         'authenticateParentUsernameAndPassword',
                         'authenticateDeleteNewStyle'):
            # none of these require data from the web anymore
            pass
        elif operation == 'setSecretChat':
            # setSecretChat needs a new playToken
            self.playToken = self.response.getString('playToken')
            self.playTokenIsEncrypted=1
        else:
            self.notify.error('Internal TTAccount error: need to extract '
                              'useful data for %s operation' %
                              operation)

        return None # no error


    def authenticateParentUsernameAndPassword(self, loginName,
                                   password, parentUsername, parentPassword):
        """
        try to authenticate the parent password
        NOTE: this does not actually set any state on the account,
        it just tests a parent password
        returns (int success, string error)
        you will get:
        (1, None) --> success, password cleared
        (0, None) --> failure, password did not clear
        (0, '<some message>') --> failure, but not due to bad password,
                                  error msg explains what the problem is
        this function will never intentionally raise an exception
        """
        try:
            errorMsg = self.talk(
                'authenticateParentUsernameAndPassword',
                data=self.__makeLoginDict(loginName, password,
                                          {'parentUsername': parentUsername,
                                           'parentPasswordNewStyle' : parentPassword,
                                           'userid': loginName}))
                
            if not errorMsg:
                return (1, None)
            
            # we got an error message; check to see if it's the
            # 'wrong password' error
            if self.response.getInt('errorCode') in (5, 72):
                return (0, None)

            # some other error, pass it back
            return (0, errorMsg)
        except TTAccountException, e:
            # connection error, bad response, etc.
            # pass it back
            return (0, str(e))


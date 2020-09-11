""" TestTTAccount: contains a test suite for TTAccount """
# import this module once Toontown is running

import random
from direct.showbase.PythonUtil import Functor

SHOULD_SUCCEED = 0
SHOULD_FAIL = 1

class TTTester:
    def __init__(self):
        self.tests = 0
        self.errStrings = []

    def __logResult(self, success, errMsg=None):
        self.tests += 1
        if not success:
            assert type(errMsg) == type('')
            self.errStrings.append(errMsg)

    def printResults(self):
        print "================================================"
        print "%s tests, %s failures" % (self.tests, len(self.errStrings))
        for i in range(len(self.errStrings)):
            print "- %s" % (self.errStrings[i])

    def runTest(self, test, shouldFail, errMsg):
        """ test is the test condition; it should be a functor that
        returns None on success, error string on failure, a la TTAccount.
        If you expect the test to fail, shouldFail should be non-zero.
        errMsg should be a string explaining what happened if the
        overall metatest fails; not used if test performs as expected.

        returns boolean 'success' of the metatest
        """
        result = test()
        if result:
            print 'result:' + result
        
        # the test may have failed, but that might be what we wanted
        passed = 0
        if shouldFail and (result is not None):
            passed = 1
        elif (not shouldFail) and (result is None):
            passed = 1
            
        # if the metatest failed, construct an error message
        err = None
        if not passed:
            err = errMsg
            if result is not None:
                err = '%s: "%s"' % (err, result)
                
        self.__logResult(passed, err)
        return passed

def getRandomString(prefix='test'):
    name = prefix
    for i in range(10):
        name += str(random.randrange(10))
    return name

def run():
    tt = base.cr.loginInterface
    tester = TTTester()

    # pick a random login and password
    # chances are that this account name has not been used before.
    name = getRandomString('login')
    pwd = getRandomString('password')

    # try logging in with an invalid account name
    tester.runTest(Functor(tt.authorize, name, pwd),
                   SHOULD_FAIL,
                   "login attempt with probably-invalid "
                   "username %s succeeded" % name)

    # try getting account data for an invalid account name
    tester.runTest(Functor(tt.getAccountData, name, pwd),
                   SHOULD_FAIL,
                   "account data 'get' with probably-invalid "
                   "username %s succeeded" % name)

    # create the account
    data = {
        'dobYear' : 1978,
        'dobMonth' : 3,
        'dobDay' : 14,
        }
    accountCreated = tester.runTest(
        Functor(tt.createAccount, name, pwd, data),
        SHOULD_SUCCEED,
        "account creation failed")

    if accountCreated:
        # try logging in with a valid account name
        tester.runTest(Functor(tt.authorize, name, pwd),
                       SHOULD_SUCCEED,
                       "login attempt failed")

        # try getting the account data
        tester.runTest(Functor(tt.getAccountData, name, pwd),
                       SHOULD_SUCCEED,
                       "failed to get account data")

    tester.printResults()

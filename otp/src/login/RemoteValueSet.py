"""RemoteValueSet.py: contains the RemoteValueSet class"""

from direct.directnotify import DirectNotifyGlobal
import TTAccount
import HTTPUtil

class RemoteValueSet:
    """
    This class retrieves key/value pairs that are returned
    by an HTTP request and makes the values available through
    its interface functions.
    The actual data is directly accessible as a dictionary called
    'RemoteValueSet.dict'.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("RemoteValueSet")
    
    def __init__(self, url, http, body='',
                 expectedHeader=None, expectedFields=[],
                 onUnexpectedResponse=None):
        """
        expectedHeader is what we expect on the first line
        of the response.
        expectedFields is a list of keys that we expect to get back;
        if we don't get all of them, it's considered an error

        on error, will raise a RemoteValueSet.UnexpectedResponse
        (unless you override 'onUnexpectedResponse'; onUnexpectedResponse
        should be a function that takes an error-message string. Note that
        the internal state of a RemoteValueSet will be undefined if
        onUnexpectedResponse is called.)
        """
        if onUnexpectedResponse is None:
            onUnexpectedResponse = self.__onUnexpectedResponse

        # get the response from the server
        response = HTTPUtil.getHTTPResponse(url, http, body)

        if expectedHeader is not None:
            if response[0] != expectedHeader:
                errMsg = 'unexpected response: %s' % response
                self.notify.warning(errMsg)
                onUnexpectedResponse(errMsg)
                return
            # eat the header
            response = response[1:]

        # put the key/value pairs in a dictionary
        self.dict = {}
        for line in response:
            # skip blank lines
            if not len(line):
                continue

            # separate the constant name and its value
            # '1' means only make one split (the first one, from the left)
            try:
                name, value = line.split('=', 1)
            except ValueError, e:
                errMsg = 'unexpected response: %s' % response
                self.notify.warning(errMsg)
                onUnexpectedResponse(errMsg)
                return

            if len(expectedFields):
                if not name in expectedFields:
                    self.notify.warning(
                        "received field '%s' that is not "
                        "in expected field list" %
                        name)

            self.dict[name] = value

        # make sure we got all of the expected fields
        for name in expectedFields:
            if not self.dict.has_key(name):
                errMsg = "missing expected field '%s'" % name
                self.notify.warning(errMsg)
                onUnexpectedResponse(errMsg)
                return

    def __repr__(self):
        return "RemoteValueSet:%s" % str(self.dict)

    def hasKey(self, key):
        return self.dict.has_key(key)

    # accessors
    # If 'name' is not found, and you provide a 'default' value,
    # 'default' will be returned. 'default' may be anything other
    # than None.
    def getBool(self, name, default=None):
        return self.__getValue(name, lambda x: int(x) != 0, default)
    def getInt(self, name, default=None):
        return self.__getValue(name, int, default)
    def getFloat(self, name, default=None):
        return self.__getValue(name, float, default)
    def getString(self, name, default=None):
        return self.__getValue(name, str, default)

    # private members
    def __getValue(self, name, convOp, default):
        # if no default value is provided, make sure to
        # throw a KeyError exception if 'name' not in dict
        if default is None:
            return convOp(self.dict[name])
        else:
            return convOp(self.dict.get(name, default))

    def __onUnexpectedResponse(self, errStr):
        raise HTTPUtil.UnexpectedResponse(errStr)

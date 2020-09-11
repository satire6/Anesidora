"""LoginGoAccount: Login using a pre-supplied GoReg token from the
registry, e.g. a DMC 'blue' token."""

from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram


class LoginGoAccount(LoginBase.LoginBase):
    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def createAccount(self, loginName, password, data):
        """
        Send a message to the server with our loginName
        return error string or None.
        """
        # We cannot create accounts in this interface.
        return 'Unsupported'

    def authorize(self, loginName, password):
        """
        Send a message to the server with our loginName
        return error string or None.
        date of birth:
          year:int
          month:int, 1..12
          day:int 1..31
        """
        # Separating authorize() and sendLoginMsg() is used more by
        # other login methods.  For us, we'll just store the parameters:
        self.loginName=loginName
        self.password=password
        return None # no error.

    def supportsRelogin(self):
        """
        Returns true if this login interface supports logging in
        multiple different times.
        """
        return 0

    def sendLoginMsg(self):
        """
        Send a message to the server with our loginName
        """
        cr=self.cr
        # Time to send a login message
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_LOGIN_2)
        # Add the token--this has been stored as the password.
        datagram.addString(self.password)
        # Add the Server Version ID
        datagram.addString(cr.serverVersion)
        # Add the dc file hash
        datagram.addUint32(cr.hashVal)
        self.__addTokenType(datagram)
        # Add the download verification string.
        datagram.addString(cr.validateDownload)
        # And the magic word enable string.
        datagram.addString(cr.wantMagicWords)
        # Send the message
        cr.send(datagram)

    def resendPlayToken(self):
        """
        Resends our playToken to the game server while still logged
        on.  This is necessary when our playTaken has changed
        properties in-game, for instance when we enable chat.
        """
        return
    
    def requestPwdReminder(self, email=None, acctName=None):
        """
        Request a password-reminder email, given an email address OR
        account name. (unused arg should be None)
        Returns non-zero on success
        """
        return 0

    def getAccountData(self, loginName, password):
        return 'Unsupported'

    # setParentPassword is not needed on this interface

    def supportsParentPassword(self):
        """Returns true if authenticateParentPassword is implemented
        and meaningful for this type of account system."""
        return 0

    def authenticateParentPassword(self, loginName,
                                   password, parentPassword):
        """
        try to authenticate the parent password
        """
        return (0, None)

    def supportsAuthenticateDelete(self):
        """ Returns true if authenticateDelete is implemented
        for this type of account system """
        return 0

    def enableSecretFriends(self, loginName, password,
                            parentPassword, enable=1):
        """
        try to enable secret friends
        """
        return (0, None)

    def __addTokenType(self, datagram):
        # We have a blue!
        datagram.addInt32(CLIENT_LOGIN_2_BLUE)

"""LoginGSAccount: Login using the original Game Server method"""

from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram


class LoginGSAccount(LoginBase.LoginBase):
    """This is the really old way toontown devs get into their local toontown environment."""
    
    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def createAccount(self, loginName, password, data):
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
        self.createFlag=1

        # Since we are faking a login here without using an account
        # server, we are just in the dev environment, and our account
        # is paid and never expires.
        self.cr.freeTimeExpiresAt = -1
        self.cr.setIsPaid(1)
        return None # no error.

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
        self.createFlag=0

        # Since we are faking a login here without using an account
        # server, we are just in the dev environment, and our account
        # is paid and never expires.
        self.cr.freeTimeExpiresAt = -1
        self.cr.setIsPaid(1)
        return None # no error.

    def supportsRelogin(self):
        """
        Returns true if this login interface supports logging in
        multiple different times.
        """
        return 1

    def sendLoginMsg(self):
        """
        Send a message to the server with our loginName
        """
        
        DISLID = config.GetInt('fake-DISL-PlayerAccountId',0)
        if not DISLID:
            NameStringId = ("DISLID_%s" % (self.loginName))
            DISLID = config.GetInt(NameStringId, 0)
        
        cr=self.cr
        # Time to send a login message
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_LOGIN)
        # Add login name
        datagram.addString(self.loginName)
        # Add our IP address
        
        if cr.connectMethod != cr.CM_HTTP:
            datagram.addUint32(cr.tcpConn.getAddress().getIp())
        else:
            # Actually, using the OpenSSL library we don't know our
            # own IP address.  But no one really cares anyway.
            datagram.addUint32(0)
        # Add the UDP port we will be listening on. (Bogus for now)
        datagram.addUint16(5150)
        # Add the Server Version ID
        datagram.addString(cr.serverVersion)
        # Add the dc file hash
        datagram.addUint32(cr.hashVal)
        # Add password
        datagram.addString(self.password)
        # Add create flag
        datagram.addBool(self.createFlag)
        # Add the download verification string.
        datagram.addString(cr.validateDownload)
        # And the magic word enable string.
        datagram.addString(cr.wantMagicWords)
        # And our dev fake DISL account ID
        datagram.addUint32(DISLID)
        # Whether or not to enable OTP_WHITELIST
        datagram.addString(config.GetString('otp-whitelist',"YES"))
        
        # Send the message
        cr.send(datagram)

    def resendPlayToken(self):
        """
        Resends our playToken to the game server while still logged
        on.  This is necessary when our playTaken has changed
        properties in-game, for instance when we enable chat.
        """
        # Here in the old login system, we don't bother to implement
        # this.
        return
    
    def requestPwdReminder(self, email=None, acctName=None):
        """
        Request a password-reminder email, given an email address OR
        account name. (unused arg should be None)
        Returns non-zero on success
        NOTE: this interface is for internal use and doesn't support this
        functionality. If it does support it in the future, this
        function should be modified
        """
        return 0

    def getAccountData(self, loginName, password):
        return 'Unsupported'

    # setParentPassword is not needed on this interface

    def supportsParentPassword(self):
        """Returns true if authenticateParentPassword is implemented
        and meaningful for this type of account system."""
        return 1

    def authenticateParentPassword(self, loginName,
                                   password, parentPassword):
        """
        try to authenticate the parent password
        """
        # This is just a stub that matches the user account password only.
        return ((password == parentPassword), None)

    def authenticateParentUsernameAndPassword(self, loginName,
                                   password, parentUsername, parentPassword):
        """
        try to authenticate the parent password
        """
        # This is just a stub that matches the user account password only.
        return ((password == parentPassword), None)    

    def supportsAuthenticateDelete(self):
        """ Returns true if authenticateDelete is implemented
        for this type of account system """
        return 1

    def authenticateDelete(self, loginName, password):
        """
        authenticate the deletion of a toon
        """
        # JAS (just another stub)
        # compare password to the login password
        return ((password == self.cr.password), None)

    def enableSecretFriends(self, loginName, password,
                            parentPassword, enable=1):
        """
        try to enable secret friends
        """
        # this is a stub function; matches the user account password only.
        return ((password == parentPassword), None)

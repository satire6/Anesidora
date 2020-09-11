"""LoginDISLTokenAccount: Login using a pre-supplied DISL token."""

from direct.showbase.ShowBaseGlobal import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram


class LoginDISLTokenAccount(LoginBase.LoginBase):
    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def supportsRelogin(self):
        """
        Returns true if this login interface supports logging in
        multiple different times.
        """
        return 0

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.DISLToken = password

    def sendLoginMsg(self):
        """
        Send a message to the server with our loginName
        """
        cr=self.cr
        # Time to send a login message
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_LOGIN_3)
        # Add the token
        datagram.addString(self.DISLToken)
        # Add the Server Version ID
        datagram.addString(cr.serverVersion)
        # Add the dc file hash
        datagram.addUint32(cr.hashVal)
        # Token type
        datagram.addInt32(CLIENT_LOGIN_3_DISL_TOKEN)
        # Add the download verification string.
        datagram.addString(cr.validateDownload)
        # And the magic word enable string.
        datagram.addString(cr.wantMagicWords)
        # Send the message
        cr.send(datagram)

    def supportsParentPassword(self):
        """Returns true if authenticateParentPassword is implemented
        and meaningful for this type of account system."""
        return 0

    def supportsAuthenticateDelete(self):
        """ Returns true if authenticateDelete is implemented
        for this type of account system """
        return 0

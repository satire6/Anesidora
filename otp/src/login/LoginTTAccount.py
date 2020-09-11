"""LoginTTAccount: Login using the Toontown Account Manager server"""

from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
import TTAccount
from TTAccount import TTAccountException
from direct.distributed.PyDatagram import PyDatagram


class LoginTTAccount(LoginBase.LoginBase, TTAccount.TTAccount):

    # Create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("LoginTTAcct")

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)
        TTAccount.TTAccount.__init__(self, cr)
        self.useTTSpecificLogin = base.config.GetBool('tt-specific-login', 0)
        self.notify.info('self.useTTSpecificLogin =%s' % self.useTTSpecificLogin)

    def supportsRelogin(self):
        """
        Returns true if this login interface supports logging in
        multiple different times.
        """
        return 1

    def sendLoginMsg(self):
        """
        Send a message to the game server with our playToken.
        """
        assert "playToken" in self.__dict__ # Hey, there's no playToken.
        #...no error code in the response, so we have a play token.
        cr=self.cr
        # Time to send a login message
        datagram = PyDatagram()
        # Add message type
        if self.useTTSpecificLogin:
            datagram.addUint16(CLIENT_LOGIN_TOONTOWN)
            self.__addPlayToken(datagram)
            # Add the Server Version ID
            datagram.addString(cr.serverVersion)
            # Add the dc file hash
            datagram.addUint32(cr.hashVal)
            self.__addTokenType(datagram)
            # Add the download verification string.
            # new version doesn't have this field
            # datagram.addString(cr.validateDownload)
            # And the magic word enable string.
            datagram.addString(cr.wantMagicWords)
        else:
            datagram.addUint16(CLIENT_LOGIN_2)
            self.__addPlayToken(datagram)
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
        assert self.response is not None
        assert not self.response.hasKey('errorMsg') # Hey, there was an error
        assert "playToken" in self.__dict__ # Hey, there's no playToken.
        #...no error code in the response, so we have a play token.
        cr=self.cr

        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_SET_SECURITY)
        self.__addPlayToken(datagram)
        self.__addTokenType(datagram)
        # Send the message
        cr.send(datagram)

    def __addPlayToken(self, datagram):
        # Adds the current playToken to the datagram to upload to the
        # server for sendLoginMsg() and resendPlayToken().

        # Strip off trailing newline
        assert hasattr(self, "playToken")
        self.playToken = self.playToken.strip()
        datagram.addString(self.playToken)

    def __addTokenType(self, datagram):
        # Adds the appropriate code to the datagram to tell the server
        # what type of playToken we have, for sendLoginMsg() and
        # resendPlayToken().
        if self.useTTSpecificLogin:
            # also known as TOKEN_TYPE_KIM_S in otp_server
            datagram.addInt32(CLIENT_LOGIN_3_DISL_TOKEN) 
        else:
            if self.playTokenIsEncrypted:
                datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN)
            else:
                # The game server doesn't yet understand this token type:
                #datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN_PLAIN)
                # Yes, this makes this if statement useless.
                datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN)
        

    # result-getters
    # these override default implementations in LoginBase
    # prefer using these over looking directly into 'response' in client code
    # these cannot be in TTAccount due to multiple-inheritance issues;
    # they would not override the LoginBase methods
    def getErrorCode(self):
        return self.response.getInt('errorCode', 0)
    def needToSetParentPassword(self):
        return self.response.getBool('secretsPasswordNotSet', 0)

    def authenticateParentPassword(self, loginName,
                                   password, parentPassword):
        """
        Authenticate the parent password, doing it correctly if he uses
        the new tt specific login or not
        """
        if base.cr.withParentAccount :
            self.notify.error("authenticateParentPassword called, but with parentAccount")
            try:
                errorMsg = self.talk(
                    'authenticateParentUsernameAndPassword',
                    data=self.makeLoginDict(loginName, parentPassword))
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
        else:
            if self.useTTSpecificLogin:
                try:
                    errorMsg = self.talk(
                        'authenticateParentPasswordNewStyle',
                        data=self.makeLoginDict(loginName, parentPassword))
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
            else:
                # old login_2 style just call to base clase
                return TTAccount.TTAccount.authenticateParentPassword(self, loginName,
                                       password, parentPassword)


    def authenticateDelete(self, loginName, password):
        """
        Authenticate the deleting with regular password, doing it correctly if he uses
        the new tt specific login or not
        """
        if self.useTTSpecificLogin :
            try:
                errorMsg = self.talk(
                    'authenticateDeleteNewStyle',
                    data=self.makeLoginDict(loginName, password))
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
        else:
            self.notify.info("using old style authenticate delete")
            result = TTAccount.TTAccount.authenticateDelete(self,loginName, password)
            return result

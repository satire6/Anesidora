"""LoginGSAccount: Login using the original Game Server method"""

from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginTTAccount
from direct.distributed.PyDatagram import PyDatagram
from TTAccount import TTAccountException

class LoginTTSpecificDevAccount(LoginTTAccount.LoginTTAccount):
    """This is a login that is meant to work only on a developer's local setup.

    This relies on the prebuilt otp_server.exe, at least version 1.319
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("LoginTTSpecificDevAccount")
    
    def __init__(self, cr):
        LoginTTAccount.LoginTTAccount.__init__(self, cr)

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
        # this is what roger expects the token to be:
        """
        TOONTOWN_ACCESS = NONE / VELVET_ROPE / FULL
        TOONTOWN_GAME_KEY = 
        WL_CHAT_ENABLED = Yes / No
        OPEN_CHAT_ENABLED = Yes /No
        CREATE_FRIENDS_WITH_CHAT=No/Code / Yes
        CHAT_CODE_CREATION_RULE=No/Parent/Yes s
        ACCOUNT_NUMBER = INT
        ACCOUNT_NAME = STRING (*may be temp, may change)
        ACCOUNT_NAME_APPROVED = BOOL  
        FAMILY_NUMBER=
        
        Deployment = same as old usage ß not sure you need this ..
        """
        cr=self.cr
        
        tokenString = ''
        # parse toontown access
        access = base.config.GetString('force-paid-status', '')
        if access == '':
            access = 'FULL'
        elif access == 'paid':
            access = 'FULL'
        elif access == 'unpaid':
            access = 'VELVET_ROPE'
        elif access == 'VELVET':
            access = 'VELVET_ROPE'
        else:
            self.notify.error("don't know what to do with force-paid-status %s" % access)
        # we must use '&' as separators not newline
        # and no spaces beside the equal sign
        tokenString += 'TOONTOWN_ACCESS=%s&' % access

        # what the heck is game key, looks like it's username
        tokenString += "TOONTOWN_GAME_KEY=%s&" % self.loginName

        # whitelist
        wlChatEnabled = 'YES'
        if base.config.GetString('otp-whitelist', 'YES') == 'NO':
            wlChatEnabled = 'NO'
        tokenString += 'WL_CHAT_ENABLED=%s &' % wlChatEnabled

        # parse open chat, well afaik we don't have any in toontown
        openChatEnabled = 'NO'
        if cr.openChatAllowed:
            openChatEnabled = 'YES'
        tokenString += 'OPEN_CHAT_ENABLED=%s&' % openChatEnabled

        # this looks like secret chat
        createFriendsWithChat = 'NO'
        if cr.allowSecretChat:
            createFriendsWithChat = 'CODE'        
        tokenString += 'CREATE_FRIENDS_WITH_CHAT=%s&' % createFriendsWithChat
        
        chatCodeCreationRule = 'No'
        if cr.allowSecretChat:
            if base.config.GetBool("secret-chat-needs-parent-password", 0):
                chatCodeCreationRule = 'PARENT'
            else:
                chatCodeCreationRule = 'YES'
        tokenString += 'CHAT_CODE_CREATION_RULE=%s&' % chatCodeCreationRule

        # at this point we don't know the account number
        DISLID = config.GetInt('fake-DISL-PlayerAccountId',0)
        if not DISLID:
            NameStringId = ("DISLID_%s" % (self.loginName))
            DISLID = config.GetInt(NameStringId, 0)
        
        tokenString += 'ACCOUNT_NUMBER=%d&' % DISLID # base.config.GetInt('new-account-number',100000002)

        # we do know username
        tokenString += 'ACCOUNT_NAME=%s&' % self.loginName
        tokenString += 'GAME_USERNAME=%s&' % self.loginName

        # I guess we just assume it's approved
        tokenString += 'ACCOUNT_NAME_APPROVED=TRUE&'

        #what the heck is family number
        tokenString += 'FAMILY_NUMBER=&'
        # assume us for now
        tokenString += 'Deployment=US&'        
        # flag if it's an account with a parent account
        withParentAccount = base.config.GetBool('dev-with-parent-account',0)
        if withParentAccount:
            tokenString += 'TOON_ACCOUNT_TYPE=WITH_PARENT_ACCOUNT&'
        else:
            tokenString += 'TOON_ACCOUNT_TYPE=NO_PARENT_ACCOUNT&'
        #and it need valid=true at the end
        tokenString += 'valid=true'

        #tokenString = base.config.GetString('faketoken','')
        
        self.notify.info("tokenString=\n%s" % tokenString)

        #import pdb; pdb.set_trace()
        # we'll cheat and just use the pirate token encryptor
        # and feed that into fake-playtoken in Config.prc
        # the correct way is to invoke $OTP/src/secure/make-playtoken.sh

        # Time to send a login message
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_LOGIN_TOONTOWN )
        

        # with no encryption, just use tokenstring
        playToken = tokenString
        
        
        # Add token
        datagram.addString(playToken)

        # add soft ver, hmm what the heck is that
        # looks like it should be dev, or probably a server version in live
        datagram.addString("dev")

        # Add the dc file hash, hope this is the dc version
        datagram.addUint32(cr.hashVal)

        # what the heck is token type, okay going throuch code, it must be 4 TOKEN_TYPE_KIM_S
        datagram.addUint32(4)

        # privilege string
        magicWords = base.config.GetString('want-magic-words','')
        datagram.addString(magicWords)



##         datagram.addString(self.loginName)
##         # Add our IP address
        
##         if cr.connectMethod != cr.CM_HTTP:
##             datagram.addUint32(cr.tcpConn.getAddress().getIp())
##         else:
##             # Actually, using the OpenSSL library we don't know our
##             # own IP address.  But no one really cares anyway.
##             datagram.addUint32(0)
##         # Add the UDP port we will be listening on. (Bogus for now)
##         datagram.addUint16(5150)
##         # Add the Server Version ID
##         datagram.addString(cr.serverVersion)
        
##         # Add password
##         datagram.addString(self.password)
##         # Add create flag
##         datagram.addBool(self.createFlag)
##         # Add the download verification string.
##         datagram.addString(cr.validateDownload)
##         # And the magic word enable string.
##         datagram.addString(cr.wantMagicWords)
##         # And our dev fake DISL account ID
##         datagram.addUint32(DISLID)
##         # Whether or not to enable OTP_WHITELIST
##         datagram.addString(config.GetString('otp-whitelist',"YES"))

        
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

##     def authenticateParentPassword(self, loginName,
##                                    password, parentPassword):
##         """
##         try to authenticate the parent password
##         """
##         # This is just a stub that matches the user account password only.
##         return ((password == parentPassword), None)

    def supportsAuthenticateDelete(self):
        """ Returns true if authenticateDelete is implemented
        for this type of account system """
        return 1

##     def authenticateDelete(self, loginName, password):
##         """
##         authenticate the deletion of a toon
##         """
##         # JAS (just another stub)
##         # compare password to the login password
##         return ((password == self.cr.password), None)

    def enableSecretFriends(self, loginName, password,
                            parentPassword, enable=1):
        """
        try to enable secret friends
        """
        # this is a stub function; matches the user account password only.
        return ((password == parentPassword), None)


    def needToSetParentPassword(self):
        """Hack to be able to login derived from LoginTTAccount."""
        return False



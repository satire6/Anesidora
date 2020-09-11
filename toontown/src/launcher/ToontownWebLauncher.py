import os
from otp.launcher.WebLauncherBase import WebLauncherBase
from toontown.toonbase import TTLocalizer
from pandac.PandaModules import *

# it's important to derive from WebLauncherBase first so that Python
# will find its methods before looking at the old launcher code.

class ToontownWebLauncher(WebLauncherBase):
    GameName = 'Toontown'

    LauncherPhases = [
        (3, 'tt_3'),
        (3.5, 'tt_3_5'),
        (4, 'tt_4'),
        (5, 'tt_5'),
        (5.5, 'tt_5_5'),
        (6, 'tt_6'),
        (7, 'tt_7'),
        (8, 'tt_8'),
        (9, 'tt_9'),
        (10, 'tt_10'),
        (11, 'tt_11'),
        (12, 'tt_12'),
        (13, 'tt_13'),
        ]
    
    Localizer = TTLocalizer

    def __init__(self, appRunner):
        WebLauncherBase.__init__(self, appRunner)
        self.http = HTTPClient.getGlobalPtr()
        
        # Before you go further, let's parse the web acct parameters
        self.webAcctParams = "WEB_ACCT_PARAMS"
        self.parseWebAcctParams()

        self.startDownload()

        # Used to pass to server for authentication
        self.toontownBlueKey = "TOONTOWN_BLUE"
        # Used to pass to server for authentication
        self.toontownPlayTokenKey = "TOONTOWN_PLAYTOKEN"
        # Used to communicate status back to the Updating Toontown flash movie
        self.launcherMessageKey = "LAUNCHER_MESSAGE"
        # Is the flash game1 done? (int 1 or 0)
        self.game1DoneKey = "GAME1_DONE"
        # Is the flash game2 done? (int 1 or 0)
        self.game2DoneKey = "GAME2_DONE"
        # Is the in-game 3d tutorial done? (int 1 or 0)
        self.tutorialCompleteKey = "TUTORIAL_DONE"

        # Start the game.
        from toontown.toonbase import ToontownStart

    def getAccountServer(self):
        return self.getValue('ACCOUNT_SERVER', '')

    def getNeedPwForSecretKey(self):
        return self.secretNeedsParentPasswordKey

    def getParentPasswordSet(self):
        """
        Get the parent password set key
        """
        # Everything is already parsed if parseWebAcctParams was called 
        return self.chatEligibleKey

    def setTutorialComplete(self):
        pass

    def getTutorialComplete(self):
        return False

    def getGame2Done(self):
        return True


    def parseWebAcctParams(self):
        """
        Parse the Web Account Params for chat related name-value pairs and store those
        in the launcher class. For security, this registry value is deleted after the
        first iteration. The client can then inquire PlayToken, ChatEligible etc.
        """
        # Allow a developer to stuff it in the config file if
        # necessary.
        s = ConfigVariableString("fake-web-acct-params", '').getValue()

        if not s:
            s = self.getValue(self.webAcctParams, '')
       
        # Parse the web account params to get chat related values
        # split s to the '&'
        l = s.split('&')
        length = len(l)

        # build a dictionary of the parameters
        dict = {}
        for index in range(0, len(l)):
            args = l[index].split('=')
            if len(args) == 3:
                # extra '=' on first entry: "webAccountParams=foo=1&..."
                name, value = args[-2:]
                dict[name] = int(value)
            elif len(args) == 2:
                name, value = args
                dict[name] = int(value)

        self.secretNeedsParentPasswordKey = 1                
        if dict.has_key('secretsNeedsParentPassword'):
            self.secretNeedsParentPasswordKey = 1 and dict['secretsNeedsParentPassword']
        else:
            self.notify.warning('no secretNeedsParentPassword token in webAcctParams')
        self.notify.info('secretNeedsParentPassword = %d' % self.secretNeedsParentPasswordKey)

        self.chatEligibleKey = 0
        if dict.has_key('chatEligible'):
            self.chatEligibleKey = 1 and dict['chatEligible']
        else:
            self.notify.warning('no chatEligible token in webAcctParams')
        self.notify.info('chatEligibleKey = %d' % self.chatEligibleKey)

    #============================================================
    # Interface of launcher to the rest of the game
    #============================================================

    def getBlue(self):
        """
        Get the blue out of the registry and return it.  The blue is
        not saved; if this method is called a second time it will
        return None.
        """
        blue = self.getValue(self.toontownBlueKey)
        # Immediately clear out the blue so it will be more
        # difficult for a hacker to pull it out of the registry.
        self.setValue(self.toontownBlueKey, "")

        if blue == "NO BLUE":
            blue = None
        return blue

    def getPlayToken(self):
        """
        Get the PlayToken out of the registry and return it.  The
        PlayToken is not saved; if this method is called a second
        time it will return None.
        """
        playToken = self.getValue(self.toontownPlayTokenKey)
        # Immediately clear out the PlayToken so it will be more
        # difficult for a hacker to pull it out of the registry.
        self.setValue(self.toontownPlayTokenKey, "")

        if playToken == "NO PLAYTOKEN":
            playToken = None
        return playToken

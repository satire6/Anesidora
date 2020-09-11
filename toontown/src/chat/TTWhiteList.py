import os
from pandac.PandaModules import *
from direct.showbase import AppRunnerGlobal
from otp.chat.WhiteList import WhiteList
from toontown.toonbase import TTLocalizer

class TTWhiteList(WhiteList):
    def __init__(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('twhitelist.dat')
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            # In the web-publish runtime, it will always be here:
            searchPath.appendDirectory(Filename.expandFrom('$TT_3_ROOT/phase_3/etc'))
        else:
            # In other environments, including the dev environment, look here:
            searchPath.appendDirectory(Filename('.'))
            searchPath.appendDirectory(Filename('etc'))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TOONTOWN/src/chat')))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('toontown/src/chat')))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('toontown/chat')))
        found = vfs.resolveFilename(filename,searchPath)
        if not found:
            print "Couldn't find whitelist data file!"

        data = vfs.readFile(filename, 1)

        lines = data.split("\n")

        WhiteList.__init__(self,lines)
        self.defaultWord = TTLocalizer.ChatGarblerDefault[0]

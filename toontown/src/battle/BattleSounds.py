from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import AppRunnerGlobal
import os

## BattleSounds exists as a separate audiomanager from the default one in Showbase.py
## so we can completely flush battle sounds when we go to areas that battles
## cannot occur. (see globalBattleSoundCache.clear() in TownLoader.py)
##
## might be simpler to use 1 audio manager so you have only 1 set if audio settings, but
## you could add tagged sounds so all the 'battle'-tagged sounds could be flushed from the 
## cache at once.  cache size might need to be increased in  battle areas though

class BattleSounds:
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleSounds')
  
    def __init__(self):
        assert(self.notify.debug("__init__()"))
        self.mgr = AudioManager.createAudioManager()
        self.isValid=0
        if self.mgr != None and self.mgr.isValid():
            self.isValid=1
            limit = base.config.GetInt('battle-sound-cache-size', 15)
            self.mgr.setCacheLimit(limit)

            # make sure user sound settings are applied to this snd manager
            base.addSfxManager(self.mgr)

            self.setupSearchPath()

    def setupSearchPath(self):
        """ Sets self.sfxSearchPath with the appropriate search path
        to find battle sound effects. """
        
        self.sfxSearchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            # In the web-publish runtime, look here:
            self.sfxSearchPath.appendDirectory(Filename.expandFrom('$TT_3_ROOT/phase_3/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename.expandFrom('$TT_3_5_ROOT/phase_3.5/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename.expandFrom('$TT_4_ROOT/phase_4/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename.expandFrom('$TT_5_ROOT/phase_5/audio/sfx'))
        else:
            # In other environments, including the dev environment, look here:
            self.sfxSearchPath.appendDirectory(Filename('phase_3/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename('phase_3.5/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename('phase_4/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename('phase_5/audio/sfx'))
            self.sfxSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TTMODELS/built/phase_3/audio/sfx')))
            self.sfxSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TTMODELS/built/phase_3.5/audio/sfx')))
            self.sfxSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TTMODELS/built/phase_4/audio/sfx')))
            self.sfxSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TTMODELS/built/phase_5/audio/sfx')))
        

    def clear(self):
        assert(self.notify.debug("clear()"))
        if self.isValid:
            self.mgr.clearCache()

    def getSound(self, name):
        assert(self.notify.debug("getSound(name=%s)"%(name)))
        if self.isValid:
            filename = Filename(name)
            found = vfs.resolveFilename(filename, self.sfxSearchPath)

            if not found:
                # If it wasn't found, try once more to reset the
                # search path.  Maybe the first time we set it, we
                # didn't have all of the phases loaded yet.
                self.setupSearchPath()
                found = vfs.resolveFilename(filename, self.sfxSearchPath)

            if not found:
                # If it's still not found, something's wrong.
                self.notify.warning('%s not found on:' % name)
                print self.sfxSearchPath
                
            else:
                return self.mgr.getSound(filename.getFullpath())

        return self.mgr.getNullSound()

globalBattleSoundCache = BattleSounds()
    

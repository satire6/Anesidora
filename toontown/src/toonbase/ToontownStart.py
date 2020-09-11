# This is the file that gets imported by the Launcher as soon as phase 3 is
# complete. This will happen once during the install/download process as soon
# as phase 3 is finished downloading. When the Launcher is run after the
# download/install is complete, it will import this file after realizing
# phase 3 is already complete.
#
#
# Note: you can run this standalone by letting the launcher default to None
#   from toontown.toonbase.ToontownStart import *
# 


# This module redefines the builtin import function with one
# that prints out every import it does in a hierarchical form
# Annoying and very noisy, but sometimes useful
# import VerboseImport

import __builtin__

class game:
    name = "toontown"
    process = "client"
__builtin__.game = game()

import time
import os
import sys
import random
# Need to import __builtin__ and use the __builtin__.foo = x
# technique here in case you start toontown from the command line
import __builtin__

# See if we have a launcher, if we do not, make an empty one
try:
    launcher
except:
    from toontown.launcher.ToontownDummyLauncher import ToontownDummyLauncher
    launcher = ToontownDummyLauncher()
    __builtin__.launcher = launcher


# Default to "normal" web exit page.  This should be set early
# so that the right thing will get done on a crash.  "normal"
# may be marketting info, thanks for playing, or the report
# bug page.  The installer.php file will use this setting.
launcher.setRegistry("EXIT_PAGE", "normal")

# The first thing we need to do is make sure the Flash intro is not playing
# If it is, we need to wait here until it is done. We check to see if it is
# done by asking the Launcher.

pollingDelay = 0.5

print 'ToontownStart: Polling for game2 to finish...'
while (not launcher.getGame2Done()):
    time.sleep(pollingDelay)
print 'ToontownStart: Game2 is finished.'

# Ok, now we know we are clear from the flash into, fire it up
print 'ToontownStart: Starting the game.'

from pandac.PandaModules import *

if launcher.isDummy():
    # Create a dummy HTTPClient so we can get that stupid openSSL
    # random seed computed before we attempt to open the window.  (We
    # only need do this if we don't have a launcher.  If we do have a
    # launcher, it's already been created.)
    http = HTTPClient()
else:
    http = launcher.http

# Preload the background scene before the window is even created
tempLoader = PandaLoader()
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background'))

from direct.gui import DirectGuiGlobals
print 'ToontownStart: setting default font'
import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)

# First open a window so we can show the loading screen

# Set the error code indicating failure opening a window in case we
# crash while opening it (the GSG code will just exit if it fails to
# get the window open).
launcher.setPandaErrorCode(7)

# Make sure we create a ToonBase first
import ToonBase
ToonBase.ToonBase()
from pandac.PandaModules import *
if (base.win == None):
    print "Unable to open window; aborting."
    sys.exit()

# Ok, we got the window open.
launcher.setPandaErrorCode(0)
# Tell the launcher that our panda window is open now so
# it can tell the browser and flash to shutdown
launcher.setPandaWindowOpen()

# Also, once we open the window, dramatically drop the timeslice
# for decompressing and extracting files, so we don't interfere
# too much with rendering.
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)

# Now put the background node under render
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
# Set the draw order explicitly
backgroundNodePath.find("**/fg").setBin('fixed', 20)
backgroundNodePath.find("**/bg").setBin('fixed', 10)
# Let a frame render so we can see the background
base.graphicsEngine.renderFrame()

# do the quest sanity check
if __debug__:
    if base.config.GetBool('quest-sanity-check',0):
        from toontown.quest import Quests
        Quests.assertAllQuestsValid()

DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx("phase_3/audio/sfx/GUI_rollover.mp3"))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx("phase_3/audio/sfx/GUI_create_toon_fwd.mp3"))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))

# Set default product prefix
import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)

# Play music at startup
# This is a bit strange because the music is created here, then
# handed off to the cr to control. This is done so keep the music
# from skipping (if we stopped it and restarted it).
if base.musicManagerIsValid:
    music = base.musicManager.getSound("phase_3/audio/bgm/tt_theme.mid")
    if music:
        music.setLoop(1)
        music.setVolume(0.9)
        music.play()
    # Update default sound
    print 'ToontownStart: Loading default gui sounds'
    DirectGuiGlobals.setDefaultRolloverSound(
        base.loadSfx("phase_3/audio/sfx/GUI_rollover.mp3"))
    DirectGuiGlobals.setDefaultClickSound(
        base.loadSfx("phase_3/audio/sfx/GUI_create_toon_fwd.mp3"))
else:
    music = None


import ToontownLoader

# tempLoaderOther = ToontownLoader.ToontownLoader(base)
# base.loader = tempLoaderOther
# __builtin__.loader = tempLoaderOther

from direct.gui.DirectGui import *

serverVersion = base.config.GetString("server-version", "no_version_set")
print 'ToontownStart: serverVersion: ', serverVersion
version = OnscreenText(serverVersion,
                       pos = (-1.3, -0.975),
                       scale = 0.06,
                       fg = Vec4(0,0,1,0.6),
                       align = TextNode.ALeft
                       )

# Now fire up toon base
loader.beginBulkLoad("init", TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE)
from ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *    

from toontown.distributed import ToontownClientRepository

# Start up the client repository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)

# Hand off the music to the TCR
cr.music = music
del music

base.initNametagGlobals()

# Save cr for debugging
base.cr = cr

loader.endBulkLoad("init")



#
# special Setup for A Global Friend Manager
#
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *

cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, "FriendManager")

# Start the show
if not launcher.isDummy():
    # If the launcher is starting us, it knows the game server
    # because it is passed in on the url
    base.startShow(cr, launcher.getGameServer())
else:
    base.startShow(cr)
    

# Now get rid of the background and the temp loader
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
# tempLoaderOther.destroy()
# del tempLoaderOther
version.cleanup()
del version

# replace the direct loader with the toontown one
base.loader = base.loader
__builtin__.loader = base.loader

autoRun = ConfigVariableBool('toontown-auto-run', 1)

if autoRun and launcher.isDummy():
    # This try .. except block exists solely to test the logic of
    # PythonUtil.describeException.  It's not at all necessary, and is
    # useful only to those debugging that function; remove it if it
    # bugs you.
    try:
        run()

    except SystemExit:
        raise

    except:
        from direct.showbase import PythonUtil
        print PythonUtil.describeException()
        raise

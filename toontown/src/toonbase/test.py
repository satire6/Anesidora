#
#imports
#
from pandac.PandaModules import *
from otp.avatar import Avatar
from otp.avatar import AvatarDNA
from direct.task import Task
from direct.showbase.MessengerGlobal import *
import sys
from pandac.PandaModules import ClockObject
from pandac.PandaModules import PStatClient
from ChatManagerGlobal import *
#
# globals
#
connected = 0
pStats = PStatClient().getGlobalPstats()
startTime = 0.0
startFrameCount = 0
globalClock = ClockObject.getGlobalClock()

#
# viewpoint list
#
vpl = (
        (Point3(-10.5, 20.3, 5.6), VBase3(-153., -14., 0.)),
        (Point3(-45., -0.3, -0.8), VBase3(-90., -4., 0.)),
        (Point3(-74.4, -46.4, 6.5), VBase3(-58., -5.8, 0.)),
        (Point3(127.7, -74., 5.), VBase3(60.5, -4.6, 0.)),
        (Point3(66.3, 62.7, 6.95), VBase3(83.0, 0., 0.))
      )
#
# load the environment
#
tt = loader.loadModel("phase_4/models/neighborhoods/toontown_central")
tt.reparentTo(render)
#
# load the avatars
#
dna1 = AvatarDNA.AvatarDNA()
dna1.newToon(("dll", "md", "l", "m"), 0.3, 0.2, 0.4)
av1 = Avatar.Avatar()
av1.setDNA(dna1)
av1.setPos(-3.0, 0.0, 1.75)
av1.setH(-90.0)
av1.loop("neutral")
av1.reparentTo(render)
dna2 = AvatarDNA.AvatarDNA()
dna2.newToon(("css", "ss", "s", "f"), 0.4, 0.2, 0.2)
av2 = Avatar.Avatar()
av2.setDNA(dna2)
av2.setPos(3.0, 0.0, 1.75)
av2.setH(90.0)
av2.loop("neutral")
av2.reparentTo(render)
#
# keyboard handling routines
#
#
# "ESC" - exit
#
def handleEscKey():
        if (pStats.isConnected()):
                print "disconnecting from PStatClient"
                pStats.disconnect()
        print "bye!"
        sys.exit()
#
# "1" - lerp to viewpoint #1
#
def handle1Key():
        base.disableMouse()
        camera.setPosHpr(vpl[0][0], vpl[0][1])
        print "viewpoint 1"
#
# "2" - lerp to viewpoint #2
#
def handle2Key():
        base.disableMouse()
        camera.setPosHpr(vpl[1][0], vpl[1][1])
        print "viewpoint 2"
#
# "3" - lerp to viewpoint #3
#
def handle3Key():
        base.disableMouse()
        camera.setPosHpr(vpl[2][0], vpl[2][1])
        print "viewpoint 3"
#
# "4" - lerp to viewpoint #4
#
def handle4Key():
        base.disableMouse()
        camera.setPosHpr(vpl[3][0], vpl[3][1])
        print "viewpoint 4"
#
# "5" - lerp to viewpoint #4
#
def handle5Key():
        base.disableMouse()
        camera.setPosHpr(vpl[4][0], vpl[4][1])
        print "viewpoint 5"
#
# "t" - trackball mode
#
def handleTKey():
        print "using trackball mode..."
        base.useTrackball()
#
# "m" - mouse mode
#
def handleDKey():
        print "using drive mode..."
        base.useDrive()
#
# "p" - print the camera position
#
def handlePKey():
        print "camera pos:"
        camera.printPos()
        camera.printHpr()
#
# "s" - toggle connection to stats
#
def handleSKey():
        if (pStats.isConnected()):
                print "disconnecting from PStatClient"
                pStats.disconnect()
        else:
                print "connecting to PStatClient"
                pStats.connect()
#
# "f" - print the frame rate
#
def handleFKey():
        global startTime
        global frameCount
        time = globalClock.getFrameTime()
        dt = time - startTime
        frameCount = globalClock.getFrameCount()
        df = frameCount - startFrameCount
        if (df > 0):
                print df, " frames in ", dt, "seconds"
                print df/dt, " fps avg. (", 1000.0/(df/dt), "ms)"
#
# "a" - automatically lerp through viewpoint list
#
def handleAKey():
        print "starting viewpoint lerps..."
        base.disableMouse()
        camera.setPosHpr(vpl[0][0], vpl[0][1])
        lerpTimeline = Task.timeline(
                        (2.0,  
                         camera.lerpPosHpr(vpl[1][0], vpl[1][1], 1.0),
                         "lerp1"),
                        (5.0,
                         camera.lerpPosHpr(vpl[2][0],vpl[2][1], 2.0),
                         "lerp2"),
                        (9.0,
                         camera.lerpPosHpr(vpl[3][0], vpl[3][1], 3.0),
                         "lerp3"),
                        (14.0, 
                         camera.lerpPosHpr(vpl[4][0], vpl[4][1], 4.0),
                         "lerp4"))

        taskMgr.add(lerpTimeline, "lerpTimeline")


#
# spawn events to look for keyStrokes
#
messenger.accept("a-up", 1, handleAKey, [], 1)
messenger.accept("f-up", 1, handleFKey, [], 1)
messenger.accept("d-up", 1, handleDKey, [], 1)
messenger.accept("t-up", 1, handleTKey, [], 1)
messenger.accept("s-up", 1, handleSKey, [], 1)
messenger.accept("d-up", 1, handleDKey, [], 1)
messenger.accept("p-up", 1, handlePKey, [], 1)
messenger.accept("1-up", 1, handle1Key, [], 1)
messenger.accept("2-up", 1, handle2Key, [], 1)
messenger.accept("3-up", 1, handle3Key, [], 1)
messenger.accept("4-up", 1, handle4Key, [], 1)
messenger.accept("5-up", 1, handle5Key, [], 1)
messenger.accept("escape-up", 1, handleEscKey, [], 1)


# start the igLoop
base.disableMouse()
camera.setPosHpr(vpl[0][0], vpl[0][1])
chatMgr.stop()
globalClock.tick()
startTime = globalClock.getFrameTime()
startFrameCount = globalClock.getFrameCount()
run()















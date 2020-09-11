from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.task.Task import Task
from direct.directnotify import DirectNotifyGlobal

notify = DirectNotifyGlobal.directNotify.newCategory("SkyUtil")
    
def cloudSkyTrack(task):
    # Every frame nail the sky to 0, with no rotation
    # Actually we can raise the sky to the lowest point
    # on the horizon since you will not be able to see
    # over or between buildings. Drawing part of the sky
    # that will always be behind buildings is wasteful.
    # DL has some 10 foot fences, so the highest we can
    # currently put the sky is at 10 feet.
    # Actually, the tag minigame uses the sky now, and wants
    # it at 0.0, so until we have real artwork there, just
    # keep it at 0
    # Rotate the sky slowly to simulate clouds passing
    task.h += (globalClock.getDt() * 0.25)
    
    if task.cloud1.isEmpty() or task.cloud2.isEmpty():
        notify.warning("Couln't find clouds!")
        return Task.done
    
    task.cloud1.setH(task.h)
    task.cloud2.setH(-task.h * 0.8)
    return Task.cont

def startCloudSky(hood, parent=camera, effects = CompassEffect.PRot | CompassEffect.PZ):
    # Parent the sky to our camera, the task will counter rotate it
    hood.sky.reparentTo(parent)
    # Turn off depth tests on the sky because as the cloud layers interpenetrate
    # we do not want to see the polys cutoff. Since there is nothing behing them
    # we can get away with this.
    hood.sky.setDepthTest(0)
    hood.sky.setDepthWrite(0)
    hood.sky.setBin("background", 100)
    # Make sure they are drawn in the correct order in the hierarchy
    # The sky should be first, then the clouds
    hood.sky.find("**/Sky").reparentTo(hood.sky, -1)

    # Nowadays we use a CompassEffect to counter-rotate the sky
    # automatically at render time, rather than depending on a
    # task to do this just before the scene is rendered.
    hood.sky.reparentTo(parent)
    hood.sky.setZ(0.0)
    hood.sky.setHpr(0.0, 0.0, 0.0)
    ce = CompassEffect.make(NodePath(), effects)
    hood.sky.node().setEffect(ce)

    # Even with the CompassEffect, we still need the task to spin
    # the clouds.

    skyTrackTask = Task(hood.skyTrack)
    # Store the clouds and h value so the task has access to it
    skyTrackTask.h = 0
    skyTrackTask.cloud1 = hood.sky.find("**/cloud1")
    skyTrackTask.cloud2 = hood.sky.find("**/cloud2")

    if (not skyTrackTask.cloud1.isEmpty()) and (not skyTrackTask.cloud2.isEmpty()):
        taskMgr.add(skyTrackTask, "skyTrack")
    else:
        notify.warning("Couln't find clouds!")
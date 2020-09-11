# Go to your estate, then run this code.
# You will want this set in your Configrc so the fake desktop is high-res
# max-texture-dimension 1024

# To make Panda run always on bottom
# fullscreen 0
# # Leave room for the windows task bar (32 pixels high)
# win-size 1600 1168
# undecorated 1
# z-order bottom


from pandac.PandaModules import *

background = loader.loadModel('phase_3/models/gui/loading-background').find("**/bg")
background.reparentTo(render)

# Fake desktop texture
background.setTexture(loader.loadTexture('/c/desktop.jpg'), 1)
background.setColor(1,1,1,1)

# Plain colored cyan like default Windows desktop
# background.setTextureOff(1)
# background.setColor(0.25,0.5,0.5)

background.reparentTo(camera)
background.setPosHpr(0,100,0,0,0,0)
background.setScale(40*1.333, 1, 40)

base.localAvatar.stopLookAround()
base.localAvatar.stopUpdateSmartCamera()
camera.reparentTo(render)
camera.setPosHpr(0,0,12,0,0,0)
base.localAvatar.setPosHpr(0,30,0,0,0,0)
base.localAvatar.useLOD(1000)

render.find("**/Estate").stash()
render.setFogOff()
taskMgr.remove('estate-check-toon-underwater')
taskMgr.remove('estate-check-cam-underwater')

base.localAvatar.book.hideButton()
base.localAvatar.laffMeter.stop()
base.localAvatar.setFriendsListButtonActive(0)
NametagGlobals.setMasterNametagsActive(0)
NametagGlobals.setMasterArrowsOn(0)

from toontown.toon import Toon
from toontown.toon import ToonDNA
import random

toonList = []
for i in range(5):
    t = Toon.Toon()
    d = ToonDNA.ToonDNA()
    d.newToonRandom()
    t.setDNA(d)
    t.loop('neutral')
    t.reparentTo(render)
    t.setPosHpr((random.random() * 20.0) - 10.0, 40, 0, 150.0 + (random.random()*60), 0, 0)
    t.useLOD(1000)
    toonList.append(t)

for i in range(len(toonList)):
    t = toonList[i]
    t.setPosHpr((i * 5.0) - 10.0, 32 + random.random() * 5.0, -0.25, 120.0 + (random.random()*90), 0, 0)
    

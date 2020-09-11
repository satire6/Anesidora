from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

dayMusic = loader.loadMusic("phase_4/audio/bgm/TC_nbrhood.mid")
# dayMusic = loader.loadMusic("phase_8/audio/bgm/TB_nbrhood.mid")
# base.cr.playGame.hood.loader.snow.cleanup()
nightMusic = loader.loadMusic("phase_8/audio/bgm/DL_nbrhood.mid")

# Load up some sfx
birdSfx1 = loader.loadSfx("phase_8/audio/sfx/SZ_DG_bird_01.mp3")
birdSfx2 = loader.loadSfx("phase_8/audio/sfx/SZ_DG_bird_02.mp3")
birdSfx3 = loader.loadSfx("phase_8/audio/sfx/SZ_DG_bird_03.mp3")
cricket1 = loader.loadSfx("/c/soundelux/Estate_Cricket_1.mp3")
cricket2 = loader.loadSfx("/c/soundelux/Estate_Cricket_2.mp3")
rooster = loader.loadSfx("/c/soundelux/Estate_rooster.mp3")

# No more tt birds chirping
taskMgr.remove("TT-birds")
# Get rid of the sky that comes with TT central
taskMgr.remove("skyTrack")
base.cr.playGame.hood.sky.hide()
base.cr.playGame.hood.loader.music.stop()

# Load up our own sky models
nightSky = loader.loadModel("phase_8/models/props/DL_sky")
nightSky.setScale(0.8)
nightSky.setTransparency(1)
nightSky.setBin("background", 102)
daySky = loader.loadModel("phase_3.5/models/props/TT_sky")
daySky.setBin("background", 100)
dayCloud1 = daySky.find("**/cloud1")
dayCloud2 = daySky.find("**/cloud2")
dayCloud1.setBin("background", 101)
dayCloud2.setBin("background", 101)
dawnSky = loader.loadModel("phase_6/models/props/MM_sky")
dawnSky.setScale(0.8)
dawnSky.setTransparency(1)
dawnSky.setBin("background", 102

pe = PolylightEffect.make()
brightness = 1.25
darkness = 0.8
pe.setWeight(brightness)
base.localAvatar.node().setEffect(pe)


for sky in (nightSky, daySky, dawnSky):
    sky.reparentTo(camera)
    sky.setZ(0.0)
    sky.setHpr(0.0, 0.0, 0.0)
    ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
    sky.node().setEffect(ce)
    sky.setDepthTest(0)
    sky.setDepthWrite(0)

# Color scale defines
dawnColor = Vec4(1,0.8,0.4,1)
dayColor = Vec4(1,1,1,1)
duskColor = Vec4(0.8,0.4,0.7,1)
nightColor = Vec4(0.3,0.3,0.5,1)
onAlpha = Vec4(1,1,1,1)
offAlpha = Vec4(1,1,1,0)

# Geom of the hood
geom = base.cr.playGame.hood.loader.geom

# List of butterflies
butterflies = base.cr.doFindAll("DistributedButterfly")

# List of lamps and glow discs
oneLights = geom.findAllMatches("**/prop_post_one_light_DNARoot")
threeLights = geom.findAllMatches("**/prop_post_three_light_DNARoot")
lamps = oneLights + threeLights
discs = []

# List of NodePaths of PolylightNodes
polylights = []
lightIndex = 0


for lamp in oneLights:
    lamp.setColorScale(1,1,1,1,1)
    disc = loader.loadModel("phase_3.5/models/props/glow")
    # Add PolylightNodes
    lightIndex += 1
    plNode = PolylightNode("pl" + str(lightIndex))
    plNode.setRadius(20)
    #plNode.setPos(0,0,2)
    plNode.setColor(1.0,0.8,0.4)
    plNode.setFlickerType(PolylightNode.FSIN)
    plNode.setFreq(6.0)
    plNode.setOffset(-0.5)
    plNodePath = NodePath(plNode)
    polylights.append(plNodePath)
    base.localAvatar.node().setEffect(base.localAvatar.node().getEffect(PolylightEffect.getClassType()).addLight(plNodePath))


    # A glow around the lamp light bulb

    disc.setBillboardPointEye()
    disc.setPos(0.2,-1,10)
    disc.setScale(8)
    disc.setColorScale(1,1,0.8,0.25,1)
    disc.setTransparency(1)
    disc.reparentTo(lamp.find("**/p13"))
    #disc.node().setEffect(pe)
    discs.append(disc)
    # A glow on the floor
    disc = loader.loadModel("phase_3.5/models/props/glow")
    disc.setPos(0,0,0.025)
    disc.setHpr(0,90,0)
    disc.setScale(14)
    disc.setColorScale(1,1,0.8,0.25,1)
    disc.setTransparency(1)
    disc.reparentTo(lamp.find("**/p13"))
    plNodePath.reparentTo(disc)
    disc.node().setEffect(pe)
    discs.append(disc)


for lamp in threeLights:
    lamp.setColorScale(1,1,1,1,1)
    disc = loader.loadModel("phase_3.5/models/props/glow")
    # Add PolylightNodes
    lightIndex += 1
    plNode = PolylightNode("pl" + str(lightIndex))
    plNode.setRadius(20)
    plNode.setColor(1.0,1.0,1.0)
    plNode.setFlickerType(PolylightNode.FRANDOM)
    #plNode.setFreq(6.0)
    plNode.setOffset(-0.5)
    plNode.setScale(0.2)
    plNode.setAttenuation(PolylightNode.AQUADRATIC)
    plNodePath = NodePath(plNode)
    polylights.append(plNodePath)
    base.localAvatar.node().setEffect(base.localAvatar.node().getEffect(PolylightEffect.getClassType()).addLight(plNodePath))


    disc.setBillboardPointEye()
    disc.setPos(0,-1,10)
    disc.setScale(10)
    disc.setColorScale(1,1,0.8,0.25,1)
    disc.setTransparency(1)
    disc.reparentTo(lamp.find("**/p23"))
    plNodePath.reparentTo(disc)
    #disc.node().setEffect(pe)
    discs.append(disc)
    # A glow on the floor
    disc = loader.loadModel("phase_3.5/models/props/glow")
    disc.setPos(0,0,0.025)
    disc.setHpr(0,90,0)
    disc.setScale(14)
    disc.setColorScale(1,1,0.8,0.2,1)
    disc.setTransparency(1)
    disc.reparentTo(lamp.find("**/p23"))
    #disc.node().setEffect(pe)
    discs.append(disc)

def makeNight():
    for lamp in lamps:
        lamp.setColorScale(1,1,1,1,1)
    for disc in discs:
        disc.show()
    base.playSfx(cricket1, volume=0.3)
    dayMusic.stop()
    base.playMusic(nightMusic, volume=0.5)
    for b in butterflies:
        b.butterflyNode.hide()
    

def makeDay():
    for lamp in lamps:
        lamp.clearColorScale()
    for disc in discs:
        disc.hide()
    base.playSfx(rooster, volume=0.2)
    nightMusic.stop()
    base.playMusic(dayMusic, volume=0.7)
    for b in butterflies:
        b.butterflyNode.show()

def lerpDaySkyFunc(color):
    daySky.setColorScale(color, 1)

def lerpDawnSkyFunc(color):
    dawnSky.setColorScale(color, 1)

def lerpNightSkyFunc(color):
    nightSky.setColorScale(color, 1)

def lerpLightWeightFunc(weight):
    base.localAvatar.node().setEffect(base.localAvatar.node().getEffect(PolylightEffect.getClassType()).setWeight(weight))

# Change this to change the day/night cycle length
t = 120.0
tSeg = t / 10.0
dayMusic.stop()
nightMusic.stop()
nightSky.setColorScale(onAlpha)
daySky.setColorScale(offAlpha)
dawnSky.setColorScale(offAlpha)
render.setColorScale(nightColor)
i = Parallel(Sequence(Parallel(LerpColorScaleInterval(render, tSeg, dawnColor),
                               LerpFunctionInterval(lerpLightWeightFunc, duration=tSeg, toData=darkness, fromData=brightness),
                               LerpFunctionInterval(lerpNightSkyFunc, duration=tSeg, toData=offAlpha, fromData=onAlpha),
                               LerpFunctionInterval(lerpDawnSkyFunc, duration=tSeg, toData=onAlpha, fromData=offAlpha),
                               ),
                      Func(makeDay),
                      Wait(tSeg),
                      Parallel(LerpFunctionInterval(lerpDawnSkyFunc, duration=tSeg, toData=offAlpha, fromData=onAlpha),
                               LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=dayColor, fromData=offAlpha),
                               LerpColorScaleInterval(render, tSeg, dayColor),
                               ),
                      Func(base.playSfx, birdSfx1, 0, 1, 0.3),
                      Wait(tSeg),
                      Func(base.playSfx, birdSfx2, 0, 1, 0.3),
                      Parallel(LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=duskColor, fromData=dayColor),
                               LerpColorScaleInterval(render, tSeg, duskColor),
                               LerpFunctionInterval(lerpLightWeightFunc, duration=tSeg, toData=brightness, fromData=darkness),
                               ),
                      Func(makeNight),
                      Parallel(LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=offAlpha, fromData=duskColor),
                               LerpFunctionInterval(lerpNightSkyFunc, duration=tSeg, toData=onAlpha, fromData=offAlpha),
                               LerpColorScaleInterval(render, tSeg, nightColor),
                               ),
                      Func(base.playSfx, cricket2, 0, 1, 0.2),
                      Wait(tSeg),
                      Func(base.playSfx, cricket1, 0, 1, 0.2),
                      Wait(tSeg),
                      ),
             )
i.loop()



"""
# To undo
i.finish()
render.clearColorScale()
dayMusic.stop()
nightMusic.stop()
"""

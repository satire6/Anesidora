from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from BattleSounds import *
from toontown.toon.ToonDNA import *
from toontown.suit.SuitDNA import *
from direct.particles.ParticleEffect import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *

import MovieUtil
import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import BattleParticles
from toontown.toonbase import ToontownGlobals
import RewardPanel

notify = DirectNotifyGlobal.directNotify.newCategory('Fanfare')

"""
    Fanfare is centered around a given toon.  It causes two trumpets
    to appear and play some music, as well as a ball of confetti to show,
    open, and shower the toon with confetti.  A message box can then
    appear, showing text and an image.
    
    The message box is initially hidden
"""

###############################################################
# methods used to set up the message panel
###############################################################
# main panel, this is also where the toon's name shows up

"""
        NOTE: The message panel is initially hidden.
"""
def makePanel(toon, showToonName):
    panel = DirectFrame(relief=None, geom=DGG.getDefaultDialogGeom(),
                              geom_color=ToontownGlobals.GlobalDialogColor,
                              geom_scale = (1.75, 1, 0.75), pos = (0, 0, 0.587))
    
    panel.initialiseoptions(RewardPanel)
    panel.setTransparency(1)
    panel.hide()
    
    if showToonName is 1:
        panel.avNameLabel = DirectLabel(
                parent = panel,
                relief = None,
                pos = Vec3(0, 0, 0.3),
                text = toon.getName(),
                text_scale = 0.08,
                )
    return panel

# where a little text message can be placed, parented to the above frame
def makeMessageBox(panel, message, messagePos, messageScale, wordwrap = 100):
    panel.itemFrame = DirectFrame(
            parent = panel,
            relief = None,
            text = message,
            text_pos = messagePos,
            text_scale = messageScale,
            text_wordwrap = wordwrap
            )

# where an image can be placed, parented to the above itemFrame
def makeImageBox(frame, image, imagePos, imageScale):
    frame.imageIcon = image.copyTo(frame)
    frame.imageIcon.setPos(imagePos)
    frame.imageIcon.setScale(imageScale)

###############################################################
# public methods to be called by other classes
# returns an interval that has the partyBall, trumpets, and confetti,
# and a RewardPanel that can be manipulated however the caller wishes
# this was done in case the RewardPanel is intended to be shown
# to just the fanfare'd toon, or to all toons around them.
###############################################################

# this just does a Fanfare with no message box
def makeFanfare(delay, toon):
    return doFanfare(delay, toon, None)

# example of call from another class
#Fanfare.makeFanfareWithMessageImage(0, base.localAvatar, 1, "This is the message", Vec2(0,0.2), 
                            #0.08, base.localAvatar.inventory.buttonLookup(1, 1), Vec3(0,0,0), 4)
    
# this does a Fanfare and brings up a box with a message. 
# user specifies what, where and how big the message is 
# messagePos of Vec2(0,.2) and messageScale of 0.08
# will make text appear under the toon name
# @return an (interval, None)
def makeFanfareWithMessage(delay, toon, showToonName, message, messagePos, messageScale, wordwrap = 100):
    panel = makePanel(toon, showToonName)
    makeMessageBox(panel, message, messagePos, messageScale, wordwrap)
    return doFanfare(delay, toon, panel)

# this does a fanfare and brings up a box with an image.
# user specifies what, where, and how big the image is
# imagePos of Vec3(0,0,0) and imageScale of 3
# using the an inventory button appears
# @return an (interval, RewardPanel)
def makeFanfareWithImage(delay, toon, showToonName, image, imagePos, imageScale, wordwrap = 100):
    panel = makePanel(toon, showToonName)
    makeMessageBox(panel, "", Vec3(0,0,0), 1, wordwrap)
    makeImageBox(panel.itemFrame, image, imagePos, imageScale)
    return doFanfare(delay, toon, panel)

# this does a Fanfare and brings up a box with a message and image
# user specifies messages and image properties
# @return an (interval, RewardPanel)
def makeFanfareWithMessageImage(delay, toon, showToonName, message, messagePos, 
                            messageScale, image, imagePos, imageScale, wordwrap = 100):
    panel = makePanel(toon, showToonName)
    makeMessageBox(panel, message, messagePos, messageScale, wordwrap)
    makeImageBox(panel.itemFrame, image, imagePos, imageScale)
    return doFanfare(delay, toon, panel)

###############################################################
# this creates the interval for the fanfare
###############################################################

# @return an (interval, RewardPanel)
def doFanfare(delay, toon, panel):
    
    fanfareNode = toon.attachNewNode('fanfareNode')    
    partyBall = fanfareNode.attachNewNode('partyBall')
    headparts = toon.getHeadParts()
    
    pos = headparts[2].getPos(fanfareNode)
    
    # the party ball is two halves of a sphere that open up
    partyBallLeft = globalPropPool.getProp('partyBall')
    partyBallLeft.reparentTo(partyBall)
    partyBallLeft.setScale(.8)
    partyBallLeft.setH(90)
    partyBallLeft.setColorScale(1,0,0,0)
    
    partyBallRight = globalPropPool.getProp('partyBall')
    partyBallRight.reparentTo(partyBall)
    partyBallRight.setScale(.8)
    partyBallRight.setH(-90)
    partyBallRight.setColorScale(1,1,0,0)
    
    # positioned above the head of the toon
    partyBall.setZ(pos.getZ()+3.2)
    
    # the ball shakes before it opens
    ballShake1 = Sequence(
                         Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,0,0), 
                                                  hpr=Vec3(90,10,0), blendType='easeInOut'),
                                  LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,0,0), 
                                                  hpr=Vec3(-90,-10,0), blendType='easeInOut')),
                         Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,10,0), 
                                                  hpr=Vec3(90,-10,0), blendType='easeInOut'),
                                  LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,-10,0), 
                                                  hpr=Vec3(-90,10,0), blendType='easeInOut')),
                         Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,-10,0), 
                                                  hpr=Vec3(90,0,0), blendType='easeInOut'),
                                  LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,10,0), 
                                                  hpr=Vec3(-90,0,0), blendType='easeInOut')))
    ballShake2 = Sequence(
                         Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,0,0), 
                                                  hpr=Vec3(90,-10,0), blendType='easeInOut'),
                                  LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,0,0), 
                                                  hpr=Vec3(-90,10,0), blendType='easeInOut')),
                         Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,-10,0), 
                                                  hpr=Vec3(90,10,0), blendType='easeInOut'),
                                  LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,10,0), 
                                                  hpr=Vec3(-90,-10,0), blendType='easeInOut')),
                         Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,10,0), 
                                                  hpr=Vec3(90,0,0), blendType='easeInOut'),
                                  LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,-10,0), 
                                                  hpr=Vec3(-90,0,0), blendType='easeInOut')))

    openBall = Parallel(LerpHprInterval(partyBallLeft, duration=.2,startHpr=Vec3(90,0,0), hpr=Vec3(90,30,0)),
                        LerpHprInterval(partyBallRight, duration=.2,startHpr=Vec3(-90,0,0), hpr=Vec3(-90,30,0)))
    confettiNode = fanfareNode.attachNewNode('confetti')
    confettiNode.setScale(3)
    confettiNode.setZ(pos.getZ()+2.5)
    
    # this method is used for the trumpet blowing.  It is just a scale in/out
    def longshake(models,num,duration):
        inShake = getScaleBlendIntervals(models,duration=duration,startScale=.23,
                                         endScale=.2,blendType='easeInOut')
        outShake = getScaleBlendIntervals(models,duration=duration,startScale=.2,
                                          endScale=.23,blendType='easeInOut')
        i = 1
        seq = Sequence()
        while i < num:
            if i % 2 == 0:
                seq.append(inShake)
            else:
                seq.append(outShake)
            i+=1
        return seq
    
    # just a way of getting two scale intervals for two different LOD models    
    def getScaleBlendIntervals(props, duration, startScale, endScale, blendType):
        tracks = Parallel()
        for prop in props:
            tracks.append(LerpScaleInterval(prop, duration, endScale,
                                            startScale=startScale,blendType=blendType))
        return tracks
    
    # creation of the two trumpets
    trumpetNode = fanfareNode.attachNewNode('trumpetNode')
    
    trumpet1 = globalPropPool.getProp('bugle')
    trumpet2 = MovieUtil.copyProp(trumpet1)
    trumpet1.reparentTo(trumpetNode)
    trumpet1.setScale(.2)
    # this should make it look at the player the fanfare centers on
    trumpet1.setPos(2,2,1)
    trumpet1.setHpr(120,65,0)    
    
    trumpet2.reparentTo(trumpetNode)
    trumpet2.setScale(.2)
    trumpet2.setPos(-2,2,1)
    trumpet2.setHpr(-120,65,0)

    # trumpets are initially transparent
    trumpetNode.setTransparency(1)
    trumpetNode.setColor(1,1,1,0)
    
    trumpturn1 = LerpHprInterval(trumpet1,duration=4,startHpr=Vec3(80,15,0), 
                                 hpr=Vec3(150,40,0))
    trumpturn2 = LerpHprInterval(trumpet2,duration=4,startHpr=Vec3(-80,15,0), 
                                 hpr=Vec3(-150,40,0))

    trumpetTurn = Parallel(trumpturn1, trumpturn2)
    
    #######################################################################
    # CONFETTI PARTICLE EFFECT
    #######################################################################
    
    BattleParticles.loadParticles()
    confettiBlue = BattleParticles.createParticleEffect('Confetti')
    confettiBlue.reparentTo(confettiNode)   
    blue_p0 = confettiBlue.getParticlesNamed('particles-1')
    blue_p0.renderer.getColorInterpolationManager().addConstant(0.0,1.0,Vec4(0.0,0.0,1.0,1.0),1)

    confettiYellow = BattleParticles.createParticleEffect('Confetti')
    confettiYellow.reparentTo(confettiNode)   
    yellow_p0 = confettiYellow.getParticlesNamed('particles-1')
    yellow_p0.renderer.getColorInterpolationManager().addConstant(0.0,1.0,Vec4(1.0,1.0,0.0,1.0),1)
    
    confettiRed = BattleParticles.createParticleEffect('Confetti')
    confettiRed.reparentTo(confettiNode)   
    red_p0 = confettiRed.getParticlesNamed('particles-1')
    red_p0.renderer.getColorInterpolationManager().addConstant(0.0,1.0,Vec4(1.0,0.0,0.0,1.0),1)
    
    #######################################################################
    
    trumpetsAppear = LerpColorInterval(trumpetNode,.3,startColor=Vec4(1,1,0,0),
                                       color=Vec4(1,1,0,1))
    trumpetsVanish = LerpColorInterval(trumpetNode,.3,startColor=Vec4(1,1,0,1),
                                       color=Vec4(1,1,0,0))

    # loads sounds, puts crabHorn at the Horn part, cutting out the scuttle
    crabHorn = globalBattleSoundCache.getSound('King_Crab.mp3')
    drumroll = globalBattleSoundCache.getSound('SZ_MM_drumroll.mp3')
    fanfare = globalBattleSoundCache.getSound('SZ_MM_fanfare.mp3')
    crabHorn.setTime(1.5)
    
    
    partyBall.setTransparency(1)
    partyBall.setColorScale(1,1,1,1)
     
    # ball intervals
    ballAppear = Parallel(LerpColorScaleInterval(partyBallLeft,.3,startColorScale=Vec4(1,0,0,0),colorScale=Vec4(1,0,0,1)), 
                          LerpColorScaleInterval(partyBallRight,.3,startColorScale=Vec4(1,1,0,0),colorScale=Vec4(1,1,0,1)))
    ballVanish = Parallel(LerpColorScaleInterval(partyBallLeft,.3,startColorScale=Vec4(1,0,0,1),colorScale=Vec4(1,0,0,0)), 
                          LerpColorScaleInterval(partyBallRight,.3,startColorScale=Vec4(1,1,0,1),colorScale=Vec4(1,1,0,0)))
    
    # the trumpets playing and the sound for the trumpets
    play = Parallel(SoundInterval(crabHorn, startTime=1.5, duration=4.0, node=toon),Sequence(Wait(.25),longshake([trumpet1,trumpet2],3,.2),
                    Wait(.5),longshake([trumpet1,trumpet2],3,.2),Wait(.5),
                    longshake([trumpet1,trumpet2],9,.1),longshake([trumpet1,trumpet2],3,.2)))
    
    # particle interval
    killParticles = Parallel(Func(blue_p0.setLitterSize,0),Func(red_p0.setLitterSize,0),Func(yellow_p0.setLitterSize,0))
    p = Parallel(ParticleInterval(confettiBlue, confettiNode, worldRelative=0, duration=3, cleanup = True),
                 ParticleInterval(confettiRed, confettiNode, worldRelative=0, duration=3, cleanup = True),
                 ParticleInterval(confettiYellow, confettiNode, worldRelative=0, duration=3, cleanup = True))
    pOff = Parallel(Func(confettiBlue.remove),
                    Func(confettiRed.remove),
                    Func(confettiYellow.remove))
    partInterval = Parallel(p,Sequence(Wait(1.7),killParticles,Wait(1.3),
                                       pOff,Func(p.finish)), 
                                       Sequence(Wait(3),Parallel(ballVanish)))

    # sets up main interval
    seq1 = Parallel(Sequence(Wait(delay+4.1),SoundInterval(drumroll, node=toon), Wait(.25),SoundInterval(fanfare,node=toon)),
                    Sequence(Wait(delay),trumpetsAppear,Wait(3),ballAppear,Wait(.5),
                    ballShake1,Wait(.1),ballShake2,Wait(.2),Wait(.1),
                    Parallel(openBall,partInterval),Func(fanfareNode.remove)))
        
    seq = Parallel(seq1, Sequence(Wait(delay),Parallel(trumpetTurn,Sequence(Wait(.5),play)),
                                  Wait(.5),trumpetsVanish))
    
    # if we need to show a panel, we return the panel we created, otherwise we return the None
    if panel != None:
        return (seq, panel)
    
    return (seq, None)


#-------------------------------------------------------------------------------
# Contact: Samik Bhowal
# Created: 06/18/09
#
# Purpose: This class is used to directly import the fireworks used in 
#          Pirates of the Carribean Online. I haven't depracated the way Toontown
#          natively did fireworks using Fireworks.py. Simply use the Fireworks.py class 
#          to create Toontown's old fireworks style or use Firework.py to create
#          Pirate's style fireworks.  
#
#-------------------------------------------------------------------------------

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
##from toontown.effects import FireworkGlobals
from toontown.effects.FireworkGlobals import *
from toontown.effects.FireworkEffect import FireworkEffect
import random

class Firework(NodePath):
    
    def __init__(self, typeId,
                 velocity=Vec3(0,0,500),scale=1.0,
                 color1=Vec4(1,1,1,1), color2=None,
                 burstDelay=1.25):
        NodePath.__init__(self, "Firework")
        
        self.typeId = typeId
        self.velocity = velocity
        self.scale = scale
        self.primaryColor = color1
        self.secondaryColor = color2
        if not self.secondaryColor:
            self.secondaryColor = self.primaryColor
        self.burstDelay = burstDelay

        self.fireworkIval = None
        self.fireworkEffects = []

    def play(self):
        if not self.fireworkIval:
            self.generateFireworkIval()
        self.fireworkIval.start()
    
    def generateFireworkIval(self):
        if not self.fireworkIval:
            self.fireworkIval = Sequence()

            # BasicPeony - A special break of colored stars, the most commonly seen
            #              shell type. Static stars appear without leaving trail. 
            # --------------------------------------------------------------------
            if (self.typeId == FireworkType.BasicPeony):
                firework = FireworkEffect(FireworkBurstType.PeonyShell,
                                          #FireworkTrailType.Polygonal,
                                          FireworkTrailType.Default,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # AdvancedPeony - Like BasicPeony, except I used particles which
            #                 travel more dynamically.
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.AdvancedPeony):
                firework = FireworkEffect(FireworkBurstType.PeonyParticleShell,
                                          #FireworkTrailType.Polygonal,
                                          FireworkTrailType.Default,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # DiademPeony - A type of Peony with a center cluster of non-moving
            #               stars, usually of a contrasting color and effect
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.DiademPeony):
                firework = FireworkEffect(FireworkBurstType.PeonyDiademShell,
                                          #FireworkTrailType.Polygonal,
                                          FireworkTrailType.Default,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # Chrysanthemum - Similar to Peony, but stars leave a visible trail of
            #                 sparks making it look like a flower it is named after
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.Chrysanthemum):
                firework = FireworkEffect(FireworkBurstType.ChrysanthemumShell,
                                          FireworkTrailType.Glow,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # DiademChrysanthemum - A type of Chrysanthemum with a center cluster of
            #                       non-moving stars of a contrasting color and effect
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.DiademChrysanthemum):
                firework = FireworkEffect(FireworkBurstType.ChrysanthemumDiademShell,
                                          #FireworkTrailType.Polygonal,
                                          FireworkTrailType.Glow,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # Ring - A shell with stars specially arranged so as to create a ring
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.Ring):
                firework = FireworkEffect(FireworkBurstType.RingShell,
                                          FireworkTrailType.Default,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # Saturn - Ring firework with additional shell inside of the burst
            #          making it look like a Saturn planet
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.Saturn):
                firework = FireworkEffect(FireworkBurstType.SaturnShell,
                                          FireworkTrailType.GlowSparkle,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # Bees - Spherical explosion of stars which move erratically in all
            #        direction while burning out
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.Bees):
                firework = FireworkEffect(FireworkBurstType.BeeShell,
                                          FireworkTrailType.Polygonal,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())
                

            # Trail Burst
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.TrailBurst):
                firework = FireworkEffect(FireworkBurstType.TrailExplosion,
                                          FireworkTrailType.Glow,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            
            # Glow Flare
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.GlowFlare):
                firework = FireworkEffect(None,
                                          FireworkTrailType.LongGlowSparkle,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                firework.gravityMult = 1.0
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # Palm Tree
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.PalmTree):
                firework = FireworkEffect(FireworkBurstType.TrailExplosion,
                                          FireworkTrailType.LongGlowSparkle,
                                          self.velocity, self.scale,
                                          self.primaryColor, self.secondaryColor,
                                          self.burstDelay)
                firework.reparentTo(self)
                firework.gravityMult = 1.0
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            # Mickey - sequence of 3 Peony fireworks forming the shape of Mickey's head
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.Mickey):
                head = FireworkEffect(FireworkBurstType.PeonyShell,
                                      FireworkTrailType.Glow,
                                      velocity = Vec3(0,0,80*self.scale),
                                      scale = self.scale/1.2,
                                      primaryColor = self.primaryColor,
                                      secondaryColor = self.secondaryColor,
                                      burstDelay = 1.5)
                leftEar = FireworkEffect(FireworkBurstType.PeonyShell,
                                         FireworkTrailType.Glow,
                                         velocity = Vec3(-25*self.scale,0,115*self.scale),
                                         scale = self.scale/1.6,
                                         primaryColor = self.primaryColor,
                                         secondaryColor = self.secondaryColor,
                                         burstDelay = 1.7)
                rightEar = FireworkEffect(FireworkBurstType.PeonyShell,
                                          FireworkTrailType.Glow,
                                          velocity = Vec3(25*self.scale,0,115*self.scale),
                                          scale = self.scale/1.6,
                                          primaryColor = self.primaryColor,
                                          secondaryColor = self.secondaryColor,
                                          burstDelay = 1.7)
                head.reparentTo(self)
                leftEar.reparentTo(self)
                rightEar.reparentTo(self)
                self.fireworkEffects=self.fireworkEffects+[head, leftEar, rightEar]
                fireworkParallel = Parallel()
                fireworkParallel.append(head.getFireworkMainIval())
                fireworkParallel.append(leftEar.getFireworkMainIval())
                fireworkParallel.append(rightEar.getFireworkMainIval())
                self.fireworkIval.append(fireworkParallel)

            # PirateSkull - sequence of 3 fireworks forming pirate skull symbol
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.PirateSkull):
                skull = FireworkEffect(FireworkBurstType.SkullBlast,
                                       FireworkTrailType.GlowSparkle,
                                       velocity = Vec3(0,0,400*self.scale),
                                       scale = self.scale,
                                       primaryColor = self.primaryColor,
                                       secondaryColor = self.secondaryColor,
                                       burstDelay = 1.75)
                leftBone = FireworkEffect(None,
                                          FireworkTrailType.LongGlowSparkle,
                                          velocity = Vec3(220*self.scale,0,250*self.scale),
                                          scale = self.scale*1.25,
                                          primaryColor = self.primaryColor,
                                          secondaryColor = self.secondaryColor,
                                          burstDelay = 2.25)
                rightBone = FireworkEffect(None,
                                           FireworkTrailType.LongGlowSparkle,
                                           velocity = Vec3(-220*self.scale,0,250*self.scale),
                                           scale = self.scale*1.25,
                                           primaryColor = self.primaryColor,
                                           secondaryColor = self.secondaryColor,
                                           burstDelay = 2.25)
                skull.reparentTo(self)
                leftBone.reparentTo(self)
                leftBone.setPos(-225*self.scale,0,0)
                leftBone.gravityMult = 3.5
                rightBone.reparentTo(self)
                rightBone.setPos(225*self.scale,0,0)
                rightBone.gravityMult = 3.5
                self.fireworkEffects=self.fireworkEffects+[skull, leftBone, rightBone]
                fireworkParallel = Parallel()
                fireworkParallel.append(skull.getFireworkMainIval())
                fireworkParallel.append(leftBone.getFireworkMainIval())
                fireworkParallel.append(rightBone.getFireworkMainIval())
                self.fireworkIval.append(fireworkParallel)

            # AmericanFlag - sequence of 5 fireworks forming american flag
            # --------------------------------------------------------------------
            elif (self.typeId == FireworkType.AmericanFlag):
                fireworkParallel = Parallel()
                colors = [Vec4(1,0,0,1),Vec4(1,1,1,1)]
                # red and white stripes
                for i in range(4):
                    firework = FireworkEffect(None,
                                              FireworkTrailType.LongGlowSparkle,
                                              velocity = Vec3(-30*self.scale,0,150*self.scale-20*i),
                                              scale = self.scale*3.0,
                                              primaryColor = colors[i%2],
                                              burstDelay = 2.5)
                    firework.reparentTo(self)
                    firework.setX(-20.0*self.scale + 10.0*i*self.scale)
                    self.fireworkEffects.append(firework)
                    fireworkParallel.append(Sequence(Wait(.25*i),firework.getFireworkMainIval()))
                # stars
                firework = FireworkEffect(FireworkBurstType.Sparkles,
                                          FireworkTrailType.Default,
                                          velocity = Vec3(20,0,90),
                                          scale = self.scale*1.5)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                fireworkParallel.append(Sequence(Wait(1.5),firework.getFireworkMainIval()))
                self.fireworkIval.append(fireworkParallel)
            # IceCream - A scoop of ice cream that's composed of ice cream cones
            elif (self.typeId == FireworkType.IceCream):
                firework = FireworkEffect(FireworkBurstType.IceCream,
                                          FireworkTrailType.Default,
                                          self.velocity, self.scale,
                                          Vec4(1,1,1,1), Vec4(1,1,1,1),
                                          self.burstDelay)
                firework.reparentTo(self)
                self.fireworkEffects.append(firework)
                self.fireworkIval.append(firework.getFireworkMainIval())

            self.fireworkIval.append(Func(self.cleanup))
            
        return self.fireworkIval

    def cleanup(self):
        if self.fireworkIval:
            self.fireworkIval.pause()
            self.fireworkIval = None
        for effect in self.fireworkEffects:
            effect.cleanupEffect()
        self.fireworkEffects = []

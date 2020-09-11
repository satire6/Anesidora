import AnimatedProp
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from toontown.effects.Splash import *
from toontown.effects.Ripples import *
import random


class FishAnimatedProp(AnimatedProp.AnimatedProp):
    def __init__(self, node):
        # To access fish in game:
        # fish = base.cr.playGame.hood.loader.animPropDict.values()[0]
        AnimatedProp.AnimatedProp.__init__(self, node)
        parent = node.getParent()
        self.fish = Actor.Actor(node, copy = 0)
        self.fish.reparentTo(parent)

        # Move the transform from the original character node,
        # self.node, to the new Actor node, self.fish.
        self.fish.setTransform(node.getTransform())
        node.clearMat()

        self.fish.loadAnims({'jump' : "phase_4/models/props/SZ_fish-jump",
                             'swim' : "phase_4/models/props/SZ_fish-swim"})

        self.splashSfxList = (loader.loadSfx("phase_4/audio/sfx/TT_splash1.mp3"),
                              loader.loadSfx("phase_4/audio/sfx/TT_splash2.mp3"),
                              )

        # Now forget about the old self.node; we're now the Actor.
        self.node = self.fish

        # Except that we still want a handle to the model node so we
        # can randomly position the fish around.
        self.geom = self.fish.getGeomNode()

        # Ripples to display when fish exits the water
        self.exitRipples = Ripples(self.geom)
        self.exitRipples.setBin('fixed', 25,1)
        # Put it a little higher to help transparency sort order
        self.exitRipples.setPosHprScale(-0.3, 0.0, 1.24,
                                        0.00, 0.00, 0.00,
                                        0.7, 0.7, 0.7)

        # Splash and ripples to display when fish re-enters the water
        self.splash = Splash(self.geom, wantParticles=0)
        self.splash.setPosHprScale(-1, 0.0, 1.23,
                                   0.00, 0.00, 0.00,
                                   0.7, 0.7, 0.7)

        randomSplash = random.choice(self.splashSfxList)

        # Track to play back the whole think
        self.track = Sequence(
            FunctionInterval(self.randomizePosition),
            Func(self.node.unstash),
            Parallel(self.fish.actorInterval('jump'),
                     # Ripples when exiting water
                     Sequence(Wait(0.25),
                              Func(self.exitRipples.play, 0.75),
                              ),
                     # Splash when re-entering water
                     Sequence(Wait(1.14),
                              Func(self.splash.play),
                              SoundInterval(randomSplash, volume=0.8, node=self.node),
                              )
                     ),
            Wait(1),
            Func(self.node.stash),
            # Wait inbetween
            Wait(4 + 10 * random.random()),
            name = self.uniqueName("Fish"))

    def delete(self):
        self.exitRipples.destroy()
        del self.exitRipples
        self.splash.destroy()
        del self.splash
        del self.track
        self.fish.removeNode()
        del self.fish
        del self.node
        del self.geom

    def randomizePosition(self):
        x = 5 * (random.random() - 0.5)
        y = 5 * (random.random() - 0.5)
        h = 360 * random.random()
        self.geom.setPos(x, y, 0)
        self.geom.setHpr(h, 0, 0)
    
    def enter(self):
        AnimatedProp.AnimatedProp.enter(self)
        self.track.loop()

    def exit(self):
        AnimatedProp.AnimatedProp.exit(self)
        self.track.finish()
        # Stop child intervals
        self.splash.stop()
        self.exitRipples.stop()

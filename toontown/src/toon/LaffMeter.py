"""LaffMeter module: contains the class definition for handling the
laff-o-meter"""

from pandac.PandaModules import *
from otp.avatar import DistributedAvatar
from toontown.toonbase import ToontownGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

class LaffMeter(DirectFrame):
    """LaffMeter class"""

    deathColor = Vec4(0.58039216, 0.80392157, 0.34117647, 1.0)

    # special methods
    def __init__(self, avdna, hp, maxHp):
        """__init(self, AvatarDNA, int, int)
        LaffMeter constructor: create a laff-o-meter for a given DA
        """
        DirectFrame.__init__(self, relief=None, sortOrder=50)
        self.initialiseoptions(LaffMeter)

        # This is to contain the scale for the animated effect
        self.container = DirectFrame(parent = self, relief = None)
        
        self.style = avdna
        self.av = None
        self.hp = hp
        self.maxHp = maxHp
        self.__obscured = 0
        if (self.style.type == 't'):
            self.isToon = 1
        else:
            self.isToon = 0
        self.load()

    def obscure(self, obscured):
        """obscureButton(self, int obscured)
        Make the be button be obscured, regardless of show and hide
        1 = obscure, 0 = unobscured
        """
        self.__obscured = obscured
        if self.__obscured:
            self.hide()

    def isObscured(self):
        return self.__obscured

    def load(self):
        gui = loader.loadModel("phase_3/models/gui/laff_o_meter")
        if self.isToon:
            hType = self.style.getType()
            if (hType == "dog"):
                headModel = gui.find("**/doghead")
            elif (hType == "cat"):
                headModel = gui.find("**/cathead")
            elif (hType == "mouse"):
                headModel = gui.find("**/mousehead")
            elif (hType == "horse"):
                headModel = gui.find("**/horsehead")
            elif (hType == "rabbit"):
                headModel = gui.find("**/bunnyhead")
            elif (hType == "duck"):
                headModel = gui.find("**/duckhead")
            elif (hType == "monkey"):
                headModel = gui.find("**/monkeyhead")
            elif (hType == "bear"):
                headModel = gui.find("**/bearhead")
            elif (hType == "pig"):
                headModel = gui.find("**/pighead")
            else:
                raise StandardError("unknown toon species: ", hType)

            self.color = self.style.getHeadColor()

            self.container['image'] = headModel
            self.container['image_color'] = self.color
            self.resetFrameSize()
            self.setScale(0.1)
            self.frown = DirectFrame(parent = self.container, relief = None,
                                image = gui.find("**/frown"))
            self.smile = DirectFrame(parent = self.container, relief = None,
                                image = gui.find("**/smile"))
            self.eyes = DirectFrame(parent = self.container, relief = None,
                               image = gui.find("**/eyes"))
            self.openSmile = DirectFrame(parent = self.container, relief = None,
                                    image = gui.find("**/open_smile"))
            self.tooth1 = DirectFrame(parent = self.openSmile, relief = None,
                                 image = gui.find("**/tooth_1"))
            self.tooth2 = DirectFrame(parent = self.openSmile, relief = None,
                                 image = gui.find("**/tooth_2"))
            self.tooth3 = DirectFrame(parent = self.openSmile, relief = None,
                                 image = gui.find("**/tooth_3"))
            self.tooth4 = DirectFrame(parent = self.openSmile, relief = None,
                                 image = gui.find("**/tooth_4"))
            self.tooth5 = DirectFrame(parent = self.openSmile, relief = None,
                                 image = gui.find("**/tooth_5"))
            self.tooth6 = DirectFrame(parent = self.openSmile, relief = None,
                                 image = gui.find("**/tooth_6"))

                        
            self.maxLabel = DirectLabel(parent = self.eyes,
                                   relief = None,
                                   pos = (0.442, 0, 0.051),
                                   text = "120",
                                   text_scale = 0.4,
                                   text_font = ToontownGlobals.getInterfaceFont(),
                                   )
            self.hpLabel = DirectLabel(parent = self.eyes,
                                  relief = None,
                                  pos = (-0.398, 0, 0.051),
                                  text = "120",
                                  text_scale = 0.4,
                                  text_font = ToontownGlobals.getInterfaceFont(),
                                  )
            
            self.teeth = [self.tooth6, self.tooth5, self.tooth4,
                          self.tooth3, self.tooth2, self.tooth1]
            self.fractions = [0., 0.166666, 0.333333, 0.5, 0.666666, 0.833333]

        gui.removeNode()

    def destroy(self):
        if self.av:
            taskMgr.remove(self.av.uniqueName('laffMeterBoing') + '-' + str(self.this))
            taskMgr.remove(self.av.uniqueName('laffMeterBoing') + '-' + str(self.this) + '-play')
            self.ignore(self.av.uniqueName("hpChange"))
        del self.style
        del self.av
        del self.hp
        del self.maxHp
        if self.isToon:
            del self.frown
            del self.smile
            del self.openSmile
            del self.tooth1
            del self.tooth2
            del self.tooth3
            del self.tooth4
            del self.tooth5
            del self.tooth6
            del self.teeth
            del self.fractions
            del self.maxLabel
            del self.hpLabel
        DirectFrame.destroy(self)

    def adjustTeeth(self):
        """adjustTeeth(self)
        if teeth are showing, decide which ones should be
        """
        if self.isToon:
            # Look through the fractions of hp for each tooth
            for i in range(len(self.teeth)):
                # if the hp is more than that fraction, turn this tooth on
                if (self.hp > (self.maxHp * self.fractions[i])):
                    self.teeth[i].show()
                else:
                    self.teeth[i].hide()

    def adjustText(self):
        """adjustText(self)
        set the text for current HP and maxHP
        """
        if self.isToon:
            # Only update if the text has changed
            if (self.maxLabel['text'] != str(self.maxHp) or
                self.hpLabel['text'] != str(self.hp)):
                self.maxLabel['text'] = str(self.maxHp)
                self.hpLabel['text'] = str(self.hp)
        return


    def animatedEffect(self, delta):
        # Note: the task name here must be unique to this avatar and
        # to this laffmeter. We'll use the python this pointer to
        # differentiate multiple laffmeters watching the same toon
        # This happens in battle and on avatar detail panels
        if (delta == 0) or (self.av == None):
            return
        taskName = self.av.uniqueName('laffMeterBoing') + '-' + str(self.this)
        taskMgr.remove(taskName)
        if delta > 0:
            # Laffmeter increase
            Sequence(self.container.scaleInterval(0.2, 1.333, blendType='easeOut'),
                     self.container.scaleInterval(0.2, 1, blendType='easeIn'),
                     name = taskName,
                     autoFinish = 1
                     ).start()
        else:
            # Laffmeter decrease
            Sequence(self.container.scaleInterval(0.2, 0.666, blendType='easeOut'),
                     self.container.scaleInterval(0.2, 1, blendType='easeIn'),
                     name = taskName,
                     autoFinish = 1
                     ).start()

    def adjustFace(self, hp, maxHp, quietly = 0):
        """adjustFace(self, int, int)
        make sure the laff-o-meter face is in sync with the avatar state
        """
        if self.isToon and self.hp != None:
            # Hide everything first
            self.frown.hide()
            self.smile.hide()
            self.openSmile.hide()
            self.eyes.hide()
            for tooth in self.teeth:
                tooth.hide()
            # Now show elements based on hp
            delta = hp - self.hp
            self.hp = hp
            self.maxHp = maxHp
            if (self.hp < 1):
                self.frown.show()
                self.container['image_color'] = self.deathColor
            elif (self.hp >= self.maxHp):
                self.smile.show()
                self.eyes.show()
                self.container['image_color'] = self.color
            else:
                self.openSmile.show()
                self.eyes.show()
                self.maxLabel.show()
                self.hpLabel.show()
                self.container['image_color'] = self.color
                self.adjustTeeth()

            self.adjustText()

            if not quietly:
                self.animatedEffect(delta)

    def start(self):
        """start
        manage the GUI elements of the laff-o-meter
        """

        if self.av:
            # Refresh the hp and max hp, in case they changed when
            # we weren't managed.
            self.hp = self.av.hp
            self.maxHp = self.av.maxHp

        if self.isToon:
            if not self.__obscured:
                self.show()
            self.adjustFace(self.hp, self.maxHp, 1) # Do not animate this first one
            if self.av:
                self.accept(self.av.uniqueName("hpChange"), self.adjustFace)

    def stop(self):
        """stop(self)
        unmanage the GUI elements of the laff-o-meter
        """
        if self.isToon:
            self.hide()
            if self.av:
                self.ignore(self.av.uniqueName("hpChange"))

    def setAvatar(self, av):
        """setAvatar(self, DistributedAvatar):
        set an avatar structure for use by the auto-update system
        """
        # Get rid of any previous avatar hooks
        if self.av:
            self.ignore(self.av.uniqueName("hpChange"))
        self.av = av

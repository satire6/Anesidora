from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TeaserPanel

class TrialerForceAcknowledge:

    def __init__(self, doneEvent):
        """___init___(self, Event)"""
        self.doneEvent = doneEvent
        self.dialog = None

    def enter(self, destHood):
        """enter(phase)
        """
        doneStatus = {}
        def letThrough(self=self, doneStatus=doneStatus):
            doneStatus['mode'] = 'pass'
            messenger.send(self.doneEvent, [doneStatus])

        if not base.restrictTrialers:
            letThrough()
            return

        if base.roamingTrialers:
            letThrough()
            return

        if base.cr.isPaid():
            # paid user, let them through
            letThrough()
            return
        
        if ZoneUtil.getCanonicalHoodId(destHood) in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ):
            # trialer going to TTC/Estate/Goofy Speedway, let them through
            letThrough()
            return
        else:
            # Careful! You may not have a localToon yet
            try:
                # Make the Toon stand still while the panel is up
                base.localAvatar.b_setAnimState('neutral', 1)
            except:
                pass
            
        doneStatus['mode'] = 'fail'
        self.doneStatus = doneStatus
        self.dialog = TeaserPanel.TeaserPanel(pageName='otherHoods',
                                              doneFunc=self.handleOk)

    def exit(self):
        """exit(self)
        """
        if self.dialog:
            self.dialog.cleanup()
            self.dialog.unload()
            self.dialog = None

    def handleOk(self):
        messenger.send(self.doneEvent, [self.doneStatus])

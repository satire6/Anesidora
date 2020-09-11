from pandac.PandaModules import TextNode
from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.interval.IntervalGlobal import Func, Sequence, Wait
from toontown.toonbase import ToontownGlobals

class ServerTimeGui(DirectFrame):
    """A class to dislay the server time nicely.
    Do not put references to the shtiker page or book,  so this
    class can be placed anywhere."""

    def __init__(self, parent, pos = (0,0,0), hourCallback=None ):
        """Construct ourself."""
        DirectFrame.__init__(self, parent=parent, pos = pos)
        self.createGuiObjects()
        # hourCallback will be called when the clock changes hours
        self.hourCallback = hourCallback
        self.lastHour = -1
        self.lastMinute = -1
        
    def createGuiObjects(self):
        """Create all gui elements and tasks."""
        # minutes label
        textScale = 0.075
        # Minnnie font doesn't have numbers!
        #timeFont = ToontownGlobals.getToonFont()
        timeFont = ToontownGlobals.getMinnieFont()
        self.hourLabel = DirectLabel(
            parent = self,
            pos = (-0.015,0,0),
            relief = None,
            text = '',
            text_scale = textScale,
            text_align = TextNode.ARight,
            text_font = timeFont,
            )
        
        self.colonLabel = DirectLabel(
            parent = self,
            relief = None,
            text = ':',
            text_scale = textScale,
            text_align = TextNode.ACenter,
            text_font = timeFont,
            )

        self.minutesLabel = DirectLabel(
            relief = None,
            parent = self,
            pos = (0.015, 0, 0),
            text = '',
            text_scale = textScale,
            text_align = TextNode.ALeft,
            text_font = timeFont,
            )

        self.amLabel = DirectLabel(
            relief = None,
            parent = self,
            pos = (0.14, 0, 0),
            text = '',
            text_scale = textScale,
            text_align = TextNode.ALeft,
            text_font = timeFont,
            )
        
        self.ival = Sequence(
            Func(self.colonLabel.show),
            Wait(0.75),
            Func(self.colonLabel.hide),
            Wait(0.25),
            Func(self.updateTime)
            )
        self.ival.loop()

    def destroy(self):
        """Do proper cleanup of the ival."""
        self.ival.finish()
        self.ival = None
        DirectFrame.destroy(self)
            
    def updateTime(self):
        """Update the time displayed to the current server time."""
        curServerDate = base.cr.toontownTimeManager.getCurServerDateTime()
        
        if self.hourCallback is not None:
            if curServerDate.hour != self.lastHour and self.lastHour != -1:
                self.lastHour = curServerDate.hour    
                self.hourCallback(curServerDate.hour)

        if not curServerDate.minute == self.lastMinute:
            self.hourLabel['text'] = curServerDate.strftime('%I')
            self.lastHour = curServerDate.hour
            if self.hourLabel['text'][0] == '0':
                self.hourLabel['text'] = self.hourLabel['text'][1:]
            self.minutesLabel['text'] = curServerDate.strftime('%M')
            self.amLabel['text'] = curServerDate.strftime('%p')

        # debug values for ease of placement
        # self.hourLabel['text'] = '12'
        # self.minutesLabel['text'] = '38'
        # self.amLabel['text'] = 'PM'

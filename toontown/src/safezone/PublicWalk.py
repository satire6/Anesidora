from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal
import Walk

class PublicWalk(Walk.Walk):
    """
    Walking around in public places. Turns on a lot of interface stuff
    that plain old walk doesn't bother with.
    """
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("PublicWalk")
    
    
    def __init__(self, parentFSM, doneEvent):
        """
        doneEvent is a string.
        PublicWalk state constructor
        """
        # Call up the chain
        Walk.Walk.__init__(self, doneEvent)

        # We'll need this later
        self.parentFSM = parentFSM

    def load(self):
        # Call up the chain
        Walk.Walk.load(self)
            
    def unload(self):
        # Call up the chain
        Walk.Walk.unload(self)
        del self.parentFSM

    def enter(self, slowWalk = 0):
        # Call up the chain
        Walk.Walk.enter(self, slowWalk)
        
        # The shticker book and associated events
        base.localAvatar.book.showButton()
        self.accept(StickerBookHotkey, self.__handleStickerBookEntry)
        self.accept("enterStickerBook", self.__handleStickerBookEntry)
        self.accept(OptionsPageHotkey, self.__handleOptionsEntry)

        # The laffMeter
        base.localAvatar.laffMeter.start()
        base.localAvatar.beginAllowPies()

    def exit(self):
        # Call up the chain
        Walk.Walk.exit(self)
        
        # Put away the book
        base.localAvatar.book.hideButton()
        self.ignore(StickerBookHotkey)
        self.ignore("enterStickerBook")
        self.ignore(OptionsPageHotkey)

        # Put away the laff meter
        base.localAvatar.laffMeter.stop()
        base.localAvatar.endAllowPies()

    def __handleStickerBookEntry(self):
        # Don't open sticker book if we're jumping
        currentState = base.localAvatar.animFSM.getCurrentState().getName()
        if currentState == 'jumpAirborne':
            return
            
        if base.localAvatar.book.isObscured():
            return
        else:
            doneStatus = {}
            doneStatus['mode'] = 'StickerBook'
            messenger.send(self.doneEvent, [doneStatus])
            return

    def __handleOptionsEntry(self):
        # Don't open the options page if we are jumping
        currentState = base.localAvatar.animFSM.getCurrentState().getName()
        if currentState == 'jumpAirborne':
            return
        
        if base.localAvatar.book.isObscured():
            return
        else:
            doneStatus = {}
            doneStatus['mode'] = 'Options'
            messenger.send(self.doneEvent, [doneStatus])
            return

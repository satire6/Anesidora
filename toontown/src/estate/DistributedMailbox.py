from direct.distributed import DistributedObject
from toontown.toonbase import ToontownGlobals
import MailboxGlobals
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogItemList
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.catalog import MailboxScreen
from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.ClockDelta import *
from pandac.PandaModules import *
import random
from direct.interval.IntervalGlobal import SoundInterval

FlagPitchEmpty = -70
FlagPitchFull = 0

class DistributedMailbox(DistributedObject.DistributedObject):

    notify = directNotify.newCategory("DistributedMailbox")

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.model = None
        self.flag = None
        self.flagIval = None
        self.nameText = None
        self.fullIndicator = 0
        
        self.mailboxGui = None
        self.mailboxDialog = None

        # To be filled in later.
        self.mailboxSphereEvent = None
        self.mailboxSphereEnterEvent = None
        
        self.mailboxGuiDoneEvent = "mailboxGuiDone"

    def announceGenerate(self):
        DistributedMailbox.notify.debug("announceGenerate")
        DistributedObject.DistributedObject.announceGenerate(self)
        self.mailboxSphereEvent = self.taskName("mailboxSphere")
        self.mailboxSphereEnterEvent = "enter" + self.mailboxSphereEvent

        # Only listen for collisions with the local toon's own mailbox.
        if self.houseId == base.localAvatar.houseId:
            self.accept(self.mailboxSphereEnterEvent,  self.__handleEnterSphere)
        self.load()

    def load(self):
        DistributedMailbox.notify.debug("load")
        randomGenerator = random.Random()
        randomGenerator.seed(self.houseId)
        r = randomGenerator.random()
        g = randomGenerator.random()
        b = randomGenerator.random()
        self.nameColor = (r, g, b, 1)

        houseNode = self.cr.playGame.hood.loader.houseNode[self.housePosInd]
        estateNode = houseNode.getParent()
        
        zOffset = 0
        if self.housePosInd == 3:
            zOffset = -1
        elif self.housePosInd == 2:
            zOffset = 0.5
        
        self.model = loader.loadModel('phase_5.5/models/estate/mailboxHouse')
        self.model.reparentTo(estateNode)
        self.model.setPos(houseNode, 19, -4, 0 + zOffset)
        self.model.setH(houseNode, 90)

        self.flag = self.model.find('**/mailbox_flag')
        if self.fullIndicator:
            self.flag.setP(FlagPitchFull)
        else:
            self.flag.setP(FlagPitchEmpty)

        self.__setupName()
        
        # Find the collision tube and rename it so we can detect
        # collisions with the mailbox.
        collision = self.model.find('**/mailbox_collision')
        collision.setName(self.mailboxSphereEvent)
        
    def disable(self):
        DistributedMailbox.notify.debug("disable")
        self.notify.debug("disable")
        self.ignoreAll()
        if self.flagIval:
            self.flagIval.finish()
            self.flagIval = None
        if self.model:
            self.model.removeNode()
            self.model = None
        if self.nameText:
            self.nameText.removeNode()
            self.nameText = None
        if self.mailboxGui:
            self.mailboxGui.hide()
            self.mailboxGui.unload()
            self.mailboxGui = None
        if self.mailboxDialog:
            self.mailboxDialog.cleanup()
            self.mailboxDialog = None

        self.mailboxSphereEvent = None
        self.mailboxSphereEnterEvent = None

        DistributedObject.DistributedObject.disable(self)

    def setHouseId(self, houseId):
        DistributedMailbox.notify.debug("setHouseId( houseId=%d )" %houseId)
        self.houseId = houseId

    def setHousePos(self, housePosInd):
        DistributedMailbox.notify.debug("setHousePos")
        self.housePosInd = housePosInd

    def setName(self, name):
        DistributedMailbox.notify.debug("setName( name=%s )" %name)
        self.name = name

    def setFullIndicator(self, full):
        DistributedMailbox.notify.debug("setFullIndicator( full=%s )" %full)
        if self.fullIndicator != full:
            self.fullIndicator = full

            if self.flag:
                # Stop existing ival
                if self.flagIval:
                    self.flagIval.pause()
                    self.flagIval = None
                    
                # Animate the flag going up or down.
                p = FlagPitchEmpty
                if self.fullIndicator:
                    p = FlagPitchFull
                self.flagIval = self.flag.hprInterval(
                    0.5, VBase3(0, p, 0),blendType = 'easeInOut')
                self.flagIval.start()
            
        
    def __handleEnterSphere(self, collEntry):
        DistributedMailbox.notify.debug("Entering Mailbox Sphere....")
        # don't let other toons open the mailbox now
        self.ignore(self.mailboxSphereEnterEvent)
        self.cr.playGame.getPlace().detectedMailboxCollision()
        self.accept('mailboxAsleep', self.__handleMailboxSleep)

        # We don't need to bother the AI (or broadcast our collision
        # to any bystanders) for many of the simple failure cases.
        #av = base.localAvatar
        #if len(av.mailboxContents) == 0:
        #    if len(av.onOrder) == 0:
        #        self.setMovie(MailboxGlobals.MAILBOX_MOVIE_EMPTY, av.doId)
        #    else:
        #        self.setMovie(MailboxGlobals.MAILBOX_MOVIE_WAITING, av.doId)
        #
        #else:
        #    self.sendUpdate("avatarEnter", [])
        self.sendUpdate("avatarEnter", [])

    def __handleMailboxSleep(self):
        DistributedMailbox.notify.debug("Mailbox Sleep")
        if self.mailboxGui:
            self.mailboxGui.hide()
            self.mailboxGui.unload()
            self.mailboxGui = None
        if self.mailboxDialog:
            self.mailboxDialog.cleanup()
            self.mailboxDialog = None
        self.__handleMailboxDone()
        
    def __handleMailboxDone(self):
        DistributedMailbox.notify.debug("Mailbox Done")
        self.sendUpdate("avatarExit", [])
        self.ignore(self.mailboxGuiDoneEvent)
        self.mailboxGui = None

    def freeAvatar(self):
        """
        This is a message from the AI used to free the avatar from movie mode
        """
        DistributedMailbox.notify.debug("freeAvatar")
        #when garden tutorial starts, we force him to  'stopped'
        #so if we're at  stopped don't switch to walk, we will do taht
        #when the tutorial ends
        #import pdb; pdb.set_trace()
        self.notify.debug("freeAvatar")
        
        curState = base.cr.playGame.getPlace().getState()
        self.notify.debug('Estate.getState() == %s' % curState)
        
        if not curState == 'stopped':
            base.cr.playGame.getPlace().setState("walk")
        self.ignore('mailboxAsleep')
        
        # Start accepting the mailbox collision sphere event again
        self.accept(self.mailboxSphereEnterEvent, self.__handleEnterSphere)

    def setMovie(self, mode, avId):
        """
        This is a message from the AI describing a movie between this mailbox
        and a Toon that has approached us. 
        """
        
        # See if this is the local toon
        isLocalToon = (avId == base.localAvatar.doId)
        
        if isLocalToon:
            DistributedMailbox.notify.debug("setMovie( mode=%d, avId=%d ) called on a local toon" %(mode, avId))
        else:
            DistributedMailbox.notify.debug("setMovie( mode=%d, avId=%d ) called on a non-local toon" %(mode, avId))

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == MailboxGlobals.MAILBOX_MOVIE_CLEAR):
            DistributedMailbox.notify.debug("setMovie: clear")
            return
        
        elif (mode == MailboxGlobals.MAILBOX_MOVIE_EXIT):
            # Play one of the two mailbox closing sounds
            if random.random() < 0.5:
                sfx = base.loadSfx(
                    "phase_5.5/audio/sfx/mailbox_close_1.mp3")
            else:
                sfx= base.loadSfx(
                    "phase_5.5/audio/sfx/mailbox_close_2.mp3")
            sfxTrack = SoundInterval(sfx, node=self.model)
            sfxTrack.start()                
            DistributedMailbox.notify.debug("setMovie: exit")
            return
        
        elif (mode == MailboxGlobals.MAILBOX_MOVIE_EMPTY):
            DistributedMailbox.notify.debug("setMovie: empty")
            if isLocalToon:
                self.mailboxDialog = TTDialog.TTDialog(
                    dialogName = 'MailboxEmpty',
                    style = TTDialog.Acknowledge,
                    text = TTLocalizer.DistributedMailboxEmpty,
                    text_wordwrap = 15,
                    fadeScreen = 1,
                    command = self.__clearDialog,
                    )
            return
        
        elif (mode == MailboxGlobals.MAILBOX_MOVIE_WAITING):
            DistributedMailbox.notify.debug("setMovie: waiting")
            if isLocalToon:
                self.mailboxDialog = TTDialog.TTDialog(
                    dialogName = 'MailboxWaiting',
                    style = TTDialog.Acknowledge,
                    text = TTLocalizer.DistributedMailboxWaiting,
                    text_wordwrap = 15,
                    fadeScreen = 1,
                    command = self.__clearDialog,
                    )
            return
        
        elif (mode == MailboxGlobals.MAILBOX_MOVIE_READY):
            DistributedMailbox.notify.debug("setMovie: ready")
            # Play one of the two mailbox opening sounds
            if random.random() < 0.5:
                sfx= base.loadSfx("phase_5.5/audio/sfx/mailbox_open_1.mp3")
            else:
                sfx= base.loadSfx("phase_5.5/audio/sfx/mailbox_open_2.mp3")
            sfxTrack = SoundInterval(sfx, node=self.model)
            sfxTrack.start()                
            # If you are local toon, show the mailbox gui
            if isLocalToon:
                self.mailboxGui = MailboxScreen.MailboxScreen(
                    self, base.localAvatar,
                    self.mailboxGuiDoneEvent)
                self.mailboxGui.show()
                self.accept(self.mailboxGuiDoneEvent, self.__handleMailboxDone)
            return

        elif (mode == MailboxGlobals.MAILBOX_MOVIE_NOT_OWNER):
            DistributedMailbox.notify.debug("setMovie: not owner")
            if isLocalToon:
                self.mailboxDialog = TTDialog.TTDialog(
                    dialogName = 'MailboxNotOwner',
                    style = TTDialog.Acknowledge,
                    text = TTLocalizer.DistributedMailboxNotOwner,
                    text_wordwrap = 15,
                    fadeScreen = 1,
                    command = self.__clearDialog,
                    )
            return

        else:
            DistributedMailbox.notify.warning("unknown mode in setMovie: %s" % (mode))
        

    def acceptItem(self, item, index, callback, optional = -1):
        # Requests the purchase of the given item from the AI.  When
        # the AI responds, calls the callback function with three
        # parameters: the appropriate code from MailboxGlobals.py,
        # followed by the item itself, and the supplied item index
        # number.
        DistributedMailbox.notify.debug("acceptItem")

        blob = item.getBlob(store = CatalogItem.Customization)
        context = self.getCallbackContext(callback, [item, index])
        self.sendUpdate("acceptItemMessage", [context, blob, index, optional])

    def acceptInvite(self, item, acceptingIndex, callback, optional =-1):
        """Tell the AI we are accepting an invite.

        Call the callback when the AI responds. Note that acceptingIndex
        is an index to all things in the mailbox, including simple mail.
        """
        DistributedMailbox.notify.debug("acceptInvite")
        context = self.getCallbackContext(callback, [item,  acceptingIndex])
        self.sendUpdate("acceptInviteMessage", [context, item.inviteKey])

    def acceptItemResponse(self, context, retcode):
        DistributedMailbox.notify.debug("acceptItemResponse")
        if retcode == ToontownGlobals.P_UserCancelled:
            print("DistributedMailbox User Canceled")
        # Sent from the AI in response to acceptItemMessage.
        self.doCallbackContext(context, [retcode])
        
    def discardItem(self, item, index, callback, optional = -1):
        DistributedMailbox.notify.debug("discardItem")
        # Discards an item
        blob = item.getBlob(store = CatalogItem.Customization)
        context = self.getCallbackContext(callback, [item, index])
        self.sendUpdate("discardItemMessage", [context, blob, index, optional])

    def rejectInvite(self, item, acceptingIndex, callback, optional =-1):
        """Tell the AI we are rejecting an invite.

        Call the callback when the AI responds. Note that acceptingIndex
        is an index to all things in the mailbox, including simple mail.
        """
        DistributedMailbox.notify.debug("rejectInvite")
        context = self.getCallbackContext(callback, [item, acceptingIndex])
        self.sendUpdate("rejectInviteMessage", [context, item.inviteKey])        
        
    def discardItemResponse(self, context, retcode):
        DistributedMailbox.notify.debug("discardItemResponse")
        # Sent from the AI in response to acceptItemMessage.
        self.doCallbackContext(context, [retcode])

    def __setupName(self):
        DistributedMailbox.notify.debug("__setupName")

        # name on side of mailbox
        if self.nameText:
            self.nameText.removeNode()
            self.nameText = None

        nameOrigin = self.model.find('**/nameLocator')
        if not nameOrigin.isEmpty():
            text = TextNode('nameText')
            text.setTextColor(*self.nameColor)
            text.setAlign(TextNode.ACenter)
            text.setFont(ToontownGlobals.getToonFont())
            text.setWordwrap(7.5)
            text.setText(self.name)
        
            self.nameText = nameOrigin.attachNewNode(text)
            self.nameText.setH(90)
            self.nameText.setScale(0.2)

    def __clearDialog(self, event):
        DistributedMailbox.notify.debug("__clearDialog")
        self.mailboxDialog.cleanup()
        self.mailboxDialog = None
        self.freeAvatar()

    def sendInviteReadButNotReplied(self, inviteKey):
        """Tell the AI the player has seen the invite, but not replied yet."""
        self.sendUpdate("markInviteReadButNotReplied", [inviteKey])

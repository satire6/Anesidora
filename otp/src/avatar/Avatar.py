"""Avatar Module: contains the avatar class"""

from pandac.PandaModules import *
from libotp import Nametag, NametagGroup
from libotp import CFSpeech, CFThought, CFTimeout, CFPageButton, CFNoQuitButton, CFQuitButton
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from direct.actor.Actor import Actor
#import AvatarDNA
from direct.distributed import ClockDelta
from otp.avatar.ShadowCaster import ShadowCaster
import random
from otp.otpbase import OTPRender
from direct.showbase.PythonUtil import recordCreationStack

def reconsiderAllUnderstandable():
    """
    This function will walk through all the currently active avatars
    and call considerUnderstandable() on each active avatar.  It
    should be called if some fundamental property has changed that
    might affect who we can understand and who we can't.
    """
    for av in Avatar.ActiveAvatars:
        av.considerUnderstandable()

class Avatar(Actor, ShadowCaster):
    """
    Avatar class: contains methods for making actors that walk
    and talk
    """
    notify = directNotify.newCategory("Avatar")
    
    # This is the list of Avatars that are currently known
    # to the player--all those that have been recently generated, and not
    # yet deleted or disabled.
    ActiveAvatars = []    

    # by default Avatar listens for nametagAmbientLightChanged events starting at __init__
    # and stops when delete is called
    # classes that want to override this behavior and handle accepting and ignoring of
    # nametagAmbientLightChanged events should set this to True
    ManagesNametagAmbientLightChanged = False

    # special methods

    def __init__(self, other=None):
        """
        Create the toon, suit, or char specified by the dna array
        """
        self.name = "" # name is used in debugPrint.
        assert self.debugPrint("Avatar()")
        try:
            self.Avatar_initialized
            return
        except:
            self.Avatar_initialized = 1

        # create an empty actor to add parts to
        Actor.__init__(self, None, None, other, flattenable = 0, setFinal = 1)
        ShadowCaster.__init__(self)

        # The default font.
        self.__font = OTPGlobals.getInterfaceFont()

        self.soundChatBubble = None
        
        # Holds Type of Avatar
        self.avatarType = ""

        self.nametagNodePath = None
        
        # Set up a nametag (actually, a group of nametags,
        # including a Nametag2d and a Nametag3d) for the avatar.
        # The nametag won't be visible until it is managed, which
        # will happen during addActive().
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        self.nametag.setFont(OTPGlobals.getInterfaceFont())
        self.nametag2dContents = Nametag.CName | Nametag.CSpeech
        # nametag2dDist is changed only by DistributedAvatar.
        self.nametag2dDist = Nametag.CName | Nametag.CSpeech
        self.nametag2dNormalContents = Nametag.CName | Nametag.CSpeech

        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag3d.setLightOff()

        #Accept ambient lighting changes
        if self.ManagesNametagAmbientLightChanged:
            self.acceptNametagAmbientLightChange()

        # do not display in reflections
        OTPRender.renderReflection (False, self.nametag3d, 'otp_avatar_nametag', None)

        # But do show in shadows, except for the nametag.
        self.getGeomNode().showThrough(OTPRender.ShadowCameraBitmask)
        self.nametag3d.hide(OTPRender.ShadowCameraBitmask)

        self.collTube = None
        self.battleTube = None
        
        # set some initial values
        self.scale = 1.0
        self.nametagScale = 1.0
        self.height = 0.0
        self.battleTubeHeight = 0.0
        self.battleTubeRadius = 0.0
        self.style = None

        # commonChatFlags is a bitmask that may include the CommonChat
        # and SuperChat bits.
        self.commonChatFlags = 0

        # This is either CCNonPlayer, CCSuit, or CCNormal,
        # according to whether there's a human behind the avatar
        # or not.  This determines the color nametag that is
        # assigned, as well as whether chat messages from this
        # avatar will be garbled.
        self.understandable = 1
        self.setPlayerType(NametagGroup.CCNormal)

        self.ghostMode = 0
        
        # Page chat private vars
        self.__chatParagraph = None
        self.__chatMessage = None
        self.__chatFlags = 0
        self.__chatPageNumber = None
        self.__chatAddressee = None
        self.__chatDialogueList = []
        self.__chatSet = 0
        self.__chatLocal = 0
        # Record current dialogue so it can be interrupted the
        # next time the avatar talks
        self.__currentDialogue = None

        # since whiteListChatFlags is not a required field, init it just in case
        self.whitelistChatFlags = 0
        

    def delete(self):
        try:
            self.Avatar_deleted
        except:
            # masad: delete nametag before actor removes me
            self.deleteNametag3d()
            Actor.cleanup(self)
            if self.ManagesNametagAmbientLightChanged:
                self.ignoreNametagAmbientLightChange()
            self.Avatar_deleted = 1
            del self.__font
            del self.style
            del self.soundChatBubble
            del self.nametag
            self.nametag3d.removeNode()
            ShadowCaster.delete(self)
            Actor.delete(self)

    def acceptNametagAmbientLightChange(self):
        self.accept("nametagAmbientLightChanged", self.nametagAmbientLightChanged)
    def ignoreNametagAmbientLightChange(self):
        self.ignore("nametagAmbientLightChanged")

    def isLocal(self):
        return 0

    def isPet(self):
        return False

    def isProxy(self):
        return False

    def setPlayerType(self, playerType):
        """
        setPlayerType(self, NametagGroup.ColorCode playerType)

        Indicates whether the avatar is a human player
        (NametagGroup.CCNormal), a friendly non-player character
        (NametagGroup.CCNonPlayer), or a suit (NametagGroup.CCSuit).
        This determines the color of the nametag, as well as whether
        chat messages from this avatar should be garbled.
        """
        self.playerType = playerType

        if not hasattr(self,'nametag'):
            self.notify.warning('no nametag attributed, but would have been used.')
            return
        if self.isUnderstandable():
            self.nametag.setColorCode(self.playerType)
            #self.nametag.setColorCode(NametagGroup.CCFreeChat)
        else:
            self.nametag.setColorCode(NametagGroup.CCNoChat)


    def setCommonChatFlags(self, commonChatFlags):
        """setCommonChatFlags(self, uint8)
        Reset the common chat flags.
        """

        self.commonChatFlags = commonChatFlags
        self.considerUnderstandable()

        if self == base.localAvatar:
            # If we change the common chat flags on localtoon, that
            # affects everyone.
            reconsiderAllUnderstandable()

    def setWhitelistChatFlags(self, whitelistChatFlags):
        """setCommonChatFlags(self, uint8)
        Reset the common chat flags.
        """
        self.whitelistChatFlags = whitelistChatFlags
        self.considerUnderstandable()

        if self == base.localAvatar:
            # If we change the common chat flags on localtoon, that
            # affects everyone.
            reconsiderAllUnderstandable()            


    def considerUnderstandable(self):
        """
        Updates the "understandable" flag according to whether the
        local toon has permission to hear this avatar's chat messages
        or not (and vice-versa).

        Some of this code is duplicated in FriendHandle.isUnderstandable().
        """
        speed = 0
        if self.playerType in  (NametagGroup.CCNormal, NametagGroup.CCFreeChat, NametagGroup.CCSpeedChat):
            self.setPlayerType(NametagGroup.CCSpeedChat)
            speed = 1
        if hasattr(base,'localAvatar') and self == base.localAvatar:
            # This *is* the local toon.  OK, one can always understand
            # oneself.
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCFreeChat)
        elif self.playerType == NametagGroup.CCSuit:
            # It's a suit!
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCSuit)
        elif self.playerType not in  (NametagGroup.CCNormal, NametagGroup.CCFreeChat, NametagGroup.CCSpeedChat):
            # It's not a player character.
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCNoChat)
        elif hasattr(base,'localAvatar') and (self.commonChatFlags & base.localAvatar.commonChatFlags & OTPGlobals.CommonChat):
            # Both this avatar and the local toon have common chat
            # permission.  OK.
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCFreeChat)
        elif self.commonChatFlags & OTPGlobals.SuperChat:
            # This avatar has "super chat" permission, so anyone
            # can understand him.  OK.
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCFreeChat)
        elif hasattr(base,'localAvatar') and (base.localAvatar.commonChatFlags & OTPGlobals.SuperChat):
            # Local toon has "super chat" permission, so we can
            # understand everyone.  OK.
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCFreeChat)
        elif base.cr.getFriendFlags(self.doId) & OTPGlobals.FriendChat:
            # This avatar is a special friend of the local toon.  OK.
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCFreeChat)
        elif base.cr.playerFriendsManager.findPlayerIdFromAvId(self.doId) is not None:
            # This is the avatar of my player friend.  Is the player friendship open chat?
            playerInfo = base.cr.playerFriendsManager.findPlayerInfoFromAvId(self.doId)
            if playerInfo.openChatFriendshipYesNo:
                self.understandable = 1                
                self.nametag.setColorCode(NametagGroup.CCFreeChat)
            elif playerInfo.isUnderstandable():
                self.understandable = 1
            else:
                self.understandable = 0
        elif hasattr(base,'localAvatar') and (self.whitelistChatFlags & base.localAvatar.whitelistChatFlags):
             # Both this avatar and the local toon have whitelist chat
             # permission.  OK.
             self.understandable = 1
        else:
            # Too bad.
            self.understandable = 0
        
        #if self.understandable:
        if not hasattr(self,'nametag'):
            self.notify.warning('no nametag attributed, but would have been used')
        else:
            self.nametag.setColorCode(self.playerType)
        #else:
        #    self.nametag.setColorCode(NametagGroup.CCNoChat)

    def isUnderstandable(self):
        """
        Returns true if this avatar can chat freely with localtoon,
        false otherwise.
        """
        return self.understandable

    # These need to be defined in child class for each type of avatar
    def setDNAString(self, dnaString):
        assert self.notify.error("called setDNAString on parent class")

    def setDNA(self, dna):
        assert self.notify.error("called setDNA on parent class")

    # accessing

    def getAvatarScale(self):
        """
        Return the avatar's scale
        """
        return self.scale

    def setAvatarScale(self, scale):
        """
        Set the avatar's scale.  This both sets the scale on the
        NodePath, and also stores it for later retrieval, not to
        mention fiddling with the nametag to keep everything
        consistent.  You should use this call to adjust the avatar's
        scale, instead of adjusting it directly.
        """
        if self.scale != scale:
            self.scale = scale
            self.getGeomNode().setScale(scale)
            self.setHeight(self.height)

    def getNametagScale(self):
        """
        Return the nametag's overall scale.  This value does not
        change in response to camera position.
        """
        return self.nametagScale

    def setNametagScale(self, scale):
        """
        Sets the scale of the 3-d nametag floating over the avatar's
        head.  The nametags will also be scaled in response to the
        camera position, but this gives us an overall scale.
        """
        self.nametagScale = scale
        self.nametag3d.setScale(scale)

    def adjustNametag3d(self,parentScale=1.0):
        """adjustNametag3d(self)
        Adjust nametag according to the height
        """
        self.nametag3d.setPos(0, 0, self.height + 0.5)

    def getHeight(self):
        """
        Return the avatar's height
        """
        return self.height

    def setHeight(self, height):
        """setHeight(self, float)
        Set the avatar's height.
        """
        # The height as it is currently designed has already been
        # scaled by the avatar's scale, so we have to compensate for
        # this.
        self.height = height
        self.adjustNametag3d()
        if self.collTube:
            self.collTube.setPointB(0, 0, height - self.getRadius())
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0,0,height - self.getRadius())

    def getRadius(self):
        """
        Returns the radius of the avatar's collision tube.
        """
        return OTPGlobals.AvatarDefaultRadius

    def getName(self):
        """
        Return the avatar's name
        """
        return self.name

    def getType(self):
        """
        Return the avatar's Type
        """
        return self.avatarType
    
    def setName(self, name):
        """
        name is a string
        
        Set the avatar's name
        """
        # if we are disguised, don't mess up our custom nametag
        if hasattr(self, "isDisguised"):
            if self.isDisguised:
                return

        self.name = name
        if hasattr(self, "nametag"):
            self.nametag.setName(name)

    def setDisplayName(self, str):
        # Sets the name that is displayed in the 3-d and 2-d nametags,
        # but not the name that is used to prefix chat messages.

        # if we are disguised, don't mess up our custom nametag
        if hasattr(self, "isDisguised"):
            if self.isDisguised:
                return

        self.nametag.setDisplayName(str)

    def getFont(self):
        """
        Returns the font used to display the avatar's name and chat
        messages.
        """
        return self.__font

    def setFont(self, font):
        """
        Changes the font used to display the avatar's name and chat
        messages.
        """
        self.__font = font
        self.nametag.setFont(font)

    def getStyle(self):
        """
        Return the dna string for the avatar
        """
        return self.style

    def setStyle(self, style):
        """setStyle(self, AvatarDNA)
        Set the dna string for the avatar
        """
        self.style = style



    ### play dialog sounds ###

    def getDialogueArray(self):
        # Inheritors should override
        return None

    def playCurrentDialogue(self, dialogue, chatFlags, interrupt = 1):
        if interrupt and (self.__currentDialogue is not None):
            self.__currentDialogue.stop()
        self.__currentDialogue = dialogue
        # If an AudioSound has been passed in, play that for dialog to
        # go along with the chat.  Interrupt any sound effect currently playing
        if dialogue:
            base.playSfx(dialogue, node=self)
        # If it is a speech-type chat message, and the avatar isn't
        # too far away to hear, play the appropriate sound effect.
        elif ((chatFlags & CFSpeech) != 0 and 
            self.nametag.getNumChatPages() > 0):
            # play the dialogue sample

            # We use getChat() instead of chatString, which
            # returns just the current page of a multi-page chat
            # message.  This way we aren't fooled by long pages
            # that end in question marks.
            self.playDialogueForString(self.nametag.getChat())
            if (self.soundChatBubble != None):
                base.playSfx(self.soundChatBubble, node=self)
    
    def playDialogueForString(self, chatString):
        """
        Play dialogue samples to match the given chat string
        """
        # use only lower case for searching
        searchString = chatString.lower()
        # determine the statement type
        if (searchString.find(OTPLocalizer.DialogSpecial) >= 0):
            # special sound
            type = "special"
        elif (searchString.find(OTPLocalizer.DialogExclamation) >= 0):
            #exclamation
            type = "exclamation"
        elif (searchString.find(OTPLocalizer.DialogQuestion) >= 0):
            # question
            type = "question"
        else:
            # statement (use two for variety)
            if random.randint(0, 1):
                type = "statementA"
            else:
                type = "statementB"

        # determine length
        stringLength = len(chatString)
        if (stringLength <= OTPLocalizer.DialogLength1):
            length = 1
        elif (stringLength <= OTPLocalizer.DialogLength2):
            length = 2
        elif (stringLength <= OTPLocalizer.DialogLength3):
            length = 3
        else:
            length = 4

        self.playDialogue(type, length)

    def playDialogue(self, type, length):
        """playDialogue(self, string, int)
        Play the specified type of dialogue for the specified time
        """

        # Inheritors may override this function or getDialogueArray(),
        # above.
        
        # Choose the appropriate sound effect.
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        
        sfxIndex = None
        if (type == "statementA" or type == "statementB"):
            if (length == 1):
                sfxIndex = 0
            elif (length == 2):
                sfxIndex = 1
            elif (length >= 3):
                sfxIndex = 2
        elif (type == "question"):
            sfxIndex = 3
        elif (type == "exclamation"):
            sfxIndex = 4
        elif (type == "special"):
            sfxIndex = 5
        else:
            notify.error("unrecognized dialogue type: ", type)

        if sfxIndex != None and sfxIndex < len(dialogueArray) and \
           dialogueArray[sfxIndex] != None:
            base.playSfx(dialogueArray[sfxIndex], node=self)

    def getDialogueSfx(self, type, length):
        """Return the correspoinding AudioSound to type and length, None if error."""
        retval = None
        # Choose the appropriate sound effect.
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return None
        
        sfxIndex = None
        if (type == "statementA" or type == "statementB"):
            if (length == 1):
                sfxIndex = 0
            elif (length == 2):
                sfxIndex = 1
            elif (length >= 3):
                sfxIndex = 2
        elif (type == "question"):
            sfxIndex = 3
        elif (type == "exclamation"):
            sfxIndex = 4
        elif (type == "special"):
            sfxIndex = 5
        else:
            notify.error("unrecognized dialogue type: ", type)

        if sfxIndex != None and sfxIndex < len(dialogueArray) and \
           dialogueArray[sfxIndex] != None:
            retval =dialogueArray[sfxIndex]

        return retval

    def setChatAbsolute(self, chatString, chatFlags, dialogue = None, interrupt = 1):
        """
        Receive the chat string, play dialogue if in range, display
        the chat message and spawn task to reset the chat message
        """
        self.nametag.setChat(chatString, chatFlags)

        # Update current dialogue, first making sure and active dialogue
        # is stopped first
        self.playCurrentDialogue(dialogue, chatFlags, interrupt)
        
    def setChatMuted(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        """
        This method is a modification of setChatAbsolute in Toontown in which
        just the text of the chat is displayed on the nametag.
        No animal sound is played along with it.
        This method is defined in toontown/src/toon/DistributedToon.
        """
        pass
    
    def displayTalk(self, chatString):
        if not base.cr.avatarFriendsManager.checkIgnored(self.doId):
            if base.talkAssistant.isThought(chatString):
                self.nametag.setChat(base.talkAssistant.removeThoughtPrefix(chatString), CFThought)
            else:
                self.nametag.setChat(chatString, CFSpeech | CFTimeout)
        

    def clearChat(self):
        """
        Clears the last chat message
        """
        self.nametag.clearChat()
    
    # util
    
    def isInView(self):
        """
        Check to see if avatar is in view. Use a point near the eye height
        to perform the test
        """
        pos = self.getPos(camera)
        eyePos = Point3(pos[0], pos[1], pos[2] + self.getHeight())
        return base.camNode.isInView(eyePos)
                                  
    # name methods

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool

        if bool:
            self.showName()
        if not (bool):
            self.hideName()

    def hideName(self):
        # Hiding the name only means hiding the 3-d name from the
        # nametag.  Speech balloons, and the 2-d nametag, remain.
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if self.__nameVisible and not self.ghostMode:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def hideNametag2d(self):
        """
        Temporarily hides the onscreen 2-d nametag.
        """
        self.nametag2dContents = 0
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def showNametag2d(self):
        """
        Reveals the onscreen 2-d nametag after a previous call to
        hideNametag2d.
        """
        self.nametag2dContents = self.nametag2dNormalContents
        if self.ghostMode:
            self.nametag2dContents = Nametag.CSpeech

        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def hideNametag3d(self):
        """
        Temporarily hides the 3-d nametag.
        """
        self.nametag.getNametag3d().setContents(0)

    def showNametag3d(self):
        """
        Reveals the 3-d nametag after a previous call to
        hideNametag3d.
        """
        if self.__nameVisible and not self.ghostMode:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)
        else:
            self.nametag.getNametag3d().setContents(0)

    def setPickable(self, flag):
        """
        Indicates whether the avatar can be picked by clicking on him
        or his nametag.
        """
        self.nametag.setActive(flag)

    def clickedNametag(self):
        """
        This hook is called whenever the user clicks on the nametag
        associated with this particular avatar (or, rather, clicks on
        the avatar itself).  It simply maps that C++-generated event
        into a Python event that includes the avatar as a parameter.
        """
        # If we have a button, we don't generate the normal clicked
        # nametag event; instead, we just advance the page (or clear
        # the chat on the last page).
        if self.nametag.hasButton():
            self.advancePageNumber()
        # Only throw the click event if the nametag is active. This
        # prevents a subtle error when double-clicking on a nametag
        # with a button in the same frame. 
        elif self.nametag.isActive():
            # No page button, so just click on the nametag normally.
            messenger.send("clickedNametag", [self])
        else:
            pass

    def setPageChat(self, addressee, paragraph, message, quitButton, extraChatFlags = None, dialogueList = [], pageButton = True):
        """
        setPageChat(self, int addressee, int paragraph, string message, bool quitButton, list dialogueList)

        The NPC is giving instruction or quest information to a
        particular Toon, which may involve multiple pages of text that
        the user must click through.

        The paragraph number indicates a unique number for the
        particular paragraph that is being spoken, and the addressee
        is the particular Toon that is being addressed.  Only the
        indicated Toon will be presented with the click-through
        buttons.

        This is normally called by the client from within a movie; it
        is not a message in its own right.
        """
        self.__chatAddressee = addressee
        self.__chatPageNumber = None
        self.__chatParagraph = paragraph
        self.__chatMessage = message
        if extraChatFlags is None:
            self.__chatFlags = CFSpeech
        else:
            self.__chatFlags = CFSpeech | extraChatFlags
        self.__chatDialogueList = dialogueList
        self.__chatSet = 0
        self.__chatLocal = 0
        self.__updatePageChat()

        if addressee == base.localAvatar.doId:
            # The chat message is addressed to us.
            if (pageButton):
                self.__chatFlags |= CFPageButton
            if quitButton == None:
                self.__chatFlags |= CFNoQuitButton
            elif quitButton:
                self.__chatFlags |= CFQuitButton

            # Since this is our own message, start out at the first
            # page.
            self.b_setPageNumber(self.__chatParagraph, 0)

    def setLocalPageChat(self, message, quitButton, extraChatFlags = None, dialogueList = []):
        """
        setLocalPageChat(self, string message, bool quitButton, list dialogueList)

        Locally sets up a multiple-page chat message.  This is
        intended for use when the NPC is giving advice to the toon in
        a local context, e.g. in the Tutorial.

        If quitButton is 1, a red cancel button will be drawn in the
        place of the page advance arrow on the last page.  If
        quitButton is 0, a page advance arrow will be drawn on the
        last page.  If quitButton is None, no button at all will be
        drawn on the last page.
        """
        self.__chatAddressee = base.localAvatar.doId
        self.__chatPageNumber = None
        self.__chatParagraph = None
        self.__chatMessage = message
        if extraChatFlags is None:
            self.__chatFlags = CFSpeech
        else:
            self.__chatFlags = CFSpeech | extraChatFlags
        self.__chatDialogueList = dialogueList
        self.__chatSet = 1
        self.__chatLocal = 1

        self.__chatFlags |= CFPageButton
        if quitButton == None:
            self.__chatFlags |= CFNoQuitButton
        elif quitButton:
            self.__chatFlags |= CFQuitButton

        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None

        self.setChatAbsolute(message, self.__chatFlags, dialogue)
        self.setPageNumber(None, 0)
        
    def setPageNumber(self, paragraph, pageNumber, timestamp = None):
        """
        setPageNumber(self, int paragraph, int pageNumber)

        This message is generated by the client when the advance-page
        button is clicked.  All clients also receive this message.
        When the pageNumber is -1, the last page has been cleared.
        """
        if timestamp == None:
            elapsed = 0.0
        else:
            elapsed = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        
        self.__chatPageNumber = [paragraph, pageNumber]
        self.__updatePageChat()

        if hasattr(self, "uniqueName"):
            # If you are derived from DistributedObjectAI
            if pageNumber >= 0:
                messenger.send(self.uniqueName("nextChatPage"),
                               [pageNumber, elapsed])
            else:
                messenger.send(self.uniqueName("doneChatPage"),
                               [elapsed])
        else:
            # If you are not derived from DistributedObjectAI
            if pageNumber >= 0:
                messenger.send("nextChatPage", [pageNumber, elapsed])
            else:
                messenger.send("doneChatPage", [elapsed])
            

    def advancePageNumber(self):
        """
        Advances the page for the previously-spoken pageChat message.
        This is a distributed call.  This is normally called only in
        response to the user clicking on the next-page button for the
        message directed to himself.
        """
        if self.__chatAddressee == base.localAvatar.doId and \
           self.__chatPageNumber != None and \
           self.__chatPageNumber[0] == self.__chatParagraph:
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                pageNumber += 1
                if pageNumber >= self.nametag.getNumChatPages():
                    # Last page; clear the chat.
                    pageNumber = -1

                if self.__chatLocal:
                    # If it's a local chat, just set the page number locally.
                    self.setPageNumber(self.__chatParagraph, pageNumber)
                else:
                    # Otherwise, distribute the page number.
                    self.b_setPageNumber(self.__chatParagraph, pageNumber)

    def __updatePageChat(self):
        """
        Updates the nametag to display the appropriate paging chat
        message, if all parameters are now available.
        """
        if (self.__chatPageNumber != None
                and self.__chatPageNumber[0] == self.__chatParagraph):
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                if not self.__chatSet:
                    # First time around use setChatAbsolute to play dialogue
                    # if specified, otherwise pass in None so that appropriate
                    # default dialogue sfx is used
                    if len(self.__chatDialogueList) > 0:
                        dialogue = self.__chatDialogueList[0]
                    else:
                        dialogue = None
                    self.setChatAbsolute(self.__chatMessage, self.__chatFlags,
                                         dialogue)
                    self.__chatSet = 1
                if pageNumber < self.nametag.getNumChatPages():
                    self.nametag.setPageNumber(pageNumber)
                    # For all chat pages beyond the first one, play
                    # appropriate dialogue sfx
                    if (pageNumber > 0):
                        if (len(self.__chatDialogueList) > pageNumber):
                            dialogue = self.__chatDialogueList[pageNumber]
                        else:
                            dialogue = None
                        self.playCurrentDialogue(dialogue, self.__chatFlags)
                else:
                    self.clearChat()
            else:
                self.clearChat()


    def getAirborneHeight(self):
        """
        Get  the avatar height from the ground. 
        """
        assert self.shadowPlacer
        height = self.getPos(self.shadowPlacer.shadowNodePath)
        # If the shadow where not pointed strait down, we would need to
        # get magnitude of the vector.  Since it is strait down, we'll
        # just get the z:
        #spammy --> assert self.debugPrint("getAirborneHeight() returning %s"%(height.getZ(),))
        return height.getZ() + 0.025

    def initializeNametag3d(self):
        """
        Put the 3-d nametag in the right place over the avatar's head.
        This is normally done at some point after initialization,
        after the NametagGroup in self.nametag has already been
        created.  This is mainly just responsible for finding the
        right node or nodes to parent the 3-d nametag to.
        """
        # Protect this function from being called twice by removing
        # the old ones first.
        self.deleteNametag3d()

        # Nowadays, there is only one nametag3d, and it is a direct
        # child of the Avatar node.  (For a while, we had a separate
        # nametag for each LOD, parented deep within the hierarchy.)
        nametagNode = self.nametag.getNametag3d()
        self.nametagNodePath = self.nametag3d.attachNewNode(nametagNode)
        iconNodePath = self.nametag.getNameIcon()

        # We also want to animate the nametag appropriately.  This
        # means we grab the appropriate CharacterJoint object for each
        # LOD and point it at this node (instead of wherever it was
        # pointed before).
        for cJoint in self.getNametagJoints():
            cJoint.clearNetTransforms()
            cJoint.addNetTransform(nametagNode)

        
    def nametagAmbientLightChanged(self,newlight):
        """
        Get new ambient light when this avatar has changed locations/TODmanagers
        """
        self.nametag3d.setLightOff()
        if newlight:
            self.nametag3d.setLight(newlight)
            
##     def deleteNametag3d(self):
##         """
##         Lose the 3-d nametag
##         """
##         children = self.nametag3d.getChildren()
##         for i in range(children.getNumPaths()):
##             children[i].removeNode()

    def deleteNametag3d(self):
        """
        Lose the 3-d nametag
        """
        if(self.nametagNodePath):
            self.nametagNodePath.removeNode()
            self.nametagNodePath = None

    def initializeBodyCollisions(self, collIdStr):
        # Nowadays the body collisions for avatars other than
        # localToon are a tube.
        self.collTube = CollisionTube(0, 0, 0.5,
                                      0, 0, self.height - self.getRadius(),
                                      self.getRadius())
        self.collNode = CollisionNode(collIdStr)
        self.collNode.addSolid(self.collTube)
        self.collNodePath = self.attachNewNode(self.collNode)
        
        if self.ghostMode:
            self.collNode.setCollideMask(OTPGlobals.GhostBitmask)
        else:
            self.collNode.setCollideMask(OTPGlobals.WallBitmask)

    def stashBodyCollisions(self):
        if hasattr(self, "collNodePath"):
            self.collNodePath.stash()

    def unstashBodyCollisions(self):
        if hasattr(self, "collNodePath"):
            self.collNodePath.unstash()

    def disableBodyCollisions(self):
        if hasattr(self, "collNodePath"):
            self.collNodePath.removeNode()
            del self.collNodePath

        self.collTube = None

    def addActive(self):
        """
        Adds the avatar to the list of currently-active avatars.
        """
        if (base.wantNametags):
            assert self.notify.debug('Adding avatar %s' % self.getName())
            
            # Just in case it was already there through some screw-up.
            try:
                Avatar.ActiveAvatars.remove(self)
            except ValueError:
                pass
            
            Avatar.ActiveAvatars.append(self)
            self.nametag.manage(base.marginManager)

            # Generate a useful event when someone clicks on our nametag.
            self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        """
        Removes the avatar from the list of currently-active avatars.
        """
        if (base.wantNametags):
            assert self.notify.debug('Removing avatar %s' % self.getName())
            try:
                Avatar.ActiveAvatars.remove(self)
            except ValueError:
                assert self.notify.warning("%s was not present..." % self.getName())

            self.nametag.unmanage(base.marginManager)
            self.ignore(self.nametag.getUniqueId())
    
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug("%s %s %s"%(id(self), self.name, message))

    def loop(self, animName, restart=1, partName=None,fromFrame=None, toFrame=None):
        return Actor.loop(self,animName,restart,partName,fromFrame,toFrame)

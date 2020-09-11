
#from pandac.PandaModules import BitMask32, Point3, TextNode

# Several other files that import this file assume we will import all
# of PandaModules.
from pandac.PandaModules import *

#### ZONE IDs ####
# Quiet zone ... The zone you go to when you transition between neighborhoods
QuietZone = 1
# Uber zone ... The zone that every client is in all the time
UberZone = 2

# These are the collision bits we use for various meanings.

# Physical walls that the avatar can't walk through:
WallBitmask = BitMask32(0x01)

# The floor polygons--triggering zone changes and setting the height
# above the ground:
FloorBitmask = BitMask32(0x02)

# Collision polygons for the camera--things the camera can't see
# through and shouldn't lurk behind.
CameraBitmask = BitMask32(0x04)

# Collision polygons that should fade out when they come between the
# camera and the avatar
CameraTransparentBitmask = BitMask32(0x08)

# Collision polygons for moving platforms (normally these are not seen
# by the player; this helps the collision system do the right thing;
# toons that are not on the platform do not react to this bit mask):
SafetyNetBitmask = BitMask32(0x200)
# Collision polygons for _near_ moving platforms (normally these are 
# not seen by the player; this helps the collision system do the 
# right thing; toons that _are_ on the platform do not react to 
# this bit mask):
SafetyGateBitmask = BitMask32(0x400)

# These are things a ghost will bump into:
GhostBitmask = BitMask32(0x800)

# Used for path finding between ray and mesh
PathFindingBitmask = BitMask32.bit(29)

# Determined empirically
# Do not change this one
OriginalCameraFov = 52.0 
# Feel free to override this when you need to
# But set it back to the original when you are done
DefaultCameraFov = 52.0 

# This should actually be 280, but the sky does not fit inside
# so I am temporarily cranking it up
DefaultCameraFar = 400.0

# note: camera collision sphere is assumed to be 1.0 currently
DefaultCameraNear = 1.0

# task priority of standard per-zone collision pass on the AI
AICollisionPriority = 10
# task priority of collision-sphere 'move to Z=0' task (for pet collisions)
# Should run after objects have been moved, and before the collision pass
AICollMovePriority = 8

# The maximum number of toon (avatar) friends you can have at any one time on your
# friends list.  This must match a number that the server also keeps.
MaxFriends = 50

# The maximum number of player (account) friends you can have at any one time on your
# friends list.  This must match a number that the server also keeps.
MaxPlayerFriends = 300


# How many items can we carry on the back catalog?
MaxBackCatalog = 48

# Bits for the friend flags.  Presently, we only use bit 1.
FriendChat = 1

# Bits for the DistributedAvatar.commonChat word.
CommonChat = 1
SuperChat = 2

# Maximum number of custom chat phrases
MaxCustomMessages = 25

# Tokens for the various nodes we can parent avatars to via
# distributed setParent().
SPInvalid = 0 # ParentMgr does not allow default values to be used as parent tokens
SPHidden = 1
SPRender = 2
SPDynamic = 5

# Cheesy rendering effects for Toons
CENormal = 0
CEBigHead = 1
CESmallHead = 2
CEBigLegs = 3
CESmallLegs = 4
CEBigToon = 5
CESmallToon = 6
CEFlatPortrait = 7
CEFlatProfile = 8
CETransparent = 9
CENoColor = 10
CEInvisible = 11
CEPumpkin = 12
CEBigWhite = 13
CESnowMan = 14
# This one is not really a cheesy effect, but it is implemented by the
# cheesy effect system.  It's a string rather than a number to ensure
# that no one cheats and asks for this via the cheesy effect
# distributed message.
CEGhost = 'g'

# How big is big and how small is small?
BigToonScale = 1.5
SmallToonScale = 0.5

# Reasons for the client to disconnect from the server and/or AI.
DisconnectUnknown = 0  # e.g. connection lost, client machine rebooted
DisconnectBookExit = 1
DisconnectCloseWindow = 2
DisconnectPythonError = 3
DisconnectSwitchShards = 4
DisconnectGraphicsError = 5

DisconnectReasons = {
    DisconnectUnknown: "unknown",
    DisconnectBookExit: "book exit",
    DisconnectCloseWindow: "closed window",
    DisconnectPythonError: "python error",
    DisconnectSwitchShards: "switch shards",
    DisconnectGraphicsError: "graphics error",
    }

# Timeouts on waiting for database responses.  These are just to
# prevent users from seeing a black screen if the database happens to
# be down and isn't responding to queries.

# Pop up a warning dialog after this amount of time.
DatabaseDialogTimeout = 20.0

# Give up altogether after this amount of additional time.
DatabaseGiveupTimeout = 45.0

# When the user has a limited number of minutes per month, pop up
# warning messages this many seconds before his time is about to
# expire and he gets booted.
PeriodTimerWarningTime = (600, 300, 60)

# How fast must we move before we start to walk?
WalkCutOff = 0.5

# How fast must we move before we break into a run cycle?
RunCutOff = 8.0

# How far above the floor should we stand to prevent our drop shadow
# from flickering?
FloorOffset = 0.025

# What should the default radius be for an avatar's collision tube/sphere?
AvatarDefaultRadius = 1

# Global values that need to be established by the particular game
# (these act like pure virtual functions for API purposes)
InterfaceFont = None
InterfaceFontPath = None
SignFont = None
SignFontPath = None
FancyFont = None
FancyFontPath = None
NametagFonts = {}
NametagFontPaths = {}
DialogClass = None
GlobalDialogClass = None
ProductPrefix = None

# Fonts.  These are functions rather than constants, so we can control
# when they get loaded.
def getInterfaceFont():
    global InterfaceFont
    if (InterfaceFont == None):
        if InterfaceFontPath == None:
            InterfaceFont = TextNode.getDefaultFont()
        else:
            InterfaceFont = loader.loadFont(InterfaceFontPath, lineHeight = 1.0)
    return InterfaceFont

def setInterfaceFont(path):
    global InterfaceFont
    global InterfaceFontPath
    InterfaceFontPath = path
    InterfaceFont = None

def getSignFont():
    global SignFont
    if (SignFont == None):
        if SignFontPath == None:
            InterfaceFont = TextNode.getDefaultFont()
            SignFont = TextNode.getDefaultFont()
        else:
            SignFont = loader.loadFont(SignFontPath, lineHeight = 1.0)
    return SignFont

def setSignFont(path):
    global SignFontPath
    SignFontPath = path
    
    
def getFancyFont():
    global FancyFont
    if (FancyFont == None):
        if FancyFontPath == None:
            InterfaceFont = TextNode.getDefaultFont()
            FancyFont = TextNode.getDefaultFont()
        else:
            FancyFont = loader.loadFont(FancyFontPath, lineHeight = 1.0)
    return FancyFont

def setFancyFont(path):
    global FancyFontPath
    FancyFontPath = path
    
    
def getNametagFont(index):
    global NametagFonts
    if ((not NametagFonts.has_key(index) )or NametagFonts[index] == None):
        if (not NametagFontPaths.has_key(index) ) or (NametagFontPaths[index] == None):
            InterfaceFont = TextNode.getDefaultFont()
            NametagFonts[index] = TextNode.getDefaultFont()
        else:
            NametagFonts[index] = loader.loadFont(NametagFontPaths[index], lineHeight = 1.0)
    return NametagFonts[index]

def setNametagFont(index, path):
    global NametagFontPaths
    NametagFontPaths[index] = path    
    
    

def getDialogClass():
    global DialogClass
    
    if DialogClass == None:
        from otp.otpgui.OTPDialog import OTPDialog
        DialogClass = OTPDialog
        
    return DialogClass

def getGlobalDialogClass():
    global GlobalDialogClass
    
    if DialogClass == None:
        from otp.otpgui.OTPDialog import GlobalDialog
        GlobalDialogClass = GlobalDialog

    return GlobalDialogClass

def setDialogClasses(dialogClass, globalDialogClass):
    global DialogClass
    DialogClass = dialogClass
    global GlobalDialogClass
    GlobalDialogClass = globalDialogClass

def getDefaultProductPrefix():
    return ProductPrefix

def setDefaultProductPrefix(prefix):
    global ProductPrefix
    ProductPrefix = prefix

NetworkLatency = 1.0

# Needed to bump this up from 9.0 to accommodate accounts that were
# created before we changed to the new TTF font.  Some of these
# account names that previously fit within 9.0 may be just a little
# bit wider now.
# Note: this width is used for both the username and password entries.
maxLoginWidth = 9.1

# Indices into standWalkRunReverse, and also return values from setSpeed().
STAND_INDEX = 0
WALK_INDEX = 1
RUN_INDEX = 2
REVERSE_INDEX = 3
STRAFE_LEFT_INDEX = 4
STRAFE_RIGHT_INDEX = 5

ToonStandableGround = 0.707 # if ToonStandableGround > angle: toon is on ground.

ToonForwardSpeed = 16.0 # feet per second
ToonJumpForce = 24.0 # feet per second
ToonReverseSpeed = 8.0 # feet per second
ToonRotateSpeed = 80.0

# When you are "dead"
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0 # feet per second
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0

MickeySpeed = 5.0 # feet per second
MinnieSpeed = 3.2 # feet per second
#DonaldSpeed = 4.6 # feet per second
DonaldSpeed = 3.68 # feet per second
GoofySpeed  = 5.2 # feet per second
PlutoSpeed  = 5.5 # feet per second per second

ThinkPosHotkey = "shift-f1"
PlaceMarkerHotkey = "f2"
FriendsListHotkey = "f7"
StickerBookHotkey = "f8"
OptionsPageHotkey = "escape"
ScreenshotHotkey = "f9"
SynchronizeHotkey = "shift-f6"
QuestsHotkeyOn = "end"
QuestsHotkeyOff = "end-up"
InventoryHotkeyOn = "home"
InventoryHotkeyOff = "home-up"
DetectGarbageHotkey = 'shift-f11'
PrintCamPosHotkey = "f12"   # just for dbging

GlobalDialogColor = (1, 1, 0.75, 1)

# This is what the background color should be when we don't explicity
# set it to something else.  It really shouldn't matter, since in most
# places the user never sees outer space.
DefaultBackgroundColor = (0.3, 0.3, 0.3, 1)

# Various scales and parameters for Toon.py

# These scales came from Bruce's line-up. The body scales were globally 
# reduced by about 10 percent to get the overall height he wanted
toonBodyScales = {
    'mouse':  0.60,
    'cat':    0.73,
    'duck':   0.66,
    'rabbit': 0.74,
    'horse':  0.85,
    'dog':    0.85,
    'monkey': 0.68,
    'bear':   0.85,
    'pig':    0.77
    }

# These are vec3s since they are non uniform
toonHeadScales = {
    # Nowadays these scales are built into the models.
    #    'mouse':  Point3(1.3078, 1.1274, 1.1274),
    #    'cat':    Point3(1.1250),
    #    'duck':   Point3(1.345, 1.1298, 1.3292),
    #    'rabbit': Point3(1.0000),
    #    'horse':  Point3(1.0000),
    #    'dog':    Point3(1.0857),
    'mouse':  Point3(1.0),
    'cat':    Point3(1.0),
    'duck':   Point3(1.0),
    'rabbit': Point3(1.0),
    'horse':  Point3(1.0),
    'dog':    Point3(1.0),
    'monkey': Point3(1.0),
    'bear':   Point3(1.0),
    'pig':    Point3(1.0)
    }

legHeightDict = {
    's': 1.5,
    'm': 2.0,
    'l': 2.75,
    }
torsoHeightDict = {
    's': 1.5,
    'm': 1.75,
    'l': 2.25,
    'ss': 1.5,
    'ms': 1.75,
    'ls': 2.25,
    'sd': 1.5,
    'md': 1.75,
    'ld': 2.25,
    }
headHeightDict = {
    'dls': 0.75,
    'dss': 0.50,
    'dsl': 0.50,
    'dll': 0.75,

    'cls': 0.75,
    'css': 0.50,
    'csl': 0.50,
    'cll': 0.75,

    'hls': 0.75,
    'hss': 0.50,
    'hsl': 0.50,
    'hll': 0.75,

    'mls': 0.75,
    'mss': 0.50,

    'rls': 0.75,
    'rss': 0.50,
    'rsl': 0.50,
    'rll': 0.75,

    'fls': 0.75,
    'fss': 0.50,
    'fsl': 0.50,
    'fll': 0.75,

    'pls': 0.75,
    'pss': 0.50,
    'psl': 0.50,
    'pll': 0.75,

    'bls': 0.75,
    'bss': 0.50,
    'bsl': 0.50,
    'bll': 0.75,
    
    'sls': 0.75,
    'sss': 0.50,
    'ssl': 0.50,
    'sll': 0.75,    

}


# Name Panel - PickAName/TypeAName
RandomButton = "Randomize"
TypeANameButton = "Type Name"
PickANameButton = "Pick-A-Name"
NameShopSubmitButton = "Submit"
RejectNameText = "That name is not allowed. Please try again."
WaitingForNameSubmission = "Submitting your name..."

NameShopNameMaster = "NameMasterEnglish.txt"
NameShopPay = "Subscribe Now!"
NameShopPlay = "Free Trial"
NameShopOnlyPaid = "Only paid users\nmay name their Toons.\nUntil you subscribe\nyour name will be\n"
NameShopContinueSubmission = "Continue Submission"
NameShopChooseAnother = "Choose Another Name"
NameShopToonCouncil = "The Toon Council\nwill review your\nname.  " + \
                      "Review may\ntake a few days.\nWhile you wait\nyour name will be\n "
PleaseTypeName = "Please type your name:"
AllNewNames = "All new names\nmust be approved\nby the Toon Council."
NameShopNameRejected = "The name you\nsubmitted has\nbeen rejected."
NameShopNameAccepted = "Congratulations!\nThe name you\nsubmitted has\nbeen accepted!"
NoPunctuation = "You can't use punctuation marks in your name!"
PeriodOnlyAfterLetter = "You can use a period in your name, but only after a letter."
ApostropheOnlyAfterLetter = "You can use an apostrophe in your name, but only after a letter."
NoNumbersInTheMiddle = "Numeric digits may not appear in the middle of a word."
ThreeWordsOrLess = "Your name must be three words or fewer."
CopyrightedNames = (
    "mickey",
    "mickey mouse",
    "mickeymouse",
    "minnie",
    "minnie mouse",
    "minniemouse",
    "donald",
    "donald duck",
    "donaldduck",
    "pluto",
    "goofy",
    )


# Guild Events
GuildUpdateMembersEvent = "guildUpdateMembersEvent"
GuildInvitationEvent = "guildInvitationEvent"
GuildAcceptInviteEvent = "guildAcceptInviteEvent"
GuildRejectInviteEvent = "guildRejectInviteEvent"

#New friends GUI events for Avatar Friends and Player Friends
#from PiratesFriendsList
AvatarFriendAddEvent = "avatarFriendAddEvent"
AvatarNewFriendAddEvent = "avatarNewFriendAddEvent"
AvatarFriendUpdateEvent = "avatarFriendUpdateEvent"
AvatarFriendRemoveEvent = "avatarFriendRemoveEvent"
PlayerFriendAddEvent = "playerFriendAddEvent"
PlayerFriendUpdateEvent = "playerFriendUpdateEvent"
PlayerFriendRemoveEvent = "playerFriendRemoveEvent"
#from AvatarFriendsManager
AvatarFriendConsideringEvent = "avatarFriendConsideringEvent"
AvatarFriendInvitationEvent = "avatarFriendInvitationEvent"
AvatarFriendRejectInviteEvent = "avatarFriendRejectInviteEvent"
AvatarFriendRetractInviteEvent = "avatarFriendRetractInviteEvent"
AvatarFriendRejectRemoveEvent = "avatarFriendRejectRemoveEvent"
#from PlayerFriendsManager
PlayerFriendInvitationEvent = "playerFriendInvitationEvent"
PlayerFriendRejectInviteEvent = "playerFriendRejectInviteEvent"
PlayerFriendRetractInviteEvent = "playerFriendRetractInviteEvent"
PlayerFriendRejectRemoveEvent = "playerFriendRejectRemoveEvent"
PlayerFriendNewSecretEvent = "playerFriendNewSecretEvent"
PlayerFriendRejectNewSecretEvent = "playerFriendRejectNewSecretEvent"
PlayerFriendRejectUseSecretEvent = "playerFriendRejectUseSecretEvent"
WhisperIncomingEvent = "whisperIncomingEvent"

#Chat Feedback
ChatFeedback_PassedBlacklist = 0x20
ChatFeedback_Whitelist = 0x40
ChatFeedback_OpenChat = 0x80

AccessUnknown = 0
AccessVelvetRope = 1
AccessFull = 2
AccessInvalid = 3 #use this for the default value of setAccess to detect when it's not being set

AvatarPendingCreate = -1
AvatarSlotUnavailable = -2
AvatarSlotAvailable = -3

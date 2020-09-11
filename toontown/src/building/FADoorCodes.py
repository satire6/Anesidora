# The following are codes that indicate different reasons that
# a door might be locked.

from toontown.toonbase import TTLocalizer

# Unlocked
UNLOCKED = 0

# You must talk to "Tutorial Tom" before entering the tutorial street
TALK_TO_TOM = 1

# You must defeat the Flunky before you can enter toon hq.
DEFEAT_FLUNKY_HQ = 2

# You must talk to "HQ Harry" to get your reward
TALK_TO_HQ = 3

# You must talk to "HQ Harry" to get your reward
WRONG_DOOR_HQ = 4

# You must go to the playground
GO_TO_PLAYGROUND = 5

# You must defeat the Flunky before you can enter toon hq.
DEFEAT_FLUNKY_TOM = 6

# You must talk to "HQ Harry" to get your reward
TALK_TO_HQ_TOM = 7

# A suit is heading towards the building.
SUIT_APPROACHING = 8

# A suit is taking over the building.  Stay away.
BUILDING_TAKEOVER = 9

# The toon does not have a complete cog diguise to enter the lobby
SB_DISGUISE_INCOMPLETE = 10
CB_DISGUISE_INCOMPLETE = 11
LB_DISGUISE_INCOMPLETE = 12
BB_DISGUISE_INCOMPLETE = 13

# Strings associated with codes
reasonDict = {
    UNLOCKED: TTLocalizer.FADoorCodes_UNLOCKED,
    TALK_TO_TOM: TTLocalizer.FADoorCodes_TALK_TO_TOM,
    DEFEAT_FLUNKY_HQ: TTLocalizer.FADoorCodes_DEFEAT_FLUNKY_HQ,
    TALK_TO_HQ: TTLocalizer.FADoorCodes_TALK_TO_HQ,
    WRONG_DOOR_HQ: TTLocalizer.FADoorCodes_WRONG_DOOR_HQ,
    GO_TO_PLAYGROUND: TTLocalizer.FADoorCodes_GO_TO_PLAYGROUND,
    DEFEAT_FLUNKY_TOM: TTLocalizer.FADoorCodes_DEFEAT_FLUNKY_TOM,
    TALK_TO_HQ_TOM: TTLocalizer.FADoorCodes_TALK_TO_HQ_TOM,
    SUIT_APPROACHING: TTLocalizer.FADoorCodes_SUIT_APPROACHING,
    BUILDING_TAKEOVER: TTLocalizer.FADoorCodes_BUILDING_TAKEOVER,
    SB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_SB_DISGUISE_INCOMPLETE,
    CB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_CB_DISGUISE_INCOMPLETE,
    LB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_LB_DISGUISE_INCOMPLETE,
    BB_DISGUISE_INCOMPLETE: TTLocalizer.FADoorCodes_BB_DISGUISE_INCOMPLETE,
    }

    

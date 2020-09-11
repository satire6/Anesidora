# These are the types of door models that a DistributedDoor can be.

# An exterior standard door. This is most of the types of doors on landmark
# building exteriors.
EXT_STANDARD = 1

# An interior standard door. This is most of the doors on building interiors.
INT_STANDARD = 2

# A door on the outside of an HQ building. These doors have models built
# into the building, and there is possibly more than one of them on
# each building.
EXT_HQ = 3

# A door on the inside of an HQ building. These are like interior standard
# doors, but there can be more than one of them leading out of the building.
INT_HQ = 4

# The exterior/interior doors  of an estate building must be handled
# differently since the houses on an estate could possibly change
EXT_HOUSE = 5
INT_HOUSE = 6

# CogHQ main building -> lobby doors
EXT_COGHQ = 7
INT_COGHQ = 8

# KartShop exterior -> interior doors
EXT_KS = 9
INT_KS = 10

# for animated landmark buildings
EXT_ANIM_STANDARD = 11

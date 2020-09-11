import CatalogFurnitureItem
import CatalogChatItem
import CatalogClothingItem
import CatalogEmoteItem
import CatalogWallpaperItem
import CatalogFlooringItem
import CatalogWainscotingItem
import CatalogMouldingItem
import CatalogWindowItem
import CatalogPoleItem
import CatalogPetTrickItem
import CatalogBeanItem
import CatalogGardenItem
import CatalogInvalidItem
import CatalogRentalItem
import CatalogGardenStarterItem
import CatalogNametagItem
import CatalogToonStatueItem
import CatalogAnimatedFurnitureItem

# Catalog item type codes.  These code numbers are written to the
# database to represent each particular type of catalog item; you may
# add to this list, but don't change previous numbers once they have
# been published.
# As you add more item types, please add to TTLocalizer.CatalogItemTypeNames too
INVALID_ITEM     = 0
FURNITURE_ITEM   = 1
CHAT_ITEM        = 2
CLOTHING_ITEM    = 3
EMOTE_ITEM       = 4
WALLPAPER_ITEM   = 5
WINDOW_ITEM      = 6
FLOORING_ITEM    = 7
MOULDING_ITEM    = 8
WAINSCOTING_ITEM = 9
POLE_ITEM        = 10
PET_TRICK_ITEM   = 11
BEAN_ITEM   = 12
GARDEN_ITEM   = 13
RENTAL_ITEM   = 14
GARDENSTARTER_ITEM   = 15
NAMETAG_ITEM   = 16
TOON_STATUE_ITEM   = 17
ANIMATED_FURNITURE_ITEM = 18

NonPermanentItemTypes = (RENTAL_ITEM, )

CatalogItemTypes = {
    CatalogInvalidItem.CatalogInvalidItem : INVALID_ITEM,
    CatalogFurnitureItem.CatalogFurnitureItem : FURNITURE_ITEM,
    CatalogChatItem.CatalogChatItem : CHAT_ITEM,
    CatalogClothingItem.CatalogClothingItem : CLOTHING_ITEM,
    CatalogEmoteItem.CatalogEmoteItem : EMOTE_ITEM,
    CatalogWallpaperItem.CatalogWallpaperItem : WALLPAPER_ITEM,
    CatalogWindowItem.CatalogWindowItem : WINDOW_ITEM,
    CatalogFlooringItem.CatalogFlooringItem : FLOORING_ITEM,
    CatalogMouldingItem.CatalogMouldingItem : MOULDING_ITEM,
    CatalogWainscotingItem.CatalogWainscotingItem : WAINSCOTING_ITEM,
    CatalogPoleItem.CatalogPoleItem : POLE_ITEM,
    CatalogPetTrickItem.CatalogPetTrickItem : PET_TRICK_ITEM,
    CatalogBeanItem.CatalogBeanItem : BEAN_ITEM,
    CatalogGardenItem.CatalogGardenItem : GARDEN_ITEM,
    CatalogRentalItem.CatalogRentalItem : RENTAL_ITEM,
    CatalogGardenStarterItem.CatalogGardenStarterItem : GARDENSTARTER_ITEM,
    CatalogNametagItem.CatalogNametagItem : NAMETAG_ITEM,
    CatalogToonStatueItem.CatalogToonStatueItem : TOON_STATUE_ITEM,
    CatalogAnimatedFurnitureItem.CatalogAnimatedFurnitureItem : ANIMATED_FURNITURE_ITEM,
    }

# for each catalog item type, indicates whether or not toons are allowed to have more than one
# of any particular item of that type
CatalogItemType2multipleAllowed = {
    INVALID_ITEM : False,
    FURNITURE_ITEM : True,
    CHAT_ITEM : False,
    CLOTHING_ITEM : False,
    EMOTE_ITEM : False,
    WALLPAPER_ITEM : True,
    WINDOW_ITEM : True,
    FLOORING_ITEM : True,
    MOULDING_ITEM : True,
    WAINSCOTING_ITEM : True,
    POLE_ITEM : False,
    PET_TRICK_ITEM : False,
    BEAN_ITEM : True,
    GARDEN_ITEM : False,
    RENTAL_ITEM : False,
    GARDENSTARTER_ITEM : False,
    NAMETAG_ITEM : False,
    TOON_STATUE_ITEM : False,
    ANIMATED_FURNITURE_ITEM : True,
    }

assert len(CatalogItemType2multipleAllowed) == len(CatalogItemTypes)

# We only use the bottom n bits of the type byte to encode the type
# number.  For now, we reserve 5 bits, which gives us type codes up to
# 31.  We can change this if we need more type codes or more
# high-order bits later.
CatalogItemTypeMask = 0x1f
assert(CatalogItemTypeMask > max(CatalogItemTypes.values()))

# The remaining high-order bits are reserved for esoteric flags on the
# catalog items.
CatalogItemSaleFlag = 0x80
CatalogItemGiftTag = 0x40



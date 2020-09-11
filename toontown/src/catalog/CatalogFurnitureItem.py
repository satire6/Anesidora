import CatalogAtticItem
import CatalogItem
import random
from toontown.toonbase import TTLocalizer

FTModelName = 0
FTColor = 1
FTColorOptions = 2
FTBasePrice = 3
FTFlags = 4
FTScale = 5

FLBank     = 0x0001
FLCloset   = 0x0002
FLRug      = 0x0004
FLPainting = 0x0008
FLOnTable  = 0x0010
FLIsTable  = 0x0020
FLPhone    = 0x0040
FLBillboard = 0x0080

# this is essentially the same as HouseGlobals.houseColors2 with the addition of alpha = 1
furnitureColors = [
    (0.792, 0.353, 0.290, 1.0), # red
    (0.176, 0.592, 0.439, 1.0), # green
    (0.439, 0.424, 0.682, 1.0), # purple
    (0.325, 0.580, 0.835, 1.0), # blue
    (0.753, 0.345, 0.557, 1.0), # pink
    (0.992, 0.843, 0.392, 1.0), # yellow
    ]

woodColors = [
    (0.9330, 0.7730, 0.5690, 1.0), # burly wood
    (0.9333, 0.6785, 0.0550, 1.0), # dark goldenrod
    (0.5450, 0.4510, 0.3330, 1.0), # peach puff
    (0.5410, 0.0000, 0.0000, 1.0), # deep red
    (0.5451, 0.2706, 0.0745, 1.0), # chocolate
    (0.5451, 0.4118, 0.4118, 1.0), # rosey brown
    ]


# This table maps the various bank ID's to the amount of jellybeans
# they hold.
BankToMoney = {
    1300 : 1000,
    1310 : 2500,
    1320 : 5000,
    1330 : 7500,
    1340 : 10000,
    }
MoneyToBank = {}
for bankId, maxMoney in BankToMoney.items():
    MoneyToBank[maxMoney] = bankId
MaxBankId = 1340

# This table maps the various closet ID's to the amount of clothes
# they hold.
ClosetToClothes = {
    500 : 10,
    502 : 15,
    504 : 20,
    506 : 25,
    510 : 10,
    512 : 15,
    514 : 20,
    516 : 25,
    }
ClothesToCloset = {}
for closetId, maxClothes in ClosetToClothes.items():
    # There is not a 1-to-1 mapping like the banks since there are boys
    # and girls closets, so we'll store a bank Id tuple.
    if not ClothesToCloset.has_key(maxClothes):
        ClothesToCloset[maxClothes] = (closetId,)
    else:
        ClothesToCloset[maxClothes] += (closetId,)
MaxClosetIds = (506, 516)


# These index numbers are written to the database.  Don't mess with them.
# Also see TTLocalizer.FurnitureNames and TTLocalizer.AwardManagerFurnitureNames
FurnitureTypes = {

    # These are examples to illustrate how we might apply color
    # options to furniture, and/or hide and show pieces or replace
    # textures to extend a single model for multiple purposes.
    
##     # Wooden chair
##     100 : ("phase_5.5/models/estate/cushionChair",
##            (("**/cushion*", None)),
##            None,
##            50),
    
##     # Cushioned chair
##     110 : ("phase_5.5/models/estate/cushionChair",
##            None,
##            None,
##            100),
    
##     # Velvet chair
##     120 : ("phase_5.5/models/estate/cushionChair",
##            (("**/cushion*", "phase_5.5/maps/velvet_cushion.jpg")),
##            { 0 : (("**/cushion*", (1, 0, 0, 1)),),
##              1 : (("**/cushion*", (0.6, 0.2, 1, 1)),),
##              2 : (("**/cushion*", (0.2, 0.2, 0.6, 1)),),
##              },
##            250),
    
##     # Library chair
##     130 : ("phase_5.5/models/estate/libraryChair",
##            None,
##            None,
##            500),

    ## CHAIRS ##
    # Chair A - Series 1
    100 : ("phase_5.5/models/estate/chairA",
           None, None, 80),

    # Chair A desaturated - Series 7
    105 : ("phase_5.5/models/estate/chairAdesat",
           None,
           { 0 : (("**/cushion*", furnitureColors[0]), ("**/arm*", furnitureColors[0]),),
             1 : (("**/cushion*", furnitureColors[1]), ("**/arm*", furnitureColors[1]),),
             2 : (("**/cushion*", furnitureColors[2]), ("**/arm*", furnitureColors[2]),),
             3 : (("**/cushion*", furnitureColors[3]), ("**/arm*", furnitureColors[3]),),
             4 : (("**/cushion*", furnitureColors[4]), ("**/arm*", furnitureColors[4]),),
             5 : (("**/cushion*", furnitureColors[5]), ("**/arm*", furnitureColors[5]),),
             },
           160),

    # Chair - Series 1
    110 : ("phase_3.5/models/modules/chair",
           None, None, 40),

    # Desk chair - Series 2
    120 : ("phase_5.5/models/estate/deskChair",
           None, None, 60),

    # Bug room chair - Series 2
    130 : ("phase_5.5/models/estate/BugRoomChair",
           None, None, 160),

    # Underwater lobster chair - Series 3
    140 : ("phase_5.5/models/estate/UWlobsterChair",
           None, None, 200),

    # Underwater lifesaver chair - Series 3
    145 : ("phase_5.5/models/estate/UWlifeSaverChair",
           None, None, 200),

    # Western saddle stool  - Series 4
    150 : ("phase_5.5/models/estate/West_saddleStool2",
           None, None, 160),

    # Western native chair  - Series 4
    160 : ("phase_5.5/models/estate/West_nativeChair",
           None, None, 160),

    # Candy cupcake Chair - Series 6
    170 : ("phase_5.5/models/estate/cupcakeChair",
           None, None, 240),
    
     
    ## BEDS ##
    # Boy's bed - Initial Furniture
    200 : ("phase_5.5/models/estate/regular_bed",
           None, None, 400),

    # Boy's bed destaturated - Series 7
    205 : ("phase_5.5/models/estate/regular_bed_desat",
           None,
           { 0 : (("**/bar*", woodColors[0]),("**/post*", woodColors[0]),("**/*support", woodColors[0]),
                  ("**/top", woodColors[0]),("**/bottom", woodColors[0]),("**/pPlane*", woodColors[0]),),
             1 : (("**/bar*", woodColors[1]),("**/post*", woodColors[1]),("**/*support", woodColors[1]),
                  ("**/top", woodColors[1]),("**/bottom", woodColors[1]),("**/pPlane*", woodColors[1]),),
             2 : (("**/bar*", woodColors[2]),("**/post*", woodColors[2]),("**/*support", woodColors[2]),
                  ("**/top", woodColors[2]),("**/bottom", woodColors[2]),("**/pPlane*", woodColors[2]),),
             3 : (("**/bar*", woodColors[3]),("**/post*", woodColors[3]),("**/*support", woodColors[3]),
                  ("**/top", woodColors[3]),("**/bottom", woodColors[3]),("**/pPlane*", woodColors[3]),),
             4 : (("**/bar*", woodColors[4]),("**/post*", woodColors[4]),("**/*support", woodColors[4]),
                  ("**/top", woodColors[4]),("**/bottom", woodColors[4]),("**/pPlane*", woodColors[4]),),
             5 : (("**/bar*", woodColors[5]),("**/post*", woodColors[5]),("**/*support", woodColors[5]),
                  ("**/top", woodColors[5]),("**/bottom", woodColors[5]),("**/pPlane*", woodColors[5]),),
             },
           800),

    # Girl's bed - Series 1
    210 : ("phase_5.5/models/estate/girly_bed",
           None, None, 450),

    # Bathtub bed - Series 1
    220 : ("phase_5.5/models/estate/bathtub_bed",
           None, None, 550),

    # Bug Room Bed - Series 2
    230 : ("phase_5.5/models/estate/bugRoomBed",
           None, None, 600),
    
    # Underwater Boat bed - Series 3
    240 : ("phase_5.5/models/estate/UWBoatBed",
           None, None, 600),

    # Western Cactus Hammoc bed - Series 4
    250 : ("phase_5.5/models/estate/West_cactusHammoc",
           None, None, 550),

    # Candy ice cream bed - Series 6
    260 : ("phase_5.5/models/estate/icecreamBed",
           None, None, 700),
           
    # Trolley bed - CatalogAnimatedFurnitureItem
    270 : ("phase_5.5/models/estate/trolley_bed",
           None, None, 1200, None, None, 0.25),

    ## MUSICAL INSTRUMENTS
    # Piano - Series 2
    300 : ("phase_5.5/models/estate/Piano",
           None, None, 1000, FLIsTable),

    # Organ - Series 2
    310 : ("phase_5.5/models/estate/Organ",
           None, None, 2500),


    ## FIREPLACES ##
    # Square Fireplace - Initial Furniture
    400 : ("phase_5.5/models/estate/FireplaceSq",
           None, None, 800),

    # Girly Fireplace - Series 1
    410 : ("phase_5.5/models/estate/FireplaceGirlee",
           None, None, 800),

    # Round Fireplace - Series 2
    420 : ("phase_5.5/models/estate/FireplaceRound",
           None, None, 800),

    # Bug Room Fireplace - Series 2
    430 : ("phase_5.5/models/estate/bugRoomFireplace",
           None, None, 800),

    # Candy Carmel Apple Fireplace - Series 6
    440 : ("phase_5.5/models/estate/CarmelAppleFireplace",
           None, None, 800),
    
    # Coral Fireplace
    450 : ("phase_5.5/models/estate/fireplace_coral",
           None, None, 950),
           
    # Coral Fireplace with fire
    460 : ("phase_5.5/models/estate/tt_m_prp_int_fireplace_coral",
           None, None, 1250, None, None, 0.5),
           
    # Square Fireplace with fire
    470 : ("phase_5.5/models/estate/tt_m_prp_int_fireplace_square",
           None, None, 1100, None, None, 0.5),
           
    # Round Fireplace with fire
    480 : ("phase_5.5/models/estate/tt_m_prp_int_fireplace_round",
           None, None, 1100, None, None, 0.5),
           
    # Girly Fireplace with fire
    490 : ("phase_5.5/models/estate/tt_m_prp_int_fireplace_girlee",
           None, None, 1100, None, None, 0.5),
           
    # Bug Room Fireplace with fire
    491 : ("phase_5.5/models/estate/tt_m_prp_int_fireplace_bugRoom",
           None, None, 1100, None, None, 0.5),
           
    # Candy Caramel Apple Fireplace with fire
    492 : ("phase_5.5/models/estate/tt_m_prp_int_fireplace_caramelApple",
           None, None, 1100, None, None, 0.5),

    ## WARDROBES ##
    # Boy's Wardrobe, 10 items - Initial Furniture
    500 : ("phase_5.5/models/estate/closetBoy",
           None, None, 500, FLCloset, 0.85),

    # Boy's Wardrobe, 15 items - Series 1
    502 : ("phase_5.5/models/estate/closetBoy",
           None, None, 500, FLCloset, 1.0),

    # Boy's Wardrobe, 20 items
    504 : ("phase_5.5/models/estate/closetBoy",
           None, None, 500, FLCloset, 1.15),

    # Boy's Wardrobe, 25 items
    506 : ("phase_5.5/models/estate/closetBoy",
           None, None, 500, FLCloset, 1.3),


    # Girl's Wardrobe, 10 items - Initial Furniture
    510 : ("phase_5.5/models/estate/closetGirl",
           None, None, 500, FLCloset, 0.85),

    # Girl's Wardrobe, 15 items - Series 1
    512 : ("phase_5.5/models/estate/closetGirl",
           None, None, 500, FLCloset, 1.0),

    # Girl's Wardrobe, 20 items
    514 : ("phase_5.5/models/estate/closetGirl",
           None, None, 500, FLCloset, 1.15),

    # Girl's Wardrobe, 25 items
    516 : ("phase_5.5/models/estate/closetGirl",
           None, None, 500, FLCloset, 1.3),

    ## LAMPS ##
    # Short lamp - Series 1
    600 : ("phase_3.5/models/modules/lamp_short",
           None, None, 45, FLOnTable),

    # Tall lamp - Series 2
    610 : ("phase_3.5/models/modules/lamp_tall",
           None, None, 45),

    # Lamp A - Series 1
    620 : ("phase_5.5/models/estate/lampA",
           None, None, 35, FLOnTable),

    # Lamp A Desaturated - Series 7
    625 : ("phase_5.5/models/estate/lampADesat",
           None,
           { 0 : (("**/top", furnitureColors[0]),),
             1 : (("**/top", furnitureColors[1]),),
             2 : (("**/top", furnitureColors[2]),),
             3 : (("**/top", furnitureColors[3]),),
             4 : (("**/top", furnitureColors[4]),),
             5 : (("**/top", furnitureColors[5]),),
             },
           70, FLOnTable),

    # Bug Room Daisy Lamp 1 - Series 2
    630 : ("phase_5.5/models/estate/bugRoomDaisyLamp1",
           None, None, 55),

    # Bug Room Daisy Lamp 2 - Series 2
    640 : ("phase_5.5/models/estate/bugRoomDaisyLamp2",
           None, None, 55),

    # Underwater Lamp 1 - Series 3
    650 : ("phase_5.5/models/estate/UWlamp_jellyfish",
           None, None, 55, FLOnTable),
           
    # Underwater Lamp 2 - Series 3
    660 : ("phase_5.5/models/estate/UWlamps_jellyfishB",
           None, None, 55, FLOnTable),

    # Cowboy Lamp - series 4
    670 : ("phase_5.5/models/estate/West_cowboyLamp",
           None, None, 55, FLOnTable),
           
    # Lamps
    680: ("phase_5.5/models/estate/tt_m_ara_int_candlestick",
        None,
        { 0 : (("**/candlestick/candlestick", (1.0, 1.0, 1.0, 1.0),),),
           1 : (("**/candlestick/candlestick", furnitureColors[1]),),
           2 : (("**/candlestick/candlestick", furnitureColors[2]),),
           3 : (("**/candlestick/candlestick", furnitureColors[3]),),
           4 : (("**/candlestick/candlestick", furnitureColors[4]),),
           5 : (("**/candlestick/candlestick", furnitureColors[5]),),
           6 : (("**/candlestick/candlestick", furnitureColors[0]),),
        },
        20, FLOnTable),           
    
    681: ("phase_5.5/models/estate/tt_m_ara_int_candlestickLit",
        None,
        { 0 : (("**/candlestick/candlestick", (1.0, 1.0, 1.0, 1.0),),),
           1 : (("**/candlestickLit/candlestick", furnitureColors[1]),),
           2 : (("**/candlestickLit/candlestick", furnitureColors[2]),),
           3 : (("**/candlestickLit/candlestick", furnitureColors[3]),),
           4 : (("**/candlestickLit/candlestick", furnitureColors[4]),),
           5 : (("**/candlestickLit/candlestick", furnitureColors[5]),),
           6 : (("**/candlestickLit/candlestick", furnitureColors[0]),),
        },
        25, FLOnTable),       

    ## COUCHES ##
    # 1-person couch - Series 1
    700 : ("phase_3.5/models/modules/couch_1person",
           None, None, 230),

    # 1-person couch desaturated - Series 7
    705 : ("phase_5.5/models/estate/couch_1personDesat",
           None,
           { 0 : (("**/*couch", furnitureColors[0]),),
             1 : (("**/*couch", furnitureColors[1]),),
             2 : (("**/*couch", furnitureColors[2]),),
             3 : (("**/*couch", furnitureColors[3]),),
             4 : (("**/*couch", furnitureColors[4]),),
             5 : (("**/*couch", furnitureColors[5]),),
             },
           460),

    # 2-person couch - Series 1
    710 : ("phase_3.5/models/modules/couch_2person",
           None, None, 230),

    # 2-person couch desaturated - Series 7
    715 : ("phase_5.5/models/estate/couch_2personDesat",
           None,
           { 0 : (("**/*couch", furnitureColors[0]),),
             1 : (("**/*couch", furnitureColors[1]),),
             2 : (("**/*couch", furnitureColors[2]),),
             3 : (("**/*couch", furnitureColors[3]),),
             4 : (("**/*couch", furnitureColors[4]),),
             5 : (("**/*couch", furnitureColors[5]),),
             },
           460),

    # Western Hay couch - Series 4
    720 : ("phase_5.5/models/estate/West_HayCouch",
           None, None, 420),

    # Candy Twinkie couch - Series 6
    730 : ("phase_5.5/models/estate/twinkieCouch",
           None, None, 480),


    ## DESKS ##
    # Desk - Series 1
    800 : ("phase_3.5/models/modules/desk_only_wo_phone",
           None, None, 65, FLIsTable),

    # Bug Room Desk - Series 2
    810 : ("phase_5.5/models/estate/BugRoomDesk",
           None, None, 125, FLIsTable),


    ## MISC PROPS ##
    # Umbrella stand - Series 1
    900 : ("phase_3.5/models/modules/umbrella_stand",
           None, None, 30),

    # Coat rack - Series 1
    910 : ("phase_3.5/models/modules/coatrack",
           None, None, 75),

    # Trashcan - Series 2
    920 : ("phase_3.5/models/modules/paper_trashcan",
           None, None, 30),

    # Bug Room Red Pot - Series 2
    930 : ("phase_5.5/models/estate/BugRoomRedMushroomPot",
           None, None, 60),

    # Bug Room Yellow Pot - Series 2
    940 : ("phase_5.5/models/estate/BugRoomYellowMushroomPot",
           None, None, 60),

    # Underwater coat rack - Series 3
    950 : ("phase_5.5/models/estate/UWcoralClothRack",
           None, None, 75),

    # Western barrel stand - Series 4
    960 : ("phase_5.5/models/estate/west_barrelStand",
           None, None, 75),

    # Western fat cactus plant - Series 4
    970 : ("phase_5.5/models/estate/West_fatCactus",
           None, None, 75),

    # Western tepee - Series 4
    980 : ("phase_5.5/models/estate/West_Tepee",
           None, None, 150),
    
    # Gag fan - CatalogAnimatedFurnitureItem
    990 : ("phase_5.5/models/estate/gag_fan",
           None, None, 500, None, None, 0.5),

    ## RUGS ##
    # Square Rug - Series 1
    1000 : ("phase_3.5/models/modules/rug",
            None, None, 75, FLRug),

    # Round Rug A - Series 1
    1010 : ("phase_5.5/models/estate/rugA",
            None, None, 75, FLRug),

    # Round Rug A desaturated - Series 7
    1015 : ("phase_5.5/models/estate/rugADesat",
            None,
            { 0 : (("**/pPlane*", furnitureColors[0]),),
              1 : (("**/pPlane*", furnitureColors[1]),),
              2 : (("**/pPlane*", furnitureColors[2]),),
              3 : (("**/pPlane*", furnitureColors[3]),),
              4 : (("**/pPlane*", furnitureColors[4]),),
              5 : (("**/pPlane*", furnitureColors[5]),),
              },
            150, FLRug),

    # Round Rug B - Series 1
    1020 : ("phase_5.5/models/estate/rugB",
            None, None, 75, FLRug, 2.5),

    # Bug Room Leaf Mat - Series 2
    1030 : ("phase_5.5/models/estate/bugRoomLeafMat",
            None, None, 75, FLRug),
            
    # Presents
    1040 : ("phase_5.5/models/estate/tt_m_ara_int_presents",
              None, None, 300),
              
    # Sled
    1050 : ("phase_5.5/models/estate/tt_m_ara_int_sled",
              None, None, 400),

    ## CABINETS ##
    # Red Wood Cabinet  - Series 1
    1100 : ("phase_5.5/models/estate/cabinetRwood",
            None, None, 825),
    
    # Yellow Wood Cabinet - Series 2
    1110 : ("phase_5.5/models/estate/cabinetYwood",
            None, None, 825),

    # Bookcase - Series 2
    1120 : ("phase_3.5/models/modules/bookcase",
            None, None, 650, FLIsTable),

    # Bookcase - Series 2
    1130 : ("phase_3.5/models/modules/bookcase_low",
            None, None, 650, FLIsTable),

    # Candy ice cream chest - Series 6
    1140 : ("phase_5.5/models/estate/icecreamChest",
            None, None, 750),


    ## TABLES ##
    # End table - Series 1
    1200 : ("phase_3.5/models/modules/ending_table",
            None, None, 60, FLIsTable),

    # Radio table - Series 1
    1210 : ("phase_5.5/models/estate/table_radio",
            None, None, 60, FLIsTable, 50.0),

    # Radio table desaturated - Series 7
    1215 : ("phase_5.5/models/estate/table_radioDesat",
            None,
            { 0 : (("**/RADIOTABLE_*", woodColors[0]),),
              1 : (("**/RADIOTABLE_*", woodColors[1]),),
              2 : (("**/RADIOTABLE_*", woodColors[2]),),
              3 : (("**/RADIOTABLE_*", woodColors[3]),),
              4 : (("**/RADIOTABLE_*", woodColors[4]),),
              5 : (("**/RADIOTABLE_*", woodColors[5]),),
              },
            120, FLIsTable, 50.0),

    # Coffee table - Series 2
    1220 : ("phase_5.5/models/estate/coffeetableSq",
            None, None, 180, FLIsTable),
            
    # Coffee table - Series 2
    1230 : ("phase_5.5/models/estate/coffeetableSq_BW",
            None, None, 180, FLIsTable),

    # Underwater coffee table - Series 3
    1240 : ("phase_5.5/models/estate/UWtable",
            None, None, 180, FLIsTable),

    # Candy cookie table - Series 6
    1250 : ("phase_5.5/models/estate/cookieTableA",
            None, None, 220, FLIsTable),

    # Desaturated bedside table - Series 7
    1260 : ("phase_5.5/models/estate/TABLE_Bedroom_Desat",
            None,
            { 0 : (("**/Bedroom_Table", woodColors[0]),),
              1 : (("**/Bedroom_Table", woodColors[1]),),
              2 : (("**/Bedroom_Table", woodColors[2]),),
              3 : (("**/Bedroom_Table", woodColors[3]),),
              4 : (("**/Bedroom_Table", woodColors[4]),),
              5 : (("**/Bedroom_Table", woodColors[5]),),
              },
            220, FLIsTable),


    ## IN GAME INTERFACE DEVICES ##
    # Jellybean Bank, 1000 beans - Initial Furniture
    1300 : ("phase_5.5/models/estate/jellybeanBank",
            None, None, 0, FLBank, 0.75),
    
    # Jellybean Bank, 2500 beans - Series 1
    1310 : ("phase_5.5/models/estate/jellybeanBank",
            None, None, 400, FLBank, 1.0),
    
    # Jellybean Bank, 5000 beans - Series 1
    1320 : ("phase_5.5/models/estate/jellybeanBank",
            None, None, 800, FLBank, 1.125),

    # Jellybean Bank, 7500 beans - Series 1
    1330 : ("phase_5.5/models/estate/jellybeanBank",
            None, None, 1600, FLBank, 1.25),

    # Jellybean Bank, 10000 beans - Series 1
    1340 : ("phase_5.5/models/estate/jellybeanBank",
            None, None, 3200, FLBank, 1.5),

    # Phone - Initial Furniture
    1399 : ("phase_5.5/models/estate/prop_phone-mod",
            None, None, 0, FLPhone),


    ## PAINTINGS ##
    # Painting: Cezanne Toon - Series 1
    1400 : ("phase_5.5/models/estate/cezanne_toon",
            None, None, 425, FLPainting, 2.0),

    # Painting: Flowers - Series 1
    1410 : ("phase_5.5/models/estate/flowers",
            None, None, 425, FLPainting, 2.0),

    # Painting: Modern Mickey - Series 1
    1420 : ("phase_5.5/models/estate/modernistMickey",
            None, None, 425, FLPainting, 2.0),

    # Painting: Rembrandt Toon - Series 1
    1430 : ("phase_5.5/models/estate/rembrandt_toon",
            None, None, 425, FLPainting, 2.0),

    # Painting: Toon Landscape - Series 2
    1440 : ("phase_5.5/models/estate/landscape",
            None, None, 425, FLPainting, 100.0),

    # Painting: Whistler's Horse - Series 2
    1441 : ("phase_5.5/models/estate/whistler-horse",
            None, None, 425, FLPainting, 2.0),

    # Painting: Degas Toon Star - Series 2
    1442 : ("phase_5.5/models/estate/degasHorseStar",
            None, None, 425, FLPainting, 2.5),

    # Painting: Toon Pie - Series 2
    1443 : ("phase_5.5/models/estate/MagPie",
            None, None, 425, FLPainting, 2.0),
            
    # Painting: Valentines Day - Mickey and Minney 
    1450 : ("phase_5.5/models/estate/tt_m_prp_int_painting_valentine",
             None, None, 425, FLPainting),


    ## APPLIANCES ##
    # Radio A - Series 2
    1500 : ("phase_5.5/models/estate/RADIO_A",
            None, None, 25, FLOnTable, 15.0),

    # Radio B - Series 1
    1510 : ("phase_5.5/models/estate/RADIO_B",
            None, None, 25, FLOnTable, 15.0),

    # Radio C - Series 2
    1520 : ("phase_5.5/models/estate/radio_c",
            None, None, 25, FLOnTable, 15.0),

    # Bug Room TV - Series 2
    1530 : ("phase_5.5/models/estate/bugRoomTV",
            None, None, 675),


    ## VASES ##
    # Vase A short - Series 1
    1600 : ("phase_5.5/models/estate/vaseA_short",
            None, None, 120, FLOnTable),

    # Vase A tall - Series 1
    1610 : ("phase_5.5/models/estate/vaseA_tall",
            None, None, 120, FLOnTable),

    # Vase B short - Series 2
    1620 : ("phase_5.5/models/estate/vaseB_short",
            None, None, 120, FLOnTable),

    # Vase B tall - Series 2
    1630 : ("phase_5.5/models/estate/vaseB_tall",
            None, None, 120, FLOnTable),

    # Vase C short - Series 2
    1640 : ("phase_5.5/models/estate/vaseC_short",
            None, None, 120, FLOnTable),

    # Vase D short - Series 2
    1650 : ("phase_5.5/models/estate/vaseD_short",
            None, None, 120, FLOnTable),

    # Underwater coral vase - Series 3
    1660 : ("phase_5.5/models/estate/UWcoralVase",
            None, None, 120, (FLOnTable | FLBillboard)),

    # Underwater shell vase - Series 3
    1661 : ("phase_5.5/models/estate/UWshellVase",
            None, None, 120, (FLOnTable | FLBillboard) ),
            
    # Valentines Day Vase - Rose Vase
    1670 : ("phase_5.5/models/estate/tt_m_prp_int_roseVase_valentine",
            None, None, 200, (FLOnTable)),
            
    # Valentines Day Vase - Rose Water Can
    1680 : ("phase_5.5/models/estate/tt_m_prp_int_roseWatercan_valentine",
            None, None, 200, (FLOnTable)),
            
    
    ## KITSCH ##
    # Popcorn cart - Series 2
    1700 : ("phase_5.5/models/estate/popcornCart",
            None, None, 400),

    # Bug Room Ladybug - Series 2
    1710 : ("phase_5.5/models/estate/bugRoomLadyBug",
            None, None, 260),

    # Underwater skateboarder statue - Series 3
    1720 : ("phase_5.5/models/estate/UWfountain",
            None, None, 450),

    # Underwater clothes dryer - Series 3
    1725 : ("phase_5.5/models/estate/UWOceanDryer",
            None, None, 400),
            

    ## Fishbowls ##
    # Underwater skull fish bowl - Series 3
    1800 : ("phase_5.5/models/estate/UWskullBowl",
            None, None, 120, FLOnTable),

    # Underwater lizard fish bowl - Series 3
    1810 : ("phase_5.5/models/estate/UWlizardBowl",
            None, None, 120, FLOnTable),


    ## Wall hangings ##
    # Underwater swordFish wall hanging - Series 3
    1900 : ("phase_5.5/models/estate/UWswordFish",
            None, None, 425, FLPainting, .5),

    # Underwater hammerhead wall hanging - Series 3
    1910 : ("phase_5.5/models/estate/UWhammerhead",
            None, None, 425, FLPainting),
            
    # Western hanging horns - Series 4
    1920 : ("phase_5.5/models/estate/West_hangingHorns",
            None, None, 475, FLPainting),

    # Western sombrero - Series 4
    1930 : ("phase_5.5/models/estate/West_Sombrero",
           None, None, 425, FLPainting),

    # Western fancy sombrero - Series 4
    1940 : ("phase_5.5/models/estate/West_fancySombrero",
           None, None, 450, FLPainting),

    # Western coyote paw - Series 4
    1950 : ("phase_5.5/models/estate/West_CoyotePawdecor",
           None, None, 475, FLPainting),

    # Western horse shoe - Series 4
    1960 : ("phase_5.5/models/estate/West_Horseshoe",
           None, None, 475, FLPainting),

    # Western bison portrait - Series 4
    1970 : ("phase_5.5/models/estate/West_bisonPortrait",
           None, None, 475, FLPainting),



    ## Play Area Items ##
    # Candy swingset - Series 6
    2000 : ("phase_5.5/models/estate/candySwingSet",
            None, None, 300),

    # Candy cake slide - Series 6
    2010 : ("phase_5.5/models/estate/cakeSlide",
            None, None, 200),


    ## Bathing Items ##
    # Candy banana split shower - Series 6
    3000 : ("phase_5.5/models/estate/BanannaSplitShower",
            None, None, 400),


    ## SPECIAL HOLIDAY THEMED ITEMS FOLLOW ##
    # short pumpkin - Halloween
    10000 : ("phase_4/models/estate/pumpkin_short",
             None, None, 200, FLOnTable),

    # tall pumpkin - Halloween
    10010 : ("phase_4/models/estate/pumpkin_tall",
             None, None, 250, FLOnTable),

    # winter tree
    10020 : ("phase_5.5/models/estate/tt_m_prp_int_winter_tree",
             None, None, 500, None, None, 0.1),

    # winter wreath
    10030 : ("phase_5.5/models/estate/tt_m_prp_int_winter_wreath",
             None, None, 200, FLPainting),

    }
# If you add any new Animated furniture, update CatalogAnimatedFurniture.AnimatedFurnitureItemKeys


class CatalogFurnitureItem(CatalogAtticItem.CatalogAtticItem):
    """CatalogFurnitureItem

    This represents a piece of furniture that the player may purchase
    and store in his house or possibly in his lawn.  Each item of
    furniture corresponds to a particular model file (possibly with
    some pieces hidden and/or texture swapped); there may also be a
    number of user-customizable options for a given piece of furniture
    (e.g. changing colors).

    """
    
    def makeNewItem(self, furnitureType, colorOption = None, posHpr = None):
        self.furnitureType = furnitureType
        self.colorOption = colorOption
        self.posHpr = posHpr
        
        CatalogAtticItem.CatalogAtticItem.makeNewItem(self)

    def needsCustomize(self):
        # Returns true if the item still needs to be customized by the
        # user (e.g. by choosing a color).
        return self.colorOption == None and \
               FurnitureTypes[self.furnitureType][FTColorOptions] != None

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def replacesExisting(self):
        # Returns true if an item of this type will, when purchased,
        # replace an existing item of the same type, or false if items
        # accumulate.
        return (self.getFlags() & (FLCloset | FLBank)) != 0

    def hasExisting(self):
        # If replacesExisting returns true, this returns true if an
        # item of this class is already owned by the avatar, false
        # otherwise.  If replacesExisting returns false, this is
        # undefined.

        # We always have a closet and bank.
        return 1

    def getYourOldDesc(self):
        # If replacesExisting returns true, this returns the name of
        # the already existing object, in sentence construct: "your
        # old ...".  If replacesExisting returns false, this is undefined.
        
        if (self.getFlags() & FLCloset):
            return TTLocalizer.FurnitureYourOldCloset
        elif (self.getFlags() & FLBank):
            return TTLocalizer.FurnitureYourOldBank
        else:
            return None

    def notOfferedTo(self, avatar):
        if (self.getFlags() & FLCloset):
            # Boys can only buy boy wardrobes, and girls can only buy
            # girl wardrobes.  Sorry.
            decade = self.furnitureType - (self.furnitureType % 10)
            forBoys = (decade == 500)
            if avatar.getStyle().getGender() == 'm':
                return not forBoys
            else:
                return forBoys

        # All other items are completely androgynous.
        return 0

    def isDeletable(self):
        # Returns true if the item can be deleted from the attic,
        # false otherwise.
        return (self.getFlags() & (FLBank | FLCloset | FLPhone)) == 0

    def getMaxBankMoney(self):
        # This special method is only defined for bank type items,
        # and returns the capacity of the bank in jellybeans.
        return BankToMoney.get(self.furnitureType)

    def getMaxClothes(self):
        # This special method is only defined for wardrobe type items,
        # and returns the number of clothing items the wardrobe holds.
        index = self.furnitureType % 10
        if index == 0:
            return 10
        elif index == 2:
            return 15
        elif index == 4:
            return 20
        elif index == 6:
            return 25
        else:
            return None

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        if self.getFlags() & FLBank:
            # No point in buying an equal or smaller bank.
            if self.getMaxBankMoney() <= avatar.getMaxBankMoney():
                return 1

            # Also if this particular bank is on order, we don't need
            # another one.
            if self in avatar.onOrder or self in avatar.mailboxContents:
                return 1

        if self.getFlags() & FLCloset:
            # No point in buying an equal or smaller wardrobe.
            if self.getMaxClothes() <= avatar.getMaxClothes():
                return 1

            # Also if this particular wardrobe is on order, we don't need
            # another one.
            if self in avatar.onOrder or self in avatar.mailboxContents:
                return 1
            
        return 0

    def getTypeName(self):
        flags = self.getFlags()
        if flags & FLPainting:
            return TTLocalizer.PaintingTypeName
        else:
            return TTLocalizer.FurnitureTypeName

    def getName(self):
        return TTLocalizer.FurnitureNames[self.furnitureType]

    def getFlags(self):
        # Returns the special flag word associated with this furniture
        # item.  This controls special properties of the item, and is
        # one or more of the bits defined above with the symbols FL*.
        defn = FurnitureTypes[self.furnitureType]
        if FTFlags < len(defn):
            flag = defn[FTFlags]
            if (flag == None):
                return 0
            else:
                return flag
        else:
            return 0
            
    def isGift(self):
        if self.getFlags() & (FLCloset | FLBank):
            return 0
        else:
            return 1

    def recordPurchase(self, avatar, optional):
        # Updates the appropriate field on the avatar to indicate the
        # purchase (or delivery).  This makes the item available to
        # use by the avatar.  This method is only called on the AI side.
        house, retcode = self.getHouseInfo(avatar)
        self.giftTag = None
        if retcode >= 0:
            house.addAtticItem(self)
            if (self.getFlags() & FLBank):
                # A special case: if we just bought a new bank, change
                # our maximum bank money accordingly.  This property
                # is stored on the toon.
                avatar.b_setMaxBankMoney(self.getMaxBankMoney())
            if (self.getFlags() & FLCloset):
                # Another special case: if we just bought a new
                # wardrobe, change our maximum clothing items
                # accordingly.  This property is also stored on the
                # toon.
                avatar.b_setMaxClothes(self.getMaxClothes())
                
        return retcode

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 24 * 60  # 24 hours.

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        model = self.loadModel()
        spin = 1

        flags = self.getFlags()
        if flags & FLRug:
            spin = 0
            model.setP(90)
        elif flags & FLPainting:
            spin = 0
        elif flags & FLBillboard:
            spin = 0
        model.setBin('unsorted', 0, 1)

##        assert (not self.hasPicture)
        self.hasPicture=True
        
        return self.makeFrameModel(model, spin)

    def output(self, store = ~0):
        return "CatalogFurnitureItem(%s%s)" % (
            self.furnitureType,
            self.formatOptionalData(store))

    def getFilename(self):
        type = FurnitureTypes[self.furnitureType]
        return type[FTModelName]

    def compareTo(self, other):
        return self.furnitureType - other.furnitureType

    def getHashContents(self):
        return self.furnitureType

    def getBasePrice(self):
        return FurnitureTypes[self.furnitureType][FTBasePrice]

    def loadModel(self):
        type = FurnitureTypes[self.furnitureType]
        model = loader.loadModel(type[FTModelName])
        self.applyColor(model, type[FTColor])
        if type[FTColorOptions] != None:
            if self.colorOption == None:
                # The user hasn't picked a color option; choose a
                # random one.
                option = random.choice(type[FTColorOptions].values())
            else:
                # Use the user's specified color option.
                option = type[FTColorOptions].get(self.colorOption)
            
            self.applyColor(model, option)

        if (FTScale < len(type)):
            scale = type[FTScale]
            if not (scale == None):
                # Also apply a scale.
                model.setScale(scale)
                model.flattenLight()
        return model

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(self, di, versionNumber, store)
        self.furnitureType = di.getInt16()
        self.colorOption = None

        # The following will raise an exception if self.furnitureType
        # is not valid.
        type = FurnitureTypes[self.furnitureType]

        if type[FTColorOptions]:
            if store & CatalogItem.Customization:
                self.colorOption = di.getUint8()

                # The following will raise an exception if
                # self.colorOption is not valid.
                option = type[FTColorOptions][self.colorOption]
        
    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addInt16(self.furnitureType)
        if FurnitureTypes[self.furnitureType][FTColorOptions]:
            if store & CatalogItem.Customization:
                dg.addUint8(self.colorOption)
        

def nextAvailableBank(avatar, duplicateItems):
    bankId = MoneyToBank.get(avatar.getMaxBankMoney())
    if bankId == None or bankId == MaxBankId:
        # No more banks for this avatar.
        return None

    bankId += 10
    item = CatalogFurnitureItem(bankId)

    # But if this bank is already on order, don't offer the same bank
    # again.  Skip to the next one instead.
    while item in avatar.onOrder or \
          item in avatar.mailboxContents:
        bankId += 10
        if bankId > MaxBankId:
            return None
        item = CatalogFurnitureItem(bankId)

    return item

def getAllBanks():
    list = []
    for bankId in BankToMoney.keys():
        list.append(CatalogFurnitureItem(bankId))
    return list

def nextAvailableCloset(avatar, duplicateItems):
    # detemine which closet index in the tuple to use
    if avatar.getStyle().getGender() == 'm':
        index = 0
    else:
        index = 1
    # handle a race a condition - dist toon ai cleaned up?
    if not hasattr(avatar, "maxClothes"):
        return None
    closetIds = ClothesToCloset.get(avatar.getMaxClothes())
    # we can't guarantee order on these dict values, so we'll sort them as a list
    closetIds = list(closetIds)
    closetIds.sort()
    closetId = closetIds[index]
    if closetId == None or closetId == MaxClosetIds[index]:
        # No more closets for this avatar.
        return None

    closetId += 2
    item = CatalogFurnitureItem(closetId)

    # But if this closet is already on order, don't offer the same bank
    # again.  Skip to the next one instead.
    while item in avatar.onOrder or \
          item in avatar.mailboxContents:
        closetId += 2
        if closetId > MaxClosetIds[index]:
            return None
        item = CatalogFurnitureItem(closetId)

    return item

def getAllClosets():
    list = []
    for closetId in ClosetsToClothes.keys():
        list.append(CatalogFurnitureItem(closetId))
    return list

def getAllFurnitures(index):
    # This function returns a list of all possible
    # CatalogFurnitureItems (that is, all color variants)
    # for the indicated type index(es).
    list = []
    colors = FurnitureTypes[index][FTColorOptions]
    for n in range(len(colors)):
        list.append(CatalogFurnitureItem(index, n))
    return list

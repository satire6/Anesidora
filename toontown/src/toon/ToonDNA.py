"""ToonDNA module: contains the methods and definitions for describing
multipart actors with a simple class"""

import random
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA

notify = directNotify.newCategory("ToonDNA")

# Warning!  DNA values are stored in the server database by indexing
# into these arrays.  Do not reorder entries in this array, or add
# things to the middle, or all toons already stored in the database
# will get screwed up.

toonSpeciesTypes = ['d',    # Dog
                    'c',    # Cat
                    'h',    # Horse
                    'm',    # Mouse
                    'r',    # Rabbit
                    'f',    # Duck
                    'p',    # Monkey
                    'b',    # Bear
                    's'     # Pig (swine)
                    ]

toonHeadTypes = [ "dls", "dss", "dsl", "dll",  # Dog
                  "cls", "css", "csl", "cll",  # Cat
                  "hls", "hss", "hsl", "hll",  # Horse
                  "mls", "mss",                # Mouse
                  "rls", "rss", "rsl", "rll",  # Rabbit
                  "fls", "fss", "fsl", "fll",  # Duck (Fowl)
                  "pls", "pss", "psl", "pll",  # Monkey (Primate)
                  "bls", "bss", "bsl", "bll",  # Bear
                  "sls", "sss", "ssl", "sll"   # Pig (swine)
                  ]
                  
def getHeadList(species):
    """
    Returns a list of head types given the species.
    This list returned is a subset of toonHeadTypes pertaining to only that species.
    """
    headList = []
    for head in toonHeadTypes:
        if (head[0] == species):
            headList.append(head)
    return headList

def getHeadStartIndex(species):
    """
    Returns an index of toonHeadTypes which corresponds to the start of
    the given species.
    """
    for head in toonHeadTypes:
        if (head[0] == species):
            return toonHeadTypes.index(head)
        
def getSpecies(head):
    """
    Returns the species when the head is given.
    """
    for species in toonSpeciesTypes:
        if (species == head[0]):
            return species
        
def getSpeciesName(head):
    """
    Returns the full name of the species in small letters
    given the head of the species.
    """
    species = getSpecies(head)
    if (species == 'd'):
        speciesName = 'dog'
    elif (species == 'c'):
        speciesName = 'cat'
    elif (species == 'h'):
        speciesName = 'horse'
    elif (species == 'm'):
        speciesName = 'mouse'
    elif (species == 'r'):
        speciesName = 'rabbit'
    elif (species == 'f'):
        speciesName = 'duck'
    elif (species == 'p'):
        speciesName = 'monkey'
    elif (species == 'b'):
        speciesName = 'bear'
    elif (species == 's'):
        speciesName = 'pig'
    return speciesName

# TODO: if base.wantNewSpecies


# NOTE: if you change the toonHeadTypes, please change below to match!
toonHeadAnimalIndices = [ 0, # start of dog heads
                          4, # start of cat heads
                          8, # start of horse heads
                          12, # start of mouse heads
                          14, # start of rabbit heads
                          18, # start of duck heads
                          22, # start of monkey heads
                          26, # start of bear heads
                          30, # start of pig heads
                          ]

# free trialers cannot be monkeys, bears, or horses
toonHeadAnimalIndicesTrial = [ 0, # start of dog heads
                               4, # start of cat heads
                               12, # start of mouse heads
                               14, # start of rabbit heads
                               18, # start of duck heads
                               30, # start of pig heads
                               ]
                               
allToonHeadAnimalIndices = [ 0, 1, 2, 3,     # Dog
                             4, 5, 6, 7,     # Cat
                             8, 9, 10, 11,   # Horse
                             12, 13,         # Mouse
                             14, 15, 16, 17, # Rabbit
                             18, 19, 20, 21, # Duck
                             22, 23, 24, 25, # Monkey
                             26, 27, 28, 29, # Bear
                             30, 31, 32, 33, # Pig
                            ]
                            
# Free trialers cannot be monkeys, Bears, or Horses
allToonHeadAnimalIndicesTrial = [ 0, 1, 2, 3,     # Dog
                                  4, 5, 6, 7,     # Cat
                                  12, 13,         # Mouse
                                  14, 15, 16, 17, # Rabbit
                                  18, 19, 20, 21, # Duck
                                  30, 31, 32, 33, # Pig
                                ]

toonTorsoTypes = [ "ss", "ms", "ls", "sd", "md", "ld", "s", "m", "l" ]
#    short shorts, medium shorts, long shorts,
#    short dress,  medium dress,  long dress.
#    short naked,  medium naked, long naked

toonLegTypes = [ "s", "m", "l" ] # Short, Medium, Long.

Shirts = [
    "phase_3/maps/desat_shirt_1.jpg", # 0 solid
    "phase_3/maps/desat_shirt_2.jpg", # 1 single stripe
    "phase_3/maps/desat_shirt_3.jpg", # 2 collar
    "phase_3/maps/desat_shirt_4.jpg", # 3 double stripe
    "phase_3/maps/desat_shirt_5.jpg", # 4 multiple stripes (boy)
    "phase_3/maps/desat_shirt_6.jpg", # 5 collar w/ pocket
    "phase_3/maps/desat_shirt_7.jpg", # 6 flower print (girl)
    "phase_3/maps/desat_shirt_8.jpg", # 7 special, flower trim (girl)
    "phase_3/maps/desat_shirt_9.jpg", # 8 hawaiian (boy)
    "phase_3/maps/desat_shirt_10.jpg", # 9 collar w/ 2 pockets
    "phase_3/maps/desat_shirt_11.jpg", # 10 bowling shirt 
    "phase_3/maps/desat_shirt_12.jpg", # 11 special, vest (boy)
    "phase_3/maps/desat_shirt_13.jpg", # 12 special (no color), denim vest (girl)
    "phase_3/maps/desat_shirt_14.jpg", # 13 peasant (girl)
    "phase_3/maps/desat_shirt_15.jpg", # 14 collar w/ ruffles
    "phase_3/maps/desat_shirt_16.jpg", # 15 peasant w/ mid stripe (girl)
    "phase_3/maps/desat_shirt_17.jpg", # 16 special (no color), soccer jersey
    "phase_3/maps/desat_shirt_18.jpg", # 17 special, lightning bolt
    "phase_3/maps/desat_shirt_19.jpg", # 18 special, jersey 19 (boy)
    "phase_3/maps/desat_shirt_20.jpg", # 19 guayavera (boy)
    "phase_3/maps/desat_shirt_21.jpg", # 20 hearts (girl)
    "phase_3/maps/desat_shirt_22.jpg", # 21 special, stars (girl)
    "phase_3/maps/desat_shirt_23.jpg", # 22 flower (girl)

    # Catalog exclusive shirts
    "phase_4/maps/female_shirt1b.jpg", # 23 blue with 3 yellow stripes
    "phase_4/maps/female_shirt2.jpg", # 24 pink and beige with flower
    "phase_4/maps/female_shirt3.jpg", # 25 yellow hooded sweatshirt (also for boys)
    "phase_4/maps/male_shirt1.jpg", # 26 blue stripes
    "phase_4/maps/male_shirt2_palm.jpg", # 27 yellow with palm tree
    "phase_4/maps/male_shirt3c.jpg", # 28 orange

    # Halloween
    "phase_4/maps/shirt_ghost.jpg", # 29 ghost (Halloween)
    "phase_4/maps/shirt_pumkin.jpg", # 30 pumpkin (Halloween)

    # Winter holiday
    "phase_4/maps/holiday_shirt1.jpg", # 31 (Winter Holiday)
    "phase_4/maps/holiday_shirt2b.jpg", # 32 (Winter Holiday)
    "phase_4/maps/holidayShirt3b.jpg", # 33 (Winter Holiday)
    "phase_4/maps/holidayShirt4.jpg", # 34 (Winter Holiday)

    # Catalog 2 exclusive shirts
    "phase_4/maps/female_shirt1b.jpg",    # 35 Blue and gold wavy stripes
    "phase_4/maps/female_shirt5New.jpg",  # 36 Blue and pink with bow
    "phase_4/maps/shirtMale4B.jpg",       # 37 Lime green with stripe
    "phase_4/maps/shirt6New.jpg",         # 38 Purple with stars
    "phase_4/maps/shirtMaleNew7.jpg",     # 39 Red kimono with checkerboard

    # Unused
    "phase_4/maps/femaleShirtNew6.jpg",   # 40 Aqua kimono white stripe

    # Valentines
    "phase_4/maps/Vday1Shirt5.jpg",       # 41 (Valentines)
    "phase_4/maps/Vday1Shirt6SHD.jpg",    # 42 (Valentines)
    "phase_4/maps/Vday1Shirt4.jpg",       # 43 (Valentines)
    "phase_4/maps/Vday_shirt2c.jpg",      # 44 (Valentines)

    # Catalog 3 exclusive shirts
    "phase_4/maps/shirtTieDyeNew.jpg",    # 45 Tie dye
    "phase_4/maps/male_shirt1.jpg",       # 46 Light blue with blue and white stripe

    # St Patrick's Day shirts
    "phase_4/maps/StPats_shirt1.jpg",     # 47 (St. Pats) Four leaf clover shirt
    "phase_4/maps/StPats_shirt2.jpg",     # 48 (St. Pats) Pot o gold

    # T-Shirt Contest shirts
    "phase_4/maps/ContestfishingVestShirt2.jpg",    # 49 (T-shirt Contest) Fishing Vest
    "phase_4/maps/ContestFishtankShirt1.jpg",       # 50 (T-shirt Contest) Fish Tank
    "phase_4/maps/ContestPawShirt1.jpg",            # 51 (T-shirt Contest) Paw Print

    # Catlog 4 exclusive shirts
    "phase_4/maps/CowboyShirt1.jpg",    # 52 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt2.jpg",    # 53 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt3.jpg",    # 54 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt4.jpg",    # 55 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt5.jpg",    # 56 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt6.jpg",    # 57 (Western) Cowboy Shirt

    # July 4 shirts
    "phase_4/maps/4thJulyShirt1.jpg",   # 58 (July 4th) Flag Shirt
    "phase_4/maps/4thJulyShirt2.jpg",   # 59 (July 4th) Fireworks Shirt

    # Catalog 7 exclusive shirts
    "phase_4/maps/shirt_Cat7_01.jpg",   # 60 Green w/ yellow buttons
    "phase_4/maps/shirt_Cat7_02.jpg",   # 61 Purple w/ big flower

    # T-Shirt Contest 2 shirts
    "phase_4/maps/contest_backpack3.jpg", # 62 Multicolor shirt w/ backpack
    "phase_4/maps/contest_leder.jpg",     # 63 Lederhosen
    "phase_4/maps/contest_mellon2.jpg",   # 64 Watermelon
    "phase_4/maps/contest_race2.jpg",     # 65 Race Shirt (UK winner)
    
    # Pajama shirts
    "phase_4/maps/PJBlueBanana2.jpg", # 66 Blue Banana PJ Shirt
    "phase_4/maps/PJRedHorn2.jpg", # 67 Red Horn PJ Shirt
    "phase_4/maps/PJGlasses2.jpg", # 68 Purple Glasses PJ Shirt
    
    # 2009 Valentines Day Shirts
    "phase_4/maps/tt_t_chr_avt_shirt_valentine1.jpg", # 69 Valentines Shirt 1
    "phase_4/maps/tt_t_chr_avt_shirt_valentine2.jpg", # 70 Valentines Shirt 2    
    
    # Award Clothes
    "phase_4/maps/tt_t_chr_avt_shirt_desat4.jpg",    # 71
    "phase_4/maps/tt_t_chr_avt_shirt_fishing1.jpg",   # 72
    "phase_4/maps/tt_t_chr_avt_shirt_fishing2.jpg",  # 73
    "phase_4/maps/tt_t_chr_avt_shirt_gardening1.jpg",   # 74
    "phase_4/maps/tt_t_chr_avt_shirt_gardening2.jpg",   # 75
    "phase_4/maps/tt_t_chr_avt_shirt_party1.jpg",   # 76
    "phase_4/maps/tt_t_chr_avt_shirt_party2.jpg",   # 77
    "phase_4/maps/tt_t_chr_avt_shirt_racing1.jpg",  # 78
    "phase_4/maps/tt_t_chr_avt_shirt_racing2.jpg",  # 79 
    "phase_4/maps/tt_t_chr_avt_shirt_summer1.jpg",   # 80
    "phase_4/maps/tt_t_chr_avt_shirt_summer2.jpg",   # 81
    
    "phase_4/maps/tt_t_chr_avt_shirt_golf1.jpg",    # 82
    "phase_4/maps/tt_t_chr_avt_shirt_golf2.jpg",    # 83
    "phase_4/maps/tt_t_chr_avt_shirt_halloween1.jpg",   # 84
    "phase_4/maps/tt_t_chr_avt_shirt_halloween2.jpg",   # 85
    "phase_4/maps/tt_t_chr_avt_shirt_marathon1.jpg",    # 86
    "phase_4/maps/tt_t_chr_avt_shirt_saveBuilding1.jpg",    # 87
    "phase_4/maps/tt_t_chr_avt_shirt_saveBuilding2.jpg",    # 88 
    "phase_4/maps/tt_t_chr_avt_shirt_toonTask1.jpg",    # 89
    "phase_4/maps/tt_t_chr_avt_shirt_toonTask2.jpg",    # 90
    "phase_4/maps/tt_t_chr_avt_shirt_trolley1.jpg",     # 91
    "phase_4/maps/tt_t_chr_avt_shirt_trolley2.jpg",     # 92
    "phase_4/maps/tt_t_chr_avt_shirt_winter1.jpg",      # 93
    "phase_4/maps/tt_t_chr_avt_shirt_halloween3.jpg",   # 94
    "phase_4/maps/tt_t_chr_avt_shirt_halloween4.jpg",   # 95
    # 2010 Valentines Day Shirts
    "phase_4/maps/tt_t_chr_avt_shirt_valentine3.jpg", # 96 Valentines Shirt 3
    
    # Scientist Shirts
    "phase_4/maps/tt_t_chr_shirt_scientistC.jpg",   # 97
    "phase_4/maps/tt_t_chr_shirt_scientistA.jpg",   # 98
    "phase_4/maps/tt_t_chr_shirt_scientistB.jpg",   # 99
    
    # Silly Story Shirts
    "phase_4/maps/tt_t_chr_avt_shirt_mailbox.jpg",  # 100 Mailbox Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_trashcan.jpg", # 101 Trash Can Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_loonyLabs.jpg",# 102 Loony Labs Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_hydrant.jpg",  # 103 Hydrant Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_whistle.jpg",  # 104 Sillymeter Whistle Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_cogbuster.jpg",  # 105 Silly Cogbuster Shirt
    
    "phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated01.jpg",  # 106 Most Cogs Defeated Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_victoryParty01.jpg",  # 107 Victory Party Shirt 1
    "phase_4/maps/tt_t_chr_avt_shirt_victoryParty02.jpg",  # 108 Victory Party Shirt 2
    ]

# These are deemed safe for MakeAToon
BoyShirts = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (8, 8), (9, 9), (10, 0), (11, 0), (14, 10), (16, 0), (17, 0), (18, 12), (19, 13)]
GirlShirts = [(0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7), (9, 9), (12, 0), (13, 11), (15, 11), (16, 0), (20, 0), (21, 0), (22, 0)]

def isValidBoyShirt(index):
    for pair in BoyShirts:
        if (index == pair[0]):
            return 1
    return 0

def isValidGirlShirt(index):
    for pair in GirlShirts:
        if (index == pair[0]):
            return 1
    return 0

Sleeves = [
    "phase_3/maps/desat_sleeve_1.jpg", # 0
    "phase_3/maps/desat_sleeve_2.jpg", # 1
    "phase_3/maps/desat_sleeve_3.jpg", # 2 
    "phase_3/maps/desat_sleeve_4.jpg", # 3
    "phase_3/maps/desat_sleeve_5.jpg", # 4 
    "phase_3/maps/desat_sleeve_6.jpg", # 5
    "phase_3/maps/desat_sleeve_7.jpg", # 6
    "phase_3/maps/desat_sleeve_8.jpg", # 7 
    "phase_3/maps/desat_sleeve_9.jpg", # 8
    "phase_3/maps/desat_sleeve_10.jpg", # 9
    "phase_3/maps/desat_sleeve_15.jpg", # 10
    "phase_3/maps/desat_sleeve_16.jpg", # 11
    "phase_3/maps/desat_sleeve_19.jpg", # 12
    "phase_3/maps/desat_sleeve_20.jpg", # 13

    # Catalog exclusive shirt sleeves
    "phase_4/maps/female_sleeve1b.jpg", # 14 blue with 3 yellow stripes
    "phase_4/maps/female_sleeve2.jpg", # 15 pink and beige with flower
    "phase_4/maps/female_sleeve3.jpg", # 16 yellow hooded sweatshirt
    "phase_4/maps/male_sleeve1.jpg", # 17 blue stripes
    "phase_4/maps/male_sleeve2_palm.jpg", # 18 yellow with palm tree
    "phase_4/maps/male_sleeve3c.jpg", # 19 orange

    "phase_4/maps/shirt_Sleeve_ghost.jpg", # 20 ghost (Halloween)
    "phase_4/maps/shirt_Sleeve_pumkin.jpg", # 21 pumpkin (Halloween)

    "phase_4/maps/holidaySleeve1.jpg", # 22 (Winter Holiday)
    "phase_4/maps/holidaySleeve3.jpg", # 23 (Winter Holiday)

    # Catalog series 2
    "phase_4/maps/female_sleeve1b.jpg",   # 24 Blue and gold wavy stripes
    "phase_4/maps/female_sleeve5New.jpg", # 25 Blue and pink with bow
    "phase_4/maps/male_sleeve4New.jpg",   # 26 Lime green with stripe
    "phase_4/maps/sleeve6New.jpg",        # 27 Purple with stars
    "phase_4/maps/SleeveMaleNew7.jpg",    # 28 Red kimono/hockey shirt

    # Unused
    "phase_4/maps/female_sleeveNew6.jpg", # 29 Aqua kimono white stripe

    "phase_4/maps/Vday5Sleeve.jpg",       # 30 (Valentines)
    "phase_4/maps/Vda6Sleeve.jpg",        # 31 (Valentines)
    "phase_4/maps/Vday_shirt4sleeve.jpg", # 32 (Valentines)
    "phase_4/maps/Vday2cSleeve.jpg",      # 33 (Valentines)

    # Catalog series 3
    "phase_4/maps/sleeveTieDye.jpg",      # 34 Tie dye
    "phase_4/maps/male_sleeve1.jpg",      # 35 Blue with blue and white stripe

    # St. Patrick's day
    "phase_4/maps/StPats_sleeve.jpg",     # 36 (St. Pats) Four leaf clover
    "phase_4/maps/StPats_sleeve2.jpg",    # 37 (St. Pats) Pot o gold

    # T-Shirt Contest sleeves
    "phase_4/maps/ContestfishingVestSleeve1.jpg",    # 38 (T-Shirt Contest) fishing vest sleeve
    "phase_4/maps/ContestFishtankSleeve1.jpg",       # 39 (T-Shirt Contest) fish bowl sleeve
    "phase_4/maps/ContestPawSleeve1.jpg",            # 40 (T-Shirt Contest) paw print sleeve

    # Catalog Series 4
    "phase_4/maps/CowboySleeve1.jpg",    # 41 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve2.jpg",    # 42 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve3.jpg",    # 43 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve4.jpg",    # 44 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve5.jpg",    # 45 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve6.jpg",    # 46 (Western) cowboy shirt sleeve

    # July 4th
    "phase_4/maps/4thJulySleeve1.jpg",   # 47 (July 4th) flag shirt sleeve
    "phase_4/maps/4thJulySleeve2.jpg",   # 48 (July 4th) fireworks shirt sleeve

    # Catlog series 7
    "phase_4/maps/shirt_sleeveCat7_01.jpg",   # 49 Green shirt w/ yellow buttons sleeve
    "phase_4/maps/shirt_sleeveCat7_02.jpg",   # 50 Purple shirt w/ big flower sleeve

    # T-Shirt Contest 2 sleeves
    "phase_4/maps/contest_backpack_sleeve.jpg",   # 51 (T-Shirt Contest) Multicolor shirt 2/ backpack sleeve
    "phase_4/maps/Contest_leder_sleeve.jpg",      # 52 (T-Shirt Contest) Lederhosen sleeve
    "phase_4/maps/contest_mellon_sleeve2.jpg",     # 53 (T-Shirt Contest) Watermelon sleeve
    "phase_4/maps/contest_race_sleeve.jpg",       # 54 (T-Shirt Contest) Race Shirt sleeve (UK winner)
    
    # Pajama sleeves
    "phase_4/maps/PJSleeveBlue.jpg",   # 55 Blue Pajama sleeve
    "phase_4/maps/PJSleeveRed.jpg",   # 56 Red Pajama sleeve
    "phase_4/maps/PJSleevePurple.jpg",   # 57 Purple Pajama sleeve
    
    # 2009 Valentines Day Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine1.jpg",   # 58 Valentines Sleeves 1
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine2.jpg",   # 59 Valentines Sleeves 2
    
    # Special Award Clothing
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_desat4.jpg",   # 60
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing1.jpg",   # 61
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing2.jpg",   # 62
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening1.jpg",   # 63
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening2.jpg",   # 64
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_party1.jpg",   # 65
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_party2.jpg",   # 66
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_racing1.jpg",   # 67
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_racing2.jpg",   # 68
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_summer1.jpg",   # 69
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_summer2.jpg",   # 70
    
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_golf1.jpg",    # 71
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_golf2.jpg",    # 72
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween1.jpg",    # 73
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween2.jpg",    # 74
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_marathon1.jpg",    # 75
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding1.jpg",    # 76
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding2.jpg",    # 77
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask1.jpg",    # 78
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask2.jpg",    # 79
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley1.jpg",    # 80
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley2.jpg",    # 81
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_winter1.jpg",    # 82
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween3.jpg",   # 83
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween4.jpg",   # 84
    
    # 2010 Valentines Day Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine3.jpg",   # 85 Valentines Sleeves 1
    
    # Scientist Sleeves
    "phase_4/maps/tt_t_chr_shirtSleeve_scientist.jpg",   # 86 Toon sceintist
    
    # Silly Story Shirt Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_mailbox.jpg",    # 87 Mailbox Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_trashcan.jpg",   # 88 Trash Can Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_loonyLabs.jpg",  # 89 Loony Labs Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_hydrant.jpg",    # 90 Hydrant Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_whistle.jpg",    # 91 Sillymeter Whistle Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_cogbuster.jpg",    # 92 Silly Cogbuster Sleeves
    
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated01.jpg",# 93 Most Cogs Defeated Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty01.jpg",    # 94 Victory Party Sleeves 1
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty02.jpg",    # 95 Victory Party Sleeves 2
    ]

# len = 9 
BoyShorts = [
    "phase_3/maps/desat_shorts_1.jpg", # plain w/ pockets
    "phase_3/maps/desat_shorts_2.jpg", # belt
    "phase_3/maps/desat_shorts_4.jpg", # cargo
    "phase_3/maps/desat_shorts_6.jpg", # hawaiian
    "phase_3/maps/desat_shorts_7.jpg", # special, side stripes
    "phase_3/maps/desat_shorts_8.jpg", # soccer shorts 
    "phase_3/maps/desat_shorts_9.jpg", # special, flames side stripes
    "phase_3/maps/desat_shorts_10.jpg", # denim (2 darker colors)

    # Valentines
    "phase_4/maps/VdayShorts2.jpg",    # 8 valentines shorts

    # Catalog series 3 exclusive
    "phase_4/maps/shorts4.jpg",        # 9 Orange with blue side stripes
    "phase_4/maps/shorts1.jpg",        # 10 Blue with gold stripes on cuff

    # St. Pats
    "phase_4/maps/shorts5.jpg",        # 11 Leprechaun shorts

    # Catalog series 4 exclusive
    "phase_4/maps/CowboyShorts1.jpg",  # 12 Cowboy Shorts 1
    "phase_4/maps/CowboyShorts2.jpg",  # 13 Cowboy Shorts 2
    # July 4th
    "phase_4/maps/4thJulyShorts1.jpg", # 14 July 4th Shorts

    # Catalog series 7
    "phase_4/maps/shortsCat7_01.jpg",  # 15 Green stripes
    
    # Pajama Shorts
    "phase_4/maps/Blue_shorts_1.jpg",  # 16 Blue Pajama shorts
    "phase_4/maps/Red_shorts_1.jpg",  # 17 Red Pajama shorts
    "phase_4/maps/Purple_shorts_1.jpg",  # 18 Purple Pajama shorts
    
    # Winter Holiday Shorts
    "phase_4/maps/tt_t_chr_avt_shorts_winter1.jpg",  # 19 Winter Holiday Shorts Style 1
    "phase_4/maps/tt_t_chr_avt_shorts_winter2.jpg",  # 20 Winter Holiday Shorts Style 2
    "phase_4/maps/tt_t_chr_avt_shorts_winter3.jpg",  # 21 Winter Holiday Shorts Style 3
    "phase_4/maps/tt_t_chr_avt_shorts_winter4.jpg",  # 22 Winter Holiday Shorts Style 4
    
    # 2009 Valentines Day Shorts
    "phase_4/maps/tt_t_chr_avt_shorts_valentine1.jpg",  # 23 Valentines Shorts 1
    "phase_4/maps/tt_t_chr_avt_shorts_valentine2.jpg",  # 24 Valentines Shorts 2
    
    # Special award Clothes
    "phase_4/maps/tt_t_chr_avt_shorts_fishing1.jpg",   # 25
    "phase_4/maps/tt_t_chr_avt_shorts_gardening1.jpg",   # 26
    "phase_4/maps/tt_t_chr_avt_shorts_party1.jpg",   # 27
    "phase_4/maps/tt_t_chr_avt_shorts_racing1.jpg",   # 28
    "phase_4/maps/tt_t_chr_avt_shorts_summer1.jpg",   # 29
    
    "phase_4/maps/tt_t_chr_avt_shorts_golf1.jpg",   # 30
    "phase_4/maps/tt_t_chr_avt_shorts_halloween1.jpg",   # 31
    "phase_4/maps/tt_t_chr_avt_shorts_halloween2.jpg",   # 32
    "phase_4/maps/tt_t_chr_avt_shorts_saveBuilding1.jpg",   # 33
    "phase_4/maps/tt_t_chr_avt_shorts_trolley1.jpg",   # 34
    "phase_4/maps/tt_t_chr_avt_shorts_halloween4.jpg",   # 35
    "phase_4/maps/tt_t_chr_avt_shorts_halloween3.jpg",   # 36
    
    "phase_4/maps/tt_t_chr_shorts_scientistA.jpg",   # 37
    "phase_4/maps/tt_t_chr_shorts_scientistB.jpg",   # 38
    "phase_4/maps/tt_t_chr_shorts_scientistC.jpg",   # 39
    
    "phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg",  # 40 Silly Cogbuster Shorts     
    ]

SHORTS = 0
SKIRT = 1

# len = 14 
GirlBottoms = [
    ("phase_3/maps/desat_skirt_1.jpg", SKIRT), # 0 solid
    ("phase_3/maps/desat_skirt_2.jpg", SKIRT), # 1 special, polka dots
    ("phase_3/maps/desat_skirt_3.jpg", SKIRT), # 2 vertical stripes
    ("phase_3/maps/desat_skirt_4.jpg", SKIRT), # 3 horizontal stripe
    ("phase_3/maps/desat_skirt_5.jpg", SKIRT), # 4 flower print
    ("phase_3/maps/desat_shorts_1.jpg", SHORTS), # 5 plain w/ pockets
    ("phase_3/maps/desat_shorts_5.jpg", SHORTS), # 6 flower
    ("phase_3/maps/desat_skirt_6.jpg", SKIRT), # 7 special, 2 pockets
    ("phase_3/maps/desat_skirt_7.jpg", SKIRT), # 8 denim (2 darker colors)
    ("phase_3/maps/desat_shorts_10.jpg", SHORTS), # 9 denim (2 darker colors)

    # Catalog Series 1 exclusive
    ("phase_4/maps/female_skirt1.jpg", SKIRT), # 10 blue with tan border and button
    ("phase_4/maps/female_skirt2.jpg", SKIRT), # 11 purple with pink border and ribbon
    ("phase_4/maps/female_skirt3.jpg", SKIRT), # 12 teal with yellow border and star

    # Valentines
    ("phase_4/maps/VdaySkirt1.jpg", SKIRT),    # 13 valentines skirts

    # Catalog Series 3 exclusive
    ("phase_4/maps/skirtNew5.jpg", SKIRT),     # 14 rainbow skirt

    ("phase_4/maps/shorts5.jpg", SHORTS),      # 15 leprechaun shorts
    # St. Pats

    # Catalog Series 4 exclusive
    ("phase_4/maps/CowboySkirt1.jpg", SKIRT),     # 16 cowboy skirt 1
    ("phase_4/maps/CowboySkirt2.jpg", SKIRT),     # 17 cowboy skirt 2

    # July 4th Skirt
    ("phase_4/maps/4thJulySkirt1.jpg", SKIRT),    # 18 july 4th skirt 1

    # Catalog series 7
    ("phase_4/maps/skirtCat7_01.jpg", SKIRT),    # 19 blue with flower
    
    # Pajama Shorts
    ("phase_4/maps/Blue_shorts_1.jpg", SHORTS),  # 20 Blue Pajama shorts
    ("phase_4/maps/Red_shorts_1.jpg", SHORTS),   # 21 Red Pajama shorts
    ("phase_4/maps/Purple_shorts_1.jpg", SHORTS),# 22 Purple Pajama shorts
    
    # Winter Holiday Skirts
    ("phase_4/maps/tt_t_chr_avt_skirt_winter1.jpg", SKIRT),  # 23 Winter Holiday Skirt Style 1
    ("phase_4/maps/tt_t_chr_avt_skirt_winter2.jpg", SKIRT),  # 24 Winter Holiday Skirt Style 2
    ("phase_4/maps/tt_t_chr_avt_skirt_winter3.jpg", SKIRT),  # 25 Winter Holiday Skirt Style 3
    ("phase_4/maps/tt_t_chr_avt_skirt_winter4.jpg", SKIRT),  # 26 Winter Holiday Skirt Style 4
    
    # 2009 Valentines Day Skirts
    ("phase_4/maps/tt_t_chr_avt_skirt_valentine1.jpg", SKIRT),  # 27 Valentines Skirt 1
    ("phase_4/maps/tt_t_chr_avt_skirt_valentine2.jpg", SKIRT),  # 28 Valentines Skirt 2
    
    # Special award clothing
    ("phase_4/maps/tt_t_chr_avt_skirt_fishing1.jpg", SKIRT),   # 29
    ("phase_4/maps/tt_t_chr_avt_skirt_gardening1.jpg", SKIRT),   # 30
    ("phase_4/maps/tt_t_chr_avt_skirt_party1.jpg", SKIRT),   # 31
    ("phase_4/maps/tt_t_chr_avt_skirt_racing1.jpg", SKIRT),   # 32
    ("phase_4/maps/tt_t_chr_avt_skirt_summer1.jpg", SKIRT),   # 33
    
    ("phase_4/maps/tt_t_chr_avt_skirt_golf1.jpg", SKIRT),   # 34
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween1.jpg", SKIRT),   # 35
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween2.jpg", SKIRT),   # 36
    ("phase_4/maps/tt_t_chr_avt_skirt_saveBuilding1.jpg", SKIRT),   # 37
    ("phase_4/maps/tt_t_chr_avt_skirt_trolley1.jpg", SKIRT),   # 38
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween3.jpg", SKIRT),   # 39
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween4.jpg", SKIRT),   # 40
    
    ("phase_4/maps/tt_t_chr_shorts_scientistA.jpg", SHORTS),   # 41
    ("phase_4/maps/tt_t_chr_shorts_scientistB.jpg", SHORTS),   # 42
    ("phase_4/maps/tt_t_chr_shorts_scientistC.jpg", SHORTS),   # 43
    
    ("phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg", SHORTS),   # 44 Silly Cogbuster Shorts 
    ]

# len = 28
ClothesColors = [
    # Boy shirts (0 - 12)
    VBase4(0.933594, 0.265625, 0.28125, 1.0),  # (0) bright red
    VBase4(0.863281, 0.40625, 0.417969, 1.0),  # (1) light red
    VBase4(0.710938, 0.234375, 0.4375, 1.0),   # (2) plum
    VBase4(0.992188, 0.480469, 0.167969, 1.0), # (3) orange
    VBase4(0.996094, 0.898438, 0.320312, 1.0), # (4) yellow
    VBase4(0.550781, 0.824219, 0.324219, 1.0), # (5) light green
    VBase4(0.242188, 0.742188, 0.515625, 1.0), # (6) seafoam   
    VBase4(0.433594, 0.90625, 0.835938, 1.0),  # (7) light blue green
    VBase4(0.347656, 0.820312, 0.953125, 1.0), # (8) light blue
    VBase4(0.191406, 0.5625, 0.773438, 1.0),   # (9) medium blue
    VBase4(0.285156, 0.328125, 0.726562, 1.0),
    VBase4(0.460938, 0.378906, 0.824219, 1.0), # (11) purple blue
    VBase4(0.546875, 0.28125, 0.75, 1.0),      # (12) dark purple blue
    # Boy shorts
    VBase4(0.570312, 0.449219, 0.164062, 1.0),
    VBase4(0.640625, 0.355469, 0.269531, 1.0),
    VBase4(0.996094, 0.695312, 0.511719, 1.0),
    VBase4(0.832031, 0.5, 0.296875, 1.0),
    VBase4(0.992188, 0.480469, 0.167969, 1.0),
    VBase4(0.550781, 0.824219, 0.324219, 1.0),
    VBase4(0.433594, 0.90625, 0.835938, 1.0),
    VBase4(0.347656, 0.820312, 0.953125, 1.0),
    # Girl clothes
    VBase4(0.96875, 0.691406, 0.699219, 1.0),  # (21) light pink 
    VBase4(0.996094, 0.957031, 0.597656, 1.0), # (22) light yellow
    VBase4(0.855469, 0.933594, 0.492188, 1.0), # (23) light yellow green
    VBase4(0.558594, 0.589844, 0.875, 1.0),    # (24) light purple
    VBase4(0.726562, 0.472656, 0.859375, 1.0), # (25) medium purple
    VBase4(0.898438, 0.617188, 0.90625, 1.0),  # (26) purple
    # Special
    VBase4(1.0, 1.0, 1.0, 1.0),                # (27) white
    # Pajama colors
    # Not using these colors yet, possibly for gloves
    VBase4(0.0, 0.2, 0.956862, 1.0),           # (28) Blue Banana Pajama
    VBase4(0.972549, 0.094117, 0.094117, 1.0), # (29) Red Horn Pajama
    VBase4(0.447058, 0.0, 0.901960, 1.0),      # (30) Purple Glasses Pajama
    ]

# If you add to this, please add to TTLocalizer.ShirtStyleDescriptions
ShirtStyles = {
    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]
    # -------------------------------------------------------------------------
    # Boy styles
    # -------------------------------------------------------------------------
    # solid 
    'bss1' : [ 0, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # single stripe
    'bss2' : [ 1, 1, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # collar
    'bss3' : [ 2, 2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # double stripe
    'bss4' : [ 3, 3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # multiple stripes
    'bss5' : [ 4, 4, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # collar w/ pocket
    'bss6' : [ 5, 5, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # hawaiian
    'bss7' : [ 8, 8, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (8, 8), (9, 9), (11, 11), (12, 12), (27, 27) ]],
    # collar w/ 2 pockets
    'bss8' : [ 9, 9, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # bowling shirt
    'bss9' : [ 10, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # vest (special)
    'bss10' : [ 11, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # collar w/ ruffles
    'bss11' : [ 14, 10, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # soccer jersey (special)
    'bss12' : [ 16, 0, [(27, 27), (27, 4), (27, 5), (27, 6), (27, 7),
                    (27, 8), (27, 9)]],
    # lightning bolt (special)
    'bss13' : [ 17, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # jersey 19 (special)
    'bss14' : [ 18, 12, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (8, 8), (9, 9), (11, 11), (12, 12), (27, 27) ]],
    # guayavera 
    'bss15' : [ 19, 13, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # -------------------------------------------------------------------------
    # Girl styles
    # -------------------------------------------------------------------------
    # solid
    'gss1' : [ 0, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26),
                    (27, 27)]],
    # single stripe
    'gss2' : [ 1, 1, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # collar
    'gss3' : [ 2, 2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # double stripes
    'gss4' : [ 3, 3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # collar w/ pocket
    'gss5' : [ 5, 5, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # flower print
    'gss6' : [ 6, 6, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # flower trim (special)
    'gss7' : [ 7, 7, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # collar w/ 2 pockets
    'gss8' : [ 9, 9, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # denim vest (special)
    'gss9' : [ 12, 0, [(27, 27)]],
    # peasant
    'gss10' : [ 13, 11, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), 
                    (26, 26) ]],
    # peasant w/ mid stripe
    'gss11' : [ 15, 11, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],
    # soccer jersey (special)
    'gss12' : [ 16, 0, [(27, 27), (27, 4), (27, 5), (27, 6), (27, 7),
                    (27, 8), (27, 9)]],
    # hearts
    'gss13' : [ 20, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],
    # stars (special)
    'gss14' : [ 21, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],
    # flower
    'gss15' : [ 22, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],


    # Special Catalog-only shirts.
    
    # yellow hooded - Series 1
    'c_ss1' : [ 25, 16, [(27, 27),]],

    # yellow with palm tree - Series 1
    'c_ss2' : [ 27, 18, [(27, 27),]],

    # purple with stars - Series 2
    'c_ss3' : [ 38, 27, [(27, 27),]],

    # blue stripes (boys only) - Series 1
    'c_bss1' : [ 26, 17, [(27, 27),]],

    # orange (boys only) - Series 1
    'c_bss2' : [ 28, 19, [(27, 27),]],

    # lime green with stripe (boys only) - Series 2
    'c_bss3' : [ 37, 26, [(27, 27),]],

    # red kimono with checkerboard (boys only) - Series 2
    'c_bss4' : [ 39, 28, [(27, 27),]],

    # blue with yellow stripes (girls only) - Series 1
    'c_gss1' : [ 23, 14, [(27, 27), ]],
    
    # pink and beige with flower (girls only) - Series 1
    'c_gss2' : [ 24, 15, [(27, 27), ]],

    # Blue and gold with wavy stripes (girls only) - Series 2
    'c_gss3' : [ 35, 24, [(27, 27), ]],

    # Blue and pink with bow (girls only) - Series 2
    'c_gss4' : [ 36, 25, [(27, 27), ]],

    # Aqua kimono white stripe (girls only) - UNUSED
    'c_gss5' : [ 40, 29, [(27, 27), ]],

    # Tie dye shirt (boys and girls) - Series 3
    'c_ss4'  : [45, 34, [(27, 27), ]],

    # light blue with blue and white stripe (boys only) - Series 3
    'c_ss5' : [ 46, 35, [(27, 27), ]],

    # cowboy shirt 1-6 : Series 4
    'c_ss6' : [ 52, 41, [(27, 27), ]],
    'c_ss7' : [ 53, 42, [(27, 27), ]],
    'c_ss8' : [ 54, 43, [(27, 27), ]],
    'c_ss9' : [ 55, 44, [(27, 27), ]],
    'c_ss10' : [ 56, 45, [(27, 27), ]],
    'c_ss11' : [ 57, 46, [(27, 27), ]],
    
    # Special Holiday-themed shirts.

    # Halloween ghost
    'hw_ss1' : [ 29, 20, [(27, 27), ]],
    # Halloween pumpkin
    'hw_ss2' : [ 30, 21, [(27, 27), ]],

    # Winter Holiday
    'wh_ss1' : [ 31, 22, [(27, 27), ]],
    # Winter Holiday
    'wh_ss2' : [ 32, 22, [(27, 27), ]],
    # Winter Holiday
    'wh_ss3' : [ 33, 23, [(27, 27), ]],
    # Winter Holiday
    'wh_ss4' : [ 34, 23, [(27, 27), ]],

    # Valentines day, pink with red hearts (girls)
    'vd_ss1' : [ 41, 30, [(27, 27), ]],
    # Valentines day, red with white hearts
    'vd_ss2' : [ 42, 31, [(27, 27), ]],
    # Valentines day, white with winged hearts (boys)
    'vd_ss3' : [ 43, 32, [(27, 27), ]],
    # Valentines day, pink with red flamed heart
    'vd_ss4' : [ 44, 33, [(27, 27), ]],
    # 2009 Valentines day, white with red cupid
    'vd_ss5' : [ 69, 58, [(27, 27), ]],
    # 2009 Valentines day, blue with green and red hearts
    'vd_ss6' : [ 70, 59, [(27, 27), ]],
    # 2010 Valentines day, red with white wings
    'vd_ss7' : [ 96, 85, [(27, 27), ]],
    # St Pat's Day, four leaf clover shirt
    'sd_ss1' : [ 47, 36, [(27, 27), ]],
    # St Pat's Day, pot o gold shirt
    'sd_ss2' : [ 48, 37, [(27, 27), ]],

    # T-Shirt Contest, Fishing Vest
    'tc_ss1' : [ 49, 38, [(27, 27), ]],
    # T-Shirt Contest, Fish Bowl    
    'tc_ss2' : [ 50, 39, [(27, 27), ]],
    # T-Shirt Contest, Paw Print    
    'tc_ss3' : [ 51, 40, [(27, 27), ]],
    # T-Shirt Contest, Backpack
    'tc_ss4' : [ 62, 51, [(27, 27), ]],
    # T-Shirt Contest, Lederhosen    
    'tc_ss5' : [ 63, 52, [(27, 27), ]],
    # T-Shirt Contest, Watermelon    
    'tc_ss6' : [ 64, 53, [(27, 27), ]],
    # T-Shirt Contest, Race Shirt    
    'tc_ss7' : [ 65, 54, [(27, 27), ]],

    # July 4th, Flag
    'j4_ss1' : [ 58, 47, [(27, 27), ]],
    # July 4th, Fireworks
    'j4_ss2' : [ 59, 48, [(27, 27), ]],

    # Catalog series 7, Green w/ yellow buttons
    'c_ss12' : [ 60, 49, [(27, 27), ]], 

    # Catalog series 7, Purple w/ big flower
    'c_ss13' : [ 61, 50, [(27, 27), ]],
    
    # Pajama series
    'pj_ss1' : [66, 55, [(27, 27),]], # Blue Banana Pajama shirt
    'pj_ss2' : [67, 56, [(27, 27),]], # Red Horn Pajama shirt
    'pj_ss3' : [68, 57, [(27, 27),]], # Purple Glasses Pajama shirt
    
    # Special Award Clothes    
    'sa_ss1' : [ 71, 60, [(27, 27),]],
    'sa_ss2' : [ 72, 61, [(27, 27),]],
    'sa_ss3' : [ 73, 62, [(27, 27),]],
    'sa_ss4' : [ 74, 63, [(27, 27),]],
    'sa_ss5' : [ 75, 64, [(27, 27),]],
    'sa_ss6' : [ 76, 65, [(27, 27),]],
    'sa_ss7' : [ 77, 66, [(27, 27),]],
    'sa_ss8' : [ 78, 67, [(27, 27),]],
    'sa_ss9' : [ 79, 68, [(27, 27),]],
    'sa_ss10' : [ 80, 69, [(27, 27),]],
    'sa_ss11' : [ 81, 70, [(27, 27),]],
    'sa_ss12' : [ 82, 71, [(27, 27),]],
    'sa_ss13' : [ 83, 72, [(27, 27),]],
    'sa_ss14' : [ 84, 73, [(27, 27),]],
    'sa_ss15' : [ 85, 74, [(27, 27),]],
    'sa_ss16' : [ 86, 75, [(27, 27),]],
    'sa_ss17' : [ 87, 76, [(27, 27),]],
    'sa_ss18' : [ 88, 77, [(27, 27),]],
    'sa_ss19' : [ 89, 78, [(27, 27),]],
    'sa_ss20' : [ 90, 79, [(27, 27),]],
    'sa_ss21' : [ 91, 80, [(27, 27),]],
    'sa_ss22' : [ 92, 81, [(27, 27),]],
    'sa_ss23' : [ 93, 82, [(27, 27),]],
    'sa_ss24' : [ 94, 83, [(27, 27),]],
    'sa_ss25' : [ 95, 84, [(27, 27),]],
    'sa_ss26' : [ 106, 93, [(27, 27), ]], # Most Cogs Defeated Shirt
    
    # Scientists
    'sc_1' : [ 97, 86, [(27, 27),]],
    'sc_2' : [ 98, 86, [(27, 27),]],
    'sc_3' : [ 99, 86, [(27, 27),]],
    
    # Silly Story Shirts
    'sil_1' : [ 100, 87, [(27, 27),]],   # Silly Mailbox Shirt
    'sil_2' : [ 101, 88, [(27, 27),]],   # Silly Trashcan Shirt
    'sil_3' : [ 102, 89, [(27, 27),]],   # Loony Labs Shirt
    'sil_4' : [ 103, 90, [(27, 27),]],   # Silly Hydrant Shirt
    'sil_5' : [ 104, 91, [(27, 27),]],   # Sillymeter Whistle Shirt
    'sil_6' : [ 105, 92, [(27, 27),]],   # Silly Cogbuster Shirt
    'sil_7' : [ 107, 94, [(27, 27),]],   # Victory Party Shirt 1
    'sil_8' : [ 108, 95, [(27, 27),]],   # Victory Party Shirt 2
    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]
    }

# If you add to this, please add to TTLocalizer.BottomStylesDescriptions
BottomStyles = {
    # name : [ bottomIdx, [bottomColorIdx, ...]]
    # -------------------------------------------------------------------------
    # Boy styles (shorts)
    # -------------------------------------------------------------------------
    # plain w/ pockets
    'bbs1' : [ 0, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # belt
    'bbs2' : [ 1, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # cargo
    'bbs3' : [ 2, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # hawaiian
    'bbs4' : [ 3, [0, 1, 2, 4, 6, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 
                                                                        27]],
    # side stripes (special)
    'bbs5' : [ 4, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # soccer shorts
    'bbs6' : [ 5, [0, 1, 2, 4, 6, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20,
                                                                        27]],
    # side flames (special) 
    'bbs7' : [ 6, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                                                                   20, 27]],
    # denim
    'bbs8' : [ 7, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                   20, 27]],
    # Valentines shorts
    'vd_bs1' : [ 8, [ 27, ]],
    # Green with red heart
    'vd_bs2' : [ 23, [ 27, ]],
    # Blue denim with green and red heart
    'vd_bs3' : [ 24, [ 27, ]],

    # Catalog only shorts
    # Orange with blue side stripes
    'c_bs1' : [ 9, [ 27, ]],
    
    # Blue with gold cuff stripes
    'c_bs2' : [ 10, [ 27, ]],

    # Green stripes - series 7
    'c_bs5' : [ 15, [ 27, ]],
    
    # St. Pats leprechaun shorts
    'sd_bs1' : [ 11, [27, ]],
    
    # Pajama shorts
    'pj_bs1' : [ 16, [27, ]], # Blue Banana Pajama pants
    'pj_bs2' : [ 17, [27, ]], # Red Horn Pajama pants
    'pj_bs3' : [ 18, [27, ]], # Purple Glasses Pajama pants
    
    # Winter Holiday Shorts
    'wh_bs1' : [ 19, [27, ]], # Winter Holiday Shorts Style 1
    'wh_bs2' : [ 20, [27, ]], # Winter Holiday Shorts Style 2
    'wh_bs3' : [ 21, [27, ]], # Winter Holiday Shorts Style 3
    'wh_bs4' : [ 22, [27, ]], # Winter Holiday Shorts Style 4
    
    # -------------------------------------------------------------------------
    # Girl styles (shorts and skirts)
    # -------------------------------------------------------------------------
    # skirts
    # -------------------------------------------------------------------------
    # solid
    'gsk1' : [ 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],
    # polka dots (special)
    'gsk2' : [ 1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # vertical stripes
    'gsk3' : [ 2, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # horizontal stripe
    'gsk4' : [ 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # flower print
    'gsk5' : [ 4, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # 2 pockets (special) 
    'gsk6' : [ 7, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                   26, 27]],
    # denim
    'gsk7' : [ 8, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                   26, 27]],
    
    # shorts
    # -------------------------------------------------------------------------
    # plain w/ pockets
    'gsh1' : [ 5, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],
    # flower
    'gsh2' : [ 6, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],
    # denim
    'gsh3' : [ 9, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],

    # Special catalog-only skirts and shorts.

    # blue skirt with tan border and button
    'c_gsk1' : [ 10, [ 27, ]],

    # purple skirt with pink and ribbon
    'c_gsk2' : [ 11, [ 27, ]],
    
    # teal skirt with yellow and star
    'c_gsk3' : [ 12, [ 27, ]],

    # Valentines skirt (note, do not name with gsk, otherwise NPC might randomly get this skirt)
    # red skirt with hearts
    'vd_gs1' : [ 13, [ 27, ]],
    # Pink flair skirt with polka hearts
    'vd_gs2' : [ 27, [ 27, ]],
    # Blue denim skirt with green and red heart
    'vd_gs3' : [ 28, [ 27, ]],

    # rainbow skirt - Series 3
    'c_gsk4' : [ 14, [ 27, ]],

    # St. Pats day shorts
    'sd_gs1' : [ 15, [ 27, ]],

    # Western skirts
    'c_gsk5' : [ 16, [ 27, ]],
    'c_gsk6' : [ 17, [ 27, ]],

    # Western shorts
    'c_bs3' : [ 12, [ 27, ]],
    'c_bs4' : [ 13, [ 27, ]],

    # July 4th shorts
    'j4_bs1' : [ 14, [ 27, ]],
    
    # July 4th Skirt
    'j4_gs1' : [ 18, [ 27, ]],    

    # Blue with flower - series 7
    'c_gsk7' : [ 19, [ 27, ]], 
    
    # pajama shorts
    'pj_gs1' : [ 20, [27, ]], # Blue Banana Pajama pants
    'pj_gs2' : [ 21, [27, ]], # Red Horn Pajama pants
    'pj_gs3' : [ 22, [27, ]], # Purple Glasses Pajama pants
    
    # Winter Holiday Skirts
    'wh_gsk1' : [ 23, [27, ]], # Winter Holiday Skirt Style 1
    'wh_gsk2' : [ 24, [27, ]], # Winter Holiday Skirt Style 2
    'wh_gsk3' : [ 25, [27, ]], # Winter Holiday Skirt Style 3
    'wh_gsk4' : [ 26, [27, ]], # Winter Holiday Skirt Style 4
    
    # Special award clothes
    'sa_bs1' : [25, [27, ]],
    'sa_bs2' : [26, [27, ]],
    'sa_bs3' : [27, [27, ]],
    'sa_bs4' : [28, [27, ]],
    'sa_bs5' : [29, [27, ]],
    'sa_bs6' : [30, [27, ]],
    'sa_bs7' : [31, [27, ]],
    'sa_bs8' : [32, [27, ]],
    'sa_bs9' : [33, [27, ]],
    'sa_bs10' : [34, [27, ]],    
    'sa_bs11' : [35, [27, ]],
    'sa_bs12' : [36, [27, ]],
    
    # Special award clothes
    'sa_gs1' : [29, [27, ]],
    'sa_gs2' : [30, [27, ]],
    'sa_gs3' : [31, [27, ]],
    'sa_gs4' : [32, [27, ]],
    'sa_gs5' : [33, [27, ]],
    'sa_gs6' : [34, [27, ]],
    'sa_gs7' : [35, [27, ]],
    'sa_gs8' : [36, [27, ]],
    'sa_gs9' : [37, [27, ]],
    'sa_gs10' : [38, [27, ]],
    'sa_gs11' : [39, [27, ]],
    'sa_gs12' : [40, [27, ]],
    
    # Scientists
    'sc_bs1' : [37, [27, ]],
    'sc_bs2' : [38, [27, ]],
    'sc_bs3' : [39, [27, ]],
    
    'sc_gs1' : [41, [27, ]],
    'sc_gs2' : [42, [27, ]],
    'sc_gs3' : [43, [27, ]],
    
    'sil_bs1' : [ 40, [27, ]], # Silly Cogbuster Shorts
    'sil_gs1' : [44, [27, ]], # Silly Cogbuster Shorts
    }

# Define MakeAToon to be Tailor 1
MAKE_A_TOON = 1
TAMMY_TAILOR = 2004 # TTC
LONGJOHN_LEROY = 1007 # DD
TAILOR_HARMONY = 4008 # MM
BONNIE_BLOSSOM = 5007 # DG
WARREN_BUNDLES = 3008 # TB
WORNOUT_WAYLON = 9010 # DDR

TailorCollections = {
    # TailorId : [ [ boyShirts ], [ girlShirts ], [boyShorts], [girlBottoms] ]
    MAKE_A_TOON : [ ['bss1', 'bss2'],
                    ['gss1', 'gss2'],
                    ['bbs1', 'bbs2'],
                    ['gsk1', 'gsh1'] ],
    TAMMY_TAILOR : [ ['bss1', 'bss2'],
                     ['gss1', 'gss2'],
                     ['bbs1', 'bbs2'],
                     ['gsk1', 'gsh1'] ],
    LONGJOHN_LEROY : [ ['bss3', 'bss4', 'bss14'], ['gss3', 'gss4', 'gss14'], ['bbs3', 'bbs4'], ['gsk2', 'gsh2'] ],
    TAILOR_HARMONY : [ ['bss5', 'bss6', 'bss10'], ['gss5', 'gss6', 'gss9'], ['bbs5'], ['gsk3', 'gsh3'] ],
    BONNIE_BLOSSOM : [ ['bss7', 'bss8', 'bss12'], ['gss8', 'gss10', 'gss12'], ['bbs6'], ['gsk4', 'gsk5'] ],
    WARREN_BUNDLES : [ ['bss9','bss13'], ['gss7', 'gss11'], ['bbs7'], ['gsk6'] ],
    WORNOUT_WAYLON : [ ['bss11', 'bss15'], ['gss13', 'gss15'], ['bbs8'], ['gsk7'] ],
    }

BOY_SHIRTS = 0
GIRL_SHIRTS = 1
BOY_SHORTS = 2
GIRL_BOTTOMS = 3


# Make a list of the girl bottoms in MakeAToon
# This is used in the body shop when switching genders
MakeAToonBoyBottoms = []
MakeAToonBoyShirts = []
MakeAToonGirlBottoms = []
MakeAToonGirlShirts = []
MakeAToonGirlSkirts = []
MakeAToonGirlShorts = []

for style in TailorCollections[MAKE_A_TOON][BOY_SHORTS]:
    index = BottomStyles[style][0]
    MakeAToonBoyBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][BOY_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonBoyShirts.append(index)

for style in TailorCollections[MAKE_A_TOON][GIRL_BOTTOMS]:
    index = BottomStyles[style][0]
    MakeAToonGirlBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][GIRL_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonGirlShirts.append(index)

# Separate out the skirts and shorts
for index in MakeAToonGirlBottoms:
    flag = GirlBottoms[index][1]
    if flag == SKIRT:
        MakeAToonGirlSkirts.append(index)
    elif flag == SHORTS:
        MakeAToonGirlShorts.append(index)
    else:
        notify.error("Invalid flag")


# Convenience funtions for clothing
def getRandomTop(gender, tailorId = MAKE_A_TOON, generator = None):
    # Returns (shirtTex, color, sleeveTex, color)
    if (generator == None):
        generator = random 
    collection = TailorCollections[tailorId]
    if (gender == 'm'):
        style = generator.choice(collection[BOY_SHIRTS])
    else:
        style = generator.choice(collection[GIRL_SHIRTS])
    styleList = ShirtStyles[style]
    colors = generator.choice(styleList[2])
    return styleList[0], colors[0], styleList[1], colors[1]

def getRandomBottom(gender, tailorId = MAKE_A_TOON, generator = None, girlBottomType = None):
    # Returns (bottomTex, color)
    if (generator == None):
        generator = random
    collection = TailorCollections[tailorId]
    if (gender == 'm'):
        style = generator.choice(collection[BOY_SHORTS])
    else:
        if (girlBottomType is None):
            style = generator.choice(collection[GIRL_BOTTOMS])
        elif (girlBottomType == SKIRT):
            skirtCollection = filter(lambda style: GirlBottoms[BottomStyles[style][0]][1] == SKIRT,
                                     collection[GIRL_BOTTOMS])
            style = generator.choice(skirtCollection)
        elif (girlBottomType == SHORTS):
            shortsCollection = filter(lambda style: GirlBottoms[BottomStyles[style][0]][1] == SHORTS,
                                      collection[GIRL_BOTTOMS])
            style = generator.choice(shortsCollection)
        else:
            notify.error("Bad girlBottomType: %s" % girlBottomType)
            
    styleList = BottomStyles[style]
    color = generator.choice(styleList[1])
    return styleList[0], color

def getRandomGirlBottom(type):
    bottoms = []
    index = 0
    for bottom in GirlBottoms:
        if (bottom[1] == type):
            bottoms.append(index)
        index += 1
    return random.choice(bottoms)

def getRandomGirlBottomAndColor(type):
    bottoms = []
    if type == SHORTS:
        typeStr = 'gsh'
    else:
        typeStr = 'gsk'
    for bottom in BottomStyles.keys():
        if bottom.find(typeStr) >= 0:
            bottoms.append(bottom)
    style = BottomStyles[random.choice(bottoms)]
    return style[0], random.choice(style[1])

def getRandomizedTops(gender, tailorId = MAKE_A_TOON, generator = None):
    # Returns a list of [ (shirt, color, sleeve, color), ... ]
    if (generator == None):
        generator = random
    collection = TailorCollections[tailorId]
    if (gender == 'm'):
        collection = collection[BOY_SHIRTS][:]
    else:
        collection = collection[GIRL_SHIRTS][:]
    tops = []
    random.shuffle(collection)
    for style in collection:
        colors = ShirtStyles[style][2][:]
        random.shuffle(colors)
        for color in colors:
            tops.append((ShirtStyles[style][0], color[0], 
                         ShirtStyles[style][1], color[1]))
    return tops

def getRandomizedBottoms(gender, tailorId = MAKE_A_TOON, generator = None):
    # Returns a list of [ (bottom, color), ... ]
    if (generator == None):
        generator = random
    collection = TailorCollections[tailorId]
    if (gender == 'm'):
        collection = collection[BOY_SHORTS][:]
    else:
        collection = collection[GIRL_BOTTOMS][:]
    bottoms = []
    random.shuffle(collection)
    for style in collection:
        colors = BottomStyles[style][1][:]
        random.shuffle(colors)
        for color in colors:
            bottoms.append((BottomStyles[style][0], color))
    return bottoms    

def getTops(gender, tailorId = MAKE_A_TOON):
    # Returns a list of [ (shirt, color, sleeve, color), ... ]
    if (gender == 'm'):
        collection = TailorCollections[tailorId][BOY_SHIRTS]
    else:
        collection = TailorCollections[tailorId][GIRL_SHIRTS]
    tops = []
    for style in collection:
        for color in ShirtStyles[style][2]:
            tops.append((ShirtStyles[style][0], color[0],
                         ShirtStyles[style][1], color[1]))
    return tops

def getAllTops(gender):
    tops = []
    for style in ShirtStyles.keys():
        if gender == 'm':
            if (style[0] == 'g') or (style[:3] == 'c_g'):
                continue
        else:
            if (style[0] == 'b') or (style[:3] == 'c_b'):
                continue
        for color in ShirtStyles[style][2]:
            tops.append((ShirtStyles[style][0], color[0],
                         ShirtStyles[style][1], color[1]))
    return tops

def getBottoms(gender, tailorId = MAKE_A_TOON):
    # Returns a list of [ (bottom, color), ... ]
    if (gender == 'm'):
        collection = TailorCollections[tailorId][BOY_SHORTS]
    else:
        collection = TailorCollections[tailorId][GIRL_BOTTOMS]
    bottoms = []
    for style in collection:
        for color in BottomStyles[style][1]:
            bottoms.append((BottomStyles[style][0], color))
    return bottoms

def getAllBottoms(gender, output = 'both'):
    bottoms = []
    for style in BottomStyles.keys():
        if gender == 'm':
            if ((style[0] == 'g') or (style[:3] == 'c_g') or
                (style[:4] == 'vd_g') or (style[:4] == 'sd_g') or
                (style[:4] == 'j4_g') or (style[:4] == 'pj_g') or
                (style[:4] == 'wh_g') or (style[:4] == 'sa_g') or
                (style[:4] == 'sc_g') or (style[:5] == 'sil_g')) :

                continue
        else:
            if ((style[0] == 'b') or (style[:3] == 'c_b') or
                (style[:4] == 'vd_b') or (style[:4] == 'sd_b') or
                (style[:4] == 'j4_b') or (style[:4] == 'pj_b') or
                (style[:4] == 'wh_b') or (style[:4] == 'sa_b') or
                (style[:4] == 'sc_b') or (style[:5] == 'sil_b')):
                continue
        
        bottomIdx = BottomStyles[style][0]
        # What type of texture is at this index?
        if gender == 'f':
            # Female textures can be shorts or skirts
            textureType = GirlBottoms[bottomIdx][1]
        else:
            # All male textures are shorts
            textureType = SHORTS
        if ((output == 'both') or
            ((output == 'skirts') and (textureType == SKIRT)) or
            ((output == 'shorts') and (textureType == SHORTS))):
            for color in BottomStyles[style][1]:
                bottoms.append((bottomIdx, color))
    return bottoms

# color defines

# Warning!  DNA values are stored in the server database by indexing
# into this array.  Do not reorder entries in this array, or add
# things to the middle, or all toons already stored in the database
# will get screwed up.

# This is the total list of all available colors a part of the toon
# might possibly be set to.  It's not the same thing as the list of
# color choices presented by make-a-toon, but it's close.

# len = 27
allColorsList = [
    VBase4(1.0, 1.0, 1.0, 1.0),                 # 0
    VBase4(0.96875, 0.691406, 0.699219, 1.0),   # 1
    VBase4(0.933594, 0.265625, 0.28125, 1.0),   # 2
    VBase4(0.863281, 0.40625, 0.417969, 1.0),   # 3
    VBase4(0.710938, 0.234375, 0.4375, 1.0),    # 4
    VBase4(0.570312, 0.449219, 0.164062, 1.0),  # 5
    VBase4(0.640625, 0.355469, 0.269531, 1.0),  # 6
    VBase4(0.996094, 0.695312, 0.511719, 1.0),  # 7
    VBase4(0.832031, 0.5, 0.296875, 1.0),       # 8
    VBase4(0.992188, 0.480469, 0.167969, 1.0),  # 9
    VBase4(0.996094, 0.898438, 0.320312, 1.0),  # 10
    VBase4(0.996094, 0.957031, 0.597656, 1.0),  # 11
    VBase4(0.855469, 0.933594, 0.492188, 1.0),  # 12
    VBase4(0.550781, 0.824219, 0.324219, 1.0),  # 13
    VBase4(0.242188, 0.742188, 0.515625, 1.0),  # 14
    VBase4(0.304688, 0.96875, 0.402344, 1.0),   # 15
    VBase4(0.433594, 0.90625, 0.835938, 1.0),   # 16
    VBase4(0.347656, 0.820312, 0.953125, 1.0),  # 17
    VBase4(0.191406, 0.5625, 0.773438, 1.0),    # 18
    VBase4(0.558594, 0.589844, 0.875, 1.0),     # 19
    VBase4(0.285156, 0.328125, 0.726562, 1.0),  # 20
    VBase4(0.460938, 0.378906, 0.824219, 1.0),  # 21
    VBase4(0.546875, 0.28125, 0.75, 1.0),       # 22
    VBase4(0.726562, 0.472656, 0.859375, 1.0),  # 23
    VBase4(0.898438, 0.617188, 0.90625, 1.0),   # 24
    VBase4(0.7, 0.7, 0.8, 1.0),                 # 25
    VBase4(0.3, 0.3, 0.35, 1.0), # black-ish cat# 26
    ]

# *This* is the list of color choices presented by make-a-toon.  It
# indexes into the above array.
defaultBoyColorList = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    ]
defaultGirlColorList = [
    1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24
    ]

class ToonDNA(AvatarDNA.AvatarDNA):
    """ToonDNA class: contains methods for describing avatars with a
    simple class. The ToonDNA class may be converted to lists of strings
    for network transmission. Also, ToonDNA objects can be constructed
    from lists of strings recieved over the network. Some examples are in
    order.

        # create a random toon dna
        dna = AvatarDNA()
        dna.newToonRandom()

        # create a random toon but specify its color
        dna = AvatarDNA()
        dna.newToonRandom(0.7, 0.6, 0.5)

        # create a specific toon by passing in a tuple of body
        # part specifier strings (see 'toon defines' above)
        dna = AvatarDNA()
        dna.newToon( ('dll', 'md', 'l', 'm') )
        # 'l'ong legs, 'm'edium 'd'ress, 'd'og w/ 'l'ong head and 'l'ong muzzle, and 'm'ale

        # create a toon with a part tuple and a color
        dna = AvatarDNA()
        dna.newToon( ('css', 'ss', 's', 'm'), 0.4, 0.2, 0.2 ) )

        # create a toon from a network packet (list of strings)
        dna = AvatarDNA()
        dna.makeFromNetString( networkPacket )

    """
    # special methods
    
    def __init__(self, str=None, type=None, dna=None, r=None, b=None, g=None):
        """__init__(self, string=None, string=None, string()=None, float=None,
        float=None, float=None)
        AvatarDNA contructor - see class comment for usage
        """
        # have they passed in a stringified DNA object?
        if (str != None):
            self.makeFromNetString(str)
        # have they specified what type of DNA?
        elif (type != None):
            if (type == 't'):  # Toon
                if (dna == None):
                    self.newToonRandom(r, g, b)
                else:
                    self.newToonFromProperties(*dna.asTuple())
            else:
                # Invalid type
                assert 0
        else:
            # mark DNA as undefined
            self.type = 'u'

    def __str__(self):
        """__str__(self)
        Avatar DNA print method
        """
        string = "type = toon\n"
        string = string + "gender = %s\n" % (self.gender)
        string = string + "head = %s, torso = %s, legs = %s\n" % \
                  (self.head, self.torso, self.legs)
        string = string + "arm color = %d\n" % \
                 (self.armColor)
        string = string + "glove color = %d\n" % \
                 (self.gloveColor)
        string = string + "leg color = %d\n" % \
                 (self.legColor)
        string = string + "head color = %d\n" % \
                 (self.headColor)
        string = string + "top texture = %d\n" % self.topTex
        string = string + "top texture color = %d\n" % self.topTexColor
        string = string + "sleeve texture = %d\n" % self.sleeveTex
        string = string + "sleeve texture color = %d\n" % self.sleeveTexColor
        string = string + "bottom texture = %d\n" % self.botTex
        string = string + "bottom texture color = %d\n" % self.botTexColor
        return string


    # stringification methods
    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if (self.type == 't'):  # Toon
            # These strings had better appear in the lists!
            headIndex = toonHeadTypes.index(self.head)
            torsoIndex = toonTorsoTypes.index(self.torso)
            legsIndex = toonLegTypes.index(self.legs)
            dg.addUint8(headIndex)
            dg.addUint8(torsoIndex)
            dg.addUint8(legsIndex)
            if self.gender == 'm':
                # male is 1
                dg.addUint8(1)
            else:
                # female is 0
                dg.addUint8(0)
            # Clothes
            dg.addUint8(self.topTex) # We assume < 256 textures.
            dg.addUint8(self.topTexColor)
            dg.addUint8(self.sleeveTex)
            dg.addUint8(self.sleeveTexColor)
            dg.addUint8(self.botTex)
            dg.addUint8(self.botTexColor)
            # Colors
            dg.addUint8(self.armColor) # We assume < 256 colors.
            dg.addUint8(self.gloveColor)
            dg.addUint8(self.legColor)
            dg.addUint8(self.headColor)
        elif (self.type == 'u'):
            notify.error("undefined avatar")
        else:
            notify.error("unknown avatar type: ", self.type)

        return dg.getMessage()

    def isValidNetString(self, string):
        dg=PyDatagram(string)
        dgi=PyDatagramIterator(dg)
        if dgi.getRemainingSize() != 15:
            return False
        type = dgi.getFixedString(1)
        if type not in ('t', ):
            return False

        headIndex = dgi.getUint8()
        torsoIndex = dgi.getUint8()
        legsIndex = dgi.getUint8()

        if headIndex >= len(toonHeadTypes):
            return False
        if torsoIndex >= len(toonTorsoTypes):
            return False
        if legsIndex >= len(toonLegTypes):
            return False

        gender = dgi.getUint8()
        if gender == 1:
            gender = 'm'
        else:
            gender = 'f'

        topTex = dgi.getUint8()
        topTexColor = dgi.getUint8()
        sleeveTex = dgi.getUint8()
        sleeveTexColor = dgi.getUint8()
        botTex = dgi.getUint8()
        botTexColor = dgi.getUint8()
        armColor = dgi.getUint8()
        gloveColor = dgi.getUint8()
        legColor = dgi.getUint8()
        headColor = dgi.getUint8()

        if topTex >= len(Shirts):
            return False
        if topTexColor >= len(ClothesColors):
            return False
        if sleeveTex >= len(Sleeves):
            return False
        if sleeveTexColor >= len(ClothesColors):
            return False
        if botTex >= choice(gender == 'm', len(BoyShorts), len(GirlBottoms)):
            return False
        if botTexColor >= len(ClothesColors):
            return False
        if armColor >= len(allColorsList):
            return False
        if gloveColor >= len(allColorsList):
            return False
        if legColor >= len(allColorsList):
            return False
        if headColor >= len(allColorsList):
            return False

        return True

    def makeFromNetString(self, string):
        dg=PyDatagram(string)
        dgi=PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if (self.type == 't'):  # Toon
            headIndex = dgi.getUint8()
            torsoIndex = dgi.getUint8()
            legsIndex = dgi.getUint8()
            self.head = toonHeadTypes[headIndex]
            self.torso = toonTorsoTypes[torsoIndex]
            self.legs = toonLegTypes[legsIndex]
            gender = dgi.getUint8()
            if gender == 1:
                self.gender = 'm'
            else:
                self.gender = 'f'
            self.topTex = dgi.getUint8()
            self.topTexColor = dgi.getUint8()
            self.sleeveTex = dgi.getUint8()
            self.sleeveTexColor = dgi.getUint8()
            self.botTex = dgi.getUint8()
            self.botTexColor = dgi.getUint8()
            self.armColor = dgi.getUint8()
            self.gloveColor = dgi.getUint8()
            self.legColor = dgi.getUint8()
            self.headColor = dgi.getUint8()
        else:
            notify.error("unknown avatar type: ", self.type)

        return None
    
    # dna methods
    def defaultColor(self):
        return 25
    
    def __defaultColors(self):
        """__defaultColors(self)
        Set everything to white by default
        """
        color = self.defaultColor()
        self.armColor = color
        # gloves are always white
        self.gloveColor = 0
        self.legColor = color
        self.headColor = color

    def newToon(self, dna, color = None):
        """newToon(self, string(), float=None, float=None, float=None)
        Return the dna for the toon described in the given tuple.
        If color is specified use for all parts. Otherwise, use the
        default color. Use default clothes textures.
        """
        if ( len(dna) == 4):
            self.type = "t"
            self.head = dna[0]
            self.torso = dna[1]
            self.legs = dna[2]
            self.gender = dna[3]
            self.topTex = 0
            self.topTexColor = 0
            self.sleeveTex = 0
            self.sleeveTexColor = 0
            self.botTex = 0
            self.botTexColor = 0

            if (color == None):
                color = self.defaultColor()
                
            self.armColor = color
            self.legColor = color
            self.headColor = color

            # gloves always white
            self.gloveColor = 0
        else:
            notify.error("tuple must be in format ('%s', '%s', '%s', '%s')")

    def newToonFromProperties(self, head, torso, legs, gender,
                              armColor, gloveColor, legColor, headColor,
                              topTexture, topTextureColor, sleeveTexture,
                              sleeveTextureColor, bottomTexture,
                              bottomTextureColor):
        """
        Fill in Toon dna using known parameters for all values. Example:
        dna.newToonFromProperties('dll', 'md', 'l', 'm', 1, 0, 23, 3, 22, 22, 30)
        """
        self.type = 't'
        self.head = head
        self.torso = torso
        self.legs = legs
        self.gender = gender
        self.armColor = armColor
        self.gloveColor = gloveColor
        self.legColor = legColor
        self.headColor = headColor
        self.topTex = topTexture
        self.topTexColor = topTextureColor
        self.sleeveTex = sleeveTexture
        self.sleeveTexColor = sleeveTextureColor
        self.botTex = bottomTexture
        self.botTexColor = bottomTextureColor 
        return

    def updateToonProperties(self, head = None, torso = None, legs = None,
                             gender = None, armColor = None, gloveColor = None,
                             legColor = None, headColor = None,
                             topTexture = None, topTextureColor = None,
                             sleeveTexture = None,
                             sleeveTextureColor = None, bottomTexture = None,
                             bottomTextureColor = None,
                             shirt = None, bottom = None):

        # Changes only the named properties.  'shirt' and 'bottom' are
        # special properties that specify an article of clothing with
        # a 2-tuple, the string and color index, e.g.: ('bss1', 1)
        
        assert self.type == 't'
        if head:
            self.head = head
        if torso:
            self.torso = torso
        if legs:
            self.legs = legs
        if gender:
            self.gender = gender
        if armColor:
            self.armColor = armColor
        if gloveColor:
            self.gloveColor = gloveColor
        if legColor:
            self.legColor = legColor
        if headColor:
            self.headColor = headColor
        if topTexture:
            self.topTex = topTexture
        if topTextureColor:
            self.topTexColor = topTextureColor
        if sleeveTexture:
            self.sleeveTex = sleeveTexture
        if sleeveTextureColor:
            self.sleeveTexColor = sleeveTextureColor
        if bottomTexture:
        # string (see 'c
            self.botTex = bottomTexture
        if bottomTextureColor:
            self.botTexColor = bottomTextureColor
        if shirt:
            str, colorIndex = shirt
            defn = ShirtStyles[str]
            self.topTex = defn[0]
            self.topTexColor = defn[2][colorIndex][0]
            self.sleeveTex = defn[1]
            self.sleeveTexColor = defn[2][colorIndex][1]
        if bottom:
            str, colorIndex = bottom
            defn = BottomStyles[str]
            self.botTex = defn[0]
            self.botTexColor = defn[1][colorIndex]
            
        return

    def newToonRandom(self, seed = None, gender = "m", npc = 0, stage = None):
        """newToonRandom(self, float=None, float=None, float=None)
        Return the dna tuple for a random toon.  Use random
        colors and random clothes textures.
        """
        if seed:
            generator = random.Random()
            generator.seed(seed)
        else:
            # Just use the normal one
            generator = random
        
        self.type = "t" # Toon.
        # Skew the leg length toward medium and long:
        self.legs = generator.choice(toonLegTypes + ["m", "l", "l", "l"])
        self.gender = gender

        # We have added the monkey species. It would be weird for existing NPCs
        # to change into monkeys so don't use those heads for NPCs.
        if not npc:
            if (stage == MAKE_A_TOON):
                if not base.cr.isPaid():
                    animalIndicesToUse = allToonHeadAnimalIndicesTrial
                else:
                    animalIndicesToUse = allToonHeadAnimalIndices
                animal = generator.choice(animalIndicesToUse)
                self.head = toonHeadTypes[animal]
            else:
                self.head = generator.choice(toonHeadTypes)
        else:
            self.head = generator.choice(toonHeadTypes[:22])
        top, topColor, sleeve, sleeveColor = getRandomTop(gender, generator = generator)
        bottom, bottomColor = getRandomBottom(gender, generator = generator)
        if gender == "m":
            self.torso = generator.choice(toonTorsoTypes[:3])
            # Choose a random boy shirt style from MakeAToon
            self.topTex = top
            self.topTexColor = topColor 
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            self.botTex = bottom 
            self.botTexColor = bottomColor
            color = generator.choice(defaultBoyColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color
        else:
            self.torso = generator.choice(toonTorsoTypes[:6])
            self.topTex = top
            self.topTexColor = topColor
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            
##            # Make sure the bottom type matches the torso type
##            if (self.torso[1] == 'd'):
##                tex, color = getRandomGirlBottomAndColor(SKIRT)
##                self.botTex = tex
##                self.botTexColor = color
##            else:
##                tex, color = getRandomGirlBottomAndColor(SKIRT) 
##                self.botTex = tex
##                self.botTexColor = color
                
            # Make sure the bottom type matches the torso type
            if (self.torso[1] == 'd'):
                bottom, bottomColor = getRandomBottom(gender, generator = generator, girlBottomType = SKIRT)
            else:
                bottom, bottomColor = getRandomBottom(gender, generator = generator, girlBottomType = SHORTS)
            self.botTex = bottom 
            self.botTexColor = bottomColor
            color = generator.choice(defaultGirlColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color

        # gloves always white
        self.gloveColor = 0

    def asTuple(self):
        return (self.head, self.torso, self.legs, self.gender,
                self.armColor, self.gloveColor, self.legColor, self.headColor,
                self.topTex, self.topTexColor, self.sleeveTex, 
                self.sleeveTexColor, self.botTex, self.botTexColor)

    def getType(self):
        """getType(self)
        Return which type of actor this dna represents.
        """
        if (self.type == 't'):
            #toon type
            type = self.getAnimal()
        else:
            notify.error("Invalid DNA type: ", self.type)

        return type

    # toon helper funcs
    def getAnimal(self):
        """getAnimal(self)
        Return animal name corresponding to head type as string
        """
        if (self.head[0] == 'd'):
            return("dog")
        elif (self.head[0] == 'c'):
            return("cat")
        elif (self.head[0] == 'm'):
            return("mouse")
        elif (self.head[0] == 'h'):
            return("horse")
        elif (self.head[0] == 'r'):
            return("rabbit")
        elif (self.head[0] == 'f'):
            return("duck")
        elif (self.head[0] == 'p'):
            return("monkey")
        elif (self.head[0] == 'b'):
            return("bear")
        elif (self.head[0] == 's'):
            return("pig")
        else:
            notify.error("unknown headStyle: ", self.head[0])

    def getHeadSize(self):
        """getHeadSize(self)
        Return head size corresponding to head type as string
        """
        if (self.head[1] == 'l'):
            return("long")
        elif (self.head[1] == 's'):
            return("short")
        else:
            notify.error("unknown head size: ", self.head[1])

    def getMuzzleSize(self):
        """getMuzzleSize(self)
        Return muzzle size corresponding to head type as string
        """
        if (self.head[2] == 'l'):
            return("long")
        elif (self.head[2] == 's'):
            return("short")
        else:
            notify.error("unknown muzzle size: ", self.head[2])

    def getTorsoSize(self):
        """getTorsoSize(self)
        Return the size of the torso as a string
        """
        if (self.torso[0] == 'l'):
            return("long")
        elif (self.torso[0] == 'm'):
            return("medium")
        elif (self.torso[0] == 's'):
            return("short")
        else:
            notify.error("unknown torso size: ", self.torso[0])

    def getLegSize(self):
        """getLegSize(self)
        Return the size of the legs as a string
        """
        if (self.legs == 'l'):
            return("long")
        elif (self.legs == 'm'):
            return("medium")
        elif (self.legs == 's'):
            return("short")
        else:
            notify.error("unknown leg size: ", self.legs)

    def getGender(self):
        return self.gender

    def getClothes(self):
        """getClothes(self)
        Return the type of clothing as a string
        """
        if (len(self.torso) == 1):
            return("naked")            
        elif (self.torso[1] == 's'):
            return("shorts")
        elif (self.torso[1] == 'd'):
            return("dress")
        else:
            notify.error("unknown clothing type: ", self.torso[1])

    def getArmColor(self):
        try:
            return allColorsList[self.armColor]
        except:
            return allColorsList[0]

    def getLegColor(self):
        try:
            return allColorsList[self.legColor]
        except:
            return allColorsList[0]

    def getHeadColor(self):
        try:
            return allColorsList[self.headColor]
        except:
            return allColorsList[0]

    def getGloveColor(self):
        try:
            return allColorsList[self.gloveColor]
        except:
            return allColorsList[0]

    def getBlackColor(self):
        try:
            return allColorsList[26]
        except:
            return allColorsList[0]



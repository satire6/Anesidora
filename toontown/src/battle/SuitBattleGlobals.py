from BattleBase import *

import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer

notify = DirectNotifyGlobal.directNotify.newCategory('SuitBattleGlobals')

"""
CorporateTrack = ['Flunky', 
                  'PencilPusher',
                  'YesMan',
                  'MicroManager',
                  'DownSizer',
                  'HeadHunter',
                  'CorporateRaider',
                  'BigCheese'] 
LegalTrack = ['BottomFeeder',
              'BloodSucker',
              'DoubleTalker',
              'AmbulanceChaser',
              'BackStabber',
              'SpinDoctor',
              'LegalEagle',
              'BigWig']
MoneyTrack = ['ShortChange',
              'PennyPincher',
              'TightWad',
              'BeanCounter',
              'NumberCruncher',
              'MoneyBags',
              'LoanShark',
              'RobberBaron']
SalesTrack = ['ColdCaller',
              'TeleMarketer',
              'NameDropper',
              'GladHander',
              'Mover&Shaker',
              'TwoFaced',
              'TheMingler',
              'MrHollywood'] 
"""

debugAttackSequence = {}

def pickFromFreqList(freqList):
    """
    Function:    randomly choose an entry from the specified list
                 of probability values which should all add up to
                 be 100
    Parameters:  list, list of probability values to choose from
    Returns:     index into 'list' for the element chosen
    """
    randNum = random.randint(0, 99)
    count = 0
    index = 0
    level = None
    for f in freqList:
        count = count + f
        if (randNum < count):
            level = index
            break
        index = index + 1
    #assert (level != None), "Element not found"
    return level

def getActualFromRelativeLevel(name, relLevel):
    """
    convert from a relative level (0-4) into the suit's
    actual level (0-11), returns a 2 item list, the first
    element being the actual level, the second being the
    relative level given (adjusted if necessary)
    """
    data = SuitAttributes[name]
    # Levels range 0-4, 1-5, 2-6, ..., 6-10, 11

    # I don't know why there was code here to special-case the
    # top-level guys to only appear to be level 12--but we don't want
    # that behavior.
    #if (name == 'tbc' or name == 'bw' or name == 'mh' or name == 'rb'):
    #    actualLevel = 11
    #else:
    #    actualLevel = data['level'] + relLevel

    actualLevel = data['level'] + relLevel
    return actualLevel

def getSuitVitals(name, level=-1):
    data = SuitAttributes[name]
    # If level isn't specified, choose one based on the frequency values
    if (level == -1):
        level = pickFromFreqList(data['freq'])
    dict = {}
    dict['level'] = getActualFromRelativeLevel(name, level)
    if dict['level'] == 11:
        level = 0
    dict['hp'] = data['hp'][level]
    dict['def'] = data['def'][level]
    attacks = data['attacks']
    alist = []
    for a in attacks:
        adict = {}
        name = a[0]
        adict['name'] = name
        adict['animName'] = SuitAttacks[name][0]
        adict['hp'] = a[1][level]
        adict['acc'] = a[2][level]
        adict['freq'] = a[3][level]
        adict['group'] = SuitAttacks[name][1]
        alist.append(adict)
    dict['attacks'] = alist
    return dict

def pickSuitAttack(attacks, suitLevel):
    """
    Function:    randomly choose an attack from a list of possible
                 ones based on each attack's frequency value
    Parameters:  attacks, list of attacks to choose from
                 suitLevel, the level of the suit we are picking the
                   attack for
    Returns:     index into the attacks list for the attack chosen
    """
    attackNum = None
    randNum = random.randint(0, 99)
    notify.debug('pickSuitAttack: rolled %d' % randNum)
    count = 0
    index = 0

    total = 0
    for c in attacks:
        total = total + c[3][suitLevel]
    assert (total == 100)
    
    for c in attacks:
        count = count + c[3][suitLevel]
        if (randNum < count):
            attackNum = index
            notify.debug('picking attack %d' % attackNum)
            break
        index = index + 1
    assert (attackNum != None), "No attack found"

#    configAttackNum = simbase.config.GetString('attack-type', 'random')
#    if configAttackNum == 'random':
#        return attackNum
#    else:
#        return configAttackNum

    configAttackName = simbase.config.GetString('attack-type', 'random')
    if configAttackName == 'random':
        # Normally, attackNum is returned
        return attackNum
    elif configAttackName == 'sequence':
        # Return each different attack only once globally, then random.
        # A special debugging mode.
        for i in range(len(attacks)):
            if not debugAttackSequence.has_key(attacks[i]):
                debugAttackSequence[attacks[i]] = 1
                return i
        return attackNum
    else:
        # However, if attack-type was specified in the configfile, look
        # it up, and return the index if it is found.
        for i in range(len(attacks)):
            if attacks[i][0] == configAttackName:
                return i

        # If it is not found, this suit can't make that kind of
        # attack, so choose a random attack.
        return attackNum

def getSuitAttack(suitName, suitLevel, attackNum=-1):
    # If no attack is specified, choose one based on frequency values
    attackChoices = SuitAttributes[suitName]['attacks']
    if (attackNum == -1):
        notify.debug('getSuitAttack: picking attacking for %s' % suitName)
        attackNum = pickSuitAttack(attackChoices, suitLevel)

    attack = attackChoices[attackNum]
    adict = {}
    adict['suitName'] = suitName
    name = attack[0]
    adict['name'] = name
    adict['id'] = SuitAttacks.keys().index(name)
    adict['animName'] = SuitAttacks[name][0]
    adict['hp'] = attack[1][suitLevel]
    adict['acc'] = attack[2][suitLevel]
    adict['freq'] = attack[3][suitLevel]
    adict['group'] = SuitAttacks[name][1]
    return adict





SuitAttributes = {
    #### Corporate ####
    #   Flunky (C)
    'f':  { 'name': TTLocalizer.SuitFlunky,
            'singularname': TTLocalizer.SuitFlunkyS,
            'pluralname': TTLocalizer.SuitFlunkyP,
            'level': 0,
            'hp': (6, 12, 20, 30, 42),  # actual suit level * 4
            'def': (2, 5, 10, 12, 15),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('PoundKey',     (2, 2, 3, 4, 6),        # dmg
                                         (75, 75, 80, 80, 90),   # acc 
                                         (30, 35, 40, 45, 50)),  # freq
                                         # cringe & sidestep
                        ('Shred',        (3, 4, 5, 6, 7),
                                         (50, 55, 60, 65, 70),
                                         (10, 15, 20, 25, 30)),
                                         # conked & sidestep
                        ('ClipOnTie',    (1, 1, 2, 2, 3),
                                         (75, 80, 85, 90, 95), 
                                         (60, 50, 40, 30, 20)),
                                         # conked & sidestep
                        # TODO: Carbon copy - not implemented
                        #('CarbonCopy',   (0, 0, 0, 0, 0),
                        #                 (75, 75, 75, 75, 75), 
                        #                 (0, 0, 0, 0, 0))
                        )
            },
    
    #   Pencil Pusher (B)
    'p':  { 'name': TTLocalizer.SuitPencilPusher,
            'singularname': TTLocalizer.SuitPencilPusherS,
            'pluralname': TTLocalizer.SuitPencilPusherP,
            'level': 1,
            'hp': (12, 20, 30, 42, 56),  # actual suit level * 4
            'def': (5, 10, 15, 20, 25),
            'freq': (50, 30, 10, 5, 5),
            'acc': (45, 50, 55, 60, 65),
            'attacks': (('FountainPen',  (2, 3, 4, 6, 9),        # dmg
                                         (75, 75, 75, 75, 75),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # flatten, sidestep-left/right
                        ('RubOut',       (4, 5, 6, 8, 12),
                                         (75, 75, 75, 75, 75), 
                                         (20, 20, 20, 20, 20)),
                                         # conked&slip-backward, sidestep-l/r
                        ('FingerWag',    (1, 2, 2, 3, 4),
                                         (75, 75, 75, 75, 75), 
                                         (35, 30, 25, 20, 15)), 
                                         # conked&slip-backward, sidestep-l/r
                        ('WriteOff',     (4, 6, 8, 10, 12),
                                         (75, 75, 75, 75, 75), 
                                         (5, 10, 15, 20, 25)), 
                                         # conked&slip-backward, sidestep-l/r
                        ('FillWithLead', (3, 4, 5, 6, 7),
                                         (75, 75, 75, 75, 75), 
                                         (20, 20, 20, 20, 20))) },
    
    #   Yes Man (A)
    'ym': { 'name': TTLocalizer.SuitYesman,
            'singularname': TTLocalizer.SuitYesmanS,
            'pluralname': TTLocalizer.SuitYesmanP,
            'level': 2,
            'hp': (20, 30, 42, 56, 72),  # actual suit level * 4
            'def': (10, 15, 20, 25, 30),
            'freq': (50, 30, 10, 5, 5),
            'acc': (65, 70, 75, 80, 85),
            'attacks': (('RubberStamp',  (2, 2, 3, 3, 4),        # dmg
                                         (75, 75, 75, 75, 75),   # acc 
                                         (35, 35, 35, 35, 35)),  # freq
                                         # flatten, sidestep-left/right
                        ('RazzleDazzle', (1, 1, 1, 1, 1),
                                         (50, 50, 50, 50, 50), 
                                         (25, 20, 15, 10, 5)),
                                         # conked&slip-backward, sidestep-l/r
                        ('Synergy',      (4, 5, 6, 7, 8),
                                         (50, 60, 70, 80, 90), 
                                         (5, 10, 15, 20, 25)),
                                         # slip-forward, jump
                        ('TeeOff',       (3, 3, 4, 4, 5),
                                         (50, 60, 70, 80, 90), 
                                         (35, 35, 35, 35, 35)),
                                         # conked&slip-backward, duck
                        # Not implementing for now 
                        #('Ditto',        (0, 0, 0, 0, 0),
                        #                 (75, 75, 75, 75, 75), 
                        #                 (0, 0, 0, 0, 0)),
                        ) },
    
    #   Micromanager (C)
    'mm': { 'name': TTLocalizer.SuitMicromanager,
            'singularname': TTLocalizer.SuitMicromanagerS,
            'pluralname': TTLocalizer.SuitMicromanagerP,
            'level': 3,
            'hp': (30, 42, 56, 72, 90),  # actual suit level * 4
            'def': (15, 20, 25, 30, 35),
            'freq': (50, 30, 10, 5, 5),
            'acc': (70, 75, 80, 82, 85),
            'attacks': (('Demotion',     (6, 8, 12, 15, 18),     # dmg
                                         (50, 60, 70, 80, 90),   # acc 
                                         (30, 30, 30, 30, 30)),  # freq
                                         # flatten, sidestep-left/right
                        ('FingerWag',    (4, 6, 9, 12, 15),
                                         (50, 60, 70, 80, 90), 
                                         (10, 10, 10, 10, 10)),
                                         # slip-forward, jump
                        ('FountainPen',  (3, 4, 6, 8, 10),
                                         (50, 60, 70, 80, 90), 
                                         (15, 15, 15, 15, 15)),
                                         # conked&slip-backward, sidestep-l/r
                        ('BrainStorm',   (4, 6, 9, 12, 15),
                                         (5, 5, 5, 5, 5), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&slip-backward, duck
                        ('BuzzWord',     (4, 6, 9, 12, 15),
                                         (50, 60, 70, 80, 90), 
                                         (20, 20, 20, 20, 20))) },
    
    #   Downsizer (B)
    'ds': { 'name': TTLocalizer.SuitDownsizer,
            'singularname': TTLocalizer.SuitDownsizerS,
            'pluralname': TTLocalizer.SuitDownsizerP,
            'level': 4,
            'hp': (42, 56, 72, 90, 110),  # actual suit level * 4
            'def': (20, 25, 30, 35, 40),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Canned',       (5, 6, 8, 10, 12),        # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (25, 25, 25, 25, 25)),  # freq
                                         # struggle&slip-backward, sidestep-left/right
                        ('Downsize',     (8, 9, 11, 13, 15),
                                         (50, 65, 70, 75, 80), 
                                         (35, 35, 35, 35, 35)),
                                         # cringe, jump
                        ('PinkSlip',     (4, 5, 6, 7, 8),
                                         (60, 65, 75, 80, 85),
                                         (25, 25, 25, 25, 25)),
                                         # slip-forward, sidestep-l/r
                        #('ReOrg',        (6, 8, 10, 12, 14),
                        #                 (70, 75, 80, 85, 90),
                        #                 (0, 0, 0, 0, 0)),
                                         # not used until can safely return toon to normal
                                         # if the movie gets cut off
                                         # cringe&jump, jump
                        ('Sacked',       (5, 6, 7, 8, 9),
                                         (50, 50, 50, 50, 50),
                                         (15, 15, 15, 15, 15))) },
                                         # struggle&jump&neutral, sidestep-l/r

    #   Head Hunter (A)
    'hh': { 'name': TTLocalizer.SuitHeadHunter,
            'singularname': TTLocalizer.SuitHeadHunterS,
            'pluralname': TTLocalizer.SuitHeadHunterP,
            'level': 5,
            'hp': (56, 72, 90, 110, 132),  # actual suit level * 4
            'def': (25, 30, 35, 40, 45),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('FountainPen',  (5, 6, 8, 10, 12),        # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (15, 15, 15, 15, 15)),  # freq
                                         # conked&slip-backward, duck
                        ('GlowerPower',  (7, 8, 10, 12, 13),
                                         (50, 60, 70, 80, 90), 
                                         (20, 20, 20, 20, 20)),
                                         # cringe&slip-backward, sidestep-l/r
                        ('HalfWindsor',  (8, 10, 12, 14, 16),
                                         (60, 65, 70, 75, 80),
                                         (20, 20, 20, 20, 20)),
                                         # conked&neutral, sidestep-l/r
                        ('HeadShrink',   (10, 12, 15, 18, 21),
                                         (65, 75, 80, 85, 95),
                                         (35, 35, 35, 35, 35)),
                                         # cringe&neutral, jump
                        ('Rolodex',      (6, 7, 8, 9, 10),
                                         (60, 65, 70, 75, 80),
                                         (10, 10, 10, 10, 10))) },
                                         # duck, sidestep-l/r

    #   Corporate Raider (C)
    'cr': { 'name': TTLocalizer.SuitCorporateRaider,
            'singularname': TTLocalizer.SuitCorporateRaiderS,
            'pluralname': TTLocalizer.SuitCorporateRaiderP,
            'level': 6,
            'hp': (72, 90, 110, 132, 156),  # actual suit level * 4
            'def': (30, 35, 40, 45, 50),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Canned',       (6, 7, 8, 9, 10),        # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # struggle&slip-backward, sidestep-left/right
                        ('EvilEye',      (12, 15, 18, 21, 24),
                                         (60, 70, 75, 80, 90), 
                                         (35, 35, 35, 35, 35)),
                                         # cringe&slip-backward, duck
                        ('PlayHardball', (7, 8, 12, 15, 16),
                                         (60, 65, 70, 75, 80),
                                         (30, 30, 30, 30, 30)),
                                         # slip-backward, sidestep-l/r
                        ('PowerTie',     (10, 12, 14, 16, 18),
                                         (65, 75, 80, 85, 95),
                                         (15, 15, 15, 15, 15))) },
                                         # conked&neutral, sidestep-l/r

    #   The Big Cheese (A)
    'tbc': {'name': TTLocalizer.SuitTheBigCheese,
            'singularname': TTLocalizer.SuitTheBigCheeseS,
            'pluralname': TTLocalizer.SuitTheBigCheeseP,
            'level': 7,
            'hp': (90, 110, 132, 156, 200),  # actual suit level * 4
            'def': (35, 40, 45, 50, 55),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('CigarSmoke',   (10, 12, 15, 18, 20),        # dmg
                                         (55, 65, 75, 85, 95),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # not implemented defaults to glower power
                                         # cringe, sidestep-left/right
                        ('FloodTheMarket', (14, 16, 18, 20, 22),
                                         (70, 75, 85, 90, 95), 
                                         (10, 10, 10, 10, 10)),
                                         # not implemented defaults to glower power
                                         # slip-backward&jump, sidestep-l/r
                        ('SongAndDance', (14, 15, 17, 19, 20),
                                         (60, 65, 70, 75, 80),
                                         (20, 20, 20, 20, 20)),
                                         # not implemented defaults to glower power
                                         # bounce&slip-backward, sidestep-l/r
                        ('TeeOff',       (8, 11, 14, 17, 20),
                                         (55, 65, 70, 75, 80),
                                         (50, 50, 50, 50, 50))) },
                                         # conked&slip-backward, duck

    #### Sales ####
    #   Cold Caller (C)
    'cc': { 'name': TTLocalizer.SuitColdCaller,
            'singularname': TTLocalizer.SuitColdCallerS,
            'pluralname': TTLocalizer.SuitColdCallerP,
            'level': 0,
            'hp': (6, 12, 20, 30, 42),  # actual suit level * 4
            'def': (2, 5, 10, 12, 15),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('FreezeAssets', (1, 1, 1, 1, 1),        # dmg
                                         (90, 90, 90, 90, 90),   # acc 
                                         (5, 10, 15, 20, 25)),  # freq
                                         # flatten, sidestep-left/right
                        ('PoundKey',     (2, 2, 3, 4, 5),
                                         (75, 80, 85, 90, 95), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&slip-backward, sidestep-l/r
                        ('DoubleTalk',   (2, 3, 4, 6, 8),
                                         (50, 55, 60, 65, 70), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&slip-backward, duck
                        ('HotAir',       (3, 4, 6, 8, 10),
                                         (50, 50, 50, 50, 50), 
                                         (45, 40, 35, 30, 25))) },
                                         # cringe, sidestep-l/r
    #   Telemarketer (B)
    'tm': { 'name': TTLocalizer.SuitTelemarketer,
            'singularname': TTLocalizer.SuitTelemarketerS,
            'pluralname': TTLocalizer.SuitTelemarketerP,
            'level': 1,
            'hp': (12, 20, 30, 42, 56),  # actual suit level * 4
            'def': (5, 10, 15, 20, 25),
            'freq': (50, 30, 10, 5, 5),
            'acc': (45, 50, 55, 60, 65),
            'attacks': (('ClipOnTie',    (2, 2, 3, 3, 4),        # dmg
                                         (75, 75, 75, 75, 75),   # acc 
                                         (15, 15, 15, 15, 15)),  # freq
                                         # flatten, sidestep-left/right
                        ('PickPocket',   (1, 1, 1, 1, 1),
                                         (75, 75, 75, 75, 75), 
                                         (15, 15, 15, 15, 15)),
                                         # conked&slip-backward, sidestep-l/r
                        ('Rolodex',      (4, 6, 7, 9, 12),
                                         (50, 50, 50, 50, 50), 
                                         (30, 30, 30, 30, 30)),
                                         # conked&slip-backward, sidestep-l/r
                        ('DoubleTalk',   (4, 6, 7, 9, 12),
                                         (75, 80, 85, 90, 95), 
                                         (40, 40, 40, 40, 40))) },
    # Namedropper (A)
    'nd': { 'name': TTLocalizer.SuitNameDropper,
            'singularname': TTLocalizer.SuitNameDropperS,
            'pluralname': TTLocalizer.SuitNameDropperP,
            'level': 2,
            'hp': (20, 30, 42, 56, 72),  # actual suit level * 4
            'def': (10, 15, 20, 25, 30),
            'freq': (50, 30, 10, 5, 5),
            'acc': (65, 70, 75, 80, 85),
            'attacks': (('RazzleDazzle', (4, 5, 6, 9, 12),       # dmg
                                         (75, 80, 85, 90, 95),   # acc
                                         (30, 30, 30, 30, 30)),  # freq
                                         # conked&slip-backward, sidestep-l/r
                        ('Rolodex',      (5, 6, 7, 10, 14),
                                         (95, 95, 95, 95, 95), 
                                         (40, 40, 40, 40, 40)),
                                         # duck, sidestep-l/r
                        ('Synergy',      (3, 4, 6, 9, 12),
                                         (50, 50, 50, 50, 50), 
                                         (15, 15, 15, 15, 15)),
                                         # slip-forward, jump
                        ('PickPocket',   (2, 2, 2, 2, 2),
                                         (95, 95, 95, 95, 95), 
                                         (15, 15, 15, 15, 15))) },
                                         # cringe, sidestep-l/r
    #   Gladhander (C)
    'gh': { 'name': TTLocalizer.SuitGladHander,
            'singularname': TTLocalizer.SuitGladHanderS,
            'pluralname': TTLocalizer.SuitGladHanderP,
            'level': 3,
            'hp': (30, 42, 56, 72, 90),  # actual suit level * 4
            'def': (15, 20, 25, 30, 35),
            'freq': (50, 30, 10, 5, 5),
            'acc': (70, 75, 80, 82, 85),
            'attacks': (('RubberStamp',  (4, 3, 3, 2, 1),        # dmg
                                         (90, 70, 50, 30, 10),   # acc 
                                         (40, 30, 20, 10, 5)),  # freq
                                         # flatten, sidestep-left/right
                        ('FountainPen',  (3, 3, 2, 1, 1),
                                         (70, 60, 50, 40, 30), 
                                         (40, 30, 20, 10, 5)),
                                         # conked&slip-backward, duck
                        ('Filibuster',   (4, 6, 9, 12, 15),
                                         (30, 40, 50, 60, 70), 
                                         (10, 20, 30, 40, 45)),
                                         # conked&slip-backward, duck
                        ('Schmooze',     (5, 7, 11, 15, 20),
                                         (55, 65, 75, 85, 95), 
                                         (10, 20, 30, 40, 45))) },

    #   Mover & Shaker (B)
    'ms': { 'name': TTLocalizer.SuitMoverShaker,
            'singularname': TTLocalizer.SuitMoverShakerS,
            'pluralname': TTLocalizer.SuitMoverShakerP,
            'level': 4,
            'hp': (42, 56, 72, 90, 110),  # actual suit level * 4
            'def': (20, 25, 30, 35, 40),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('BrainStorm',   (5, 6, 8, 10, 12),      # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (15, 15, 15, 15, 15)),  # freq
                                         # conked&slip-backward, duck
                        ('HalfWindsor',  (6, 9, 11, 13, 16),
                                         (50, 65, 70, 75, 80), 
                                         (20, 20, 20, 20, 20)),
                                         # conked&neutral, sidestep-l/r
                        ('Quake',        (9, 12, 15, 18, 21),
                                         (60, 65, 75, 80, 85),
                                         (20, 20, 20, 20, 20)),
                                         # shake, sidestep-l/r
                        ('Shake',        (6, 8, 10, 12, 14),
                                         (70, 75, 80, 85, 90),
                                         (25, 25, 25, 25, 25)),
                                         # shake, jump
                        ('Tremor',       (5, 6, 7, 8, 9),
                                         (50, 50, 50, 50, 50),
                                         (20, 20, 20, 20, 20))) },
                                         # shake, sidestep-l/r

    #   Two-Face (A)
    'tf': { 'name': TTLocalizer.SuitTwoFace,
            'singularname': TTLocalizer.SuitTwoFaceS,
            'pluralname': TTLocalizer.SuitTwoFaceP,
            'level': 5,
            'hp': (56, 72, 90, 110, 132),  # actual suit level * 4
            'def': (25, 30, 35, 40, 45),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('EvilEye',      (10, 12, 14, 16, 18),   # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (30, 30, 30, 30, 30)),  # freq
                                         # cringe&slip-backward, duck
                        ('HangUp',       (7, 8, 10, 12, 13),
                                         (50, 60, 70, 80, 90), 
                                         (15, 15, 15, 15, 15)),
                                         # slip-backward&neutral, sidestep-l/r
                        ('RazzleDazzle', (8, 10, 12, 14, 16),
                                         (60, 65, 70, 75, 80),
                                         (30, 30, 30, 30, 30)),
                                         # conked&slip-backward, sidestep-l/r
                        ('RedTape',      (6, 7, 8, 9, 10),
                                         (60, 65, 75, 85, 90),
                                         (25, 25, 25, 25, 25))) },
                                         # bound&jump, sidestep-l/r

    #   The Mingler (A)
    'm': { 'name': TTLocalizer.SuitTheMingler,
            'singularname': TTLocalizer.SuitTheMinglerS,
            'pluralname': TTLocalizer.SuitTheMinglerP,
            'level': 6,
            'hp': (72, 90, 110, 132, 156),  # actual suit level * 4
            'def': (30, 35, 40, 45, 50),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('BuzzWord',     (10, 11, 13, 15, 16),   # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # cringe, sidestep-left/right
                        ('ParadigmShift', (12, 15, 18, 21, 24),
                                         (60, 70, 75, 80, 90), 
                                         (25, 25, 25, 25, 25)),
                                         # shift, sidestep-l/r
                        ('PowerTrip',    (10, 13, 14, 15, 18),
                                         (60, 65, 70, 75, 80),
                                         (15, 15, 15, 15, 15)),
                                         # slip-forward, jump
                        ('Schmooze',     (7, 8, 12, 15, 16),
                                         (55, 65, 75, 85, 95),
                                         (30, 30, 30, 30, 30)),
                                         # slip-backward, sidestep-l/r
                        ('TeeOff',       (8, 9, 10, 11, 12),
                                         (70, 75, 80, 85, 95),
                                         (10, 10, 10, 10, 10))) },
                                         # conked&slip-backward, duck

    #   Mr. Hollywood (A)
    'mh': {'name': TTLocalizer.SuitMrHollywood,
            'singularname': TTLocalizer.SuitMrHollywoodS,
            'pluralname': TTLocalizer.SuitMrHollywoodP,
            'level': 7,
            'hp': (90, 110, 132, 156, 200),  # actual suit level * 4
            'def': (35, 40, 45, 50, 55),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('PowerTrip',    (10, 12, 15, 18, 20),   # dmg
                                         (55, 65, 75, 85, 95),   # acc 
                                         (50, 50, 50, 50, 50)),  # freq
                                         # slip-forward, jump
                        ('RazzleDazzle', (8, 11, 14, 17, 20),
                                         (70, 75, 85, 90, 95), 
                                         (50, 50, 50, 50, 50)),
                                         # conked&slip-backward, sidestep-l/r
                        #('SandTrap',     (14, 15, 17, 19, 20),
                        #                 (60, 65, 70, 75, 80),
                        #                 (0, 0, 0, 0, 0)),
                                         # not implemented defaults to razzle dazzle
                                         # slip-forward, duck
                        #('SongAndDance', (12, 14, 16, 18, 20),
                        #                 (65, 75, 80, 85, 95),
                        #                 (0, 0, 0, 0, 0)),
                                         # not implemented defaults to razzle dazzle
                        ) },
                                         # bounce&slip-backward, sidestep-l/r

    #### Money ####
    #   Short Change (C)
    'sc': { 'name': TTLocalizer.SuitShortChange,
            'singularname': TTLocalizer.SuitShortChangeS,
            'pluralname': TTLocalizer.SuitShortChangeP,
            'level': 0,
            'hp': (6, 12, 20, 30, 42),  # actual suit level * 4
            'def': (2, 5, 10, 12, 15),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Watercooler',  (2, 2, 3, 4, 6),        # dmg
                                         (50, 50, 50, 50, 50),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # flatten, sidestep-left/right
                        ('BounceCheck',  (3, 5, 7, 9, 11),
                                         (75, 80, 85, 90, 95), 
                                         (15, 15, 15, 15, 15)),
                                         # conked&slip-backward, duck
                        ('ClipOnTie',    (1, 1, 2, 2, 3),
                                         (50, 50, 50, 50, 50), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&slip-backward, duck
                        ('PickPocket',   (2, 2, 3, 4, 6),
                                         (95, 95, 95, 95, 95), 
                                         (40, 40, 40, 40, 40))) },
    #   Penny Pincher (A)
    'pp': { 'name': TTLocalizer.SuitPennyPincher,
            'singularname': TTLocalizer.SuitPennyPincherS,
            'pluralname': TTLocalizer.SuitPennyPincherP,
            'level': 1,
            'hp': (12, 20, 30, 42, 56),  # actual suit level * 4
            'def': (5, 10, 15, 20, 25),
            'freq': (50, 30, 10, 5, 5),
            'acc': (45, 50, 55, 60, 65),
            'attacks': (('BounceCheck',  (4, 5, 6, 8, 12),       # dmg
                                         (75, 75, 75, 75, 75),   # acc 
                                         (45, 45, 45, 45, 45)),  # freq
                                         # flatten, sidestep-left/right
                        ('FreezeAssets', (2, 3, 4, 6, 9),
                                         (75, 75, 75, 75, 75), 
                                         (20, 20, 20, 20, 20)),
                                         # conked&slip-backward, sidestep-l/r
                        ('FingerWag',    (1, 2, 3, 4, 6),
                                         (50, 50, 50, 50, 50), 
                                         (35, 35, 35, 35, 35)),
                                         # conked&slip-backward, sidestep-l/r
                        # PennyPinch not implemented
                        #('PennyPinch',   (0, 0, 0, 0, 0),
                        #                 (75, 75, 75, 75, 75), 
                        #                 (0, 0, 0, 0, 0)),
                        ) },
    #   Tightwad (C)
    'tw': { 'name': TTLocalizer.SuitTightwad,
            'singularname': TTLocalizer.SuitTightwadS,
            'pluralname': TTLocalizer.SuitTightwadP,
            'level': 2,
            'hp': (20, 30, 42, 56, 72),  # actual suit level * 4
            'def': (10, 15, 20, 25, 30),
            'freq': (50, 30, 10, 5, 5),
            'acc': (65, 70, 75, 80, 85),
            'attacks': (('Fired',        (3, 4, 5, 5, 6),      # dmg
                                         (75, 75, 75, 75, 75), # acc
                                         (75, 5, 5, 5, 5)), # freq
                                         # cringe, sidestep-l/r
                        ('GlowerPower',  (3, 4, 6, 9, 12),
                                         (95, 95, 95, 95, 95), 
                                         (10, 15, 20, 25, 30)),
                                         # cringe&slip-backward, sidestep-l/r
                        ('FingerWag',    (3, 3, 4, 4, 5),
                                         (75, 75, 75, 75, 75), 
                                         (5, 70, 5, 5, 5)),
                                         # slip-backward, sidestep-l/r
                        ('FreezeAssets', (3, 4, 6, 9, 12),
                                         (75, 75, 75, 75, 75), 
                                         (5, 5, 65, 5, 30)),
                                         # cringe, sidestep-l/r
                        ('BounceCheck',  (5, 6, 9, 13, 18),
                                         (75, 75, 75, 75, 75), 
                                         (5, 5, 5, 60, 30))) },
                                         # conked, jump
    #   Bean Counter (B)
    'bc': { 'name': TTLocalizer.SuitBeanCounter,
            'singularname': TTLocalizer.SuitBeanCounterS,
            'pluralname': TTLocalizer.SuitBeanCounterP,
            'level': 3,
            'hp': (30, 42, 56, 72, 90),  # actual suit level * 4
            'def': (15, 20, 25, 30, 35),
            'freq': (50, 30, 10, 5, 5),
            'acc': (70, 75, 80, 82, 85),
            'attacks': (('Audit',        (4, 6, 9, 12, 15),      # dmg
                                         (95, 95, 95, 95, 95),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # flatten, sidestep-left/right
                        ('Calculate',    (4, 6, 9, 12, 15),
                                         (75, 75, 75, 75, 75), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&slip-backward, duck
                        ('Tabulate',     (4, 6, 9, 12, 15),
                                         (75, 75, 75, 75, 75), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&slip-backward, duck
                        ('WriteOff',     (4, 6, 9, 12, 15),
                                         (95, 95, 95, 95, 95), 
                                         (30, 30, 30, 30, 30))) },

    #   Number Cruncher (A)
    'nc': { 'name': TTLocalizer.SuitNumberCruncher,
            'singularname': TTLocalizer.SuitNumberCruncherS,
            'pluralname': TTLocalizer.SuitNumberCruncherP,
            'level': 4,
            'hp': (42, 56, 72, 90, 110),  # actual suit level * 4
            'def': (20, 25, 30, 35, 40),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Audit',        (5, 6, 8, 10, 12),      # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (15, 15, 15, 15, 15)),  # freq
                                         # flatten, sidestep-left/right
                        ('Calculate',    (6, 7, 9, 11, 13),
                                         (50, 65, 70, 75, 80), 
                                         (30, 30, 30, 30, 30)),
                                         # conked&slip-backward, duck
                        ('Crunch',       (8, 9, 11, 13, 15),
                                         (60, 65, 75, 80, 85),
                                         (35, 35, 35, 35, 35)),
                                         # slip-forward&flatten, sidestep-l/r
                        ('Tabulate',     (5, 6, 7, 8, 9),
                                         (50, 50, 50, 50, 50),
                                         (20, 20, 20, 20, 20))) },
                                         # conked&slip-backward, duck

    #   Money Bags (C)
    'mb': { 'name': TTLocalizer.SuitMoneyBags,
            'singularname': TTLocalizer.SuitMoneyBagsS,
            'pluralname': TTLocalizer.SuitMoneyBagsP,
            'level': 5,
            'hp': (56, 72, 90, 110, 132),  # actual suit level * 4
            'def': (25, 30, 35, 40, 45),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Liquidate',    (10, 12, 14, 16, 18),   # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (30, 30, 30, 30, 30)),  # freq
                                         # melt&jump, sidestep-l/r
                        ('MarketCrash',  (8, 10, 12, 14, 16),
                                         (60, 65, 70, 75, 80),
                                         (45, 45, 45, 45, 45)),
                                         # flatten&jump, sidestep-l/r
                        ('PowerTie',     (6, 7, 8, 9, 10),
                                         (60, 65, 75, 85, 90),
                                         (25, 25, 25, 25, 25))) },
                                         # conked&neutral, sidestep-l/r

    #   Loan Shark (B)
    'ls': { 'name': TTLocalizer.SuitLoanShark,
            'singularname': TTLocalizer.SuitLoanSharkS,
            'pluralname': TTLocalizer.SuitLoanSharkP,
            'level': 6,
            'hp': (72, 90, 110, 132, 156),  # actual suit level * 4
            'def': (30, 35, 40, 45, 50),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Bite',         (10, 11, 13, 15, 16),   # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (30, 30, 30, 30, 30)),  # freq
                                         # conked, duck
                        ('Chomp',        (12, 15, 18, 21, 24),
                                         (60, 70, 75, 80, 90), 
                                         (35, 35, 35, 35, 35)),
                                         # slip-backward, sidestep-l/r
                        ('PlayHardball', (9, 11, 12, 13, 15),
                                         (55, 65, 75, 85, 95),
                                         (20, 20, 20, 20, 20)),
                                         # slip-backward, sidestep-l/r
                        ('WriteOff',     (6, 8, 10, 12, 14),
                                         (70, 75, 80, 85, 95),
                                         (15, 15, 15, 15, 15))) },
                                         # slip-forward, sidestep-l/r

    #   Robber Baron (A)
    'rb': { 'name': TTLocalizer.SuitRobberBaron,
            'singularname': TTLocalizer.SuitRobberBaronS,
            'pluralname': TTLocalizer.SuitRobberBaronP,
            'level': 7,
            'hp': (90, 110, 132, 156, 200),  # actual suit level * 4
            'def': (35, 40, 45, 50, 55),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (
                        #('FiveOClockShadow', (14, 17, 19, 21, 24),   # dmg
                        #                 (55, 65, 75, 85, 95),   # acc 
                        #                 (0, 0, 0, 0, 0)),  # freq
                                         # not implemented defaults to tee off
                                         # slip-forward, jump
                        #('FloodTheMarket', (12, 15, 18, 21, 24),
                        #                 (70, 75, 85, 90, 95), 
                        #                 (0, 0, 0, 0, 0)),
                                         # not implemented defaults to tee off
                                         # slip-backward&jump, sidestep-l/r
                        ('PowerTrip',    (11, 14, 16, 18, 21),
                                         (60, 65, 70, 75, 80),
                                         (50, 50, 50, 50, 50)),
                                         # slip-forward, jump
                        ('TeeOff',       (10, 12, 14, 16, 18),
                                         (60, 65, 75, 85, 90),
                                         (50, 50, 50, 50, 50))) },
                                         # conked&slip-backward, duck

    #### Legal ####
    #   Bottom Feeder (C)
    'bf': { 'name': TTLocalizer.SuitBottomFeeder,
            'singularname': TTLocalizer.SuitBottomFeederS,
            'pluralname': TTLocalizer.SuitBottomFeederP,
            'level': 0,
            'hp': (6, 12, 20, 30, 42),  # actual suit level * 4
            'def': (2, 5, 10, 12, 15),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('RubberStamp',  (2, 3, 4, 5, 6),        # dmg
                                         (75, 80, 85, 90, 95),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # flatten, sidestep-left/right
                        ('Shred',        (2, 4, 6, 8, 10),
                                         (50, 55, 60, 65, 70), 
                                         (20, 20, 20, 20, 20)),
                                         # conked&slip-backward, duck
                        ('Watercooler',  (3, 4, 5, 6, 7),
                                         (95, 95, 95, 95, 95), 
                                         (10, 10, 10, 10, 10)),
                                         # conked&slip-backward, duck
                        ('PickPocket',   (1, 1, 2, 2, 3),
                                         (25, 30, 35, 40, 45), 
                                         (50, 50, 50, 50, 50))) },
    #   Bloodsucker (B)
    'b':  { 'name': TTLocalizer.SuitBloodsucker,
            'singularname': TTLocalizer.SuitBloodsuckerS,
            'pluralname': TTLocalizer.SuitBloodsuckerP,
            'level': 1,
            'hp': (12, 20, 30, 42, 56),  # actual suit level * 4
            'def': (5, 10, 15, 20, 25),
            'freq': (50, 30, 10, 5, 5),
            'acc': (45, 50, 55, 60, 65),
            'attacks': (('EvictionNotice', (1, 2, 3, 3, 4),      # dmg
                                         (75, 75, 75, 75, 75),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # flatten, sidestep-left/right
                        ('RedTape',      (2, 3, 4, 6, 9),
                                         (75, 75, 75, 75, 75), 
                                         (20, 20, 20, 20, 20)),
                                         # conked&slip-backward, sidestep-l/r
                        ('Withdrawal',   (6, 8, 10, 12, 14),
                                         (95, 95, 95, 95, 95), 
                                         (10, 10, 10, 10, 10)),
                                         # conked&slip-backward, sidestep-l/r
                        ('Liquidate',    (2, 3, 4, 6, 9),
                                         (50, 60, 70, 80, 90), 
                                         (50, 50, 50, 50, 50))) },
    #   Double Talker (A)
    'dt': { 'name': TTLocalizer.SuitDoubleTalker,
            'singularname': TTLocalizer.SuitDoubleTalkerS,
            'pluralname': TTLocalizer.SuitDoubleTalkerP,
            'level': 2,
            'hp': (20, 30, 42, 56, 72),  # actual suit level * 4
            'def': (10, 15, 20, 25, 30),
            'freq': (50, 30, 10, 5, 5),
            'acc': (65, 70, 75, 80, 85),
            'attacks': (('RubberStamp',  (1, 1, 1, 1, 1),      # dmg
                                         (50, 60, 70, 80, 90), # acc
                                         (5, 5, 5, 5, 5)), # freq
                                         # cringe, sidestep-l/r
                        ('BounceCheck',  (1, 1, 1, 1, 1),
                                         (50, 60, 70, 80, 90), 
                                         (5, 5, 5, 5, 5)),
                                         # conked, jump
                        ('BuzzWord',     (1, 2, 3, 5, 6),
                                         (50, 60, 70, 80, 90),
                                         (20, 20, 20, 20, 20)),
                                         # cringe, duck
                        ('DoubleTalk',   (6, 6, 9, 13, 18),
                                         (50, 60, 70, 80, 90),
                                         (25, 25, 25, 25, 25)),
                                         # cringe, sidestep-l/r
                        ('Jargon',       (3, 4, 6, 9, 12),
                                         (50, 60, 70, 80, 90),
                                         (25, 25, 25, 25, 25)),
                                         # cringe, sidestep-l/r
                        ('MumboJumbo',   (3, 4, 6, 9, 12),
                                         (50, 60, 70, 80, 90),
                                         (20, 20, 20, 20, 20))) },
                                         # cringe, sidestep-l/r
    # Ambulance Chaser (B)
    'ac': { 'name': TTLocalizer.SuitAmbulanceChaser,
            'singularname': TTLocalizer.SuitAmbulanceChaserS,
            'pluralname': TTLocalizer.SuitAmbulanceChaserP,
            'level': 3,
            'hp': (30, 42, 56, 72, 90),  # actual suit level * 4
            'def': (15, 20, 25, 30, 35),
            'freq': (50, 30, 10, 5, 5),
            'acc': (65, 70, 75, 80, 85),
            'attacks': (('Shake',        (4, 6, 9, 12, 15),      # dmg
                                         (75, 75, 75, 75, 75), # acc
                                         (15, 15, 15, 15, 15)), # freq
                                         # shake, jump
                        ('RedTape',      (6, 8, 12, 15, 19),
                                         (75, 75, 75, 75, 75), 
                                         (30, 30, 30, 30, 30)),
                                         # bound&jump, sidestep-l/r
                        ('Rolodex',      (3, 4, 5, 6, 7),
                                         (75, 75, 75, 75, 75), 
                                         (20, 20, 20, 20, 20)),
                                         # duck, sidestep-l/r
                        ('HangUp',       (2, 3, 4, 5, 6),
                                         (75, 75, 75, 75, 75), 
                                         (35, 35, 35, 35, 35))) },
                                         # slip-backward&neutral, sidestep-l/r

    #   Back Stabber (A)
    'bs': { 'name': TTLocalizer.SuitBackStabber,
            'singularname': TTLocalizer.SuitBackStabberS,
            'pluralname': TTLocalizer.SuitBackStabberP,
            'level': 4,
            'hp': (42, 56, 72, 90, 110),  # actual suit level * 4
            'def': (20, 25, 30, 35, 40),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('GuiltTrip',    (8, 11, 13, 15, 18),      # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (40, 40, 40, 40, 40)),  # freq
                                         # slip-forward&neutral, jump
                        ('RestrainingOrder', (6, 7, 9, 11, 13),
                                         (50, 65, 70, 75, 90), 
                                         (25, 25, 25, 25, 25)),
                                         # conked&bound, sidestep-l/r
                        ('FingerWag',    (5, 6, 7, 8, 9),
                                         (50, 55, 65, 75, 80),
                                         (35, 35, 35, 35, 35))) },
                                         # slip-backward, sidestep-l/r

    #   Spin Doctor (B)
    'sd': { 'name': TTLocalizer.SuitSpinDoctor,
            'singularname': TTLocalizer.SuitSpinDoctorS,
            'pluralname': TTLocalizer.SuitSpinDoctorP,
            'level': 5,
            'hp': (56, 72, 90, 110, 132),  # actual suit level * 4
            'def': (25, 30, 35, 40, 45),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('ParadigmShift', (9, 10, 13, 16, 17),   # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (30, 30, 30, 30, 30)),  # freq
                                         # shift, sidestep-l/r
                        ('Quake',        (8, 10, 12, 14, 16),
                                         (60, 65, 70, 75, 80),
                                         (20, 20, 20, 20, 20)),
                                         # shake, sidestep-l/r
                        ('Spin',         (10, 12, 15, 18, 20),
                                         (70, 75, 80, 85, 90),
                                         (35, 35, 35, 35, 35)),
                                         # spin, sidestep-l/r
                        ('WriteOff',     (6, 7, 8, 9, 10),
                                         (60, 65, 75, 85, 90),
                                         (15, 15, 15, 15, 15))) },
                                         # slip-forward, sidestep-l/r

    #   Legal Eagle (A)
    'le': { 'name': TTLocalizer.SuitLegalEagle,
            'singularname': TTLocalizer.SuitLegalEagleS,
            'pluralname': TTLocalizer.SuitLegalEagleP,
            'level': 6,
            'hp': (72, 90, 110, 132, 156),  # actual suit level * 4
            'def': (30, 35, 40, 45, 50),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('EvilEye',      (10, 11, 13, 15, 16),   # dmg
                                         (60, 75, 80, 85, 90),   # acc 
                                         (20, 20, 20, 20, 20)),  # freq
                                         # cringe&slip-backward, duck
                        ('Jargon',       (7, 9, 11, 13, 15),
                                         (60, 70, 75, 80, 90), 
                                         (15, 15, 15, 15, 15)),
                                         # cringe, sidestep-l/r
                        ('Legalese',     (11, 13, 16, 19, 21),
                                         (55, 65, 75, 85, 95),
                                         (35, 35, 35, 35, 35)),
                                         # cringe, sidestep-l/r
                        ('PeckingOrder', (12, 15, 17, 19, 22),
                                         (70, 75, 80, 85, 95),
                                         (30, 30, 30, 30, 30))) },
                                         # duck, sidestep-l/r

    #   Big Wig (A)
    'bw': { 'name': TTLocalizer.SuitBigWig,
            'singularname': TTLocalizer.SuitBigWigS,
            'pluralname': TTLocalizer.SuitBigWigP,
            'level': 7,
            'hp': (90, 110, 132, 156, 200),  # actual suit level * 4
            'def': (35, 40, 45, 50, 55),
            'freq': (50, 30, 10, 5, 5),
            'acc': (35, 40, 45, 50, 55),
            'attacks': (
                        #('CigarSmoke',   (12, 14, 16, 18, 20),   # dmg
                        #                 (65, 75, 85, 90, 95),   # acc 
                        #                 (0, 0, 0, 0, 0)),  # freq
                                         # not implemented defaults to finger wag
                                         # cringe, sidestep-left/right
                        #('Gavel',        (14, 16, 19, 22, 24),
                        #                 (70, 75, 85, 90, 95), 
                        #                 (0, 0, 0, 0, 0)),
                                         # not implemented defaults to finger wag
                                         # slip-backward, sidestep-l/r
                        ('PowerTrip',    (10, 11, 13, 15, 16),
                                         (75, 80, 85, 90, 95),
                                         (50, 50, 50, 50, 50)),
                                         # slip-forward, jump
                        ('ThrowBook',    (13, 15, 17, 19, 21),
                                         (80, 85, 85, 85, 90),
                                         (50, 50, 50, 50, 50))) },
                                         # not implemented defaults to finger wag
                                         # conked&neutral, sidestep-l/r

    }

ATK_TGT_UNKNOWN = 1
ATK_TGT_SINGLE = 2
ATK_TGT_GROUP = 3
SuitAttacks = {
    'Audit':            ('phone',           ATK_TGT_SINGLE),
    'Bite':             ('throw-paper',     ATK_TGT_SINGLE),    
    'BounceCheck':      ('throw-paper',     ATK_TGT_SINGLE),
    'BrainStorm':       ('effort',          ATK_TGT_SINGLE),
    'BuzzWord':         ('speak',           ATK_TGT_SINGLE),
    'Calculate':        ('phone',           ATK_TGT_SINGLE),
    'Canned':           ('throw-paper',     ATK_TGT_SINGLE),
    'Chomp':            ('throw-paper',     ATK_TGT_SINGLE),
    'CigarSmoke':       ('cigar-smoke',     ATK_TGT_SINGLE),
    'ClipOnTie':        ('throw-paper',     ATK_TGT_SINGLE),
    'Crunch':           ('throw-object',    ATK_TGT_SINGLE),
    'Demotion':         ('magic1',          ATK_TGT_SINGLE),
    'DoubleTalk':       ('speak',           ATK_TGT_SINGLE),
    'Downsize':         ('magic2',          ATK_TGT_SINGLE),
    'EvictionNotice':   ('throw-paper',     ATK_TGT_SINGLE),
    'EvilEye':          ('glower',          ATK_TGT_SINGLE),
    'Filibuster':       ('speak',           ATK_TGT_SINGLE),
    'FillWithLead':     ('pencil-sharpener', ATK_TGT_SINGLE),
    'FingerWag':        ('finger-wag',      ATK_TGT_SINGLE),
    'Fired':            ('magic2',          ATK_TGT_SINGLE),
    'FiveOClockShadow': ('glower',          ATK_TGT_SINGLE),
    'FloodTheMarket':   ('glower',          ATK_TGT_SINGLE),
    'FountainPen':      ('pen-squirt',      ATK_TGT_SINGLE),
    'FreezeAssets':     ('glower',          ATK_TGT_SINGLE),
    'Gavel':            ('gavel',           ATK_TGT_SINGLE),
    'GlowerPower':      ('glower',          ATK_TGT_SINGLE),
    'GuiltTrip':        ('magic1',          ATK_TGT_GROUP),
    'HalfWindsor':      ('throw-paper',     ATK_TGT_SINGLE),
    'HangUp':           ('phone',           ATK_TGT_SINGLE),
    'HeadShrink':       ('magic1',          ATK_TGT_SINGLE),
    'HotAir':           ('speak',           ATK_TGT_SINGLE),
    'Jargon':           ('speak',           ATK_TGT_SINGLE),
    'Legalese':         ('speak',           ATK_TGT_SINGLE),
    'Liquidate':        ('magic1',          ATK_TGT_SINGLE),
    'MarketCrash':      ('throw-paper',     ATK_TGT_SINGLE),
    'MumboJumbo':       ('speak',           ATK_TGT_SINGLE),
    'ParadigmShift':    ('magic2',          ATK_TGT_GROUP),
    'PeckingOrder':     ('throw-object',    ATK_TGT_SINGLE),
    'PickPocket':       ('pickpocket',      ATK_TGT_SINGLE),
    'PinkSlip':         ('throw-paper',     ATK_TGT_SINGLE),
    'PlayHardball':     ('throw-paper',     ATK_TGT_SINGLE),
    'PoundKey':         ('phone',           ATK_TGT_SINGLE),
    'PowerTie':         ('throw-paper',     ATK_TGT_SINGLE),
    'PowerTrip':        ('magic1',          ATK_TGT_GROUP),
    'Quake':            ('quick-jump',      ATK_TGT_GROUP),
    'RazzleDazzle':     ('smile',           ATK_TGT_SINGLE),
    'RedTape':          ('throw-object',    ATK_TGT_SINGLE),
    'ReOrg':            ('magic3',          ATK_TGT_SINGLE),
    'RestrainingOrder': ('throw-paper',     ATK_TGT_SINGLE),
    'Rolodex':          ('roll-o-dex',      ATK_TGT_SINGLE),
    'RubberStamp':      ('rubber-stamp',    ATK_TGT_SINGLE),
    'RubOut':           ('hold-eraser',     ATK_TGT_SINGLE),
    'Sacked':           ('throw-paper',     ATK_TGT_SINGLE),
    'SandTrap':         ('golf-club-swing', ATK_TGT_SINGLE),
    'Schmooze':         ('speak',           ATK_TGT_SINGLE),
    'Shake':            ('stomp',           ATK_TGT_GROUP),
    'Shred':            ('shredder',        ATK_TGT_SINGLE),
    'SongAndDance':     ('song-and-dance',  ATK_TGT_SINGLE),
    'Spin':             ('magic3',          ATK_TGT_SINGLE),
    'Synergy':          ('magic3',          ATK_TGT_GROUP),
    'Tabulate':         ('phone',           ATK_TGT_SINGLE),
    'TeeOff':           ('golf-club-swing', ATK_TGT_SINGLE),
    'ThrowBook':        ('throw-object',    ATK_TGT_SINGLE),
    'Tremor':           ('stomp',           ATK_TGT_GROUP),
    'Watercooler':      ('watercooler',     ATK_TGT_SINGLE),
    'Withdrawal':       ('magic1',          ATK_TGT_SINGLE),
    'WriteOff':         ('hold-pencil',     ATK_TGT_SINGLE),
    }

AUDIT = SuitAttacks.keys().index('Audit')
BITE = SuitAttacks.keys().index('Bite')
BOUNCE_CHECK = SuitAttacks.keys().index('BounceCheck')
BRAIN_STORM = SuitAttacks.keys().index('BrainStorm')
BUZZ_WORD = SuitAttacks.keys().index('BuzzWord')
CALCULATE = SuitAttacks.keys().index('Calculate')
CANNED = SuitAttacks.keys().index('Canned')
CHOMP = SuitAttacks.keys().index('Chomp')
CIGAR_SMOKE = SuitAttacks.keys().index('CigarSmoke')
CLIPON_TIE = SuitAttacks.keys().index('ClipOnTie')
CRUNCH = SuitAttacks.keys().index('Crunch')
DEMOTION = SuitAttacks.keys().index('Demotion')
DOWNSIZE = SuitAttacks.keys().index('Downsize')
DOUBLE_TALK = SuitAttacks.keys().index('DoubleTalk')
EVICTION_NOTICE = SuitAttacks.keys().index('EvictionNotice')
EVIL_EYE = SuitAttacks.keys().index('EvilEye')
FILIBUSTER = SuitAttacks.keys().index('Filibuster')
FILL_WITH_LEAD = SuitAttacks.keys().index('FillWithLead')
FINGER_WAG = SuitAttacks.keys().index('FingerWag')
FIRED = SuitAttacks.keys().index('Fired')
FIVE_O_CLOCK_SHADOW = SuitAttacks.keys().index('FiveOClockShadow')
FLOOD_THE_MARKET = SuitAttacks.keys().index('FloodTheMarket')
FOUNTAIN_PEN = SuitAttacks.keys().index('FountainPen')
FREEZE_ASSETS = SuitAttacks.keys().index('FreezeAssets')
GAVEL = SuitAttacks.keys().index('Gavel')
GLOWER_POWER = SuitAttacks.keys().index('GlowerPower')
GUILT_TRIP = SuitAttacks.keys().index('GuiltTrip')
HALF_WINDSOR = SuitAttacks.keys().index('HalfWindsor')
HANG_UP = SuitAttacks.keys().index('HangUp')
HEAD_SHRINK = SuitAttacks.keys().index('HeadShrink')
HOT_AIR = SuitAttacks.keys().index('HotAir')
JARGON = SuitAttacks.keys().index('Jargon')
LEGALESE = SuitAttacks.keys().index('Legalese')
LIQUIDATE = SuitAttacks.keys().index('Liquidate')
MARKET_CRASH = SuitAttacks.keys().index('MarketCrash')
MUMBO_JUMBO = SuitAttacks.keys().index('MumboJumbo')
PARADIGM_SHIFT = SuitAttacks.keys().index('ParadigmShift')
PECKING_ORDER = SuitAttacks.keys().index('PeckingOrder')
PICK_POCKET = SuitAttacks.keys().index('PickPocket')
PINK_SLIP = SuitAttacks.keys().index('PinkSlip')
PLAY_HARDBALL = SuitAttacks.keys().index('PlayHardball')
POUND_KEY = SuitAttacks.keys().index('PoundKey')
POWER_TIE = SuitAttacks.keys().index('PowerTie')
POWER_TRIP = SuitAttacks.keys().index('PowerTrip')
QUAKE = SuitAttacks.keys().index('Quake')
RAZZLE_DAZZLE = SuitAttacks.keys().index('RazzleDazzle')
RED_TAPE = SuitAttacks.keys().index('RedTape')
RE_ORG = SuitAttacks.keys().index('ReOrg')
RESTRAINING_ORDER = SuitAttacks.keys().index('RestrainingOrder')
ROLODEX = SuitAttacks.keys().index('Rolodex')
RUBBER_STAMP = SuitAttacks.keys().index('RubberStamp')
RUB_OUT = SuitAttacks.keys().index('RubOut')
SACKED = SuitAttacks.keys().index('Sacked')
SANDTRAP = SuitAttacks.keys().index('SandTrap')
SCHMOOZE = SuitAttacks.keys().index('Schmooze')
SHAKE = SuitAttacks.keys().index('Shake')
SHRED = SuitAttacks.keys().index('Shred')
SONG_AND_DANCE = SuitAttacks.keys().index('SongAndDance')
SPIN = SuitAttacks.keys().index('Spin')
SYNERGY = SuitAttacks.keys().index('Synergy')
TABULATE = SuitAttacks.keys().index('Tabulate')
TEE_OFF = SuitAttacks.keys().index('TeeOff')
THROW_BOOK = SuitAttacks.keys().index('ThrowBook')
TREMOR = SuitAttacks.keys().index('Tremor')
WATERCOOLER = SuitAttacks.keys().index('Watercooler')
WITHDRAWAL = SuitAttacks.keys().index('Withdrawal')
WRITE_OFF = SuitAttacks.keys().index('WriteOff')

def getFaceoffTaunt(suitName, doId):
    if SuitFaceoffTaunts.has_key(suitName):
        taunts = SuitFaceoffTaunts[suitName]
    else:
        taunts = TTLocalizer.SuitFaceoffDefaultTaunts
    #return random.choice(taunts)
    return taunts[doId % len(taunts)]

SuitFaceoffTaunts = OTPLocalizer.SuitFaceoffTaunts



def getAttackTauntIndexFromIndex(suit, attackIndex):
    adict = getSuitAttack(suit.getStyleName(), suit.getLevel(), attackIndex)
    return getAttackTauntIndex(adict['name'])

def getAttackTauntIndex(attackName):
    if (SuitAttackTaunts.has_key(attackName)):
        taunts = SuitAttackTaunts[attackName]
        return random.randint(0, len(taunts)-1)
    else:
        return 1

def getAttackTaunt(attackName, index=None):
    if (SuitAttackTaunts.has_key(attackName)):
        taunts = SuitAttackTaunts[attackName]
    else:
        taunts = TTLocalizer.SuitAttackDefaultTaunts

    if (index != None):
        # If there's been a mistake, just use a default taunt
        if (index >= len(taunts)):
            notify.warning("index exceeds length of taunts list in getAttackTaunt")
            return TTLocalizer.SuitAttackDefaultTaunts[0]

        return taunts[index]
    else:
        return random.choice(taunts)



SuitAttackTaunts = TTLocalizer.SuitAttackTaunts


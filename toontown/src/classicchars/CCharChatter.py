
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

GREETING = 0
COMMENT  = 1
GOODBYE  = 2

DaisyChatter = TTLocalizer.DaisyChatter
MickeyChatter = TTLocalizer.MickeyChatter
VampireMickeyChatter = TTLocalizer.VampireMickeyChatter
MinnieChatter = TTLocalizer.MinnieChatter
GoofyChatter = TTLocalizer.GoofyChatter
GoofySpeedwayChatter = TTLocalizer.GoofySpeedwayChatter
DonaldChatter = TTLocalizer.DonaldChatter
ChipChatter = TTLocalizer.ChipChatter
DaleChatter = TTLocalizer.DaleChatter

def getChatter( charName, chatterType ):
    if charName==TTLocalizer.Mickey:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFMickeyChatter
        elif chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterMickeyCChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS:
            return TTLocalizer.WinterMickeyDChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesMickeyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_ONE:
            SillyMickeyChatter = MickeyChatter
            SillyMickeyChatter[1].extend(TTLocalizer.SillyPhase1Chatter)
            return SillyMickeyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_TWO:
            SillyMickeyChatter = MickeyChatter
            SillyMickeyChatter[1].extend(TTLocalizer.SillyPhase2Chatter)
            return SillyMickeyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_THREE:
            SillyMickeyChatter = MickeyChatter
            SillyMickeyChatter[1].extend(TTLocalizer.SillyPhase3Chatter)
            return SillyMickeyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_FOUR:
            SillyMickeyChatter = MickeyChatter
            SillyMickeyChatter[1].extend(TTLocalizer.SillyPhase4Chatter)
            return SillyMickeyChatter
        else:
            return MickeyChatter
    
    elif charName==TTLocalizer.VampireMickey:
        return VampireMickeyChatter
    
    elif charName==TTLocalizer.Minnie:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFMinnieChatter
        elif chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterMinnieCChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS:
            return TTLocalizer.WinterMinnieDChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesMinnieChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_ONE:
            SillyMinnieChatter = MinnieChatter
            SillyMinnieChatter[1].extend(TTLocalizer.SillyPhase1Chatter)
            return SillyMinnieChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_TWO:
            SillyMinnieChatter = MinnieChatter
            SillyMinnieChatter[1].extend(TTLocalizer.SillyPhase2Chatter)
            return SillyMinnieChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_THREE:
            SillyMinnieChatter = MinnieChatter
            SillyMinnieChatter[1].extend(TTLocalizer.SillyPhase3Chatter)
            return SillyMinnieChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_FOUR:
            SillyMinnieChatter = MinnieChatter
            SillyMinnieChatter[1].extend(TTLocalizer.SillyPhase4Chatter)
            return SillyMinnieChatter
        else:
            return MinnieChatter
    
    elif charName == TTLocalizer.WitchMinnie:
        return TTLocalizer.WitchMinnieChatter
    
    elif charName==TTLocalizer.Daisy:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFDaisyChatter
        elif chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.HalloweenDaisyChatter
        elif chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterDaisyCChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS:
            return TTLocalizer.WinterDaisyDChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesDaisyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_ONE:
            SillyDaisyChatter = DaisyChatter
            SillyDaisyChatter[1].extend(TTLocalizer.SillyPhase1Chatter)
            return SillyDaisyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_TWO:
            SillyDaisyChatter = DaisyChatter
            SillyDaisyChatter[1].extend(TTLocalizer.SillyPhase2Chatter)
            return SillyDaisyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_THREE:
            SillyDaisyChatter = DaisyChatter
            SillyDaisyChatter[1].extend(TTLocalizer.SillyPhase3Chatter)
            return SillyDaisyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_FOUR:
            SillyDaisyChatter = DaisyChatter
            SillyDaisyChatter[1].extend(TTLocalizer.SillyPhase4Chatter)
            return SillyDaisyChatter
        else:
            return DaisyChatter
    
    elif charName==TTLocalizer.Goofy:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFGoofySpeedwayChatter                        
        elif chatterType == ToontownGlobals.CRASHED_LEADERBOARD:        
            return TTLocalizer.CLGoofySpeedwayChatter
        elif chatterType == ToontownGlobals.CIRCUIT_RACING_EVENT:        
            return TTLocalizer.GPGoofySpeedwayChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS \
            or chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterGoofyChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesGoofyChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_ONE:
            SillyGoofySpeedwayChatter = GoofySpeedwayChatter
            SillyGoofySpeedwayChatter[1].extend(TTLocalizer.SillyPhase1Chatter)
            return SillyGoofySpeedwayChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_TWO:
            SillyGoofySpeedwayChatter = GoofySpeedwayChatter
            SillyGoofySpeedwayChatter[1].extend(TTLocalizer.SillyPhase2Chatter)
            return SillyGoofySpeedwayChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_THREE:
            SillyGoofySpeedwayChatter = GoofySpeedwayChatter
            SillyGoofySpeedwayChatter[1].extend(TTLocalizer.SillyPhase3Chatter)
            return SillyGoofySpeedwayChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_FOUR:
            SillyGoofySpeedwayChatter = GoofySpeedwayChatter
            SillyGoofySpeedwayChatter[1].extend(TTLocalizer.SillyPhase4Chatter)
            return SillyGoofySpeedwayChatter
        else:
            return GoofySpeedwayChatter
    
    elif charName==TTLocalizer.SuperGoofy:
        return TTLocalizer.SuperGoofyChatter
    
    elif charName==TTLocalizer.Donald:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFDonaldChatter
        elif chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.HalloweenDreamlandChatter
        elif chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterDreamlandCChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS:
            return TTLocalizer.WinterDreamlandDChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesDreamlandChatter
        else:
            return DonaldChatter
    
    elif charName==TTLocalizer.DonaldDock:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFDonaldDockChatter
        elif chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.HalloweenDonaldChatter
        elif chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterDonaldCChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS:
            return TTLocalizer.WinterDonaldDChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesDonaldChatter
        else:
            return None
    
    elif charName==TTLocalizer.Pluto:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFPlutoChatter
        elif chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.WesternPlutoChatter
        elif chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterPlutoCChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS:
            return TTLocalizer.WinterPlutoDChatter
        else:
            # Pluto don't play that!
            return None
    
    elif charName==TTLocalizer.WesternPluto:
        if chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.WesternPlutoChatter
        else:
            return None
    
    elif charName == TTLocalizer.Chip:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFChipChatter
        elif chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.HalloweenChipChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS \
            or chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterChipChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesChipChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_ONE:
            SillyChipChatter = ChipChatter
            SillyChipChatter[1].extend(TTLocalizer.SillyPhase1Chatter)
            return SillyChipChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_TWO:
            SillyChipChatter = ChipChatter
            SillyChipChatter[1].extend(TTLocalizer.SillyPhase2Chatter)
            return SillyChipChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_THREE:
            SillyChipChatter = ChipChatter
            SillyChipChatter[1].extend(TTLocalizer.SillyPhase3Chatter)
            return SillyChipChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_FOUR:
            SillyChipChatter = ChipChatter
            SillyChipChatter[1].extend(TTLocalizer.SillyPhase4Chatter)
            return SillyChipChatter
        else:
            return ChipChatter
    
    elif charName == TTLocalizer.Dale:
        if chatterType == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            return TTLocalizer.AFDaleChatter
        elif chatterType == ToontownGlobals.HALLOWEEN_COSTUMES:
            return TTLocalizer.HalloweenDaleChatter
        elif chatterType == ToontownGlobals.WINTER_DECORATIONS \
            or chatterType == ToontownGlobals.WINTER_CAROLING:
            return TTLocalizer.WinterDaleChatter
        elif chatterType == ToontownGlobals.VALENTINES_DAY:
            return TTLocalizer.ValentinesDaleChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_ONE:
            SillyDaleChatter = DaleChatter
            SillyDaleChatter[1].extend(TTLocalizer.SillyPhase1Chatter)
            return SillyDaleChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_TWO:
            SillyDaleChatter = DaleChatter
            SillyDaleChatter[1].extend(TTLocalizer.SillyPhase2Chatter)
            return SillyDaleChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_THREE:
            SillyDaleChatter = DaleChatter
            SillyDaleChatter[1].extend(TTLocalizer.SillyPhase3Chatter)
            return SillyDaleChatter
        elif chatterType == ToontownGlobals.SILLY_CHATTER_FOUR:
            SillyDaleChatter = DaleChatter
            SillyDaleChatter[1].extend(TTLocalizer.SillyPhase4Chatter)
            return SillyDaleChatter
        else:
            return DaleChatter
    else:
        assert 0, "Unknown chatter information"

from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import Sequence,  Func
from toontown.hood import InteractiveAnimatedProp
from toontown.hood import GenericAnimatedProp
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals, TTLocalizer

    
class HydrantInteractiveProp(InteractiveAnimatedProp.InteractiveAnimatedProp):
    """We need much more functionality than GenericAnimatedProp to
    make interactive props behave correctly in battle.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'HydrantInteractiveProp')

    BattleCheerText =  TTLocalizer.InteractivePropTrackBonusTerms[ToontownBattleGlobals.SQUIRT_TRACK]
    
    # ZoneToIdles format
    # sound has been taken out assumed to be same as animation file, but starts with tt_s
    # animation, minNumberOfLoops, maxNumberOfLoops, settleAnim, minPauseTime, maxPauseTime
    
    ZoneToIdles = { 
        ToontownGlobals.ToontownCentral: (
        ('tt_a_ara_ttc_hydrant_idle0', 1, 1, None, 3, 10),
        ('tt_a_ara_ttc_hydrant_idle2', 1, 1, None, 3, 10),
        ('tt_a_ara_ttc_hydrant_idle1', 1, 1, None, 3, 10),
        ('tt_a_ara_ttc_hydrant_idleAwesome3', 1, 1, None, 3, 10),
        ),
        # dod hydrants are actually ttc
        ToontownGlobals.DonaldsDock: (
        ('tt_a_ara_ttc_hydrant_idle0', 1, 1, None, 3, 10),
        ('tt_a_ara_ttc_hydrant_idle2', 1, 1, None, 3, 10),
        ('tt_a_ara_ttc_hydrant_idle1', 1, 1, None, 3, 10),
        ('tt_a_ara_ttc_hydrant_idleAwesome3', 1, 1, None, 3, 10),
        ),
        ToontownGlobals.DaisyGardens: (
        ('tt_a_ara_dga_hydrant_idle0', 3, 10, 'tt_a_ara_dga_hydrant_idle0settle', 3, 10),
        ('tt_a_ara_dga_hydrant_idleLook1', 1, 1, None, 3, 10),
        ('tt_a_ara_dga_hydrant_idleSneeze2', 1, 1, None, 3, 10),
        ('tt_a_ara_dga_hydrant_idleAwesome3', 1, 1, None, 3, 10),
        ),
        ToontownGlobals.MinniesMelodyland: (
        ('tt_a_ara_mml_hydrant_idle0', 3, 10, 'tt_a_ara_mml_hydrant_idle0settle', 3, 10),
        ('tt_a_ara_mml_hydrant_idle2', 3, 10, 'tt_a_ara_mml_hydrant_idle2settle', 3, 10),
        ('tt_a_ara_mml_hydrant_idle1', 3, 10, 'tt_a_ara_mml_hydrant_idle1settle', 3, 10),
        ('tt_a_ara_mml_hydrant_idleAwesome3', 1, 1, None, 3, 10),
        ),
        ToontownGlobals.TheBrrrgh: (
        ('tt_a_ara_tbr_hydrant_idleShiver1', 1, 1, None, 3, 10),
        ('tt_a_ara_tbr_hydrant_idleRubNose0', 1, 1, None, 3, 10),
        ('tt_a_ara_tbr_hydrant_idleSneeze2', 1, 1, None, 3, 10),
        ('tt_a_ara_tbr_hydrant_idleAwesome3', 1, 1, None, 3, 10),

        ),
        ToontownGlobals.DonaldsDreamland: (
        ('tt_a_ara_ddl_hydrant_idle0', 3, 10, None, 0, 0),
        ('tt_a_ara_ddl_hydrant_idle1', 1, 1, None, 0, 0),
        ('tt_a_ara_ddl_hydrant_idle2', 1, 1, None, 0, 0),
        ('tt_a_ara_ddl_hydrant_idleAwesome3', 1, 1, None, 0, 0),
        ),
     }

    ZoneToIdleIntoFightAnims = {
        ToontownGlobals.ToontownCentral: 'tt_a_ara_ttc_hydrant_idleIntoFight',
        # dod hydrants are actually ttc
        ToontownGlobals.DonaldsDock: 'tt_a_ara_ttc_hydrant_idleIntoFight',
        ToontownGlobals.DaisyGardens: 'tt_a_ara_dga_hydrant_idleIntoFight',
        ToontownGlobals.MinniesMelodyland: 'tt_a_ara_mml_hydrant_idleIntoFight',
        ToontownGlobals.TheBrrrgh: 'tt_a_ara_tbr_hydrant_idleIntoFight',
        ToontownGlobals.DonaldsDreamland: 'tt_a_ara_ddl_hydrant_idleIntoFight',
     }

    ZoneToVictoryAnims = {
        ToontownGlobals.ToontownCentral: 'tt_a_ara_ttc_hydrant_victoryDance',
        # dod hydrants are actually ttc
        ToontownGlobals.DonaldsDock: 'tt_a_ara_ttc_hydrant_victoryDance',
        ToontownGlobals.DaisyGardens: 'tt_a_ara_dga_hydrant_victoryDance',
        ToontownGlobals.MinniesMelodyland: 'tt_a_ara_mml_hydrant_victoryDance',
        ToontownGlobals.TheBrrrgh: 'tt_a_ara_tbr_hydrant_victoryDance',
        ToontownGlobals.DonaldsDreamland: 'tt_a_ara_ddl_hydrant_victoryDance',
     }

    ZoneToSadAnims = {
        ToontownGlobals.ToontownCentral: 'tt_a_ara_ttc_hydrant_fightSad',
        # dod hydrants are actually ttc
        ToontownGlobals.DonaldsDock: 'tt_a_ara_ttc_hydrant_fightSad',
        ToontownGlobals.DaisyGardens: 'tt_a_ara_dga_hydrant_fightSad',
        ToontownGlobals.MinniesMelodyland: 'tt_a_ara_mml_hydrant_fightSad',
        ToontownGlobals.TheBrrrgh: 'tt_a_ara_tbr_hydrant_fightSad',
        ToontownGlobals.DonaldsDreamland: 'tt_a_ara_ddl_hydrant_fightSad',
     }       

    ZoneToFightAnims = {
        ToontownGlobals.ToontownCentral: (
        'tt_a_ara_ttc_hydrant_fightBoost',
        'tt_a_ara_ttc_hydrant_fightCheer',
        'tt_a_ara_ttc_hydrant_fightIdle',
        ),
        # dod hydrants are actually ttc
        ToontownGlobals.DonaldsDock: (
        'tt_a_ara_ttc_hydrant_fightBoost',
        'tt_a_ara_ttc_hydrant_fightCheer',
        'tt_a_ara_ttc_hydrant_fightIdle',
        ),
        ToontownGlobals.DaisyGardens: (
        'tt_a_ara_dga_hydrant_fightBoost',
        'tt_a_ara_dga_hydrant_fightCheer',
        'tt_a_ara_dga_hydrant_fightIdle',
        ),
        ToontownGlobals.MinniesMelodyland: (
        'tt_a_ara_mml_hydrant_fightBoost',
        'tt_a_ara_mml_hydrant_fightCheer',
        'tt_a_ara_mml_hydrant_fightIdle',
        ),
        ToontownGlobals.TheBrrrgh: (
        'tt_a_ara_tbr_hydrant_fightBoost',
        'tt_a_ara_tbr_hydrant_fightCheer',
        'tt_a_ara_tbr_hydrant_fightIdle',
        ),
        ToontownGlobals.DonaldsDreamland: (
        'tt_a_ara_ddl_hydrant_fightBoost',
        'tt_a_ara_ddl_hydrant_fightCheer',
        'tt_a_ara_ddl_hydrant_fightIdle',
        ),
     }

    IdlePauseTime = base.config.GetFloat('prop-idle-pause-time',0.0)

    def __init__(self, node):
        """Construct ourself, in the correct orrder."""
        self.leftWater = None
        self.rightWater = None
        InteractiveAnimatedProp.InteractiveAnimatedProp.__init__(self, node, ToontownGlobals.HYDRANTS_BUFF_BATTLES)
        

    def setupActor(self, node):
        InteractiveAnimatedProp.InteractiveAnimatedProp.setupActor(self, node)
        if not self.hoodId == ToontownGlobals.TheBrrrgh:
            water = loader.loadModel('phase_5/models/char/tt_m_efx_hydrantSquirt')
            self.leftWater = water.find("**/efx_hydrantSquirtLeft")
            self.rightWater = water.find("**/efx_hydrantSquirtRight")
            dx_left_water = self.node.find('**/dx_left_water')
            if self.leftWater:
                self.leftWater.reparentTo(dx_left_water)
                base.leftWater = self.leftWater
                self.leftWater.hide()
            else:
                self.notify.warning("couldnt find %s in rig for hood %d" % ('dx_left_water', self.hoodId))
            dx_right_water = self.node.find('**/dx_right_water')
            if self.rightWater:
                self.rightWater.reparentTo(dx_right_water)
                self.rightWater.hide()
            else:
                self.notify.warning("couldnt find %s in rig for hood %d" % ('dx_left_water', self.hoodId))

    def hideWater(self):
        """Hide our water parts if any."""
        if self.leftWater:
            self.leftWater.hide()
        if self.rightWater:
            self.rightWater.hide()

    def showWater(self):
        """Show our water parts, if any."""
        if self.leftWater:
            self.leftWater.show()
        if self.rightWater:
            self.rightWater.show()

    def hasOverrideIval(self, origAnimName):
        """We need to show and hide water parts for fightBoost."""
        result = False
        if ( ("fightBoost" in origAnimName) or ('fightCheer' in origAnimName) ) and \
           not self.hoodId == ToontownGlobals.TheBrrrgh:
            result = True
        return result

    def getOverrideIval(self, origAnimName):
        """Return the actor interval sandwiched betweeh show and hide water."""
        result = Sequence()
        if ( ("fightBoost" in origAnimName) or ('fightCheer' in origAnimName) )  and \
           not self.hoodId == ToontownGlobals.TheBrrrgh:
            result.append(Func(self.showWater))
            # a little bit of special info here we know fightBoost is fight0
            if 'fightBoost' in origAnimName:
                animKey = "fight0"
            else:
                animKey = "fight1"
            animAndSound = self.createAnimAndSoundIval(animKey)
            result.append(animAndSound)
            result.append(Func(self.hideWater))
        return result

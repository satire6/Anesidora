from SpecImports import *
from toontown.toonbase import ToontownGlobals

###### TO BE CONVERTED TO ENTITY SYSTEM ######
# entIds of entities that the cogs are put under
CogParent = 10000

# unique IDs for battle cells
BattleCellId = 0

BattleCells = {
    BattleCellId : {'parentEntId' : CogParent,
                    'pos' : Point3(0,0,0),
                    },
    }

CogData = [
    {'parentEntId' : CogParent,
     'boss' : 0,
     'level' : ToontownGlobals.CashbotMintCogLevel,
     'battleCell' : BattleCellId,
     'pos' : Point3(-6,0,0),
     'h' : 180,
     'behavior' : 'stand',
     'path' : None,
     'skeleton' : 0,
     },
    {'parentEntId' : CogParent,
     'boss' : 0,
     'level' : ToontownGlobals.CashbotMintCogLevel+1,
     'battleCell' : BattleCellId,
     'pos' : Point3(-2,0,0),
     'h' : 180,
     'behavior' : 'stand',
     'path' : None,
     'skeleton' : 0,
     },
    {'parentEntId' : CogParent,
     'boss' : 0,
     'level' : ToontownGlobals.CashbotMintCogLevel,
     'battleCell' : BattleCellId,
     'pos' : Point3(2,0,0),
     'h' : 180,
     'behavior' : 'stand',
     'path' : None,
     'skeleton' : 0,
     },
    {'parentEntId' : CogParent,
     'boss' : 0,
     'level' : ToontownGlobals.CashbotMintCogLevel+1,
     'battleCell' : BattleCellId,
     'pos' : Point3(6,0,0),
     'h' : 180,
     'behavior' : 'stand',
     'path' : None,
     'skeleton' : 0,
     },
    ]

ReserveCogData = [
    ]

from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct

# MintShelf is very close to MintProduct, but is *not* a 'MintProduct';
# I'm deriving anyway
class MintShelf(MintProduct.MintProduct):
    Models = {
        CashbotMintIntA : 'phase_10/models/cashbotHQ/shelf_A1MoneyBags',
        CashbotMintIntB : 'phase_10/models/cashbotHQ/shelf_A1Money',
        CashbotMintIntC : 'phase_10/models/cashbotHQ/shelf_A1Gold',
        }
    Scales = {
        CashbotMintIntA : 1.,
        CashbotMintIntB : 1.,
        CashbotMintIntC : 1.,
        }

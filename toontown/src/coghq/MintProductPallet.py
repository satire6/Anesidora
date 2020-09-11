from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct

# MintProductPallet is very close to MintProduct, but is *not* a 'MintProduct';
# I'm deriving anyway
class MintProductPallet(MintProduct.MintProduct):
    Models = {
        CashbotMintIntA : 'phase_10/models/cashbotHQ/DoubleCoinStack.bam',
        CashbotMintIntB : 'phase_10/models/cogHQ/DoubleMoneyStack.bam',
        CashbotMintIntC : 'phase_10/models/cashbotHQ/DoubleGoldStack.bam',
        }
    Scales = {
        CashbotMintIntA : 1.,
        CashbotMintIntB : 1.,
        CashbotMintIntC : 1.,
        }

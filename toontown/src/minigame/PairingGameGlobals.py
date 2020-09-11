import PlayingCardDeck

EasiestGameDuration = 120
HardestGameDuration = 90

EndlessGame = config.GetBool('endless-pairing-game', 0)

# what is the highest rank we use in the game
MaxRankIndexUsed = [7,7,7,8,9]


# we define this here, to make sure AI and client use the same version
def createDeck(deckSeed, numPlayers):
    deck = PlayingCardDeck.PlayingCardDeck()
    deck.shuffleWithSeed(deckSeed)
    deck.removeRanksAbove(MaxRankIndexUsed[numPlayers])
    return deck
    
def calcGameDuration(difficulty):
    # difficulty should be from 0..1
    difference = EasiestGameDuration - HardestGameDuration
    adjust = difference * difficulty
    retval = EasiestGameDuration - adjust
    return retval

def calcLowFlipModifier(matches, flips):
    # returns 0..1 
    idealFlips = round ( (matches * 2) * 1.6)
    if idealFlips < 2:
        idealFlips = 2
    maxFlipsForBonus = idealFlips * 2
    retval = 0
    if flips < idealFlips:
        retval =  1
    elif  maxFlipsForBonus < flips:
        retval = 0
    else:
        divisor = maxFlipsForBonus - idealFlips
        difference = maxFlipsForBonus - flips
        retval = float(difference) / divisor
    return retval
        
        
        
        
    

"""ChatGarbler module: conatins the ChatGarbler class"""

import string
#import whrandom
import random
from otp.otpbase import OTPLocalizer

class ChatGarbler:
    """ChatGarbler class: contains methods to convert chat messages
    to animal sounds"""

    def garble(self, avatar, message):
        """garble(self, Avatar, string)
        Replace a chat message with a series of animal sounds
        based on the toon's animal type
        Algorithm completely disregards original message to
        prohibit any sort of meaningful communication
        """
        newMessage = ""

        numWords = random.randint(1, 7)

        wordlist = OTPLocalizer.ChatGarblerDefault
        
        for i in range(1, numWords+1):
            wordIndex = random.randint(0, len(wordlist)-1)
            newMessage = newMessage + wordlist[wordIndex]
            if (i < numWords):
                newMessage = newMessage + " "

        return newMessage
        
    def garbleSingle(self, avatar, message):
        """garble(self, Avatar, string)
        Replace a chat message with a series of animal sounds
        based on the toon's animal type
        Algorithm completely disregards original message to
        prohibit any sort of meaningful communication
        """
        newMessage = ""

        numWords = 1

        wordlist = OTPLocalizer.ChatGarblerDefault
        
        for i in range(1, numWords+1):
            wordIndex = random.randint(0, len(wordlist)-1)
            newMessage = newMessage + wordlist[wordIndex]
            if (i < numWords):
                newMessage = newMessage + " "

        return newMessage





"""ChatGarbler module: conatins the ChatGarbler class"""

import string
import random
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from otp.chat import ChatGarbler

class ToonChatGarbler(ChatGarbler.ChatGarbler):
    """ToonChatGarbler class: contains methods to convert chat messages
    to animal sounds"""

    animalSounds = {
        "dog" : TTLocalizer.ChatGarblerDog,
        "cat" : TTLocalizer.ChatGarblerCat,
        "mouse" : TTLocalizer.ChatGarblerMouse,
        "horse" : TTLocalizer.ChatGarblerHorse,
        "rabbit" : TTLocalizer.ChatGarblerRabbit,
        "duck" : TTLocalizer.ChatGarblerDuck,
        "monkey" : TTLocalizer.ChatGarblerMonkey,
        "bear" : TTLocalizer.ChatGarblerBear,
        "pig"  : TTLocalizer.ChatGarblerPig,
        "default" : OTPLocalizer.ChatGarblerDefault,
        }


    def garble(self, toon, message):
        """garble(self, Avatar, string)
        Replace a chat message with a series of animal sounds
        based on the toon's animal type
        Algorithm completely disregards original message to
        prohibit any sort of meaningful communication
        """
        newMessage = ""

        animalType = toon.getStyle().getType()

        if (ToonChatGarbler.animalSounds.has_key(animalType)):
            wordlist = ToonChatGarbler.animalSounds[animalType]
        else:
            wordlist = ToonChatGarbler.animalSounds["default"]
        
        numWords = random.randint(1, 7)

        for i in range(1, numWords+1):
            wordIndex = random.randint(0, len(wordlist)-1)
            newMessage = newMessage + wordlist[wordIndex]
            if (i < numWords):
                newMessage = newMessage + " "

        return newMessage
        
    def garbleSingle(self, toon, message):
        """garble(self, Avatar, string)
        Replace a chat message with a series of animal sounds
        based on the toon's animal type
        Algorithm completely disregards original message to
        prohibit any sort of meaningful communication
        """
        newMessage = ""

        animalType = toon.getStyle().getType()

        if (ToonChatGarbler.animalSounds.has_key(animalType)):
            wordlist = ToonChatGarbler.animalSounds[animalType]
        else:
            wordlist = ToonChatGarbler.animalSounds["default"]
        
        numWords = 1

        for i in range(1, numWords+1):
            wordIndex = random.randint(0, len(wordlist)-1)
            newMessage = newMessage + wordlist[wordIndex]
            if (i < numWords):
                newMessage = newMessage + " "

        return newMessage





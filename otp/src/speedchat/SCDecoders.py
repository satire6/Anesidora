"""SCDecoders.py: contains functions to decode SpeedChat messages """

"""
Each of these functions normally returns the ready-to-display text
string that corresponds to the encoded message. If there is a problem,
None is returned.
"""
from SCStaticTextTerminal import decodeSCStaticTextMsg
from SCCustomTerminal     import decodeSCCustomMsg
from SCEmoteTerminal      import decodeSCEmoteWhisperMsg

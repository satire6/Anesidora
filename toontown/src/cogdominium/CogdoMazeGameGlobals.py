"""
@author: Schell Games
3-10-2010
"""
import math

from direct.showbase import PythonUtil

from pandac.PandaModules import VBase4

from toontown.minigame import MazeData

TempMazeFile = "phase_4/models/minigames/maze_3player"
TempMazeData = MazeData.mazeData[TempMazeFile]

GameActions = PythonUtil.Enum((
        "Unlock",
        "EnterDoor",
        "RevealLock",
        "RevealDoor",
        "GameOver",
    ))

GameDuration = 180.0

ToonRunSpeed = 9.778

OverheadCameraAngle = math.radians(60)
OverheadCameraDistance = 30

LockColors = (
    VBase4(1, 1, 1, 1),
    VBase4(0, 0, 1, 1),
    VBase4(1, 1, 0, 1),
    VBase4(1, 0, 0, 1),
    )

LockNames = (
    "White",
    "Blue",
    "Yellow",
    "Red"
    )

#===============================================================================
# AUDIO
#===============================================================================

MusicFiles = {
    "normal" : "phase_9/audio/bgm/CHQ_FACT_bg.mid",
    "suspense": "phase_7/audio/bgm/encntr_general_bg_indoor.mid",
    "timeRunningOut": "phase_7/audio/bgm/encntr_suit_winning_indoor.mid",
    "end" : "phase_4/audio/bgm/FF_safezone.mid"
    }

SfxFiles = {
    "doorOpen": "phase_5/audio/sfx/elevator_door_open.mp3",
    "fusePlaced": "phase_11/audio/sfx/LB_laser_beam_on_2.mp3",
    "notification": "phase_3.5/audio/sfx/GUI_whisper_3.mp3",
    }

# TEMP Placed here!

class CogdoMazeLockInfo:
    def __init__(self, toonId, tileX, tileY, locked=True):
        self.toonId = toonId
        self.locked = locked
        self.tileX = tileX
        self.tileY = tileY

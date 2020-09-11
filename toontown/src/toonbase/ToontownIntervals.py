"""Generic intervals that can be used throughout Toontown classes."""

from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait, Func

PULSE_GUI_DURATION = 0.2
PULSE_GUI_CHANGE = .333

def cleanup(name):
    """Clean stop of an ival"""
    taskMgr.remove(name)   

def start(ival):
    """Clean start of an ival"""
    cleanup(ival.getName())
    ival.start()
    
def loop(ival):
    """Clean loop of an ival"""
    cleanup(ival.getName())
    ival.loop()


def getPulseLargerIval(np, name, duration=PULSE_GUI_DURATION, scale=1):
    """Creates a boing larger effect"""
    return getPulseIval(np, name, 1 + PULSE_GUI_CHANGE, duration=duration, scale=scale)
    
def getPulseSmallerIval(np, name, duration=PULSE_GUI_DURATION, scale=1):
    """Creates a boing smaller effect"""
    return getPulseIval(np, name, 1 - PULSE_GUI_CHANGE, duration=duration, scale=scale)
    
def getPulseIval(np, name, change, duration=PULSE_GUI_CHANGE, scale=1):
    """Creates a boing interval builder"""
    return Sequence(
        np.scaleInterval(duration, scale * change, blendType='easeOut'),
        np.scaleInterval(duration, scale, blendType='easeIn'),
        name=name,
        autoFinish=1
        )

    
def getPresentGuiIval(np, name, waitDuration=0.5, moveDuration=1.0, parent=aspect2d):
    """
    Presents a new GUI:
    Shows/boings the gui right on the center of the screen,
    then moves the gui to where it's supposed to go.
    """
    endPos = np.getPos()
    np.setPos(parent, 0, 0, 0)
    
    return Sequence(
        Func(np.show),
        getPulseLargerIval(np, "", scale=np.getScale()),
        Wait(waitDuration),
        np.posInterval(
            moveDuration,
            endPos,
            blendType="easeInOut",
            ),
        name=name,
        autoFinish=1
        )
        
    

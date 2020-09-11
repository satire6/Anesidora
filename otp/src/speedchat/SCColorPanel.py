from SCColorScheme import SCColorScheme
from direct.tkwidgets.Valuator import *

colors = {}
panels = {}

def scRgbPanel(callback, title, initColor):
    def getScaledColor(color, s):
        return tuple(map(lambda x: x*s, color))
    sInitColor = getScaledColor(initColor, 255.)
    vgp = ValuatorGroupPanel(title=title,
                             dim=3,
                             labels=['R','G','B'],
                             value=[int(sInitColor[0]),
                                    int(sInitColor[1]),
                                    int(sInitColor[2])],
                             type = 'slider',
                             valuator_style='mini',
                             valuator_min=0,
                             valuator_max=255,
                             valuator_resolution=1,
                             fDestroy=1)
    # Add a print button which will also serve as a color tile
    pButton = Button(vgp.interior(), text = '',
                     bg = getTkColorString(sInitColor))
    pButton.pack(expand = 1, fill = BOTH)

    def acceptColor(color):
        pButton['bg'] = getTkColorString(color)
        # scale colors to 0..1
        callback(getScaledColor(color, 1/255.))

    def getDefaultFrameColor():
        global colors
        # set the color scheme without the frameColor
        base.speedChat.setColorScheme(SCColorScheme(
            arrowColor=colors['arrowColor'],
            rolloverColor=colors['rolloverColor'],
            ))
        # update the colors dictionary
        colors['frameColor'] = \
            base.speedChat.getColorScheme().getFrameColor()
        p = panels['frameColor'].component('valuatorGroup')
        c = colors['frameColor']
        p.component('valuator0').set(math.floor(c[0]*255))
        p.component('valuator1').set(math.floor(c[1]*255))
        p.component('valuator2').set(math.floor(c[2]*255))

    def updateAllPanels():
        global colors
        # update the colors dictionary
        cs = base.speedChat.getColorScheme()
        colors['arrowColor'] = cs.getArrowColor()
        colors['rolloverColor'] = cs.getRolloverColor()
        colors['frameColor'] = cs.getFrameColor()

        # update the panels
        for panelName in colors.keys():
            p = panels[panelName].component('valuatorGroup')
            c = colors[panelName]
            p.component('valuator0').set(math.floor(c[0]*255))
            p.component('valuator1').set(math.floor(c[1]*255))
            p.component('valuator2').set(math.floor(c[2]*255))

    # Update menu
    menu = vgp.component('menubar').component('Valuator Group-menu')
    # Some helper functions
    menu.insert_command(index = 0, label = 'Get Default FrameColor',
                        command = getDefaultFrameColor)
    menu.insert_command(index = 1, label = 'Update All Panels',
                        command = updateAllPanels)


    vgp['command'] = acceptColor
    return vgp

# adjust the main and contrasting speedchat colors
def adjustSCColors():
    global colors
    base.startTk()
    cs = base.speedChat.getColorScheme()
    colors = {
        'arrowColor': cs.getArrowColor(),
        'rolloverColor': cs.getRolloverColor(),
        'frameColor': cs.getFrameColor(),
        }
    for colorName in colors.keys():
        def handleCallback(color, colorName=colorName):
            global colors
            colors[colorName] = tuple(color)
            base.speedChat.setColorScheme(SCColorScheme(**colors))
        
        panels[colorName] = scRgbPanel(handleCallback, colorName, colors[colorName])

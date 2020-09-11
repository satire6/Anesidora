import sys
import string
import __builtin__
from direct.directtools.DirectUtil import getFileData
from direct.distributed.PyDatagram import PyDatagram
from math import tan

from pandac.PandaModules import *

try:
    __builtin__.launcher
except AttributeError:
    __builtin__.launcher = None

def hexToColor(hexString, alpha = None):
    if alpha == None:
        alpha = 1
        if len(hexString) >= 8:
            alpha = eval ('0x' + hexString[6:8])/255.
        
    return Vec4(eval ('0x' + hexString[0:2])/255.,
                eval ('0x' + hexString[2:4])/255.,
                eval ('0x' + hexString[4:6])/255.,
                alpha)

# Parse command line arguments
headAngle = 0
pitchAngle = -1
rollAngle = 20
ringColor = 'F0AA40'
bgColor = 'FFFFCC'
ringScale = 0.1
fov = 20
fillFactor = 0.75
outputDirectory = '.'
inputFile = 'TopToons.txt'
overrideTexture = None
backgroundImage = 'Sky'
lookAtTarget = 'head'
fHideRing = 0
argFlag = None
outputExtension = 'jpg'
size = 50

def printHelp():
    print
    print 'ppython TopToonPics.py [options]'
    print 'Options:'
    print '  -a headAngle         Specify angle of toons head (default 10 deg)'
    print '  -b BG color          Specify background color (default FFFFCC)'
    print '  -B BG image          Specify file name for background image'
    print '  -c Ring color        Specify ring color (default F0AA40)'
    print '  -d outputDirectory   Specify directory for resulting images'
    print '  -f FOV               Specify camera FOV'
    print '  -F fillFactor        Specify percent of FOV to fill (1-100)'
    print '  -i inputFile         Specify filename holding DNA strings'
    print '  -l lookTarget        Specify look at target (head/body)'
    print '  -nr                  Hide circular frame surrounding toon'
    print '  -p head pitch        Specify pitch of toons head (default -1 deg)'
    print '  -r roll              Specify camera roll'
    print '  -s ring thickness    Specify thickness for outer ring (0 no-ring)'
    print '  -e extension         Specify extension (and file type) of output'
    print '  -S size              Specify the width/height of the images in pixes. Default is 50'
    print '  -h                   Print this help message'
    sys.exit()

for arg in sys.argv:
    if arg == '-a':
        argFlag = 'a'
    elif arg == '-b':
        argFlag = 'b'
    elif arg == '-B':
        argFlag = 'B'
    elif arg == '-c':
        argFlag = 'c'
    elif arg == '-d':
        argFlag = 'd'
    elif arg == '-f':
        argFlag = 'f'
    elif arg == '-F':
        argFlag = 'F'
    elif arg == '-h':
        printHelp()
    elif arg == '-i':
        argFlag = 'i'
    elif arg == '-l':
        argFlag = 'l'
    elif arg == '-nr':
        fHideRing = 1
        argFlag = None
    elif arg == '-p':
        argFlag = 'p'
    elif arg == '-r':
        argFlag = 'r'
    elif arg == '-s':
        argFlag = 's'
    elif arg == '-S':
        argFlag = 'S'
    elif arg == '-e':
        argFlag = 'e'
    elif argFlag == 'a':
        headAngle = string.atof(arg)
        argFlag = None
    elif argFlag == 'b':
        bgColor = arg
        argFlag = None
    elif argFlag == 'B':
        overrideTexture = 1
        backgroundImage = arg
        argFlag = None
    elif argFlag == 'c':
        ringColor = arg
        argFlag = None
    elif argFlag == 'd':
        outputDirectory = arg
        argFlag = None
    elif argFlag == 'f':
        fov = string.atof(arg)
        argFlag = None
    elif argFlag == 'F':
        fillFactor = string.atof(arg)/100.0
        argFlag = None
    elif argFlag == 'i':
        inputFile = arg
        argFlag = None
    elif argFlag == 'l':
        lookAtTarget = arg
        argFlag = None
    elif argFlag == 'p':
        pitchAngle = string.atof(arg)
        argFlag = None
    elif argFlag == 'r':
        rollAngle = string.atof(arg)
        argFlag = None
    elif argFlag == 's':
        ringScale = string.atof(arg)
        argFlag = None
    elif argFlag == 'e':
        outputExtension = arg
        argFlag = None
    elif argFlag == 'S':
        size = string.atoi(arg)
        argFlag = None
    else:
        argFlag = None

print "Input File: %s" % inputFile
print "Output Directory: %s" % outputDirectory
print "Look Target: %s" % lookAtTarget
print "Head Angle: %f" % headAngle
print "Pitch Angle: %f" % pitchAngle
print "Roll Angle: %f" % rollAngle
print "FOV: %f" % fov
print "FOV Fill Percent: %f" % (fillFactor * 100.0)
print "Background Color: %s" % bgColor
print "Background Image: %s" % backgroundImage
if fHideRing:
    print "No Ring"
else:
    print "Show Ring"
    print "Ring Color: %s" % ringColor
    print "Ring Thickness: %f" % ringScale

ConfigVariableInt('win-size').setStringValue('%d %d' % (size,size))

from direct.directbase.DirectStart import *
from Toon import *
import ToonDNA

frame = render2d.attachNewNode('frame')
base.win.setClearColor(VBase4(0,0,0,0))

topModels = loader.loadModel('models/gui/topToonPictures')

outerFrame = topModels.find('**/topToonPictureFrame').copyTo(frame)
outerFrame.setScale(2 + ringScale)
# output this outer frame so we have a hole in the middle
# to test for
base.graphicsEngine.renderFrame()
outerFrameImg = PNMImage.PNMImage(size,size)
base.win.getScreenshot(outerFrameImg)
outerFrame.setColor(hexToColor(bgColor, alpha = 1))
outerFrame.setBin('fixed', 1)

pictureFrame = topModels.find('**/topToonPictureFrame').copyTo(frame)
pictureFrame.setColor(hexToColor(ringColor))
pictureFrame.setScale(2)
pictureFrame.setBin('fixed', 0)

# Make one more frame layer, this one specially set not to draw to the
# color channels, but to write the inverse alpha channel (so the
# resulting image can have a transparent or semitransparent
# background).
alphaFrame = topModels.find('**/topToonPictureFrame').copyTo(frame)

ts = TextureStage('invertAlpha')
ts.setCombineRgb(TextureStage.CMReplace,
                 TextureStage.CSTexture, TextureStage.COSrcColor)
ts.setCombineAlpha(TextureStage.CMAdd,
                   TextureStage.CSTexture, TextureStage.COOneMinusSrcAlpha,
                   TextureStage.CSPrevious, TextureStage.COSrcAlpha)
tex = alphaFrame.findTexture('*')
alphaFrame.setTextureOff(1)
alphaFrame.setTexture(ts, tex, 1)

alphaFrame.setColor(hexToColor(bgColor))
alphaFrame.setScale(2 + ringScale)    
alphaFrame.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CAlpha))
alphaFrame.setTransparency(TransparencyAttrib.MNone, 1)
alphaFrame.setBin('fixed', 2)

if fHideRing:
    frame.hide()

background = topModels.find('**/topToonBackground')
background.reparentTo(camera)
background.setPos(0,40,-1)
background.setScale(40)
if overrideTexture:
    overrideTexture = Texture()
    overrideTexture.read(Filename(backgroundImage))
    overrideTexture.setMinfilter(Texture.FTLinearMipmapLinear)
    overrideTexture.setMagfilter(Texture.FTLinear)
    background.setTexture(overrideTexture, 1)

# effectiveFOV is the approximate FOV of the ring
effectiveFOV = fov * 0.75

def calcBodyBounds():
    p1,p2 = tt.getTightBounds()
    c = Vec3((p2 + p1)/2.0)
    delta = p2 - p1
    return c, delta[2]

def calcHeadBounds():
    head = tt.getPart('head', '1000')
    headParent = head.getParent()
    # Temporarily reparent head to render to get bounds aligned with render
    head.wrtReparentTo(render)
    # Look for explicitly named ears and stash them
    ears = head.findAllMatches('**/ear*')
    # And stash them before computing bounds
    for ear in ears.asList():
        ear.stash()
    stashed = []
    # If this is a horse and we didn't find any ears,
    # stash nodes with empty string names
    if ears.isEmpty() and (tt.style.head[0] == 'h'):
        # Now stash all unnamed nodes
        for child in head.getChildrenAsList():
            if child.getName() == '':
                stashed.append(child)
                child.stash()
    # Where is center of head in render space?
    p1,p2 = head.getTightBounds()
    # Put all stashed things back
    for ear in ears.asList():
        ear.unstash()
    for child in stashed:
        child.unstash()
    c = Vec3((p2 + p1)/2.0)
    delta = p2 - p1
    # Restore orientation
    head.wrtReparentTo(headParent)
    return c, delta[2]

def lookAtToon():
    if lookAtTarget == 'head':
        c,height = calcHeadBounds()
    else:
        c,height = calcBodyBounds()
    # Move camera there
    camera.setHpr(render, -180, 0, 0)
    camera.setPos(render, c)
    # Move it back to fit around the target
    offset = ((height/2.0)/
              tan(deg2Rad((fillFactor * effectiveFOV)/2.0)))
    camera.setY(camera, -offset)
    
tt = Toon()
dna = ToonDNA.ToonDNA()
dna.newToonRandom(gender = 'f')
tt.setDNA(dna)
tt.reparentTo(render)

base.disableMouse()
base.camLens.setFov(fov,fov)

def convertServerDNAString(serverString):
    # Strip out blank space and take last 30 characters
    serverString = serverString.replace(' ', '')
    stringLen = 30
    serverString = serverString[-stringLen:]
    # Create a datagram from server string
    dg = PyDatagram()
    for i in range(0,len(serverString),2):
        eval('dg.addUint8(0x%s)' % serverString[i:i+2])
    return dg.getMessage()

def updateToon(DNAString):
    dna = ToonDNA.ToonDNA()
    dna.makeFromNetString(convertServerDNAString(DNAString))
    tt.setDNA(dna)
    tt.pose('neutral', 0)
    tt.stopLookAroundNow()
    tt.stopBlink()
    head = tt.getPart('head', '1000')
    head.setHpr(headAngle, pitchAngle, rollAngle)

def snapPics():
    data = getFileData(Filename(inputFile))
    myBgColorAlpha = hexToColor(bgColor)[3]
    for topToonData in data:
        DNAString = topToonData[0].replace(' ', '')
        print DNAString
        updateToon(DNAString)
        base.graphicsEngine.renderFrame()
        lookAtToon()
        base.graphicsEngine.renderFrame()
        imageName = outputDirectory + '/' + DNAString + "." + outputExtension
        print ("Taking screenshot: " + imageName)
        if myBgColorAlpha == 1.0:
            base.win.saveScreenshot(Filename(imageName))
        else:
            myImage = PNMImage.PNMImage(size,size)        
            base.win.getScreenshot(myImage)
            myImage.addAlpha()
            for y in xrange(size):
                for x in xrange(size):
                    isOuterFramePixel = outerFrameImg.getRed(x,y)
                    if isOuterFramePixel:
                        myImage.setAlpha(x,y,myBgColorAlpha)
                    else:
                        myImage.setAlpha(x,y,1)
            print myImage
            myImage.write(Filename(imageName))

snapPics()


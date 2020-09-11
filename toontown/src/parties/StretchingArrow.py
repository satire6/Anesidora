#===============================================================================
# Contact: Carlos Pineda (Schell Games)
# Created: October 2009
#
# Purpose: Arrow widget that stretches from one point to another.
# Used in PartyCogActivity
#===============================================================================
import math

from direct.gui.DirectGui import DirectFrame

from pandac.PandaModules import Point3

class StretchingArrow(DirectFrame):
    """
    Arrow widget that can stretch its body to any specified size.
    """
    notify = directNotify.newCategory("StretchingArrow")
    
    arrowMoving = 0
    arrowBegin = 1
    arrowComplete = 2
    
    body = None
    head = None

    def __init__(self, parent, useColor="blue", autoload=True):
        DirectFrame.__init__(self, parent)
        
        self.useColor = useColor
            
        self.endOffset = 1.5
        self.startOffset = 0.0
        self.shrinkRange = 7.0
        
        #self.distanceDrawn = 0.0
        self.ratioDrawn = 0.0
        
        if autoload:
            self.load()
        
        self.stash()
    
    
    def load(self):
        model = loader.loadModel("phase_13/models/parties/stretchingArrow")
        model.setP(-90)
        
        self.body = model.find("**/arrowBody_" + self.useColor)
        self.body.wrtReparentTo(self)
        
        self.head = model.find("**/arrowHead_" + self.useColor)
        self.head.wrtReparentTo(self)

        model.removeNode()
        
    def unload(self):
        if self.body is not None:
            self.body.removeNode()
            self.body = None
            
        if self.head is not None:
            self.body.removeNode()
            self.body = None
    
    def reset(self):
        self.ratioDrawn = 0.0
    
    def draw(self, fromPoint, toPoint, rotation=0, animate=True):
        arrowlength = 2.72
        # TODO: Review this description. Is it still true?
        """  
        Draws the arrow from fromPoint to toPoint, with the head at the toPoint.  
        The arrow is animated to draw from the start to the finish, fade out and
        start again.  when the animation begins, StretchingArrow.arrowBegin is
        returned.  When it completes, StretchingArrow.arrowComplete is returned.
        At all other times, StretchingArrow.arrowMoving is returned.
        """
        if self.body is None or self.head is None:
            assert(self.notify.debug("draw(): Assets not loaded, therefore cannot draw"))
            return
        
        actualDifference = fromPoint - toPoint
        actualLength = actualDifference.length()
            
        oldRatio = self.ratioDrawn
        # TODO: move this to the constructor so it is only called once.
        #       it is here now to allow for changes at runtime 
        drawSpeed = 1.6
        drawSpeedMin = 0.6
        downTime = 1.0
        fadeOutTime = 0.5
        
        # calculate how fast to draw the arrow
        drawRate = max(drawSpeedMin, drawSpeed * actualLength / arrowlength)
        
        # increment how much of the arrow is drawn
        self.ratioDrawn += globalClock.getDt() / drawRate
        
        # set basic return
        result = StretchingArrow.arrowMoving
        
        # if arrow hits its end, set it back to the downTime
        if self.ratioDrawn >= 1.0:
            result = StretchingArrow.arrowComplete
            self.ratioDrawn = -downTime
        
        # if arrow is starting out
        if cmp(oldRatio,0) != cmp(self.ratioDrawn, 0) and result != StretchingArrow.arrowComplete:
            result = StretchingArrow.arrowBegin
        
        if not animate:
            self.ratioDrawn = 1.0
        
        normal = Point3(actualDifference.getX(), actualDifference.getY(), actualDifference.getZ())
        normal.normalize()
        rotation = math.degrees(math.atan2(actualDifference.getY(), actualDifference.getX()))
        endPoint = toPoint + (normal * self.endOffset)
        startPoint = fromPoint - (normal * self.startOffset)
        newlength = (endPoint - startPoint).length() / arrowlength
        newScale = min(actualLength/self.shrinkRange, 1.0)
        self.head.setScale(newScale)
        
        ratio = max(0.0, self.ratioDrawn)
        if ratio == 0.0:
            ratio = 1.0
        newlength *= ratio
        
        if actualLength < self.endOffset:
            self.stash()
        else:
            self.unstash()
        
        self.body.setPos(startPoint)
        self.body.setH(rotation)
        self.head.setH(rotation -90)
        self.body.setScale(newlength-(0.013*newScale), newScale, newScale)
        
        vec = (startPoint-endPoint)
        vec *= ratio
        self.head.setPos(startPoint - vec)
        self.head.setZ(render, self.body.getZ(render) + 0.001)
        
        # fade out if it is in negative
        if self.ratioDrawn < 0.0:
            self.setAlphaScale((abs(self.ratioDrawn) - (downTime - fadeOutTime)))
        else:
            self.setAlphaScale(1.0)
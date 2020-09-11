from direct.leveleditor.LevelEditorUIBase import *

class LevelEditorUI(LevelEditorUIBase):
    """ Class for Panda3D LevelEditor """ 
    frameWidth = 800
    frameHeight = 600
    appversion      = '1.0'
    appname         = 'OTP Level Editor'
    
    def __init__(self, editor, *args, **kw):
        if not kw.get('size'):
            kw['size'] = wx.Size(self.frameWidth, self.frameHeight)
        LevelEditorUIBase.__init__(self, editor, *args, **kw)       


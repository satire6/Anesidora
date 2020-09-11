"""
Toontown Sign Edit Frame
"""

import wx
from LevelStyleManager import *
from wx.lib.agw.knobctrl import *

class ToonKnobCtrl(KnobCtrl):
      def __init__(self, parent, scale=1, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize):
          KnobCtrl.__init__(self, parent, id, pos, size)

          self._totalVal = 0.0
          self._oldVal = 0.0
          self._scale = scale

      def SetTotal(self, totalVal):
          self._totalVal = totalVal*self._scale

      def SetTrackPosition(self):
          """ Used internally. """

          width, height = self.GetSize()

          x = self._mousePosition.x
          y = self._mousePosition.y

          ang = self.GetAngleFromCoord(x, y)
          val = ang*180.0/math.pi

          deltarange = self._maxvalue - self._minvalue
          deltaangle = self._angleend - self._anglestart

          coeff = float(deltaangle)/float(deltarange)

          if self._anglestart < 0 and val >= 360.0 + self._anglestart:
              scaledval = (val  - (360.0 + self._anglestart))/coeff
          else:
              scaledval = (val  - self._anglestart)/coeff

          diff = val - self._oldVal
          absdiff = abs(diff)
          if absdiff >= 0.0 and absdiff < 180.0:
                self._totalVal = self._totalVal + diff
          elif absdiff >= 180.0 and absdiff < 360.0:
               if 360.0 > 360.0 - diff:
                  self._totalVal = self._totalVal - (360.0 - diff)
               else:
                  self._totalVal = self._totalVal + (360.0 + diff)

          event = KnobCtrlEvent(wxKC_EVENT_ANGLE_CHANGING, self.GetId())
          event.SetEventObject(self)
          event.SetOldValue(self.GetValue())
          event.SetValue(round(self._totalVal/self._scale, 2))

          if self.GetEventHandler().ProcessEvent(event):
              # the caller didn't use event.Skip()
              return

          self.SetValue(scaledval)
          event.SetEventType(wxKC_EVENT_ANGLE_CHANGED)
          event.SetOldValue(scaledval)
          self.GetEventHandler().ProcessEvent(event)

          self._old_ang = ang
          self._oldVal = val

class ToonSignTextCtrlValidator(wx.PyValidator):
      def __init__(self):
          wx.PyValidator.__init__(self)
          
      def Clone(self):
          return ToonSignTextCtrlValidator()
      
      def TransferToWindow(self):
          return True
          
      def TransferFromWindow(self):
          return True

      def Validate(self, win):
          textCtrl = self.GetWindow()
          text = textCtrl.GetValue()
          #print "Validating %s" %(text)
          try:
             #print "Valid %d" %(float(text))
             return True
          except ValueError:
              return False

class ToonSignTextCtrl(wx.TextCtrl):
      def __init__(self, parent, id=-1, value=wx.EmptyString, pos=wx.DefaultPosition):
          wx.TextCtrl.__init__(self, parent.panel, id, pos=pos, value=value, validator=ToonSignTextCtrlValidator())

          self.parent = parent
          self.Bind(wx.EVT_TEXT, self.OnText)
          self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

      def OnText(self, event):
          #print "Got %s" %(self.GetValue())
          try:
             val = float(self.GetValue())
             self.parent.WritePandaValue(self, val)
             self.parent.knobCtrl.SetTotal(val)

          except ValueError:
              #print "Clearing..."
              i=0

      def OnSetFocus(self, event):
          #print "Setting total %d" %(float(self.GetValue()))
          self.parent.knobCtrl.SetTotal(float(self.GetValue()))

class SignEditFrame(wx.MiniFrame):
      def __init__(self, parent, editor, baselineDNA, objNP, hasGraphics=False):
          wx.MiniFrame.__init__(self, parent, -1, 'Sign Text', size=(400, 500), style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT)
          self.panel = wx.Panel(self, -1, size=(400, 500))

          self.editor = editor
          self.baselineDNA = baselineDNA
          self.txtOrig = DNAGetBaselineString(self.baselineDNA)
          self.baselineStyleOrig = DNABaselineStyle()
          self.baselineStyleOrig.copy(self.baselineDNA)
          self.objNP = objNP
          self.scale = 100
          self.hasGraphics = hasGraphics

          self.signTxtStatic = wx.StaticText(self.panel, -1, "Caption", pos=(15, 15))
          self.signTxt =  wx.TextCtrl(self.panel, -1, "", pos=(60, 15), size=(270, 20))

          fontChoices = self.editor.styleManager.getCatalogCodes('font')
          self.fontStatic = wx.StaticText(self.panel, -1, "Font", pos=(15, 45))
          self.fontChoice = wx.ComboBox(self.panel, -1, "", pos=(60, 45), size=(100, 20), choices=fontChoices, style=wx.CB_READONLY)

          self.CapFirstLetterCheck = wx.CheckBox(self.panel, -1, "Capitalize First Letter", pos=(215, 45))
          self.AllCapsCheck = wx.CheckBox(self.panel, -1, "Make All Caps", pos=(215, 65))
          self.DropShadowCheck = wx.CheckBox(self.panel, -1, "Drop Shadow", pos=(215, 85))

          self.topOffset = 90

          self.kernStatic = wx.StaticText(self.panel, -1, "Kern", pos=(15, 15 + self.topOffset))
          self.kernValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 15 + self.topOffset))

          self.wiggleStatic = wx.StaticText(self.panel, -1, "Wiggle", pos=(15, 45 + self.topOffset))
          self.wiggleValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 45 + self.topOffset))

          self.stumbleStatic = wx.StaticText(self.panel, -1, "Stumble", pos=(15, 75 + self.topOffset))
          self.stumbleValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 75 + self.topOffset))

          self.stompStatic = wx.StaticText(self.panel, -1, "Stopm", pos=(15, 105 + self.topOffset))
          self.stompValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 105 + self.topOffset))

          self.curveStatic = wx.StaticText(self.panel, -1, "Curve", pos=(15, 135 + self.topOffset))
          self.curveValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 135 + self.topOffset))

          self.xStatic = wx.StaticText(self.panel, -1, "X", pos=(15, 165 + self.topOffset))
          self.xValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 165 + self.topOffset))

          self.zStatic = wx.StaticText(self.panel, -1, "Z", pos=(15, 195 + self.topOffset))
          self.zValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 195 + self.topOffset))

          self.xScaleStatic = wx.StaticText(self.panel, -1, "Scale X", pos=(15, 225 + self.topOffset))
          self.xScaleValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 225 + self.topOffset))

          self.zScaleStatic = wx.StaticText(self.panel, -1, "Scale Z", pos=(15, 255 + self.topOffset))
          self.zScaleValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 255 + self.topOffset))

          self.rollStatic = wx.StaticText(self.panel, -1, "Roll", pos=(15, 285 + self.topOffset))
          self.rollValue =  ToonSignTextCtrl(self, -1, "0", pos=(60, 285 + self.topOffset))

          self.revertAllButton = wx.Button(self.panel, -1, "Revert All", pos=(60, 315 + self.topOffset), size=(100, 20))

          #self.tmpValue =  FloatSpin(self.panel, -1, pos=(15, 315 + self.topOffset))
          #self.tmpSpinButton = wx.SpinButton(self.panel, -1, pos=(120, 315 + self.topOffset), size=(20, 20), style=wx.SP_VERTICAL)

          if self.hasGraphics:
             self.signTxt.Enable(False)
             self.fontChoice.Enable(False)
             self.CapFirstLetterCheck.Enable(False)
             self.AllCapsCheck.Enable(False)
             self.DropShadowCheck.Enable(False)
             self.kernValue.Enable(False)
             self.wiggleValue.Enable(False)
             self.stumbleValue.Enable(False)
             self.stompValue.Enable(False)
             self.curveValue.Enable(False)

          self.knobCtrl = ToonKnobCtrl(self.panel, scale=self.scale, pos=(200, 80 + self.topOffset), size=(150, 150))
          self.knobCtrl.SetKnobRadius(6.0)
          self.knobCtrl.SetAngularRange(0.0, 360.0)

          self.ReadPandaValues(self.baselineDNA)

          self.Bind(KC_EVENT_ANGLE_CHANGED, self.OnKnobAngleChanged, self.knobCtrl)
          self.Bind(wx.EVT_TEXT, self.OnSignText, self.signTxt)
          self.Bind(wx.EVT_COMBOBOX, self.OnFontChoice, self.fontChoice)
          self.Bind(wx.EVT_BUTTON, self.OnRevertAll, self.revertAllButton)
          self.Bind(wx.EVT_CHECKBOX, self.OnCapFirstLetterCheck, self.CapFirstLetterCheck)
          self.Bind(wx.EVT_CHECKBOX, self.OnAllCapsCheck, self.AllCapsCheck)
          self.Bind(wx.EVT_CHECKBOX, self.OnDropShadowCheck, self.DropShadowCheck)
#          self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
#          self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
          self.Bind(wx.EVT_SHOW, self.OnShowWindow)
#          self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

      def OnKnobAngleChanged(self, event):
          val = event.GetValue()
          window = self.FindFocus()
          if isinstance(window, ToonSignTextCtrl):
             self.WritePandaValue(window, val)
             window.SetValue(str(val))

      def ReadPandaValues(self, baseline):
          self.signTxt.SetValue(self.txtOrig)
          self.fontChoice.SetValue(baseline.getCode())
          self.kernValue.SetValue(str(round(baseline.getKern(), 2)))
          self.wiggleValue.SetValue(str(round(baseline.getWiggle(), 2)))
          self.stumbleValue.SetValue(str(round(baseline.getStumble(), 2)))
          self.stompValue.SetValue(str(round(baseline.getStomp(), 2)))

          width = baseline.getWidth()
          if width:
              curve = 1.0/width
          else:
              curve = 0.0
          self.curveValue.SetValue(str(round(curve, 2)))

          pos = baseline.getPos()
          self.xValue.SetValue(str(round(pos[0], 2)))
          self.zValue.SetValue(str(round(pos[2], 2)))

          scale = baseline.getScale()
          self.xScaleValue.SetValue(str(round(scale[0], 2)))
          self.zScaleValue.SetValue(str(round(scale[2], 2)))

          hpr = baseline.getHpr()
          self.rollValue.SetValue(str(round(hpr[2], 2)))

          flags = baseline.getFlags()
          if 'b' in flags:
             self.CapFirstLetterCheck.SetValue(True)
          else:
             self.CapFirstLetterCheck.SetValue(False)

          if 'c' in flags:
             self.AllCapsCheck.SetValue(True)
          else:
             self.AllCapsCheck.SetValue(False)

          if 'd' in flags:
             self.DropShadowCheck.SetValue(True)
          else:
             self.DropShadowCheck.SetValue(False)

          color = baseline.getColor()
          #TODO: implement color picker ansd set color

      def WritePandaValue(self, window, val):
          if window == self.kernValue:
            self.SetSignBaselineKern(val)
          elif window == self.wiggleValue:
            self.SetSignBaselineWiggle(val)
          elif window == self.stumbleValue:
            self.SetSignBaselineStumble(val)
          elif window == self.stompValue:
            self.SetSignBaselineStomp(val)
          elif window == self.curveValue:
            self.SetSignBaselineCurve(val)
          elif window == self.xValue:
            self.SetSignBaselineX(val)
          elif window == self.zValue:
            self.SetSignBaselineZ(val)
          elif window == self.xScaleValue:
            self.SetSignBaselineScaleX(val)
          elif window == self.zScaleValue:
            self.SetSignBaselineScaleZ(val)
          elif window == self.rollValue:
            self.SetSignBaselineRoll(val)

      def SetSignBaselineText(self, val):
          if self.baselineDNA:
             if self.hasGraphics == False:
                DNASetBaselineString(self.baselineDNA, val)
                self.objNP.replace()

      def SetSignBaselineFont(self, val):
          if self.baselineDNA:
             self.baselineDNA.setCode(val)
             self.objNP.replace()

      def SetSignBaselineKern(self, val):
          if self.baselineDNA:
             self.baselineDNA.setKern(val)
             self.objNP.replace()

      def SetSignBaselineWiggle(self, val):
          if self.baselineDNA:
             self.baselineDNA.setWiggle(val)
             self.objNP.replace()

      def SetSignBaselineStumble(self, val):
          if self.baselineDNA:
             self.baselineDNA.setStumble(val)
             self.objNP.replace()

      def SetSignBaselineStomp(self, val):
          if self.baselineDNA:
             self.baselineDNA.setStomp(val)
             self.objNP.replace()

      def SetSignBaselineCurve(self, val):
          if self.baselineDNA:
             try:
                val=1.0/val
             except ZeroDivisionError:
                val=0.0
             self.baselineDNA.setWidth(val)
             self.baselineDNA.setHeight(val)
             self.objNP.replace()

      def SetSignBaselineX(self, val):
          if self.baselineDNA:
             pos=self.baselineDNA.getPos()
             pos=VBase3(val, pos[1], pos[2])
             self.baselineDNA.setPos(pos)
             self.objNP.replace()

      def SetSignBaselineZ(self, val):
          if self.baselineDNA:
             pos=self.baselineDNA.getPos()
             pos=VBase3(pos[0], pos[1], val)
             self.baselineDNA.setPos(pos)
             self.objNP.replace()

      def SetSignBaselineScaleX(self, val):
          if self.baselineDNA:
             scale=self.baselineDNA.getScale()
             scale=VBase3(val, scale[1], scale[2])
             self.baselineDNA.setScale(scale)
             self.objNP.replace()

      def SetSignBaselineScaleZ(self, val):
          if self.baselineDNA:
             scale=self.baselineDNA.getScale()
             scale=VBase3(scale[0], scale[1], val)
             self.baselineDNA.setScale(scale)
             self.objNP.replace()

      def SetSignBaselineRoll(self, val):
          if self.baselineDNA:
             hpr=self.baselineDNA.getHpr()
             hpr=VBase3(hpr[0], hpr[1], val)
             self.baselineDNA.setHpr(hpr)
             self.objNP.replace()

      def SetSignBaselineColor(self, var):
          if self.baselineDNA:
             self.baselineDNA.setColor(var)
             self.objNP.replace()

      def SetSignBaselineFlag(self, flagChar):
          if self.baselineDNA:
             flags = self.baselineDNA.getFlags()
             if not flagChar in flags:
                # Add the flag:
                self.baselineDNA.setFlags(flags+flagChar)
             elif flagChar in flags:
                # Remove the flag:
                flags=string.join(flags.split(flagChar), '')
                self.baselineDNA.setFlags(flags)
             self.objNP.replace()

      def OnSignText(self, event):
          self.SetSignBaselineText(self.signTxt.GetValue())

      def OnFontChoice(self, event):
          self.SetSignBaselineFont(self.fontChoice.GetValue())

      def OnCapFirstLetterCheck(self, event):
          self.SetSignBaselineFlag('b')

      def OnAllCapsCheck(self, event):
          self.SetSignBaselineFlag('c')

      def OnDropShadowCheck(self, event):
          self.SetSignBaselineFlag('d')

      def OnRevertAll(self, event):
          self.baselineStyleOrig.copyTo(self.baselineDNA)
          self.ReadPandaValues(self.baselineDNA)

      def OnSetFocus(self, event):
          self.editor.ui.bindKeyEvents(False)

      def OnShowWindow(self, event):
          self.editor.ui.bindKeyEvents(False)

      def OnCloseWindow(self, event):
          self.editor.ui.bindKeyEvents(True)

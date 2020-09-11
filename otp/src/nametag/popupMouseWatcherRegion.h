// Filename: popupMouseWatcherRegion.h
// Created by:  drose (20Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef POPUPMOUSEWATCHERREGION_H
#define POPUPMOUSEWATCHERREGION_H

#include "otpbase.h"

#include "mouseWatcherRegion.h"

class ClickablePopup;

////////////////////////////////////////////////////////////////////
//       Class : PopupMouseWatcherRegion
// Description : This is a specialization on MouseWatcherRegion, to
//               tie it back to its associated ClickablePopup.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP PopupMouseWatcherRegion : public MouseWatcherRegion {
public:
  PopupMouseWatcherRegion(ClickablePopup *popup, const string &name,
                          const LVecBase4f &frame);
  virtual ~PopupMouseWatcherRegion();

  virtual void enter_region(const MouseWatcherParameter &param);
  virtual void exit_region(const MouseWatcherParameter &param);
  virtual void press(const MouseWatcherParameter &param);
  virtual void release(const MouseWatcherParameter &param);

private:
  ClickablePopup *_popup;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    MouseWatcherRegion::init_type();
    register_type(_type_handle, "PopupMouseWatcherRegion",
                  MouseWatcherRegion::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "popupMouseWatcherRegion.I"

#endif

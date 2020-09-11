// Filename: clickablePopup.h
// Created by:  drose (14Jun02)
//
////////////////////////////////////////////////////////////////////

#ifndef CLICKABLEPOPUP_H
#define CLICKABLEPOPUP_H

#include "otpbase.h"
#include "popupMouseWatcherRegion.h"

#include "referenceCount.h"
#include "pointerTo.h"
#include "pgButton.h"
#include "updateSeq.h"
#include "nodePath.h"

class MouseWatcherParameter;
class MarginManager;

////////////////////////////////////////////////////////////////////
//       Class : ClickablePopup
// Description : An abstract base class defining the interface to
//               something other than a GUI button that appears
//               onscreen and may be clicked on with the mouse.  This
//               includes 2-d nametags, 3-d nametags, and margin
//               messages like whispers.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP ClickablePopup {
public:
  ClickablePopup();
  virtual ~ClickablePopup();

public:
  virtual void enter_region(const MouseWatcherParameter &param);
  virtual void exit_region(const MouseWatcherParameter &param);
  virtual void press(const MouseWatcherParameter &param);
  virtual void release(const MouseWatcherParameter &param);
  virtual void click();

  virtual void set_state(PGButton::State state);
  virtual PGButton::State get_state() const;

protected:
  virtual void update_contents();

protected:
  PGButton::State _state;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    register_type(_type_handle, "ClickablePopup");
  }

PUBLISHED:
  // We define get_type() even though we don't inherit from
  // TypedObject.  We can't actually inherit from TypedObject because
  // of the whole multiple-inheritance thing in our derived classes.
  virtual TypeHandle get_type() const {
    return get_class_type();
  }

private:
  static TypeHandle _type_handle;
};

#include "clickablePopup.I"

#endif

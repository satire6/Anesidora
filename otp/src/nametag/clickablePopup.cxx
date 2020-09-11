// Filename: clickablePopup.cxx
// Created by:  drose (14Jun02)
//
////////////////////////////////////////////////////////////////////

#include "clickablePopup.h"
#include "nametagGlobals.h"
#include "popupMouseWatcherRegion.h"

#include "audioSound.h"
#include "mouseWatcherParameter.h"
#include "mouseButton.h"

TypeHandle ClickablePopup::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
ClickablePopup::
ClickablePopup() {
  _state = PGButton::S_ready;
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
ClickablePopup::
~ClickablePopup() {
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::enter_region
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever the
//               mouse enters the region.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
enter_region(const MouseWatcherParameter &) {
  AudioSound *sound = NametagGlobals::get_rollover_sound();
  if (sound != (AudioSound *)NULL) {
    sound->play();
  }
  set_state(PGButton::S_rollover);
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::exit_region
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever the
//               mouse exits the region.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
exit_region(const MouseWatcherParameter &) {
  set_state(PGButton::S_ready);
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::press
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button is depressed while the mouse
//               is within the region.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
press(const MouseWatcherParameter &param) {
  if (param.get_button() == MouseButton::one()) {
    AudioSound *sound = NametagGlobals::get_click_sound();
    if (sound != (AudioSound *)NULL) {
      sound->play();
    }
    set_state(PGButton::S_depressed);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::release
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button previously depressed with
//               press() is released.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
release(const MouseWatcherParameter &param) {
  if (param.get_button() == MouseButton::one()) {
    if (param.is_outside()) {
      // If the mouse was outside the region when we released, then
      // never mind.
      set_state(PGButton::S_ready);

    } else {
      // If the mouse was within the region when we released, this
      // is considered a "click".
      set_state(PGButton::S_rollover);
      click();
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::click
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button previously depressed with
//               press() is released.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
click() {
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::set_state
//       Access: Public, Virtual
//  Description: Changes the visual appearance of the ClickablePopup in
//               respect to the mouse.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
set_state(PGButton::State state) {
  if (_state != state) {
    _state = state;
    update_contents();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::get_state
//       Access: Public, Virtual
//  Description: Returns the current visual state of this ClickablePopup,
//               with respect to the mouse.
////////////////////////////////////////////////////////////////////
PGButton::State ClickablePopup::
get_state() const {
  return _state;
}

////////////////////////////////////////////////////////////////////
//     Function: ClickablePopup::update_contents
//       Access: Protected, Virtual
//  Description: Recomputes the ClickablePopup according to its
//               ClickablePopupGroup's current state.
////////////////////////////////////////////////////////////////////
void ClickablePopup::
update_contents() {
}

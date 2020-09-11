// Filename: popupMouseWatcherRegion.cxx
// Created by:  drose (20Jul01)
//
////////////////////////////////////////////////////////////////////

#include "popupMouseWatcherRegion.h"
#include "clickablePopup.h"

TypeHandle PopupMouseWatcherRegion::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: PopupMouseWatcherRegion::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
PopupMouseWatcherRegion::
PopupMouseWatcherRegion(ClickablePopup *popup, const string &name,
                        const LVecBase4f &frame) :
  MouseWatcherRegion(name, frame),
  _popup(popup)
{
  set_active(true);
}

////////////////////////////////////////////////////////////////////
//     Function: PopupMouseWatcherRegion::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
PopupMouseWatcherRegion::
~PopupMouseWatcherRegion() {
}


////////////////////////////////////////////////////////////////////
//     Function: PopupMouseWatcherRegion::enter_region
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever the
//               mouse enters the region.
////////////////////////////////////////////////////////////////////
void PopupMouseWatcherRegion::
enter_region(const MouseWatcherParameter &param) {
  if (_popup != (ClickablePopup *)NULL) {
    _popup->enter_region(param);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PopupMouseWatcherRegion::exit_region
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever the
//               mouse exits the region.
////////////////////////////////////////////////////////////////////
void PopupMouseWatcherRegion::
exit_region(const MouseWatcherParameter &param) {
  if (_popup != (ClickablePopup *)NULL) {
    _popup->exit_region(param);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PopupMouseWatcherRegion::press
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button is depressed while the mouse
//               is within the region.
////////////////////////////////////////////////////////////////////
void PopupMouseWatcherRegion::
press(const MouseWatcherParameter &param) {
  if (_popup != (ClickablePopup *)NULL) {
    _popup->press(param);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PopupMouseWatcherRegion::release
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button previously depressed with
//               press() is released.
////////////////////////////////////////////////////////////////////
void PopupMouseWatcherRegion::
release(const MouseWatcherParameter &param) {
  if (_popup != (ClickablePopup *)NULL) {
    _popup->release(param);
  }
}

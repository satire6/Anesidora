// Filename: marginPopup.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "marginPopup.h"
#include "nametagGlobals.h"

TypeHandle MarginPopup::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
MarginPopup::
MarginPopup() : PandaNode("") {
  _managed = false;
  _visible = false;
  _cell_width = 1.0f;
  _master_margin_prop_seq = NametagGlobals::margin_prop_seq;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
MarginPopup::
~MarginPopup() {
  // We'd better be no longer managed or visible by the time we
  // destruct.
  nassertv(!_managed && !_visible);
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::get_score
//       Access: Public, Virtual
//  Description: Returns a number representing how much this
//               particular MarginPopup deserves to be onscreen.
//               This is used to resolve conflicts when there are too
//               many MarginPopups that all want to be onscreen
//               simultaneously.  The larger the number, the more
//               likely this particular popup is to be made visible.
////////////////////////////////////////////////////////////////////
float MarginPopup::
get_score() {
  return 0.0f;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::get_object_code
//       Access: Public, Virtual
//  Description: Returns an integer that represents a uniquifying code
//               for this popup.  If the code is nonzero, then of any
//               two popups that are simultaneously onscreen and share
//               the same unique code, only the one with the highest
//               score will actually be shown.  This is intended to
//               prevent display of multiple nametags that refer to
//               the same object.
////////////////////////////////////////////////////////////////////
int MarginPopup::
get_object_code() {
  return 0;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::update_contents
//       Access: Protected, Virtual
//  Description: Recomputes the MarginPopup according to possible
//               changes in the global state.
////////////////////////////////////////////////////////////////////
void MarginPopup::
update_contents() {
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::frame_callback
//       Access: Protected, Virtual
//  Description: This is called exactly once every frame by the
//               MarginManager for each managed popup, whether the
//               popup is visible or not.  It does whatever the popup
//               might need to do once per frame.
////////////////////////////////////////////////////////////////////
void MarginPopup::
frame_callback() {
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::consider_manage
//       Access: Protected, Virtual
//  Description: This is called once a frame by the
//               MarginManager to query whether the MarginPopup
//               believes it should continue to be managed.  If it
//               returns false, the popup will be removed from the
//               list of managed popups.
////////////////////////////////////////////////////////////////////
bool MarginPopup::
consider_manage() {
  // By default, a MarginPopup always wants to be managed.
  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::consider_visible
//       Access: Protected, Virtual
//  Description: This is called once a frame by the
//               MarginManager to query whether the MarginPopup
//               believes it should be made visible.  If it returns
//               true, the popup will be made visible; otherwise, it
//               will be made invisible.
////////////////////////////////////////////////////////////////////
bool MarginPopup::
consider_visible() {
  // Make sure that no important properties have changed.
  if (_master_margin_prop_seq != NametagGlobals::margin_prop_seq) {
    _master_margin_prop_seq = NametagGlobals::margin_prop_seq;
    update_contents();
  }

  // By default, a MarginPopup always wants to be visible.
  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::set_managed
//       Access: Protected, Virtual
//  Description: This is called only by the MarginManager to
//               change the state of the is_managed() flag.  It
//               provides a hook for the MarginPopup to do something
//               special about it at that moment, if necessary.
////////////////////////////////////////////////////////////////////
void MarginPopup::
set_managed(bool flag) {
  _managed = flag;

  // While we are managed, we keep _this_np set, and we clear it while
  // we are not managed.  This helps prevent leakage due to excessive
  // self-reference-counting.
  if (_managed) {
    _this_np = NodePath(this);
  } else {
    _this_np = NodePath();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::set_visible
//       Access: Protected, Virtual
//  Description: This is called only by the MarginManager to
//               change the state of the is_visible() flag.  It
//               provides a hook for the MarginPopup to do something
//               special about it at that moment, if necessary.
////////////////////////////////////////////////////////////////////
void MarginPopup::
set_visible(bool flag) {
  _visible = flag;
}

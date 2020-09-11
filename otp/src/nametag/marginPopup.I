// Filename: marginPopup.I
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::is_managed
//       Access: Published
//  Description: Returns true if this popup is currently managed
//               (that is, available to be made visible), or false if
//               it is not managed (it will never be visible).
////////////////////////////////////////////////////////////////////
INLINE bool MarginPopup::
is_managed() const {
  return _managed;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::is_visible
//       Access: Published
//  Description: Returns true if this popup is currently visible
//               or false if it is invisible (which may mean that it
//               is managed, but not visible).
////////////////////////////////////////////////////////////////////
INLINE bool MarginPopup::
is_visible() const {
  return _visible;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginPopup::get_cell_width
//       Access: Public
//  Description: Returns the width of the cell into which the popup has
//               been assigned, in its own coordinate space.
////////////////////////////////////////////////////////////////////
INLINE float MarginPopup::
get_cell_width() const {
  return _cell_width;
}

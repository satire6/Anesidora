// Filename: marginManager.I
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: MarginManager::PopupInfo::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE MarginManager::PopupInfo::
PopupInfo() {
  _cell_index = -1;
  _wants_visible = false;
  _score = 0.0f;
  _code = 0;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::SortPopupsByScore::Function operator
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool MarginManager::SortPopupsByScore::
operator () (Popups::iterator i1, Popups::iterator i2) const {
  return (*i2).second._score < (*i1).second._score;
}

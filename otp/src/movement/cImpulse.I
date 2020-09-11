// Filename: cImpulse.I
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::get_mover
//       Access: Published
//  Description: Returns pointer to mover obj that we're attached to;
//               may be 0.
////////////////////////////////////////////////////////////////////
INLINE CMover *CImpulse::
get_mover() const {
  return _mover;
}

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::get_node_path
//       Access: Published
//  Description: Returns NodePath that our mover is moving around.
////////////////////////////////////////////////////////////////////
INLINE NodePath CImpulse::
get_node_path() const {
  return _node_path;
}

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::is_cpp
//       Access: Published
//  Description: Indicates the state the interval believes it is in:
//               whether it has been started, is currently in the
//               middle, or has been finalized.
////////////////////////////////////////////////////////////////////
INLINE bool CImpulse::
is_cpp() const {
  return true;
}

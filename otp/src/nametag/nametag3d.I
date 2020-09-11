// Filename: nametag3d.I
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::set_billboard_offset
//       Access: Published
//  Description: Sets the offset distance by which the Nametag is slid
//               towards the camera after billboarding.  This is used
//               to help the Nametag not be obscured by the avatar.
//
//               The default value is set in NametagGlobals, but this
//               may be overridden at runtime.
////////////////////////////////////////////////////////////////////
INLINE void Nametag3d::
set_billboard_offset(float billboard_offset) {
  _billboard_offset = billboard_offset;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::get_billboard_offset
//       Access: Published
//  Description: Returns the offset distance by which the Nametag is
//               slid towards the camera after billboarding.  See
//               set_billboard_offset().
////////////////////////////////////////////////////////////////////
INLINE float Nametag3d::
get_billboard_offset() const {
  return _billboard_offset;
}

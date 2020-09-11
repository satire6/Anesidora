// Filename: suitLegList.I
// Created by:  drose (08Nov01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::Indexing Operator
//       Access: Published
//  Description: Returns the nth leg of the list.
////////////////////////////////////////////////////////////////////
INLINE const SuitLeg &SuitLegList::
operator [] (int n) const {
  return get_leg(n);
}


////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_type
//       Access: Published
//  Description: Returns the type of this leg.  Most legs are of type
//               T_bellicose, which corresponds to just plain walking
//               down the street, but other legs particularly at both
//               ends of the path may represent other modes.
////////////////////////////////////////////////////////////////////
INLINE SuitLeg::Type SuitLegList::
get_type(int n) const {
  return get_leg(n).get_type();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_start_time
//       Access: Published
//  Description: Returns the time (in seconds elapsed since the
//               beginning of the path) at which this leg begins.
////////////////////////////////////////////////////////////////////
INLINE double SuitLegList::
get_start_time(int n) const {
  return get_leg(n).get_start_time();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_leg_time
//       Access: Published
//  Description: Returns the total length of time, in seconds, which
//               this leg represents.
////////////////////////////////////////////////////////////////////
INLINE double SuitLegList::
get_leg_time(int n) const {
  return get_leg(n).get_leg_time();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_zone_id
//       Access: Published
//  Description: Returns the Zone ID associated with this leg.
////////////////////////////////////////////////////////////////////
INLINE int SuitLegList::
get_zone_id(int n) const {
  return get_leg(n).get_zone_id();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_block_number
//       Access: Published
//  Description: Returns the block number associated with this leg, if
//               any.  Normally this is only relevant for CogHQ door
//               type legs, in which it represents the particular door
//               index we're going through.
////////////////////////////////////////////////////////////////////
INLINE int SuitLegList::
get_block_number(int n) const {
  return get_leg(n).get_block_number();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_point_a
//       Access: Published
//  Description: Returns the first DNASuitPoint associated with this
//               leg.  In most cases, the leg represents the path
//               between point A and point B.
////////////////////////////////////////////////////////////////////
INLINE int SuitLegList::
get_point_a(int n) const {
  return get_leg(n).get_point_a();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_point_b
//       Access: Published
//  Description: Returns the first DNASuitPoint associated with this
//               leg.  In most cases, the leg represents the path
//               between point A and point B.
////////////////////////////////////////////////////////////////////
INLINE int SuitLegList::
get_point_b(int n) const {
  return get_leg(n).get_point_b();
}

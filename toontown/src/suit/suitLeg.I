// Filename: suitLeg.I
// Created by:  drose (08Nov01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_type
//       Access: Published
//  Description: Returns the type of this leg.  Most legs are of type
//               T_bellicose, which corresponds to just plain walking
//               down the street, but other legs particularly at both
//               ends of the path may represent other modes.
////////////////////////////////////////////////////////////////////
INLINE SuitLeg::Type SuitLeg::
get_type() const {
  return _type;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_start_time
//       Access: Published
//  Description: Returns the time (in seconds elapsed since the
//               beginning of the path) at which this leg begins.
////////////////////////////////////////////////////////////////////
INLINE double SuitLeg::
get_start_time() const {
  return _start_time;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_leg_time
//       Access: Published
//  Description: Returns the total length of time, in seconds, which
//               this leg represents.
////////////////////////////////////////////////////////////////////
INLINE double SuitLeg::
get_leg_time() const {
  return _leg_time;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_zone_id
//       Access: Published
//  Description: Returns the Zone ID associated with this leg.
////////////////////////////////////////////////////////////////////
INLINE int SuitLeg::
get_zone_id() const {
  return _zone_id;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_block_number
//       Access: Published
//  Description: Returns the block number associated with this leg, if
//               any.  Normally this is only relevant for CogHQ door
//               type legs, in which it represents the particular door
//               index we're going through.
////////////////////////////////////////////////////////////////////
INLINE int SuitLeg::
get_block_number() const {
  return _block_number;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_point_a
//       Access: Published
//  Description: Returns the first DNASuitPoint associated with this
//               leg.  In most cases, the leg represents the path
//               between point A and point B.
////////////////////////////////////////////////////////////////////
INLINE int SuitLeg::
get_point_a() const {
  return _point_a;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_point_b
//       Access: Published
//  Description: Returns the second DNASuitPoint associated with this
//               leg.  In most cases, the leg represents the path
//               between point A and point B.
////////////////////////////////////////////////////////////////////
INLINE int SuitLeg::
get_point_b() const {
  return _point_b;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_pos_a
//       Access: Published
//  Description: Returns the point in space associated with point A.
////////////////////////////////////////////////////////////////////
INLINE LPoint3f SuitLeg::
get_pos_a() const {
  return _pos_a;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_pos_b
//       Access: Published
//  Description: Returns the point in space associated with point B.
////////////////////////////////////////////////////////////////////
INLINE LPoint3f SuitLeg::
get_pos_b() const {
  return _pos_b;
}

INLINE ostream &
operator << (ostream &out, const SuitLeg &leg) {
  leg.output(out);
  return out;
}

INLINE ostream &operator << (ostream &out, SuitLeg::Type type) {
  return out << SuitLeg::get_type_name(type);
}

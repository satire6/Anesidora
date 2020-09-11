// Filename: suitLeg.cxx
// Created by:  drose (08Nov01)
//
////////////////////////////////////////////////////////////////////

#include "suitLeg.h"

#include "dnaSuitPoint.h"

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
SuitLeg::
SuitLeg(Type type, double start_time, double leg_time, int zone_id,
        int block_number,
        const DNASuitPoint *point_a, const DNASuitPoint *point_b) :
  _type(type),
  _start_time(start_time),
  _leg_time(leg_time),
  _zone_id(zone_id),
  _block_number(block_number),
  _point_a(point_a->get_index()),
  _point_b(point_b->get_index()),
  _pos_a(point_a->get_pos()),
  _pos_b(point_b->get_pos())
{
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_pos_at_time
//       Access: Published
//  Description: Returns the expected position of the suit at the
//               indicated time, in seconds elapsed since the start of
//               this leg.
////////////////////////////////////////////////////////////////////
LPoint3f SuitLeg::
get_pos_at_time(double time) const {
  switch (_type) {
  case T_walk_from_street:
  case T_walk_to_street:
  case T_walk:
    break;

  case T_from_sky:
    return _pos_a;

  case T_to_sky:
    return _pos_b;

  case T_from_suit_building:
    return _pos_a;

  case T_to_suit_building:
    return _pos_b;

  case T_to_toon_building:
    return _pos_b;

  case T_from_coghq:
    return _pos_a;

  case T_to_coghq:
    return _pos_b;

  case T_off:
    return _pos_b;
  }

  if (time < 0.0) {
    return _pos_a;
  } else if (time > _leg_time) {
    return _pos_b;
  } else {
    return _pos_a + (time / _leg_time) * (_pos_b - _pos_a);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::get_type_name
//       Access: Published, Static
//  Description: Returns the string name associated with the indicated
//               type.  This is also the name that corresponds to a
//               state in DistributedSuit.
////////////////////////////////////////////////////////////////////
string SuitLeg::
get_type_name(SuitLeg::Type type) {
  switch (type) {
  case T_walk_from_street:
    return "WalkFromStreet";

  case T_walk_to_street:
    return "WalkToStreet";

  case T_walk:
    return "Walk";

  case T_from_sky:
    return "FromSky";

  case T_to_sky:
    return "ToSky";

  case T_from_suit_building:
    return "FromSuitBuilding";

  case T_to_suit_building:
    return "ToSuitBuilding";

  case T_to_toon_building:
    return "ToToonBuilding";

  case T_from_coghq:
    return "FromCogHQ";

  case T_to_coghq:
    return "ToCogHQ";

  case T_off:
    return "Off";
  }

  return "**invalid**";
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLeg::output
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
void SuitLeg::
output(ostream &out) const {
  out << "(" << _type << ", " << _start_time << " (" << _leg_time
      << "), " << _zone_id << ", " << _point_a << ", "
      << _point_b << ")";
}



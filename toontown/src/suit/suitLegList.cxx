// Filename: suitLegList.cxx
// Created by:  drose (08Nov01)
//
////////////////////////////////////////////////////////////////////

#include "suitLegList.h"

#include "dnaStorage.h"
#include "dnaSuitPoint.h"
#include "string_utils.h"

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::Constructor
//       Access: Published
//  Description: Fills up the list with the SuitLeg objects that
//               reflect the indicated DNASuitPath.
//
//               The path is just a set of DNA points along the
//               street; the legs define the actual timings and states
//               for walking between those points.
//
//               We define one leg for each pair of points, plus an
//               additional leg at the beginning and end of the path
//               for transitioning in and out.  Finally, there is one
//               additional "leg" at the end of the whole sequence,
//               which marks the removal of the Suit.
//
//               The last five parameters are the lengths of time, in
//               seconds, we should allow for each of the
//               corresponding transitions.
////////////////////////////////////////////////////////////////////
SuitLegList::
SuitLegList(const DNASuitPath *path, const DNAStorage &storage,
            double suit_walk_speed,
            double from_sky_time,
            double to_sky_time,
            double from_suit_building_time,
            double to_suit_building_time,
            double to_toon_building_time) {
  nassertv(path->get_num_points() > 0);

  int i = 0;
  int pi = path->get_point_index(i);
  DNASuitPoint *point = storage.get_suit_point_with_index(pi);

  int next_pi = path->get_point_index(i + 1);
  DNASuitPoint *next_point = storage.get_suit_point_with_index(next_pi);

  SuitLeg::Type type = get_first_leg_type(point);
  double time = 0.0;
  int zone_id = 0;

  double leg_time;
  switch (type) {
  case SuitLeg::T_from_sky:
    leg_time = from_sky_time;
    break;

  case SuitLeg::T_from_suit_building:
    leg_time = from_suit_building_time;
    break;

  default:
    leg_time = 0.0;
    break;
  }

  _legs.clear();
  // We expect to have one leg for each pair of points, plus three extras.
  int expected_num_legs = path->get_num_points() - 1 + 3;
  _legs.reserve(expected_num_legs);

  // First, record the first leg.  This transitions the suit onstage.
  _legs.push_back(SuitLeg(type, time, leg_time, zone_id, 0, point, next_point));
  time += leg_time;

  // Now record the subsequent legs.  We make one of these for
  // each pair of points.
  i++;
  while (i < path->get_num_points()) {
    next_pi = path->get_point_index(i);
    next_point = storage.get_suit_point_with_index(next_pi);
    zone_id = get_zone_id(storage, pi, next_pi);

    if (point->get_point_type() == DNASuitPoint::COGHQ_OUT_POINT) {
      // A special case: if we're about to walk out of a CogHQ door,
      // insert a new leg to open the door.
      type = SuitLeg::T_from_coghq;
      leg_time = from_suit_building_time;
      _legs.push_back(SuitLeg(type, time, leg_time, zone_id,
                              point->get_landmark_building_index(),
                              point, point));
      time += leg_time;
    }

    type = get_next_leg_type(point, next_point);
    leg_time = storage.get_suit_edge_travel_time(pi, next_pi, suit_walk_speed);

    _legs.push_back(SuitLeg(type, time, leg_time, zone_id, 
                            0, point, next_point));
    time += leg_time;

    if (next_point->get_point_type() == DNASuitPoint::COGHQ_IN_POINT) {
      // A special case: if we just walked into a CogHQ door, insert a
      // new leg to open the door.
      type = SuitLeg::T_to_coghq;
      leg_time = to_suit_building_time;
      _legs.push_back(SuitLeg(type, time, leg_time, zone_id,
                              next_point->get_landmark_building_index(),
                              next_point, next_point));
      time += leg_time;
    }

    point = next_point;
    pi = next_pi;
    i++;
  }

  // Now record the last leg, to transition the suit offstage.
  type = get_last_leg_type(point);
  switch (type) {
  case SuitLeg::T_to_sky:
    leg_time = to_sky_time;
    break;

  case SuitLeg::T_to_suit_building:
    leg_time = to_suit_building_time;
    break;

  case SuitLeg::T_to_toon_building:
    leg_time = to_toon_building_time;
    break;

  default:
    leg_time = 0.0;
  }

  // Back up and get the penultimate point again.
  pi = path->get_point_index(i - 2);
  point = storage.get_suit_point_with_index(pi);

  _legs.push_back(SuitLeg(type, time, leg_time, zone_id, 0, point, next_point));

  // And one more to remove the suit.
  time += leg_time;
  _legs.push_back(SuitLeg(SuitLeg::T_off, time, 0.0, zone_id, 0, point, next_point));

  // Also, extend the zoneId backwards from the 1 element to the
  // 0 element.
  _legs[0]._zone_id = _legs[1]._zone_id;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::Destructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
SuitLegList::
~SuitLegList() {
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_num_legs
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
int SuitLegList::
get_num_legs() const {
  return _legs.size();
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_leg
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
const SuitLeg &SuitLegList::
get_leg(int n) const {
  nassertr(n >= 0 && n < (int)_legs.size(), _legs[0]);
  return _legs[n];
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_leg_index_at_time
//       Access: Published
//  Description: Returns the index of the leg within the list that
//               covers the indicated elapsed time from the beginning
//               of the path.
//
//               start is a hint, the index at which to start
//               searching.
////////////////////////////////////////////////////////////////////
int SuitLegList::
get_leg_index_at_time(double time, int start) const {
  if (start < 0 || start >= (int)_legs.size() ||
      _legs[start]._start_time > time) {
    start = 0;
  }

  int i = start;
  while (i + 1 < (int)_legs.size() &&
         _legs[i + 1]._start_time <= time) {
    i++;
  }

  return i;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::is_point_in_range
//       Access: Published
//  Description: Returns true if the indicated point lies on this
//               path, between times begin and end, or false
//               otherwise.  This is useful for ensuring two suits
//               aren't assigned paths too close to each other.
////////////////////////////////////////////////////////////////////
bool SuitLegList::
is_point_in_range(const DNASuitPoint *point, double begin,
                  double end) const {
  int point_index = point->get_index();
  int start_index = get_leg_index_at_time(begin, 0);
  int end_index = get_leg_index_at_time(end, start_index);

  for (int i = start_index; i <= end_index; i++) {
    nassertr(i >= 0 && i < (int)_legs.size(), false);
    const SuitLeg &leg = _legs[i];
    if (leg.get_point_a() == point_index || leg.get_point_b() == point_index) {
      return true;
    }
  }

  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::output
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
void SuitLegList::
output(ostream &out) const {
  out << "SuitLegList, " << _legs.size() << " legs.";
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::write
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
void SuitLegList::
write(ostream &out) const {
  out << "SuitLegList:\n";
  for (size_t i = 0; i < _legs.size(); i++) {
    out << "  " << i << ". " << _legs[i] << "\n";
  }
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_first_leg_type
//       Access: Private, Static
//  Description: Returns the type of the first leg in the path, given
//               the indicated first DNASuitPoint.
////////////////////////////////////////////////////////////////////
SuitLeg::Type SuitLegList::
get_first_leg_type(const DNASuitPoint *point) {
  switch (point->get_point_type()) {
  case DNASuitPoint::SIDE_DOOR_POINT:
    return SuitLeg::T_from_suit_building;

  default:
    return SuitLeg::T_from_sky;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_next_leg_type
//       Access: Private, Static
//  Description: Returns the type of an intermediate leg in the path,
//               given a DNASuitPoint and the one preceding it.
////////////////////////////////////////////////////////////////////
SuitLeg::Type SuitLegList::
get_next_leg_type(const DNASuitPoint *prev_point,
                  const DNASuitPoint *curr_point) {
  switch (curr_point->get_point_type()) {
  case DNASuitPoint::FRONT_DOOR_POINT:
  case DNASuitPoint::SIDE_DOOR_POINT:
    return SuitLeg::T_walk_from_street;

  default:
    break;
  }

  switch (prev_point->get_point_type()) {
  case DNASuitPoint::FRONT_DOOR_POINT:
  case DNASuitPoint::SIDE_DOOR_POINT:
    return SuitLeg::T_walk_to_street;

  default:
    break;
  }

  return SuitLeg::T_walk;
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_last_leg_type
//       Access: Private, Static
//  Description: Returns the type of the last leg in the path, given
//               the indicated last DNASuitPoint.
////////////////////////////////////////////////////////////////////
SuitLeg::Type SuitLegList::
get_last_leg_type(const DNASuitPoint *point) {
  switch (point->get_point_type()) {
  case DNASuitPoint::FRONT_DOOR_POINT:
    return SuitLeg::T_to_toon_building;

  case DNASuitPoint::SIDE_DOOR_POINT:
    return SuitLeg::T_to_suit_building;

  default:
    return SuitLeg::T_to_sky;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: SuitLegList::get_zone_id
//       Access: Private, Static
//  Description: Returns the Zone ID associated with the edge defined
//               by the two suit points.
////////////////////////////////////////////////////////////////////
int SuitLegList::
get_zone_id(const DNAStorage &storage, int pi_a, int pi_b) {
  string name = storage.get_suit_edge_zone(pi_a, pi_b);

  // Get the part of the name before the first colon, if any.
  size_t colon = name.find(':');
  if (colon != string::npos) {
    name = name.substr(0, colon);
  }

  // That should be just a numeric zone ID.
  int zone_id;
  bool result = string_to_int(name, zone_id);
  nassertr(result, 0);

  return zone_id;
}

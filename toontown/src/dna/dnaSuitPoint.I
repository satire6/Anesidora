// Filename: dnaSuitPoint.I
// Created by:  shochet (28Jan01)
//
////////////////////////////////////////////////////////////////////



INLINE void DNASuitPoint::set_index(int index) {
  _index = index;
}

INLINE int DNASuitPoint::get_index() const {
  return _index;
}

INLINE DNASuitPoint::DNASuitPointType DNASuitPoint::get_point_type() const {
  return _type;
}

INLINE void DNASuitPoint::set_point_type(DNASuitPoint::DNASuitPointType type) {
  _type = type;
}

INLINE LPoint3f DNASuitPoint::get_pos() const {
  return _pos;
}

INLINE void DNASuitPoint::set_pos(LPoint3f pos) {
  _pos = pos;
}

INLINE void DNASuitPoint::set_graph_id(int graph_id) {
  _graph_id = graph_id;
}

INLINE int DNASuitPoint::get_graph_id() const {
  return _graph_id;
}

INLINE int DNASuitPoint::get_landmark_building_index() const {
  return _lb_index;
}

INLINE void DNASuitPoint::set_landmark_building_index(int lb_index) {
  _lb_index = lb_index;
}

////////////////////////////////////////////////////////////////////
//     Function: DNASuitPoint::is_terminal
//       Access: Published
//  Description: Returns true if this point is the sort of point you
//               find at the beginning or end of a suit path (like a
//               FRONT_DOOR_POINT or SIDE_DOOR_POINT), or false if it
//               is something you're more likely to find in the middle
//               of a suit path (like a STREET_POINT).
////////////////////////////////////////////////////////////////////
INLINE bool DNASuitPoint::
is_terminal() const {
  switch (_type) {
  case FRONT_DOOR_POINT:
  case SIDE_DOOR_POINT:
    return true;

  default:
    return false;
  }
}

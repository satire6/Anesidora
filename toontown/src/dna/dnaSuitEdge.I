// Filename: dnaSuitEdge.I
// Created by:  shochet (28Jan01)
//
////////////////////////////////////////////////////////////////////

INLINE bool DNASuitEdge::
operator == (const DNASuitEdge &other) const {
  return (_start_point == other._start_point &&
          _end_point == other._end_point);
}

INLINE PT(DNASuitPoint) DNASuitEdge::get_start_point() const {
  return _start_point;
}

INLINE PT(DNASuitPoint) DNASuitEdge::get_end_point() const {
  return _end_point;
}

INLINE string DNASuitEdge::get_zone_id() const {
  return _zone_id;
}

INLINE void DNASuitEdge::set_zone_id(string zone_id) {
  _zone_id = zone_id;
}

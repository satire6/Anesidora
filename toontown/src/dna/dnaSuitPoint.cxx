// Filename: dnaSuitPoint.cxx
// Created by:  shochet (28Jan01)
//
////////////////////////////////////////////////////////////////////

#include "dnaSuitPoint.h"


////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNASuitPoint::_type_handle;

ostream &
operator << (ostream &out, DNASuitPoint::DNASuitPointType type) {
  switch (type) {
  case DNASuitPoint::STREET_POINT:
    return out << "STREET_POINT";

  case DNASuitPoint::FRONT_DOOR_POINT:
    return out << "FRONT_DOOR_POINT";

  case DNASuitPoint::SIDE_DOOR_POINT:
    return out << "SIDE_DOOR_POINT";

  case DNASuitPoint::COGHQ_IN_POINT:
    return out << "COGHQ_IN_POINT";

  case DNASuitPoint::COGHQ_OUT_POINT:
    return out << "COGHQ_OUT_POINT";
  }

  return out << "**invalid**";
}

////////////////////////////////////////////////////////////////////
//     Function: DNASuitPoint::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASuitPoint::DNASuitPoint(int index, DNASuitPointType type, LPoint3f pos, int lb_index) {
  // The index gets set when the point is stored in the dnaStorage
  _index = index;
  _type = type;
  _pos = pos;
  _graph_id = 0;
  _lb_index = lb_index;
}

////////////////////////////////////////////////////////////////////
//     Function: DNASuitPoint::output
//       Access: Public
//  Description: Output all the properties to the stream
////////////////////////////////////////////////////////////////////
void DNASuitPoint::output(ostream &out) const {
  out << "<" << _index << ", " << _type << ", " << _pos;
  if (_lb_index >= 0) {
    out << ", " << _lb_index;
  }
  out << ">";
}

////////////////////////////////////////////////////////////////////
//     Function: DNASuitPoint::write
//       Access: Public
//  Description: write the suit point back out to the dna
////////////////////////////////////////////////////////////////////
void DNASuitPoint::write(ostream &out, int indent_level) const {
  if (_lb_index >= 0) {
    indent(out, indent_level) << "store_suit_point [ "
                              << _index << ", "
                              << _type << ", "
                              << _pos << ", "
                              << _lb_index
                              << " ]\n";
  } else {
    indent(out, indent_level) << "store_suit_point [ "
                              << _index << ", "
                              << _type << ", "
                              << _pos << " ]\n";
  }
}

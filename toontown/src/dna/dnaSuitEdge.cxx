// Filename: dnaSuitEdge.cxx
// Created by:  shochet (28Jan01)
//
////////////////////////////////////////////////////////////////////

#include "dnaSuitEdge.h"
#include "dnaStorage.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNASuitEdge::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: DNASuitEdge::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASuitEdge::DNASuitEdge(PT(DNASuitPoint) start_point,
                         PT(DNASuitPoint) end_point,
                         string zone_id) {
  _start_point = start_point;
  _end_point = end_point;
  _zone_id = zone_id;
}


////////////////////////////////////////////////////////////////////
//     Function: DNASuitEdge::output
//       Access: Public
//  Description: Outputs all the properties to ostream
////////////////////////////////////////////////////////////////////
void DNASuitEdge::output(ostream &out) const {
  out << "<" << _start_point->get_index()
      << " " << _end_point->get_index()
      << " zone " << _zone_id << ">";
}


////////////////////////////////////////////////////////////////////
//     Function: DNASuitEdge::write
//       Access: Public
//  Description: Writes the edge and properties
////////////////////////////////////////////////////////////////////
void DNASuitEdge::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level)
    << "suit_edge [ "
    << _start_point->get_index() << " "
    << _end_point->get_index() << " ]\n";
}

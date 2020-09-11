// Filename: dnaBattleCell.cxx
// Created by:  shochet (31Jan01)
//
////////////////////////////////////////////////////////////////////

#include "dnaBattleCell.h"
#include "dnaStorage.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNABattleCell::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNABattleCell::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNABattleCell::DNABattleCell(float width, float height, LPoint3f pos) {
  _width = width;
  _height = height;
  _pos = pos;
}

////////////////////////////////////////////////////////////////////
//     Function: DNABattleCell::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNABattleCell::traverse(NodePath &parent, DNAStorage *store, int editing) {
  return parent;
}

////////////////////////////////////////////////////////////////////
//     Function: DNABattleCell::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNABattleCell::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "battle_cell [ "
                            << _width << " " << _height << " "
                            << _pos[0] << " " << _pos[1] << " " << _pos[2]
                            << " ]\n";
}


////////////////////////////////////////////////////////////////////
//     Function: DNABattleCell::output
//       Access: Public
//  Description: Writes the cell properties to output
////////////////////////////////////////////////////////////////////
void DNABattleCell::output(ostream &out) const {
  out << "Width: " << _width
      << " Height: " << _height
      << " Pos: " << _pos;
}

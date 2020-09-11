// Filename: dnaInteractiveProp.I
// Created by:  gjeon (02Oct09)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
//     Function: DNAInteractiveProp::set_cell_id
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void DNAInteractiveProp::set_cell_id(int cell_id) {
  _cell_id = cell_id;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAInteractiveProp::get_cell_id
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE int DNAInteractiveProp::get_cell_id() const {
  return _cell_id;
}

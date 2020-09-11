// Filename: dnaSuitPath.I
// Created by:  shochet (28Jan01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: DNASuitPath::get_num_points
//       Access: Public
//  Description: How many points are along this path, including the
//               starting and ending points
////////////////////////////////////////////////////////////////////
INLINE int DNASuitPath::get_num_points() const {
  return _path.size();
}


////////////////////////////////////////////////////////////////////
//     Function: DNASuitPath::get_point_index
//       Access: Public
//  Description: Returns the point index at location i. This index
//               can then be looked up in the dna storage to ask
//               properties of the actual point
////////////////////////////////////////////////////////////////////
INLINE int DNASuitPath::get_point_index(int i) const {
  nassertr(i < (int)_path.size(), -1);
  return _path[i];
}


////////////////////////////////////////////////////////////////////
//     Function: DNASuitPath::add_point
//       Access: Public
//  Description: Adds a point to the end of current path
////////////////////////////////////////////////////////////////////
INLINE void DNASuitPath::add_point(int index) {
  _path.push_back(index);
}


////////////////////////////////////////////////////////////////////
//     Function: DNASuitPath::reverse
//       Access: Public
//  Description: Reverse the path. Useful when the points got added
//               from end to start as the dna Storage does them
////////////////////////////////////////////////////////////////////
INLINE void DNASuitPath::reverse_path() {
  reverse(_path.begin(), _path.end());
}


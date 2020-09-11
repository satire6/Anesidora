// Filename: cPetChase.I
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::set_target
//       Access: Published
//  Description: Sets the NodePath that this pet should chase
////////////////////////////////////////////////////////////////////
INLINE void CPetChase::
set_target(const NodePath &target) {
  _target = target;
}

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::get_target
//       Access: Published
//  Description: Returns the NodePath that this pet is chasing
////////////////////////////////////////////////////////////////////
INLINE NodePath CPetChase::
get_target() const {
  return _target;
}

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::set_min_dist
//       Access: Published
//  Description: Sets the minimum distance for which the pet should
//               approach the target it is chasing.
////////////////////////////////////////////////////////////////////
INLINE void CPetChase::
set_min_dist(float min_dist) {
  _min_dist = min_dist;
}

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::get_min_dist
//       Access: Published
//  Description: returns the minimum distance for which the pet should
//               approach the target it is chasing.
////////////////////////////////////////////////////////////////////
INLINE float CPetChase::
get_min_dist() const{
  return _min_dist;
}

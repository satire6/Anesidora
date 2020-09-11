// Filename: cPetBrain.h
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

#include "cPetBrain.h"
#include "luse.h"

////////////////////////////////////////////////////////////////////
//     Function: CPetBrain::Constructor
//       Access: Published
//  Description: 
////////////////////////////////////////////////////////////////////
CPetBrain::
CPetBrain() {
}

////////////////////////////////////////////////////////////////////
//     Function: CPetBrain::is_attending_us
//       Access: Published
//  Description: Calculates whether another avatar is paying
//               attention to us
////////////////////////////////////////////////////////////////////
bool CPetBrain::
is_attending_us(NodePath &us, NodePath &them) {
  LVector3f avRelPos(them.get_pos(us));
  float distSq = avRelPos.length_squared();
  //cerr << "distSq " << distSq << endl;
  if (distSq > 100) {
    return false;
  }
  LVector3f selfRelPos(us.get_pos(them));
  selfRelPos.normalize();
  float dot = selfRelPos.dot(selfRelPos.forward());
  //cerr << "dot " << dot << endl;
  if (dot < .8) {
    return false;
  }
  return true;
}

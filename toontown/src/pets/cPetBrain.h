// Filename: cPetBrain.h
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

#ifndef CPETBRAIN_H
#define CPETBRAIN_H

#include "toontownbase.h"
#include "nodePath.h"

class EXPCL_TOONTOWN CPetBrain {
PUBLISHED:
  CPetBrain();
  bool is_attending_us(NodePath &us, NodePath &them);
};

#endif

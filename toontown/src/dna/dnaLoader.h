// Filename: dnaLoader.h
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////

#ifndef DNALOADER_H
#define DNALOADER_H

#include "toontownbase.h"
#include "nodePath.h"
#include "pandaNode.h"

#include "dnaStorage.h"
#include "dnaGroup.h"
#include "dnaVisGroup.h"
#include "dnaNode.h"
#include "dnaBuildings.h"
#include "dnaData.h"


///////////////////////////////////////////////////////////////////
//       Class : DNALoader
// Description : Converts a dna structure, possibly read from a
//               dna file but not necessarily, into a scene graph
//               suitable for rendering.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNALoader {
PUBLISHED:
  DNALoader();
  PT(PandaNode) build_graph(DNAStorage *dna_store, int editing=0);
  PT(DNAData) get_data();
  PT(PandaNode) _top_node;
  NodePath _root;
  PT(DNAData) _data;
};

#endif

// Filename: dnaLoader.cxx
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////

#include "dnaLoader.h"
#include "dnaStorage.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "pointerTo.h"


////////////////////////////////////////////////////////////////////
//     Function: DNALoader::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNALoader::DNALoader() {
  _data = new DNAData("loader_data");
  PT(PandaNode) _top_node = new PandaNode("dna");
  _root = NodePath(_top_node);
}


////////////////////////////////////////////////////////////////////
//     Function: DNALoader::build_graph
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
PT(PandaNode) DNALoader::
build_graph(DNAStorage *dna_store, int editing) {
  // Return the first child of the root
  NodePath top = _data->top_level_traverse(_root, dna_store, editing);
  if (!(top.get_num_children() == 0)) {
    return top.get_child(0).node();
  }
  else {
    dna_cat.debug()
      << "DNA File contained no geometry, returning empty node" << endl;
    return (PandaNode *)NULL;
  }
}

PT(DNAData) DNALoader::get_data() {
  return _data;
}


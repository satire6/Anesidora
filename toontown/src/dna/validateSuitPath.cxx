// Filename: validateSuitPath.cxx
// Created by:  drose (19Jul04)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) 2001 - 2004, Disney Enterprises, Inc.  All rights reserved
//
// All use of this software is subject to the terms of the Panda 3d
// Software license.  You should have received a copy of this license
// along with this source code; you will also find a current copy of
// the license at http://etc.cmu.edu/panda3d/docs/license/ .
//
// To contact the maintainers of this program write to
// panda3d-general@lists.sourceforge.net .
//
////////////////////////////////////////////////////////////////////

#include "toontownbase.h"
#include "dnaVisGroup.h"
#include "dnaStorage.h"
#include "load_dna_file.h"
#include "config_dna.h"

#include "pmap.h"

#include <stdlib.h>

int
main(int argc, char *argv[]) {
  DNAStorage *dna_store = new DNAStorage;

  // Load up all of the named files.
  int i;
  for (i = 1; i < argc; i++) {
    load_DNA_file_AI(dna_store, argv[i]);
  }

  int num_graphs = dna_store->discover_continuity();
  dna_cat.info()
    << num_graphs << " suit path(s).\n";

  // Check the assignment of zone IDs to battle cell center points.
  for (i = 0; i < dna_store->get_num_DNAVisGroupsAI(); i++) {
    PT(DNAVisGroup) vg = dna_store->get_DNAVisGroupAI(i);
    if (vg->get_num_battle_cells() > 1) {
      dna_cat.warning()
        << "Multiple battle cells for zone " << vg->get_name() << "\n";
    }
  }

  return (0);
}

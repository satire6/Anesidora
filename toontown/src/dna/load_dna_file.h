// Filename: load_dna_file.h
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////

#ifndef LOAD_DNA_FILE_H
#define LOAD_DNA_FILE_H

#include "toontownbase.h"
#include "dnaData.h"
#include "pointerTo.h"
#include "pandaNode.h"
#include "coordinateSystem.h"

class DNAStorage;
class DNALoader;

BEGIN_PUBLISH

////////////////////////////////////////////////////////////////////
//     Function: load_dna_file
//  Description: A convenience function; the primary interface to this
//               package.  Loads up the indicated dna file, and
//               returns the root of a scene graph.  Returns NULL if
//               the file cannot be read for some reason.
////////////////////////////////////////////////////////////////////
EXPCL_TOONTOWN PT(PandaNode)
load_DNA_file(DNAStorage *dna_store,
              const string &filename,
              CoordinateSystem cs = CS_default,
              int editing = 0);



////////////////////////////////////////////////////////////////////
//     Function: load_dna_file_ai
//  Description: Loads up the indicated dna file but does not create
//               any geometry from it. It simply creates the dna
//               structures that can then be accessed via the dnaStorage
//               Returns the DNAData object on success, or NULL if the
//               file cannot be read for some reason.
////////////////////////////////////////////////////////////////////
EXPCL_TOONTOWN PT(DNAData)
load_DNA_file_AI(DNAStorage *dna_store,
                 const string &filename,
                 CoordinateSystem cs = CS_default);

END_PUBLISH

#endif

// Filename: load_dna_file.cxx
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////

#include "config_dna.h"
#include "load_dna_file.h"
#include "dnaLoader.h"
#include "dnaData.h"
#include "dnaStorage.h"
#include "config_util.h"
#include "virtualFileSystem.h"

////////////////////////////////////////////////////////////////////
//     Function: load_dna_file
//  Description: A convenience function.  Loads up the indicated dna
//               file, and returns the root of a scene graph.  Returns
//               NULL if the file cannot be read for some reason.
//
//               Unlike load_egg_file(), this function *does* search
//               for the file along the model_path (as well as the
//               dna_path) if it is not already fully qualified.
//               Begin the filename with ./ to prevent this behavior.
////////////////////////////////////////////////////////////////////
PT(PandaNode)
load_DNA_file(DNAStorage *dna_store,
              const string &filename,
              CoordinateSystem cs,
              int editing) {
  // We use binary mode to avoid Windows' end-of-line convention.
  Filename dna_filename = Filename::binary_filename(filename);
  if (!dna_filename.is_fully_qualified()) {
    if (!DNAData::resolve_dna_filename(dna_filename)) {
      dna_cat.error() << "load_DNA_file could not find " << filename
        <<"\n    in dna_path: "<<get_dna_path()
        <<"\n    or model_path: "<<get_model_path()<<"\n";
      return (PandaNode *)NULL;
    }
  }

  dna_cat.info() << "Reading " << dna_filename << "\n";

  DNALoader loader;
  loader._data->set_dna_filename(dna_filename);
  loader._data->set_dna_storage(dna_store);
  if (cs != CS_default) {
    loader._data->set_coordinate_system(cs);
  }
  bool ok_flag;

  VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();
  istream *istr = vfs->open_read_file(dna_filename, true);
  if (istr == (istream *)NULL) {
    dna_cat.error()
      << "Could not open " << dna_filename << " for reading.\n";
    return (PandaNode *)NULL;
  }
  ok_flag = loader._data->read(*istr);
  vfs->close_read_file(istr);

  if (!ok_flag) {
    dna_cat.error() << "Error reading " << dna_filename << "\n";
    return (PandaNode *)NULL;
  }

  dna_cat.debug() << "About to call loader.build_graph\n";
  return loader.build_graph(dna_store, editing);
}



////////////////////////////////////////////////////////////////////
//     Function: load_dna_file_AI
//  Description: Loads up the indicated dna file but does not create
//               geometry.  Returns the DNAData loaded, or NULL.
////////////////////////////////////////////////////////////////////
PT(DNAData)
load_DNA_file_AI(DNAStorage *dna_store,
              const string &filename,
              CoordinateSystem cs) {
  Filename dna_filename = Filename::text_filename(filename);
  if (!DNAData::resolve_dna_filename(dna_filename)) {
    dna_cat.error() << "load_DNA_file_AI could not find " << filename
      <<"\n    in dna_path: "<<get_dna_path()
      <<"\n    or model_path: "<<get_model_path()<<"\n";
    return NULL;
  }

  dna_cat.info() << "Reading " << dna_filename << "\n";

  DNALoader loader;
  loader._data->set_dna_filename(dna_filename);
  loader._data->set_dna_storage(dna_store);
  if (cs != CS_default) {
    loader._data->set_coordinate_system(cs);
  }
  bool ok_flag;

  VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();
  istream *istr = vfs->open_read_file(dna_filename, true);
  if (istr == (istream *)NULL) {
    dna_cat.error()
      << "Could not open " << dna_filename << " for reading.\n";
    return NULL;
  }
  ok_flag = loader._data->read(*istr);
  vfs->close_read_file(istr);

  if (!ok_flag) {
    dna_cat.error() << "Error reading " << dna_filename << "\n";
    return NULL;
  }

  // Success!
  return loader._data;
}

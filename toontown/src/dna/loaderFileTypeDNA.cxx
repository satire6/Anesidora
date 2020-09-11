// Filename: loaderFileTypeDNA.cxx
// Created by:  drose (28Aug00)
//
////////////////////////////////////////////////////////////////////

#include "loaderFileTypeDNA.h"
#include "load_dna_file.h"
#include "dnaStorage.h"
#include "config_dna.h"

#include "config_util.h"
#include "virtualFileSystem.h"

DNAStorage *LoaderFileTypeDNA::_dna_store = (DNAStorage *)NULL;
TypeHandle LoaderFileTypeDNA::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: LoaderFileTypeDNA::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
LoaderFileTypeDNA::
LoaderFileTypeDNA() {
}

////////////////////////////////////////////////////////////////////
//     Function: LoaderFileTypeDNA::get_name
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
string LoaderFileTypeDNA::
get_name() const {
  return "DNA";
}

////////////////////////////////////////////////////////////////////
//     Function: LoaderFileTypeDNA::get_extension
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
string LoaderFileTypeDNA::
get_extension() const {
  return "dna";
}

////////////////////////////////////////////////////////////////////
//     Function: LoaderFileTypeDNA::resolve_filename
//       Access: Public, Virtual
//  Description: Searches for the indicated filename on whatever paths
//               are appropriate to this file type, and updates it if
//               it is found.
////////////////////////////////////////////////////////////////////
void LoaderFileTypeDNA::
resolve_filename(Filename &path) const {
  VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();
  vfs->resolve_filename(path, get_dna_path());
  vfs->resolve_filename(path, get_model_path());
}

////////////////////////////////////////////////////////////////////
//     Function: LoaderFileTypeDNA::load_file
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
PT(PandaNode) LoaderFileTypeDNA::
load_file(const Filename &path, const LoaderOptions &, 
          BamCacheRecord *record) const {
  if (_dna_store == (DNAStorage *)NULL) {
    _dna_store = new DNAStorage;

    // Preload whatever we asked to preload in the config file.
    VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();

    int num_preload = dna_preload.get_num_unique_values();
    for (int pi = 0; pi < num_preload; pi++) {
      Filename path = dna_preload.get_unique_value(pi);
      vfs->resolve_filename(path, get_model_path());
      load_DNA_file(_dna_store, path);
    }
  }

  // Return the resulting node
  return load_DNA_file(_dna_store, path);
}

// Filename: dnaData.cxx
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////
#include "dnaData.h"
#include "config_dna.h"
#include "config_util.h"

#include "string_utils.h"
#include "coordinateSystem.h"
#include "luse.h"
#include "dSearchPath.h"
#include "config_util.h"
#include "virtualFileSystem.h"

extern int dnayyparse(void);
#include "parserDefs.h"
#include "lexerDefs.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNAData::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: DnaData::resolve_dna_filename
//       Access: Public, Static
//  Description: Looks for the indicated filename, first along the
//               indicated searchpath, and then along the dna_path and
//               finally along the model_path.  If found, updates the
//               filename to the full path and returns true;
//               otherwise, returns false.
////////////////////////////////////////////////////////////////////
bool DNAData::
resolve_dna_filename(Filename &dna_filename, const DSearchPath &searchpath) {
  VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();
  
  vfs->resolve_filename(dna_filename, searchpath, "dna") ||
    vfs->resolve_filename(dna_filename, get_dna_path(), "dna") ||
    vfs->resolve_filename(dna_filename, get_model_path(), "dna");
  return vfs->exists(dna_filename);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::read
//       Access: Public
//  Description: Opens the indicated filename and reads the DNA data
//               contents from it.  Returns true if the file was
//               successfully opened and read, false if there were
//               some errors, in which case the data may be partially
//               read.
//
//               error is the output stream to which to write error
//               messages.
////////////////////////////////////////////////////////////////////
bool DNAData::
read(Filename filename, ostream &error) {
  if (!resolve_dna_filename(filename)) {
    error << "Could not find " << filename << "\n";
    return false;
  }

  // We use binary mode to avoid Windows' end-of-line convention.
  filename.set_binary();
  set_dna_filename(filename);

  pifstream file;
  if (!filename.open_read(file)) {
    error << "Unable to open " << filename << "\n";
    return false;
  }

  return read(file, error);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::read
//       Access: Public
//  Description: Parses the DNA syntax contained in the indicated
//               input stream.  Returns true if the stream was a
//               completely valid DNA file, false if there were some
//               errors, in which case the data may be partially read.
////////////////////////////////////////////////////////////////////
bool DNAData::
read(istream &in, ostream &error) {
  // First, dispense with any children we had previously.  We will
  // replace them with the new data.
  dna_cat.debug() << "start of dnData.read\n";
  _group_vector.clear();

  dna_init_parser(in, error, get_dna_filename(), this);
  dnayyparse();
  dna_cleanup_parser();

  post_read(error);

  dna_cat.debug() << "end of DNAData.read\n";
  return (dna_error_count() == 0);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::resolve_externals
//       Access: Public
//  Description: Loads up all the dna files referenced by <File>
//               entries within the dna structure, and inserts their
//               contents in place of the <File> entries.  Searches
//               for files in the searchpath, if not found directly,
//               and writes error messages to the indicated output
//               stream.  Returns true if all externals were loaded
//               successfully, false otherwise.
////////////////////////////////////////////////////////////////////
bool DNAData::
resolve_externals(const string &searchpath, ostream &error) {
  //return r_resolve_externals(searchpath, error, get_coordinate_system());
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::write_dna
//       Access: Public
//  Description: The main interface for writing complete dna files.
////////////////////////////////////////////////////////////////////
bool DNAData::
write_dna(Filename filename, ostream &error, DNAStorage *store) {
  // We use binary mode to avoid Windows' end-of-line convention.
  filename.set_binary();
  filename.unlink();

  pofstream file;
  if (!filename.open_write(file)) {
    error << "Unable to open " << filename << " for writing.\n";
    return false;
  }

  return write_dna(file, error, store);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::write_dna
//       Access: Public
//  Description: The main interface for writing complete dna files.
////////////////////////////////////////////////////////////////////
bool DNAData::
write_dna(ostream &out, ostream &, DNAStorage *store) {
  pre_write();
  write(out, store, 0);
  return true;
}



////////////////////////////////////////////////////////////////////
//     Function: DNAData::set_coordinate_system
//       Access: Public
//  Description: Changes the coordinate system of the DNAData.  If the
//               coordinate system was previously different, this may
//               result in a conversion of the data.
////////////////////////////////////////////////////////////////////
void DNAData::
set_coordinate_system(CoordinateSystem new_coordsys) {
  if (new_coordsys == CS_default) {
    new_coordsys = get_default_coordinate_system();
  }
  if (new_coordsys != _coordsys &&
      (_coordsys != CS_default && _coordsys != CS_invalid)) {
    // Time to convert the data.
    //    r_transform(LMatrix4d::convert_mat(_coordsys, new_coordsys),
    //          LMatrix4d::convert_mat(new_coordsys, _coordsys),
    //          new_coordsys);
  }

  _coordsys = new_coordsys;
}




////////////////////////////////////////////////////////////////////
//     Function: DNAData::post_read
//       Access: Private
//  Description: Does whatever processing is appropriate after reading
//               the data in from an dna file.
////////////////////////////////////////////////////////////////////
void DNAData::
post_read(ostream &error) {

  // Resolve filenames that are relative to the dna file.
  //resolve_filenames(get_dna_filename().get_dirname());
}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::pre_write
//       Access: Private
//  Description: Does whatever processing is appropriate just before
//               writing the data out to an dna file.
////////////////////////////////////////////////////////////////////
void DNAData::
pre_write() {

}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::write
//       Access: Public, Virtual
//  Description: Writes the dna data out to the indicated output
//               stream.
////////////////////////////////////////////////////////////////////
void DNAData::
write(ostream &out, DNAStorage *store, int indent_level) const {
  // Write out anything the store wants to write
  store->fixup();
  store->write(out, indent_level);

  // Do not write out this group, just the children
  // DNAGroup::write(out, store, indent_level);
  // Write all the children
  pvector<PT(DNAGroup)>::const_iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *i;
    group->write(out, store, indent_level);
  }

  out << flush;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAData::make_copy() {
  return new DNAData(*this);
}

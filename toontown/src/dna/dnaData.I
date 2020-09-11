// Filename: dnaData.I
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: DNAData::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE DNAData::
DNAData(const string &initial_name) :
  DNAGroup(initial_name)
{
  _coordsys = CS_default;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::Copy constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE DNAData::
DNAData(const DNAData &copy) :
  DNAGroup(copy),
  _coordsys(copy._coordsys),
  _dna_filename(copy._dna_filename) {
}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::Copy assignment operator
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE DNAData &DNAData::
operator = (const DNAData &copy) {
  //DnaGroupNode::operator = (copy);
  _coordsys = copy._coordsys;
  _dna_filename = copy._dna_filename;
  return *this;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::get_coordinate_system
//       Access: Public
//  Description: Returns the coordinate system in which the dna file
//               is defined.
////////////////////////////////////////////////////////////////////
INLINE CoordinateSystem DNAData::
get_coordinate_system() const {
  return _coordsys;
}




////////////////////////////////////////////////////////////////////
//     Function: DNAData::set_dna_filename
//       Access: Public
//  Description: Sets the directory in which the dna file is
//               considered to reside.  This is also implicitly set by
//               read().
////////////////////////////////////////////////////////////////////
INLINE void DNAData::
set_dna_filename(const Filename &directory) {
  _dna_filename = directory;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::get_dna_filename
//       Access: Public
//  Description: Returns the directory in which the dna file is
//               considered to reside.
////////////////////////////////////////////////////////////////////
INLINE const Filename &DNAData::
get_dna_filename() const {
  return _dna_filename;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAData::set_dna_storage
//       Access: Public
//  Description: Sets the current dna storage facility
////////////////////////////////////////////////////////////////////
INLINE void DNAData::
set_dna_storage(DNAStorage *store) {
  _dna_store = store;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAData::get_dna_storage
//       Access: Public
//  Description: Returns the current dna storage facility
////////////////////////////////////////////////////////////////////
INLINE DNAStorage *DNAData::
get_dna_storage() {
  return _dna_store;
}





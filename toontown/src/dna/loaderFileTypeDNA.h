// Filename: loaderFileTypeDNA.h
// Created by:  drose (28Aug00)
//
////////////////////////////////////////////////////////////////////

#ifndef LOADERFILETYPEDNA_H
#define LOADERFILETYPEDNA_H

#include "toontownbase.h"

#include "loaderFileType.h"

class DNAStorage;

////////////////////////////////////////////////////////////////////
//       Class : LoaderFileTypeDNA
// Description : This defines the Loader interface to read DNA files.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN LoaderFileTypeDNA : public LoaderFileType {
public:
  LoaderFileTypeDNA();

  virtual string get_name() const;
  virtual string get_extension() const;

  virtual void resolve_filename(Filename &path) const;
  virtual PT(PandaNode) load_file(const Filename &path, const LoaderOptions &options,
                                  BamCacheRecord *record) const;

  static DNAStorage *_dna_store;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    LoaderFileType::init_type();
    register_type(_type_handle, "LoaderFileTypeDNA",
                  LoaderFileType::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#endif


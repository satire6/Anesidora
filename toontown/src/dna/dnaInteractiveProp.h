// Filename: dnaInteractiveProp.h
// Created by:  gjeon (28Sep09)
//
////////////////////////////////////////////////////////////////////
#ifndef DNAINTERACTIVEPROP_H
#define DNAINTERACTIVEPROP_H
//

#include "dnaStorage.h"
#include "dnaAnimProp.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"

////////////////////////////////////////////////////////////////////
//       Class : DNAInteractiveProp
// Description : An interactive prop like a walking hydrant.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAInteractiveProp : public DNAAnimProp  {
PUBLISHED:
  DNAInteractiveProp(const string &initial_name = "");
  DNAInteractiveProp(const DNAInteractiveProp &interactive_prop);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;
  INLINE void set_cell_id(int cell_id);
  INLINE int get_cell_id() const;

private:
  virtual DNAGroup* make_copy();

protected:
  int _cell_id;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNAInteractiveProp",
                  DNANode::get_class_type()
                  );
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "dnaInteractiveProp.I"

#endif

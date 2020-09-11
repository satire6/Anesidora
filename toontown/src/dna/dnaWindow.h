// Filename: dnaWindow.h
// Created by:  shochet (11Jun00)
//
////////////////////////////////////////////////////////////////////

//
#ifndef DNAWINDOW_H
#define DNAWINDOW_H
//
////////////////////////////////////////////////////////////////////
// Includes
////////////////////////////////////////////////////////////////////
#include "dnaStorage.h"
#include "dnaNode.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"


////////////////////////////////////////////////////////////////////
//       Class : DNAWindows
// Description : A group of windows with a default layout
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAWindows : public DNAGroup  {
PUBLISHED:
  DNAWindows(const string &initial_name = "");
  DNAWindows(const DNAWindows &window);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_window_count(int count);
  INLINE int get_window_count() const;

  INLINE void set_color(const Colorf &color);
  INLINE Colorf get_color() const;

private:
  virtual DNAGroup* make_copy();

private:
  string _code;
  int _window_count;
  Colorf _color;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNAGroup::init_type();
    register_type(_type_handle, "DNAWindows",
                  DNAGroup::get_class_type()
                  );
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "dnaWindow.I"

#endif

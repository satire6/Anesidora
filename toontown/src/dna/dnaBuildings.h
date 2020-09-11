// Filename: dnaBuildings.h
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////
#ifndef DNABUILDINGS_H
#define DNABUILDINGS_H
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
// Description : current_wall_height represents the current wall
//               height to allow the next wall to be stacked properly
//               on top
////////////////////////////////////////////////////////////////////
extern float current_wall_height;


////////////////////////////////////////////////////////////////////
//       Class : DNAWall
// Description : A stackable wall.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAWall : public DNANode  {
PUBLISHED:
  DNAWall(const string &initial_name = "");
  DNAWall(const DNAWall &wall);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_height(float height);
  INLINE float get_height() const ;

  INLINE void set_color(const Colorf &color);
  INLINE Colorf get_color() const;

private:
  virtual DNAGroup* make_copy();


private:
  string _code;
  float _height;
  Colorf _color;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNAWall",
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




////////////////////////////////////////////////////////////////////
//       Class : DNAFlatBuilding
// Description : A flat building.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAFlatBuilding : public DNANode  {
PUBLISHED:
  DNAFlatBuilding(const string &initial_name = "");
  DNAFlatBuilding(const DNAFlatBuilding &building);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_width(float width);
  INLINE float get_width() const;

  INLINE float get_current_wall_height();

protected:
  bool has_door(PT(DNAGroup) group_vector);
  void setup_suit_flat_building(NodePath &parent, DNAStorage *store);

private:
  virtual DNAGroup* make_copy();

private:
  float _width;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNAFlatBuilding",
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


////////////////////////////////////////////////////////////////////
//       Class : DNALandmarkBuilding
// Description : A landmark building.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNALandmarkBuilding : public DNANode  {
PUBLISHED:
  DNALandmarkBuilding(const string &initial_name = "");
  DNALandmarkBuilding(const DNALandmarkBuilding &building);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_title(const string &title);
  INLINE string get_title() const;

  INLINE void set_article(const string &article);
  INLINE string get_article() const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_wall_color(const Colorf &color);
  INLINE Colorf get_wall_color() const;

  INLINE void set_building_type(const string& type);
  INLINE string get_building_type() const;

protected:
  void setup_suit_building_origin(NodePath &parent,
    NodePath &building_node_path);

private:
  virtual DNAGroup* make_copy();

protected:
  string _code;
  Colorf _wall_color;
  string _title;
  string _article;
  string _building_type;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNALandmarkBuilding",
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

#include "dnaBuildings.I"

#endif

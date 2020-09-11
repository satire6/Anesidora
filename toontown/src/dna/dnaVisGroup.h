// Filename: dnaVisGroup.h
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////

//
#ifndef DNAVISGROUP_H
#define DNAVISGROUP_H
//
////////////////////////////////////////////////////////////////////
// Includes
////////////////////////////////////////////////////////////////////
#include "toontownbase.h"

#include "typedObject.h"
#include "namable.h"
#include "nodePath.h"
#include "pvector.h"
#include <string>
#include "pointerTo.h"

#include "dnaGroup.h"
#include "dnaSuitEdge.h"
#include "dnaBattleCell.h"

class DNAStorage;

////////////////////////////////////////////////////////////////////
//       Class : DNAVisGroup
// Description : A group of dna nodes with special visibility info
//               tagged in a vis property. The vis property should list
//               all the other DNAVisGroups (including itself) that
//               should be rendered when the avatar is standing in this group
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAVisGroup : public DNAGroup {
PUBLISHED:
  DNAVisGroup(const string &initial_name = "");
  DNAVisGroup(const DNAVisGroup &group);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  void add_visible(const string &vis_group_name);
  int remove_visible(const string &vis_group_name);
  int get_num_visibles() const;
  string get_visible_name(uint i) const;

  void add_suit_edge(PT(DNASuitEdge) edge);
  int remove_suit_edge(PT(DNASuitEdge) edge);
  int get_num_suit_edges() const;
  PT(DNASuitEdge) get_suit_edge(uint i) const;

  void add_battle_cell(PT(DNABattleCell) cell);
  int remove_battle_cell(PT(DNABattleCell) cell);
  int get_num_battle_cells() const;
  PT(DNABattleCell) get_battle_cell(uint i) const;

private:
  virtual DNAGroup* make_copy();

protected:
  pvector< string > _vis_vector;
  pvector< PT(DNASuitEdge) > _suit_edge_vector;
  pvector< PT(DNABattleCell) > _battle_cell_vector;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNAGroup::init_type();
    register_type(_type_handle, "DNAVisGroup",
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

#endif

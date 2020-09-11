// Filename: dnaVisGroup.cxx
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////

#include "dnaVisGroup.h"
#include "dnaStorage.h"
#include "pandaNode.h"
#include "pointerTo.h"
#include "indent.h"
#include "sceneGraphReducer.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNAVisGroup::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAVisGroup::DNAVisGroup(const string &initial_name) :
  DNAGroup(initial_name)
{

}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::CopyConstructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAVisGroup::DNAVisGroup(const DNAVisGroup &copy) :
  DNAGroup(copy)
{
  pvector<string>::const_iterator i = copy._vis_vector.begin();
  for(; i != copy._vis_vector.end(); ++i) {
    // Push in a copy of the vis string
    _vis_vector.push_back(*i);
  }
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::add_visible
//       Access: Public
//  Description: Add a vis group name to this group's list
////////////////////////////////////////////////////////////////////
void DNAVisGroup::add_visible(const string &vis_group_name) {
  _vis_vector.push_back(vis_group_name);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::remove_vis_group
//       Access: Public
//  Description: Remove a vis group name to this group's list
////////////////////////////////////////////////////////////////////
int DNAVisGroup::remove_visible(const string &vis_group_name) {
  pvector<string>::iterator i = find(_vis_vector.begin(),
                                    _vis_vector.end(),
                                    vis_group_name);
  if (i == _vis_vector.end()) {
    dna_cat.warning()
      << "DNAVisGroup: vis group not found in map: " << vis_group_name << endl;
    return 0;
  }

  // Erase him out of our vector
  _vis_vector.erase(i);
  return 1;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::get_num_visibles
//       Access: Public
//  Description: Ask how many visibles this vis group has
////////////////////////////////////////////////////////////////////
int DNAVisGroup::get_num_visibles() const {
  return _vis_vector.size();
}



////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::get_visible_name
//       Access: Public
//  Description: Return the string name of the ith visible
////////////////////////////////////////////////////////////////////
string DNAVisGroup::get_visible_name(uint i) const {
  nassertr(i < _vis_vector.size(), "");
  return _vis_vector[i];
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::add_suit_edge
//       Access: Public
//  Description: Adds a suit edge to this vis group
//               This is only stored here so we can write it back out
////////////////////////////////////////////////////////////////////
void DNAVisGroup::add_suit_edge(PT(DNASuitEdge) edge) {
  if (edge->get_start_point() == edge->get_end_point()) {
    // Don't add degenerate edges.
    return;
  }

  // Don't repeat edges either.
  pvector< PT(DNASuitEdge) >::iterator i;
  for (i = _suit_edge_vector.begin(); i != _suit_edge_vector.end(); ++i) {
    if (*(*i) == *edge) {
      return;
    }
  }

  _suit_edge_vector.push_back(edge);
}



////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::remove_suit_edge
//       Access: Public
//  Description: Remove this suit edge
////////////////////////////////////////////////////////////////////
int DNAVisGroup::remove_suit_edge(PT(DNASuitEdge) edge) {
  pvector< PT(DNASuitEdge) >::iterator i = find(_suit_edge_vector.begin(),
                                    _suit_edge_vector.end(),
                                    edge);
  if (i == _suit_edge_vector.end()) {
    dna_cat.debug()
      << "DNASuitEdge: edge not found in vector: " << (*edge) << endl;
    return 0;
  }

  // Erase him out of our vector
  _suit_edge_vector.erase(i);
  return 1;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::get_num_suit_edges
//       Access: Public
//  Description: Ask how many edges this vis group has
////////////////////////////////////////////////////////////////////
int DNAVisGroup::get_num_suit_edges() const {
  return _suit_edge_vector.size();
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::get_suit_edge
//       Access: Public
//  Description: Return the ith edge in the vector
////////////////////////////////////////////////////////////////////
PT(DNASuitEdge) DNAVisGroup::get_suit_edge(uint i) const {
  nassertr(i < _suit_edge_vector.size(), (DNASuitEdge *)NULL);
  return _suit_edge_vector[i];
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::add_battle_cell
//       Access: Public
//  Description: Adds a battle_cell to this vis group
//               This is only stored here so we can write it back out
////////////////////////////////////////////////////////////////////
void DNAVisGroup::add_battle_cell(PT(DNABattleCell) cell) {
  _battle_cell_vector.push_back(cell);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::remove_battle_cell
//       Access: Public
//  Description: Remove this battle cell
////////////////////////////////////////////////////////////////////
int DNAVisGroup::remove_battle_cell(PT(DNABattleCell) cell) {
  pvector< PT(DNABattleCell) >::iterator i = find(_battle_cell_vector.begin(),
                                                 _battle_cell_vector.end(),
                                                 cell);
  if (i == _battle_cell_vector.end()) {
    dna_cat.warning()
      << "DNABattleCell: cell not found in vector: " << (*cell) << endl;
    return 0;
  }

  // Erase him out of our vector
  _battle_cell_vector.erase(i);
  return 1;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::get_num_battle_cells
//       Access: Public
//  Description: Ask how many cells this vis group has
////////////////////////////////////////////////////////////////////
int DNAVisGroup::get_num_battle_cells() const {
  return _battle_cell_vector.size();
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::get_battle_cell
//       Access: Public
//  Description: Return the ith cell in the vector
////////////////////////////////////////////////////////////////////
PT(DNABattleCell) DNAVisGroup::get_battle_cell(uint i) const {
  nassertr(i < _battle_cell_vector.size(), (DNABattleCell *)NULL);
  return _battle_cell_vector[i];
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAVisGroup::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make a new node for this group

  PT(PandaNode) new_node = new PandaNode(get_name());
  NodePath group_node_path = parent.attach_new_node(new_node);

  // Traverse each node in our vector
  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    PT(DNAGroup) group = *i;
    group->traverse(group_node_path, store, editing);
  }

  if (editing) {
    // Remember that this nodepath is associated with this dnaVisGroup
    store->store_DNAGroup(group_node_path.node(), this);

  }

  // For retrieving vis data, a separate map is maintained
  // containing all the vis group info. Store us in that too
  // Even if we are not editing, this needs to go in the dna vis group
  // map so it can be extracted for visibility information
  store->store_DNAVisGroup(group_node_path.node(), this);

  return group_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAVisGroup::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "visgroup ";
  out << '"' << get_name() << '"' << " [\n";

  // Write the vis info
  indent(out, indent_level + 1) << "vis [ ";
  pvector<string>::const_iterator i = _vis_vector.begin();
  for(; i != _vis_vector.end(); ++i) {
    // Traverse each vis string in our vis vector
    indent(out, indent_level + 1) << '"' << (*i) << '"' << " ";
  }
  indent(out, indent_level + 1) << "]\n";

  // Write the suit edges
  pvector<PT(DNASuitEdge)>::const_iterator e = _suit_edge_vector.begin();
  for(; e != _suit_edge_vector.end(); ++e) {
    PT(DNASuitEdge) edge = *e;
    edge->write(out, store, indent_level + 1);
  }

  // Write the battle cells
  pvector<PT(DNABattleCell)>::const_iterator c = _battle_cell_vector.begin();
  for(; c != _battle_cell_vector.end(); ++c) {
    PT(DNABattleCell) cell = *c;
    cell->write(out, store, indent_level + 1);
  }

  // Write all the children
  pvector<PT(DNAGroup)>::const_iterator j = _group_vector.begin();
  for(; j != _group_vector.end(); ++j) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *j;
    group->write(out, store, indent_level + 1);
  }

  indent(out, indent_level) << "]\n";

}

////////////////////////////////////////////////////////////////////
//     Function: DNAVisGroup::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAVisGroup::make_copy() {
  return new DNAVisGroup(*this);
}

// Filename: dnaGroup.cxx
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////

#include "dnaGroup.h"
#include "dnaStorage.h"
#include "pandaNode.h"
#include "pointerTo.h"
#include "indent.h"
#include "sceneGraphReducer.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNAGroup::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAGroup::DNAGroup(const string &initial_name) :
  Namable(initial_name)
{
  _parent = NULL;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::CopyConstructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAGroup::DNAGroup(const DNAGroup &copy) :
  Namable(copy)
{
  _parent = NULL;
  pvector<PT(DNAGroup)>::const_iterator i = copy._group_vector.begin();
  for(; i != copy._group_vector.end(); ++i) {
    // Push in a copy of the dna group
    _group_vector.push_back((*i)->make_copy());
  }
}


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAGroup::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make a new node for this group

  PT(PandaNode) new_node = new PandaNode(get_name());
  NodePath group_node_path = parent.attach_new_node(new_node);

  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *i;
    group->traverse(group_node_path, store, editing);
  }

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(group_node_path.node(), this);
  }

  return group_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::top_level_traverse
//       Access: Public
//  Description: The top level traverse does some special things
////////////////////////////////////////////////////////////////////
NodePath DNAGroup::top_level_traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make a new node for this group

  PT(PandaNode) new_node = new PandaNode(get_name());
  NodePath group_node_path = parent.attach_new_node(new_node);

  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *i;
    group->traverse(group_node_path, store, editing);
    // Top level groups do not have parents
    group->clear_parent();
  }

  // Do not flatten here. It is done in Python now.

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(group_node_path.node(), this);
  }

  return group_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::add
//       Access: Public
//  Description: add a DNAGroup to this vector of nodes
////////////////////////////////////////////////////////////////////
void DNAGroup::add(PT(DNAGroup) group) {
  _group_vector.push_back(group);
  // This child group's parent is now this group
  group->set_parent(this);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::remove
//       Access: Public
//  Description: Remove a group from this vector. Note, this is
//               not really meant for heavy use, since we are using
//               an STL vector which erases in linear time.
//               Should be ok, since removal will be rare.
////////////////////////////////////////////////////////////////////
void DNAGroup::remove(PT(DNAGroup) group) {
  pvector<PT(DNAGroup)>::iterator i = find(_group_vector.begin(),
                                          _group_vector.end(), group);
  if (i == _group_vector.end()) {
    dna_cat.warning()
      << "DNAGroup: group not found in map" << endl;
    return;
  }

  // This child group no longer has a parent
  group->clear_parent();

  // Erase him out of our vector
  _group_vector.erase(i);
}



////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAGroup::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "group ";
  out << '"' << get_name() << '"' << " [\n";

  // Write all the children
  pvector<PT(DNAGroup)>::const_iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *i;
    group->write(out, store, indent_level + 1);
  }

  indent(out, indent_level) << "]\n";

}


////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::ls
//       Access: Public
//  Description: Writes the group and all children to cout (for debugging)
////////////////////////////////////////////////////////////////////
void DNAGroup::ls() const {
  write(cout, 0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAGroup::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
//               Redefine this for every class that subclasses DNAGroup
//               It is used in the copy constructor
////////////////////////////////////////////////////////////////////
DNAGroup* DNAGroup::make_copy() {
  return new DNAGroup(*this);
}

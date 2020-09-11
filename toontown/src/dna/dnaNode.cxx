// Filename: dnaNode.cxx
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////

#include "dnaNode.h"
#include "config_linmath.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNANode::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: DNANode::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNANode::DNANode(const string &initial_name) :
  DNAGroup(initial_name)
{
  _pos.set(0.0, 0.0, 0.0);
  _hpr.set(0.0, 0.0, 0.0);
  _scale.set(1.0, 1.0, 1.0);
}


////////////////////////////////////////////////////////////////////
//     Function: DNANode::CopyConstructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNANode::DNANode(const DNANode &copy) :
  DNAGroup(copy)
{
  _pos = copy.get_pos();
  _hpr = copy.get_hpr();
  _scale = copy.get_scale();
}



////////////////////////////////////////////////////////////////////
//     Function: DNANode::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNANode::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make a new node for this group
  PT(PandaNode) new_node = new PandaNode(get_name());
  NodePath node_path = parent.attach_new_node(new_node);

  node_path.set_pos_hpr_scale(_pos, _hpr, _scale);

  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *i;
    group->traverse(node_path, store, editing);
  }

  if (editing) {
    // Remember that this nodepath is associated with this dnaNode
    store->store_DNAGroup(node_path.node(), this);
  }

  return node_path;
}



////////////////////////////////////////////////////////////////////
//     Function: DNANode::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNANode::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "node ";
  out << '"' << get_name() << '"' << " [\n";

  // If none of the properties are set, do not write them out
  if ((!_pos.almost_equal(LVecBase3f::zero())) ||
      (!_hpr.almost_equal(LVecBase3f::zero())) ||
      (!_scale.almost_equal(LVecBase3f(1.0, 1.0, 1.0)))) {
    // Write out all properties
    indent(out, indent_level + 1) << "pos [ " <<
      _pos[0] << " " << _pos[1] << " " << _pos[2] << " ]\n";
    if (temp_hpr_fix) {
      indent(out, indent_level + 1) << "nhpr [ " <<
        _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
    } else {
      indent(out, indent_level + 1) << "hpr [ " <<
        _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
    }
    indent(out, indent_level + 1) << "scale [ " <<
      _scale[0] << " " << _scale[1] << " " << _scale[2] << " ]\n";
  }

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
//     Function: DNANode::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNANode::make_copy() {
  return new DNANode(*this);
}

// Filename: dnaDoor.cxx
// Created by:  shochet (27Jun00)
//
////////////////////////////////////////////////////////////////////

#include "dnaDoor.h"
#include "nodePath.h"
#include "dnaStorage.h"
#include "decalEffect.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNADoor::_type_handle;
TypeHandle DNAFlatDoor::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNADoor::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNADoor::DNADoor(const string &initial_name) :
  DNAGroup(initial_name) {
  _code = "";
  _color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNADoor::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNADoor::DNADoor(const DNADoor &door) :
  DNAGroup(door) {
  _code = door.get_code();
  _color = door.get_color();
}


////////////////////////////////////////////////////////////////////
//     Function: DNADoor::set_color
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNADoor::set_color(const Colorf &color) {
  _color = color;
}


////////////////////////////////////////////////////////////////////
//     Function: DNADoor::get_color
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
Colorf DNADoor::get_color() const {
  return _color;
}


////////////////////////////////////////////////////////////////////
//     Function: DNADoor::set_code
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNADoor::set_code(string code) {
  _code = code;
}


////////////////////////////////////////////////////////////////////
//     Function: DNADoor::get_code
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
string DNADoor::get_code() const {
  return _code;
}


////////////////////////////////////////////////////////////////////
//     Function: DNADoor::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNADoor::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make this a decal onto the wall
  // It should be the only geom node under a group ending with _front
  NodePath building_front = parent.find("**/*_front");
  nassertr(!building_front.is_empty(), parent);
  // If the _front is not a GeomNode, look for the first geom node under that
  if (!building_front.node()->is_geom_node()) {
    building_front = building_front.find("**/+GeomNode");
    nassertr(!building_front.is_empty(), parent);
  }

  PandaNode *node = building_front.node();
  node->set_effect(DecalEffect::make());

  // Try to find this door in the node map
  NodePath door_code = store->find_node(_code);
  if (door_code.is_empty()) {
    dna_cat.error()
      << "Door not found: " << _code << "\n";
    return parent;
  }

  NodePath door_node_path = door_code.copy_to(building_front);
  nassertr(!door_node_path.is_empty(), parent);
  // Doors do not have meaningful names so do not name them

  // The door_origin is a special node in the model with a local
  // origin that we position the door wrt
  NodePath door_origin = parent.find("**/*door_origin");
  nassertr(!door_origin.is_empty(), parent);

  string block=store->get_block(parent.node()->get_name());
  setup_door(door_node_path, parent, door_origin, store, block, _color);
  store->store_block_door_pos_hpr(block,
      door_origin.get_pos(NodePath()), door_origin.get_hpr(NodePath()));

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(door_node_path.node(), this);
  }

  // We don't traverse our children because there will not be any

  return door_node_path;
}

void DNADoor::setup_door(NodePath& door_node_path,
    NodePath& parent, NodePath& door_origin, DNAStorage *store,
    const string& block, const LVector4f& color) {
  // Place the door at the bottom center of the building,
  // three feet out from the origin where the wall is
  door_node_path.set_pos_hpr_scale(door_origin,
           LVector3f(0.0),
           LVector3f(0.0),
           LVector3f(1.0));
  door_node_path.set_color(color);

  // Rename the left hole in the door frame:
  NodePath doorFrameHoleLeft=door_node_path.find("door_*_hole_left");
  nassertv(!doorFrameHoleLeft.is_empty());
  doorFrameHoleLeft.node()->set_name("doorFrameHoleLeft");
  // Rename the right hole in the door frame:
  NodePath doorFrameHoleRight=door_node_path.find("door_*_hole_right");
  nassertv(!doorFrameHoleRight.is_empty());
  doorFrameHoleRight.node()->set_name("doorFrameHoleRight");

  // Rename the 3D door panels:
  NodePath rightDoor = door_node_path.find("door_*_right");
  nassertv(!rightDoor.is_empty());
  rightDoor.node()->set_name("rightDoor");
  // Repeat for the left door:
  NodePath leftDoor = door_node_path.find("door_*_left");
  nassertv(!leftDoor.is_empty());
  leftDoor.node()->set_name("leftDoor");

  // Move the hole onto the frame (aka "flat"):
  NodePath doorFrame = door_node_path.find("door_*_flat");
  if ( doorFrame.is_empty() )
    {
      // this door does not have a flat... always show the 
      // normal geometry
    }
  else
    {
      doorFrameHoleLeft.wrt_reparent_to(doorFrame);
      doorFrameHoleRight.wrt_reparent_to(doorFrame);
      PandaNode *doorFrameNode = doorFrame.node();
      doorFrameNode->set_effect(DecalEffect::make());

      // Move the 3D door panels out from the decal:
      rightDoor.wrt_reparent_to(parent);
      leftDoor.wrt_reparent_to(parent);

      // Hide the 3D door:
      rightDoor.hide();
      leftDoor.hide();
    }      

  doorFrameHoleLeft.hide();
  doorFrameHoleRight.hide();

  // Color the doors
  rightDoor.set_color(color);
  leftDoor.set_color(color);
  // Color the holes
  doorFrameHoleLeft.set_color(LVector4f(0.0, 0.0, 0.0, 1.0));
  doorFrameHoleRight.set_color(LVector4f(0.0, 0.0, 0.0, 1.0));

  // Set the trigger:
  NodePath doorTrigger = door_node_path.find("door_*_trigger");
  nassertv(!doorTrigger.is_empty());
  doorTrigger.wrt_reparent_to(parent);
  doorTrigger.node()->set_name("door_trigger_"+block);
}


////////////////////////////////////////////////////////////////////
//     Function: DNADoor::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNADoor::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "door [\n";

  // Write out all properties
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  indent(out, indent_level + 1) << "color [ " <<
    _color[0] << " " << _color[1] << " " << _color[2] << " " << _color[3] <<
    " ]\n";

  // We dont traverse our children because we do not have any
  indent(out, indent_level) << "]\n";
}

////////////////////////////////////////////////////////////////////
//     Function: DNADoor::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNADoor::make_copy() {
  return new DNADoor(*this);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAFlatDoor::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAFlatDoor::DNAFlatDoor(const string &initial_name) :
  DNADoor(initial_name) {
}

////////////////////////////////////////////////////////////////////
//     Function: DNAFlatDoor::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAFlatDoor::DNAFlatDoor(const DNAFlatDoor &door) :
  DNADoor(door) {
}

////////////////////////////////////////////////////////////////////
//     Function: DNAFlatDoor::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAFlatDoor::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Try to find this door in the node map
  NodePath door_node_path = (store->find_node(_code)).copy_to(parent);
  nassertr(!door_node_path.is_empty(), parent);
  // Doors do not have meaningful names so do not name them

  door_node_path.set_scale(NodePath(), 1, 1, 1);
  door_node_path.set_pos_hpr(0.5, 0, 0, 0, 0, 0);
  door_node_path.set_color(_color);

  if (editing) {
    // Make this a decal onto the walls
    PandaNode *node = parent.node();
    node->set_effect(DecalEffect::make());
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(door_node_path.node(), this);
  }

  // We don't traverse our children because there will not be any
  return door_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAFlatDoor::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAFlatDoor::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "flat_door [\n";

  // Write out all properties
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  indent(out, indent_level + 1) << "color [ " <<
    _color[0] << " " << _color[1] << " " << _color[2] << " " << _color[3] <<
    " ]\n";

  // We dont traverse our children because we do not have any
  indent(out, indent_level) << "]\n";
}


////////////////////////////////////////////////////////////////////
//     Function: DNAFlatDoor::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAFlatDoor::make_copy() {
  return new DNAFlatDoor(*this);
}

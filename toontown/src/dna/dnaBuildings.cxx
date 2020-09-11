// Filename: dnaBuildings.cxx
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////

#include "dnaBuildings.h"
#include "dnaStorage.h"
#include "modelNode.h"
#include "pandaNode.h"
#include "compose_matrix.h"
#include "luse.h"
#include "sceneGraphReducer.h"
#include "pointerTo.h"
#include "nodePathCollection.h"
#include "decalEffect.h"
#include "collisionSphere.h"
#include "config_linmath.h"

// For fixing encodings
// #include "textNode.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNAWall::_type_handle;
TypeHandle DNAFlatBuilding::_type_handle;
TypeHandle DNALandmarkBuilding::_type_handle;

float current_wall_height = 0.0;


////////////////////////////////////////////////////////////////////
//     Function: DNAWall::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAWall::DNAWall(const string &initial_name) :
  DNANode(initial_name)
{
  _code = "";
  _height = 10.0;
  _color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAWall::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAWall::DNAWall(const DNAWall &wall) :
  DNANode(wall)
{
  _code = wall.get_code();
  _height = wall.get_height();
  _color = wall.get_color();
}

////////////////////////////////////////////////////////////////////
//     Function: DNAWall::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAWall::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Try to find this building's walls and windows in the node map
  NodePath wall_node_path = (store->find_node(_code)).copy_to(parent);

  // Move the wall to the current height to stack on the previous one
  _pos.set_z(current_wall_height);

  // Scale it up, set properties
  _scale.set_z(_height);
  wall_node_path.set_pos_hpr_scale(_pos, _hpr, _scale);
  wall_node_path.set_color(_color);

  // Traverse each node in our vector
  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    PT(DNAGroup) group = *i;
    group->traverse(wall_node_path, store, editing);
  }

  // Only store the dnawall in the storage if we are in editing mode
  // otherwise it gets flattened by the flat building and will lose
  // this node
  if (editing) {
    store->store_DNAGroup(wall_node_path.node(), this);
  }

  // Update the current_wall_height so the next wall will be on top
  current_wall_height += _height;

  return wall_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAWall::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAWall::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "wall [\n";


  // Write out all properties
  indent(out, indent_level + 1) << "height [ " <<
    _height << " ]\n";
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  indent(out, indent_level + 1) << "color [ " <<
    _color[0] << " " << _color[1] << " " << _color[2] << " " << _color[3] <<
    " ]\n";

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
//     Function: DNAWall::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAWall::make_copy() {
  return new DNAWall(*this);
}


////////////////////////////////////////////////////////////////////
//     Function: DNAFlatBuilding::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAFlatBuilding::DNAFlatBuilding(const string &initial_name) :
  DNANode(initial_name)
{
  _width = 10.0;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAFlatBuilding::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAFlatBuilding::DNAFlatBuilding(const DNAFlatBuilding &building) :
  DNANode(building)
{
  _width = building.get_width();
}


////////////////////////////////////////////////////////////////////
//     Function: DNAFlatBuilding::setup_suit_flat_building
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
bool DNAFlatBuilding::has_door(PT(DNAGroup) parent_group) {
  int i=0;
  int limit=parent_group->get_num_children();
  for(; i < limit; ++i) {
    PT(DNAGroup) group = parent_group->at(i);
    nassertr(group, false);
    if (group->is_of_type(DNAFlatDoor::get_class_type())) {
      // ...found a door.
      return true;
    } else {
      if (has_door(group)) {
        return true;
      }
    }
  }
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAFlatBuilding::setup_suit_flat_building
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNAFlatBuilding::setup_suit_flat_building(NodePath &parent,
      DNAStorage *store) {
  // Get the toon building name:
  string name = get_name();
  if (!(name[0]=='t' &&
      name[1]=='b' &&
      isdigit(name[2]) &&
      name.find(':')!=string::npos)) {
    // ...this building is not setup to taken over.
    // Skip it:
    return;
  }
  // Make it a suit name:
  nassertv(name.length() > 0);
  name[0]='s';
  // Create the node to hang suit buildings on:
  // ModelNode is used to preserve the name of the node so that we can
  // do a find() for it later.
  PT(PandaNode) suit_node = new ModelNode(name);
  NodePath suit_building_node_path = parent.attach_new_node(suit_node);
  // Size and place it correctly:
  LVector3f scale = get_scale();
  scale[2]*=current_wall_height;
  suit_building_node_path.set_pos_hpr_scale(get_pos(), get_hpr(), scale);
  // Pick a suit wall:
  int count=store->get_num_catalog_codes("suit_wall");
  name=store->get_catalog_code("suit_wall", rand()%count);
  NodePath np=store->find_node(name);
  if (!np.is_empty()) {
    // Put it in the world:
    NodePath newNP=np.copy_to(suit_building_node_path);
    nassertv(!newNP.is_empty());
    // Look for a door:
    if (has_door(this)) {
      NodePath wall_node_path=suit_building_node_path.find("wall_*");
      nassertv(!wall_node_path.is_empty());
      NodePath door_node_path =
          (store->find_node("suit_door")).copy_to(wall_node_path);
      nassertv(!door_node_path.is_empty());
      door_node_path.set_scale(NodePath(), 1, 1, 1);
      door_node_path.set_pos_hpr(0.5, 0, 0, 0, 0, 0);
      //door_node_path.set_color(0.5, 0.5, 1.0, 1.0);
      wall_node_path.node()->set_effect(DecalEffect::make());
    }
  }
  // Flatten the wall to get rid of the pos hpr scale
  // The toon take over just uses a Z scale and does not need them
  suit_building_node_path.flatten_medium();
  suit_building_node_path.stash();
}

////////////////////////////////////////////////////////////////////
//     Function: DNAFlatBuilding::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAFlatBuilding::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Clear the current_wall_height so the first wall will be on the ground
  current_wall_height = 0;

  // Make a new building node
  NodePath building_node_path = parent.attach_new_node(get_name());
  // Create an extra node for flattening purposes
  NodePath internal_node_path = building_node_path.attach_new_node(get_name()+"-internal");

  // Set the scale on the internal node so it will get flattened out
  _scale.set_x(_width);
  internal_node_path.set_scale(_scale);

  // Set the pos and hpr on the top node so we can move it easily in the editor
  building_node_path.set_pos_hpr(_pos, _hpr);

  // Traverse each node in our vector
  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    PT(DNAGroup) group = *i;
    // Walls go under the internal_node_path because they need to pick up
    // the scaled width, everything else goes under the building node path
    // because they do not want that scale
    if (group->is_of_type(DNAWall::get_class_type())) {
      group->traverse(internal_node_path, store, editing);
    } else {
      group->traverse(building_node_path, store, editing);
    }
  }

  // For some reason the dna has some flat buildings with no walls
  // we should fix them as we find them
  if (current_wall_height == 0.0) {
    dna_cat.warning() << "empty flat building with no walls" << endl;
    return parent;
  }

  // Copy a camera barrier wall to us
  NodePath wall_camera_barrier_node_path =
    (store->find_node("wall_camera_barrier")).copy_to(internal_node_path);
  // Scale the camera collide geometry up to cover the entire wall
  wall_camera_barrier_node_path.set_scale(1.0, 1.0, current_wall_height);

  // Build origin for suit flat building:
  setup_suit_flat_building(parent, store);

  // Get rid of the transitions
  SceneGraphReducer gr;
  gr.apply_attribs(internal_node_path.node());

  // Do not flatten if we are editing because it will invalidate some
  // of the node relations we have stored on the walls
  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(building_node_path.node(), this);
  } else {
    // See if there is a door here:
    NodePath door_sphere_node_path = building_node_path.find(
        "**/door_*/+CollisionNode");
    if (!door_sphere_node_path.is_empty()) {
      // Rename the collision sphere:
      string block=store->get_block(get_name());
      door_sphere_node_path.node()->set_name("KnockKnockDoorSphere_"+block);
    }

    // Move the collision node up and out of here for better flattening
    wall_camera_barrier_node_path.wrt_reparent_to(parent);

    // Find all the walls under the internal node path
    NodePathCollection wall_collection = internal_node_path.find_all_matches("wall*");

    // Make a wall holder to temporarily store the wall nodes, so we
    // can flatten them all into a single node.
    NodePath wall_holder = building_node_path.attach_new_node("wall_holder");
    // Make a wall decal holder to temporarily store the cornice and windows
    NodePath wall_decal_holder = building_node_path.attach_new_node("wall_decal_holder");

    // Get all the windows, doors, and cornices
    NodePathCollection window_collection =
      internal_node_path.find_all_matches("**/window*");
    NodePathCollection door_collection =
      internal_node_path.find_all_matches("**/door*");
    NodePathCollection cornice_collection =
      internal_node_path.find_all_matches("**/cornice*_d");

    // Put the pieces in their holders
    wall_collection.reparent_to(wall_holder);
    window_collection.reparent_to(wall_decal_holder);
    door_collection.reparent_to(wall_decal_holder);
    cornice_collection.reparent_to(wall_decal_holder);

    // Before we flatten, remove the DNA tags.
    for (int i = 0; i < wall_holder.get_num_children(); ++i) {
      NodePath child = wall_holder.get_child(i);
      child.clear_tag("DNACode");
      child.clear_tag("DNARoot");
    }

    // Flatten the holders, combining siblings
    gr.flatten(wall_holder.node(), ~0);
    gr.flatten(wall_decal_holder.node(), ~0);

    // Now there should only be one wall geom node, make sure
    nassertr(wall_holder.get_num_children() == 1, parent);

    // Put the windows and cornice back under the wall
    NodePath wall = wall_holder.get_child(0);
    wall_decal_holder.get_children().reparent_to(wall);
    // Put the wall back under the internal node path
    wall.reparent_to(internal_node_path);

    // Flag this final wall as a decal
    wall.node()->set_effect(DecalEffect::make());

    // Get rid of these temp containers
    wall_holder.remove_node();
    wall_decal_holder.remove_node();

    // Now flatten everything again
    gr.flatten(building_node_path.node(), ~0);
  }

  return building_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAFlatBuilding::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAFlatBuilding::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "flat_building ";
  out << '"' << get_name() << '"' << " [\n";

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
  indent(out, indent_level + 1) << "width [ " <<
    _width << " ]\n";

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
//     Function: DNAFlatBuilding::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAFlatBuilding::make_copy() {
  return new DNAFlatBuilding(*this);
}


////////////////////////////////////////////////////////////////////
//     Function: DNALandmarkBuilding::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNALandmarkBuilding::DNALandmarkBuilding(const string &initial_name) :
  DNANode(initial_name)
{
  _code = "";
  _building_type = "";
  _wall_color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNALandmarkBuilding::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNALandmarkBuilding::DNALandmarkBuilding(const DNALandmarkBuilding &building) :
  DNANode(building)
{
  _code = building.get_code();
  _building_type = building.get_building_type();
  _wall_color = building.get_wall_color();
  _title = building.get_title();
  _article = building.get_article();
}


////////////////////////////////////////////////////////////////////
//     Function: DNALandmarkBuilding::setup_suit_building_origin
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNALandmarkBuilding::setup_suit_building_origin(NodePath &parent,
    NodePath &building_node_path) {
  // Copy the name from the toon building:
  string name = get_name();
  if (!(name[0]=='t' &&
      name[1]=='b' &&
      isdigit(name[2]) &&
      name.find(':')!=string::npos)) {
    // ...this building is not setup to taken over.
    // Skip it:
    return;
  }
  // Make it a suit name:
  nassertv(name.length() > 0);
  name[0]='s';
  NodePath np = building_node_path.find("**/*suit_building_origin");
  if (!np.is_empty()) {
    // Make the suit origin a peer of the toon building:
    np.wrt_reparent_to(parent);
    // Change the name:
    np.node()->set_name(name);
  } else {
    dna_cat.warning() << "DNALandmarkBuilding " << name
                      << " did not find **/*suit_building_origin" << endl;
    // Create the node to hang suit buildings on:
    NodePath suit_building_node_path = parent.attach_new_node(name);
    // Size and place it correctly:
    suit_building_node_path.set_pos_hpr_scale(get_pos(), get_hpr(), get_scale());
  }
}


////////////////////////////////////////////////////////////////////
//     Function: DNALandmarkBuilding::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNALandmarkBuilding::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Try to find this building in the node map
  NodePath building_node_path = (store->find_node(_code)).copy_to(parent);

  // Retain the name from the dna
  building_node_path.node()->set_name(get_name());

  // Do not set the color until we can blend
  // Actually we can blend now, but nobody is using color now
  // building_walls_node_path.set_color(_wall_color);

  // Set the building position
  building_node_path.set_pos_hpr_scale(_pos, _hpr, _scale);

  // Remember the article and title of the building, for later:
  string block=store->get_block(get_name());
  store->store_block_title(block, _title);
  store->store_block_article(block, _article);

  // Copy the suit building origin to the parent:
  if (get_building_type() == "") {
    // head quarters have no building origin
    setup_suit_building_origin(parent, building_node_path);
  }

  // Traverse each node in our vector
  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    PT(DNAGroup) group = *i;
    group->traverse(building_node_path, store, editing);
  }

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(building_node_path.node(), this);
  }
  else {
    SceneGraphReducer gr;
    // Get rid of the transitions
    gr.apply_attribs(building_node_path.node());
    gr.flatten(building_node_path.node(), ~0);

    // HQs need the door_origins around because they do not have dnaDoors
    if (get_building_type() != string("hq")) {
      // Get rid of these placement origins since we do not need them anymore
      NodePath door_origin = building_node_path.find("**/*door_origin");
      if (!door_origin.is_empty()) {
        door_origin.remove_node();
      }
    }
    NodePath sign_origin = building_node_path.find("**/*sign_origin");
    if (!sign_origin.is_empty()) {
      sign_origin.remove_node();
    }
  }
  return building_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNALandmarkBuilding::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNALandmarkBuilding::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "landmark_building ";
  out << '"' << get_name() << '"' << " [\n";

  // Write out all properties
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  if (!get_building_type().empty()) {
    indent(out, indent_level + 1) << "building_type [ " << '"' << get_building_type() << '"' << " ]\n";
  }

  // Whoops, the titles were entered as iso8859 and we need to convert them to utf8 
  // We only want to run this when we need to fix an improper encoding
  // Note - you need to change the indent function below too
  // string utf8title = TextNode::reencode_text(_title, TextNode::E_iso8859, TextNode::E_utf8);
  if (!_article.empty()) {
    indent(out, indent_level + 1) << "article [ " << '"' <<
      _article << '"' << " ]\n";
  }
  indent(out, indent_level + 1) << "title [ " << '"' <<
    _title << '"' << " ]\n";
  indent(out, indent_level + 1) << "pos [ " <<
    _pos[0] << " " << _pos[1] << " " << _pos[2] << " ]\n";
  if (temp_hpr_fix) {
    indent(out, indent_level + 1) << "nhpr [ " <<
      _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
  } else {
    indent(out, indent_level + 1) << "hpr [ " <<
      _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
  }

  // Do not write out color if it is white to save work
  if (!_wall_color.almost_equal(LVecBase4f(1.0, 1.0, 1.0, 1.0))) {
    indent(out, indent_level + 1) << "color [ " <<
      _wall_color[0] << " " << _wall_color[1] << " " << _wall_color[2] << " " << _wall_color[3] <<
      " ]\n";
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
//     Function: DNALandmarkBuilding::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNALandmarkBuilding::make_copy() {
  return new DNALandmarkBuilding(*this);
}


// Filename: dnaStorage.I
// Created by:  shochet (29Mar00)
//
////////////////////////////////////////////////////////////////////

#include "texture.h"
#include "modelRoot.h"


////////////////////////////////////////////////////////////////////
//     Function: store_node
//       Access: Public
//  Description: Store a node pointer in the node map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::store_node(const string &code_string, NodePath node, const string &code_category) {
  if ((code_category == "holiday_prop") && !(node.node()->is_of_type(ModelNode::get_class_type()))) {
    // These should not be flattened
    NodePath modelNode(new ModelNode(node.get_name()));
    node.copy_to(modelNode);
    node = modelNode;
  }
  node.set_tag("DNACode", code_string);
  node.set_tag("DNARoot", code_category);
  _node_map[code_string] = node;
}


////////////////////////////////////////////////////////////////////
//     Function: store_hood_node
//       Access: Public
//  Description: Store a neighborhood specific node pointer in the
//               hood node map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::store_hood_node(const string &code_string, NodePath node, const string &code_category) {
  if ((code_category == "holiday_prop") && !(node.node()->is_of_type(ModelNode::get_class_type()))) {
    // These should not be flattened
    NodePath modelNode(new ModelNode(node.get_name()));
    node.copy_to(modelNode);
    node = modelNode;
  }
  node.set_tag("DNACode", code_string);
  node.set_tag("DNARoot", code_category);
  _hood_node_map[code_string] = node;
}

////////////////////////////////////////////////////////////////////
//     Function: store_place_node
//       Access: Public
//  Description: Store a neighborhood specific node pointer in the
//               place node map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::store_place_node(const string &code_string, NodePath node, const string &code_category) {
  if ((code_category == "holiday_prop") && !(node.node()->is_of_type(ModelNode::get_class_type()))) {
    // These should not be flattened
    NodePath modelNode(new ModelNode(node.get_name()));
    node.copy_to(modelNode);
    node = modelNode;
  }
  node.set_tag("DNACode", code_string);
  node.set_tag("DNARoot", code_category);
  _place_node_map[code_string] = node;
}


////////////////////////////////////////////////////////////////////
//     Function: reset_nodes
//       Access: Public
//  Description: clear out the map of shared nodes
//               so the ref counter will delete them
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_nodes() {
  _node_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_textures
//       Access: Public
//  Description: clear out the map of shared textures
//               so the ref counter will delete them
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_textures() {
  _texture_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_hood
//       Access: Public
//  Description: clear out everything associated with the current hood
//               this is called in Python whenever we leave a hood. It
//               is easier to add things here than to have to keep
//               updating the showcode.
//               Reseting the hood also resets the place nodes.
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_hood() {
  reset_hood_nodes();
  reset_place_nodes();
  reset_suit_points();
  reset_battle_cells();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_hood_nodes
//       Access: Public
//  Description: clear out the map of neighborhood specific nodes
//               so the ref counter will delete them
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_hood_nodes() {
  _hood_node_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_place_nodes
//       Access: Public
//  Description: clear out the map of town and sz specific nodes
//               so the ref counter will delete them
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_place_nodes() {
  _place_node_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_suit_points
//       Access: Public
//  Description: clear out all maps relating to suit points
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_suit_points() {
  _suit_point_vector.clear();
  _suit_point_map.clear();
  _suit_start_point_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_battle_cells
//       Access: Public
//  Description: clear out all battle cells
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_battle_cells() {
  _battle_cell_vector.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_DNAGroups
//       Access: Public
//  Description: clear out the map of DNAGroups
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_DNAGroups() {
  _n2group_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: store_DNAVisGroup
//       Access: Public
//  Description: store a DNAVisGroup at the node path pointer
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::store_DNAVisGroup(PT(PandaNode) rr, PT(DNAVisGroup) group) {
  nassertv(rr != (PandaNode *)NULL);
  nassertv(group != (DNAVisGroup *)NULL);

  _n2visgroup_map[rr] = group;
}


////////////////////////////////////////////////////////////////////
//     Function: remove_DNAVisGroup
//       Access: Public
//  Description: remove the DNAVisGroup pointed to by rr from the map
////////////////////////////////////////////////////////////////////
INLINE int DNAStorage::remove_DNAVisGroup(PT(PandaNode) rr) {
  nassertr(rr != (PandaNode *)NULL, 0);
  return _n2visgroup_map.erase(rr);
}


////////////////////////////////////////////////////////////////////
//     Function: reset_DNAVisGroups
//       Access: Public
//  Description: clear out the map of DNAVisGroups
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_DNAVisGroups() {
  _n2visgroup_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_DNAVisGroups
//       Access: Public
//  Description: Ask how many vis groups this dna store knows about
////////////////////////////////////////////////////////////////////
INLINE int DNAStorage::get_num_DNAVisGroups() const {
  return _n2visgroup_map.size();
}



////////////////////////////////////////////////////////////////////
//     Function: get_num_DNAVisGroupsAI
//       Access: Public
//  Description: Ask how many vis groups this dna store knows about
////////////////////////////////////////////////////////////////////
INLINE int DNAStorage::get_num_DNAVisGroupsAI() const {
  return _vis_group_vector.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_DNAVisGroupAI
//       Access: Public
//  Description: Return the ith vis group in our storage
////////////////////////////////////////////////////////////////////
INLINE PT(DNAVisGroup) DNAStorage::get_DNAVisGroupAI(uint i) const {
  nassertr(i < _vis_group_vector.size(), (DNAVisGroup *)NULL);
  return _vis_group_vector[i];
}


////////////////////////////////////////////////////////////////////
//     Function: reset_block_door_pos_hpr
//       Access: Public
//  Description: clear out the map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_block_door_pos_hprs() {
  _block_door_pos_hpr_map.clear();
}

////////////////////////////////////////////////////////////////////
//     Function: reset_block_sign_transform
//       Access: Public
//  Description: clear out the map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_block_sign_transforms() {
  _block_sign_transform_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_block_title
//       Access: Public
//  Description: clear out the map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_block_title() {
  _block_title_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_block_number
//       Access: Public
//  Description: clear out the map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_block_numbers() {
  _block_map.clear();
}

////////////////////////////////////////////////////////////////////
//     Function: reset_block_article
//       Access: Public
//  Description: clear out the map
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_block_article() {
  _block_article_map.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: reset_DNAVisGroupsAI
//       Access: Public
//  Description: clear out the vector of DNAVisGroups
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::reset_DNAVisGroupsAI() {
  _vis_group_vector.clear();
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_PandaNodes
//       Access: Public
//  Description: how many node paths do we have in our map
////////////////////////////////////////////////////////////////////
INLINE int DNAStorage::get_num_PandaNodes() const {
  return _n2group_map.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_suit_points
//       Access: Public
//  Description: How many suit points are in the map now?
////////////////////////////////////////////////////////////////////
INLINE int DNAStorage::get_num_suit_points() const {
  return _suit_point_vector.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_suit_point_at_index
//       Access: Private
//  Description: Convient way to return the point at index internally
////////////////////////////////////////////////////////////////////
INLINE PT(DNASuitPoint) DNAStorage::get_suit_point_at_index(int index) const {
  nassertr(index < (int)_suit_point_vector.size(), (DNASuitPoint *)NULL);
  return _suit_point_vector[index];
}


////////////////////////////////////////////////////////////////////
//     Function: get_suit_point_with_index
//       Access: Private
//  Description: Convient way to return the point at index internally
////////////////////////////////////////////////////////////////////
INLINE PT(DNASuitPoint) DNAStorage::get_suit_point_with_index(int index) const {
  SuitPointMap::const_iterator si = _suit_point_map.find(index);
  nassertr(si != _suit_point_map.end(), (DNASuitPoint *)NULL);
  return (*si).second;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::Constructor
//       Access: Public
//  Description: Constructs the head of the path.
////////////////////////////////////////////////////////////////////
INLINE DNAStorage::WorkingSuitPath::
WorkingSuitPath(int point_index) {
  _next_deleted = (WorkingSuitPath *)NULL;
  _point_index = point_index;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::Constructor
//       Access: Public
//  Description: Constructs the next element of a path.
////////////////////////////////////////////////////////////////////
INLINE DNAStorage::WorkingSuitPath::
WorkingSuitPath(WorkingSuitPath *next, int point_index) {
  _next_in_path = next;
  _next_deleted = (WorkingSuitPath *)NULL;
  _point_index = point_index;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::Destructor
//       Access: Public
//  Description: 
////////////////////////////////////////////////////////////////////
INLINE DNAStorage::WorkingSuitPath::
~WorkingSuitPath() {
  // We set this just so we can prove it's still set later, and also
  // to help detect when we accidentally delete path components.
  _point_index = -101;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::get_point_index
//       Access: Public
//  Description: Returns the index of the suit point this path element
//               refers to.
////////////////////////////////////////////////////////////////////
INLINE int DNAStorage::WorkingSuitPath::
get_point_index() const {
  return _point_index;
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::operator new
//       Access: Public
//  Description: Allocates the memory for a new WorkingSuitPath.  This
//               is specialized here to provide for fast allocation of
//               these things (since we may create and destroy
//               thousands of these each frame).
////////////////////////////////////////////////////////////////////
INLINE void *DNAStorage::WorkingSuitPath::
operator new(size_t size) {
  if (_deleted_chain != (WorkingSuitPath *)NULL) {
    WorkingSuitPath *obj = _deleted_chain;
    _deleted_chain = _deleted_chain->_next_deleted;
    nassertr(obj->_point_index == -101, ::operator new(size));
    return obj;
  }
  return ::operator new(size);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::operator delete
//       Access: Public
//  Description: Frees the memory for a deleted WorkingSuitPath.  This
//               is specialized here to provide for fast allocation of
//               these things (since we may create and destroy
//               thousands of these each frame).
////////////////////////////////////////////////////////////////////
INLINE void DNAStorage::WorkingSuitPath::
operator delete(void *ptr) {
  WorkingSuitPath *obj = (WorkingSuitPath *)ptr;
  nassertv(obj->_point_index == -101);

  // As tempting as it is, we can't use either the _next_in_path or
  // the _next_in_chain members to store the next deleted pointer,
  // because those are reference-counting pointers, and these objects
  // have already been destructed.  We use _next_deleted instead,
  // which is set aside for just this purpose.  Yeah, it's a small
  // waste of memory; deal with it.
  
  obj->_next_deleted = _deleted_chain;
  _deleted_chain = obj;
}

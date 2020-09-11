// Filename: dnaStorage.cxx
// Created by:  shochet (29Mar00)
//
////////////////////////////////////////////////////////////////////

#include "dnaStorage.h"
#include <deque>

DNAStorage::WorkingSuitPath *DNAStorage::WorkingSuitPath::_deleted_chain = (DNAStorage::WorkingSuitPath *)NULL;

////////////////////////////////////////////////////////////////////
//     Function: Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAStorage::DNAStorage() {
}


////////////////////////////////////////////////////////////////////
//     Function: print_node_storage
//       Access: Public
//  Description: Print out the key/pointer pairs
////////////////////////////////////////////////////////////////////
void DNAStorage::print_node_storage() const {
  cout << "Model Pool Nodes" << endl;
  for(NodeMap::const_iterator i = _node_map.begin();
      i != _node_map.end();
      ++i) {
    cout << "\t(" << (*i).first << " " << (*i).second << ") " << endl;
  }
  cout << "Hood Nodes" << endl;
  for(NodeMap::const_iterator h = _hood_node_map.begin();
      h != _hood_node_map.end();
      ++h) {
    cout << "\t(" << (*h).first << " " << (*h).second << ") " << endl;
  }
  cout << "Place Nodes" << endl;
  for(NodeMap::const_iterator p = _place_node_map.begin();
      p != _place_node_map.end();
      ++p) {
    cout << "\t(" << (*p).first << " " << (*p).second << ") " << endl;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: print_texture_storage
//       Access: Public
//  Description: Print out the key/pointer pairs
////////////////////////////////////////////////////////////////////
void DNAStorage::print_texture_storage() const {
  for(TextureMap::const_iterator i = _texture_map.begin();
      i != _texture_map.end();
      ++i) {
    cout << "\t(" << (*i).first << " " << (*i).second << ") " << endl;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: print_font_storage
//       Access: Public
//  Description: Print out the key/pointer pairs
////////////////////////////////////////////////////////////////////
void DNAStorage::print_font_storage() const {
  for(FontMap::const_iterator i = _font_map.begin();
      i != _font_map.end();
      ++i) {
    cout << "\t(" << (*i).first << " " << (*i).second << ") " << endl;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: print_suit_point_storage
//       Access: Public
//  Description: Print out the key/pointer pairs
////////////////////////////////////////////////////////////////////
void DNAStorage::print_suit_point_storage() const {
  cout << "Suit points" << endl;
  for(SuitPointVector::const_iterator i = _suit_point_vector.begin();
      i != _suit_point_vector.end();
      ++i) {
    // To output the actual point, we need to dereference the PointerTo
    cout << "\t" << *(*i) << endl;
  }
  cout << "Suit edges" << endl;
  for(SuitStartPointMap::const_iterator si = _suit_start_point_map.begin();
      si != _suit_start_point_map.end();
      ++si) {
    cout << "\tIndex: " << (*si).first << endl;
    for(SuitEdgeVector::const_iterator evi = ((*si).second).begin();
        evi != ((*si).second).end();
        ++evi) {
      // To output the actual edge, we need to dereference the PointerTo
      cout << "\t  Edge: " << *((*evi)) << endl;
      }
  }
}


////////////////////////////////////////////////////////////////////
//     Function: print_battle_cell_storage
//       Access: Public
//  Description: Print out the battle cells
////////////////////////////////////////////////////////////////////
void DNAStorage::print_battle_cell_storage() const {
  for(BattleCellVector::const_iterator i = _battle_cell_vector.begin();
      i != _battle_cell_vector.end();
      ++i) {
    // To output the actual battle cell, we need to dereference the PointerTo
    cout << "Battle cell: " << *(*i) << endl;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: store_texture
//       Access: Public
//  Description: Store a texture pointer in the texture map
////////////////////////////////////////////////////////////////////
void DNAStorage::store_texture(const string &code_string, PT(Texture) texture) {
  nassertv(texture != (Texture *)NULL);
  // Assume all these textures are mipmap. Actually it should
  // match the textures.txa, but how do I know what is in there?
  // Note: take these out when we have a better solution for getting
  // and setting these parameters
  texture->set_minfilter(Texture::FT_linear_mipmap_linear);
  texture->set_magfilter(Texture::FT_linear);
  texture->set_anisotropic_degree(4);
  _texture_map[code_string] = texture;
}

////////////////////////////////////////////////////////////////////
//     Function: store_font
//       Access: Public
//  Description: Store a font pointer in the font map
////////////////////////////////////////////////////////////////////
void DNAStorage::store_font(const string &code_string, PT(TextFont) font) {
  nassertv(font != (TextFont *)NULL);
  _font_map[code_string] = font;
}

////////////////////////////////////////////////////////////////////
//     Function: store_suit_point
//       Access: Public
//  Description: Store a point in the suit point map. If that pos
//               already exists, return the existing point, otherwise
//               create a new point and store that.
////////////////////////////////////////////////////////////////////
PT(DNASuitPoint) DNAStorage::store_suit_point(DNASuitPoint::DNASuitPointType type,
                                              LPoint3f pos) {
  for(SuitPointVector::const_iterator i = _suit_point_vector.begin();
      i != _suit_point_vector.end();
      ++i) {
    // See if this point pos is close enough to the pos passed in
    PT(DNASuitPoint) point = (*i);
    // Do not check the type anymore
    // if ((type == point->get_point_type()) &&
    if (pos.almost_equal(point->get_pos(), 0.9)) {
      // Found it, return the existing point
      return point;
    }
  }

  // If we got here, we did not find the point in the map
  // Create a new one
  int index = get_highest_suit_point_index() + 1;
  PT(DNASuitPoint) point = new DNASuitPoint(index, type, pos);
  // Ok, now actually store the point
  store_suit_point(point);
  return point;
}



////////////////////////////////////////////////////////////////////
//     Function: store_suit_point
//       Access: Public
//  Description: Store a suit point in the suit point map
////////////////////////////////////////////////////////////////////
int DNAStorage::store_suit_point(PT(DNASuitPoint) point) {
  nassertr(point != (DNASuitPoint *)NULL, -1);
  _suit_point_vector.push_back(point);
  // NOTE: perhaps this should check to make sure there is
  // not one there already
  _suit_point_map[point->get_index()] = point;
  return point->get_index();
}


int DNAStorage::get_highest_suit_point_index() {
  int highest = -1;
  int index = 0;

  // Iterate all the suit points looking for the highest index
  for(SuitPointVector::const_iterator i = _suit_point_vector.begin();
      i != _suit_point_vector.end();
      ++i) {

    index = (*i)->get_index();
    if (index > highest) {
      highest = index;
    }
  }
  return highest;
}


////////////////////////////////////////////////////////////////////
//     Function: fix_coincident_suit_points
//       Access: Public
//  Description: Runs through the list of suit points fixing
//               any points that are coincident by deleting the
//               duplicates and patching up the effected edges
////////////////////////////////////////////////////////////////////
int DNAStorage::fix_coincident_suit_points() {

  int num_repeats = 0;
  PT(DNASuitPoint) point1;
  PT(DNASuitPoint) point2;

  // Iterate over the point vector. With each point in the vector, check
  // every other point to see if they are "almost_equal"
  // Note: this will double report them
  for(SuitPointVector::const_iterator i = _suit_point_vector.begin();
      i != _suit_point_vector.end();
      ++i) {

    point1 = (*i);

    for(SuitPointVector::const_iterator ii = _suit_point_vector.begin();
        ii != _suit_point_vector.end();
        ++ii) {
      point2 = (*ii);
      // Do not count being almost equal to yourself
      if ((point1 != point2) &&
          (point1->get_pos().almost_equal(point2->get_pos(), 0.9))) {
        dna_cat.info() << "found coincident points: " << point1->get_index() << ": " << point1->get_point_type()
                       << ", " << point2->get_index() << ": " << point2->get_point_type() << endl;

        // TODO:
        // remove from the SuitPointMap
        // remove from the SuitStartPointMap
        // remove edges in dnaStorage that contain this point
        // remove edges in any visgroups that contain this point

        num_repeats++;
      }
    }
  }
  // Return the number of matches we found
  dna_cat.debug() << "fixed " << num_repeats << " suit points" << endl;
  return num_repeats;
}


////////////////////////////////////////////////////////////////////
//     Function: delete_unused_suit_points
//       Access: Public
//  Description: Runs through the list of suit points deleting
//               any points that are not on any edges.
//               This is computationally expensive, but it is only run
//               when we save the dna in the editor, not at run time.
////////////////////////////////////////////////////////////////////
int DNAStorage::delete_unused_suit_points() {
  int num_deleted = 0;
  int used = 0;
  PT(DNASuitPoint) point;
  PT(DNASuitEdge) edge;

  // Iterate over all the suit points
  for(SuitPointVector::iterator i = _suit_point_vector.begin();
      i != _suit_point_vector.end();
      ++i) {
    point = (*i);
    used = 0;

    // First, try to find this start_index in the map
    SuitStartPointMap::const_iterator si = _suit_start_point_map.find(point->get_index());
    if (si != _suit_start_point_map.end()) {
      // It is being used, so do not delete it.
      used = 1;
      // Go on to the next point.
      continue;
    }

    // Check all the edges in all the vis groups to see if we use this point
    for(VisGroupVectorAI::const_iterator vi = _vis_group_vector.begin();
        vi != _vis_group_vector.end();
        ++vi) {
      int num_suit_edges = (*vi)->get_num_suit_edges();
      for (int e=0; e < num_suit_edges; e++) {
        edge = (*vi)->get_suit_edge(e);
        if ((point == edge->get_start_point()) ||
            (point == edge->get_end_point())) {
          // This point is used, stop looking
          used = 1;
          break;
        }
      }
      if (used) {
        break;
      }
    }

    if (!used) {
      // Delete the point from the suit point vector
      dna_cat.info() << "deleting unused point " << *point << endl;
      _suit_point_vector.erase(i--);
      num_deleted++;
    }
  }

  // Return the number of matches we found
  dna_cat.debug() << "deleted " << num_deleted << " suit points" << endl;
  return num_deleted;
}



////////////////////////////////////////////////////////////////////
//     Function: remove_suit_point
//       Access: Public
//  Description: Remove a suit point from the suit point map
//               Returns the number of points removed (0 or 1)
////////////////////////////////////////////////////////////////////
int DNAStorage::remove_suit_point(PT(DNASuitPoint) point) {
  nassertr(point != (DNASuitPoint *)NULL, 0);
  int result = 0;
  PT(DNASuitEdge) edge;

  // Iterate over all the start points
  for(SuitStartPointMap::iterator si = _suit_start_point_map.begin();
      si != _suit_start_point_map.end();
      ++si) {
    // For each start point, iterate over the edges that use that start point
    for(SuitEdgeVector::iterator evi = (*si).second.begin();
        evi != (*si).second.end();
        ++evi) {

      edge = (*evi);

      // See if this point is in this edge. If it is, remove the edge
      if ((point == edge->get_start_point()) ||
          (point == edge->get_end_point())) {
        dna_cat.warning() <<  "removing edge containing point " << *(edge) << endl;

        // Erase this edge from this vector, decrementing the iterator
        // so we do not invalidate it when erasing an element it was pointing to
        (*si).second.erase(evi--);

        // remove the edge from any vis groups that contain it
        for(VisGroupVectorAI::iterator vi = _vis_group_vector.begin();
            vi != _vis_group_vector.end();
            ++vi) {
          if ((*vi)->remove_suit_edge(edge)) {
            dna_cat.debug() << "removed edge from vis group " << (*vi)->get_name() << endl;
          }
        }
      }
    }
  }

  // Erase the point from the suit start point map
  result += _suit_start_point_map.erase(point->get_index());

  // Erase the point from the suit point vector
  SuitPointVector::iterator pi = find(_suit_point_vector.begin(),
                                      _suit_point_vector.end(),
                                      point);
  if (pi != _suit_point_vector.end()) {
    _suit_point_vector.erase(pi);
    result += 1;
  }

  return result;
}


////////////////////////////////////////////////////////////////////
//     Function: store_block_number
//       Access: Public
//  Description: Store a block and zone
////////////////////////////////////////////////////////////////////
void DNAStorage::store_block_number(const string& block, const string& zone_id) {
  nassertv(!block.empty());
  nassertv(!zone_id.empty());
  // Get the block number (e.g. in "tb22:blah_blah" the block number is "22").
  string block_num = block.substr(2, block.find(':')-2);
  _block_map[atoi(block_num.c_str())]=atoi(zone_id.c_str());
}


////////////////////////////////////////////////////////////////////
//     Function: get_zone_from_block_number
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
int DNAStorage::get_zone_from_block_number(int block_number) const {
  // Try to find this code in the map
  BlockToZoneMap::const_iterator i = _block_map.find(block_number);
  if (i == _block_map.end()) {
    dna_cat.error()
      << "block number: " << block_number << " not found in map" << endl;
    return 0;
  }
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_block_number
//       Access: Public
//  Description: Ask how many block numbers
////////////////////////////////////////////////////////////////////
int DNAStorage::get_num_block_numbers() const {
  return _block_map.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_block_number_at
//       Access: Public
//  Description: Get key at index
////////////////////////////////////////////////////////////////////
int DNAStorage::get_block_number_at(uint index) const {
  nassertr(index < _block_map.size(), 0);

  uint current = 0;

  // Loop over the map entries:
  for(BlockToZoneMap::const_iterator it = _block_map.begin();
      it != _block_map.end();
      ++it) {
    if (index == current) {
      nassertr((*it).first != 0, 0);
      return (*it).first;
    }
    current++;
  }

  dna_cat.error()
    << "DNAStorage::get_block_number_at index not found, returning 0"
    << endl;
  return 0;
}


////////////////////////////////////////////////////////////////////
//     Function: store_block_door_pos_hpr
//       Access: Public
//  Description: Store a block and zone
////////////////////////////////////////////////////////////////////
void DNAStorage::store_block_door_pos_hpr(const string& block,
    const LPoint3f& pos,
    const LPoint3f& hpr) {
  nassertv(!block.empty());
  _block_door_pos_hpr_map[atoi(block.c_str())]=PosHpr(pos, hpr);
}


////////////////////////////////////////////////////////////////////
//     Function: get_door_pos_hpr_from_block_number
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
const PosHpr& DNAStorage::get_door_pos_hpr_from_block_number(int block_number) const {
  // Try to find this code in the map
  BlockToPosHprMap::const_iterator i = _block_door_pos_hpr_map.find(block_number);
  if (i == _block_door_pos_hpr_map.end()) {
    dna_cat.error()
      << "block number: " << block_number << " not found in map" << endl;
    static PosHpr blank;
    return blank;
  }
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_block_door_pos_hprs
//       Access: Public
//  Description: Ask how many block numbers
////////////////////////////////////////////////////////////////////
int DNAStorage::get_num_block_door_pos_hprs() const {
  return _block_door_pos_hpr_map.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_door_pos_hpr_block_at
//       Access: Public
//  Description: Get key at index
////////////////////////////////////////////////////////////////////
int DNAStorage::get_door_pos_hpr_block_at(uint index) const {
  nassertr(index < _block_door_pos_hpr_map.size(), 0);

  uint current = 0;

  // Loop over the map entries:
  for(BlockToPosHprMap::const_iterator it = _block_door_pos_hpr_map.begin();
      it != _block_door_pos_hpr_map.end();
      ++it) {
    if (index == current) {
      nassertr((*it).first != 0, 0);
      return (*it).first;
    }
    current++;
  }

  dna_cat.error()
    << "DNAStorage::get_door_pos_hpr_block_at index not found, returning 0"
    << endl;
  return 0;
}


////////////////////////////////////////////////////////////////////
//     Function: store_block_sign_transform
//       Access: Public
//  Description: Store a block and zone
////////////////////////////////////////////////////////////////////
void DNAStorage::store_block_sign_transform(const string& block,
                                            const LMatrix4f& mat) {
  nassertv(!block.empty());
  _block_sign_transform_map[atoi(block.c_str())]=mat;
}


////////////////////////////////////////////////////////////////////
//     Function: get_sign_transform_from_block_number
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
const LMatrix4f& DNAStorage::get_sign_transform_from_block_number(int block_number) const {
  // Try to find this code in the map
  BlockToTransformMap::const_iterator i = _block_sign_transform_map.find(block_number);
  if (i == _block_sign_transform_map.end()) {
    dna_cat.error()
      << "block number: " << block_number << " not found in map" << endl;
    return LMatrix4f::ident_mat();
  }
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_block_sign_transforms
//       Access: Public
//  Description: Ask how many block numbers
////////////////////////////////////////////////////////////////////
int DNAStorage::get_num_block_sign_transforms() const {
  return _block_sign_transform_map.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_sign_transform_block_at
//       Access: Public
//  Description: Get key at index
////////////////////////////////////////////////////////////////////
int DNAStorage::get_sign_transform_block_at(uint index) const {
  nassertr(index < _block_sign_transform_map.size(), 0);

  uint current = 0;

  // Loop over the map entries:
  for(BlockToTransformMap::const_iterator it = _block_sign_transform_map.begin();
      it != _block_sign_transform_map.end();
      ++it) {
    if (index == current) {
      nassertr((*it).first != 0, 0);
      return (*it).first;
    }
    current++;
  }

  dna_cat.error()
    << "DNAStorage::get_sign_transform_block_at index not found, returning 0"
    << endl;
  return 0;
}


////////////////////////////////////////////////////////////////////
//     Function: store_block_title
//       Access: Public
//  Description: Store a block and zone
////////////////////////////////////////////////////////////////////
void DNAStorage::store_block_title(const string& block,
    const string& title) {
  nassertv(!block.empty());
  _block_title_map[atoi(block.c_str())]=title;
}




////////////////////////////////////////////////////////////////////
//     Function: get_title_from_block_number
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
string DNAStorage::get_title_from_block_number(int block_number) const {
  // Try to find this code in the map
  BlockToTitleMap::const_iterator i = _block_title_map.find(block_number);
  if (i == _block_title_map.end()) {
    dna_cat.error()
      << "block number: " << block_number << " not found in title map" << endl;
    return "";
  }
  return (*i).second;
}

////////////////////////////////////////////////////////////////////
//     Function: store_block_article
//       Access: Public
//  Description: Store a block and zone
////////////////////////////////////////////////////////////////////
void DNAStorage::store_block_article(const string& block,
    const string& article) {
  nassertv(!block.empty());
  _block_article_map[atoi(block.c_str())]=article;
}

////////////////////////////////////////////////////////////////////
//     Function: get_article_from_block_number
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
string DNAStorage::get_article_from_block_number(int block_number) const {
  // Try to find this code in the map
  BlockToArticleMap::const_iterator i = _block_article_map.find(block_number);
  if (i == _block_article_map.end()) {
    dna_cat.error()
      << "block number: " << block_number << " not found in article map" << endl;
    return "";
  }
  return (*i).second;
}

////////////////////////////////////////////////////////////////////
//     Function: store_block_building_type
//       Access: Public
//  Description: Store a block and zone
////////////////////////////////////////////////////////////////////
void DNAStorage::
store_block_building_type(const string& block, const string& type) {
  nassertv(!block.empty());
  // Get the block number (e.g. in "tb22:blah_blah" the block number is "22").
  string block_num = block.substr(2, block.find(':')-2);
  dna_cat.debug()
    << "block: " << block << "blocknum: " << block_num << " type:" << type << endl;
  _block_building_type_map[atoi(block_num.c_str())]=type;
}

////////////////////////////////////////////////////////////////////
//     Function: get_block_building_type
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
string DNAStorage::get_block_building_type(int block_number) const {
  // Try to find this code in the map
  BlockToBuildingTypeMap::const_iterator i = _block_building_type_map.find(block_number);
  // If it is not found, consider it false
  if (i == _block_building_type_map.end()) {
    dna_cat.debug()
      << "block number: " << block_number << " not found in building type map" << endl;
    return "";
  }
  return (*i).second;
}

////////////////////////////////////////////////////////////////////
//     Function: get_num_block_titles
//       Access: Public
//  Description: Ask how many block numbers
////////////////////////////////////////////////////////////////////
int DNAStorage::get_num_block_titles() const {
  return _block_title_map.size();
}


////////////////////////////////////////////////////////////////////
//     Function: get_title_block_at
//       Access: Public
//  Description: Get key at index
////////////////////////////////////////////////////////////////////
int DNAStorage::get_title_block_at(uint index) const {
  nassertr(index < _block_title_map.size(), 0);

  uint current = 0;

  // Loop over the map entries:
  for(BlockToTitleMap::const_iterator it = _block_title_map.begin();
      it != _block_title_map.end();
      ++it) {
    if (index == current) {
      nassertr((*it).first != 0, 0);
      return (*it).first;
    }
    current++;
  }

  dna_cat.error()
    << "DNAStorage::get_title_block_at index not found, returning 0"
    << endl;
  return 0;
}


////////////////////////////////////////////////////////////////////
//     Function: store_battle_cell
//       Access: Public
//  Description: Store a battle cell in the battle cell vector
////////////////////////////////////////////////////////////////////
void DNAStorage::store_battle_cell(PT(DNABattleCell) cell) {
  nassertv(cell != (DNABattleCell *)NULL);
  _battle_cell_vector.push_back(cell);
}


////////////////////////////////////////////////////////////////////
//     Function: remove_battle_cell
//       Access: Public
//  Description: Remove a battle cell from the battle cell vector
////////////////////////////////////////////////////////////////////
int DNAStorage::remove_battle_cell(PT(DNABattleCell) cell) {
  nassertr(cell != (DNABattleCell *)NULL, -1);
  BattleCellVector::iterator i = find(_battle_cell_vector.begin(),
                                     _battle_cell_vector.end(),
                                     cell);
  if (i == _battle_cell_vector.end()) {
    // Could not find this cell
    return 0;
  };
  _battle_cell_vector.erase(i);
  return 1;
}


////////////////////////////////////////////////////////////////////
//     Function: store_suit_edge
//       Access: Public
//  Description: Store a suit edge represented by the start and end
//               indexes in the suit start point map. These indexes
//               better be stored in the suit_point_vector already
////////////////////////////////////////////////////////////////////
PT(DNASuitEdge) DNAStorage::store_suit_edge(int start_index,
                                            int end_index,
                                            string zone_id) {
  PT(DNASuitPoint) start_point = get_suit_point_with_index(start_index);
  nassertr(start_point != (DNASuitPoint *)NULL, (DNASuitEdge *)NULL);

  PT(DNASuitPoint) end_point = get_suit_point_with_index(end_index);
  nassertr(end_point != (DNASuitPoint *)NULL, (DNASuitEdge *)NULL);

  // Make a brand new edge from start to end in zone_id
  PT(DNASuitEdge) edge = new DNASuitEdge(start_point,
                                         end_point,
                                         zone_id);
  // Now store that edge for real
  return store_suit_edge(edge);
}


////////////////////////////////////////////////////////////////////
//     Function: store_suit_edge
//       Access: Public
//  Description: Store a suit edge in the suit start point map,
//               listed under the index of the start point
////////////////////////////////////////////////////////////////////
PT(DNASuitEdge) DNAStorage::store_suit_edge(PT(DNASuitEdge) edge) {
  nassertr(edge != (DNASuitEdge *)NULL, (DNASuitEdge *)NULL);
  if (edge->get_start_point() == edge->get_end_point()) {
    // Don't add degenerate edges.
    return edge;
  }

  int start_index = edge->get_start_point()->get_index();
  SuitEdgeVector &sev = _suit_start_point_map[start_index];

  // Make sure the edge isn't already there first.
  SuitEdgeVector::iterator ei;
  for (ei = sev.begin(); ei != sev.end(); ++ei) {
    if (*(*ei) == *edge) {
      return (*ei);
    }
  }
  
  sev.push_back(edge);
  return edge;
}


////////////////////////////////////////////////////////////////////
//     Function: remove_suit_edge
//       Access: Public
//  Description: Removes a suit edge from the map
////////////////////////////////////////////////////////////////////
int DNAStorage::remove_suit_edge(PT(DNASuitEdge) edge) {
  nassertr(edge != (DNASuitEdge *)NULL, -1);

  int found = 0;

  // Try to find this start_index in the map
  int start_index = edge->get_start_point()->get_index();
  SuitStartPointMap::iterator i = _suit_start_point_map.find(start_index);

  // If we did not find it, there is nothing to remove
  if (i != _suit_start_point_map.end()) {
    SuitEdgeVector::iterator ei = find((*i).second.begin(),
                                       (*i).second.end(),
                                       edge);
    if (ei != (*i).second.end()) {
      // Erase him out of our vector
      dna_cat.debug() << "removed edge from suit edge vector" << endl;
      (*i).second.erase(ei);
      found = 1;
    }
  }

  // remove the edge from any vis groups that contain it
  for(VisGroupVectorAI::const_iterator vi = _vis_group_vector.begin();
      vi != _vis_group_vector.end();
      ++vi) {
    if ((*vi)->remove_suit_edge(edge)) {
      dna_cat.debug() << "removed edge from vis group " << (*vi)->get_name() << endl;
    }
  }

  return found;
}



////////////////////////////////////////////////////////////////////
//     Function: find_texture
//       Access: Public
//  Description: A convenient interface if you only know the codes
//               by name, not by number
////////////////////////////////////////////////////////////////////
PT(Texture) DNAStorage::find_texture(const string &dna_string) const {
  // Try to find this code in the map
  TextureMap::const_iterator i = _texture_map.find(dna_string);
  if (i == _texture_map.end()) {
    dna_cat.error()
      << "texture: " << dna_string << " not found in map" << endl;
    return (Texture *)NULL;
  }
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: find_node
//       Access: Public
//  Description: A convenient interface if you only know the codes
//               by name, not by number
////////////////////////////////////////////////////////////////////
NodePath DNAStorage::find_node(const string &dna_string) const {
  // Try to find this code in the map
  NodeMap::const_iterator i = _node_map.find(dna_string);
  if (i == _node_map.end()) {

    // Then try to find this code in the hood node map
    i = _hood_node_map.find(dna_string);
    if (i == _hood_node_map.end()) {

      // Then try to find this code in the place node map
      i = _place_node_map.find(dna_string);
      if (i == _place_node_map.end()) {

        dna_cat.debug()
          << "node: " << dna_string
          << " not found in pool, hood, or place map, returning empty NodePath" << endl;
        return NodePath();
      }
    }
  }
  return (*i).second;
}

////////////////////////////////////////////////////////////////////
//     Function: find_node
//       Access: Public
//  Description: A convenient interface if you only know the codes
//               by name, not by number
////////////////////////////////////////////////////////////////////
PT(TextFont) DNAStorage::find_font(const string &dna_string) const {
  // Try to find this code in the map
  FontMap::const_iterator i = _font_map.find(dna_string);
  if (i == _font_map.end()) {
    dna_cat.error()
      << "font: " << dna_string << " not found in map" << endl;
    return (TextFont *)NULL;
  }
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: store_catalog_string
//       Access: Public
//  Description: Add a string
////////////////////////////////////////////////////////////////////
void DNAStorage::store_catalog_string(const string &catalog_string, const string &dna_string) {

  // Try to find this catalog in the map
  CodeCatalog::iterator i = _code_catalog.find(catalog_string);

  // If we did not find it, put a new CodeSet at this new catalog
  if (i == _code_catalog.end()) {
    CodeSet cs;
    cs.insert(dna_string);
    _code_catalog[catalog_string] = cs;
  } else {
    // If we did find the catalog string in the catalog, see if the specified dna string is already in the code map
    CodeSet::iterator csi = ((*i).second).find(dna_string);
    if (csi == ((*i).second).end()) {
      // Not in the code vector, add it
      ((*i).second).insert(dna_string);
      return;
    }
  }
  return;
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_catalog_codes
//       Access: Public
//  Description: Return the number of entries in this catalog
//               Return -1 if the catalog is not found
////////////////////////////////////////////////////////////////////
int DNAStorage::get_num_catalog_codes(const string &catalog_string) const {

  // Try to find this catalog in the map
  CodeCatalog::const_iterator i = _code_catalog.find(catalog_string);

  // If we did not find it just return -1
  if (i == _code_catalog.end()) {
    return -1;
  } else {
    // If we did find it, return the size of is
    return (*i).second.size();
  }
}


////////////////////////////////////////////////////////////////////
//     Function: get_catalog_code
//       Access: Public
//  Description: Return the number of entries in this catalog
//               Return empty string if the catalog is not found
////////////////////////////////////////////////////////////////////
string DNAStorage::get_catalog_code(const string &catalog_string, int index) const {

  // Try to find this catalog in the map
  CodeCatalog::const_iterator i = _code_catalog.find(catalog_string);

  // If we did not find it just return an empty string
  if (i == _code_catalog.end()) {
    return "";
  } else {
    // If we did find it, return the string
    // Loop over the items in this category to get to the desired item
    int count = 0;
    for(CodeSet::const_iterator csi = ((*i).second).begin();
        csi != ((*i).second).end();
        ++csi) {
      if (count == index) {
        return (*csi);
      }
      count++;
    }
    return "";
  }
}


////////////////////////////////////////////////////////////////////
//     Function: print_catalog
//       Access: Public
//  Description: print the catalog
////////////////////////////////////////////////////////////////////
void DNAStorage::print_catalog() const {
  cout << "Category" << endl;

  // Loop over the categories
  for(CodeCatalog::const_iterator i = _code_catalog.begin();
      i != _code_catalog.end();
      ++i) {

    cout << "Category: " << (*i).first << endl;

    // Loop over the items in this category
    for(CodeSet::const_iterator csi = ((*i).second).begin();
        csi != ((*i).second).end();
        ++csi) {
      cout << "\t" << (*csi) << endl;
    }
  }
}


////////////////////////////////////////////////////////////////////
//     Function: store_DNAGroup
//       Access: Public
//  Description: store a DNAGroup at the node path pointer
////////////////////////////////////////////////////////////////////
void DNAStorage::store_DNAGroup(PT(PandaNode) rr, PT(DNAGroup) group) {
  nassertv(rr != (PandaNode *)NULL);
  nassertv(group != (DNAGroup *)NULL);

  // Return the group
  _n2group_map[rr] = group;
}


////////////////////////////////////////////////////////////////////
//     Function: find_DNAGroup
//       Access: Public
//  Description: find a DNAGroup at the node path pointer
////////////////////////////////////////////////////////////////////
PT(DNAGroup) DNAStorage::find_DNAGroup(PT(PandaNode) rr) const {
  nassertr(rr != (PandaNode *)NULL, (DNAGroup *)NULL);
  // Try to find this group in the map
  Node2GroupMap::const_iterator i = _n2group_map.find(rr);
  if (i == _n2group_map.end()) {
    dna_cat.debug()
      << "PandaNode not found in Node2GroupMap" << endl;
    return (DNAGroup *)NULL;
  }
  nassertr((*i).second != (DNAGroup *)NULL, (DNAGroup *)NULL);
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: find_PandaNode
//       Access: Public
//  Description: find a PandaNode at the DNAGroup
////////////////////////////////////////////////////////////////////
PT(PandaNode) DNAStorage::find_PandaNode(PT(DNAGroup) group) const {
  nassertr(group != (DNAGroup *)NULL, (PandaNode *)NULL);

  // Since the node relations are actually the keys in this map, we
  // loop over all the entries, looking to see if the value (i.second)
  // matches the group passed in. If it does we return the key (i.first)
  // Note that it is possible for the map to contain multiple group values
  // that are the same, but this application should not do that. We simply
  // return the first one that matches
  for(Node2GroupMap::const_iterator i = _n2group_map.begin();
      i != _n2group_map.end();
      ++i) {
    if (group == (*i).second) {
      return (*i).first;
    }
  }

  // Ok, now look in the vis group map and see if it is in there
  for(Node2VisGroupMap::const_iterator vi = _n2visgroup_map.begin();
      vi != _n2visgroup_map.end();
      ++vi) {
    if (group == (DNAGroup *)(*vi).second) {
      return (*vi).first;
    }
  }

  // If you got here, you did not find it
  dna_cat.error()
    << "DNAStorage::find_PandaNode: DNAGroup <"
    << group->get_name() << " type: " << group->get_type()
    << "> not found in Node2GroupMap or Node2VisGroupMap" << endl;
  return (PandaNode *)NULL;
}


////////////////////////////////////////////////////////////////////
//     Function: remove_DNAGroup
//       Access: Public
//  Description: remove the DNAGroup pointed to by rr from the map
//               It also removes all children of the dnaGroup.
//               Returns the total number of DNAGroups removed.
////////////////////////////////////////////////////////////////////
int DNAStorage::remove_DNAGroup(PT(PandaNode) rr) {
  nassertr((rr != (PandaNode *)NULL), 0);

  // Recursively remove all children of this DNAGroup
  PT(DNAGroup) group = find_DNAGroup(rr);
  if (group == (DNAGroup *)NULL) {
    dna_cat.warning()
      << "Render relation did not point to any DNAGroups in the storage" << endl;
    return 0;
  } else {
    return remove_DNAGroup(group);
  }
}


////////////////////////////////////////////////////////////////////
//     Function: remove_DNAGroup
//       Access: Public
//  Description: remove the DNAGroup from the map
//               It also removes all children of the dnaGroup.
//               Returns the total number of DNAGroups removed.
////////////////////////////////////////////////////////////////////
int DNAStorage::remove_DNAGroup(PT(DNAGroup) group) {
  int num_removed = 0;

  PT(PandaNode) rr = find_PandaNode(group);
  if (rr != (PandaNode *)NULL) {
    num_removed += _n2group_map.erase(rr);
  }

  // Recursively remove all children of this DNAGroup
  int num_children = group->get_num_children();
  for (int i=0; i < num_children; i++) {
    PT(DNAGroup) child = group->at(i);
    num_removed += remove_DNAGroup(child);
  }

  return num_removed;
}


////////////////////////////////////////////////////////////////////
//     Function: find_DNAVisGroup
//       Access: Public
//  Description: find a DNAVisGroup at the node path pointer
////////////////////////////////////////////////////////////////////
PT(DNAVisGroup) DNAStorage::find_DNAVisGroup(PT(PandaNode) rr) const {
  nassertr(rr != (PandaNode *)NULL, (DNAVisGroup *)NULL);
  // Try to find this code in the map
  Node2VisGroupMap::const_iterator i = _n2visgroup_map.find(rr);
  if (i == _n2visgroup_map.end()) {
    dna_cat.error()
      << "DNAStorage::find_DNAVisGroup: NodePath not found in Node2VisGroupMap" << endl;
    return (DNAVisGroup *)NULL;
  }

  nassertr((*i).second != (DNAVisGroup *)NULL, (DNAVisGroup *)NULL);
  return (*i).second;
}


////////////////////////////////////////////////////////////////////
//     Function: get_DNAVisGroup
//       Access: Public
//  Description: Return the ith vis group in our storage
////////////////////////////////////////////////////////////////////
PT(DNAVisGroup) DNAStorage::get_DNAVisGroup(uint i) const {
  nassertr(i < _n2visgroup_map.size(), (DNAVisGroup *)NULL);

  uint current = 0;

  // Loop over the vis groups
  for(Node2VisGroupMap::const_iterator it = _n2visgroup_map.begin();
      it != _n2visgroup_map.end();
      ++it) {
    if (i == current) {
      nassertr((*it).first != (PandaNode *)NULL, (DNAVisGroup *)NULL);
      return (*it).second;
    }
    current++;
  }

  dna_cat.error()
    << "DNAStorage::get_DNAVisGroup: vis group not found, returning NULL"
    << endl;
  return (DNAVisGroup *)NULL;
}


////////////////////////////////////////////////////////////////////
//     Function: get_num_visibles_in_DNAVisGroup
//       Access: Public
//  Description: Ask how many visibles there are in this visgroup
////////////////////////////////////////////////////////////////////
int DNAStorage::get_num_visibles_in_DNAVisGroup(uint i) const {
  PT(DNAVisGroup) group;
  group = get_DNAVisGroup(i);
  if (group != (DNAVisGroup *)NULL) {
    return group->get_num_visibles();
  }
  else {
    dna_cat.error()
      << "DNAStorage::get_num_visibles_in_DNAVisGroup: vis group not found"
      << " returning -1" << endl;
    return -1;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: get_DNAVisGroup_name
//       Access: Public
//  Description: Ask for the name of the nth DNAVisGroup in the map
////////////////////////////////////////////////////////////////////
string DNAStorage::get_DNAVisGroup_name(uint i) const {
  PT(DNAVisGroup) group;
  group = get_DNAVisGroup(i);
  if (group != (DNAVisGroup *)NULL) {
    return group->get_name();
  }
  else {
    dna_cat.error()
      << "DNAStorage::get_DNAVisGroup_name: vis group not found,"
      << " returning empty string" << endl;
    return "";
  }
}


////////////////////////////////////////////////////////////////////
//     Function: get_visible_name
//       Access: Public
//  Description: Ask for the name of the nth visible in the nth DNAVisGroup
////////////////////////////////////////////////////////////////////
string DNAStorage::get_visible_name(uint visgroup_index, uint visible_index) const {
  PT(DNAVisGroup) group;
  group = get_DNAVisGroup(visgroup_index);
  if (group != (DNAVisGroup *)NULL) {
    return group->get_visible_name(visible_index);
  }
  else {
    dna_cat.error()
      << "DNAStorage::get_num_visibles_in_DNAVisGroup: vis group not found,"
      << " returning empty string" << endl;
    return "";
  }
}

////////////////////////////////////////////////////////////////////
//     Function: store_DNAVisGroupAI
//       Access: Public
//  Description: store a DNAVisGroup in a vector so the AI can
//               retrieve it without traversing the DNA
////////////////////////////////////////////////////////////////////
void DNAStorage::store_DNAVisGroupAI(PT(DNAVisGroup) vis_group) {
  nassertv(vis_group != (DNAVisGroup *)NULL);
  _vis_group_vector.push_back(vis_group);
}




////////////////////////////////////////////////////////////////////
//     Function: get_PandaNode_at
//       Access: Public
//  Description: return the ith NodePath
////////////////////////////////////////////////////////////////////
PT(PandaNode) DNAStorage::get_PandaNode_at(uint i) const {
  nassertr(i < _n2group_map.size(), (PandaNode *)NULL);

  uint current = 0;

  // Loop over the PandaNodes
  for(Node2GroupMap::const_iterator it = _n2group_map.begin();
      it != _n2group_map.end();
      ++it) {
    if (i == current) {
      nassertr((*it).first != (PandaNode *)NULL, (PandaNode *)NULL);
      return (*it).first;
    }
    current++;
  }

  dna_cat.error()
    << "DNAStorage::get_PandaNode_at PandaNode not found, returning NULL"
    << endl;
  return (PandaNode *)NULL;
}


void DNAStorage::print_PandaNodes() const {
  // Loop over the PandaNodes
  for(Node2GroupMap::const_iterator it = _n2group_map.begin();
      it != _n2group_map.end();
      ++it) {
    cout << "PandaNode " << (void *)(*it).first
         << " DNAGroup " << (void *)(*it).second
         << " " << ((*it).second)->get_name() << endl;
  }
  // Don't forget the vis groups
  for(Node2VisGroupMap::const_iterator vit = _n2visgroup_map.begin();
      vit != _n2visgroup_map.end();
      ++vit) {
    cout << "PandaNode " << (void *)(*vit).first
         << " DNAVisGroup " << (void *)(*vit).second
         << " " << ((*vit).second)->get_name() <<  endl;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: get_suit_edge
//       Access: Public
//  Description: Ask for the edge that connects these two points
////////////////////////////////////////////////////////////////////
PT(DNASuitEdge) DNAStorage::get_suit_edge(int start_index, int end_index) const {
  // Look in the start point map for this start index
  SuitStartPointMap::const_iterator i = _suit_start_point_map.find(start_index);
  if (i == _suit_start_point_map.end()) {
    dna_cat.error()
      << "DNASuitStartPoint index: " << start_index
      << " not found in map" << endl;
    return (DNASuitEdge *)NULL;
  } else {
    // Ok, found the start index, lets see if it connects directly to
    // the end index. Find the end index in the edge vector associated
    // with this start index
    for(SuitEdgeVector::const_iterator evi = ((*i).second).begin();
        evi != ((*i).second).end();
        ++evi) {
      if (end_index == (*evi)->get_end_point()->get_index()) {
        // Found it, return the edge
        return (*evi);
      }
    }

    // Did not find the end point connected to this start point
    dna_cat.error()
      << "DNASuitStartPoint start index: " << start_index
      << " not connected to end index: " << end_index << endl;
    return (DNASuitEdge *)NULL;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: get_suit_edge_zone
//       Access: Public
//  Description: Ask for the zone that this edge is in
//               Returns -1 if there is no edge between these points
////////////////////////////////////////////////////////////////////
string DNAStorage::get_suit_edge_zone(int start_index, int end_index) const {
  // First find the edge that connects these two points
  PT(DNASuitEdge) edge = get_suit_edge(start_index, end_index);
  // Make sure the edge is valid, if not, return empty string
  nassertr(edge != (DNASuitEdge *)NULL, "");
  // Return the zone this edge thinks it is in
  return edge->get_zone_id();
}


////////////////////////////////////////////////////////////////////
//     Function: get_suit_travel_time
//       Access: Public
//  Description: Ask how long in seconds it will take a suit to walk
//               from the start point to the end point if he is
//               walking this constant rate in units/second
//               If there is not connection, return -1.0
////////////////////////////////////////////////////////////////////
float DNAStorage::get_suit_edge_travel_time(int start_index,
                                            int end_index,
                                            float rate) const {
  // Make sure the rate is a positive number
  nassertr(rate > 0.0, -1.0);

  // Find the edge that connects these two points
  PT(DNASuitEdge) edge = get_suit_edge(start_index, end_index);
  // Make sure the edge is valid, if not, return -1.0
  nassertr(edge != (DNASuitEdge *)NULL, -1.0);

  // Find the distance between the two points
  float distance = length(edge->get_end_point()->get_pos() - edge->get_start_point()->get_pos());

  // Compute the time
  float time = (distance / rate);
  return time;
}




////////////////////////////////////////////////////////////////////
//     Function: get_suit_path
//       Access: Public
//  Description: Find a valid path from start to end for a suit to
//               walk on given all the points and edges that are
//               loaded in the current branch
//               To make this easy, the SuitStartPointMap is organized
//               as a map of points to edge lists that that point starts
//               {
//                 start_point1 { edge1 edge2 edge3 }
//                 start_point2 { edge4 edge5 }
//                 start_point3 { edge6 edge7 edge8 }
//               }
////////////////////////////////////////////////////////////////////
PT(DNASuitPath) DNAStorage::
get_suit_path(const DNASuitPoint *start_point, const DNASuitPoint *end_point,
              int min_length, int max_length) const {
  if (start_point->get_graph_id() != end_point->get_graph_id()) {
    if (dna_cat.is_debug()) {
      dna_cat.debug()
        << "Not looking for path between disconnected points "
        << (*start_point) << " and " << (*end_point) << ".\n";
    }
    return NULL;
  }

  if (dna_cat.is_debug()) {
    dna_cat.debug()
      << "get_suit_path: About to look for path from "
      << (*start_point)
      << " to " << (*end_point) 
      << " min_length = " << min_length << ", max_length = " 
      << max_length << "\n";
  }

  PT(DNASuitPath) path = 
    get_suit_path_breadth_first(start_point, end_point, min_length, max_length);
  if (path != (DNASuitPath *)NULL) {
    if (dna_cat.is_debug()) {
      dna_cat.debug()
        << "get_suit_path: Path from " << (*start_point)
        << " to " << (*end_point) << " is "
        << (*path) << endl;
      dna_cat.debug()
        << "get_suit_path: Path contains " << path->get_num_points()
        << " points " << endl;
    }

  } else {
    dna_cat.warning()
      << "get_suit_path: could not find path" << endl
      << "  from: " << (*start_point) << endl
      << "    to: " << (*end_point)   << endl;
  }

  return path;
}

////////////////////////////////////////////////////////////////////
//     Function: get_adjacent_points
//       Access: Public
//  Description: Returns all of the points adjacent to the indicated
//               point.  The result is returned as a DNASuitPath, even
//               though it's not actually a path; it's just a set of
//               points.
////////////////////////////////////////////////////////////////////
PT(DNASuitPath) DNAStorage::
get_adjacent_points(PT(DNASuitPoint) start_point) const {
  PT(DNASuitPath) path = new DNASuitPath();

  int current_point_index = start_point->get_index();

  SuitStartPointMap::const_iterator si =
    _suit_start_point_map.find(current_point_index);
  if (si == _suit_start_point_map.end()) {
    return path;
  }

  // Get each edge connecting to the current point.
  SuitEdgeVector edge_list = (*si).second;
  for(SuitEdgeVector::const_iterator evi = edge_list.begin();
      evi != edge_list.end(); ++evi) {
    PT(DNASuitEdge) edge = (*evi);
    PT(DNASuitPoint) end_point = edge->get_end_point();

    path->add_point(end_point->get_index());
  }

  return path;
}

////////////////////////////////////////////////////////////////////
//     Function: discover_continuity
//       Access: Public
//  Description: This should be called once the DNA file has been read
//               and the set of suit points is complete.  It walks
//               through the points and discovers which points are
//               connected to each other and which are not.  Each
//               group of suit points that can be reached from each
//               other are assigned a unique graph_id number, which
//               has no other meaning.  The return value is the number
//               of disconnected graphs we have.
////////////////////////////////////////////////////////////////////
int DNAStorage::
discover_continuity() {
  int graph_id = 0;
  SuitPointVector::iterator vi;
  for (vi = _suit_point_vector.begin(); vi != _suit_point_vector.end(); ++vi) {
    DNASuitPoint *point = (*vi);
    if (point->get_graph_id() == 0) {
      graph_id++;

      // Recursively discover all the points that are connected to
      // point, and identify them all with graph_id.
      r_discover_connections(point, graph_id);
    }
  }
  
  return graph_id;
}

////////////////////////////////////////////////////////////////////
//     Function: r_discover_connections
//       Access: Private
//  Description: Called by discover_continuity() recursively find all
//               the points that are connected to the indicated point.
////////////////////////////////////////////////////////////////////
void DNAStorage::
r_discover_connections(DNASuitPoint *point, int graph_id) {
  if (point->get_graph_id() != 0) {
    if (point->get_graph_id() != graph_id) {
      dna_cat.warning()
        << *point << " is connected to graph only one-way.\n";
    }
    return;
  }
  point->set_graph_id(graph_id);
  int point_index = point->get_index();

  SuitStartPointMap::const_iterator si =
    _suit_start_point_map.find(point_index);
  
  if (si == _suit_start_point_map.end()) {
    dna_cat.warning()
      << "Could not find point " << point_index << " in map.\n";
    
  } else {
    const SuitEdgeVector &edge_list = (*si).second;
    for(SuitEdgeVector::const_iterator evi = edge_list.begin();
        evi != edge_list.end(); 
        ++evi) {
      DNASuitEdge *edge = (*evi);
      r_discover_connections(edge->get_end_point(), graph_id);
    }
  }
}

PT(DNASuitPath) DNAStorage::
get_suit_path_breadth_first(const DNASuitPoint *start_point,
                            const DNASuitPoint *end_point,
                            int min_length, int max_length) const {
  // Perform a breadth-first traversal of the connected suit points to
  // try to find the shortest path from start_point to end_point that
  // is at least min_length points long (and not longer than
  // max_length).

  // To performing a breadth-first traversal, you must first generate
  // all the paths of length 1, then all the paths of length 2, then
  // all the paths of length 3, etc.  You must keep around all the
  // paths of each generation until you have generated all the paths
  // of the next generation (or found a solution).

  // We use the WorkingSuitPath nested class to generate these paths
  // with a minimal overhead.  Each instance of a WorkingSuitPath
  // object represents one step in a path.  A linked list of
  // WorkingSuitPath objects represents one complete path under
  // consideration.  This "path" is defined by the _next_in_path
  // member of WorkingSuitPath; traversing through these pointers in
  // reverse order gives the original path.

  // Each generation of the search requires storing several of these
  // paths, in no particular order.  We store this set of paths as a
  // linked chain of pointers to the heads of the individual paths;
  // these are traversed by walking through the _next_in_chain
  // members.  That is, each WorkingSuitPath object pointed to by the
  // _next_in_chain member represents the head of a different path,
  // which may then be traversed along the _next_in_path member.

  // Finally, for efficient memory management, we don't actually free
  // these WorkingSuitPath objects; instead, they get added to a
  // deleted chain, which is a linked list defined by the
  // _next_deleted member.

  // Start with one path on the queue that has only the start point.
  PT(WorkingSuitPath) chain = new WorkingSuitPath(start_point->get_index());

  int length = 1;

  // First, generate all the paths from start_point that contain at
  // least (min_length - 1) steps.  In this pass, we may visit points
  // multiple times and thus generate looping paths.
  while (length < min_length - 1) {
    ++length;
    if (dna_cat.is_debug()) {
      // Count up the number of paths on the chain for debug output.
      int num_paths = 0;
      for (WorkingSuitPath *p = chain; 
           p != (WorkingSuitPath *)NULL; 
           p = p->_next_in_chain) {
        num_paths++;
      }
      dna_cat.debug()
        << "Generating from " << num_paths << " paths of length " << length
        << "\n";
    }
    generate_next_suit_path_chain(chain);
  }

  // Now, we're ready to start looking for an actual solution.
  // Generate all the paths that contain min_length steps and more.
  // From now on, we stop considering loops, since looping won't take
  // us closer to a solution, and it just increases our search time.
  pset<int> visited_points;
  while (length < max_length && chain != (WorkingSuitPath *)NULL) {
    ++length;
    if (dna_cat.is_debug()) {
      // Count up the number of paths on the chain for debug output.
      int num_paths = 0;
      for (WorkingSuitPath *p = chain; 
           p != (WorkingSuitPath *)NULL; 
           p = p->_next_in_chain) {
        num_paths++;
      }
      dna_cat.debug()
        << "Considering " << num_paths << " paths of length " << length
        << "\n";
    }
    if (consider_next_suit_path_chain(chain, end_point, visited_points)) {
      // We found a solution!
      PT(DNASuitPath) path = new DNASuitPath(length);
      chain->get_path(path);
      return path;
    }
  }

  // No solution could be found within the prescribed length.
  return NULL;
}

void DNAStorage::
generate_next_suit_path_chain(PT(DNAStorage::WorkingSuitPath) &chain) const {
  // Make a complete pass through the chain of working paths given in
  // chain.  At this point, we are not looking for a solution; we are
  // just looking to see where we can go from the current point(s).
  PT(WorkingSuitPath) next_chain = NULL;

  PT(WorkingSuitPath) current_path = chain;
  while (current_path != (WorkingSuitPath *)NULL) {
    PT(WorkingSuitPath) next_path = current_path->_next_in_chain;
    current_path->_next_in_chain = (WorkingSuitPath *)NULL;
    int current_point_index = current_path->get_point_index();

    if (dna_cat.is_spam()) {
      dna_cat.spam()
        << "Generating next path: [ ";
      current_path->output(dna_cat.spam(false));
      dna_cat.spam(false)
        << " ]\n";
    }

    // Some edges are incorrectly given backwards in the dna files
    // (along with their correct forwards listing).  To detect and
    // avoid these, we must ensure they do not take us back to the
    // previous point in the path.
    int prev_point_index = -1;
    if (current_path->_next_in_path != (WorkingSuitPath *)NULL) {
      prev_point_index = current_path->_next_in_path->get_point_index();
    }

    // Try to find this current point index in the map
    SuitStartPointMap::const_iterator si =
      _suit_start_point_map.find(current_point_index);

    if (si == _suit_start_point_map.end()) {
      dna_cat.warning()
        << "Could not find point " << current_point_index << " in map.\n";

    } else {
      // Look over each edge connecting to current point index
      const SuitEdgeVector &edge_list = (*si).second;
      for(SuitEdgeVector::const_iterator evi = edge_list.begin();
          evi != edge_list.end(); 
          ++evi) {
        DNASuitEdge *edge = (*evi);
        int next_point_index = edge->get_end_point()->get_index();
        
        if (dna_cat.is_spam()) {
          dna_cat.spam()
            << "get_suit_path_breadth_first: Examining edge: "
            << (*edge) << endl;
        }

        // We don't step off the street points unless it is onto our
        // final, solution point.
        if (!edge->get_end_point()->is_terminal()) {
          if (next_point_index == current_point_index || 
              next_point_index == prev_point_index) {
            dna_cat.warning()
              << "Invalid edge detected in dna: " << (*edge) << "\n";
          } else {
            // Extend the path by the current point and save it on the
            // new chain.
            PT(WorkingSuitPath) new_path = 
              new WorkingSuitPath(current_path, next_point_index);
            new_path->_next_in_chain = next_chain;
            next_chain = new_path;
          }
        } else if (dna_cat.is_spam()) {
          dna_cat.spam()
            << "Rejected edge, not street point.\n";
        }
      }
    }

    current_path = next_path;
  }

  chain = next_chain;
}

bool DNAStorage::
consider_next_suit_path_chain(PT(DNAStorage::WorkingSuitPath) &chain,
                              const DNASuitPoint *end_point,
                              pset<int> visited_points) const {
  // As above, but this time in addition to generating the next chain,
  // we also look for a solution along the way.  If one is found,
  // returns true and set chain to the single found path.  Otherwise,
  // returns false and set chain to the next chain of paths generated.
  PT(WorkingSuitPath) next_chain = NULL;

  PT(WorkingSuitPath) current_path = chain;
  while (current_path != (WorkingSuitPath *)NULL) {
    PT(WorkingSuitPath) next_path = current_path->_next_in_chain;
    current_path->_next_in_chain = (WorkingSuitPath *)NULL;
    int current_point_index = current_path->get_point_index();

    if (dna_cat.is_spam()) {
      dna_cat.spam()
        << "Considering path: [ ";
      current_path->output(dna_cat.spam(false));
      dna_cat.spam(false)
        << " ]\n";
    }

    // Some edges are incorrectly given backwards in the dna files
    // (along with their correct forwards listing).  To detect and
    // avoid these, we must ensure they do not take us back to the
    // previous point in the path.
    int prev_point_index = -1;
    if (current_path->_next_in_path != (WorkingSuitPath *)NULL) {
      prev_point_index = current_path->_next_in_path->get_point_index();
    }

    // Try to find this current point index in the map
    SuitStartPointMap::const_iterator si =
      _suit_start_point_map.find(current_point_index);

    if (si == _suit_start_point_map.end()) {
      dna_cat.warning()
        << "Could not find point " << current_point_index << " in map.\n";

    } else {
      // Look over each edge connecting to current point index
      const SuitEdgeVector &edge_list = (*si).second;
      for(SuitEdgeVector::const_iterator evi = edge_list.begin();
          evi != edge_list.end(); 
          ++evi) {
        DNASuitEdge *edge = (*evi);
        int next_point_index = edge->get_end_point()->get_index();
        
        if (dna_cat.is_spam()) {
          dna_cat.spam()
            << "get_suit_path_breadth_first: Examining edge: "
            << (*edge) << endl;
        }
        
        // See if this is the one we are looking for
        if (next_point_index == end_point->get_index()) {
          // Add this final point
          PT(WorkingSuitPath) new_path = 
            new WorkingSuitPath(current_path, next_point_index);
            
          if (dna_cat.is_debug()) {
            dna_cat.debug()
              << "Found solution:\n";
            new_path->write(dna_cat.debug(false));
          }
          chain = new_path;
          return true;
        }

        // We don't step off the street points unless it is onto our
        // final, solution point.
        if (!edge->get_end_point()->is_terminal()) {
          if (next_point_index == current_point_index || 
              next_point_index == prev_point_index) {
            dna_cat.warning()
              << "Invalid edge detected in dna: " << (*edge) << "\n";
          } else {
            // Record that we have now visited this new point.
            if (visited_points.insert(next_point_index).second) {
              // Extend the path by the current point and save it on the
              // new chain.
              PT(WorkingSuitPath) new_path = 
                new WorkingSuitPath(current_path, next_point_index);
              new_path->_next_in_chain = next_chain;
              next_chain = new_path;
            } else if (dna_cat.is_spam()) {
              dna_cat.spam()
                << "Rejected edge, already visited " << next_point_index
                << ".\n";
            }
          }
        } else if (dna_cat.is_spam()) {
          dna_cat.spam()
            << "Rejected edge, not street point.\n";
        }
      }
    }

    current_path = next_path;
  }

  // All paths on the chain evaluated, and no solutions found.  Carry on.
  chain = next_chain;
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: get_block
//       Access: Public
//  Description: Get the block number as a string from the building
//               name.
////////////////////////////////////////////////////////////////////
string DNAStorage::get_block(const string& name) const {
  // The block number is in the parent name, between "tb" and ":"
  // (e.g. "tb22:blah_blah").
  size_t pos=name.find(':');
  string block=name.substr(2, pos-2);
  return block;
}


////////////////////////////////////////////////////////////////////
//     Function: fixup
//       Access: Public
//  Description: Do any processing here before we write the file
//               to cleanup or fixup the dna storage
////////////////////////////////////////////////////////////////////
void DNAStorage::fixup() {
  // First, fix any coincident suit points
  delete_unused_suit_points();
  fix_coincident_suit_points();
}


////////////////////////////////////////////////////////////////////
//     Function: write
//       Access: Public
//  Description: Write out to the dna file whatever the storage
//               feels it needs to. For instance, the suit points.
////////////////////////////////////////////////////////////////////
void DNAStorage::write(ostream &out, int indent_level) const {
  for(SuitPointVector::const_iterator i = _suit_point_vector.begin();
      i != _suit_point_vector.end();
      ++i) {
    (*i)->write(out, indent_level);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::get_path
//       Access: Public
//  Description: Converts the temporary WorkingSuitPath construct to a
//               DNASuitPath object by recursively filling the
//               indicated path up with each element, one at a time.
////////////////////////////////////////////////////////////////////
void DNAStorage::WorkingSuitPath::
get_path(DNASuitPath *path) const {
  if (_next_in_path != (WorkingSuitPath *)NULL) {
    _next_in_path->get_path(path);
  }
  path->add_point(get_point_index());
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::output
//       Access: Public
//  Description: 
////////////////////////////////////////////////////////////////////
void DNAStorage::WorkingSuitPath::
output(ostream &out) const {
  if (_next_in_path != (WorkingSuitPath *)NULL) {
    _next_in_path->output(out);
    out << " " << get_point_index();
  } else {
    out << get_point_index();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStorage::WorkingSuitPath::write
//       Access: Public
//  Description: 
////////////////////////////////////////////////////////////////////
void DNAStorage::WorkingSuitPath::
write(ostream &out) const {
  out << "[ ";
  output(out);
  out << " ]\n";
}

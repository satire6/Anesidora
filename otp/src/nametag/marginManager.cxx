// Filename: marginManager.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "marginManager.h"
#include "nametagGlobals.h"

#include "compose_matrix.h"
#include "lineSegs.h"
#include "transformState.h"
#include "clockObject.h"
#include "omniBoundingVolume.h"
#include "indent.h"

#include <algorithm>

TypeHandle MarginManager::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
MarginManager::
MarginManager() : PandaNode("popups") {
  set_cull_callback();

  _num_available_cells = 0;

  // A MarginManager has an infinite bounding volume, so it never gets
  // culled.
  OmniBoundingVolume volume;
  set_bounds(&volume);
  set_final(true);
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::Destructor
//       Access: Published, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
MarginManager::
~MarginManager() {
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::add_grid_cell
//       Access: Published
//  Description: This variant on add_cell() adds a new cell based on
//               its coordinates within an imaginary grid, where (0,
//               0) is the bottom left corner and
//               (NametagGlobals::grid_count_horizontal - 1,
//               NametagGlobals::grid_count_vertical - 1) is the upper
//               right corner.  The dimensions of the entire screen
//               are given.
//
//               The return value is the index number associated with
//               this cell, which may be passed to get_cell_available()
//               or set_cell_available().
////////////////////////////////////////////////////////////////////
int MarginManager::
add_grid_cell(float x, float y,
              float screen_left, float screen_right,
              float screen_bottom, float screen_top) {
  float screen_width = (screen_right - screen_left);
  float screen_height = (screen_top - screen_bottom);

  float cell_width = screen_width / NametagGlobals::grid_count_horizontal;
  float cell_height = screen_height / NametagGlobals::grid_count_vertical;

  float left = screen_left + x * cell_width;
  float right = left + cell_width;
  float bottom = screen_bottom + y * cell_height;
  float top = bottom + cell_height;

  float horz_margin = NametagGlobals::grid_spacing_horizontal * 0.5f;
  float vert_margin = NametagGlobals::grid_spacing_vertical * 0.5f;

  return add_cell(left + horz_margin, right - horz_margin,
                  bottom + vert_margin, top - vert_margin);
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::add_cell
//       Access: Published
//  Description: Adds a new cell to the list of available cells for
//               popups.  The coordinates given define the rectangular
//               region that defines the cell; the cell will be set up
//               in a coordinate space that maps -1 .. 1 in the y
//               dimension and -width .. width in the x dimension to
//               the rectangle defined.
//
//               The return value is the index number associated with
//               this cell, which may be passed to get_cell_available()
//               or set_cell_available().
////////////////////////////////////////////////////////////////////
int MarginManager::
add_cell(float left, float right, float bottom, float top) {
  // We choose the appropriate scale such that -1 .. 1 maps to the top
  // and bottom of the rectangle, and the appropriate translation such
  // that (0, 0) is in the center of the rectangle.
  float vert_scale = (top - bottom) * 0.5f;
  LVecBase3f scale(vert_scale, vert_scale, vert_scale);
  LVecBase3f hpr(0.0f, 0.0f, 0.0f);
  LVecBase3f trans((left + right) * 0.5f,
                   0.0f,
                   (bottom + top) * 0.5f);

  int cell_index = _cells.size();
  _cells.push_back(Cell());
  Cell &cell = _cells.back();
  cell._is_available = true;
  compose_matrix(cell._mat, scale, hpr, trans);

  // Now we compute the width such that -width .. width represents the
  // left-to-right extents of the rectangle.
  float horz_scale = (right - left) * 0.5f;
  cell._width = horz_scale / vert_scale;

  cell._popup = (MarginPopup *)NULL;
  cell._popup_code = 0;
  cell._np = NodePath();
  cell._hide_time = 0.0f;

  _num_available_cells++;

  return cell_index;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::set_cell_available
//       Access: Published
//  Description: Sets whether the indicated cell may be used to
//               display popups.  See get_cell_available().
////////////////////////////////////////////////////////////////////
void MarginManager::
set_cell_available(int cell_index, bool available) {
  nassertv(cell_index >= 0 && cell_index < (int)_cells.size());

  if (_cells[cell_index]._is_available) {
    _num_available_cells--;
  }
  _cells[cell_index]._is_available = available;
  if (_cells[cell_index]._is_available) {
    _num_available_cells++;
  }

  if (!_cells[cell_index]._np.is_empty()) {
    // The cell is not currently vacant.  That means this popup must
    // find another cell, next pass through.
    hide(cell_index);

    // And forget about whatever used to be here; don't try to put it
    // back here later.
    Cell &cell = _cells[cell_index];
    cell._popup = (MarginPopup *)NULL;
    cell._popup_code = 0;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::get_cell_available
//       Access: Published
//  Description: Returns true if the indicated cell number is
//               currently available, false if not.  If the cell is
//               available, it may be used to display popups; otherwise,
//               it must remain empty.
////////////////////////////////////////////////////////////////////
bool MarginManager::
get_cell_available(int cell_index) const {
  nassertr(cell_index >= 0 && cell_index < (int)_cells.size(), false);

  return _cells[cell_index]._is_available;
}

#ifndef NDEBUG
////////////////////////////////////////////////////////////////////
//     Function: MarginManager::show_cells
//       Access: Published
//  Description: Draws a frame around each cell to make it visible,
//               for debugging.
////////////////////////////////////////////////////////////////////
void MarginManager::
show_cells() {
  hide_cells();

  LineSegs lines;

  Cells::const_iterator ci;
  for (ci = _cells.begin(); ci != _cells.end(); ++ci) {
    const Cell &cell = (*ci);

    if (cell._is_available) {
      lines.set_color(0.5f, 0.2f, 1.0f);
    } else {
      lines.set_color(0.5f, 0.5f, 0.5f);
    }

    lines.move_to(LPoint3f(-cell._width, 0.0f, 1.0f) * cell._mat);
    lines.draw_to(LPoint3f(-cell._width, 0.0f, -1.0f) * cell._mat);
    lines.draw_to(LPoint3f(cell._width, 0.0f, -1.0f) * cell._mat);
    lines.draw_to(LPoint3f(cell._width, 0.0f, 1.0f) * cell._mat);
    lines.draw_to(LPoint3f(-cell._width, 0.0f, 1.0f) * cell._mat);
  }

  NodePath this_np(this);
  _show_cells = this_np.attach_new_node(lines.create());
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::hide_cells
//       Access: Published
//  Description: Removes the frames drawn in a previous call to
//               show_cells().
////////////////////////////////////////////////////////////////////
void MarginManager::
hide_cells() {
  _show_cells.remove_node();
}
#endif

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::manage_popup
//       Access: Public
//  Description: Adds the indicated popup to the set of popups that are
//               managed.  The popup will be made visible whenever it
//               reports that it should be made visible.
////////////////////////////////////////////////////////////////////
void MarginManager::
manage_popup(MarginPopup *popup) {
  nassertv(!popup->is_managed());
  nassertv(!popup->is_visible());
  popup->set_managed(true);
  PopupInfo info;
  info._code = popup->get_object_code();
  _popups.insert(Popups::value_type(popup, info));
  if (info._code != 0) {
    _popups_by_code[info._code].insert(popup);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::unmanage
//       Access: Public
//  Description: Removes the indicated popup from the set of popups that
//               will be kept onscreen.  This popup will immediately
//               become invisible.
////////////////////////////////////////////////////////////////////
void MarginManager::
unmanage_popup(MarginPopup *popup) {
  Popups::iterator pi = _popups.find(popup);
  if (pi == _popups.end()) {
    // Not on the list.
    return;
  }

  PopupInfo &info = (*pi).second;

  int cell_index = info._cell_index;
  if (cell_index >= 0) {
    // It's already visible; make it invisible.
    nassertv(cell_index < (int)_cells.size());
    nassertv(_cells[cell_index]._popup == popup);
    hide(cell_index);
  }

  popup->set_managed(false);

  if (info._code != 0) {
    _popups_by_code[info._code].erase(popup);
  }
  _popups.erase(pi);
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::update
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void MarginManager::
update() {
  // First, query all of our managed popups to see if they should
  // change their managed/unmanaged state.
  Popups::iterator pi;
  pi = _popups.begin();
  while (pi != _popups.end()) {
    MarginPopup *popup = (*pi).first;
    PopupInfo &info = (*pi).second;
    Popups::iterator next_pi = pi;
    ++next_pi;

    if (!popup->consider_manage()) {
      // This popup wants to unmanage itself.
      int cell_index = info._cell_index;
      if (cell_index >= 0) {
        // It's already visible; make it invisible.
        nassertv(cell_index < (int)_cells.size());
        nassertv(_cells[cell_index]._popup == popup);
        hide(cell_index);
      }

      popup->set_managed(false);
      if (info._code != 0) {
        _popups_by_code[info._code].erase(popup);
      }
      _popups.erase(pi);

    } else {
      // This popup wants to continue being managed.
      info._wants_visible = popup->consider_visible();
      if (info._wants_visible && info._code != 0) {
        info._score = popup->get_score();
      }
    }

    pi = next_pi;
  }

  // Now go back and consider which popups should be made visible.
  int num_visible = 0;
  bool any_new_visible = false;

  for (pi = _popups.begin(); pi != _popups.end(); ++pi) {
    MarginPopup *popup = (*pi).first;
    PopupInfo &info = (*pi).second;

    if (info._wants_visible && info._code != 0) {
      // This popup thinks it wants to be visible, but it has a
      // uniquifying code.  Of all the popups that share this code,
      // only the one with the highest score actually wants to be
      // visible.
      PopupSet &popup_set = _popups_by_code[info._code];

      if (popup_set.size() > 1) {
        // Find the one with the highest score.
        float best_score = info._score;
        MarginPopup *best_popup = popup;
        PopupSet::iterator psi;
        for (psi = popup_set.begin(); psi != popup_set.end(); ++psi) {
          MarginPopup *try_popup = (*psi);
          PopupInfo &try_info = _popups[try_popup];
          if (try_info._wants_visible && try_info._score > best_score) {
            best_score = try_info._score;
            best_popup = try_popup;
          }
        }

        // Now set all the other ones invisible.
        for (psi = popup_set.begin(); psi != popup_set.end(); ++psi) {
          MarginPopup *try_popup = (*psi);
          PopupInfo &try_info = _popups[try_popup];
          if (try_popup != best_popup) {
            try_info._wants_visible = false;
          }
        }
      }
    }

    // Okay, does this popup still want to be visible?
    if (info._wants_visible) {
      num_visible++;
    }
    if (!info._wants_visible && popup->is_visible()) {
      // If the popup wants to hide itself, we can oblige it right
      // away.
      hide(info._cell_index);
      
    } else if (info._wants_visible && !popup->is_visible()) {
      // This popup wants to reveal itself; we'll have to defer that
      // request for a bit until we've looked at all the popups.
      any_new_visible = true;
    }
  }

  if (any_new_visible) {
    // Now, can we satisfy all the popups that want visibility?
    if (num_visible <= _num_available_cells) {
      // Hooray, no conflict!
      show_visible_no_conflict();
    } else {
      // Too bad, we can only show some of them.
      show_visible_resolve_conflict();
    }
  }

  // Now do all the callbacks.
  for (pi = _popups.begin(); pi != _popups.end(); ++pi) {
    MarginPopup *popup = (*pi).first;

    popup->frame_callback();
  }

#ifndef NDEBUG
  // Update the visualization of the MouseWatcherRegions, if this
  // happens to be enabled.
  MouseWatcher *mouse_watcher = NametagGlobals::get_mouse_watcher();
  if (mouse_watcher != (MouseWatcher *)NULL) {
    mouse_watcher->update_regions();
  }
#endif
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::cull_callback
//       Access: Public, Virtual
//  Description: This function will be called during the cull
//               traversal to perform any additional operations that
//               should be performed at cull time.  This may include
//               additional manipulation of render state or additional
//               visible/invisible decisions, or any other arbitrary
//               operation.
//
//               Note that this function will *not* be called unless
//               set_cull_callback() is called in the constructor of
//               the derived class.  It is necessary to call
//               set_cull_callback() to indicated that we require
//               cull_callback() to be called.
//
//               By the time this function is called, the node has
//               already passed the bounding-volume test for the
//               viewing frustum, and the node's transform and state
//               have already been applied to the indicated
//               CullTraverserData object.
//
//               The return value is true if this node should be
//               visible, or false if it should be culled.
////////////////////////////////////////////////////////////////////
bool MarginManager::
cull_callback(CullTraverser *, CullTraverserData &) {
  update();
  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::is_renderable
//       Access: Public, Virtual
//  Description: Returns true if there is some value to visiting this
//               particular node during the cull traversal for any
//               camera, false otherwise.  This will be used to
//               optimize the result of get_net_draw_show_mask(), so
//               that any subtrees that contain only nodes for which
//               is_renderable() is false need not be visited.
////////////////////////////////////////////////////////////////////
bool MarginManager::
is_renderable() const {
  // We flag the MarginManager as renderable, even though it
  // technically doesn't have anything to render, but we do need the
  // traverser to visit it every frame.
  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::write
//       Access: Published, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
void MarginManager::
write(ostream &out, int indent_level) const {
  PandaNode::write(out, indent_level);

  Popups::const_iterator pi;
  for (pi = _popups.begin(); pi != _popups.end(); ++pi) {
    MarginPopup *popup = (*pi).first;
    const PopupInfo &info = (*pi).second;

    indent(out, indent_level + 2)
      << *popup;
    if (popup->is_visible()) {
      out << " cell " << info._cell_index;
    } else {
      out << " wants_visible=" << info._wants_visible;
    }
    if (info._wants_visible) {
      out << " score=" << info._score;
    }
    out << "\n";
  }
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::show_visible_no_conflict
//       Access: Private
//  Description: Shows all the popups that want to be made visible.
//               We know that we can show all the popups without
//               running out of empty cells.
////////////////////////////////////////////////////////////////////
void MarginManager::
show_visible_no_conflict() {
  // First, find all the empty cells.
  vector_int empty_cells;
  Cells::const_iterator ci;
  for (ci = _cells.begin(); ci != _cells.end(); ++ci) {
    if ((*ci)._is_available && (*ci)._np.is_empty()) {
      // Here's an empty cell.
      int cell_index = (ci - _cells.begin());
      empty_cells.push_back(cell_index);
    }
  }

  // Randomize the list, so we'll pull the cells out in random order.
  random_shuffle(empty_cells.begin(), empty_cells.end());

  // Now find a home for each popup that needs one.
  Popups::iterator pi;
  for (pi = _popups.begin(); pi != _popups.end(); ++pi) {
    MarginPopup *popup = (*pi).first;
    PopupInfo &info = (*pi).second;

    if (info._wants_visible && !popup->is_visible()) {
      int cell_index = choose_cell(popup, empty_cells);
      nassertv(cell_index >= 0);

      show(popup, cell_index);
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::show_visible_resolve_conflict
//       Access: Private
//  Description: Shows all the popups that want to be made visible.
//               We know that we we have more popups than cells
//               available, so we have to resolve the conflict and
//               show only those popups with the highest scores.
////////////////////////////////////////////////////////////////////
void MarginManager::
show_visible_resolve_conflict() {
  // First, get a list of the popups that want to be visible in
  // descending order by score.
  typedef pvector<Popups::iterator> PopupsByScore;
  PopupsByScore by_score;

  Popups::iterator pi;
  for (pi = _popups.begin(); pi != _popups.end(); ++pi) {
    MarginPopup *popup = (*pi).first;
    PopupInfo &info = (*pi).second;

    if (info._wants_visible) {
      info._score = popup->get_score();
      by_score.push_back(pi);
    }
  }

  sort(by_score.begin(), by_score.end(), SortPopupsByScore());

  // Now all the popups on the head of this list will be visible, and
  // all the ones on the tail will be invisible.  Start from the
  // beginning of the tail and make sure they're all invisible.
  int i;
  for (i = _num_available_cells; i < (int)by_score.size(); i++) {
    pi = by_score[i];
    MarginPopup *popup = (*pi).first;
    PopupInfo &info = (*pi).second;
    if (popup->is_visible()) {
      hide(info._cell_index);
    }
  }

  // Now we can find all the empty cells.
  vector_int empty_cells;
  Cells::const_iterator ci;
  for (ci = _cells.begin(); ci != _cells.end(); ++ci) {
    if ((*ci)._is_available && (*ci)._np.is_empty()) {
      // Here's an empty cell.
      int cell_index = (ci - _cells.begin());
      empty_cells.push_back(cell_index);
    }
  }

  // Randomize the list, so we'll pull the cells out in random order.
  random_shuffle(empty_cells.begin(), empty_cells.end());


  // And place all the cells from the head of the wants-visible list.
  // There should be an empty cell available for each of them.
  for (i = 0; i < _num_available_cells; i++) {
    pi = by_score[i];
    MarginPopup *popup = (*pi).first;
    if (!popup->is_visible()) {
      int cell_index = choose_cell(popup, empty_cells);
      nassertv(cell_index >= 0);

      show(popup, cell_index);
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::choose_cell
//       Access: Private
//  Description: Chooses a particular cell for the indicated Popup,
//               from the given list of empty cells.
////////////////////////////////////////////////////////////////////
int MarginManager::
choose_cell(MarginPopup *popup, vector_int &empty_cells) {
  double now = ClockObject::get_global_clock()->get_frame_time();
  int popup_code = popup->get_object_code();

  // First, see if one of the empty cells still remembers this popup.
  vector_int::iterator ii;
  for (ii = empty_cells.begin(); ii != empty_cells.end(); ++ii) {
    int cell_index = (*ii);
    Cell &cell = _cells[cell_index];
    if ((cell._popup == popup ||
         (popup_code != 0 && cell._popup_code == popup_code)) &&
        (now - cell._hide_time) <= NametagGlobals::cell_memory_time) {
      // Here's an empty cell that remembers this popup!
      empty_cells.erase(ii);
      return cell_index;
    }
  }

  // Ok, now look for an empty cell that doesn't remember anyone.
  // We look from the back to the front to maximize the probability
  // that the cell we find is towards the back of the empty_cells list
  // (which makes the erase operation slightly faster).
  ii = empty_cells.end();
  while (ii != empty_cells.begin()) {
    --ii;
    int cell_index = (*ii);
    if (_cells[cell_index]._popup == (MarginPopup *)NULL ||
        (now - _cells[cell_index]._hide_time) > NametagGlobals::cell_memory_time) {
      // Here's one.
      empty_cells.erase(ii);
      return cell_index;
    }
  }

  // All right, if all else fails, just use the last cell.  There
  // should be at least one cell available, or we wouldn't have come
  // into choose_cell().
  nassertr(!empty_cells.empty(), -1);
  int cell_index = empty_cells.back();
  empty_cells.pop_back();

  return cell_index;
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::show
//       Access: Private
//  Description: Shows the popup within the indicated cell.
////////////////////////////////////////////////////////////////////
void MarginManager::
show(MarginPopup *popup, int cell_index) {
  nassertv(cell_index >= 0 && cell_index < (int)_cells.size());
  nassertv(_cells[cell_index]._np.is_empty());

  NodePath this_np(this);

  _cells[cell_index]._popup = popup;
  _cells[cell_index]._popup_code = popup->get_object_code();
  _cells[cell_index]._np = this_np.attach_new_node(popup);

  const LMatrix4f &mat = _cells[cell_index]._mat;
  _cells[cell_index]._np.set_mat(mat);

  _popups[popup]._cell_index = cell_index;
  popup->_cell_width = _cells[cell_index]._width;
  popup->set_visible(true);
}

////////////////////////////////////////////////////////////////////
//     Function: MarginManager::hide
//       Access: Private
//  Description: Hides whatever popup currently occupies the
//               indicated cell.
////////////////////////////////////////////////////////////////////
void MarginManager::
hide(int cell_index) {
  nassertv(cell_index >= 0 && cell_index < (int)_cells.size());
  nassertv(!_cells[cell_index]._np.is_empty());

  PT(MarginPopup) popup = _cells[cell_index]._popup;
  nassertv(popup != (MarginPopup *)NULL);

  _cells[cell_index]._np.remove_node();
  _cells[cell_index]._hide_time =
    ClockObject::get_global_clock()->get_frame_time();

  _popups[popup]._cell_index = -1;
  popup->set_visible(false);
}

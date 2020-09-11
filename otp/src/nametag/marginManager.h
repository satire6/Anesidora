// Filename: marginManager.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef MARGINMANAGER_H
#define MARGINMANAGER_H

#include "otpbase.h"
#include "marginPopup.h"

#include "pointerTo.h"
#include "pandaNode.h"
#include "pmap.h"
#include "pvector.h"
#include "vector_int.h"
#include "nodePath.h"

////////////////////////////////////////////////////////////////////
//       Class : MarginManager
// Description : This class manages the collection of MarginPopup
//               objects visible in the world.  It's responsible for
//               parenting them and setting their initial transforms
//               to place them properly margin.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP MarginManager : public PandaNode {
PUBLISHED:
  MarginManager();
  virtual ~MarginManager();

  int add_grid_cell(float x, float y,
                     float screen_left, float screen_right,
                     float screen_bottom, float screen_top);
  int add_cell(float left, float right, float bottom, float top);

  void set_cell_available(int cell_index, bool available);
  bool get_cell_available(int cell_index) const;

#ifndef NDEBUG
  void show_cells();
  void hide_cells();
#endif

public:
  void manage_popup(MarginPopup *popup);
  void unmanage_popup(MarginPopup *popup);
  void update();

public:
  // From base class PandaNode.
  virtual bool cull_callback(CullTraverser *trav, CullTraverserData &data);
  virtual bool is_renderable() const;

  virtual void write(ostream &out, int indent_level) const;

private:
  void show_visible_no_conflict();
  void show_visible_resolve_conflict();
  int choose_cell(MarginPopup *popup, vector_int &empty_cells);

  void show(MarginPopup *popup, int cell_index);
  void hide(int cell_index);

private:
  class PopupInfo {
  public:
    INLINE PopupInfo();

    int _cell_index;
    bool _wants_visible;
    float _score;
    int _code;
  };
  typedef pmap<PT(MarginPopup), PopupInfo> Popups;
  Popups _popups;

  typedef pset<MarginPopup *> PopupSet;
  typedef pmap<int, PopupSet> PopupsByCode;
  PopupsByCode _popups_by_code;

  class Cell {
  public:
    LMatrix4f _mat;
    float _width;
    bool _is_available;

    // If the cell is vacant, _np is empty; otherwise, it is non-empty.
    NodePath _np;

    // The popup pointer serves to indicate both the current popup in
    // the cell, if the cell is occupied, and the last popup to occupy
    // the cell, if it is vacant.
    MarginPopup *_popup;
    int _popup_code;

    // This represents the time at which the cell last became vacant.
    double _hide_time;
  };

  LVecBase3f _cell_scale;
  typedef pvector<Cell> Cells;
  Cells _cells;
  int _num_available_cells;

#ifndef NDEBUG
  NodePath _show_cells;
#endif

  // This STL function object is used to sort a vector of Popups
  // iterators in descending order by the score, for placing just the
  // most important MarginPopups when we don't have enough space for
  // all of them.
  class SortPopupsByScore {
  public:
    INLINE bool operator () (Popups::iterator i1, Popups::iterator i2) const;
  };

public:
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    PandaNode::init_type();
    register_type(_type_handle, "MarginManager",
                  PandaNode::get_class_type());
  }

private:
  static TypeHandle _type_handle;
};

#include "marginManager.I"

#endif

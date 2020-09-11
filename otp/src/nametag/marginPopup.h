// Filename: marginPopup.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef MARGINPOPUP_H
#define MARGINPOPUP_H

#include "otpbase.h"

#include "pandaNode.h"
#include "updateSeq.h"
#include "nodePath.h"

////////////////////////////////////////////////////////////////////
//       Class : MarginPopup
// Description : This is a special kind of Node that represents
//               geometry that may appear along the edges of the
//               screen during gameplay.  In particular, this will be
//               a Nametag2d or a WhisperPopup message.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP MarginPopup : public PandaNode {
public:
  MarginPopup();
  virtual ~MarginPopup();

  virtual float get_score();
  virtual int get_object_code();

PUBLISHED:
  INLINE bool is_managed() const;
  INLINE bool is_visible() const;

public:
  INLINE float get_cell_width() const;

protected:
  virtual void update_contents();
  virtual void frame_callback();
  virtual bool consider_manage();
  virtual bool consider_visible();
  virtual void set_managed(bool flag);
  virtual void set_visible(bool flag);

protected:
  UpdateSeq _master_margin_prop_seq;
  NodePath _this_np;

private:
  bool _managed;
  bool _visible;
  float _cell_width;

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
    register_type(_type_handle, "MarginPopup",
                  PandaNode::get_class_type());
  }

private:
  static TypeHandle _type_handle;

  friend class MarginManager;
};

#include "marginPopup.I"

#endif

// Filename: nametag3d.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef NAMETAG3D_H
#define NAMETAG3D_H

#include "otpbase.h"

#include "nametag.h"
#include "pandaNode.h"
#include "pointerTo.h"
#include "pStatCollector.h"
#include "nodePath.h"

class ChatBalloon;

////////////////////////////////////////////////////////////////////
//       Class : Nametag3d
// Description : This is a particular kind of Nametag that hovers over
//               the avatar's head in the 3-d world.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP Nametag3d : public Nametag, public PandaNode {
public:
  Nametag3d();
  virtual ~Nametag3d();

PUBLISHED:
  INLINE void set_billboard_offset(float billboard_offset);
  INLINE float get_billboard_offset() const;

public:
  // From base class PandaNode.
  virtual bool safe_to_flatten() const;
  virtual bool safe_to_flatten_below() const;
  virtual bool cull_callback(CullTraverser *trav, CullTraverserData &data);

  // From base class Nametag.
  virtual void release(const MouseWatcherParameter &param);

protected:
  // from base class Nametag.
  virtual void update_contents();
  virtual void manage(MarginManager *manager);
  virtual void unmanage(MarginManager *manager);

private:
  void generate_name();
  void generate_chat(ChatBalloon *balloon);
  void adjust_to_camera(const NodePath &this_np, int bin_sort);

protected:
  bool _for_3d;

private:
  float _billboard_offset;

  NodePath _top;
  NodePath _name;
  NodePath _card;
  NodePath _balloon;

  bool _has_frame;
  LVecBase4f _frame;

public:
  // Statistics
  static PStatCollector _contents_pcollector;
  static PStatCollector _adjust_pcollector;

public:
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

PUBLISHED:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
public:
  static void init_type() {
    Nametag::init_type();
    PandaNode::init_type();
    register_type(_type_handle, "Nametag3d",
                  Nametag::get_class_type(),
                  PandaNode::get_class_type());
  }

private:
  static TypeHandle _type_handle;
};

#include "nametag3d.I"

#endif


// Filename: nametag2d.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef NAMETAG2D_H
#define NAMETAG2D_H

#include "otpbase.h"

#include "nametag.h"
#include "marginPopup.h"
#include "pStatCollector.h"
#include "nodePath.h"

class ChatBalloon;

////////////////////////////////////////////////////////////////////
//       Class : Nametag2d
// Description : This is a particular kind of Nametag that appears on
//               the margins of the screen.
//
//               Unlike a Nametag3d, a Nametag2d need not be
//               explicitly parented to any node.  Instead, it should
//               be managed() by an MarginManager, which will be
//               responsible for parenting it in an out of the scene
//               graph as appropriate.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP Nametag2d : public Nametag, public MarginPopup {
public:
  Nametag2d();
  virtual ~Nametag2d();

public:
  // From base class PandaNode.
  virtual bool cull_callback(CullTraverser *trav, CullTraverserData &data);

  // From base class MarginPopup.
  virtual float get_score();
  virtual int get_object_code();

protected:
  // from base class Nametag.
  virtual void update_contents();
  virtual void manage(MarginManager *manager);
  virtual void unmanage(MarginManager *manager);

  // from base class MarginPopup.
  virtual void frame_callback();
  virtual bool consider_visible();
  virtual void set_managed(bool flag);
  virtual void set_visible(bool flag);

private:
  void generate_name();
  void generate_chat(ChatBalloon *balloon);
  void rotate_arrow();
  float get_distance2() const;

private:
  NodePath _name;
  NodePath _card;
  NodePath _arrow;
  NodePath _balloon;
  LPoint3f _arrow_center;
  bool _master_arrows;

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
    MarginPopup::init_type();
    register_type(_type_handle, "Nametag2d",
                  Nametag::get_class_type(),
                  MarginPopup::get_class_type());
  }

private:
  static TypeHandle _type_handle;
};

#include "nametag2d.I"

#endif


// Filename: nametag.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef NAMETAG_H
#define NAMETAG_H

#include "otpbase.h"
#include "popupMouseWatcherRegion.h"
#include "clickablePopup.h"

#include "referenceCount.h"
#include "pointerTo.h"
#include "pgButton.h"
#include "updateSeq.h"
#include "nodePath.h"
#include "cInterval.h"
#include "mouseWatcher.h"

class NametagGroup;
class MouseWatcherParameter;
class MarginManager;

////////////////////////////////////////////////////////////////////
//       Class : Nametag
// Description : This is an abstract base class defining the interface
//               to a nametag object.  This is an object that may be
//               attached to a NametagGroup and is typically
//               associated with an avatar; it displays the avatar's
//               name and/or his chat messages, and can be clicked on
//               to select the avatar.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP Nametag : virtual public ReferenceCount, public ClickablePopup {
public:
  Nametag(float chat_wordwrap);
  virtual ~Nametag();

  void deactivate();

PUBLISHED:
  enum Contents {
    C_name     = 0x0001,
    C_speech   = 0x0002,
    C_thought  = 0x0004,
  };

  INLINE void set_contents(int flags);
  INLINE int get_contents() const;

  INLINE void set_active(bool active);
  INLINE bool is_active() const;
  bool display_as_active() const;

  INLINE bool has_group() const;
  INLINE NametagGroup *get_group() const;

  INLINE void set_draw_order(int draw_order);
  INLINE void clear_draw_order();

  INLINE void set_chat_wordwrap(float wordwrap);
  INLINE float get_chat_wordwrap() const;

  INLINE void set_avatar(const NodePath &node);
  INLINE void clear_avatar();
  const NodePath &get_avatar() const;

public:
  bool is_group_managed() const;

  // From base class ClickablePopup.
  virtual void click();
  virtual PGButton::State get_state() const;

protected:
  int determine_contents();

  virtual void manage(MarginManager *manager);
  virtual void unmanage(MarginManager *manager);

  void set_region(const LVecBase4f &frame, int sort = 0);
  void keep_region();
  void clear_region();

  void start_flash(NodePath &button);
  void stop_flash();

  int _current_contents;

  int _draw_order;
  bool _has_draw_order;

private:
  void update_region(UpdateSeq region_seq);

  int _contents;
  bool _active;
  NametagGroup *_group;
  float _chat_wordwrap;
  NodePath _avatar;

  string _flash_track_name;
  PT(CInterval) _flash_track;

  PT(PopupMouseWatcherRegion) _region;

  bool _region_active;
  UpdateSeq _region_seq;
  PT(MouseWatcher) _mouse_watcher;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    ReferenceCount::init_type();
    register_type(_type_handle, "Nametag",
                  ReferenceCount::get_class_type());
  }

PUBLISHED:
  // We define get_type() even though we don't inherit from
  // TypedObject.  We can't actually inherit from TypedObject because
  // of the whole multiple-inheritance thing in our derived classes.
  virtual TypeHandle get_type() const {
    return get_class_type();
  }

private:
  static TypeHandle _type_handle;

  friend class NametagGroup;
};

#include "nametag.I"

#endif

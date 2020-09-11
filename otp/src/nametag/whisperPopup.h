// Filename: whisperPopup.h
// Created by:  drose (25Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef WHISPERPOPUP_H
#define WHISPERPOPUP_H

#include "otpbase.h"

#include "clickablePopup.h"
#include "marginPopup.h"
#include "popupMouseWatcherRegion.h"

#include "textFont.h"
#include "pointerTo.h"
#include "nodePath.h"
#include "mouseWatcher.h"

class ChatBalloon;
class MarginManager;

////////////////////////////////////////////////////////////////////
//       Class : WhisperPopup
// Description : This is a whisper message that pops up on the screen
//               from someone else in the game.  It's not associated
//               with a Nametag, but it occupies the same space in the
//               screen that Nametag2d's occupy.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP WhisperPopup : public MarginPopup, public ClickablePopup {
PUBLISHED:
  // Types of whisper messages.
  enum WhisperType {
    WT_normal,
    WT_quick_talker,
    WT_system,
    WT_battle_SOS,
    WT_emote,
	WT_toontown_boarding_group
  };

  WhisperPopup(const string &text, TextFont *font, WhisperType whisper_type);
  virtual ~WhisperPopup();

  void set_clickable(const string &avatar_name, int avatar_id, int is_player_id = 0);

  void manage(MarginManager *manager);
  void unmanage(MarginManager *manager);

public:
  // From base class PandaNode.
  virtual bool cull_callback(CullTraverser *trav, CullTraverserData &data);

  // From base class MarginPopup.
  virtual float get_score();

  // From base class ClickablePopup.
  virtual void click();

protected:
  // From base class MarginPopup.
  virtual void update_contents();
  virtual bool consider_manage();
  virtual bool consider_visible();
  virtual void set_visible(bool flag);

private:
  void generate_text(ChatBalloon *balloon, const string &text, TextFont *font);
  void set_region(const LVecBase4f &frame, int sort = 0);

  bool _has_rendered;
  double _first_appeared;

  string _text;
  PT(TextFont) _font;
  WhisperType _whisper_type;

  NodePath _balloon;

  bool _clickable;
  string _avatar_name;
  int _avatar_id;
  bool _is_player_id;

  PT(PopupMouseWatcherRegion) _region;
  PT(MouseWatcher) _mouse_watcher;

public:
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    MarginPopup::init_type();
    register_type(_type_handle, "WhisperPopup",
                  MarginPopup::get_class_type());
  }

private:
  static TypeHandle _type_handle;
};

#include "whisperPopup.I"

#endif

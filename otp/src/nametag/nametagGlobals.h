// Filename: nametagGlobals.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef NAMETAGGLOBALS_H
#define NAMETAGGLOBALS_H

#include "otpbase.h"
#include "nametagGroup.h"
#include "chatBalloon.h"
#include "whisperPopup.h"

#include "luse.h"
#include "pointerTo.h"
#include "nodePath.h"
#include "audioSound.h"
#include "mouseWatcher.h"
#include "pointerTo.h"
#include "textNode.h"
#include "updateSeq.h"
#include "pgButton.h"

static const int max_button_states = 4;  // From PGButton::State.

////////////////////////////////////////////////////////////////////
//       Class : NametagGlobals
// Description : This class serves primarily as a storage point for
//               global parameters that affect Nametags, both of the
//               2-d and 3-d variety.  Some of these can be (and must
//               be!) defined at runtime by the Python code; others
//               are compiled in.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP NametagGlobals {
PUBLISHED:
  INLINE static float get_name_wordwrap();
  INLINE static const LVecBase4f &get_card_pad();

  INLINE static void set_camera(const NodePath &node);
  INLINE static const NodePath &get_camera();

  INLINE static void set_toon(const NodePath &node);
  INLINE static const NodePath &get_toon();

  INLINE static void set_arrow_model(const NodePath &node);
  INLINE static const NodePath &get_arrow_model();

  INLINE static void set_page_button(int state, const NodePath &node);
  INLINE static const NodePath &get_page_button(int state);

  INLINE static void set_quit_button(int state, const NodePath &node);
  INLINE static const NodePath &get_quit_button(int state);

  INLINE static void set_nametag_card(const NodePath &node, const LVecBase4f &frame);
  INLINE static const NodePath &get_nametag_card();
  INLINE static const LVecBase4f &get_nametag_card_frame();

  INLINE static void set_rollover_sound(AudioSound *sound);
  INLINE static AudioSound *get_rollover_sound();

  INLINE static void set_click_sound(AudioSound *sound);
  INLINE static AudioSound *get_click_sound();

  INLINE static void set_mouse_watcher(MouseWatcher *watcher);
  INLINE static MouseWatcher *get_mouse_watcher();

  INLINE static void set_speech_balloon_2d(ChatBalloon *balloon);
  INLINE static ChatBalloon *get_speech_balloon_2d();

  INLINE static void set_thought_balloon_2d(ChatBalloon *balloon);
  INLINE static ChatBalloon *get_thought_balloon_2d();

  INLINE static void set_speech_balloon_3d(ChatBalloon *balloon);
  INLINE static ChatBalloon *get_speech_balloon_3d();

  INLINE static void set_thought_balloon_3d(ChatBalloon *balloon);
  INLINE static ChatBalloon *get_thought_balloon_3d();

  INLINE static void set_master_nametags_active(bool active);
  INLINE static bool get_master_nametags_active();

  INLINE static void set_master_nametags_visible(bool visible);
  INLINE static bool get_master_nametags_visible();

  INLINE static void set_master_arrows_on(bool active);
  INLINE static bool get_master_arrows_on();

  INLINE static void set_onscreen_chat_forced(bool active);
  INLINE static bool get_onscreen_chat_forced();

  INLINE static void set_max_2d_alpha(float alpha);
  INLINE static float get_max_2d_alpha();

  INLINE static void set_min_2d_alpha(float alpha);
  INLINE static float get_min_2d_alpha();

  INLINE static void set_global_nametag_scale(float scale);
  INLINE static float get_global_nametag_scale();

  INLINE static const Colorf &get_name_fg(NametagGroup::ColorCode color_code,
                                          PGButton::State state);
  INLINE static const Colorf &get_name_bg(NametagGroup::ColorCode color_code,
                                          PGButton::State state);

  INLINE static const Colorf &get_balloon_modulation_color();
  INLINE static void set_balloon_modulation_color(const Colorf &color);

public:
  static const float billboard_offset;
  static const float far_distance;
  static const float far_scale;
  static const float scale_exponent;

  static const float arrow_scale;
  static const float arrow_offset;

  static const LVecBase4f card_pad;

  static const float nominal_avatar_width;

  static const float name_wordwrap;
  static const float building_name_wordwrap;
  static const float house_name_wordwrap;
  static const float chat_2d_wordwrap;
  static const float chat_3d_wordwrap;
  static const float balloon_internal_width;
  static const float balloon_external_width;
  static const float balloon_min_hscale;
  static const LPoint3f balloon_text_origin;

  static const float grid_count_horizontal;
  static const float grid_count_vertical;
  static const float grid_spacing_horizontal;
  static const float grid_spacing_vertical;

  static const double cell_memory_time;

  static const double whisper_priority_time;
  static const double whisper_total_time;

  static const double button_delay_time;

  static const float building_nametag_distance;

  static const Colorf default_qt_color;
  static const Colorf default_balloon_modulation_color;

  static UpdateSeq margin_prop_seq;

  static TextNode *get_text_node();

  class Colors {
  public:
    Colors(const Colorf &name_fg,
           const Colorf &name_bg,
           const Colorf &chat_fg,
           const Colorf &chat_bg);

    Colorf _name_fg;
    Colorf _name_bg;
    Colorf _chat_fg;
    Colorf _chat_bg;
  };

  static const Colorf &get_arrow_color(NametagGroup::ColorCode color_code);

  static const Colors &get_colors(NametagGroup::ColorCode color_code,
                                  PGButton::State state);

  static const Colors &get_whisper_colors(WhisperPopup::WhisperType type,
                                          PGButton::State state);


private:
  static NodePath _camera;
  static NodePath _toon;
  static NodePath _arrow_model;
  static NodePath _page_button[max_button_states];
  static NodePath _quit_button[max_button_states];
  static NodePath _nametag_card;
  static LVecBase4f _nametag_card_frame;

  static PT(AudioSound) _rollover_sound;
  static PT(AudioSound) _click_sound;

  static PT(MouseWatcher) _mouse_watcher;

  static PT(TextNode) _text_node;

  static PT(ChatBalloon) _speech_balloon_2d;
  static PT(ChatBalloon) _thought_balloon_2d;
  static PT(ChatBalloon) _speech_balloon_3d;
  static PT(ChatBalloon) _thought_balloon_3d;

  static bool _master_nametags_active;
  static bool _master_nametags_visible;
  static bool _master_arrows_on;
  static bool _onscreen_chat_forced;

  static float _max_2d_alpha;
  static float _min_2d_alpha;

  static float _global_nametag_scale;

  static Colorf balloon_modulation_color;
};

#include "nametagGlobals.I"

#endif

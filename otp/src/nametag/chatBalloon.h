// Filename: chatBalloon.h
// Created by:  drose (23Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef CHATBALLOON_H
#define CHATBALLOON_H

#include "otpbase.h"

#include "referenceCount.h"
#include "pointerTo.h"
#include "luse.h"

class TextFont;
class PandaNode;
class NodePath;

////////////////////////////////////////////////////////////////////
//       Class : ChatBalloon
// Description : This class encapsulates a model specifically made for
//               putting text into as a speech or thought balloon that
//               floats over an avatar's head, or appears in a little
//               rectangle in the margins onscreen.
//
//               It is created with a particular model loaded from
//               disk, which is expected to include a node named
//               "chatBalloon", with three children named "bottom",
//               "middle", and "top".
//
//               These nodes will be sized and translated
//               appropriately to frame the text as generated.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP ChatBalloon : public ReferenceCount {
PUBLISHED:
  ChatBalloon(PandaNode *root_node);
  ~ChatBalloon();
  PT(PandaNode) generate(const string &text, TextFont *font, float wordwrap,
                         const Colorf &text_color, const Colorf &balloon_color,
                         bool for_3d, bool has_draw_order, int draw_order,
                         const NodePath &page_button, bool space_for_button,
                         bool reversed, NodePath &new_button);

public:
  INLINE float get_hscale() const;
  INLINE float get_text_height() const;
  INLINE const LVecBase4f &get_text_frame() const;

private:
  bool scan(PandaNode *node);
  bool scan_balloon(PandaNode *node);

  static PandaNode *find_middle_geom(PandaNode *parent);
  static PandaNode *find_geom_node(PandaNode *parent);

  PT(PandaNode) _parent;
  PT(PandaNode) _top_node;
  PT(PandaNode) _middle_node;
  PT(PandaNode) _bottom_node;

  LMatrix4f _top_mat;
  LMatrix4f _middle_mat;

  float _hscale;
  float _text_height;
  LVecBase4f _text_frame;
};

#include "chatBalloon.I"

#endif

// Filename: chatBalloon.I
// Created by:  drose (23Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::get_hscale
//       Access: Public
//  Description: Returns the horizontal scale applied to the chat
//               balloon in the last call to generate().
////////////////////////////////////////////////////////////////////
INLINE float ChatBalloon::
get_hscale() const {
  return _hscale;
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::get_text_height
//       Access: Public
//  Description: Returns the height of the text within the balloon, in
//               scaled units.
////////////////////////////////////////////////////////////////////
INLINE float ChatBalloon::
get_text_height() const {
  return _text_height;
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::get_text_frame
//       Access: Public
//  Description: Returns the size of the rectangular region that
//               tightly bounds the text within the balloon.
////////////////////////////////////////////////////////////////////
INLINE const LVecBase4f &ChatBalloon::
get_text_frame() const {
  return _text_frame;
}

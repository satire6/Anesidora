// Filename: dnaSignText.I
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////


INLINE void DNASignText::
set_color(const Colorf &color) {
  _use_baseline_color = false;
  _color = color;
}

INLINE Colorf DNASignText::
get_color() const {
  return _color;
}

INLINE void DNASignText::
set_code(string code) {
  _code = code;
}

INLINE string DNASignText::
get_code() const {
  return _code;
}

INLINE void DNASignText::
set_letters(string letters) {
  _letters = letters;
}

INLINE string DNASignText::
get_letters() const {
  return _letters;
}

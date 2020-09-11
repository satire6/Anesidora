// Filename: dnaSignGraphic.I
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////


INLINE void DNASignGraphic::
set_code(string code) {
  _code = code;
}

INLINE string DNASignGraphic::
get_code() const {
  return _code;
}

INLINE void DNASignGraphic::
set_color(const Colorf &color) {
  _use_baseline_color = false;
  _color = color;
}

INLINE Colorf DNASignGraphic::
get_color() const {
  return _color;
}

INLINE void DNASignGraphic::
set_width(float width) {
  _width = width;
}

INLINE float DNASignGraphic::
get_width() const {
  return _width;
}

INLINE void DNASignGraphic::
set_height(float height) {
  _height = height;
}

INLINE float DNASignGraphic::
get_height() const {
  return _height;
}

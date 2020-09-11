
#ifndef PATHTABLE_H
#define PATHTABLE_H

#include <string>
#include <vector>
#include <iostream>
#include <assert.h>

#include "otpbase.h"
#include "Python.h"

typedef std::vector<unsigned short> VectorUS;
typedef std::basic_string<unsigned char> StringUC;

////////////////////////////////////////////////////////////////////
//       Class : PathTable
////////////////////////////////////////////////////////////////////
class EXPCL_OTP PathTable {
PUBLISHED:
  PathTable();
  PathTable(PyObject* pathData, PyObject* connections);
  ~PathTable();

  void initTable(PyObject* pathData, PyObject* connections);

  INLINE PyObject* findRoute(unsigned short startNode, unsigned short goalNode);

private:
  std::vector<StringUC> _pathData;
  std::vector<VectorUS> _connectionData;

  INLINE unsigned char nextStepLookup(unsigned short startNode, unsigned short goalNode);
};

#include "pathTable.I"

#endif


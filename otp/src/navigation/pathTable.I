
// PathTable lookup functions.
// "The bit we care about optimizing."


// nextStepLookup: Finds the next node in the optimal path from startNode to goalNode.
INLINE unsigned char PathTable::
nextStepLookup(unsigned short startNode, unsigned short goalNode) {
  assert(startNode < _pathData.size());
  assert(goalNode < _pathData.size());

  StringUC *str = &_pathData[startNode];

  unsigned short pos = 0;

  while((pos < str->size()) && ((256*(unsigned short)str->at(pos) + (unsigned short)str->at(pos+1)) <= goalNode)) {
    pos += 3;
  }

  pos -= 3;

  return str->at(pos+2);
}


// findRoute: Finds all nodes in the optimal path from startNode to goalNode.
INLINE PyObject* PathTable::
findRoute(unsigned short startNode, unsigned short goalNode) {
  assert(startNode < _pathData.size());
  assert(goalNode < _pathData.size());

  PyObject *route = PyList_New(0);
  PyObject *num;
  unsigned short currNode = startNode;

  num = PyInt_FromLong((long)startNode);

  PyList_Append(route,num);
  Py_DECREF(num);
  
  while(currNode != goalNode) {
    currNode = _connectionData[currNode][nextStepLookup(currNode,goalNode)];

    assert(currNode != 65535);

    num = PyInt_FromLong((long)currNode);
  
    PyList_Append(route,num);
    Py_DECREF(num);
  }

  return route;
}

// Filename: log.cxx
// Created by:
//
////////////////////////////////////////////////////////////////////

#include "pragma.h"
#include <windows.h>
#include "log.h"

ofstream errorLog;

int openLogFile(const char *filename)
{
  //errorLog.open(filename, ios_base::out | ios_base::app); // append

#if 0
  // this becomes unnecessary since we now name logs by time
  // also, errorLog.fail() returns true occasionally.  could this DeleteFile be causing it?

  //delete previous log, so file creation time becomes same as log creation time
  DeleteFile(filename);
#endif

  if(errorLog.is_open()) {
     // bugbug: need to check if filename the same as currently open log.  if so, return 0.
     errorLog.close();
  }

  // Make sure the fail bits are cleared before we try to open.
  // Failing to clear this may make the errorLog seem to return fail()
  // even though it has successfully been opened.
  errorLog.clear();
  errorLog.open(filename, ios_base::out | ios_base::trunc); // overwrite
  errorLog.flags(errorLog.flags() | ios::unitbuf);

  return errorLog.fail();
}

#if _MSC_VER < 1300
// int64 stream handlers
std::ostream& operator<<(std::ostream& os, __int64 i )
{
    char buf[20];
    sprintf(buf,"%I64d", i );
    os << buf;
    return os;
}

std::ostream& operator<<(std::ostream& os, unsigned __int64 i )
{
    char buf[20];
    sprintf(buf,"%I64d", i );
    os << buf;
    return os;
}
#endif

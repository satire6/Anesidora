#include <windows.h>

extern char *URLEncode(const char *lpBuffer,DWORD cbSize,char *pOutputBuf,DWORD cbOutputSize,const char *pIgnoreChSet);
extern char *URLEncode2(char *lpBuffer,DWORD cbSize);


/// VFPUrlEncode
/// Wrapper around URLEncode
/// Returns physical string in a buffer
//unsigned int VFPURLEncode(char *lpInputBuffer, unsigned int cbInputSize);


#include "urlencode.h"

// utility fns to urlencode and urldecode a string

// #if out urldecode stuff until we need it
#if 0
//----------------------------------------------------------------------
//    FUNCTION: HexToAscii
//
//   PURPOSE: This function will replace %xx (hexadecemal) symbols to the
//           ASCII representation by calling HexToAscii .
//----------------------------------------------------------------------
char HexToAscii(char *lpString)
{
    char CH;

    CH =  (lpString[0] >= 'A' ? ( (lpString[0] & 0xDF) - 'A' ) + 10
: (lpString[0] - '0') );
    CH *= 16;
    CH += (lpString[1] >= 'A' ? ( (lpString[1] & 0xDF) - 'A' ) + 10
: (lpString[1] - '0') );

    return CH;
}

///////////////////////////////////////////////////////////////////////

//----------------------------------------------------------------------
//   FUNCTION: EscapeToAscii
//
//   PURPOSE: This function calls HexToAscii for each occurance of %xx in the
//           parametr string.
//----------------------------------------------------------------------
void EscapeToAscii(char *lpEscape)
{
    int i, j;

    for( i = 0, j = 0; lpEscape[j] ; ++i, ++j )
    {
        if( (lpEscape[i] = lpEscape[j]) == '%' )
        {
            lpEscape[i] = HexToAscii( &lpEscape[j+1] );
            j+=2;
        }
    }

    lpEscape[i] = '\0';
}


DWORD  EscapeToAscii2(char *lpEscape)
{
    DWORD i, j;

    for( i = 0, j = 0; lpEscape[j] ; ++i, ++j )
    {
        if( (lpEscape[i] = lpEscape[j]) == '%' )
        {
            lpEscape[i] = HexToAscii( &lpEscape[j+1] );
            j+=2;
        }
    }

   return i;

}

//----------------------------------------------------------------------
// FUNCTION: GetKeyValue
//
// PURPOSE: This function return value assosiated with lpszParam in the
//        lpszQuery string.
//
// COMMENTS:
//    Don't forget to free the returned new string with delete []!
//     If  lpszQuery   does not have  lpszParam  in it or no value
//        is assisiated with with  lpszParam  NULL will be return.
//    Example:
//             lpszQuery = "COMMAND1=Test1&COMMAND2=Test2"
//             lpszParam = "COMMAND2"
//            Return string: Test2
//----------------------------------------------------------------------
char *GetKeyValue(char *lpszQuery, char *lpszParam)
{
    char *pValueStart = NULL;
    char *pValueEnd   = NULL;
    char *lpszValue   = NULL;
    char *szTemp1     = NULL;
    DWORD cbValue;

    // Find the value passed in by the client for some particular
    // parameter within the query string.
    //
    // First we find the occurance of the parameter, add the length of the
    // parameter name, and then add one for the "=" character put between
    // the parameter and the value; this locates the value.
    pValueStart = strstr( lpszQuery, lpszParam );
    if( !pValueStart || (pValueStart[lstrlen(lpszParam)] != '='))
    // parameter doesn't exist
       return NULL;

    pValueStart += lstrlen( lpszParam ) + 1;

    // Now determine the length of the value string.
    pValueEnd = strchr(pValueStart, '&');
    if(pValueEnd)
        // if this wasn't the last param in the list
        cbValue = pValueEnd - pValueStart;
    else
        // this was the last param in the list
        cbValue = lstrlen(pValueStart);

    // Return NULL if we  have zero length string.
    if( !cbValue )
        return NULL;

    lpszValue = new char[cbValue + 1];
    if(!lpszValue)
        return NULL;

    ZeroMemory(lpszValue,(cbValue + 1));

    strncpy(lpszValue, pValueStart, cbValue);

    // Finally lpszValue has needed value.

    // Now replace "+" characters with " " characters adn
    // "%xx" (hexadecemal) to the ASCII representation.

    for(szTemp1 = lpszValue;(*szTemp1!='\0');szTemp1++ ) {
        if( *szTemp1 == '+' )
            *szTemp1 = ' ';
    }

    EscapeToAscii(lpszValue);

    return lpszValue;
}

unsigned int URLDecode(char *lpBuffer) {
   unsigned int lnSize;
   char *lpWork = lpBuffer;

   if (!lpBuffer)
      return 0;

   lnSize=lstrlen(lpBuffer);

   while( * lpBuffer ) {
        if( *lpBuffer ==  '+' )
            *lpBuffer = ' ';
        lpBuffer++;
    }

   lnSize = EscapeToAscii2(lpWork);
   return lnSize;
}

#endif

char *URLEncode2(char *lpBuffer,DWORD cbSize) {
    return URLEncode(lpBuffer,cbSize,NULL,0,NULL);
}

char *URLEncode(const char *lpBuffer,DWORD cbSize,char *pOutputBuf,DWORD cbOutputSize,const char *pIgnoreChSet) {
   char  *lpszValue, *lpszResult;
   DWORD cbCount = 0;

   if (cbSize == 0)
       return NULL;

   DWORD cbBuffer;

   if(pOutputBuf!=NULL) {
       lpszResult=pOutputBuf;
       cbBuffer = cbSize * 3 + 1;
   } else {
       // if no outputbuf passed in, alloc and return one
       // caller make sure to delete [] it!
       cbBuffer = cbSize * 3 + 1;
       lpszResult=new char[cbBuffer];
       if (!lpszResult)
          return NULL;
   }

   // encoded chars will lengthen output string, so init the output string to be 3 times larger
   // than original (is this worst case?)
   ZeroMemory(lpszResult,cbBuffer);

   /// Create work pointer to walk the string
   lpszValue = lpszResult;

   for(DWORD x=0; x < cbSize; x++)  {
      if ( (*lpBuffer >= 'a' && *lpBuffer <='z') ||
           (*lpBuffer >= 'A' && *lpBuffer <='Z') ||
           (*lpBuffer >= '0' && *lpBuffer <='9'))
          *lpszValue =  *lpBuffer;
      else if (*lpBuffer == ' ')
          *lpszValue = '+';
      else {
        if(pIgnoreChSet!=NULL) {
            for(const char *pCh=pIgnoreChSet;*pCh!='\0';pCh++) {
                if(*pCh==*lpBuffer) {
                   *lpszValue =  *lpBuffer;
                   goto skipconversion;
                }
            }
        }
        /// Convert to hex: %XX
        wsprintf(lpszValue,"%%%02X",(unsigned char) *lpBuffer);
        lpszValue += 2;
        cbCount += 2;
      }

     skipconversion:

      lpBuffer++;
      lpszValue++;
      cbCount++;
   }

   // Terminating NULL
   *lpszValue = '\0';

   return lpszResult;
}

#if 0
/// Wrapper around URLEncode
/// overwrites input str w/output str
unsigned int VFPURLEncode(char *lpInputBuffer, unsigned int cbInputSize) {

   char *lpzEncoded = URLEncode(lpInputBuffer,cbInputSize,NULL,NULL);

   if(!lpzEncoded)
      return 0;

   lstrcpy(lpInputBuffer,lpzEncoded);

   cbInputSize=lstrlen(lpzEncoded);
   delete [] lpzEncoded;
   return cbInputSize;
}
#endif

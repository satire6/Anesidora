#include "stdafx.h"

static  const char  szEnvKeyToAddToChildProcessEnvBlock []  = "DisneyOnlineGamesToken";
static  const char  szInstallerCommandLineOptionPrefix  []  = "/";
static  const char  szInstallerSilentRunModeOption      []  = "S";

typedef struct _tag_MMOG_FLAVOR
{
    const   int     mode;
    const   char *  pszInstallerURL;
    const   char *  pszLauncherCSIDL;
    const   char *  pszLauncherPathname;
} MMOG_FLAVOR, *PMMOG_FLAVOR;

static  const   MMOG_FLAVOR     gsc_mmogFlavor  []  = {
    {
        // Development
        1,
        "http://build64.online.disney.com:3120/english/currentVersion/dev/PotC-setup_DEV.exe",
        "PROGRAM_FILES",
        "\\Disney\\Disney Online\\PiratesOnline_DEV\\Launcher1.exe",
    }
    ,
    {   // QA
        2,
        "http://pirate143b.starwave.com:1420/english/currentVersion/qa/PotC-setup_QA.exe",
        "PROGRAM_FILES",
        "\\Disney\\Disney Online\\PiratesOnline_QA\\Launcher1.exe",
    }
    ,
    {   // Test
        3,
        "http://download.test.piratesonline.com/english/currentVersion/PotC-setup_TEST.exe",
        "PROGRAM_FILES",
        "\\Disney\\Disney Online\\PiratesOnline_TEST\\Launcher1.exe",
    }
    ,
    {   // Live
        4,
        "http://download.piratesonline.com/english/currentVersion/PotC-setup.exe",
        "PROGRAM_FILES",
        "\\Disney\\Disney Online\\PiratesOnline\\Launcher1.exe",
    }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static  const char  c_szFolderNameDelimiter_DOS []  = "\\";
static  const char  c_chFolderNameDelimiter_UNIX    = '/';

#if defined(_DEBUG)
#define ODS(s)  { printf (s); printf ("\r\n"); }
#endif

static  char   *g_paszAcceptTypes []  = { "*/*", NULL };

#if defined(_DEBUG)
PSZ     CRunPiratesOnline::get_http_specific_error_description (DWORD  dwError)
{ 
    switch (dwError)
    {
    case 12001:
        return  "Out of handles";
    case 12002:
        return  "Timeout";
    case 12004:
        return  "Internal Error";
    case 12005:
        return  "Invalid URL";
    case 12007:
        return  "Service Name Not Resolved";
    case 12008:
        return  "Protocol Not Found";
    case 12013:
        return  "Incorrect User Name";
    case 12014:
        return  "Incorrect Password";
    case 12015:
        return  "Login Failure";
    case 12016:
        return  "Invalid Operation";
    case 12017:
        return  "Operation Canceled";
    case 12020:
        return  "Not Proxy Request";
    case 12023:
        return  "No Direct Access";
    case 12026:
        return  "Request Pending";
    case 12027:
        return  "Incorrect Format";
    case 12028:
        return  "Item not found";
    case 12029:
        return  "Cannot connect";
    case 12030:
        return  "Connection Aborted";
    case 12031:
        return  "Connection Reset";
    case 12033:
        return  "Invalid Proxy Request";
    case 12034:
        return  "Need UI";
    case 12035:
        return  "Sec Cert Date Invalid";
    case 12038:
        return  "Sec Cert CN Invalid";
    case 12044:
        return  "Client Auth Cert Needed";
    case 12045:
        return  "Invalid CA Cert";
    case 12046:
        return  "Client Auth Not Setup";
    case 12150:
        return  "HTTP Header Not Found";
    case 12152:
        return  "Invalid HTTP Server Response";
    case 12153:
        return  "Invalid HTTP Header";
    case 120154:
        return  "Invalid Query Request";
    case 120156:
        return  "Redirect Failed";
    case 120159:
        return  "TCP/IP not installed";
    default:
        return  "Error";
    }
}
#endif

ENUM_RESPONSE_CODE  CRunPiratesOnline::response_data_available_and_successfully_read   (HINTERNET   hRequest,
                                                                                        char *      pszHttpResponseData,
                                                                                        DWORD       dwNumHttpResponseDataBufferBytes,
                                                                                        DWORD *     pdwNumBytesResponseDataRead)
{
    // If we can NOT query the server to determine the amount of data available
    DWORD   dwNumberOfBytesAvailableToBeRead    = 0;
    if (!InternetQueryDataAvailable (
        hRequest,
        &dwNumberOfBytesAvailableToBeRead,
        0,
        0))
    {
#if defined(_DEBUG)
        {
            DWORD   dwLastError;
            dwLastError = GetLastError ();
            char    szMsgBuf    [1024];
            wsprintf (
                szMsgBuf,
                "%s\t%s: %u=%s",
                __FUNCTION__,
                "ERROR: InternetQueryDataAvailable",
                dwLastError,
                get_http_specific_error_description (dwLastError));
            ODS(szMsgBuf)
        }
#endif
        return  RESPONSE_CODE__CANNOT_QUERY_SERVER;
    }
    // If no data is available
    if (0 == dwNumberOfBytesAvailableToBeRead)
    {
#if defined(_DEBUG)
        {
            char    szMsgBuf    [1024];
            wsprintf (
                szMsgBuf,
                "%s\t%s: Indicates that zero (0) bytes are available to be read",
                __FUNCTION__,
                "InternetQueryDataAvailable");
            ODS(szMsgBuf)
        }
#endif
        return  RESPONSE_CODE__SUCCESS;
    }
    // If the number of bytes available to be read is more than the size of our in-memory buffer
    if (dwNumberOfBytesAvailableToBeRead > dwNumHttpResponseDataBufferBytes)
    {
        // Clamp the number of bytes to be read to the size of our in-memory buffer
        dwNumberOfBytesAvailableToBeRead    = dwNumHttpResponseDataBufferBytes;
    }
    // If the number of bytes available to be read will require a read past the end of the content
    if ((dwNumberOfBytesAvailableToBeRead + m.dwNumBytesResponseDataReadTotal) > m.dwContentLen)
    {
        // Clip the number of bytes to be read to ensure exactly m.dwContentLen bytes are read
        dwNumberOfBytesAvailableToBeRead    = m.dwContentLen - m.dwNumBytesResponseDataReadTotal;
    }
    // If we can NOT read data from the handle opened by function InternetOpenUrl
    if (!InternetReadFile (
        hRequest,
        pszHttpResponseData,
        dwNumberOfBytesAvailableToBeRead,
        pdwNumBytesResponseDataRead))
    {
#if defined(_DEBUG)
        {
            DWORD   dwLastError;
            dwLastError = GetLastError ();
            char    szMsgBuf    [1024];
            wsprintf (
                szMsgBuf,
                "%s\t%s: %u=%s",
                __FUNCTION__,
                "ERROR: InternetReadFile",
                dwLastError,
                get_http_specific_error_description (dwLastError));
            ODS(szMsgBuf)
        }
#endif
        return  RESPONSE_CODE__INTERNET_READ_FAILURE;
    }
    // If the number of byte available to be read is NOT equal to the number of bytes read
    if (dwNumberOfBytesAvailableToBeRead != *pdwNumBytesResponseDataRead)
    {
#if defined(_DEBUG)
        {
            char    szMsgBuf    [1024];
            wsprintf (
                szMsgBuf,
                "%s\t%s: The number of bytes available to be read = <%u>, but <%u> bytes were successfully read",
                __FUNCTION__,
                "ERROR: InternetReadFile",
                dwNumberOfBytesAvailableToBeRead,
                *pdwNumBytesResponseDataRead);
            ODS(szMsgBuf)
        }
#endif
        return  RESPONSE_CODE__INVALID_NUMBER_OF_BYTES_READ;
    }
#if defined(_DEBUG)
    {
        char    szMsgBuf    [1024];
        wsprintf (
            szMsgBuf,
            "%s\tSuccessfully read <%d> bytes",
            __FUNCTION__,
            *pdwNumBytesResponseDataRead);
        ODS(szMsgBuf)
    }
#endif
    // Indicate success
    return  RESPONSE_CODE__SUCCESS;
}

ENUM_RESPONSE_CODE  CRunPiratesOnline::download_installer  (HANDLE  hFile)
{
#if defined(_DEBUG)
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"ENTER: "
        "%s",__FUNCTION__);ODS(szMsgBuf)}
#endif
    ENUM_RESPONSE_CODE  enumResponseCode    = RESPONSE_CODE__SUCCESS;
    //
    char    hostnamebuf [512];
    memset (hostnamebuf, 0, sizeof (hostnamebuf));
    //
    char    urlstrbuf   [1024];
    //
    URL_COMPONENTS  url_comp;
    memset (&url_comp, 0, sizeof (url_comp));
    url_comp.dwStructSize       = sizeof (url_comp);
    url_comp.lpszHostName       = hostnamebuf;
    url_comp.dwHostNameLength   = sizeof (hostnamebuf);
    url_comp.lpszUrlPath        = urlstrbuf;
    url_comp.dwUrlPathLength    = sizeof (urlstrbuf);
    // If the source URL cannot be cracked into its component parts
#if defined(_DEBUG)
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call InternetCrackUrl",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (!InternetCrackUrl (gsc_mmogFlavor[m.immogFlavorIdx].pszInstallerURL, 0, 0x0, &url_comp))
    {
#if defined(_DEBUG)
        {
            DWORD   dwLastError;
            dwLastError = GetLastError ();
            char    szMsgBuf    [1024];
            wsprintf (
                szMsgBuf,
                "%s\t"
                "%s: %u=%s",
                __FUNCTION__,
                "ERROR: InternetCrackUrl",
                dwLastError,
                get_http_specific_error_description (dwLastError));
            ODS(szMsgBuf)
        }
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_CRACK_SOURCE_URL;
    }
    else
    if ((url_comp.nScheme != INTERNET_SCHEME_HTTP)
        &&
        (url_comp.nScheme != INTERNET_SCHEME_HTTPS)
       )
    {
#if defined(_DEBUG)
        {
            char    szMsgBuf    [1024];
            wsprintf (
                szMsgBuf,
                "%s"
                "\t"
                "ERROR: Only HTTP and HTTPS are supported",
                __FUNCTION__);
            ODS(szMsgBuf)
        }
#endif
        enumResponseCode    = RESPONSE_CODE__UNSUPPORTED_INTERNET_PROTOCOL_SCHEME;
    }

    // Initialize the HttpOpenRequest bit flags
    //
    DWORD   dwHttpOpenRequestBitFlags   =
        INTERNET_FLAG_RELOAD            //  0x80000000  // retrieve the original item
        |
        INTERNET_FLAG_NO_CACHE_WRITE    //  0x04000000  // don't write this item to the cache
        |
        INTERNET_FLAG_KEEP_CONNECTION   //  0x00400000  // use keep-alive semantics
        |
        INTERNET_FLAG_PRAGMA_NOCACHE    //  0x00000100  // asking wininet to add "pragma: no-cache"
        ;

    // Set the server port number
    //
    if (INTERNET_SCHEME_HTTPS == url_comp.nScheme)
    {
        dwHttpOpenRequestBitFlags   |= (
            INTERNET_FLAG_SECURE                        //  0x00800000  // use PCT/SSL if applicable (HTTP)
            |
            INTERNET_FLAG_IGNORE_CERT_CN_INVALID        //  0x00001000  // bad common name in X509 Cert.
            |
            INTERNET_FLAG_IGNORE_CERT_DATE_INVALID);    //  0x00002000  // expired X509 Cert.
    }

    HINTERNET   hSession;
    HINTERNET   hConnection = NULL;
    HINTERNET   hRequest    = NULL;
    //
#define MAX_HEADER_SIZE     8192
    char *  pRequestHdrBuf  = new char [MAX_HEADER_SIZE];
    DWORD   dwBufLen        = MAX_HEADER_SIZE;
    //
    DWORD   HTTP_StatusCode     = 0;
    DWORD   dwSizeOfStatusCode  = sizeof (HTTP_StatusCode);
    //
    DWORD   dwSizeOf_ContentLen = sizeof (m.dwContentLen);

    // Initialize this apps use of the WinINet functions
#if defined(_DEBUG)
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call InternetOpen",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (NULL == (hSession = InternetOpen (
        "DisneyOnlineGames",
        INTERNET_OPEN_TYPE_PRECONFIG,
        NULL,
        NULL,
        0)))
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: InternetOpen",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_OPEN_SESSION;
    }
    // Open an HTTP session for the specified site
    else
#if defined(_DEBUG)
    {
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - url_comp.lpszHostName=[%s]",__FUNCTION__,url_comp.lpszHostName);ODS(szMsgBuf)}
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - url_comp.nPort=[%d]",__FUNCTION__,url_comp.nPort);ODS(szMsgBuf)}
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - urlstrbuf=[%s]",__FUNCTION__,urlstrbuf);ODS(szMsgBuf)}
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call InternetConnect",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (NULL == (hConnection = InternetConnect (
        hSession,
        url_comp.lpszHostName,
        url_comp.nPort,
        NULL,
        NULL,
        INTERNET_SERVICE_HTTP,
        INTERNET_FLAG_NO_CACHE_WRITE,
        0)))
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: InternetConnect",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_CONNECT;
    }
    // Open an HTTP request handle
    else
#if defined(_DEBUG)
    {
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call HttpOpenRequest",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (NULL == (hRequest = HttpOpenRequest (
        hConnection,
        "GET",
        url_comp.lpszUrlPath,
        "HTTP/1.1",
        NULL,
        (LPCTSTR *)g_paszAcceptTypes,
        dwHttpOpenRequestBitFlags,
        0)))
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: HttpOpenRequest",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_OPEN_REQUEST;
    }
    else
#if defined(_DEBUG)
    {
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call HttpQueryInfo",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (!HttpQueryInfo (
        hRequest,
        HTTP_QUERY_RAW_HEADERS_CRLF | HTTP_QUERY_FLAG_REQUEST_HEADERS,
        (LPVOID)pRequestHdrBuf,
        &dwBufLen,
        0))
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: HttpQueryInfo",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_OBTAIN_HEADERS_RETURNED_BY_SERVER;
    }
    else
#if defined(_DEBUG)
    {
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call HttpSendRequest",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (!HttpSendRequest (
        hRequest,
        NULL,       // No extra headers
        0,          // No extra Header length
        NULL,       // Not sending a POST
        0))         // Not sending a POST
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: HttpQueryInfo",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__HTTP_SERVER_REQUEST_FAILURE;
    }
    else
#if defined(_DEBUG)
    {
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call HttpQueryInfo",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (!HttpQueryInfo (
        hRequest,
        HTTP_QUERY_STATUS_CODE | HTTP_QUERY_FLAG_NUMBER,    // HTTP_QUERY_FLAG_NUMBER tells it to return a dword, not a string
        (LPVOID)&HTTP_StatusCode,
        &dwSizeOfStatusCode,
        NULL))
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: HttpQueryInfo",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_OBTAIN_STATUS_CODE;
    }
    else if (HTTP_STATUS_OK != HTTP_StatusCode)
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: HttpQueryInfo",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__HTTP_STATUS_ERROR;
    }
    else
#if defined(_DEBUG)
    {
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s"
        " - about to call HttpQueryInfo",__FUNCTION__);ODS(szMsgBuf)}
#endif
    if (!HttpQueryInfo (
        hRequest,
        HTTP_QUERY_CONTENT_LENGTH | HTTP_QUERY_FLAG_NUMBER,
        (LPVOID)&(m.dwContentLen),
        &dwSizeOf_ContentLen,
        NULL))
    {
#if defined(_DEBUG)
        {DWORD   dwLastError;dwLastError = GetLastError ();char    szMsgBuf    [1024];wsprintf (szMsgBuf,"%s\t"
            "%s: %u=%s",__FUNCTION__,"ERROR: HttpQueryInfo",dwLastError,get_http_specific_error_description (dwLastError));ODS(szMsgBuf)}
#endif
        enumResponseCode    = RESPONSE_CODE__CANNOT_OBTAIN_CONTENT_LENGTH;
    }
    else
    {
        // While response data is available is being successfully read
        //
        static  const int NUM_HTTP_RESPONSE_DATA_BUFFER_BYTES = 8192;
        char    szHttpResponseData  [NUM_HTTP_RESPONSE_DATA_BUFFER_BYTES];
        DWORD   dwNumBytesResponseDataRead      = 0;
        ENUM_RESPONSE_CODE  enumResponseCode;
        while (
            (m.dwNumBytesResponseDataReadTotal < m.dwContentLen)
            &&
            (RESPONSE_CODE__SUCCESS == (enumResponseCode = response_data_available_and_successfully_read (
                hRequest,
                szHttpResponseData,
                NUM_HTTP_RESPONSE_DATA_BUFFER_BYTES,
                &dwNumBytesResponseDataRead)))
              )
        {
            // Update the total number of response data bytes read
            m.dwNumBytesResponseDataReadTotal   += dwNumBytesResponseDataRead;
            // If the destination file write fails
            DWORD   dwNumberOfBytesWritten;
            if (!WriteFile (
                hFile,
                szHttpResponseData,
                dwNumBytesResponseDataRead,
                &dwNumberOfBytesWritten,
                NULL))
            {
                enumResponseCode    = RESPONSE_CODE__FILE_WRITE_FAILURE;
                break;
            }
            if (dwNumBytesResponseDataRead != dwNumberOfBytesWritten)
            {
                enumResponseCode    = RESPONSE_CODE__UNEXPECTED_NUMBER_OF_BYTES_WRITTEN_TO_FILE;
                break;
            }
        }
    }
#if defined(_DEBUG)
    }
    }
    }
    }
    }
    }
#endif

    // Close the handle opened by the call to function HttpOpenRequest
    //
    if (hRequest)
    {
        InternetCloseHandle (hRequest);
    }

    // Close the handle opened by the call to function InternetConnect
    //
    if (hConnection)
    {
        InternetCloseHandle (hConnection);
    }

    // Close the Internet handle opened by the call to function InternetOpen
    //
    if (hSession)
    {
        InternetCloseHandle (hSession);
    }

#if defined(_DEBUG)
    { char    szMsgBuf    [1024];wsprintf (szMsgBuf,"LEAVE: "
        "%s",__FUNCTION__);ODS(szMsgBuf)}
#endif
    return  enumResponseCode;
}

ENUM_RESPONSE_CODE  CRunPiratesOnline::download_and_run_installer  (const char *    pszInstallerURL)
{
    // If the request to obtain the path to temporary directory failed
    char    szTempPath  [MAX_PATH];
    if (0 == GetTempPath (MAX_PATH, szTempPath))
    {
        return  RESPONSE_CODE__UNABLE_TO_OBTAIN_TEMP_PATHNAME;
    }
    // If the request to obtain a unique temporary filename failed
    char    szInstallerFullPathname  [MAX_PATH];
    if (0 == GetTempFileName (szTempPath, NULL, 0, szInstallerFullPathname))
    {
        return  RESPONSE_CODE__UNABLE_TO_OBTAIN_TEMP_FILENAME;
    }
    // If the temporary file was not successfully opened for writing
    HANDLE  hFile;
    if (INVALID_HANDLE_VALUE == (hFile = CreateFile (
        szInstallerFullPathname,
        GENERIC_WRITE,
        0,
        NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        NULL
       )))
    {
        return  RESPONSE_CODE__UNABLE_TO_CREATE_DESTINATION_FILENAME;
    }
    //
    ENUM_RESPONSE_CODE  enumResponseCode;
    enumResponseCode    = download_installer (hFile);
    //
    if (!CloseHandle (hFile))
    {
        enumResponseCode    = RESPONSE_CODE__CANNOT_CLOSE_DESTINATION_FILE;
    }
    //
    if (RESPONSE_CODE__SUCCESS != enumResponseCode)
    {
        DeleteFile (szInstallerFullPathname);
	    return  enumResponseCode;
    }
    // Register file szInstallerFullPathname to be deleted when the system restarts
    // NOTES:
    //  1) The system moves the file immediately after AUTOCHK is executed, but before creating any
    //      paging files.
    //  2) Parameter value MOVEFILE_DELAY_UNTIL_REBOOT can be used only if the process is in the
    //      context of a user who belongs to the administrator group or the LocalSystem account.
    MoveFileEx (szInstallerFullPathname, NULL, MOVEFILE_DELAY_UNTIL_REBOOT);
    // Set command line
    CString strCommandLine (szInstallerFullPathname);
    strCommandLine.Append (" ");
    strCommandLine.Append (szInstallerCommandLineOptionPrefix);
    strCommandLine.Append (szInstallerSilentRunModeOption);
    strCommandLine.Append (" ");
    strCommandLine.Append (szInstallerCommandLineOptionPrefix);
    strCommandLine.Append (szEnvKeyToAddToChildProcessEnvBlock);
    strCommandLine.Append (" ");
    strCommandLine.Append (m.pszToken);
    // Attempt to run the installer executable
    return  create_process (strCommandLine);
}

ENUM_RESPONSE_CODE  CRunPiratesOnline::create_process  (CString &   strCommandLine)
{
    // Create security attributes
    SECURITY_DESCRIPTOR     sd;
    InitializeSecurityDescriptor (&sd, SECURITY_DESCRIPTOR_REVISION);
    SetSecurityDescriptorDacl (&sd, TRUE, 0, FALSE);
    SECURITY_ATTRIBUTES     sa  = { sizeof(SECURITY_ATTRIBUTES), &sd, true };
    // Create child process environment block
    CString     strEnvForChildProcess;
    CEnvBlock   EnvBlock (m.pszToken);
    EnvBlock.Create (szEnvKeyToAddToChildProcessEnvBlock, strEnvForChildProcess);
    // Set startup information
    STARTUPINFO si;
    memset (&si, 0, sizeof (si));
    si.cb           = sizeof (si);
    si.dwFlags      = STARTF_USESHOWWINDOW;
    si.wShowWindow  = SW_SHOWNORMAL;
    // Initialize process information structure
    PROCESS_INFORMATION     pi;
    ZeroMemory (&pi, sizeof (pi));
    // Attempt to run the executable
    if (!CreateProcess (
        NULL,
        strCommandLine.GetBuffer (),
        &sa,
        &sa,
        true,
        0,
        strEnvForChildProcess.GetBuffer (),
        NULL,
        &si,
        &pi))
    {
        return  RESPONSE_CODE__CREATE_PROCESS_FAILED;
    }
    return  RESPONSE_CODE__SUCCESS;
}

bool    CRunPiratesOnline::map_folder_to_csidl (const char *    pszCSIDL,
                                                int *           pcsidl)
{
    bool    fRet    = true;
    //
    *pcsidl = 0;
    if (0 == _strcmpi (pszCSIDL /* .GetBuffer () */ , "ADMINTOOLS"))
    {
        // The file system directory that is used to store administrative tools for an individual user.
        //  The Microsoft Management Console (MMC) will save customized consoles to this directory, and
        //      it will roam with the user.
        *pcsidl |= CSIDL_ADMINTOOLS;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "COMMON_ADMINTOOLS"))
    {
        // The file system directory containing administrative tools for all users of the computer.
        *pcsidl |= CSIDL_COMMON_ADMINTOOLS;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "APPDATA"))
    {
        // The file system directory that serves as a common repository for application-specific data.
        //  A typical path is C:\Documents and Settings\username\Application Data.
        //  This CSIDL is supported by the redistributable Shfolder.dll for systems that do not have
        //      the Microsoft Internet Explorer 4.0 integrated Shell installed.
        *pcsidl |= CSIDL_APPDATA;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "COMMON_APPDATA"))
    {
        // The file system directory containing application data for all users.
        //  A typical path is C:\Documents and Settings\All Users\Application Data.
        *pcsidl |= CSIDL_COMMON_APPDATA;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "COMMON_DOCUMENTS"))
    {
        // The file system directory that contains documents that are common to all users.
        //  A typical paths is C:\Documents and Settings\All Users\Documents.
        //  Valid for Windows NT systems and Microsoft Windows 95 and Windows 98 systems with
        //      Shfolder.dll installed.
        *pcsidl |= CSIDL_COMMON_DOCUMENTS;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "COOKIES"))
    {
        // The file system directory that serves as a common repository for Internet cookies.
        //  A typical path is C:\Documents and Settings\username\Cookies.
        *pcsidl |= CSIDL_COOKIES;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "HISTORY"))
    {
        // The file system directory that serves as a common repository for Internet history items.
        *pcsidl |= CSIDL_HISTORY;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "INTERNET_CACHE"))
    {
        // The file system directory that serves as a common repository for temporary Internet files.
        //  A typical path is C:\Documents and Settings\username\Local Settings\Temporary Internet Files.
        *pcsidl |= CSIDL_INTERNET_CACHE;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "LOCAL_APPDATA"))
    {
        // The file system directory that serves as a data repository for local (nonroaming) applications.
        //  A typical path is C:\Documents and Settings\username\Local Settings\Application Data.
        *pcsidl |= CSIDL_LOCAL_APPDATA;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "MYPICTURES"))
    {
        // The file system directory that serves as a common repository for image files.
        //  A typical path is C:\Documents and Settings\username\My Documents\My Pictures.
        *pcsidl |= CSIDL_MYPICTURES;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "PERSONAL"))
    {
        // The virtual folder representing the My Documents desktop item.
        //  This is equivalent to CSIDL_MYDOCUMENTS.
        *pcsidl |= CSIDL_PERSONAL;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "PROGRAM_FILES"))
    {
        // The Program Files folder.
        //  A typical path is C:\Program Files.
        *pcsidl |= CSIDL_PROGRAM_FILES;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "PROGRAM_FILES_COMMON"))
    {
        // A folder for components that are shared across applications.
        //  A typical path is C:\Program Files\Common.
        //  Valid only for Windows NT, Windows 2000, and Windows XP systems.
        //  Not valid for Windows Millennium Edition (Windows Me).
        *pcsidl |= CSIDL_PROGRAM_FILES_COMMON;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "SYSTEM"))
    {
        // The Windows System folder.
        //  A typical path is C:\Windows\System32.
        *pcsidl |= CSIDL_SYSTEM;
    }
    else
    if (0 == _strcmpi (pszCSIDL, "WINDOWS"))
    {
        // The Windows directory or SYSROOT.
        //  This corresponds to the %windir% or %SYSTEMROOT% environment variables.
        //  A typical path is C:\Windows.
        *pcsidl |= CSIDL_WINDOWS;
    }
    else
    {
        fRet    = false;
    }
    return  fRet;
}

ENUM_RESPONSE_CODE  CRunPiratesOnline::run_launcher    (const char *    pszLauncherCSIDL,
                                                        const char *    pszLauncherPathname)
{
    // Given a CSIDL as a string, if the corresponding pathname cannot be obtained
    int csidl   = 0;
    if (!map_folder_to_csidl (pszLauncherCSIDL, &csidl))
    {
        return  RESPONSE_CODE__UNRECOGNIZED_DESTINATION_FOLDER;
    }
    // Given a CSIDL of a folder, if a path was NOT returned
    char    szPathFromCSIDL   [MAX_PATH];
    if (!(SUCCEEDED(SHGetFolderPath (
        NULL,               // handle to an owner window
        csidl,              // CSIDL value that identifies the folder whose path is to be retrieved
        NULL,               // access token that can be used to represent a particular user
        SHGFP_TYPE_CURRENT, // flags to specify which path is to be returned
        szPathFromCSIDL     // pointer to a null-terminated string of length MAX_PATH which will receive the path
        ))))
    {
        return  RESPONSE_CODE__CANNOT_OBTAIN_SPECIAL_ROOT_FOLDER_PATHNAME;
    }
    // Obtain string lengths
    size_t  stPath_Len              = strlen (szPathFromCSIDL);
    size_t  stLancherPathname_Len   = strlen (pszLauncherPathname);
    // If launcher executable full pathname will be too long
    if (MAX_PATH <= (stPath_Len + stLancherPathname_Len))
    {
        return  RESPONSE_CODE__LAUNCHER_FULL_PATHNAME_TOO_LONG;
    }
    // Set launcher executable full pathname
    char    szLauncherFullPathname  [MAX_PATH];
    strcpy (szLauncherFullPathname, szPathFromCSIDL);
    strcat (szLauncherFullPathname, pszLauncherPathname);
    // Set command line
    CString strCommandLine (szLauncherFullPathname);
    strCommandLine.Append (" ");
    strCommandLine.Append (szEnvKeyToAddToChildProcessEnvBlock);
    strCommandLine.Append ("=");
    strCommandLine.Append (m.pszToken);
    // Return indication of whether or not the launcher process was successfully created
    return  create_process (strCommandLine);
}

ENUM_RESPONSE_CODE  CRunPiratesOnline::validate_inputs (const int   ModeId)
{
    ENUM_RESPONSE_CODE  enumResponseCode    = RESPONSE_CODE__INVALID_MODE;
    for (m.immogFlavorIdx = 0; m.immogFlavorIdx < (sizeof (gsc_mmogFlavor) / sizeof (MMOG_FLAVOR)); m.immogFlavorIdx++)
    {
        if (gsc_mmogFlavor[m.immogFlavorIdx].mode == ModeId)
        {
            enumResponseCode    = RESPONSE_CODE__SUCCESS;
            break;
        }
    }
    return  enumResponseCode;
}

ULONG   CRunPiratesOnline::Run (const int       ModeId,
                                const char *    pszToken)
{
    m.pszToken  = pszToken;
    ENUM_RESPONSE_CODE  ResponseCode;
    if (RESPONSE_CODE__SUCCESS == (ResponseCode = validate_inputs (ModeId)))
    {
        if (RESPONSE_CODE__SUCCESS != (ResponseCode = run_launcher (
            gsc_mmogFlavor[m.immogFlavorIdx].pszLauncherCSIDL,
            gsc_mmogFlavor[m.immogFlavorIdx].pszLauncherPathname)))
        {
            ResponseCode    = download_and_run_installer (
                gsc_mmogFlavor[m.immogFlavorIdx].pszInstallerURL);
        }
    }
    return  ResponseCode;
}

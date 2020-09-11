#pragma once

enum ENUM_RESPONSE_CODE
{
    RESPONSE_CODE__SUCCESS                                      = 0,
        // Success
    RESPONSE_CODE__INVALID_MODE                                 = 1,
        // Mode input is invalid
    RESPONSE_CODE__UNRECOGNIZED_DESTINATION_FOLDER              = 2,
        // Unrecognized Destination Folder argument
        // Please reference [Valid Destination Folder Parameter Values] below
    RESPONSE_CODE__CANNOT_OBTAIN_SPECIAL_ROOT_FOLDER_PATHNAME   = 3,
        // Cannot obtain special root folder pathname
    RESPONSE_CODE__LAUNCHER_FULL_PATHNAME_TOO_LONG              = 4,
        // Full pathname to launcher executable is too long
    RESPONSE_CODE__BAD_PATHNAME                                 = 5,
        // Possible issue: Relative paths are not allowed
    RESPONSE_CODE__FILENAME_EXCED_RANGE                         = 6,
        // Destination Folder + Destination Sub-folder + Destination Filename > 256 characters
    RESPONSE_CODE__PATH_NOT_FOUND                               = 7,
        // The system cannot find the path
        // Possible issue: The path contains an invalid entry
    RESPONSE_CODE__CANCELLED                                    = 8,
        // The user canceled the operation
    RESPONSE_CODE__SHCDEX_UNRECOGNIZED_RET_CODE                 = 9,
        // Call to create Destination Folder failed with an unrecognized reason code
    RESPONSE_CODE__DESTINATION_FILENAME_TOO_LONG                = 10,
        // Destination filename too long
    RESPONSE_CODE__DESTINATION_FILENAME_IS_A_DIRECTORY          = 11,
        // A directory exists with the same full pathname as the requested destination
    RESPONSE_CODE__UNABLE_TO_CREATE_DESTINATION_FILENAME        = 12,
        // Unable to create destination file on user's HDD
    RESPONSE_CODE__CANNOT_CRACK_SOURCE_URL                      = 13,
        // Cannot crack source URL
    RESPONSE_CODE__UNSUPPORTED_INTERNET_PROTOCOL_SCHEME         = 14,
        // Internet protocol scheme not supported
        // Supported Internet protocol schemes: HTTP, HTTPS
    RESPONSE_CODE__CANNOT_OBTAIN_CONTENT_LENGTH                 = 15,
        // Cannot obtain content length from server
    RESPONSE_CODE__CANNOT_OPEN_SESSION                          = 16,
        // Call to open protocol session failed
    RESPONSE_CODE__CANNOT_CONNECT                               = 17,
        // Attempt to connect to server failed
    RESPONSE_CODE__CANNOT_OPEN_REQUEST                          = 18,
        // Protocol request handle creation failure
    RESPONSE_CODE__CANNOT_OBTAIN_HEADERS_RETURNED_BY_SERVER     = 19,
        // Unable to retrieve header information associated with server request
    RESPONSE_CODE__HTTP_SERVER_REQUEST_FAILURE                  = 20,
        // Server request failure
    RESPONSE_CODE__CANNOT_OBTAIN_STATUS_CODE                    = 21,
        // Server request could not complete
    RESPONSE_CODE__HTTP_STATUS_ERROR                            = 22,
        // Status code returned from server indicates error
    RESPONSE_CODE__CANNOT_QUERY_SERVER                          = 23,
        // Cannot query server
        // Failure occurred when querying server to determine data size
    RESPONSE_CODE__INTERNET_READ_FAILURE                        = 24,
        // Call to read data from server failed
    RESPONSE_CODE__INVALID_NUMBER_OF_BYTES_READ                 = 25,
        // The number of bytes requested to be read is not equal to the number of bytes read from
        //  the server
    RESPONSE_CODE__FILE_WRITE_FAILURE                           = 26,
        // HDD write failure
        // User’s hard drive may be out of space
    RESPONSE_CODE__UNEXPECTED_NUMBER_OF_BYTES_WRITTEN_TO_FILE   = 27,
        // Number of bytes written to HDD does not match the number of bytes requested to be written
    RESPONSE_CODE__CANNOT_CLOSE_DESTINATION_FILE                = 28,
        // Call to close the Destination Filename failed
    RESPONSE_CODE__CREATE_PROCESS_FAILED                        = 29,
        // Unable to run downloaded executable
    //
    //
    RESPONSE_CODE__UNABLE_TO_OBTAIN_TEMP_PATHNAME               = 51,
    RESPONSE_CODE__UNABLE_TO_OBTAIN_TEMP_FILENAME               = 52,
    //
    //
    RESPONSE_CODE__FAILURE                                      = 99,
        // Non-specific failure
};

class CRunPiratesOnline
{
public:
    CRunPiratesOnline  (void)
    {
        memset (&m, 0, sizeof (m));
    }
    ~CRunPiratesOnline (void)
    {
    }
    ULONG   Run        (const int       ModeId,
                        const char *    pszToken);
private:
    struct
    {
        const char *    pszToken;
        int             immogFlavorIdx;
        DWORD           dwContentLen;
        DWORD           dwNumBytesResponseDataReadTotal;
    } m;
private:
#if defined(_DEBUG)
    PSZ                 get_http_specific_error_description            (DWORD           dwError);
#endif
    //
    ENUM_RESPONSE_CODE  response_data_available_and_successfully_read  (HINTERNET       hRequest,
                                                                        char *          pszHttpResponseData,
                                                                        DWORD           dwNumHttpResponseDataBufferBytes,
                                                                        DWORD *         pdwNumBytesResponseDataRead);
    //
    ENUM_RESPONSE_CODE  download_installer                             (HANDLE          hFile);
    //
    ENUM_RESPONSE_CODE  download_and_run_installer                     (const char *    pszInstallerURL);
    //
    void                insert_env_block_key_value_pair                (CString &       strEnvForChildProcess,
                                                                        int *           pInsertIdx,
                                                                        char *          lpszVariable);
    //
    void                create_child_process_environment_block         (CString &       strEnvForChildProcess);
    //
    ENUM_RESPONSE_CODE  create_process                                 (CString &       strCommandLine);
    //
    ENUM_RESPONSE_CODE  validate_inputs                                (const int       ModeId);
    //
    ENUM_RESPONSE_CODE  run_launcher                                   (const char *    pszLauncherCSIDL,
                                                                        const char *    pszLauncherPathname);
    //
    bool                map_folder_to_csidl                            (const char *    pszCSIDL,
                                                                        int *           pcsidl);
};

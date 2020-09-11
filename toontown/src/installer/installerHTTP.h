#ifndef _INSTALLER_HTTP_H_
#define _INSTALLER_HTTP_H_

// currently installerBase downloadToMem() doesnt use this library
#if 0
// Error codes
#define E_HTTP_SUCCESS                                  0
#define E_HTTP_ERROR_BASE                               -10000
#define E_HTTP_FAIL                                             (E_HTTP_ERROR_BASE)
#define E_HTTP_URL_FORMAT_ERROR                 (E_HTTP_ERROR_BASE-1)
#define E_HTTP_CONNECTION_FAILED                (E_HTTP_ERROR_BASE-2)
#define E_HTTP_INVALID_ADDRESS                  (E_HTTP_ERROR_BASE-3)
#define E_HTTP_NO_CONTENT_LENGTH                (E_HTTP_ERROR_BASE-4)

int http_download_to_buffer(const char *url,
                                                        char *proxy_host, int proxy_port,
                                                        char **returned_buffer, unsigned long *buffer_length);
#endif

#endif
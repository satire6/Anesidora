#include "pragma.h"

#if 0
#include <windows.h>
#include <io.h>
#include <winsock.h>
#include "installerHTTP.h"

#define MAX_BUFFER_LEN  (8196)
#define MAX_URL_LEN             (2048*2)

// Misc HTTP functions
static int http_open_connection(char *rhost, int rport, SOCKET *sd);
static int http_get_response_header(SOCKET sd, unsigned int *contentLength);
static int http_crack_url(const char *url, char *rhost, int *rport, char *uri);

// Misc Network functions
static int net_readline(SOCKET s, char **returned_line);
static int net_read(SOCKET s, char *buffer, int len);
static int net_readn(SOCKET s, char *buffer, int len);

// Misc General functions
static char *matchi(char *haystack, char *needle);
static char *skip_spaces(char *in);

//////////////////////////////////////////////////
// Testing...
//////////////////////////////////////////////////
#ifdef _HTTP_TEST_
#include <stdio.h>

struct _testData
{
        char *url;
        char *proxyHost;
        int proxyPort;
};

int main(int argc, char *argv[])
{
        struct _testData data[] =
        {
//              { "http://www.apache.org/", NULL, 0 },
//              { "http://www.disney.com/", NULL, 0 },
                { "http://www.yahoo.com/", NULL, 0 }
        };

        for (int i=0; i<sizeof(data)/sizeof(data[0]); i++)
        {
                printf("===========================\n[URL=%s] ", data[i].url);
                if (data[i].proxyHost)
                        printf(" via proxy %s:%d", data[i].proxyHost, data[i].proxyPort);
                printf("\n");

                char *buf=NULL;
                unsigned long bufLen;
                if (http_download_to_buffer(data[i].url, data[i].proxyHost, data[i].proxyPort, &buf, &bufLen) >= 0)
                {
                        printf("Success. Buffer len=%d, Buffer=%s\n", bufLen, buf ? buf : "<n/a>");
                        delete [] buf;
                }
                else
                {
                        printf("Error\n");
                }
        }
        return 0;
}
#endif

//////////////////////////////////////////////////
// Main Function
//////////////////////////////////////////////////

int http_download_to_buffer(const char *url,
                                                        char *proxy_host, int proxy_port,
                                                        char **returned_buffer, unsigned long *buffer_length)
{
        SOCKET sd = INVALID_SOCKET;
        WSADATA wsaData;
        char full_url[MAX_URL_LEN];
        char host[MAX_PATH];
        int port;
        char uri[MAX_PATH];
        char *rhost = NULL;
        int rport = 80;
        int error = 0;
        unsigned int contentLength = 0;
        unsigned int len = 0;

        // Initialize
        *returned_buffer = 0;
        *buffer_length = 0;
        WSAStartup(0x0101, (LPWSADATA)&wsaData);

        if (http_crack_url(url, host, &port, uri) < 0)
        {
                // URL format error
                error = E_HTTP_URL_FORMAT_ERROR;
                goto cleanup;
        }

        // Connect to server

        // Handle case for proxy servers
        if (proxy_host && proxy_host[0] != '\0')
        {
                rhost = proxy_host;
                rport = proxy_port;
                wsprintf(full_url, "http://%s:%d%s", host, port, uri);
        }
        else
        {
                rhost = host;
        }

        if (http_open_connection(rhost, rport, &sd) < 0)
        {
                // Error connecting to server
                error = E_HTTP_CONNECTION_FAILED;
                goto cleanup;
        }

        // Send Request
        char buf[MAX_BUFFER_LEN];
        wsprintf(buf,   "GET %s HTTP/1.1\r\n"
                                        "Host: %s\r\n"
                                        "Accept: */*\r\n"
                                        "User-Agent: Mozilla/4.0 WinNT\r\n\r\n",
                                proxy_host ? full_url : uri, rhost);
#ifdef _HTTP_TEST_
        printf("Request header...\n%s", buf);
#endif

        if (send(sd, buf, strlen(buf), 0) == SOCKET_ERROR)
        {
                error = -WSAGetLastError();
                goto cleanup;
        }

        // Get Response
        if ((error = http_get_response_header(sd, &contentLength)) < 0)
        {
                goto cleanup;
        }

        if (contentLength > 0)
        {
                *returned_buffer = new char[contentLength+1];
                *buffer_length = contentLength;
                len = net_readn(sd, *returned_buffer, contentLength);
                if (len != contentLength)
                {
                        error = -WSAGetLastError();
                        delete [] *returned_buffer;
                }
        }
        else
        {
                // TODO: Add support for CGI-type responses where Content-Length is not present
                unsigned int buffer_inc_amt = 8196;
                unsigned int buffer_len = buffer_inc_amt;
                unsigned int write_head = 0;
                char *buffer = new char[buffer_len+1];

                while (1)
                {
                        // read some bytes
                        len = net_read(sd, &buffer[write_head], buffer_len - write_head);
                        if (len <= 0)
                                break;

                        // If we fill the buffer, enlarge it
                        if (len == buffer_len - write_head)
                        {
                                unsigned int old_buffer_len = buffer_len;

                                buffer_len += buffer_inc_amt;
                                char *buf = new char[buffer_len+1];
                                memcpy(buf, buffer, old_buffer_len);
                                delete [] buffer;
                                buffer = buf;
                        }

                        // Advance the write head
                        write_head += len;
                }

                // Return with correctly sized buffer
                if (write_head > 0)
                {
                        *returned_buffer = new char[write_head+1];
                        *buffer_length = write_head;
                        memcpy(*returned_buffer, buffer, write_head);
                        delete [] buffer;
                }
        }

        // Cleanup and return
cleanup:
        if (*buffer_length > 0)
                (*returned_buffer)[*buffer_length] = 0;
        if (sd != INVALID_SOCKET)
                closesocket(sd);
        WSACleanup();
        return error;
}


////////////////////////////////////////////////////////
// Static functions
////////////////////////////////////////////////////////

static int http_open_connection(char *rhost, int rport, SOCKET *sd)
{
        struct sockaddr_in addr;
        struct in_addr server_addr;
        struct hostent *remote;
        int error = 0;

        if ((*sd = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET)
        {
                return -WSAGetLastError();
        }
        if (isdigit(rhost[0]))
        {
                unsigned long addr;

                if ((addr = inet_addr(rhost)) != INADDR_NONE)
                        memcpy(&server_addr, &addr, sizeof(server_addr));
                else
                        error = E_HTTP_INVALID_ADDRESS;
        }
        else
        {
                remote = gethostbyname(rhost);
                if (remote == NULL)
                        error = -WSAGetLastError();
                else
                {
                        if (remote->h_addr_list[0] == NULL)
                                error = -WSAGetLastError();
                        else
                        {
                                memcpy(&server_addr, *remote->h_addr_list, sizeof(server_addr));
                        }
                }
        }
        if (error == 0)
        {
                addr.sin_family = AF_INET;
                addr.sin_port = htons((u_short)rport);
                addr.sin_addr.s_addr = server_addr.s_addr;
                if (connect(*sd, (struct sockaddr*)&addr, sizeof(addr)) < 0)
                        error = -WSAGetLastError();
        }
        return error;
}

static int http_get_response_header(SOCKET sd, unsigned int *contentLength)
{
        int error = 0;

#ifdef _HTTP_TEST_
        printf("Response header..\n");
#endif
        for (;;)
        {
                char *line = NULL;
                int num;
                char *ptr = NULL;

                num = net_readline(sd, &line);

                if (num < 0)
                {
                        error = num;
                        break;
                }
                if (line == NULL || strlen(line) == 0)
                        break;
                else
                {
                        if ((ptr = matchi(line,"content-length:")) != NULL)
                        {
                                ptr = skip_spaces(ptr);
                                *contentLength = atoi(ptr);
                        }
                }
#ifdef _HTTP_TEST_
                printf("%s\n", line);
#endif
                //OutputDebugString(line);
                //OutputDebugString("\n");
                if (line) free(line);
        }
#ifdef _HTTP_TEST_
        printf("\n");
#endif
        return error;
}

static int http_crack_url(const char *url, char *rhost, int *rport, char *uri)
{
        char *ptr;
        char pbuf[8196];
        char *ppbuf = pbuf;
        int i = 0;
        char *puri = uri;

        if ((ptr = (char*)url) == 0)
                return E_HTTP_FAIL;

        if (!strncmp(ptr, "http://", 7) || !strncmp(ptr, "HTTP://", 7))
        {
                ptr += 7;
                while (*ptr && *ptr != '/' && *ptr != ':')
                        *rhost++ = *ptr++;
                *rhost = 0;
                if (*ptr == ':')
                {
                        ptr++;
                        while (*ptr && *ptr != '/')
                                *ppbuf++ = *ptr++;
                        *ppbuf = 0;
                        *rport = atoi(pbuf);
                }
                else
                        *rport = 80;

                while (*ptr && *ptr != ' ')
                        *uri++ = *ptr++;
                *uri = 0;
        }
        else
        {
                rhost[0] = 0;
                *rport = 80;
        }

        if (puri[0] == 0)
        {
                puri[0] = '/';
                puri[1] = 0;
        }

        return E_HTTP_SUCCESS;
}

static int net_readline(SOCKET s, char **returned_line)
{
        int linesize = 0;
        int count = 0;
        char lastch = '\0';
        int allocation_sizes[] = { 2048, 8196 };
        int i;
        char *line = NULL;        // this MUST be NULL so that realloc will work the first time
        char *ptr = NULL;

        *returned_line = 0;

        for (i = 0; i < sizeof(allocation_sizes)/sizeof(allocation_sizes[0]); i++)
        {
                linesize = allocation_sizes[i];
                if ((ptr = (char*)realloc(line, linesize)) != NULL)
                        line = ptr;
                else
                {
                        free(line); // if the realloc failed and we already had realloced, then free
                        return -1;
                }

                while (count < linesize)
                {
                        char ch;

                        int num = recv(s, &ch, 1, 0);
                        if (num != 1)
                        {
                                // this could be error or connection close.
                                // in either case, propagate error up
                                free(line);
                                return num;
                        }

                        line[count] = ch;
                        if (ch == '\n')
                        {
                                // got complete line

                                if (count <= 1)  // got \r\n or \n at start of line
                                {
                                        free(line);
                                        return 0;
                                }
                                if (lastch == '\r')
                                        line[count-1] = 0;      // chop off the \r\n
                                else
                                        line[count] = 0; //chop off the \n

                                *returned_line = line;
                                return count;
                        }
                        lastch = ch;
                        count++;
                }
        }

        // if we got here, we've overrun the max allocation limit per line
        free(line);
        return -1;
}

static int net_read(SOCKET s, char *buffer, int len)
{
        int num;

        if ((num = recv(s, buffer, len, 0)) == SOCKET_ERROR)
        {
                return -WSAGetLastError();
        }
        return num;
}

// Either read len bytes or return with error
static int net_readn(SOCKET s, char *buffer, int len)
{
        int readlen = 0;
        int num = 0;

        while (readlen < len)
        {
                if ((num = net_read(s, buffer+readlen, len-readlen)) <= 0)   // check <= 0
                        break;
                readlen += num;
        }
        return readlen == len ? len : num;
}

static char *skip_spaces(char *in)
{
        char *out;

        out = in;

        while (*out && isspace(*out))
                out++;
        return out;
}

static char *matchi(char *haystack, char *needle)
{
        if (!needle || !haystack)
                return NULL;

        while (*needle && *haystack)
        {
                int a,b;

                a = toupper(*haystack);
                b = toupper(*needle);

                if (a != b)
                        return NULL;

                haystack++;
                needle++;
        }
        return haystack;
}

#endif

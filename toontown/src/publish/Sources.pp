
// Write the encryption key to a Python file that the Scrubber can read.
#output PRCEncryptionKey.py notouch
key = $[PRC_ENCRYPTION_KEY]
#end PRCEncryptionKey.py

#define INSTALL_SCRIPTS \
    AIcopyfiles AIprintdir AIprintfiles AIprintfiles-unix \
    AIprintfiles-unix-installed AIprintfiles-win32 AIprintlib \
    AItarfiles AIzipfiles \
    ttown-build-ai.sh ttown-run-ai.sh


# please don't publish this file!

import base64
import sys

def decode(s):
    # insert super-secret decode algorithm here
    return base64.b64decode(s)

if __name__ == '__main__':
    data = sys.stdin.readline()
    print decode(data)

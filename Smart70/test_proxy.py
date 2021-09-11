#!/bin/env python3
#
# Test proxy on smart70

from Smart70 import *


if __name__ == '__main__':
    sm70 = Smart70 ('192.168.1.17', 11110, verbose=1)

    # Run proxy
    sm70.Proxy (8080)

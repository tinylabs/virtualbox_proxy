#!/bin/env python3
#
# Test proxy on smart70

from Smart70 import *


if __name__ == '__main__':

    # Create smart70
    sm70 = Smart70 ('192.168.1.17', 11110)

    # Open connection
    sm70.Open ()

    # Get devices
    devs = sm70.GetDevices ()
    for d in devs:
        print ('Found: ' + d.Name ())
    
    hop = Device.Select (devs, 'HOPPER')
    ptr = Device.Select (devs, 'PRINTER')
    flip = Device.Select (devs, 'FLIPPER')
    print (hop.GetFirmware ())
    print (ptr.GetFirmware ())
    print (flip.GetFirmware ())
    
    # Close connection
    sm70.Close ()

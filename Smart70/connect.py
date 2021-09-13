#!/bin/env python3
#
# Test proxy on smart70

from Smart70 import *
import time

if __name__ == '__main__':

    # Create smart70
    sm70 = Smart70 ('192.168.1.17', 11110, verbose=1)

    # Open connection
    sm70.Open ()

    # Get system device
    sys = sm70.GetSystem ()
    
    # Get devices
    devs = sys.GetDevices ()
    for d in devs:
        print ('Found: ' + d.Name ())
    
    hop = Device.Select (devs, 'Hopper')
    print (hop)
    ptr = Device.Select (devs, 'Printer')
    print (ptr)
    flip = Device.Select (devs, 'Flipper')
    print (flip)
    print (hop.GetStr ('FIRMWARE'))
    print (ptr.GetStr ('FIRMWARE'))
    print (flip.GetStr ('FIRMWARE'))

    print (hop.GetStr ('STATE'))
    print (ptr.GetStr ('STATE'))
    print (flip.GetStr ('STATE'))

    #for n in range (0, 100):
    #    time.sleep (0.2)
    #    print ('HOP: ' + hop.GetStateStr ())
    #    print ('PTR: ' + ptr.GetStateStr ())
    #    print ('FLIP: ' + flip.GetStateStr ())

    # Close connection
    sm70.Close ()

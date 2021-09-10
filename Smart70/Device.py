#
# Smart70 connection manager
#
# Manages connection to device
# Also can proxy traffic to decode in transit
#
#
import socket
import struct
from Packet import *

class Device:

    NAME = {
        0x00 : 'SYSTEM',
        0x10 : 'HOPPER',
        0x40 : 'PRINTER',
        0x60 : 'FLIPPER'
    }
    ATTR = {
        'FIRMWARE' : 0x0150,
        'STATUS'   : 0x0003,
        'STATE'    : 0x0360,
        }

    def __init__ (self, dev_id, conn, state):
        self.dev_id = dev_id
        self.state = state
        self.conn = conn
        
    @staticmethod
    def Select (dlist, name):
        for d in dlist:
            if d.Name() == name:
                return d
            
    # Return 64 bit status of module
    def GetStatus (self):
        pass

    # Get module state
    # 0x04 - Module has card
    # 0x08 - Module is initializing
    # 0x10 - Running last command
    # 0x20 - Failed last command
    def GetState (self):
        pass

    def Encode (self, ptype, attr):
        pkt = Packet()
        pkt.Encode (ptype, struct.pack ('<H', self.ATTR[attr]) + struct.pack ('B', self.dev_id))
        return pkt
    
    def GetFirmware (self):
        pkt = self.Encode (Packet.GET, 'FIRMWARE')
        pkt.SendRecv (self.conn)
        return pkt.payload.decode ('ascii')
    
    def CardIn (self):
        pass

    def CardOut (self):
        pass

    def Name (self):
        return self.NAME[self.dev_id]
        
    

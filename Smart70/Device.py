#
# Smart70 connection manager
#
# Manages connection to device
# Also can proxy traffic to decode in transit
#
#
import sys
import socket
import struct
from Packet import *
#import Devices
#

class Device:

    NAME = {
        0x00 : 'System',
        0x10 : 'Hopper',
        0x40 : 'Printer',
        0x60 : 'Flipper'
    }
        
    def __init__ (self, dev_id, conn, int_id):
        self.dev_id = dev_id
        self.int_id = int_id
        self.conn = conn

        self.ATTR = {
            'FIRMWARE' : {
                'ID'  : 0x0150,
                'REQ' : Packet.GET,
                'RSP' : lambda x: x,
                'DEC' : lambda x: x.decode ('ascii')
            },
            'STATUS' : {
                'ID'  : 0x0003,
                'REQ' : Packet.GET,
                'RSP' : lambda x: struct.unpack ('<Q', x[0:8])[0],
                'DEC' : self.StatusStr
            },
            'STATE' : {
                'ID'  : 0x0360,
                'REQ' : Packet.GET,
                'RSP' : lambda x: x[1],
                'DEC' : self.StateStr
            }
        }

    @staticmethod
    def Create (dev_id, conn, int_id):
        if dev_id in Device.NAME.keys():
            cls =  getattr (sys.modules[__name__], Device.NAME[dev_id])
            return cls (dev_id, conn, int_id)
        else:
            return None
        
    def Name (self):
        return self.NAME[self.dev_id]
        
    def __str__ (self):
        return self.Name () + '[' + hex (self.int_id) + ']'

    def Encode (self, ptype, attr):
        pkt = Packet()
        pkt.Encode (ptype, struct.pack ('<H', attr) + struct.pack ('B', self.dev_id))
        return pkt


    def Get (self, attr):
        # Create packet
        pkt = self.Encode (self.ATTR[attr]['REQ'], self.ATTR[attr]['ID'])

        # Send and receive response
        pkt.SendRecv (self.conn)

        # Parse payload
        return self.ATTR[attr]['RSP'] (pkt.payload)

    def GetStr (self, attr):
        val = self.Get (attr)
        return self.ATTR[attr]['DEC'] (val)
                           
    # Get module state
    # 0x04 - Module has card
    # 0x08 - Module is initializing
    # 0x10 - Running last command
    # 0x20 - Failed last command
    def StateStr (self, val):
        ret = ''
        if val & 0x04:
            ret += 'CARD|'
        elif val & 0x08:
            ret += 'INIT|'
        elif val & 0x10:
            ret += 'RUNNING|'
        elif val & 0x20:
            ret += 'FAILED|'
        return '[' + ret[:-1] + ']'

    # Shall be overridden by derived class
    def StatusStr (self, val):
        return hex (val)
    
    # Decode Packet for proxy
    def DecodeStr (self, pkt):

        # Handle requests
        if pkt.direction == 'REQ':
            attr = struct.unpack ('<H', pkt.payload[0:2])[0]
            name = ''
            for key,val in self.ATTR.items ():
                if val['ID'] == attr:
                    name = key
                    break

            ret = self.Name() + ' ' + name

            # Save attribute
            self.pattr = name

        # Handle responses
        elif self.pattr in self.ATTR.keys():
            val = self.ATTR[self.pattr]['RSP'] (pkt.payload)
            ret = self.pattr + ' ' + self.ATTR[self.pattr]['DEC'] (val)

        # Return string
        return ret
            

    def CardIn (self):
        pass

    def CardOut (self):
        pass

    # Select device from array by name
    @staticmethod
    def Select (dlist, name):
        for d in dlist:
            if d.Name() == name:
                return d

# Must do this here to avoid circular dependency
from Devices import *

#
# Smart70 connection manager
#
# Manages connection to device
# Also can proxy traffic to decode in transit
#
#
import socket
import struct
import re
import string

class Packet:

    # Save these global variables to ease connections
    idx = 0
    token = 0
    
    MAGIC      = b'ISNP'
    CONNECT    = 0x03e8
    DISCONNECT = 0x03e9
    GET        = 0x0c1c
    SET        = 0x0c1d
    DIAG       = 0x0bca
    AAAA       = 0x0bb8
    BBBB       = 0x0bbc
    CCCC       = 0x0bbe
    DDDD       = 0x0bc2
    EEEE       = 0x0bc4
    FFFF       = 0x006f
    CMD = {
        CONNECT : { 'STR' : 'CONNECT',
                    'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                    'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        DISCONNECT : { 'STR' : 'DISCONNECT',
                       'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                       'RSP' : { 'TOKEN' : False, 'FIELDS' : [] }},
        GET : { 'STR' : 'GET',
                'REQ' : { 'TOKEN' : True, 'FIELDS' : [4] },
                'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        SET : { 'STR' : 'SET',
                'REQ' : { 'TOKEN' : True, 'FIELDS' : [4] },
                'RSP' : { 'TOKEN' : False, 'FIELDS' : [] }},
        DIAG : { 'STR' : 'DIAG',
                 'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                 'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        AAAA : { 'STR' : 'AAAA',
                 'REQ' : { 'TOKEN' : True, 'FIELDS' : [4] },
                 'RSP' : { 'TOKEN' : False, 'FIELDS' : [] }},
        BBBB : { 'STR' : 'BBBB',
                 'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                 'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        CCCC : { 'STR' : 'CCCC',
                 'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                 'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        DDDD : { 'STR' : 'DDDD',
                 'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                 'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        EEEE : { 'STR' : 'EEEE',
                 'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                 'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        FFFF : { 'STR' : 'FFFF',
                 'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                 'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
    }

    def __init__ (self):
        self.raw = b''

    def Reset (self):
        Packet.idx = 0

    def DeviceID (self):
        if ((self.pkt_type == Packet.GET) or
            (self.pkt_type == Packet.SET)):
            return self.payload[2]
        else:
            return None
        
    def Encode (self, ptype, payload):

        # Setup local variables
        self.magic = Packet.MAGIC
        self.idx = Packet.idx
        self.pkt_type = ptype
        self.direction = 'REQ'
        self.field_cnt = len(self.CMD[ptype]['REQ']['FIELDS']) + 1
        self.field = []
        for n in range (0, self.field_cnt - 1):
            self.field.append (self.CMD[ptype]['REQ']['FIELDS'][n])
        self.payload_len = len (payload)
        self.field.append (self.payload_len)
        if self.CMD[ptype]['REQ']['TOKEN']:
            self.token = Packet.token
        else:
            self.token = 0xFFFFFFFF
        self.payload = payload

        # Assemble into raw packet
        self.raw = self.magic
        self.raw += struct.pack ('<I', self.idx)
        self.raw += struct.pack ('<H', self.pkt_type)
        # Type = REQUEST
        self.raw += struct.pack ('<H', 1) 
        self.raw += struct.pack ('<I', self.field_cnt)
        # Fields
        for n in range (0, self.field_cnt):
            self.raw += struct.pack ('<I', self.field[n])
        # Add token if needed
        if self.CMD[ptype]['REQ']['TOKEN']:
            self.raw += struct.pack ('<I', self.token)
        # Add payload
        self.raw += payload
        
    def SendRecv (self, conn):
        conn.send (self.raw)
        self.Recv (conn)
        Packet.idx += 1
        # Save token if connect
        if self.pkt_type == Packet.CONNECT:
            Packet.token = struct.unpack ("<I", self.payload)[0]
        
    def Recv (self, conn):

        # Read first 16 bytes
        self.raw = conn.recv (16)
            
        # Decode global items
        self.magic = self.raw[0:4]
        self.idx = struct.unpack ("<I", self.raw[4:8])[0]
        self.pkt_type = struct.unpack ("<H", self.raw[8:10])[0]
        self.direction = struct.unpack ("<H", self.raw[10:12])[0]
        if self.direction == 1:
            self.direction = 'REQ'
        elif self.direction == 2:
            self.direction = 'RSP'
        else:
            self.direction = 'UNK'
        self.field_cnt = struct.unpack ("<I", self.raw[12:16])[0]
        self.field = []

        # Read fields
        idx = 16
        self.raw += conn.recv (self.field_cnt * 4)
        for n in range (0, self.field_cnt):
            self.field.append (struct.unpack ("<I", self.raw[idx:idx+4])[0])
            idx += 4

        # Length seems to be last field
        self.payload_len = self.field[self.field_cnt-1]

        # If expecting token then parse
        if ((self.pkt_type in self.CMD.keys()) and
            (self.CMD[self.pkt_type][self.direction]['TOKEN'])):
            self.raw += conn.recv (4)
            self.token = struct.unpack ("<I", self.raw[idx:idx+4])[0]
            idx += 4
        else:
            self.token = 0xFFFFFFFF

        # Read and store payload
        self.raw += conn.recv (self.payload_len)
        self.payload = self.raw[idx:]

    def Validate (self):
        if self.pkt_type not in self.CMD.keys():
            return False
        # Check magic
        if self.magic != self.MAGIC:
            return False
        # Check dir
        if self.direction != 'REQ' and self.direction != 'RSP':
            return False
        # Check length
        if self.payload_len != len(self.payload):
            return False
        # Passed validation
        return True

    def __str__ (self):
        if self.pkt_type not in self.CMD.keys ():
            ret = self.Debug ()
        else:
            ret = str (self.idx) + ':'
            ret += self.direction + ' '
            if self.direction == 'REQ':
                ret += self.CMD[self.pkt_type]['STR'] + ' '
        return ret

    # Dump out packet
    def Debug (self):
        ret = ""
        if self.Validate ():
            ret += "VALIDATE: OK\n"
        else:
            ret += "VALIDATE: FAIL\n"
        ret += "DIR  : " + self.direction + '\n'
        ret += "MAGIC: " + str(self.magic) + '\n'
        ret += "INDEX: " + str(self.idx) + '\n'
        if self.pkt_type in self.CMD.keys():            
            ret += "TYPE : " + self.CMD[self.pkt_type]['STR'] + '\n'
        else:
            ret += "TYPE : UNKNOWN:" + hex (self.pkt_type) + '\n'
        ret += "FCNT : " + str(self.field_cnt) + '\n'
        for n in range (0, self.field_cnt):
            ret += ' [' + str(n) + '] : ' + str(self.field[n]) + '\n'
        ret += "PLEN : " + str(self.payload_len) + '\n'
        ret += "TOKEN: " + str( hex (self.token)) + '\n'
        ret += "PAYLOAD:\n" + Packet.byte2hex (self.payload) + '\n\n'
        ret += Packet.byte2hex (self.raw) + '\n' + Packet.byte2hexstr (self.raw) + '\n'
        return ret

    @staticmethod
    def byte2hex (data):
        pdata = ' '.join("{:02x}".format(d) for d in data)
        pdata = '\n'.join(pdata[i:i+48] for i in range(0, len(pdata), 48))
        return pdata

    @staticmethod
    def byte2hexstr (data):
        ret = re.sub(f'[^{re.escape(string.printable)}]', '.', data.decode ('ascii', 'replace'))
        return re.sub(r"\s+", '.', ret)

    def Send (self, conn):
        conn.send (self.raw)

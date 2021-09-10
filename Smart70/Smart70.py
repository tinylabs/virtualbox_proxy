#
# Smart70 connection manager
#
# Manages connection to device
# Also can proxy traffic to decode in transit
#
#
import time
import socket
import ssl
import struct
import threading
import re
import string
from collections import defaultdict


class Packet:

    idx = 0
    MAGIC = b'ISNP'
    
    CMD = {
        0x03e8 : { 'STR' : 'CONNECT',
                   'REQ' : { 'TOKEN' : False, 'FIELDS' : [] },
                   'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        0x03e9 : { 'STR' : 'DISCONNECT',
                   'REQ' : { 'TOKEN' : True, 'FIELDS' : [] },
                   'RSP' : { 'TOKEN' : False, 'FIELDS' : [] }},
        0x0c1c : { 'STR' : 'GET',
                   'REQ' : { 'TOKEN' : True, 'FIELDS' : [4] },
                   'RSP' : { 'TOKEN' : True, 'FIELDS' : [4] }},
        0x0c1d : { 'STR' : 'PUT',
                   'REQ' : { 'TOKEN' : True, 'FIELDS' : [4] },
                   'RSP' : { 'TOKEN' : False, 'FIELDS' : [] }},
    }


    def __init__ (self, token=0):
        self.token = token
        self.raw = b''

    def Reset (self):
        Packet.idx = 0

    def Encode (self, ptype, payload):
        self.raw = Packet.MAGIC
        self.raw += Packet.idx
        Packet.idx += 1
        
    def Send (self, conn):
        conn.send (self.raw)
        
    def Recv (self, conn):

        # Read first 16 bytes
        self.raw = conn.recv (16)
            
        # Decode global items
        self.magic = self.raw[0:4]
        self.idx = struct.unpack ("<I", self.raw[4:8])[0]
        self.pkt_type = struct.unpack ("<H", self.raw[8:10])[0]
        self.direction = self.REQ_RESP[struct.unpack ("<H", self.raw[10:12])[0]]
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
        if self.CMD[self.pkt_type][self.direction]['TOKEN']:
            self.raw += conn.recv (4)
            self.token = struct.unpack ("<I", self.raw[idx:idx+4])[0]
            idx += 4
        else:
            self.token = 0xFFFFFFFF

        # Read and store payload
        self.raw += conn.recv (1024)
        self.payload = self.raw[idx:]

    def Validate (self):
        # Check magic
        if self.magic != self.MAGIC:
            return 0
        # Check dir
        if self.direction != 'REQ' and self.direction != 'RSP':
            return 0
        # Check length
        if self.payload_len != len(self.payload):
            return 0
        # Passed validation
        return 1

    def __str__ (self):
        ret = str (self.idx) + ':'
        ret += self.CMD[self.pkt_type]['STR'] + ' '
        ret += self.byte2hex (self.payload)
        return ret
    
    # Dump out packet
    def Verbose (self):
        ret = ""
        if self.Validate ():
            ret += "VALIDATE: OK\n"
        else:
            ret += "VALIDATE: FAIL\n"
        ret += "DIR  : " + self.direction + '\n'
        ret += "MAGIC: " + str(self.magic) + '\n'
        ret += "INDEX: " + str(self.idx) + '\n'
        ret += "TYPE : " + str(self.pkt_type) + '\n'
        ret += "FCNT : " + str(self.field_cnt) + '\n'
        for n in range (0, self.field_cnt):
            ret += ' [' + str(n) + '] : ' + str(self.field[n]) + '\n'
        ret += "PLEN : " + str(self.payload_len) + '\n'
        ret += "TOKEN: " + str( hex (self.token)) + '\n'
        ret += "PAYLOAD:\n" + self.byte2hex (self.payload) + '\n\n'
        ret += self.byte2hex (self.raw) + '\n' + self.byte2hexstr (self.raw) + '\n'
        return ret
    
    def byte2hex (self, data):
        pdata = ' '.join("{:02x}".format(d) for d in data)
        pdata = '\n'.join(pdata[i:i+48] for i in range(0, len(pdata), 48))
        return pdata

    def byte2hexstr (self, data):
        ret = re.sub(f'[^{re.escape(string.printable)}]', '.', data.decode ('ascii', 'replace'))
        return re.sub(r"\s+", '.', ret)

    def Send (self, conn):
        conn.send (self.raw)

class Smart70:

    # Connection modes
    MODE_CLIENT = 0
    MODE_PROXY  = 1

    # Openssl cipher spec for smart70
    CIPHER_SPEC = 'ADH-AES128-SHA:@SECLEVEL=0'
    
    def __init__ (self, remote_ip, remote_port):

        # Save params
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        
    def Connect (self):

        # Create client sock
        sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn = ssl.wrap_socket (sock,
                                            ssl_version=ssl.PROTOCOL_TLSv1,
                                            ciphers=self.CIPHER_SPEC)

        # Connect to server
        self.client_conn.connect ((self.remote_ip, self.remote_port))            

    # Open Smart70 system
    def Open (self):

        # Make SSL connection
        self.Connect ()
        
        # Connect to machine
        pkt = Packet ()
        pkt.Reset ()
        pkt.Encode (0x3e8, 'SMART'.encode ('utf-16'))
        pkt.Send ()

        # Receive response and token
        pkt.Recv ()

    # Close Smart70 system
    def Close (self):
        pass

    # Get list of modules
    def GetModules (self):
        pass

    # Return 64 bit status of module
    def GetStatus (self, mod):
        pass

    # Get module state
    # 0x04 - Module has card
    # 0x08 - Module is initializing
    # 0x10 - Running last command
    # 0x20 - Failed last command
    def GetState (self, mod):
        pass

    def CardIn (self, mod):
        pass

    def CardOut (self, mod):
        pass

    def CardMove (self, mod_from, mod_to):
        pass
    
    # Handle server to client responses
    def server2client (self, lock):

        while True:
        
            # Wait for packet from server
            try:
                pkt = Packet ()
                pkt.Recv (self.server_conn)
            except:
                print ("server conn broken")
                break
            
            # Send packet
            pkt.Send (self.client_conn)

            # Acquire lock
            lock.acquire ()

            # print response
            print (pkt)
            #print (pkt.Verbose())
        
            # Release lock
            lock.release ()

            # Break if disconnect
            if pkt.pkt_type == 'DISCONNECT':
                break

    def Proxy (self, server_port, mode='PARSED', pkt_handler=None):

        # Save mode
        self.mode = mode
        
        # Create server
        context = ssl.SSLContext (ssl.PROTOCOL_TLSv1)
        context.set_ciphers (self.CIPHER_SPEC)
        context.load_dh_params ("dhparam.pem")
        with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as server_tcp_sock:

            # Setup server socket
            server_tcp_sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_tcp_sock.bind (('', server_port))
            server_tcp_sock.listen (1)

            # Wrap in SSL
            with context.wrap_socket (server_tcp_sock,
                                      server_side = True) as server_sock:
                print ("SSL server listening on localhost:8080")

                while True:

                    # Accept connections
                    self.server_conn, addr = server_sock.accept ()
                    print ("Client connected:" + str(addr))

                    # Create client connection
                    self.Connect ()
                    print ("Connected to server: " + self.remote_ip + ':' + str(self.remote_port))

                    # Create communication lock
                    lock = threading.Lock ()
                
                    # Create server thread
                    sthread = threading.Thread (target=self.server2client, args=(lock,))
                    sthread.start ()
                    
                    # Shuttle packets from client to server
                    while True:
                        
                        # Wait for packet from server
                        try:
                            pkt = Packet ()
                            pkt.Recv (self.client_conn)
                        except:
                            print ("client conn broken")
                            break
            
                        # Pass packet to server
                        pkt.Send (self.server_conn)
                        
                        # Acquire lock
                        lock.acquire ()

                        # print response
                        print (pkt)
                        #print (pkt.Verbose())
            
                        # Release lock
                        lock.release ()

                        # Break if disconnect
                        if pkt.pkt_type == 'DISCONNECT':
                            break
                        
                    # Wait for thread to join
                    sthread.join ()
                
    
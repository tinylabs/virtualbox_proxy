#
# Smart70 connection manager
#
# Manages connection to device
# Also can proxy traffic to decode in transit
#
#
import socket
import ssl
import struct
import threading

from Device import *
from Packet import *

class Smart70:

    # Openssl cipher spec for smart70
    CIPHER_SPEC = 'ADH-AES128-SHA:@SECLEVEL=0'

    # System wide commands
    GET_DEVICES = 0x3250
    
    def __init__ (self, remote_ip, remote_port, verbose=0):

        # Save params
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.verbose = verbose
        self.device = {}
        self.get_devices = False
        self.pdev = None
        
    def Connect (self):

        # Create client sock
        sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn = ssl.wrap_socket (sock,
                                            ssl_version=ssl.PROTOCOL_TLSv1,
                                            ciphers=self.CIPHER_SPEC)

        # Connect to server
        self.client_conn.connect ((self.remote_ip, self.remote_port))            

    def Disconnect (self):
        self.client_conn.close ()
        
    # Open Smart70 system
    def Open (self):

        # Make SSL connection
        self.Connect ()
        
        # Connect to machine
        pkt = Packet ()
        pkt.Reset (self.verbose)
        pkt.Encode (Packet.CONNECT, b'S\x00M\x00A\x00R\x00T\x00\x00\x00')

        # Token stored automatically
        pkt.SendRecv (self.client_conn)

    # Close Smart70 system
    def Close (self):

        # Create disconnect packet
        pkt = Packet ()
        pkt.Encode (Packet.DISCONNECT, struct.pack ('<I', Packet.token))
        pkt.SendRecv (self.client_conn)

        # Close socket
        self.Disconnect ()

    def GetDevicesDecode (self, pkt):
        # Decode response
        devices = []
        cnt = pkt.payload[0]
        dp = pkt.payload[1:]
        for n in range (0, cnt):
            dev = Device.Create (dp[n*2], self.client_conn, dp[n*2+1])
            devices.append (dev)
            self.device[dp[n*2]] = dev
        return devices
        
    # Get list of modules
    def GetDevices (self):

        # Create a packet
        pkt = Packet ()
        pkt.Encode (Packet.GET, struct.pack ('<H', self.GET_DEVICES) + b'\x00')
        pkt.SendRecv (self.client_conn)
        return self.GetDevicesDecode (pkt)
    
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
            if self.verbose == 1:
                print (pkt, end='')
                if pkt.payload[-1] in self.device.keys ():
                    self.pdev = self.device[pkt.payload[-1]]
                    print (self.pdev.DecodeStr (pkt))
                else:
                    self.pdev = None
                    print (pkt.byte2hex (pkt.payload))
            elif self.verbose == 2:
                print (pkt.Verbose())
        
            # Release lock
            lock.release ()

            # Break if disconnect
            if pkt.pkt_type == Packet.DISCONNECT:
                break
            elif (pkt.direction == 'REQ') and (pkt.payload == b'\x50\x32\x00'):
                self.get_devices = True

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
                        if self.verbose == 1:
                            print (pkt, end='')
                            if self.pdev:
                                print (self.pdev.DecodeStr (pkt))
                            else:
                                print (pkt.byte2hex (pkt.payload))

                        elif self.verbose == 2:
                            print (pkt.Verbose())
            
                        # Release lock
                        lock.release ()

                        # Decode device list if GET_DEVICES response
                        if self.get_devices:
                            self.get_devices = False
                            self.GetDevicesDecode (pkt)

                        # Break if disconnect
                        if pkt.pkt_type == Packet.DISCONNECT:
                            break
                        
                    # Wait for thread to join
                    sthread.join ()
                
    

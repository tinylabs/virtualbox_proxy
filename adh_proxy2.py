#!/bin/env python3
#
# Use openssl to create a proxy for the given port
# redirect all output to target but print
# plaintext conversation
#

import re
import string
import shlex
import subprocess
import time
import threading
import argparse
import datetime
import struct
import signal

# Describe packet structure to talk to printer
class Packet:
    MAGIC = b'ISNP'
    REQUEST      = 0x0001
    RESPONSE     = 0x0002
    TYPE_TOKEN   = 1000
    TYPE_ITEM    = 3100
    ACT_DEVICES  = 0x3250
    ACT_FIRMWARE = 0x0150
    ACT_STATUS   = 0x0003
    ACT_STATE    = 0x0360
    DEV_SYSTEM   = 0x00
    DEV_HOPPER   = 0x10
    DEV_PRINTER  = 0x40
    DEV_FLIPPER  = 0x60
    
    dir_str = {
        REQUEST       : 'REQUEST',
        RESPONSE      : 'RESPONS'
    }
    type_str = {
        TYPE_TOKEN   : 'TOKEN',
        TYPE_ITEM    : 'ITEM'
    }
    dev_str = {
        DEV_SYSTEM   : 'SYSTEM',
        DEV_HOPPER   : 'HOPPER',
        DEV_PRINTER  : 'PRINTER',
        DEV_FLIPPER  : 'FLIPPER'
    }
    act_str = {
        ACT_DEVICES  : 'DEVICES',  # Get devices
        ACT_FIRMWARE : 'FIRMWARE', # Short status
        ACT_STATUS   : 'STATUS',   # Extended status
        ACT_STATE    : 'STATE',    # Get state
    }

    # Store previous action
    pact = None
    
    def __init__ (self, data):
        self.raw = data
        self.magic = data[0:4]
        self.idx = struct.unpack ("<I", data[4:8])[0]
        self.type = struct.unpack ("<H", data[8:10])[0]
        self.dir = struct.unpack ("<H", data[10:12])[0]
        self.fcnt = struct.unpack ("<I", data[12:16])[0]
        idx = 16
        self.field = []
        for n in range (0, self.fcnt):
            self.field.append (struct.unpack ("<I", data[idx:idx+4])[0])
            idx += 4
        # Length seems to be last field
        self.plen = self.field[self.fcnt-1]
        # Will be zero on response
        if self.field[0] == 4:
            self.token = struct.unpack ("<I", data[idx:idx+4])[0]
            idx += 4
        else:
            self.token = 0xFFFF
        self.payload = data[idx:]

        # Decode action if request
        if self.dir == self.REQUEST and self.type == self.TYPE_ITEM:
            self.act = struct.unpack ("<H", self.payload[0:2])[0]
            Packet.pact = self.act
            
    def dump_raw (self):
        print ("DIR  : " + self.dir_str ())
        print ("MAGIC: " + str(self.magic))
        print ("INDEX: " + str(self.idx))
        if self.validate ():
            print ("VALIDATE: OK")
        else:
            print ("VALIDATE: FAIL")
        print ("TYPE : " + str(self.type))
        print ("FCNT : " + str(self.fcnt))
        for n in range (0, self.fcnt):
            print (' [' + str(n) + '] : ' + str(self.field[n]))
        print ("PLEN : " + str(self.plen))
        print ("TOKEN: " + str( hex (self.token)))
        print ("PAYLOAD: " + self.byte2hex (self.payload))
        
    def __str__ (self):
        ret = self.dir_str[self.dir] + '[' + str(self.idx) + '] '
        ret += self.type_str[self.type] + ' : '

        # Handle token
        if self.type == self.TYPE_TOKEN:
            if self.dir == self.REQUEST:
                ret += self.payload.decode ('utf-16')[:-1]
            else:
                ret += hex (struct.unpack ("<I", self.payload)[0])
            
        # Handle ITEM packets
        elif self.type == self.TYPE_ITEM:

            # Handle Item requests
            if self.dir == self.REQUEST:

                # Decode destinaton devices
                ret += self.dev_str[self.payload[-1]] + ' : '

                # Decode action from payload
                ret += self.act_str[self.act]

            # Handle ITEM responses
            else:

                # Handle firmware request
                if Packet.pact == self.ACT_FIRMWARE:
                    ret += self.payload.decode ('ascii')
                # Handle STATUS                
                elif Packet.pact == self.ACT_STATUS:
                    code = struct.unpack("<Q", self.payload[0:8])[0]
                    ret += 'STATUS=' + hex(code)
                    if len (self.payload) > 8:
                        ret += ' +[' + self.byte2hex (self.payload[8:]) + ']'
                # Handle STATE
                elif Packet.pact == self.ACT_STATE:
                    ret += 'STATE=' + hex (self.payload[1])
                elif Packet.pact == self.ACT_DEVICES:
                    cnt = self.payload[0]
                    ret += 'FOUND ' + str (cnt) + ' ['
                    for n in range (0, cnt):
                        ret += self.dev_str[self.payload[n * 2 + 1]] + ' '
                    ret += ']'
                    
                # Catch all
                else:
                    ret += self.byte2hex (self.payload)
        return ret
    
    def validate (self):
        # Check magic
        if self.magic != self.MAGIC:
            return 0
        # Check dir
        if self.dir != self.REQUEST and self.dir != self.RESPONSE:
            return 0
        # Check length
        if self.plen != len(self.payload):
            return 0
        # Passed validation
        return 1

    def byte2hex (self, data):
        pdata = ' '.join("{:02x}".format(d) for d in data)
        pdata = '\n'.join(pdata[i:i+48] for i in range(0, len(pdata), 48))
        return pdata

    def byte2hexstr(self, data):
        ret = re.sub(f'[^{re.escape(string.printable)}]', '.', data.decode ('ascii', 'replace'))
        return re.sub(r"\s+", '.', ret)


# Globals for cleanup
#cproc = None
#sproc = None
#cthread = None
#sthread = None
#def control_c (signum, frame):
#    # Clean up
#    print ("Cleaning up")
#    cproc.terminate ()
#    cthread.join ()
#    sproc.terminate ()        
#    sthread.join ()
#    sys.exit (0)
    

# Listen for client requests from the application
# client => server
def listen_client (port, cproc, sproc, log):
    print ("server listening on *:" + port)
    cin = cproc.stdout.raw
    data = b''
    while 1:
        data += cin.read (1024)
        #ts = datetime.datetime.now().strftime("%M.%S.%f")
        if data and len(data) >= 31:
            sproc.stdin.write (data)
            sproc.stdin.flush ()
            p = Packet (data)
            data = b''
            print (p)
            #p.dump_raw ()
            #ldata = '>>>\n'
            #ldata += decode_req (data)
            #ldata += byte2hex (data) + '\n'
            #ldata += byte2hexstr (data) + '\n'
            #if log:
            #    log.write (ldata)
            #    log.flush ()
            #print (ldata)
        time.sleep (0.1)

# Listen for server responses
# server => client
def listen_server (server, sproc, cproc, log):
    print ("connected to server:" + server)
    sin = sproc.stdout.raw
    while 1:
        data = sin.read (1024)
        #ts = datetime.datetime.now().strftime("%M.%S.%f")
        cproc.stdin.write (data)
        cproc.stdin.flush ()
        if data:
            p = Packet (data)
            #p.dump_raw ()
            print (p)
            #ldata = '<<<\n'
            #ldata += decode_resp (data)
            #ldata += byte2hex (data) + '\n'
            #ldata += byte2hexstr (data) + '\n'
            #if log:
            #    log.write (ldata)
            #    log.flush ()
            #print (ldata)
        time.sleep (0.1)
    

def main (args):

    global cproc, sproc, cthread, sthread
    
    # Server command
    scmd = 'stdbuf -o0 openssl s_server -cipher "ADH-AES128-SHA:@SECLEVEL=0" -accept *:' + args.port + ' -nocert -quiet'
    
    # Create subprocess for server, disable buffering
    sproc = subprocess.Popen(shlex.split(scmd), stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # Client command
    ccmd = 'stdbuf -o0 openssl s_client -tls1 -cipher "ADH-AES128-SHA:@SECLEVEL=0" -connect ' + args.server + ' -noservername -quiet'
    
    # Create subprocess for server, disable buffering
    cproc = subprocess.Popen(shlex.split(ccmd), stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # Create logging file
    if args.log:
        log = open (args.log, 'w')
    else:
        log = None
        
    # Create thread to handle client request
    sthread = threading.Thread (target=listen_client, args=(args.port, sproc, cproc, log))
    sthread.start ()

    # Create thread to handle client request
    cthread = threading.Thread (target=listen_server, args=(args.server, cproc, sproc, log))
    cthread.start ()
    print ("Threads started - kill with CTRL^C")

    # Catch control-c
    #signal.signal (signal.SIGINT, control_c)
    
    # Wait for client to disconnect
    sthread.join ()
    cproc.terminate ()
    cthread.join ()

    
if __name__ == '__main__':

    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument ('--port', type=str, help='listening port', required=True)
    parser.add_argument ('--server', type=str, help='server_ip:port', required=True)
    parser.add_argument ('--log', type=str, help='log file')
    args = parser.parse_args ()
    main (args)
    

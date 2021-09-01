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
from termcolor import colored

def byte2hexstr(data):
    ret = re.sub(f'[^{re.escape(string.printable)}]', '.', data.decode ('ascii', 'replace'))
    return re.sub(r"\s+", '.', ret)

# Listen for client requests from the application
# client => server
def listen_client (port, cproc, sproc):
    print ("server listening on *:" + port)
    cin = cproc.stdout.raw
    while 1:
        data = cin.read (1024)
        #ts = datetime.datetime.now().strftime("%M.%S.%f")
        sproc.stdin.write (data)
        sproc.stdin.flush ()
        if data:
            pdata = ' '.join("{:02x}".format(d) for d in data)
            pdata = '\n'.join(pdata[i:i+48] for i in range(0, len(pdata), 48))
            print (colored (pdata, 'red'))
            print (colored (byte2hexstr (data), 'red'))
            time.sleep (0.1)

# Listen for server responses
# server => client
def listen_server (server, sproc, cproc):
    print ("connected to server:" + server)
    sin = sproc.stdout.raw
    while 1:
        data = sin.read (1024)
        #ts = datetime.datetime.now().strftime("%M.%S.%f")
        cproc.stdin.write (data)
        cproc.stdin.flush ()
        if data:
            pdata = ' '.join("{:02x}".format(d) for d in data)
            pdata = '\n'.join(pdata[i:i+48] for i in range(0, len(pdata), 48))
            print (colored (pdata, 'blue'))
            print (colored (byte2hexstr (data), 'blue'))
        time.sleep (0.1)
    

def main (args):

    # Server command
    scmd = 'stdbuf -o0 openssl s_server -cipher "ADH-AES128-SHA:@SECLEVEL=0" -accept *:' + args.port + ' -nocert -quiet'
    
    # Create subprocess for server, disable buffering
    sproc = subprocess.Popen(shlex.split(scmd), stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # Client command
    ccmd = 'stdbuf -o0 openssl s_client -tls1 -cipher "ADH-AES128-SHA:@SECLEVEL=0" -connect ' + args.server + ' -noservername -quiet'
    
    # Create subprocess for server, disable buffering
    cproc = subprocess.Popen(shlex.split(ccmd), stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # Create thread to handle client request
    sthread = threading.Thread (target=listen_client, args=(args.port, sproc, cproc))
    sthread.start ()

    # Create thread to handle client request
    cthread = threading.Thread (target=listen_server, args=(args.server, cproc, sproc))
    cthread.start ()
    print ("Threads started - kill with CTRL^C")
    
    # Wait for client to disconnect
    sthread.join ()
    print ("Client disconnected... Cleaning up")
    cproc.terminate ()        

    
if __name__ == '__main__':

    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument ('--port', type=str, help='listening port')
    parser.add_argument ('--server', type=str, help='server_ip:port')
    parser.add_argument ('--log', type=str, help='log file')
    args = parser.parse_args ()
    main (args)
    

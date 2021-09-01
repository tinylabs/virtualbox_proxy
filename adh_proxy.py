#!/bin/env python3
#
# Create an ADH server and client
# Proxy connection between two while dumping plaintext data
import socket
import ssl



if __name__ == '__main__':

    # Create client socket
    client_tcp_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    # Wrap socket with SSL
    client_sock = ssl.wrap_socket (client_tcp_sock,
                                   ssl_version=ssl.PROTOCOL_TLSv1,
                                   ciphers='ADH-AES128-SHA:@SECLEVEL=0')

    # Connect to server
    client_sock.connect (('192.168.1.17', 11110))
    print ("Connected to target server")
    
    # Create server
    #context = ssl.SSLContext (ssl.PROTOCOL_TLS_SERVER)
    context = ssl.SSLContext (ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    #context = ssl.create_default_context (purpose=ssl.Purpose.CLIENT_AUTH)
    #context.options |= ssl.OP_NO_SSLv3
    #context.options |= ssl.OP_NO_SSLv2
    #context.options |= ssl.OP_NO_TLSv1_1
    #context.options |= ssl.OP_NO_TLSv1_2
    #context.options |= ssl.OP_NO_TLSv1_3
    #context.set_ciphers ('ADH-AES128-SHA:@SECLEVEL=0')
    #context.set_ciphers ('ALL:@SECLEVEL=0')
    context.set_ciphers ('ADH-AES128-SHA:@SECLEVEL=0')
    #print (context.get_ciphers ())
    
    with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as server_tcp_sock:
        server_tcp_sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_tcp_sock.bind (('192.168.56.1', 8080))
        server_tcp_sock.listen (5)

        # Wrap in SSL
        with context.wrap_socket (server_tcp_sock,
                                  server_side = True) as server_sock:
            print ("SSL server listening on localhost:8080")
            #print (context.get_ciphers ())
            
            # Accept connections
            conn, addr = server_sock.accept ()
            print ("New conn from " + addr)
            
            # Read from client
            req = conn.recv ()

            # Send to server
            client_sock.send (msg)

            # Read from server
            resp = client_sock.recv ()

            # Send to client
            conn.sendall (resp)

        # Cleanup
        client_sock.close ()
        server_sock.shutdown (socket.SHUT_RDWR)
        server_sock.close ()

    

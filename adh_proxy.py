#!/bin/env python3
#
# Create an ADH server and client
# Proxy connection between two while dumping plaintext data
import socket
import ssl



if __name__ == '__main__':

    # Create client socket
    client_tcp_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    #import pdb; pdb.set_trace()

    # Override default ciphers
    ssl._ssl._DEFAULT_CIPHERS = 'ADH-AES128-SHA:@SECLEVEL=0'
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
    context.set_ciphers ('ADH-AES128-SHA:@SECLEVEL=0')
    context.load_dh_params ("dhparam.pem")
    with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as server_tcp_sock:

        # Setup server socket
        server_tcp_sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_tcp_sock.bind (('', 8080))
        server_tcp_sock.listen (1)
        
        # Wrap in SSL
        with context.wrap_socket (server_tcp_sock,
                                  server_side = True) as server_sock:
            print ("SSL server listening on localhost:8080")
            #print (context.get_ciphers ())
            
            # Accept connections
            conn, addr = server_sock.accept ()
            print ("New conn from " + str(addr))

            # Read from client
            req = conn.recv ()

            # Send to server
            client_sock.send (req)

            # Read from server
            resp = client_sock.recv ()

            # Send to client
            conn.sendall (resp)

        # Cleanup
        client_sock.close ()
        server_sock.shutdown (socket.SHUT_RDWR)
        server_sock.close ()

    '''
    server_tcp_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    server_tcp_sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_tcp_sock.bind (('', 8080))
    server_tcp_sock.listen (1)

    while True:
        conn, addr = ssl.wrap_socket (
            server_tcp_sock,
            server_side = True,
            cert_reqs = ssl.CERT_NONE,
            certfile = 'ca.crt',
            keyfile = 'ca.key',
            ssl_version=ssl.PROTOCOL_TLSv1,
            do_handshake_on_connect=False,
            ciphers='ADH-AES128-SHA:@SECLEVEL=0'
        ).accept()

        import pdb; pdb.set_trace()

    '''
    
    #import pdb; pdb.set_trace()

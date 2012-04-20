#! /usr/bin/env python
import sys
import socket
import miniapp
import string

running = True

def handle_connection(sock):
    sentinel = '\r\n\r\n'
    data = ''
    while 1:
        try:
            receivedByte = sock.recv(1)
            data += receivedByte    
            
            if sentinel in data:
                break
        except socket.error:
            break
    
    #check if this is a POST request
    tmp = data
    tmp.strip()
    allLines = tmp.split('\r\n')
    request = allLines.pop(0)
    requestInfoList = request.split(' ')
    
    if "Content-Type: application/x-www-form-urlencoded" in tmp:
        contentLength = 0
        
        # get the content length
        for line in allLines:
            splitLine = line.split(':', 2)
            if splitLine[0].lower() == 'content-length':
                contentLength = splitLine[1].strip()
        # now we loop a sock.recv of size 1 to get all POST data
        # the Content-Length header denotes how long the POST data is
        # eg. 45 = 45 bytes, so sock.recv(1) 45 times
        contentLength = int(contentLength)
        if contentLength > 0:
            i = 0
            while i < contentLength:
                x = sock.recv(1)
                data += x
                i += 1
        print "data:", (data,)
        

    try:            
        response = miniapp.buildResponse(string.split(data, '\r\n'))
        sock.sendall(response)
        sock.close()
    except socket.error:
        print 'socket failed'        

def runServer(ip, port):
    port = int(port)

    print 'binding', ip, port
    sock = socket.socket()
    sock.bind( (ip, port) )
    sock.listen(5)

    while running:
        #print 'waiting...'
        (client_sock, client_address) = sock.accept()
        #print 'got connection', client_address
        handle_connection(client_sock)
        
    sock.close()   

if __name__ == '__main__':
    interface, port = sys.argv[1:3]
    runServer(interface, port)
    
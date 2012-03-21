import unittest
import serve2
import socket

class fake_socket(object):
    closed = False
    index = 0
    #try to retreive the index page
    retVal = 'GET / HTTP/1.1\r\n\r\n'
    
    def recv(self, size):
        data = self.retVal[self.index]
        self.index+=1
        if self.index > len(self.retVal):
            return ''
        return data    
            
    def sendall(self, data):
        #catches the first response and second response
        assert ('POST /RPC2 HTTP/1.1' in data or 
                '<p>Please login to create and delete messages</p>' in data)
        
    def getsockname(self):
        return ('127.0.0.1','8001')
    
    def close(self):
        self.closed = True
        
        
#needed all of this extra crap, otherwise warnings were shown in httplib.py
    def readline(self, *args):
        pass
    
    def __call__(self, *args):
        return self        
        
    def connect(self, *args):
        pass
    
    def makefile(self, *args):
        class fake_makefile(object):
            def readline(self, *args):
                return 'foo'
            
            def read(self, *args):
                return 'foo'
            
            def readlines(self, *args):
                return 'foo'
        
        return fake_makefile()
    


class TestMeepLib(unittest.TestCase):
    
    def setUp(self):
        self.socket_save = socket.socket
        socket.socket = fake_socket()
        
    def test_for_socket_closed(self):
        fs = fake_socket()
        serve2.handle_connection(fs)
        assert fs.closed

    def tearDown(self):
        socket.socket = self.socket_save

if __name__ == '__main__':
    unittest.main()
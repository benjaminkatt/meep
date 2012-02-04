import unittest
import string
import os
import meep_example_app

class TestApp(unittest.TestCase):
    def setUp(self):
        #the backup file causes some of the tests to fail - not sure why
        #remove the backup file before every test
        try:
            os.remove(meep_example_app.meeplib._getFileName())
        except:
            pass    #the file does not exist
        
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app

    def test_index(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        #The app does not allow messages to be added here since nobody is logged in
        #assert 'Add a message' in data[0]
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
        assert 'Create a New User' in data[0]
        assert 'Show messages' in data[0]
        
    def test_create_user(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'
        environ['wsgi.input'] = ''
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert string.find(data, 'Username') != -1
        assert string.find(data, 'Password') != -1
    
    def test_login_and_logout(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
        
        #check that the user is logged out to begin with    
        data = self.app(environ, fake_start_response)
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
        
        #log in
        meep_example_app.meeplib.set_current_user('studentx')
        data = self.app(environ, fake_start_response)
        assert 'you are logged in as user: studentx' in data[0]
        assert 'Log out' in data[0]
        
        #log out
        meep_example_app.meeplib.set_current_user('')
        data = self.app(environ, fake_start_response)
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
    
    def test_show_messages(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert 'This is my message!' in data[0]
        #nobody is logged in, so no creation of responses or deleting allowed
        assert 'Submit response' not in data[0]
        assert 'Delete this message' not in data[0]
        
        #log in, creation of responses and deleting is allowed
        meep_example_app.meeplib.set_current_user('studentx')
        data = self.app(environ, fake_start_response)
        assert 'Submit response' in data[0]
        assert 'Delete this message' in data[0]

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

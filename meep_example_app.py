import meeplib
import traceback
import cgi
import meepcookie
import Cookie

from jinja2 import Environment, FileSystemLoader
from fileServer import FileServer

def initialize():
    #clear everything out before loading, this fixes a few tests
    meeplib._messages = {}
    meeplib._users = {}
    meeplib._user_ids = {}
    meeplib._load_backup()
    
    if (len(meeplib._messages) == 0 and len(meeplib._users) == 0):
        # create default users
        u = meeplib.User('test', 'foo')
        u.insertIntoDB()
        a = meeplib.User('Anonymous', 'password')
        a.insertIntoDB()
        x = meeplib.User('studentx', 'passwordx')
        x.insertIntoDB()
        y = meeplib.User('studenty', 'passwordy')
        y.insertIntoDB()
        z = meeplib.User('studentz', 'passwordz')
        z.insertIntoDB()
        m = meeplib.Message('my title', 'This is my message!', u.id, -1)
        m.insertIntoDB()
        
        
env = Environment(loader=FileSystemLoader('templates'))

def render_page(filename, **variables):
    template = env.get_template(filename)
    x = template.render(**variables)
    return str(x)

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def authHandler(self, environ):
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            user = meeplib.getUserFromUUID(username)
            return user
        except:
            return None
        
    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        return [ render_page("create_user.html") ]
       
        
    def create_user_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
        try:
            username = form['username'].value
            password = form['password'].value
            u = meeplib.User(username, password)
            u.insertIntoDB()
        except:
            pass

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers = [('Content-type', 'text/html')]
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return ["no such content"]
        
    def index(self, environ, start_response):
        user = self.authHandler(environ)
        start_response("200 OK", [('Content-type', 'text/html')])
        return [ render_page('index.html', user = user) ]
        
    def login(self, environ, start_response):
        user = self.authHandler(environ)
        
        headers = [('Content-type', 'text/html')]
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        try:
            username = form['username'].value
            user = meeplib.get_user(username)
            password = form['password'].value
        except:
            password = None
               
        if ((user is not None) and 
            (password is not None) and 
            (user.password == password)):
            k = 'Location'
            v = '/'
            headers.append((k, v))
            cookie_name, cookie_val = meepcookie.make_set_cookie_header('username', user)
            headers.append((cookie_name, cookie_val))
            
        start_response('302 Found', headers)
        return [ render_page('login.html') ]
        

    def logout(self, environ, start_response):
        user = self.authHandler(environ)
        # does nothing
        headers = [('Content-type', 'text/html')]
        
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
        username = cookie["username"].value
        cookie_name, cookie_val = meepcookie.destroyCookieHeader(username)
        headers.append((cookie_name, cookie_val))
        start_response('302 Found', headers)
        
        return ["no such content"]

    def list_messages(self, environ, start_response):
        user = self.authHandler(environ)
        messages = meeplib.get_all_messages()
        userIDs = meeplib.getUserIDs()
        start_response("200 OK", [('Content-type', 'text/html')])
        return [ render_page('list_messages.html', user = user, messages = messages, userIDs = userIDs) ]

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", [('Content-type', 'text/html')])
        return [ render_page('add_message.html') ]

    def remove_message(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        messageID = form['messageID'].value
        message = meeplib.get_message(int(messageID))
        meeplib.delete_message(message)
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message removed"]
    
    def reply_message(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        parentPostID = int(form['parentPostID'].value)
        user = self.authHandler(environ)
        new_message = meeplib.Message(title, message, user.id, parentPostID)
        new_message.insertIntoDB()

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def add_message_action(self, environ, start_response):
        user = self.authHandler(environ)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        parentPostID = int(form['parentPostID'].value)
        
        new_message = meeplib.Message(title, message, user.id, parentPostID)
        new_message.insertIntoDB()

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      #'/home': self.home,
                      '/create_user': self.create_user,
                      '/create_user_action': self.create_user_action,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/remove': self.remove_message,
                      '/m/reply': self.reply_message,
                      '/m/add_action': self.add_message_action,
                      '/style.css': FileServer('styles/style.css'),
                      '/images/background.png': FileServer('styles/images/background.png'),
                      '/images/background_content.gif': FileServer('styles/images/background_content.gif'),
                      '/images/background_top.gif' : FileServer('styles/images/background_top.gif'),
                      '/images/background_bottom.gif' : FileServer('styles/images/background_bottom.gif')

                      }

        # see if the URL is in 'call_dict'; if it is, call that function.
        url = environ['PATH_INFO']
        fn = call_dict.get(url)

        if fn is None:
            start_response("404 Not Found", [('Content-type', 'text/html')])
            return ["Page not found."]

        try:
            return fn(environ, start_response)
        except:
            tb = traceback.format_exc()
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]

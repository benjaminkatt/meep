import meeplib
import traceback
import cgi
import pickle
import meepcookie


#Updated for HW3 11:43 Jan26
#username = 'test'
def initialize():
    try:
        meeplib._load_backup()
    except IOError:
        # create default users
        u = meeplib.User('test', 'foo')
        a = meeplib.User('Anonymous', 'password')
        x = meeplib.User('studentx', 'passwordx')
        y = meeplib.User('studenty', 'passwordy')
        z = meeplib.User('studentz', 'passwordz')
        meeplib.Message('my title', 'This is my message!', u, -1)

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def authHandler(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
        except:
            username = ''    
        user = meeplib.get_user(username)
    
    def index(self, environ, start_response):
        user = self.authHandler(environ, start_response)
        
        if user is None:
            return ["""Please login to create and delete messages
			    <p><a href='/login'>Log in</a>
			    <p><a href='/create_user'>Create a New User</a>
			    <p><a href='/m/list'>Show messages</a>"""]
        else:
            return ["""you are logged in as user: %s
			    <p><a href='/m/add'>Add a message</a>
			    <p><a href='/create_user'>Create a New User</a>
			    <p><a href='/logout'>Log out</a>
			    <p><a href='/m/list'>Show messages</a>""" % user.username]
        
    def login(self, environ, start_response):
        user = self.authHandler(environ, start_response)
        headers = [('Content-type', 'text/html')]
        if user is not None:
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return """<form action='login_action' method='POST'>
                        Username: <input type='text' name='username'><br>
                        Password:<input type='text' name='password'><br>
                        <input type='submit' value='Login' />
                    </form>"""
        
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        try:
            username = form['username'].value
            password = form['password'].value
        except:
            username = ''
            password = ''
            
        user = meeplib.get_user(username)
        if user is not None and user.password == password:
            k = 'Location'
            v = '/'
            headers.append((k, v))
            cookie_name, cookie_val = meepcookie.make_set_cookie_header('username', user.username)
            headers.append((cookie_name, cookie_val))
        elif user is None:
            return login_failed(environ, start_response)
        
        return index(environ, start_response)

        

    def login_failed(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        
        return ["""Login Failed. Please Try Again.<p><p><p><a href='/'>Index</a>"""]
    

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
       
        return """<form action='create_user_action' method='POST'>
                    Username: <input type='text' name='username'><br>
                    Password:<input type='text' name='password'><br>
                    <input type='Submit' value='Create User' />
                </form>"""
       
        
    def create_user_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
                
        try:
            username = form['username'].value
        except KeyError:
            username = None

        try:
            password = form['password'].value
        except KeyError:
            password = None

        u = meeplib.User(username, password)

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers = [('Content-type', 'text/html')]
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

        
        

    def logout(self, environ, start_response):
        # does nothing
        headers = [('Content-type', 'text/html')]
        meeplib.set_current_user('')
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()

        s = []
        stack = []
        for m in messages:
            while (len(stack) > 0) and (stack[-1] != m.parentPostID):
                stack.pop()
                
            s.append('<div style=margin-left:' + str(len(stack) * 100) + 'px>id: %d<p>' % (m.id))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            s.append('author: %s<p>' % (m.author.username))
            if meeplib.get_current_user() != '':
                s.append("""
                    <script type='text/javascript'>var clearedResponseText = false;</script>
                    <form action='reply' method='POST'>
                    <input type='hidden' name='title' value='""" + str(m.title) + """' />
                    <input type='hidden' name='parentPostID' value='""" + str(m.id) + """' />
                    <input type='text' name='message' value='Enter a response here'
                        onclick="if (!clearedResponseText) {
                            value = ''; 
                            clearedResponseText = true;
                        }" />
                    <input type='submit' value='Submit response' />
                    </form>""")
                s.append("""
                    <form action='remove' method='POST'>
                    <input type='hidden' name='messageID' value='""" + str(m.id) + """' />
                    <input type='submit' value='Delete this message' />
                    </form>""")
            s.append('</div><hr>')
            if m.id != -1:
                stack.append(m.id)


        s.append("<a href='../../'>index</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """
            <form action='add_action' method='POST'>
            <input type='hidden' name='parentPostID' value='-1' />
            Title: <input type='text' name='title'><br>
            Message:<input type='text' name='message'><br>
            <input type='submit'>
            </form>
            """

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
        user = meeplib.get_user(meeplib.get_current_user())
        new_message = meeplib.Message(title, message, user, parentPostID)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def add_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        parentPostID = int(form['parentPostID'].value)
        print meeplib.get_current_user()
        user = meeplib.get_user(meeplib.get_current_user())
        
        new_message = meeplib.Message(title, message, user, parentPostID)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def delete_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        id = form['messageID'].value
        message = meeplib.get_message(int(id))
        meeplib.delete_message(message)
                     
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message deleted"]
        

        
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      #'/home': self.home,
                      '/create_user': self.create_user,
                      '/create_user_action': self.create_user_action,
                      '/login': self.login,
                      '/login_failed': self.login_failed,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,

                      '/m/remove': self.remove_message,
                      '/m/reply': self.reply_message,
                      '/m/add_action': self.add_message_action

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

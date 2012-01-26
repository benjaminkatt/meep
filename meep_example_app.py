import meeplib
import traceback
import cgi


#Updated for HW2  12:17 Jan24
#username = 'test'
def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')
    a = meeplib.User('Anonymous', 'password')
    x = meeplib.User('studentx', 'passwordx')
    y = meeplib.User('studenty', 'passwordy')
    z = meeplib.User('studentz', 'passwordz')
    meeplib.set_current_user('Anonymous')
    #e = meeplib.get_user('studenty')
    #print e
    
    # create a single message
    meeplib.Message('my title', 'This is my message!', u, -1)

    #loggedIn = False
    
    # done

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    #currentUser = 'test'
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        #username = 'student'
        #print username
        #print loggedIn
        #if (loggedIn == 0):
         #   print "qwerty"
        #if loggedIn:
        #print get_user(username)
        username = 'test'
        #return ["""you are logged in as user: %s<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % meeplib.get_current_user()]
        return ["""you are logged in as user: %s<p><a href='/m/add'>Add a message</a><p><a href='/create_user'>Create a New User</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % meeplib.get_current_user()]
        
    def login(self, environ, start_response):
        print "login test 1"
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        
        return """<form action='login_action' method='POST'>Username: <input type='text' name='username'><br>Password:<input type='text' name='password'><br><input type='submit'></form>"""

    def login_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
        #loggedIn = 1
        
        try:
            username = form['username'].value
        except KeyError:
            username = None

        try:
            password = form['password'].value
        except KeyError:
            password = None

            
        if username is not None:
            #print username
            if password is not None:
                print password
                if meeplib.is_user(username, password):
                    print "correct password"
                    meeplib.set_current_user(username)
                    print username
                    print meeplib.get_current_user()
                    v = '/'
                else:
                    print 'incorrect password'
                    v = '/login_failed'
            else:
                print 'bad password'
                v = '/login_failed'
            
        else:
            print 'bad username'
            v = '/login_failed'

        
            
        # retrieve user
        user = meeplib.get_user(username)

        # set content-type
        headers = [('Content-type', 'text/html')]
        
        # send back a redirect to '/'
        k = 'Location'
        
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def login_failed(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        
        return ["""Login Failed. Please Try Again.<p><p><p><a href='/'>Index</a>"""]
    

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
       
        return """<form action='create_user_action' method='POST'>Username: <input type='text' name='username'><br>Password:<input type='text' name='password'><br><input type='Submit'></form>"""
       
        
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
                <input type='submit' value='Delete this message' 
                    onclick="return confirm('Are you sure you want to delete this message? Any responses will also be deleted.')" />
                </form></div>""")
            s.append('<hr>')
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
        username = 'test'
        user = meeplib.get_user(username)
        

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
        username = 'test'
        user = meeplib.get_user(username)
        
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
                      '/login_action': self.login_action,
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

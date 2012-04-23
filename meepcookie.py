from Cookie import SimpleCookie
from mysqlConnection import con, cur
import uuid

def make_set_cookie_header(name, value, path='/'):
    """
    Makes a 'Set-Cookie' header.
    
    """
    
    sessionID = str(uuid.uuid4())
    c = SimpleCookie()
    c[name] = sessionID
    c[name]['path'] = path
    
    #insert entry into database
    cur.execute("""INSERT INTO SESSION(ID, USER_ID) VALUES('%s',   
        %d)""" % (sessionID, value.id))
    con.commit()
    
    # can also set expires and other stuff.  See
    # Examples under http://docs.python.org/library/cookie.html.

    s = c.output()
    (key, value) = s.split(': ')
    return (key, value)

def destroyCookieHeader(id):
    cur.execute("""DELETE FROM SESSION WHERE ID='%s'""" % (id))
    con.commit()
    
    c = SimpleCookie()
    c['username'] = ''
    
    s = c.output()
    (key, value) = s.split(': ')
    return (key, value)
    

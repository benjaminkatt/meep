"""
meeplib - A simple message board back-end implementation.

Functions and classes:

 * u = User(username, password) - creates & saves a User object.  u.id
     is a guaranteed unique integer reference.

 * m = Message(title, post, author) - creates & saves a Message object.
     'author' must be a User object.  'm.id' guaranteed unique integer.

 * get_all_messages() - returns a list of all Message objects.

 * get_all_users() - returns a list of all User objects.

 * delete_message(m) - deletes Message object 'm' from internal lists.

 * delete_user(u) - deletes User object 'u' from internal lists.

 * get_user(username) - retrieves User object for user 'username'.

 * get_message(msg_id) - retrieves Message object for message with id msg_id.

"""

__all__ = ['Message', 'get_all_messages', 'get_message', 'delete_message',
           'User', 'set_current_user', 'get_current_user', 'get_user',
           'get_all_users', 'delete_user', 'is_user']

###
# internal data structures & functions; please don't access these
# directly from outside the module.  Note, I'm not responsible for
# what happens to you if you do access them directly.  CTB

# a dictionary, storing all messages by a (unique, int) ID -> Message object.
_messages = {}


_root_messages= {}


def _get_next_message_id():
    if _messages:
        return max(_messages.keys()) + 1
    return 0

# a dictionary, storing all users by a (unique, int) ID -> User object.
_user_ids = {}

# a dictionary, storing all users by username
_users = {}

#a string that holds the username of the current logged in user
_current_user = ''


def _get_next_user_id():
    if _users:
        #print _users.keys()
 
        return max(_user_ids.keys()) + 1
        
    return 0

def _reset():
    """
    Clean out all persistent data structures, for testing purposes.
    """

    global _messages, _users, _user_ids, _root_messages, current_user

    _messages = {}
    _root_messages = {}
    _users = {}
    _user_ids = {}
    _current_user = ''

###

class Message(object):
    """
    Simple "Message" object, containing title/post/author.

    'author' must be an object of type 'User'.
    
    """
    def __init__(self, title, post, author, parentPostID):
        self.title = title
        self.post = post
        assert isinstance(author, User)
        self.author = author
        self.parentPostID = parentPostID
        self.children = {}
        if parentPostID == -1:
            self._save_message()
            _root_messages[self.id] = self
        else:
            self.id = _get_next_message_id()
            _messages.get(parentPostID).children[self.id] = self
            _messages[self.id] = self

    def _save_message(self):
        self.id = _get_next_message_id()
        
        # register this new message with the messages list:
        _messages[self.id] = self
        
    def __del__(self):
        for c in children:
            del _messages[c.id]
            
        del _messages[msg.id]
        

def build_tree(children):
    tree = []
    for c in children:
        tree.append(c)
        tree += build_tree(c.children.values())
 
    return tree

def get_all_messages():
    return build_tree(_root_messages.values())
    
def get_message(id):
    return _messages[id]

def delete_message(msg):

    if msg.parentPostID == -1:
        del _root_messages[msg.id]
    else:
        del _messages[msg.parentPostID].children[msg.id]


###

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print "user test 1"
        self._save_user()

    def _save_user(self):
        print "save user test2"
        self.id = _get_next_user_id()
        print "save user test3"

        # register new user ID with the users list:
        _user_ids[self.id] = self
        _users[self.username] = self

def set_current_user(username):
    print "----"
    print username
    global _current_user
    _current_user = username
    print _current_user
    print "-----"

def get_current_user():
    print "xxxx"
    print _current_user
    print "xxxx"
    return _current_user

def get_user(username):
    return _users.get(username)         # return None if no such user

def get_all_users():
    return _users.values()

def delete_user(user):
    del _users[user.username]
    del _user_ids[user.id]

def is_user(username, password):
    try:
        thisUser = get_user(username)
        #print 'success1'
    except NameError:
        thisUser = None
        #print 'fail1'

    #print thisUser.password
    #print password
    if thisUser is not None:
        if str(thisUser.password) == str(password):
            #print "true"
            return True
        #print "false1"
    else:
        #print "false2"
        return False
    

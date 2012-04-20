import unittest
import meeplib
import os
import MySQLdb as mdb

# note:
#
# functions start within test_ are discovered and run
#       between setUp and tearDown;
# setUp and tearDown are run *once* for *each* test_ function.

class TestMeepLib(unittest.TestCase):
    def setUp(self):
        try:
            #the backup data causes some of the tests to fail - not sure why
            #remove the backup data before every test
            dbHost = 'localhost'
            dbName = 'meep'
            dbUsername = 'root'
            dbPassword = 'password'
            con = None
            con = mdb.connect(dbHost, dbUsername, dbPassword, dbName)
            cur = con.cursor()
            cur.execute("DELETE FROM MESSAGE")
            cur.execute("DELETE FROM USER")
            meeplib._reset()
            con.commit()  
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        u = meeplib.User('foo', 'bar')
        u.insertIntoDB()
        m = meeplib.Message('the title', 'the content', u.id, -1)
        m.insertIntoDB()
        
    def test_backup_and_load_meep(self):        
        #create a user, and message, then backup, reset data in app
        meeplib.User('admin', 'admin')
        author = meeplib.get_user('admin')
        author.insertIntoDB()
        message = meeplib.Message('title', 'message', author.id, -1)
        message.insertIntoDB()
        
        
        meeplib._reset()
        
        #check that the file exists and contains information about the message and user
        try:
            meeplib._load_backup()
            assert author in meeplib._users.values()
            assert message in meeplib._messages.values()
        except:
            assert False    #the test failed
            
    def test_get_next_message_id(self):
        #there should be 1 message initially created
        assert meeplib._get_next_message_id() == 1
        user = meeplib.User('admin', 'admin')
        user.insertIntoDB()
        author = meeplib.get_user('admin')
        message = meeplib.Message('title', 'message', author.id, -1)
        message.insertIntoDB()
        
        #there should not be two messages
        assert meeplib._get_next_message_id() == 2
        
    def test_get_next_user_id(self):
        #there should be 1 user initially
        assert meeplib._get_next_user_id() == 1
        user = meeplib.User('admin', 'admin')
        user.insertIntoDB()
        #there should be 2 users now
        assert meeplib._get_next_user_id() == 2
        
    def test_reset(self):
        #there should be 1 user and 1 message initially
        assert meeplib._get_next_message_id() == 1
        assert meeplib._get_next_user_id() == 1
        meeplib._reset()
        assert meeplib._get_next_message_id() == 0
        assert meeplib._get_next_user_id() == 0
        
    def test_get_root_messages(self):
        user = meeplib.User('admin', 'admin')
        user.insertIntoDB()
        author = meeplib.get_user('admin')
        message1 = meeplib.Message('title1', 'message1', author.id, -1)
        message1.insertIntoDB()
        message2 = meeplib.Message('title2', 'message2', author.id, -1)
        message2.insertIntoDB()
        message3 = meeplib.Message('title3', 'message3', author.id, 0)
        message3.insertIntoDB()
        
        root_messages = meeplib._get_root_messages()
        assert message1 in root_messages
        assert message2 in root_messages
        assert message3 not in root_messages

    def test_for_message_existence(self):
        x = meeplib.get_all_messages()
        assert len(x) == 1
        assert x[0].title == 'the title'
        assert x[0].post == 'the content'

    def test_message_ownership(self):
        x = meeplib.get_all_users()
        assert len(x) == 1
        u = x[0]

        x = meeplib.get_all_messages()
        assert len(x) == 1
        m = x[0]

        assert m.author == u.id
        
    def test_get_message(self):
        user = meeplib._users['foo']
        assert meeplib.Message('the title', 'the content', user.id, -1) == meeplib._messages[0]
        
    def test_get_user(self):
        assert meeplib._users['foo'] == meeplib.get_user('foo')
        
    def test_get_all_users(self):
        #create one more user, so there are 2 users in total
        user = meeplib.User('foo2', 'bar2')
        user.insertIntoDB()
        assert len(meeplib.get_all_users()) == 2
        
    def test_delete_user(self):
        #check that there is 1 user
        assert len(meeplib.get_all_users()) == 1
        assert len(meeplib._user_ids) == 1
        for msg in meeplib._messages.values():
            meeplib.delete_message(msg)
        meeplib.delete_user(meeplib.get_user('foo'))
        

        #check that there are no users
        assert len(meeplib.get_all_users()) == 0
        assert len(meeplib._user_ids) == 0


    def tearDown(self):
        meeplib._reset()
        dbHost = 'localhost'
        dbName = 'meep'
        dbUsername = 'root'
        dbPassword = 'password'
        con = mdb.connect(dbHost, dbUsername, dbPassword, dbName)
        cur = con.cursor()
        cur.execute("DELETE FROM MESSAGE")
        cur.execute("DELETE FROM USER")
        meeplib._reset()
        con.commit() 
        assert len(meeplib._messages) == 0
        assert len(meeplib._users) == 0
        assert len(meeplib._user_ids) == 0

if __name__ == '__main__':
    unittest.main()

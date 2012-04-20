import twill
import MySQLdb as mdb

def resetDB():
    dbHost = 'localhost'
    dbName = 'meep'
    dbUsername = 'root'
    dbPassword = 'password'
    try:
        con = mdb.connect(dbHost, dbUsername, dbPassword, dbName)
        cur = con.cursor()
        cur.execute("DELETE FROM MESSAGE")
        cur.execute("DELETE FROM USER")
        con.commit()   
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

address = "http://localhost:8000"
twill.execute_file("test_create_user.twill", initial_url=address)
twill.execute_file("test_add_message.twill", initial_url=address)
twill.execute_file("test_create_response.twill", initial_url=address)
twill.execute_file("test_delete_response.twill", initial_url=address)
twill.execute_file("test_initial_login.twill", initial_url=address)
twill.execute_file("test_initial_logout.twill", initial_url=address)
twill.execute_file("test_logged_in_postings.twill", initial_url=address)
twill.execute_file("test_not_logged_in_postings.twill", initial_url=address)
resetDB()

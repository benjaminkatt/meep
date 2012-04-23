import MySQLdb as mdb

dbHost = 'localhost'
dbName = 'meep'
dbUsername = 'root'
dbPassword = 'password'
con = None
cur = None
try:
    con = mdb.connect(dbHost, dbUsername, dbPassword, dbName)
    cur = con.cursor()   
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
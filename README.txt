Important:

Running this requires MySQLdb to be installed in python.
-The MySQL credentials need to be edited in the mysqlConnection.py

Running Instructions:
1. The application requires mysql - to create the required tables run:
	mysql < meep.sql -u <username> -p
2. Run: python serve2.py localhost 8000
3. The application should now be running

Testing Instructions (this will remove all data from the database - this should be tested on a different machine than production):
1. Again, make sure the meep database has been created with the schema provided.
2. The tests require that the database be empty when the application is started. This can be accomplished with:
	DELETE FROM MESSAGE;
	DELETE FROM SESSION;
	DELETE FROM USER;
3. Run in one window: python serve2.py localhost 8000
4. In another window: cd into the source directories and run: nosetests
5. To rerun the tests: stop serve2.py and rerun this section (the database will already be empty after running the tests). 

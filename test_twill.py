import twill
from mysqlConnection import con, cur

def resetDB():
    cur.execute("DELETE FROM SESSION")
    cur.execute("DELETE FROM MESSAGE")
    cur.execute("DELETE FROM USER")
    con.commit()   

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

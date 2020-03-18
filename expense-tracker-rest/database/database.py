import pymysql

class Database:
    def __init__(self):
        host = "localhost"
        user = "docker"
        password = "docker"
        db = "expense_tracker"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
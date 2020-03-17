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


class Users:
    def __init__(self, db):
        self.db = db
        self.table_name = 'user'

    def list_users(self):
        self.db.cur.execute("SELECT * FROM user")
        result = self.db.cur.fetchall()

        return result

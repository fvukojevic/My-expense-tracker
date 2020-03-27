import pymysql
import os

class Database:
    def __init__(self):
        host = 'db'
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        db = os.getenv('MYSQL_DB')
        self.con = pymysql.connect(host=host, port=3306, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
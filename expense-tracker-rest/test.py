from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

class Database:
    def __init__(self):
        host = "localhost"
        user = "docker"
        password = "docker"
        db = "expense_tracker"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def list_employees(self):
        self.cur.execute("SELECT * FROM user")
        result = self.cur.fetchall()

        return result

@app.route('/')
def users():
    def db_query():
        db = Database()
        emps = db.list_employees()
        return emps
    res = db_query()
    return jsonify(res)

if __name__ == '__main__':
    app.run()
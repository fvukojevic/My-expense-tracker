from flask import Flask, jsonify
from database import database

app = Flask(__name__)
db = database.Database()

@app.route('/')
def users():
    def db_query():
        users = database.Users(db).list_users()
        return users
    res = db_query()
    return jsonify(res)

if __name__ == '__main__':
    app.run()
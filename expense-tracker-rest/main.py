from flask import Flask, jsonify, request
from database import database

app = Flask(__name__)
db = database.Database()


@app.route('/users', methods=['GET'])
def users():
    def db_query():
        return database.Users(db).get_users()

    res = db_query()
    return jsonify(res)


@app.route('/users/<identifier>', methods=['GET'])
def user(identifier):
    user_id = None
    user_su = None
    if int(identifier) > 10000: user_su = identifier
    else: user_id = identifier

    def db_query():
        return database.Users(db).get_user(user_id) if user_id is not None else database.Users(db).get_user_by_su(user_su)

    res = db_query()
    return jsonify(res)


@app.route('/users', methods=['POST'])
def store_user():
    def db_query():
        return database.Users(db).store_user(request.json)
    res = db_query()
    return jsonify(res)


if __name__ == '__main__':
    app.run()

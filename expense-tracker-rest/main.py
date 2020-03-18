from flask import Flask, jsonify, request
from database import database
from models.user import User
from models.category import Category

app = Flask(__name__)
db = database.Database()


@app.route('/users', methods=['GET'])
def users():
    def db_query():
        return User(db).get_users()

    res = db_query()
    return jsonify(res)


@app.route('/users/<identifier>', methods=['GET'])
def user(identifier):
    user_id = None
    user_su = None
    if int(identifier) > 10000:
        user_su = identifier
    else:
        user_id = identifier

    def db_query():
        return User(db).get_user(user_id) if user_id is not None \
            else User(db).get_user_by_su(user_su)

    res = db_query()
    return jsonify(res)


@app.route('/users', methods=['POST'])
def store_user():
    def db_query():
        return User(db).store_user(request.json)

    res = db_query()
    return jsonify(res)


@app.route('/categories', methods=['GET'])
def categories():
    def db_query():
        return Category(db).get_categories()

    res = db_query()
    return jsonify(res)


@app.route('/categories/<identifier>', methods=['GET'])
def category(identifier):
    category_id = None
    category_name = None
    try:
        category_id = int(identifier)
    except ValueError:
        category_name = identifier

    def db_query():
        return Category(db).get_category(category_id) if category_id is not None \
            else Category(db).get_category_by_name(category_name)

    res = db_query()
    return jsonify(res)


@app.route('/categories', methods=['POST'])
def store_category():
    def db_query():
        return Category(db).store_category(request.json)

    res = db_query()
    return jsonify(res)


if __name__ == '__main__':
    app.run()

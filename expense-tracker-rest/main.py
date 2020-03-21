import time
from flask import Flask, jsonify, request
from database import database
from models.user import User
from models.category import Category
from models.expense import Expense
from models.user_category import UserCategory

app = Flask(__name__)
db = database.Database()


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


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


@app.route('/user/categories/<identifier>')
def user_categories(identifier):
    def db_query():
        user = User(db).get_user_by_su(identifier)
        user_id = user[0]['id']
        return UserCategory(db).get_user_categories(user_id)

    res = db_query()
    return jsonify(res)


@app.route('/user/categories/<identifier>', methods=['POST'])
def store_user_category(identifier):
    def db_query():
        user = User(db).get_user_by_su(identifier)
        user_id = user[0]['id']
        data = request.json
        data['user_id'] = user_id
        return UserCategory(db).store_user_category(data)

    res = db_query()
    return jsonify(res)


@app.route('/expenses/<identifier>', methods=['GET'])
def expenses(identifier):
    def db_query():
        return Expense(db).get_user_expenses(identifier)

    res = db_query()
    return jsonify(res)


@app.route('/expenses/<identifier>', methods=['POST'])
def expenses_from_to(identifier):
    def db_query():
        data = request.json
        if data is None:
            return Expense(db).get_user_expenses(identifier)
        else:
            if 'start_date' not in data:
                data['start_date'] = '2000-01-01'
            if 'end_date' not in data:
                data['end_date'] = time.strftime('%Y-%m-%d')
            return Expense(db).get_user_expenses_from_to(data, identifier)

    res = db_query()
    return jsonify(res)


@app.route('/expenses', methods=['POST'])
def store_expense():
    def db_query():
        data = request.json
        return Expense(db).store_expense(data)

    res = db_query()
    return jsonify(res)


@app.route('/download/<identifier>', methods=['GET'])
def download(identifier):
    def func():
        return Expense(db).download_expenses(identifier)
    res = func()
    return res


if __name__ == '__main__':
    app.run()

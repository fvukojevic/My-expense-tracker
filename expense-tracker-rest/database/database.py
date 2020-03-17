import pymysql
import json


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

    # Returns ALL users from the database
    def get_users(self):
        self.db.cur.execute(f"SELECT * FROM {self.table_name}")
        users = self.db.cur.fetchall()

        return users

    # Returns a single user by ID
    def get_user(self, user_id):
        self.db.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = {user_id}")
        user = self.db.cur.fetchall()

        return user

    # Returns a single user by SU
    def get_user_by_su(self, user_su):
        self.db.cur.execute(f"SELECT * FROM {self.table_name} WHERE su = {user_su}")
        result = self.db.cur.fetchall()

        return result

    # Stores a user in database
    def store_user(self, data):
        try:
            sql = f"INSERT INTO `{self.table_name}` (`su`, `name`, `email`) VALUES ('{data['SU']}', '{data['Ad']}', '{data['email']}')"
            self.db.cur.execute(sql)
            self.db.con.commit()
            return {'statusCode': 200, 'msg': 'User stored successfully'}
        except KeyError as e:
            return {'statusCode': 500, 'msg': f'Got KeyError - reason {str(e)}'}
        except:
            return {'statusCode': 500, 'msg': 'Whoops. An Error occurred'}

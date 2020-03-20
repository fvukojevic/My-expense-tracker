from .user import User
from .category import Category
from .user_category import UserCategory
import time

class Expense:
    def __init__(self, db):
        self.db = db
        self.table_name = 'expense'
        self.user_table = 'user'
        self.category_table = 'category'
        self.user_category_table = 'user_category'

    # Returns ALL expenses from a specific user from the database
    def get_user_expenses(self, user_identifier):
        category_sql = f"SELECT SUM(ex.amount) as amount, u.name AS user_name, c.name AS category_name \
                FROM {self.table_name} AS ex \
                INNER JOIN {self.user_table} AS u ON u.id = ex.fk_user \
                INNER JOIN {self.category_table} AS c ON c.id = ex.fk_category \
                WHERE u.su = {user_identifier} \
                GROUP BY category_name, user_name"
        user_category_sql = f"SELECT SUM(ex.amount) as amount, u.name AS user_name, uc.name AS category_name \
                FROM {self.table_name} AS ex \
                INNER JOIN {self.user_table} AS u ON u.id = ex.fk_user \
                INNER JOIN {self.user_category_table} AS uc ON uc.id = ex.fk_user_category \
                WHERE u.su = {user_identifier} \
                GROUP BY category_name, user_name"
        self.db.cur.execute(category_sql)
        user_expenses = self.db.cur.fetchall()
        self.db.cur.execute(user_category_sql)
        if type(user_expenses) is tuple:
            user_expenses = self.db.cur.fetchall()
        else:
            user_expenses.extend(self.db.cur.fetchall())
        return user_expenses

    # Returns expenses from - to date
    def get_user_expenses_from_to(self, data, user_identifier):
        category_sql = f"SELECT SUM(ex.amount) as amount, u.name AS user_name, c.name AS category_name \
            FROM {self.table_name} AS ex \
            INNER JOIN {self.user_table} u ON u.id = ex.fk_user \
            INNER JOIN {self.category_table} c ON c.id = ex.fk_category \
            WHERE ex.`created_at` >= '{data['start_date']}' AND ex.`created_at` <= '{data['end_date']}' \
            AND u.su = {user_identifier} \
            GROUP BY user_name, category_name"
        user_category_sql = f"SELECT SUM(ex.amount) as amount, u.name AS user_name, uc.name AS category_name \
                    FROM {self.table_name} AS ex \
                    INNER JOIN {self.user_table} u ON u.id = ex.fk_user \
                    INNER JOIN {self.user_category_table} uc ON uc.id = ex.fk_user_category \
                    WHERE ex.`created_at` >= '{data['start_date']}' AND ex.`created_at` <= '{data['end_date']}' \
                    AND u.su = {user_identifier} \
                    GROUP BY user_name, category_name"
        self.db.cur.execute(category_sql)
        user_expenses = self.db.cur.fetchall()
        self.db.cur.execute(user_category_sql)
        if type(user_expenses) is tuple:
            user_expenses = self.db.cur.fetchall()
        else:
            user_expenses.extend(self.db.cur.fetchall())
        return user_expenses

    # Stores an expense in database
    def store_expense(self, data):
        user = User(self.db).get_user_by_su(data['SU'])[0]
        user_id = user['id']
        category = Category(self.db).get_category_by_name(data['name'])
        user_category = UserCategory(self.db).get_user_category_by_name(data['name'])
        created_at = time.strftime('%Y-%m-%d')
        if category:
            sql = f"INSERT INTO `{self.table_name}` (`amount`, `created_at`, `fk_category`, `fk_user`)" \
                  f" VALUES ('{data['amount']}', '{created_at}', {category[0]['id']} ,{user_id})"
            self.db.cur.execute(sql)
            self.db.con.commit()
            return {'statusCode': 200, 'msg': 'Expense stored successfully'}
        elif user_category:
            sql = f"INSERT INTO `{self.table_name}` (`amount`, `created_at`, `fk_user_category`, `fk_user`)" \
                  f" VALUES ('{data['amount']}', '{created_at}', {user_category[0]['id']} ,{user_id})"
            self.db.cur.execute(sql)
            self.db.con.commit()
            return {'statusCode': 200, 'msg': 'Expense stored successfully'}
        else:
            return {'statusCode': 500, 'msg': 'Something went wrong'}

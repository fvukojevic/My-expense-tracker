import urllib.request
from .user import User
from .category import Category
from .user_category import UserCategory
import time
import pandas as pd
import os
from pathlib import Path

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

    def get_raw_user_expenses(self, user_identifier):
        query = f'SELECT amount, created_at, c.name as category_name, uc.name as category_name \
                  FROM {self.table_name} ex \
                  LEFT JOIN {self.category_table} c ON c.id = ex.fk_category \
                  LEFT JOIN {self.user_category_table} uc on uc.id = ex.fk_user_category \
                  LEFT JOIN {self.user_table} u on u.id = ex.fk_user \
                  WHERE u.su = {user_identifier} AND created_at IS NOT NULL \
                  UNION \
                  SELECT amount, created_at, c.name as category_name, uc.name as category_name \
                  FROM {self.table_name} ex \
                  RIGHT JOIN {self.category_table} c ON c.id = ex.fk_category \
                  RIGHT JOIN {self.user_category_table} uc on uc.id = ex.fk_user_category \
                  RIGHT JOIN {self.user_table} u on u.id = ex.fk_user \
                  WHERE u.su = {user_identifier} AND created_at IS NOT NULL \
                  ORDER BY created_at ASC;'
        self.db.cur.execute(query)
        user_expenses = self.db.cur.fetchall()
        return user_expenses

    def download_expenses(self, user_identifier):
        user_expenses = self.get_raw_user_expenses(user_identifier)
        hash_expense = create_hash_list_for_excel(user_expenses)

        # data frame for hash_expense dictionary
        df = pd.DataFrame(hash_expense)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(str(os.path.join(Path.home(), 'Downloads/demo.xlsx')), engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Expenses', index=False)

        worksheet = writer.sheets['Expenses']
        # Add conditional formatting for Age column
        workbook = writer.book
        header = workbook.add_format({'bg_color': 'yellow'})
        money = workbook.add_format({'num_format': '$#,##0'})
        total = workbook.add_format({'bg_color': '#90ee90',
                                     'bold': True})

        worksheet.conditional_format(0, 0, 0, 10, {'type': 'no_blanks', 'format': header})
        worksheet.conditional_format(len(hash_expense), len(hash_expense) - 1, 0, 10, {'type': 'no_blanks', 'format': money})
        worksheet.conditional_format(len(hash_expense), len(hash_expense) - 1, len(hash_expense), 10,
                                     {'type': 'no_blanks', 'format': total})
        width = 15
        worksheet.set_column(0, 0, width)
        # Close writer
        writer.save()
        writer.close()

        return {'statusCode': 200, 'msg': 'File Created successfully'}


def create_hash_list_for_excel(user_expenses):
    print(user_expenses)
    category_names = []
    hash_expenses = {'Date': []}
    for expense in user_expenses:
        if expense['category_name'] is not None:
            if expense['category_name'] not in category_names:
                category_names.append(expense['category_name'])
                hash_expenses[expense['category_name']] = []
        else:
            if expense['.category_name'] not in category_names:
                category_names.append(expense['.category_name'])
                hash_expenses[expense['.category_name']] = []
    hash_expenses['Total'] = []
    index = -1
    for expense in user_expenses:
        formatted_time = expense['created_at'].strftime('%Y-%m-%d')
        if formatted_time not in hash_expenses['Date']:
            hash_expenses['Date'].append(formatted_time)
            index += 1
        total = 0
        for category in category_names:
            if expense['category_name'] == category:
                try:
                    if hash_expenses[category][index] is not None:
                        hash_expenses[category][index] += expense['amount']
                    else:
                        hash_expenses[category][index] = expense['amount']
                except IndexError:
                    hash_expenses[category].append(expense['amount'])
            else:
                try:
                    if hash_expenses[category][index] is not None:
                        hash_expenses[category][index] += 0
                except IndexError:
                    hash_expenses[category].append(None)
            if hash_expenses[category][index] is not None:
                total += hash_expenses[category][index]
        try:
            hash_expenses['Total'][index] = total
        except IndexError:
            hash_expenses['Total'].append(total)

    for key in hash_expenses:
        if key != 'Total':
            hash_expenses[key].append(None)
    hash_expenses['Total'].append(sum(hash_expenses['Total']))

    return hash_expenses

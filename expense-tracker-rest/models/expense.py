class Expense:
    def __init__(self, db):
        self.db = db
        self.table_name = 'expense'
        self.user_table = 'user'
        self.category_table = 'category'

    # Returns ALL expenses from a specific user from the database
    def get_user_expenses(self, user_identifier):
        sql = f"SELECT SUM(ex.amount), u.name AS user_name, c.name AS category_name FROM {self.table_name} AS ex \
                INNER JOIN {self.user_table} AS u ON u.id = ex.fk_user \
                INNER JOIN {self.category_table} AS c ON c.id = ex.fk_category \
                WHERE u.su = {user_identifier} \
                GROUP BY category_name, user_name"
        print(sql)
        self.db.cur.execute(sql)
        user_expenses = self.db.cur.fetchall()
        print(user_expenses)
        return user_expenses

    # Returns expenses from/to date
    def get_user_expenses_from_to(self, user_id):
        pass

    # Stores an expense in database
    def store_expense(self, data):
        pass

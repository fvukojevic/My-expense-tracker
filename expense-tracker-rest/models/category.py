class Category:
    def __init__(self, db):
        self.db = db
        self.table_name = 'category'

    # Returns ALL categories from the database
    def get_categories(self):
        self.db.cur.execute(f"SELECT * FROM {self.table_name}")
        categories = self.db.cur.fetchall()

        return categories

    # Returns a single category by ID
    def get_category(self, category_id):
        self.db.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = {category_id}")
        category = self.db.cur.fetchall()

        return category

    # Returns a single category by name
    def get_category_by_name(self, category_name):
        self.db.cur.execute(f"SELECT * FROM {self.table_name} WHERE name = '{category_name}'")
        category = self.db.cur.fetchall()

        return category

    # Stores a category in database
    def store_category(self, data):
        try:
            sql = f"INSERT INTO `{self.table_name}` (`name`) VALUES ('{data['name']}')"
            self.db.cur.execute(sql)
            self.db.con.commit()
            return {'statusCode': 200, 'msg': 'Category stored successfully'}
        except KeyError as e:
            return {'statusCode': 500, 'msg': f'Got KeyError - reason {str(e)}'}
        except:
            return {'statusCode': 500, 'msg': 'Whoops. An Error occurred'}

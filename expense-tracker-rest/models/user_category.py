class UserCategory:
    def __init__(self, db):
        self.db = db
        self.table_name = 'user_category'

    # Returns ALL categories from the database
    def get_user_categories(self, fk_user):
        self.db.cur.execute(f"SELECT * FROM {self.table_name} WHERE fk_user = {fk_user}")
        categories = self.db.cur.fetchall()

        return categories

    # Stores a category in database
    def store_user_category(self, data):
        try:
            self.db.cur.execute(f"SELECT * FROM {self.table_name} WHERE fk_user = {data['user_id']} AND name = ('{data['name']}')")
            category = self.db.cur.fetchall()
            if not category:
                sql = f"INSERT INTO `{self.table_name}` (`name`, `fk_user`) VALUES ('{data['name']}', {data['user_id']})"
                self.db.cur.execute(sql)
                self.db.con.commit()
                return {'statusCode': 200, 'msg': 'Custom category stored successfully'}
            else:
                return {'statusCode': 500, 'msg': 'Custom category already exist'}
        except KeyError as e:
            return {'statusCode': 500, 'msg': f'Got KeyError - reason {str(e)}'}
        except:
            return {'statusCode': 500, 'msg': 'Whoops. An Error occurred'}

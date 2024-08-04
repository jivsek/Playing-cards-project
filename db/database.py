import sqlite3

class Database:
    def __init__(self, db_name='cards.db'):
        self.db_name = db_name

    def execute_query(self, query, params=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
        
    def execute_many(self, query, params_list):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()

    def fetch_query(self, query, params=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    
from db.database import Database
from faker import Faker

class Zbiratelj(Database):
    def __init__(self, db_name='cards.db'):
        super().__init__(db_name)
        self.fake = Faker()
    
    def create_table(self):
        self.execute_query("DROP TABLE IF EXISTS ZBIRATELJ")
        create_table_query = """ CREATE TABLE ZBIRATELJ(
                id_zbiratelj INTEGER PRIMARY KEY,
                ime VARCHAR(255) NOT NULL,
                priimek VARCHAR(255) NOT NULL,
                eposta VARCHAR(255)
                );
                """
        self.execute_query(create_table_query)
    
    def insert_data(self, ime, priimek, eposta):
        insert_query = '''
        INSERT INTO ZBIRATELJ (ime, priimek, eposta)
        VALUES (?, ?, ?)
        '''
        self.execute_query(insert_query, (ime, priimek, eposta))

    def generate_fake_data(self, num_entries=30):
        for _ in range(num_entries):
            ime = self.fake.first_name()
            priimek = self.fake.last_name()
            eposta = self.fake.email()
            self.insert_data(ime, priimek, eposta)

    @classmethod
    def get_all(cls):
        result = Database().fetch_query('SELECT * FROM ZBIRATELJ')
        
        collectors = []
        for row in result:
            collector = {
                'id_zbiratelj': row[0],
                'ime': row[1],
                'priimek': row[2],
                'eposta': row[3]
            }
            collectors.append(collector)
            
        return collectors

    @classmethod
    def get_by_id(cls, id_zbiratelj):
        query = 'SELECT * FROM ZBIRATELJ WHERE id_zbiratelj = ?'
        result = Database().fetch_query(query, (id_zbiratelj,))[0]
        
        collector = {
            'id_zbiratelj': result[0],
            'ime': result[1],
            'priimek': result[2],
            'eposta': result[3]
        }
            
        return collector

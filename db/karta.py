from .database import Database

class Karta(Database):
    def __init__(self, db_name='cards.db'):
        super().__init__(db_name)
    
    def create_table(self):
        self.execute_query("DROP TABLE IF EXISTS KARTA")
        create_table_query = """ CREATE TABLE KARTA(
                id_karta INTEGER PRIMARY KEY,
                ime VARCHAR(255) NOT NULL,
                zaloga INT NOT NULL,
                cena INT NOT NULL,
                slika VARCHAR(255) NOT NULL
                );
                """
        self.execute_query(create_table_query)
    
    def insert_data(self, product_name, availability, price, img_src):
        insert_query = '''
        INSERT INTO KARTA (ime, zaloga, cena, slika)
        VALUES (?, ?, ?, ?)
        '''
        self.execute_query(insert_query, (product_name, availability, price, img_src))

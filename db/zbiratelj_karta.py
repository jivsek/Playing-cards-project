from .database import Database
import random

class ZbirateljKarta(Database):
    def __init__(self, db_name='cards.db'):
        super().__init__(db_name)
    
    def create_table(self):
        self.execute_query("""DROP TABLE IF EXISTS ZBIRATELJ_KARTA""")
        create_table_query = """ CREATE TABLE IF NOT EXISTS ZBIRATELJ_KARTA (
                id INTEGER PRIMARY KEY,
                id_zbiratelj INTEGER,
                id_karta INTEGER,
                FOREIGN KEY (id_zbiratelj) REFERENCES ZBIRATELJ (id_zbiratelj),
                FOREIGN KEY (id_karta) REFERENCES KARTA (id_karta)
                );
                """
        self.execute_query(create_table_query)
    
    def insert_data(self, id_zbiratelj, id_karta):
        insert_query = '''
        INSERT INTO COLLECTOR_CARDS (id_zbiratelj, id_karta)
        VALUES (?, ?)
        '''
        self.execute_query(insert_query, (id_zbiratelj, id_karta))
    
    def populate_table(self, num_cards, num_collectors):
        card_collector = [(random.randint(1, num_collectors), card_id) for card_id in range(1, num_cards + 1)]
        insert_query = "INSERT INTO ZBIRATELJ_KARTA (id_zbiratelj, id_karta) VALUES (?, ?)"
        self.execute_many(insert_query, card_collector)
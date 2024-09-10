from db.database import Database

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
                slika VARCHAR(255)
                );
                """
        self.execute_query(create_table_query)
    
    def insert_data(self, ime, zaloga, cena, slika):
        insert_query = '''
        INSERT INTO KARTA (ime, zaloga, cena, slika)
        VALUES (?, ?, ?, ?)
        '''
        self.execute_query(insert_query, (ime, zaloga, cena, slika))

    @classmethod
    def get_all(cls, sort_by, order):
        query = f"SELECT * FROM KARTA ORDER BY {sort_by} {order}"
        conn = Database().fetch_query(query)
        
        cards = []
        for row in conn:
            card = {
                'id_karta': row[0],
                'ime': row[1],
                'zaloga': row[2],
                'cena': row[3],
                'slika': row[4]
            }
            cards.append(card)
        return cards
    
    @classmethod
    def get_all_name(cls, search_term):
        search_term = '%' + search_term + '%'
        conn = Database().fetch_query(f'SELECT * FROM KARTA WHERE ime LIKE ?', 
                             ('%' + search_term + '%',))
        
        cards = []
        for row in conn:
            card = {
                'id_karta': row[0],
                'ime': row[1],
                'zaloga': row[2],
                'cena': row[3],
                'slika': row[4]
            }
            cards.append(card)
        return cards

    @classmethod
    def get_by_collector(cls, id_zbiratelj):
        query = '''
            SELECT KARTA.* FROM KARTA
            JOIN ZBIRATELJ_KARTA ON KARTA.id_karta = ZBIRATELJ_KARTA.id_karta
            WHERE ZBIRATELJ_KARTA.id_zbiratelj = ?
        '''
        result = Database().fetch_query(query, (id_zbiratelj,))
        cards = []
        for row in result:
            card = {
                'id_karta': row[0],
                'ime': row[1],
                'zaloga': row[2],
                'cena': row[3],
                'slika': row[4]
            }
            cards.append(card)
        return cards

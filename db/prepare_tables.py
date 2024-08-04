from db.zbiratelj import Zbiratelj
from db.karta import Karta

def prepare_tables():
    
    karta = Karta()
    karta.create_table()
    
    zbiratelj = Zbiratelj()
    zbiratelj.create_table()
    zbiratelj.generate_fake_data(30)
    
    print("Created table Karta and Zbiratelj")


if __name__=="__main__":
    prepare_tables()
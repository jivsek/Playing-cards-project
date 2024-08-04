from db.zbiratelj import Zbiratelj
from db.karta import Karta
from db.zbiratelj_karta import ZbirateljKarta

def prepare_tables():
    
    karta = Karta()
    karta.create_table()
    print("Created table Karta")
    
    zbiratelj = Zbiratelj()
    zbiratelj.create_table()
    print("Created table Zbiratelj")
    
    zbiratelj_karta = ZbirateljKarta()
    zbiratelj_karta.create_table()
    print("Created table Zbiratelj_Karta")


if __name__=="__main__":
    prepare_tables()
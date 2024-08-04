from db.zbiratelj import Zbiratelj
from db.zbiratelj_karta import ZbirateljKarta

def populate_tables():
    
    zbiratelj = Zbiratelj()
    n = 30
    zbiratelj.generate_fake_data(n)
    print(f"Populated table Zbiratelj: {n} entries")
    
    zbiratelj_karta = ZbirateljKarta()
    zbiratelj_karta.populate_table(280, n)
    print("Populated table Zbiratelj_Karta")
    
if __name__=="__main__":
    populate_tables()
from database import Database

db = Database()

result = db.fetch_query("SELECT COUNT(*) FROM KARTA")
print("Number of rows in KARTA:", result[0][0])

result = db.fetch_query("SELECT COUNT(*) FROM ZBIRATELJ")
print("Number of rows in ZBIRATELJ:", result[0][0])

result = db.fetch_query("SELECT COUNT(*) FROM ZBIRATELJ_KARTA")
print("Number of rows in ZBIRATELJ_KARTA:", result[0][0])

result = db.fetch_query("SELECT * FROM ZBIRATELJ_KARTA")
print(result)
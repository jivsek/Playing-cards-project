from db.prepare_tables import prepare_tables
from scraper.scraper import scrape_data

if __name__=="__main__":
    prepare_tables()
    scrape_data()
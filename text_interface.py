import sys
from models.karta import Karta
from models.zbiratelj import Zbiratelj
from models.zbiratelj_karta import ZbirateljKarta

def display_menu():
    print("\n--- Card Database ---")
    print("Izberi opcijo:")
    print("1. Prikaži vse karte")
    print("2. Poišči karto po imenu")
    print("3. Dodaj novo karto")
    print("4. Prikaži vse zbiratelje")
    print("5. Prikaži karte od zbiratelja")
    print("6. Prenesi karto na drugega zbiratelja")
    print("7. Zapri program")

def show_all_cards():
    cards = Karta.get_all(sort_by="id_karta", order="asc")
    print(cards)
    for card in cards:
        print(f"{card["id_karta"]}. {card["ime"]} | Zaloga: {card["zaloga"]} | Cena: {card["cena"]} | Slika: {card["slika"]}")

def search_card():
    name = input("Vnesi ime karte: ")
    cards = Karta.get_all_name(name)
    if cards:
        for card in cards:
            print(f"{card["id_karta"]}. {card["ime"]} | Zaloga: {card["zaloga"]} | Cena: {card["cena"]} | Slika: {card["slika"]}")
    else:
        print("Karta ni bila najdena.")

def add_new_card():
    name = input("Vnesi ime karte: ")
    availability = input("Vnesi zalogo: ")
    price = input("Vnesi ceno: ")
    image_url = input("Vnesi URL slike: ")

    if name and availability and price:
        Karta().insert_data(name, availability, price, image_url)
        print(f"Karta {name} je bila uspešno dodana.")
    else:
        print("Vsi podatki so obvezni.")

def show_all_collectors():
    collectors = Zbiratelj.get_all()
    for collector in collectors:
        print(f"{collector["id_zbiratelj"]}. {collector["ime"]} {collector["priimek"]} | E-pošta: {collector["eposta"]}")

def show_collectors_cards():
    show_all_collectors()
    collector_id = int(input("\nVnesi ID zbiratelja: "))
    
    cards = Karta.get_by_collector(collector_id)
    if cards:
        for card in cards:
            print(f"{card["id_karta"]}. {card["ime"]} | Zaloga: {card["zaloga"]} | Cena: {card["cena"]} | Slika: {card["slika"]}")
    else:
        print("Zbiratelj nima nobene karte.")

def transfer_card():
    show_all_cards()
    card_id = int(input("\nVnesi ID karte za prenos: "))
    show_all_collectors()
    new_collector_id = int(input("\nVnesi ID novega zbiratelja: "))

    result = ZbirateljKarta().transfer_card(card_id, new_collector_id)
    if result:
        print(result)
    else:
        print("Karta je bila uspešno prenesena.")

def main():
    while True:
        display_menu()
        choice = input("Vnesite izbiro: ")

        if choice == "1":
            show_all_cards()
        elif choice == "2":
            search_card()
        elif choice == "3":
            add_new_card()
        elif choice == "4":
            show_all_collectors()
        elif choice == "5":
            show_collectors_cards()
        elif choice == "6":
            transfer_card()
        elif choice == "7":
            print("Zapiranje programa.")
            sys.exit()
        else:
            print("Neveljavna izbira.")

if __name__ == "__main__":
    main()

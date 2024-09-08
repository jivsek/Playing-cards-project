# Podatkovne baze 1 - Playing cards project

Ta projekt iz spletne strani https://www.cardmarket.com/en/Pokemon/Products/Singles?idCategory=51&idExpansion=0&idRarity=0 pobere vse igralne karte in jih shrani v bazo. Potem generira 30 fake zbirateljev in naključno generira relacije med karto in zbirateljem.
Na spletni strani potem prikaže seznam vseh kart, zbirateljev ter karte v njihovi lasti. Prav tako pa so dodane funkcije dodajanje kart, iskanje po imenu karte, sortiranje kart po imenu, ceni itd. Dodana je tudi funkcija za prenos karte med zbiratelji.

## Kako pognati projekt

1. Priporočljivo: ustvari virtualenv `python -m venv venv` in ga aktiviraj `.\venv\Scripts\activate`
2. Naloži vse potrebne pakete `pip install -r requirements.txt`
3. Poženi `main.py`. Ta pripravi tabele, scrape-a in generira podatke ter zapolni tabele.
4. Poženi `app.py`

Spletna stran na `http://127.0.0.1:5000`


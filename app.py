from flask import Flask, render_template, request, redirect, url_for, flash
from models.karta import Karta
from models.zbiratelj import Zbiratelj
from models.zbiratelj_karta import ZbirateljKarta

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'moj_tajni_kljuc_za_sesije'

karta = Karta()
zbiratelj = Zbiratelj()
zbiratelj_karta = ZbirateljKarta()

@app.route('/')
def index():
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort_by')
    if not sort_by:
        sort_by = "ime"
    order = request.args.get('order')
    if not order:
        order = "asc"
    
    if search_term:
        cards = karta.get_all_name(search_term)
    else:
        cards = karta.get_all(sort_by, order)
    return render_template('index.html', cards=cards)

@app.route('/collectors')
def collectors():
    collectors = zbiratelj.get_all()
    return render_template('collectors.html', collectors=collectors)

@app.route('/collector/<int:id>')
def collector(id):
    collector = zbiratelj.get_by_id(id)
    cards = karta.get_by_collector(id)
    return render_template('collector.html', collector=collector, cards=cards)

@app.route('/transfer_card', methods=['POST'])
def transfer_card():
    card_id = request.form.get('card_id')
    new_collector_id = request.form.get('new_collector_id')

    if not card_id or not new_collector_id:
        flash("Napaka: Karta ali zbiratelj ni bil izbran.")
        return redirect(request.referrer)

    zbiratelj_karta.transfer_card(card_id, new_collector_id)
    flash("Karta je bila uspešno prenesena.")
    return redirect(request.referrer)

@app.route('/add_card', methods=['POST'])
def add_card():
    product_name = request.form['product_name']
    availability = request.form['availability']
    price = request.form['price']
    img_src = request.form['img_src']

    if product_name and availability and price:
        karta.insert_data(product_name, availability, price, img_src)
        flash("Karta je bila uspešno dodana.")
        return redirect(url_for('index'))
    else:
        return "Napaka: Manjkajo obvezni podatki."
    

@app.route('/proxy-image')
def proxy_image():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)

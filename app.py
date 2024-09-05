from flask import Flask, render_template, request, send_file, abort, redirect, url_for, flash
import sqlite3
import requests
from io import BytesIO
from db.karta import Karta

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'moj_tajni_kljuc_za_sesije'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

COOKIES = {
    'PHPSESSID': '5os2qocc94kb2lbgrscr6srngb',
    '_cfuvid': 'ssSeDVwP8Jk.JN8Y6Ol4m6ucR6CPLzBsY4yrpjx5f7Q-1722074177563-0.0.1.1-604800000',
    '_ga': 'GA1.1.1437496798.1700832934',
    '_ga_G8GDQ4EM48': 'GS1.1.1703331270.4.0.1703331270.60.0.0',
    '_uetvid': '582011708ace11eeb0a3832f890ef2f0',
    '_vwo_ssm': '1',
    '_vwo_uuid': 'D0981BE1E635AAD15FDFB71848A9DC9C3',
    '_vwo_uuid_v2': 'DF3214716F6CBCD56121DA444A1E9DDA7',
    'cookie_settings': 'preferences%3D1%2Cstatistics%3D1%2Cmarketing%3D1'
}

def get_db_connection():
    conn = sqlite3.connect('cards.db')
    conn.row_factory = sqlite3.Row
    return conn

karta = Karta()

@app.route('/')
def index():
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')
    
    if sort_by not in ['ime', 'zaloga', 'cena']:
        sort_by = 'ime'
    if order not in ['asc', 'desc']:
        order = 'asc'
        
    
    conn = get_db_connection()
    if search_term:
        cards = conn.execute(f'SELECT * FROM KARTA WHERE ime LIKE ? ORDER BY {sort_by} {order}', 
                             ('%' + search_term + '%',)).fetchall()
    else:
        cards = conn.execute(f'SELECT * FROM KARTA ORDER BY {sort_by} {order}').fetchall()
    conn.close()
    return render_template('index.html', cards=cards, sort_by=sort_by, order=order)

@app.route('/collectors')
def collectors():
    conn = get_db_connection()
    collectors = conn.execute('SELECT * FROM ZBIRATELJ').fetchall()
    conn.close()
    return render_template('collectors.html', collectors=collectors)

@app.route('/collector/<int:id>')
def collector(id):
    conn = get_db_connection()
    collector = conn.execute('SELECT * FROM ZBIRATELJ WHERE id_zbiratelj = ?', (id,)).fetchone()
    cards = conn.execute('''
        SELECT KARTA.* FROM KARTA
        JOIN ZBIRATELJ_KARTA ON KARTA.id_karta = ZBIRATELJ_KARTA.id_karta
        WHERE ZBIRATELJ_KARTA.id_zbiratelj = ?
    ''', (id,)).fetchall()
    conn.close()
    return render_template('collector.html', collector=collector, cards=cards)

@app.route('/transfer_card', methods=['POST'])
def transfer_card():
    card_id = request.form.get('card_id')
    new_collector_id = request.form.get('new_collector_id')

    if not card_id or not new_collector_id:
        flash("Napaka: Karta ali zbiratelj ni bil izbran.")
        return redirect(request.referrer)

    try:
        conn = get_db_connection()
        
        # Preveri, kateri je trenutni zbiratelj karte
        current_relation = conn.execute('SELECT * FROM ZBIRATELJ_KARTA WHERE id_karta = ?', (card_id,)).fetchone()
        
        # Preveri, če prejemnik karte obstaja
        collector_exist = conn.execute('SELECT * FROM ZBIRATELJ WHERE id_zbiratelj = ?', (new_collector_id,)).fetchone()
        
        #Preveri, če karta obstaja
        card_exist = conn.execute('SELECT * FROM KARTA WHERE id_karta = ?', (card_id,)).fetchone()
        
        if not card_exist:
            flash("The card does not exist!")
        if not collector_exist:
            flash("The collector does not exist!")
        if card_exist and current_relation and collector_exist:
            current_collector_id = current_relation['id_zbiratelj']
            
            # Posodobi tabelo ZBIRATELJ_KARTA
            conn.execute('UPDATE ZBIRATELJ_KARTA SET id_zbiratelj = ? WHERE id_karta = ?', (new_collector_id, card_id))
            flash("The card was successfully transfered!")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        flash(f"Error: {e}")
    
    return redirect(request.referrer)

@app.route('/add_card', methods=['POST'])
def add_card():
    product_name = request.form['product_name']
    availability = request.form['availability']
    price = request.form['price']
    img_src = request.form['img_src']

    if product_name and availability and price:
        karta.insert_data(product_name, availability, price, img_src)
        flash("The card was successfully added!")
        return redirect(url_for('index'))
    else:
        return "Error: All fields except 'Image URL' are required."

@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        abort(404)

    cookies = {
        'PHPSESSID': '5os2qocc94kb2lbgrscr6srngb',
        '_cfuvid': 'ssSeDVwP8Jk.JN8Y6Ol4m6ucR6CPLzBsY4yrpjx5f7Q-1722074177563-0.0.1.1-604800000',
        '_ga': 'GA1.1.1437496798.1700832934',
        '_ga_G8GDQ4EM48': 'GS1.1.1703331270.4.0.1703331270.60.0.0',
        '_uetvid': '582011708ace11eeb0a3832f890ef2f0',
        '_vwo_ssm': '1',
        '_vwo_uuid': 'D0981BE1E635AAD15FDFB71848A9DC9C3',
        '_vwo_uuid_v2': 'DF3214716F6CBCD56121DA444A1E9DDA7',
        'cookie_settings': 'preferences%3D1%2Cstatistics%3D1%2Cmarketing%3D1'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    try:
        response = requests.get(image_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        return send_file(BytesIO(response.content), mimetype='image/jpeg')
    except requests.RequestException as e:
        print(f"Error fetching image from {image_url}: {e}")
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)

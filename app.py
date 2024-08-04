from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cards.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cards = conn.execute('SELECT * FROM KARTA').fetchall()
    conn.close()
    return render_template('index.html', cards=cards)

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

if __name__ == '__main__':
    app.run(debug=True)
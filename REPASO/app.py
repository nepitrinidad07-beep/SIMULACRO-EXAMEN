from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = 'gestion_it.db'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Inicialización de la base de datos (Las 4 entidades)
with sqlite3.connect(DB_PATH) as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS dispositivos (id INTEGER PRIMARY KEY, nombre TEXT, ip TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS ubicaciones (id INTEGER PRIMARY KEY, sala TEXT, rack TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS software (id INTEGER PRIMARY KEY, nombre TEXT, version TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT, puesto TEXT)')

@app.route('/')
def index():
    context = {
        "dispositivos": query_db('SELECT * FROM dispositivos'),
        "ubicaciones": query_db('SELECT * FROM ubicaciones'),
        "software": query_db('SELECT * FROM software'),
        "usuarios": query_db('SELECT * FROM usuarios')
    }
    return render_template('index.html', **context)

@app.route('/add/<tabla>', methods=['POST'])
def add(tabla):
    if tabla == 'dispositivos':
        query_db('INSERT INTO dispositivos (nombre, ip) VALUES (?, ?)', [request.form['val1'], request.form['val2']])
    elif tabla == 'ubicaciones':
        query_db('INSERT INTO ubicaciones (sala, rack) VALUES (?, ?)', [request.form['val1'], request.form['val2']])
    elif tabla == 'software':
        query_db('INSERT INTO software (nombre, version) VALUES (?, ?)', [request.form['val1'], request.form['val2']])
    elif tabla == 'usuarios':
        query_db('INSERT INTO usuarios (nombre, puesto) VALUES (?, ?)', [request.form['val1'], request.form['val2']])
    return redirect(url_for('index'))

@app.route('/delete/<tabla>/<int:id>')
def delete(tabla, id):
    query_db(f'DELETE FROM {tabla} WHERE id = ?', [id])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
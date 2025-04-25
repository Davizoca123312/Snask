from flask import Flask, render_template, g, request, redirect, url_for, Response, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'libs.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        exists = os.path.exists(DATABASE)
        db = g._database = sqlite3.connect(DATABASE)
        if not exists:
            with app.app_context():
                init_db()
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT NOT NULL,
            code TEXT NOT NULL
        )
    ''')
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, description FROM libraries')
    libs = cursor.fetchall()
    return render_template('index.html', libraries=libs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        description = request.form['description']
        code = request.form['code']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO libraries (name, author, description, code) VALUES (?, ?, ?, ?)',
                       (name, author, description, code))
        db.commit()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/lib/<int:lib_id>')
def view(lib_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, author, description FROM libraries WHERE id=?', (lib_id,))
    lib = cursor.fetchone()
    if lib:
        return render_template('view.html', lib=lib, lib_id=lib_id)
    return "Biblioteca não encontrada", 404

# 🆕 Rota de download da biblioteca
@app.route('/download/<name>')
def download(name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT code FROM libraries WHERE name=?', (name,))
    row = cursor.fetchone()
    if row:
        return Response(row[0], mimetype='text/plain')
    return "Biblioteca não encontrada", 404

# 🆕 Rota para snaskget.py (formato JSON)
@app.route('/api/lib/<string:name>')
def api_lib(name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT code FROM libraries WHERE name=?', (name,))
    result = cursor.fetchone()
    if result:
        return jsonify({'code': result[0]})
    return jsonify({'error': 'Biblioteca não encontrada'}), 404
from flask import send_file

# 🆕 Rota para baixar o instalador completo do Snask (.rar)
@app.route('/download/font')
def download_font():
    rar_path = "C:/Users/User/Desktop/Snask/chat/Site/snask.zip"  # arquivo deve estar na raiz do projeto
    if os.path.exists(rar_path):
        return send_file(rar_path, as_attachment=True)
    
    return "Arquivo snask.rar não encontrado", 404
    
if __name__ == '__main__':
    app.run(debug=True)

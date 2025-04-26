from flask import Flask, render_template, g, request, redirect, url_for, Response, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'libs.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        
            
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


from flask import send_file

@app.route('/download/installer')
def download_installer():
    installer_path = os.path.join('templates', 'installer.exe')
    if os.path.exists(installer_path):
        return send_file(installer_path, as_attachment=True)
    return "Arquivo installer.exe não encontrado", 404

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

# 🆕 Rota para baixar o instalador completo do Snask (.zip)
@app.route('/download/font')
def download_font():
    zip_path = os.path.join(app.root_path, "templates", "snask.zip")  # Caminho absoluto correto
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    
    return "Arquivo snask.zip não encontrado", 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

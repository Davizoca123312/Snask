from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import os
import json

app = Flask(__name__)
LIBS_FILE = 'libs.json'

# Função para carregar o conteúdo de libs.json
def load_libs():
    if os.path.exists(LIBS_FILE):
        with open(LIBS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Função para salvar as bibliotecas no libs.json
def save_libs(libs):
    with open(LIBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(libs, f, indent=4)

@app.route('/')
def index():
    libs = load_libs()
    return render_template('index.html', libraries=libs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        description = request.form['description']
        code = request.form['code']
        
        libs = load_libs()
        new_lib = {
            'name': name,
            'author': author,
            'description': description,
            'code': code
        }
        libs.append(new_lib)
        save_libs(libs)
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/lib/<int:lib_id>')
def view(lib_id):
    libs = load_libs()
    if lib_id < len(libs):
        lib = libs[lib_id]
        return render_template('view.html', lib=lib, lib_id=lib_id)
    return "Biblioteca não encontrada", 404

# 🆕 Rota de download da biblioteca
@app.route('/download/<name>')
def download(name):
    libs = load_libs()
    for lib in libs:
        if lib['name'] == name:
            return Response(lib['code'], mimetype='text/plain')
    return "Biblioteca não encontrada", 404

# 🆕 Rota para snaskget.py (formato JSON)
@app.route('/api/lib/<string:name>')
def api_lib(name):
    libs = load_libs()
    for lib in libs:
        if lib['name'] == name:
            return jsonify({'code': lib['code']})
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

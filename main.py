from flask import Flask, render_template, g, request, redirect, url_for, Response, jsonify
import sqlite3
import os

app = Flask(__name__)
@app.route('/')
def download_installer():
    installer_path = os.path.join('templates', 'installer.exe')
    if os.path.exists(installer_path):
        return send_file(installer_path, as_attachment=True)
    return "Arquivo installer.exe não encontrado", 404
if __name__ == '__main__':
   

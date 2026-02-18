import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Conexión a la base de datos de Render
def get_db_connection():
    # Render te dará una "External Database URL"
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

# Crear la tabla de comentarios si no existe
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS sugerencias (id serial PRIMARY KEY, nombre varchar(100), mensaje text);')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sugerencias;')
    comentarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', comentarios=comentarios)

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    mensaje = request.form['mensaje']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO sugerencias (nombre, mensaje) VALUES (%s, %s)', (nombre, mensaje))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/admin')
def admin():
    clave = request.args.get('clave')
    PASSWORD_SECRETA = "perfume2026"

    if clave == PASSWORD_SECRETA:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sugerencias ORDER BY ID desc;')
        comentarios = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('admin.html', comentarios=comentarios)
    else:
        return "<h1>Acceso Denegado</h1><p>No tienes permiso para ver esta página.</p>", 403
    
init_db()

if __name__ == '__main__':
    app.run(debug=True)


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
    cur.execute('SELECT nombre, mensaje FROM sugerencias;')
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

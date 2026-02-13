from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Aquí guardaremos los comentarios (en una lista temporal por ahora)
comentarios = []

@app.route('/')
def inicio():
    return """
    <h1>Perfumería Elite</h1>
    <p>Bienvenido a nuestra tienda de fragancias exclusivas.</p>
    <hr>
    <h3>Déjanos una sugerencia:</h3>
    <form action="/enviar" method="POST">
        <input type="text" name="nombre" placeholder="Tu nombre" required>
        <br><br>
        <textarea name="mensaje" placeholder="Tu sugerencia" required></textarea>
        <br>
        <button type="submit">Enviar</button>
    </form>
    <hr>
    <h3>Comentarios recientes:</h3>
    <ul>
    """ + "".join([f"<li><b>{c['nombre']}:</b> {c['mensaje']}</li>" for c in comentarios]) + "</ul>"

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    mensaje = request.form.get('mensaje')
    comentarios.append({'nombre': nombre, 'mensaje': mensaje})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

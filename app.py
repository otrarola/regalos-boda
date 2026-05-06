# app.py acces 127.0.0.1:5000

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

items = [
    {"id": 1, "title": "Viaje 1 todo pagado", "image": "/static/img/viaje1.jpg", "available": True},
    {"id": 2, "title": "Viaje 2 todo pagado", "image": "/static/img/viaje2.jpg", "available": False},
    {"id": 3, "title": "Viaje 3 todo pagado", "image": "/static/img/viaje3.jpg", "available": True},
    {"id": 4, "title": "Viaje 4 todo pagado", "image": "/static/img/viaje4.jpg", "available": True},
    {"id": 5, "title": "Viaje 5 todo pagado", "image": "/static/img/viaje5.jpg", "available": True},
    {"id": 6, "title": "Viaje 6 todo pagado", "image": "/static/img/viaje6.jpg", "available": True},
    {"id": 7, "title": "Viaje 7 todo pagado", "image": "/static/img/viaje7.jpg", "available": True},
    {"id": 8, "title": "Viaje 8 todo pagado", "image": "/static/img/viaje8.jpg", "available": True},
    {"id": 9, "title": "Viaje 9 todo pagado", "image": "/static/img/viaje9.jpg", "available": True},
    {"id": 10, "title": "Viaje 10 todo pagado", "image": "/static/img/viaje10.jpg", "available": True},
]

#  Formulario Login
@app.route('/')
def login():
    return render_template('login.html')

# ingresar enviando formulario
@app.route('/ingresar', methods=['POST'])
def ingresar():
    nombre = request.form.get('nombre')
    rut = request.form.get('rut')
    correo = request.form.get('correo')

#  guardar datos
    return redirect(url_for('index'))

#  Vista regalos
@app.route('/regalos')
def index():
    return render_template('index.html', items=items)

@app.route('/toggle/<int:item_id>', methods=['POST'])
def toggle(item_id):
    for item in items:
        if item['id'] == item_id and item['available']:
            item['available'] = False
            return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    app.run()
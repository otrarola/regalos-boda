# app.py acces 127.0.0.1:5000

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secreto"

# conexión BD
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# creación de tablas
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # tabla regalos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        image TEXT,
        available INTEGER
    )
    """)

    # tabla reservas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        rut TEXT,
        correo TEXT,
        item_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


#  insertar datos iniciales
def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]

    if count == 0:
        data = [
            ("Viaje 1 todo pagado", "/static/img/viaje1.jpg", 1),
            ("Viaje 2 todo pagado", "/static/img/viaje2.jpg", 0),
            # ("Viaje 3 todo pagado", "/static/img/viaje3.jpg", 1),
            # ("Viaje 4 todo pagado", "/static/img/viaje4.jpg", 1),
            # ("Viaje 5 todo pagado", "/static/img/viaje5.jpg", 1),
            # ("Viaje 6 todo pagado", "/static/img/viaje6.jpg", 1),
            # ("Viaje 7 todo pagado", "/static/img/viaje7.jpg", 1),
            # ("Viaje 8 todo pagado", "/static/img/viaje8.jpg", 1),
            # ("Viaje 9 todo pagado", "/static/img/viaje9.jpg", 1),
            # ("Viaje 10 todo pagado", "/static/img/viaje10.jpg", 1),
        ]

        cursor.executemany(
            "INSERT INTO items (title, image, available) VALUES (?, ?, ?)", data
        )

    conn.commit()
    conn.close()


# LOGIN
@app.route('/')
def login():
    return render_template('login.html')


#  guardar datos usuario 
@app.route('/ingresar', methods=['POST'])
def ingresar():
    session['nombre'] = request.form.get('nombre')
    session['rut'] = request.form.get('rut')
    session['correo'] = request.form.get('correo')

    return redirect(url_for('index'))


# vista regalos quien reservo 
@app.route('/regalos')
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT items.*, reservas.nombre as reservado_por
        FROM items
        LEFT JOIN reservas ON items.id = reservas.item_id
    """)

    items = cursor.fetchall()
    conn.close()

    return render_template('index.html', items=items)


#  reservar regalo
@app.route('/toggle/<int:item_id>', methods=['POST'])
def toggle(item_id):
    conn = get_db()
    cursor = conn.cursor()

    # verificar disponibilidad
    cursor.execute("SELECT available FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()

    if item and item["available"] == 1:

        # guardar reserva
        cursor.execute("""
            INSERT INTO reservas (nombre, rut, correo, item_id)
            VALUES (?, ?, ?, ?)
        """, (
            session.get('nombre'),
            session.get('rut'),
            session.get('correo'),
            item_id
        ))

        # marcar como no disponible
        cursor.execute("""
            UPDATE items
            SET available = 0
            WHERE id = ?
        """, (item_id,))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    conn.close()
    return jsonify({"success": False})


#  iniciar app
if __name__ == "__main__":
    init_db()
    seed_db()
    app.run(debug=True)
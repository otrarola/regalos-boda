import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# borrar reservas
cursor.execute("DELETE FROM reservas")

# dejar todos los items disponibles
cursor.execute("UPDATE items SET available = 1")

conn.commit()
conn.close()

print("Base de datos reseteada ✔")
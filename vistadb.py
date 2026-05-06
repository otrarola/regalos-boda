import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
SELECT 
    reservas.nombre,
    reservas.rut,
    reservas.correo,
    items.title
FROM reservas
JOIN items ON reservas.item_id = items.id
""")

rows = cursor.fetchall()

# encabezados
headers = ["Nombre", "RUT", "Correo", "Regalo"]

# calcular ancho de columnas
col_widths = [len(h) for h in headers]

for row in rows:
    for i, value in enumerate(row):
        col_widths[i] = max(col_widths[i], len(str(value)))

# función para imprimir fila
def print_row(row):
    print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))

# imprimir tabla
print("\n RESERVAS:\n")

print_row(headers)
print("-" * (sum(col_widths) + 3 * (len(headers)-1)))

for row in rows:
    print_row(row)

conn.close()
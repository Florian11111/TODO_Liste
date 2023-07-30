import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Tabellennamen abrufen
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Tabellennamen ausgeben
for table in tables:
    print(table[0])

# Verbindung schließen
conn.close()
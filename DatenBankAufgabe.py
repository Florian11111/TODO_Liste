import sqlite3

# Verbindung zur Datenbank herstellen oder eine neue erstellen
conn = sqlite3.connect("test.db")

# Ein Cursor-Objekt erstellen, um die Datenbankabfragen auszuführen
cursor = conn.cursor()

# Tabelle erstellen
cursor.execute("""
    CREATE TABLE IF NOT EXISTS aufgabe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT NOT NULL,
        beschreibung TEXT,
        wiederholl INTEGER
    )
""")

# Beispiel-Daten einfügen
cursor.execute("""
    INSERT INTO aufgabe (titel, beschreibung, wiederholl) VALUES 
    ('Eintrag 1', 'Beschreibung für Eintrag 1', 1),
    ('Eintrag 2', 'Beschreibung für Eintrag 2', 0),
    ('Eintrag 3', 'Beschreibung für Eintrag 3', 1)
""")

# Änderungen speichern
conn.commit()


# Daten aus der Tabelle abrufen
cursor.execute("SELECT * FROM aufgabe")
rows = cursor.fetchall()

# Ergebnisse ausgeben
for row in rows:
    print(row)

# Verbindung schließen
conn.close()

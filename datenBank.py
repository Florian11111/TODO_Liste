import sqlite3

datenBankpfad = "test.db"
# Verbindung zur Datenbank herstellen oder eine neue erstellen
conn = sqlite3.connect(datenBankpfad)

# Ein Cursor-Objekt erstellen, um die Datenbankabfragen auszuführen
cursor = conn.cursor()

# Erstellt erste Tabelle
cursor.execute("""
    CREATE TABLE IF NOT EXISTS aufgabe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT NOT NULL,
        beschreibung TEXT,
        wiederholl INTEGER
    )
""")

# Erstellt zweite Tabelle
cursor.execute("""
    CREATE TABLE IF NOT EXISTS aufgabenEintag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farbe INTEGER NOT NULL,
        bisWann TEXT NOT NULL,
        wannErledigt Text,
        aufgabeID INTEGER
    )
""")

# Erstellt dritte Tabelle
cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiederhollEintag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farbe INTEGER NOT NULL,
        naechstesVorkommen INTEGER NOT NULL,
        intervall INTEGER NOT NULL,
        aufgabeID INTEGER
    )
""")
# Änderung speichern
conn.commit()
conn.close()
print("Datenbank erfolgreich gestatet!")


'''
# Daten aus der Tabelle abrufen
cursor.execute("SELECT * FROM aufgabe")
rows = cursor.fetchall()

# Ergebnisse ausgeben
for row in rows:
    print(row)
'''

# returnt die Aufgabe mit der id, wenn id nicht gefunen -1
def getAufgabe(id):
    conn = sqlite3.connect(datenBankpfad)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM aufgabe WHERE id = ?
    """, (id,))
    aufgabe = cursor.fetchone()  # Fetch the first row
    conn.close()
    if aufgabe is None:
        return -1
    else:
        return aufgabe

# returnt den AufgabeEintag mit der id, wenn id nicht gefunen -1
def getAufgabenEintag(id):
    conn = sqlite3.connect(datenBankpfad)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM aufgabenEintag WHERE id = ?
    """, (id,))
    aufgabeneintag = cursor.fetchone()
    conn.close()
    if aufgabeneintag is None:
        return -1
    else:
        return aufgabeneintag


# Erstelle aufgabe, gibt die id zurück
def neueAufgabe(titel, beschreibung, aufgabenwiederhollung):
    conn = sqlite3.connect(datenBankpfad)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aufgabe (titel, beschreibung, wiederholl)
        VALUES (?, ?, ?)
    """, (titel, beschreibung, aufgabenwiederhollung))
    conn.commit()
    aufgaben_id = cursor.lastrowid
    conn.close()
    return aufgaben_id

# Erstellt eine aufgabe und ein dazugehörige Aufgabeneintrag
def neueAufgabeUndEintrag(titel, beschreibung, farbe, bisWann):
    aufgaben_id = neueAufgabe(titel, beschreibung, 0)
    conn = sqlite3.connect(datenBankpfad)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aufgabenEintag (farbe, bisWann, aufgabeID)
        VALUES (?, ?, ?)
    """, (farbe, bisWann, aufgaben_id))
    conn.commit()
    conn.close()
    return aufgaben_id

''' 
Wird aufgerufen wenn ein eintrag abgehackt wird.
Wenn es ein Aufgaben eintrag mit der id gibt wird dieser aktualliesiert
und der neue Status zurückgebenen wenn es die id nicht gibt -1
'''
def aktuelle(id, aktuellerStatus):
    return aktuellerStatus


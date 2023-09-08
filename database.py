import sqlite3
from datetime import datetime
import re

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
        erledigt INTEGER NOT NULL,
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
print("Datenbank [", datenBankpfad, "] gestatet!")

# lösche AufgabenEintrag und Aufgabe (falls sinvoll)
def loescheAufgabenEintrag(aufgabenEintrag_id):
    connection = sqlite3.connect(datenBankpfad)
    cursor = connection.cursor()
    cursor.execute("SELECT aufgabeID FROM aufgabenEintag WHERE id = ?", (aufgabenEintrag_id,))
    aufgabe_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM aufgabenEintag WHERE id = ?", (aufgabenEintrag_id,))
    cursor.execute("SELECT COUNT(*) FROM aufgabenEintag WHERE aufgabeID = ?", (aufgabe_id,))
    num_related_entries = cursor.fetchone()[0]
    if num_related_entries == 0:
        cursor.execute("DELETE FROM aufgabe WHERE id = ?", (aufgabe_id,))
    connection.commit()

def datum_ersetzen(id, new_date):
    if not re.match(r'\d{4}-\d{2}-\d{2}', new_date):
        raise ValueError("das gegebene datum ist nicht im iso-format!")
    connection = sqlite3.connect(datenBankpfad)
    cursor = connection.cursor()
    cursor.execute("SELECT bisWann FROM aufgabenEintag WHERE id = ?", (id,))
    current_date_str = cursor.fetchone()[0]
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    new_date = datetime.strptime(new_date, "%Y-%m-%d")
    if new_date == current_date:
        return 0
    elif new_date < current_date:
        raise ValueError("Das übergebene Datum liegt in der Vergangenheit.")
    else:
        cursor.execute("UPDATE aufgabenEintag SET bisWann = ? WHERE id = ?", (new_date, id))
        connection.commit()
        return 1

# returnt die Aufgaben die am tag x zu erledigen ist
def getAufgabenTagX(datum):
    connection = sqlite3.connect(datenBankpfad)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM aufgabenEintag
        WHERE DATE(bisWann) = DATE(?)
    """, (datum,))
    aufgaben = cursor.fetchall()
    connection.close()
    return aufgaben

def aufgabenVonHeute():
    datumHeute = datetime.now().date().isoformat()
    temp = []
    for x in getAufgabenTagX(datumHeute):
        aufgabe = getAufgabe(x[5])
        formatted_item = {
        'id': x[0],
        'color': x[1],#
        'title': aufgabe[1],
        'checkt': x[4]
        }
        temp.append(formatted_item)
    return temp

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
def neueAufgabe(titel, aufgabenwiederhollung):
    conn = sqlite3.connect(datenBankpfad)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aufgabe (titel, wiederholl)
        VALUES (?, ?)
    """, (titel, aufgabenwiederhollung))
    conn.commit()
    aufgaben_id = cursor.lastrowid
    conn.close()
    return aufgaben_id

# Erstellt eine aufgabe und ein dazugehörige Aufgabeneintrag
def neueAufgabeUndEintrag(titel, farbe, bisWann):
    if titel is None or farbe is None or bisWann is None:
        raise ValueError("Das Argument darf nicht None sein.")
    aufgaben_id = neueAufgabe(titel, 0)
    conn = sqlite3.connect(datenBankpfad)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aufgabenEintag (farbe, bisWann, aufgabeID, erledigt)
        VALUES (?, ?, ?, 0)
    """, (farbe, bisWann, aufgaben_id))
    conn.commit()
    conn.close()
    return aufgaben_id

''' 
TODO: Wird aufgerufen wenn ein eintrag abgehackt wird.
Wenn es ein Aufgaben eintrag mit der id gibt wird dieser aktualliesiert, Außerdem wird
das erlegigt datum gespeichert / gelöscht
und der neue Status zurückgebenen wenn es die id nicht gibt -1 
''' 
def aktuelle(id, aktuellerStatus):
    connection = sqlite3.connect(datenBankpfad)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM aufgabenEintag WHERE id = ?", (id,))
    eintrag = cursor.fetchone()
    if eintrag:
        if int(aktuellerStatus) == 1:
            # Eintrag wurde abgehakt, also aktualisieren
            cursor.execute("UPDATE aufgabenEintag SET wannErledigt = DATE('now'), erledigt = 1 WHERE id = ?", (id,))
            returnTemp = 1
        else:
            # Eintrag wird als nicht abgehakt markiert
            cursor.execute("UPDATE aufgabenEintag SET wannErledigt = NULL, erledigt = 0 WHERE id = ?", (id,))
            returnTemp = 0
        connection.commit()
    else:
        returnTemp = -1
    connection.close()
    return returnTemp

def getFormatierteAufgabe(id):
    tempaufgabe = getAufgabenEintag(id)
    if tempaufgabe == -1:
        return -1
    aufgabe = getAufgabe(tempaufgabe[5])
    return {
    'id': tempaufgabe[0],
    'color': tempaufgabe[1],
    'title': aufgabe[1],
    'checkt': tempaufgabe[4]
    }
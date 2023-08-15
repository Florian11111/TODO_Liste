import datenBank as db
import random

def farbeZufall():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)   
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

# ISO-Format Datum
datum = "2023-08-15"
datum2 = "2023-08-16"

anzahl_daten = 8
for x in range(8):
    print(db.neueAufgabeUndEintrag(f'TestTitel{x}', f'Das ist ein Test {x}', farbeZufall(), datum))


temp = db.getAufgabenEintag(1)
print("Aufgabe: ", db.getAufgabe(temp[5]))
print("Aufgaben Eintrag: ", temp)
print(db.getAufgabenTagX(datum2))
print(db.aufgabenVonHeute())
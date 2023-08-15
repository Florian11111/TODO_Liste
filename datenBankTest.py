import datenBank as db
import random

def farbeZufall():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)   
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

# ISO-Format Datum
datum = "2023-08-13"
datum2 = "2023-08-14"
datum3 = "2023-08-07"
print(db.neueAufgabeUndEintrag("TestTitel", "Das ist ein Test", farbeZufall(), datum))
print(db.neueAufgabeUndEintrag("TestTitel2", "Das ist ein Test2", farbeZufall(), datum))
print(db.neueAufgabeUndEintrag("TestTitel3", "Das ist ein Test3", farbeZufall(), datum))
print(db.neueAufgabeUndEintrag("TestTitel4", "Das ist ein Test4", farbeZufall(), datum2))
print(db.neueAufgabeUndEintrag("TestTitel5", "Das ist ein Test5", farbeZufall(), datum2))


temp = db.getAufgabenEintag(1)
print("Aufgabe: ", db.getAufgabe(temp[5]))
print("Aufgaben Eintrag: ", temp)
print(db.getAufgabenTagX(datum3))
print(db.aufgabenVonHeute())
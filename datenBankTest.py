import datenBank as db

# ISO-Format Datum
datum = "2023-08-05"
datum2 = "2023-08-06"
datum3 = "2023-08-07"
farbe = '#ff7645'
'''
print(db.neueAufgabeUndEintrag("TestTitel", "Das ist ein Test", farbe, datum))
print(db.neueAufgabeUndEintrag("TestTitel2", "Das ist ein Test2", farbe, datum))
print(db.neueAufgabeUndEintrag("TestTitel3", "Das ist ein Test3", farbe, datum))
print(db.neueAufgabeUndEintrag("TestTitel4", "Das ist ein Test4", farbe, datum2))
print(db.neueAufgabeUndEintrag("TestTitel5", "Das ist ein Test5", farbe, datum2))
'''

temp = db.getAufgabenEintag(1)
print("Aufgabe: ", db.getAufgabe(temp[5]))
print("Aufgaben Eintrag: ", temp)
print(db.getAufgabenTagX(datum3))
print(db.aufgabenVonHeute())
import datenBank as db

# ISO-Format Datum
datum = "2023-08-05"
farbe = '#ff7645'

print(db.neueAufgabeUndEintrag("TestTitel", "Das ist ein Test", farbe, datum))
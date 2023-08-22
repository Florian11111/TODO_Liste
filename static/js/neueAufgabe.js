const toggleKnopf = document.getElementById("toggleKnopf");
const meinDiv = document.getElementById("meinDiv");

toggleKnopf.addEventListener("click", () => {
  document.getElementById("error").innerHTML = "";
  if (meinDiv.style.display === "none") {
      meinDiv.style.display = "block"; //
  } else {
      meinDiv.style.display = "none";  
  }
});

function auswaehlen() {
  // Zugriff auf die Formularelemente
  var title = document.getElementById("title").value;
  var beschreibung = document.getElementById("beschreibung").value;
  var date = document.getElementById("date").value;
  var color = document.getElementById("color").value;
  
  // wenn alle != null dann neue aufgabe erstellen. => wenn erfolgreich => datum auf heute, farbe auf rot, titel und beschreibung leeren
  if (title === "" || date == "" || color == "") {
    document.getElementById("error").innerHTML = "bitte fülle alle datum und titel aus\n";
  } else {
    // Ausgabe der Werte in der Konsole
    fetch(apiUrl + '/api/addTask', {
      method: 'GET',
      headers: {
          'titel': title,
          'beschreibung': beschreibung,
          'farbe': color,
          'datum': date,
      }
  })
  .then(response => response.json())
  .then(data => {   
      if (data == 1) {
        document.getElementById("error").innerHTML = "";
        datumHeute();
        syncColor();
        document.getElementById("title").value = "";
        document.getElementById("beschreibung").value = "";
        meinDiv.style.display = "none";  
        alleAufgaben();
      }
  })
  .catch(error => {
      // Zeige eine Fehlermeldung, wenn die Anfrage fehlschlägt
      document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
  });
  }
}
  
// Funktionen für die "Heute" und "Morgen" Buttons
function datumHeute() {
  document.getElementById("date").value = new Date().toISOString().split('T')[0];
}

function datumMorgen() {
  var morgen = new Date();
  morgen.setDate(morgen.getDate() + 1);
  document.getElementById("date").value = morgen.toISOString().split('T')[0];
}

// Funktion zum Synchronisieren der ausgewählten Farbe mit dem Farbfeld
function syncColor() {
  var presetColors = document.getElementById("presetColors");
  var colorInput = document.getElementById("color");
  colorInput.value = presetColors.value;
}

datumHeute();
syncColor();
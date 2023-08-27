// speichert alle tasks
let aufgabenListe = [];

function neuLaden() {
    document.getElementById("taskList").innerHTML = "";
    document.getElementById("taskListFertig").innerHTML = "";
    // kurzer time out so das man sieht dsa die seite wirklich neu geladen hat
    alleAufgaben();
}

function alleAufgaben() {
    fetch(apiUrl + '/api/alleTask', {
        method: 'GET',
        headers: {
            'Authorization': ''
        }
    })
    .then(response => response.json())
    .then(data => {   
        aufgabenListe = data; 
        document.getElementById("taskList").innerHTML = "";
        document.getElementById("taskListFertig").innerHTML = "";
        aufgabenListe.forEach((task, index) => {
            const listItem = createListItem(index);
            if (task.checkt === 0) {
                taskList.appendChild(listItem);
            } else {
                taskListFertig.appendChild(listItem);
            }
        });
    })
    .catch(error => {
        // Zeige eine Fehlermeldung, wenn die Anfrage fehlschlägt
        document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
    });
}


function createListItem(index) {
    const { id, color, title, checkt } = aufgabenListe[index];

    const listDiv1 = document.createElement("div");
    listDiv1.classList.add("listDiv1");
    listDiv1.style.backgroundColor = color;

    const titleStrong = document.createElement("strong");
    titleStrong.textContent = title;
    listDiv1.appendChild(titleStrong);

    const toggleButton = document.createElement("button");
    toggleButton.textContent = "Toggle";

    const abhackenButton = document.createElement("button");
    abhackenButton.textContent = "Abhacken";
    abhackenButton.addEventListener("click", () => abhackenKnopf(index));

    const buttonContainer = document.createElement("div");
    buttonContainer.classList.add("buttonContainer"); // Füge die CSS-Klasse für Flex-Layout hinzu
    buttonContainer.appendChild(toggleButton);
    buttonContainer.appendChild(abhackenButton);

    listDiv1.appendChild(buttonContainer);


    const listDiv2 = document.createElement("div");
    listDiv2.classList.add("listDiv2");
    listDiv2.style.display = "none"; // Start with inner div hidden

    const button2 = document.createElement("button");
    button2.textContent = "Löschen";
    button2.addEventListener("click", () => loeschenKnopf(index));
    listDiv2.appendChild(button2);

    const datumDiv = document.createElement("div");
    const dateInput = document.createElement("input");
    dateInput.type = "date";
    dateInput.id = "date";
    dateInput.name = "date";
    dateInput.required = true;
    
    const morgen = new Date();
    morgen.setDate(morgen.getDate() + 1);
    
    // Setzen Sie das Standarddatum auf morgen ohne Uhrzeit
    dateInput.defaultValue = morgen.toISOString().split("T")[0];
    
    datumDiv.appendChild(dateInput);


    const verschiebenButton = document.createElement("button");
    verschiebenButton.textContent = "Verschieben";
    verschiebenButton.addEventListener("click", () => {
        datum_ersetzen(index, dateInput.value);
    });
    datumDiv.appendChild(verschiebenButton);

    listDiv2.appendChild(datumDiv);

    const toggleButton2 = document.createElement("button");
    toggleButton2.textContent = "Toggle";
    listDiv2.appendChild(toggleButton2);

    listDiv1.appendChild(listDiv2);

    toggleButton.addEventListener("click", () => {
        listDiv2.style.display = "flex";
        listDiv1.style.display = "none";
    });

    toggleButton2.addEventListener("click", () => {
        listDiv2.style.display = "none";
        listDiv1.style.display = "flex";
    });

    const li = document.createElement("li");
    li.classList.add("listElement");
    li.appendChild(listDiv1);
    li.appendChild(listDiv2);
    return li;
}

/*
function neueAufgabe() {
    fetch(apiUrl + '/api/addTask', {
        method: 'GET',
        headers: {
            
            titel = request.headers.get('titel')
            beschreibung = request.headers.get('beschreibung')
            farbe = request.headers.get('farbe')
            datum = request.headers.get('datum')
            
        }
    })
    .then(response => response.json())
    .then(antwort => {  
        aufgabenListe[index].checkt = antwort.aktuallisiert;
        updateAlleAufgaben();
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
        updateAlleAufgaben();
    });
} 
*/

function datum_ersetzen(index, datum) {
    const heute = new Date();

    if (new Date(datum) >= heute) {
        console.log("datum gültig.");
    } else {
        console.log("datum ungültig.");
        return;
    }
    console.log(datum)
    fetch(apiUrl + '/api/moveTask', {
        method: 'GET',
        headers: {
            'Authorization': '',
            'id': aufgabenListe[index].id,
            'datum': datum
        }
    })
    .then(response => response.json())
    .then(antwort => {  
        if (antwort === 1) {
            if (aufgabenListe[index].checkt === 0) {
                removeListItemFromList(index, taskList)
            } else {
                removeListItemFromList(index, taskListFertig)
            }
        } else {
            console.log("Fehler bei löschen einer Aufgabe!")
        }
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
    });
}

function loeschenKnopf(index) {
    fetch(apiUrl + '/api/deleteTask', {
        method: 'GET',
        headers: {
            'Authorization': '',
            'id': aufgabenListe[index].id
        }
    })
    .then(response => response.json())
    .then(antwort => {  
        if (antwort === 1) {
            if (aufgabenListe[index].checkt === 0) {
                removeListItemFromList(index, taskList)
            } else {
                removeListItemFromList(index, taskListFertig)
            }
        } else {
            console.log("Fehler bei löschen einer Aufgabe!")
        }
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
    });
}

function abhackenKnopf(index) {
    const newChecktValue = aufgabenListe[index].checkt === 0 ? 1 : 0;
    if (aufgabenListe[index].checkt === 0) {
        removeListItemFromList(index, taskList)
    } else {
        removeListItemFromList(index, taskListFertig)
    }

    fetch(apiUrl + '/api/aufgabeCheck', {
        method: 'GET',
        headers: {
            'Authorization': '',
            'AufgabenlisteID': aufgabenListe[index].id,
            'neuerStand': newChecktValue
        }
    })
    .then(response => response.json())
    .then(antwort => {  
        aufgabenListe[index].checkt = antwort.aktuallisiert;
        updateAlleAufgaben();
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
        updateAlleAufgaben();
    });
}

function removeListItemFromList(index, list) {
    const listItems = list.querySelectorAll("li");
    if (listItems[index]) {
        listItems[index].remove();
    }
}

function updateAlleAufgaben() {
    const taskList = document.getElementById("taskList");
    const taskListFertig = document.getElementById("taskListFertig");

    taskList.innerHTML = ""; // Leere die Listen
    taskListFertig.innerHTML = "";

    aufgabenListe.forEach((task, index) => {
        const listItem = createListItem(index);
        if (task.checkt === 0) {
            taskList.appendChild(listItem);
        } else {
            taskListFertig.appendChild(listItem);
        }
    });
}

var socket;
function connectToSocket() {
    socket = io.connect(apiUrl, {
        query: { token: '' }
    });

    socket.on('connect', function() {
        console.log('WebSocket connected');
    });

    socket.on('update', function(state) {
        if (state == 1) {
            console.log("update!")
            alleAufgaben(); // updatet alle Aufgaben
        }
    });
    socket.on('invalid_token', function() {
        console.log('Invalid token. Closing WebSocket connection.');
        socket.close();
    });
}
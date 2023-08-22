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
    const { id, color, title, description, checkt } = aufgabenListe[index];

    const li = document.createElement("li");
    li.style.backgroundColor = color;

    const strong = document.createElement("strong");
    strong.textContent = title;
    li.appendChild(strong);

    const p = document.createElement("p");
    p.textContent = description;
    li.appendChild(p);

    const button = document.createElement("button");
    button.textContent = "Abhacken";
    button.addEventListener("click", () => abhackenKnopf(index));
    li.appendChild(button);
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
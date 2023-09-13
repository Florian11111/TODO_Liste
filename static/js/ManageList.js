// speichert alle tasks
let aufgabenListe = [];

function listReload() {
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

function findIndex(searchID) {
    for (let index = 0; index < aufgabenListe.length; index++) {  
        if (aufgabenListe[index].id == searchID) {
            return index; // ID gefunden, Index speichern und Methode beenden
        }
    }
    console.error("ID Nichts gefunden.");
    return -1;
}

function update_task(id) {
    index = findIndex(id)
    if (index == -1) {
        return;
    }
    fetch(apiUrl + '/api/singleTask', {
        method: 'GET',
        headers: {
            'Authorization': '',
            'id': aufgabenListe[index].id,
        }
    })
    .then(response => response.json())
    .then(antwort => {  
        if (aufgabenListe[index].checkt === 0) {
            removeListItemFromList(index, taskList)
        } else {
            removeListItemFromList(index, taskListFertig)
        }
        console.log(antwort);
        aufgabenListe[index] = antwort;
        updateAlleAufgaben();
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Fehler beim Abrufen der Daten.';
    });
    
    aufgabenListe
}

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


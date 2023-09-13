function createListItem(index) {
    const { id, color, title, checkt } = aufgabenListe[index];

    const listDiv1 = document.createElement("div");
    listDiv1.classList.add("listDiv1");
    if (!checkt) {
        listDiv1.style.backgroundColor = color;
    } else {
        listDiv1.style.backgroundColor = "#555555";
    }

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
    if (!checkt) {
        buttonContainer.appendChild(toggleButton);
    }
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

    fetch(apiUrl + '/api/checkTask', {
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
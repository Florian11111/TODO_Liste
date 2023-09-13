var socket;
function connectToSocket() {
    socket = io.connect(apiUrl, {
        query: { token: '' }
    });

    socket.on('connect', function() {
        console.log('WebSocket connected');
    });

    socket.on('update_all', function(state) {
        if (state == 1) {
            console.log("update all!")
            alleAufgaben(); // updatet alle Aufgaben
        }
    });

    socket.on('update_taks', function(id) {
        console.log("update ID: " + id + "!");
        update_task(id); 
    });

    socket.on('delete_taks', function(id) {
        console.log("deletes ID: " + id + "!") + " (not implementet)";
        // update_task(id); 
    });
    

    socket.on('invalid_token', function() {
        console.log('Invalid token. Closing WebSocket connection.');
        socket.close();
    });
}
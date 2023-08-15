from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
import json
import threading
# eigene imports
import datenBank

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
# daten aus json geladen
app.secret_key = config["secret_key"]
SECRET_TOKEN = config["secret_token"]
users = config["users"]
# wenn eine änderung verhanden ist update = 1
updateWeb = 0
updateLokal = 0
valid_token = '123' 


# Route für die Anmeldeseite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('protected'))
        else:
            return 'Ungültige Anmeldedaten. Versuche es erneut.'
    return render_template('login.html')

# Route für die geschützte Seite
@app.route('/protected')
def protected():
    if 'logged_in' in session and session['logged_in']:
        return render_template('todo.html')
        # return render_template('todo.html', information="test") wert übergeben
    else:
        return 'Du musst dich zuerst anmelden, um diese Seite zu sehen.'

# Route für die Abmeldung
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('protected'))
    else:
        return redirect(url_for('login'))

# REST API TEIL --------------------------------------------------------------

@app.route('/api/addTask', methods=['GET'])
def addTask():
    if 'logged_in' in session and session['logged_in']:
        titel = request.headers.get('titel')
        beschreibung = request.headers.get('beschreibung')
        farbe = request.headers.get('farbe')
        datum = request.headers.get('datum')
        datenBank.neueAufgabeUndEintrag(titel, beschreibung, farbe, datum)

@app.route('/api/alleTask', methods=['GET'])
def alleTask():
    # TODO: update verhalten ändern
    global update
    update = 0
    token = request.headers.get('Authorization')
    # Überprüfe, ob der Benutzer eingeloggt ist oder ein gültiges Token gesendet wurde
    if 'logged_in' in session and session['logged_in']:
        return jsonify(datenBank.aufgabenVonHeute()), 200
    elif token and token == f"Bearer {SECRET_TOKEN}":
        return jsonify(datenBank.aufgabenVonHeute()), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401



@app.route('/api/aufgabeCheck', methods=['GET'])
def aufgabeCheck():
    global updateWeb
    token = request.headers.get('Authorization')
    if 'logged_in' in session and session['logged_in'] or (token and token == f"Bearer {SECRET_TOKEN}"):
        ids = request.headers.get('AufgabenlisteID')
        status = request.headers.get('neuerStand')
        temp = datenBank.aktuelle(ids, status)
        if temp == -1:
            raise ValueError("Aufgabenid nicht gefunden:", ids)
        updateWeb = 1
        return jsonify({'aktuallisiert': temp}), 200
    else:
        updateWeb = 1
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


# Websocket Teil --------------------------------------------------
@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    if token != valid_token and not 'logged_in' in session or not session['logged_in']:
        emit('invalid_token')
        disconnect()
    else:
        emit('message', 'Successfully connected')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    socketio.send('Message received: ' + message)


def updateAenderung():
    global updateLokal
    while True:
        if updateLokal == 1:
            socketio.emit('update', 1)
            updateLokal = 0
            print("Gesendet!")

# ----------------------- TODO: remove
def Entfernen():
    global updateLokal
    while True:
        if input() == "updaten!":
            updateLokal = 1

update_thread1 = threading.Thread(target=Entfernen, daemon=True).start()
# ----------------------- remove

update_thread = threading.Thread(target=updateAenderung, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

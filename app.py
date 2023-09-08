from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
import json
# own files
import database

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

app.secret_key = config["secret_key"]
LOCAL_TOKEN = config["local_token"]
WEBSOCKET_Token = config["websocket_token"]
users = config["users"]

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

@app.route('/api/moveTask', methods=['GET'])
def move_Task():
    if 'logged_in' in session and session['logged_in']:
        id = str(request.headers.get('id'))
        datum = str(request.headers.get('datum'))
        status = database.datum_ersetzen(id, datum)
        update = 1# TODO:
        return jsonify(status), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


@app.route('/api/deleteTask', methods=['GET'])
def delete_Task():
    if 'logged_in' in session and session['logged_in']:
        id = str(request.headers.get('id'))
        database.loescheAufgabenEintrag(id)
        update = 1 # TODO:
        return jsonify(1), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


@app.route('/api/addTask', methods=['GET'])
def add_Task():
    if 'logged_in' in session and session['logged_in']:
        titel = str(request.headers.get('titel'))
        farbe = str(request.headers.get('farbe'))
        datum = str(request.headers.get('datum'))
        id = database.neueAufgabeUndEintrag(titel, farbe, datum)
        update_List(id)
        return jsonify(1), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401

@app.route('/api/alleTask', methods=['GET'])
def alle_Task():
    # TODO: update verhalten ändern
    token = request.headers.get('Authorization')
    # Überprüfe, ob der Benutzer eingeloggt ist oder ein gültiges Token gesendet wurde
    if 'logged_in' in session and session['logged_in']:
        return jsonify(database.aufgabenVonHeute()), 200
    elif token and token == f"Bearer {LOCAL_TOKEN}":
        return jsonify(database.aufgabenVonHeute()), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


@app.route('/api/checkTask', methods=['GET'])
def check_Task():
    token = request.headers.get('Authorization')
    if 'logged_in' in session and session['logged_in'] or (token and token == f"Bearer {LOCAL_TOKEN}"):
        ids = request.headers.get('AufgabenlisteID')
        status = request.headers.get('neuerStand')
        temp = database.aktuelle(ids, status)
        if temp == -1:
            raise ValueError("Aufgabenid nicht gefunden:", ids)
        update_List(ids)
        return jsonify({'aktuallisiert': temp}), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


@app.route('/api/singleTask', methods=['GET'])
def single_Task():
    global update
    token = request.headers.get('Authorization')
    if 'logged_in' in session and session['logged_in'] or (token and token == f"Bearer {LOCAL_TOKEN}"):
        ids = request.headers.get('id')
        upgedatete_daten = database.getFormatierteAufgabe(ids)
        if upgedatete_daten == -1:
            raise ValueError("Aufgabenid nicht gefunden:", ids)
        return jsonify(upgedatete_daten), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


# Websocket Teil --------------------------------------------------
@socketio.on('connect')
def connect():
    token = request.args.get('token')
    if token == WEBSOCKET_Token or 'logged_in' in session and session['logged_in']:
        emit('message', 'Successfully connected')
        socketio.emit('update_all', 1)
        print("Gesendet!")
    else:
        emit('invalid_token')
        disconnect()

def update_List(id):
    socketio.emit('update_taks', id)

def delete_single_Item(id):
    socketio.emit('delete_taks', id)

def update_all(id):
    socketio.emit('update_all', 1)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

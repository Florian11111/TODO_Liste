from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import json
import datenBank

app = Flask(__name__)
CORS(app)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
# daten aus json geladen
app.secret_key = config["secret_key"]
SECRET_TOKEN = config["secret_token"]
users = config["users"]
# wenn eine änderung verhanden ist update = 1
update = 0

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
        return f'Willkommen, {session["username"]}! Dies ist die geschützte Seite.'
    else:
        return 'Du musst dich zuerst anmelden, um diese Seite zu sehen.'

# Route für die Abmeldung
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# REST API TEIL --------------------------------------------------------------
@app.route('/api/alleTask', methods=['GET'])
def alleTask_api():
    global update
    update = 0
    token = request.headers.get('Authorization')
    # Überprüfe, ob ein Token gesendet wurde und ob es dem erwarteten Token entspricht
    if token and token == f"Bearer {SECRET_TOKEN}":
        return jsonify(datenBank.aufgabenVonHeute()), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


@app.route('/api/aufgabeCheck', methods=['GET'])
def aufgabeCheck_api():
    global update
    update = 1
    token = request.headers.get('Authorization')
    # Überprüfe, ob ein Token gesendet wurde und ob es dem erwarteten Token entspricht
    if token and token == f"Bearer {SECRET_TOKEN}":
        ids = request.headers.get('AufgabenlisteID')
        status = request.headers.get('neuerStand')
        temp = datenBank.aktuelle(ids, status)
        if temp == -1:
            raise ValueError("Aufgabenid nicht gefunden: ", ids)
        return jsonify({'aktuallisiert': temp}), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401


@app.route('/api/webSocket', methods=['GET'])
def updateCheck():
    global update
    token = request.headers.get('Authorization')
    if token and token == f"Bearer {SECRET_TOKEN}":
        return jsonify({'update': update}), 200
    else:
        return jsonify({'message': 'Unautorisierter Zugriff'}), 401
    
if __name__ == '__main__':
    app.run(debug=True)

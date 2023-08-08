from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

valid_token = '123'  # Replace with your valid token

@app.route('/')
def index():
    return "test"

@socketio.on('connect')
def handle_connect():
    user_token = request.args.get('token')
    if user_token != valid_token:
        emit('invalid_token')
        disconnect()
    else:
        emit('message', 'Successfully connected')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    socketio.send('Message received: ' + message)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

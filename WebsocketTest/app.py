from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, async_mode='eventlet')
CORS(app)
socketio.init_app(app, cors_allowed_origins="http://localhost:8000")

valid_token = '123'

@app.route('/')
def index():
    return "Hallo"

@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'Connected'})

@socketio.on('token_verification')
def verify_token(data):
    if data.get('token') == valid_token:
        emit('token_verified', {'message': 'Token verified'})
    else:
        emit('token_verification_failed', {'message': 'Token verification failed'})
        socketio.disconnect()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

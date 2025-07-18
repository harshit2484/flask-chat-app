import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

VALID_PASSWORD = "HARI"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if password == VALID_PASSWORD and username.strip():
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"}), 401

@socketio.on('message')
def handle_message(data):
    print(f"{data['user']}: {data['message']}")
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

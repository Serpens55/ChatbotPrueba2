import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room
import uuid
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', manage_session=False)

# Diccionario para almacenar los chats y usuarios
chats = {}
clientes_conectados = {}

@app.route('/', methods=['GET', 'HEAD'])
def client_page():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'HEAD'])
def admin_page():
    return render_template('admin.html')

@socketio.on('connect')
def handle_connect():
    # Generamos un ID único para cada cliente en cada conexión
    user_id = str(uuid.uuid4())  # Generar un ID único usando uuid
    # Almacenamos el user_id directamente en clientes_conectados con request.sid
    clientes_conectados[request.sid] = {'user_id': user_id}

    # Emitimos el ID al cliente
    emit('connected', {'user_id': user_id})
    emit('update_chat_list', list(clientes_conectados.keys()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get('user_id')
    if user_id:
        clientes_conectados.pop(request.sid, None)
        chats.pop(user_id, None)
        emit('update_chat_list', list(clientes_conectados.keys()), broadcast=True)

@socketio.on('join')
def handle_join():
    user_id = session.get('user_id')
    join_room(request.sid)  # Unir a la sala basada en el SID de la conexión actual
    if user_id not in chats:
        chats[user_id] = []
    emit('chat_history', chats[user_id], room=request.sid)

@socketio.on('message')
def handle_message(data):
    user_id = session.get('user_id')
    if user_id not in chats:
        chats[user_id] = []

    msg = {'text': data['text'], 'timestamp': time.strftime('%H:%M:%S'), 'sender': 'cliente'}
    chats[user_id].append(msg)

    emit('message', msg, room=request.sid)
    emit('message_admin', {'user_id': user_id, 'message': msg}, broadcast=True)

@socketio.on('admin_select_chat')
def admin_select_chat(data):
    user_id = data['user_id']
    if user_id in chats:
        emit('chat_history', chats[user_id], room=request.sid)

@socketio.on('admin_message')
def handle_admin_message(data):
    user_id = data['user_id']
    msg = {'text': data['text'], 'timestamp': time.strftime('%H:%M:%S'), 'sender': 'admin'}

    if user_id in chats:
        chats[user_id].append(msg)

    emit('message', msg, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': msg}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

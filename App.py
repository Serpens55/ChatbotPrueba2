from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='gevent', manage_session=False)

chats = {}
clientes_conectados = {}

@app.route('/')
def client_page():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@socketio.on('connect')
def handle_connect():
    emit('connected', {'user_id': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    clientes_conectados.pop(user_id, None)
    chats.pop(user_id, None)
    emit('update_chat_list', [
        {'user_id': uid, 'name': info['name']}
        for uid, info in clientes_conectados.items()
    ], broadcast=True)

@socketio.on('join')
def handle_join():
    user_id = request.sid
    join_room(user_id)
    if user_id not in chats:
        chats[user_id] = []
    emit('chat_history', chats[user_id], room=user_id)

@socketio.on('register_name')
def handle_register_name(data):
    name = data.get('name', 'Invitado')
    user_id = request.sid
    clientes_conectados[user_id] = {'name': name}
    emit('update_chat_list', [
        {'user_id': uid, 'name': info['name']}
        for uid, info in clientes_conectados.items()
    ], broadcast=True)

@socketio.on('message')
def handle_message(data):
    user_id = request.sid
    name = clientes_conectados.get(user_id, {}).get('name', 'Invitado')
    text = data['text'].strip().lower()

    if text == "menu":
        emit('show_menu', room=user_id)
        return

    msg = {
        'text': data['text'],
        'timestamp': time.strftime('%H:%M:%S'),
        'sender': name
    }
    chats.setdefault(user_id, []).append(msg)

    emit('message', msg, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': msg}, broadcast=True)

    if text == "hola":
        enviar_audio(user_id, 'hola.mp3')
    elif text == "contacta con un administrador":
        enviar_audio(user_id, 'contactoadmin.mp3')
    elif text == "gracias":
        enviar_audio(user_id, 'agradecimiento.mp3')

@socketio.on('menu_option_selected')
def handle_menu_option(data):
    user_id = request.sid
    option = data.get('option')

    submenus = {
        "1": ["Subopción 1.1", "Subopción 1.2", "Subopción 1.3"],
        "2": ["Subopción 2.1", "Subopción 2.2"],
        "3": ["Subopción 3.1", "Subopción 3.2", "Subopción 3.3"],
        "4": ["Subopción 4.1"]
    }

    submenu = submenus.get(option, [])

    # Enviar submenú al cliente
    emit('show_submenu', {'option': option, 'submenu': submenu}, room=user_id)

    # Notificar al administrador que el cliente interactuó con el menú
    emit('menu_interaction', {
        'user_id': user_id,
        'selection': f"Opción {option}"
    }, broadcast=True)

def enviar_audio(user_id, archivo):
    audio_msg = {
        'audio_url': f'/static/audio/{archivo}',
        'timestamp': time.strftime('%H:%M:%S'),
        'sender': 'Asistente'
    }
    chats[user_id].append(audio_msg)
    emit('message', audio_msg, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': audio_msg}, broadcast=True)

@socketio.on('admin_select_chat')
def admin_select_chat(data):
    user_id = data['user_id']
    join_room(user_id)
    emit('chat_history', chats.get(user_id, []), room=request.sid)

@socketio.on('admin_message')
def handle_admin_message(data):
    user_id = data['user_id']
    msg = {
        'text': data['text'],
        'timestamp': time.strftime('%H:%M:%S'),
        'sender': 'Admin'
    }
    chats.setdefault(user_id, []).append(msg)
    emit('message', msg, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': msg}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

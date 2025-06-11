
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

    print(f"Usuario registrado: {name} ({user_id})")

    emit('update_chat_list', [
        {'user_id': uid, 'name': info['name']}
        for uid, info in clientes_conectados.items()
    ], broadcast=True)

    # Mensaje de bienvenida de Cientibot
    bienvenida = {
        'text': f'Hola {name}, yo soy Cientibot. Para empezar, escriba "Menu" para abrir el menú interactivo 🚀',
        'timestamp': data.get("timestamp"),
        'sender': 'Cientibot'
    }

    # Mensaje de audio de bienvenida (usa tu archivo de audio aquí)
    audio_bienvenida = {
        'audio_url': '/static/audio/bienvenida.mp3',  # Asegúrate de tener este archivo
        'timestamp': data.get("timestamp"),
        'sender': 'Cientibot'
    }

    # Guardar en historial
    chats.setdefault(user_id, []).extend([bienvenida, audio_bienvenida])

    # Enviar ambos mensajes al cliente
    emit('message', bienvenida, room=user_id)
    emit('message', audio_bienvenida, room=user_id)

    # También enviar al administrador
    emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)
    emit('message_admin', {'user_id': user_id, 'message': audio_bienvenida}, broadcast=True)


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
        'timestamp': data.get("timestamp"),
        'sender': name
    }
    chats.setdefault(user_id, []).append(msg)

    emit('message', msg, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': msg}, broadcast=True)

    if text == "hola":
        enviar_audio(user_id, 'hola.mp3')
        bienvenida = {
            'text': "Un saludo amigo, yo soy Cientibot, tu asistente virtual. ¿En qué puedo ayudarte?",
            'timestamp': data.get("timestamp"),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)

    if text == "contacta con un administrador":
        enviar_audio(user_id, 'contactoadmin.mp3')
        bienvenida = {
            'text': "Espera un momento, seras contactado con un administrador en unos segundos para que pueda atenderte",
            'timestamp': data.get("timestamp"),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)

    if text == "gracias":
        enviar_audio(user_id, 'agradecimiento.mp3')
        bienvenida = {
            'text': "Ha sido un placer ser de ayuda, espero estes satisfecho.",
            'timestamp': data.get("timestamp"),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)

@socketio.on('register_name')
def handle_register_name(data):
    name = data.get('name', 'Invitado')
    user_id = request.sid
    clientes_conectados[user_id] = {'name': name}

    print(f"Usuario registrado: {name} ({user_id})")

    emit('update_chat_list', [
        {'user_id': uid, 'name': info['name']}
        for uid, info in clientes_conectados.items()
    ], broadcast=True)
        # Enviar mensaje de bienvenida al cliente
    bienvenida = {
        'text': f'Hola {name}, yo soy Cientibot. Para empezar, escriba "Menu" para abrir el menú interactivo 🚀',
        'timestamp': data.get("timestamp"),
        'sender': 'Cientibot'
    }
    
    chats.setdefault(user_id, []).append(bienvenida)
    emit('message', bienvenida, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)


def enviar_audio(user_id, archivo):
    audio_msg = {
        'audio_url': f'/static/audio/{archivo}',
        'timestamp': data.get("timestamp"),
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
        'timestamp': data.get("timestamp"),
        'sender': 'Admin'
    }
    chats.setdefault(user_id, []).append(msg)
    emit('message', msg, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': msg}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

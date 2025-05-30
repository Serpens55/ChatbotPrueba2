
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
        bienvenida = {
            'text': "Un saludo amigo, yo soy Cientibot, tu asistente virtual. ¿En qué puedo ayudarte?",
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)

@socketio.on('menu_option_selected')
def handle_menu_option(data):
    user_id = request.sid
    option = data.get('option')

    if option == "1":  # Ámbar
        submenu = ["Ámbar Alumnos", "Ámbar Inglés"]
        emit('show_submenu', {'option': option, 'submenu': submenu}, room=user_id)

    elif option == "2":  # Novedades
        bienvenida = {
            'text': "Estas son las novedades de hoy:",
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)

        submenu = ["Novedades1", "Novedades2", "Novedades3"]
        emit('show_submenu', {'option': option, 'submenu': submenu}, room=user_id)

    elif option == "3":  # Convocatorias
        bienvenida = {
            'text': "Estas son las convocatorias que tenemos disponibles en este momento:",
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)

        submenu = ["Convocatoria1", "Convocatoria2", "Convocatoria3"]
        emit('show_submenu', {'option': option, 'submenu': submenu}, room=user_id)

    elif option == "4":  # Mapa
        mensaje = {
            'text': "Aquí tienes el mapa de las instalaciones:",
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Asistente'
        }
        chats[user_id].append(mensaje)
        emit('message', mensaje, room=user_id)
        emit('show_map', {'image': '/static/img/mapa.jpg'}, room=user_id)

    emit('menu_interaction', {
        'user_id': user_id,
        'selection': f"Opción {option}"
    }, broadcast=True)

@socketio.on('submenu_option_selected')
def handle_submenu_option(data):
    user_id = request.sid
    label = data.get('label')

    if label == "Ámbar Alumnos":
        emit('show_link', {'label': label, 'link': 'https://ejemplo.com/ambar-alumnos'}, room=user_id)
    elif label == "Ámbar Inglés":
        emit('show_link', {'label': label, 'link': 'https://ejemplo.com/ambar-ingles'}, room=user_id)
    elif label.startswith("Novedades1"):
        emit('show_link', {'label': f"Título de {label}", 'link': f'https://www.culiacan.tecnm.mx/se-realiza-con-exito-el-evento-ingeniatec-2025-en-la-extension-navolato-del-itc/'}, room=user_id)
    elif label.startswith("Novedades2"):
        emit('show_link', {'label': f"Título de {label}", 'link': f'https://www.culiacan.tecnm.mx/conoce-el-proceso-de-carga-para-los-cursos-de-verano-2025/'}, room=user_id)
    elif label.startswith("Novedades3"):
        emit('show_link', {'label': f"Título de {label}", 'link': f'https://www.culiacan.tecnm.mx/estudiantes-de-ingenieria-mecanica-desarrollan-biodigestor-para-generar-gas-metano-como-combustible/'}, room=user_id)  

    elif label.startswith("Convocatoria"):
        emit('show_image_link', {
            'label': label,
            'image': f'/static/img/{label.lower()}.jpg',
            'link': f'https://ejemplo.com/{label.lower()}'
        }, room=user_id)

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

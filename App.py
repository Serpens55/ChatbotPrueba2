
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
        'timestamp': time.strftime('%H:%M:%S'),
        'sender': 'Cientibot'
    }

    # Mensaje de audio de bienvenida (usa tu archivo de audio aquí)
    audio_bienvenida = {
        'audio_url': '/static/audio/bienvenida.mp3',  # Asegúrate de tener este archivo
        'timestamp': time.strftime('%H:%M:%S'),
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

    if text == "contacta con un administrador":
        enviar_audio(user_id, 'contactoadmin.mp3')
        bienvenida = {
            'text': "Espera un momento, seras contactado con un administrador en unos segundos para que pueda atenderte",
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)

    if text == "gracias":
        enviar_audio(user_id, 'agradecimiento.mp3')
        bienvenida = {
            'text': "Ha sido un placer ser de ayuda, espero estes satisfecho.",
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Asistente'
        }
        chats[user_id].append(bienvenida)
        emit('message', bienvenida, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)

    if data['text'].strip().lower() == "menudos":
        welcome_msg = {
            'text': 'Selecciona una opción:',
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': 'Cientibot'
        }
        chats[user_id].append(welcome_msg)
        emit('message', welcome_msg, room=user_id)
        emit('message_admin', {'user_id': user_id, 'message': welcome_msg}, broadcast=True)

        # Instrucción para el cliente para mostrar el menú raíz
        emit('show_menu', {'options': ["Ambar", "Novedades", "Convocatorias", "Mapa"]}, room=user_id)


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
        emit('show_map', {'image': '/static/img/mapa.png'}, room=user_id)

    emit('menu_interaction', {
        'user_id': user_id,
        'selection': f"Opción {option}"
    }, broadcast=True)

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
        'timestamp': time.strftime('%H:%M:%S'),
        'sender': 'Cientibot'
    }
    
    chats.setdefault(user_id, []).append(bienvenida)
    emit('message', bienvenida, room=user_id)
    emit('message_admin', {'user_id': user_id, 'message': bienvenida}, broadcast=True)


@socketio.on('submenu_option_selected')
def handle_submenu_option(data):
    user_id = request.sid
    label = data.get('label')

    if label == "Ámbar Alumnos":
        emit('show_link', {'label': label, 'link': 'https://culiacan.ambar.tecnm.mx/auth/Account/Login?ReturnUrl=%2Fauth%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Destudiantes-spa%26redirect_uri%3Dhttps%3A%2F%2Fculiacan.ambar.tecnm.mx%2Festudiantes%2Foidc-callback%26response_type%3Dcode%26scope%3Dopenid%20profile%20api-planteles%20api-escolares%20offline_access%26state%3D3617484454ef473bbc348d742c7706f2%26code_challenge%3DBrjSrHqYVowU7OV3VQLHVKrNnLbqbYktGjjGiBBNhdA%26code_challenge_method%3DS256%26response_mode%3Dquery'}, room=user_id)
    elif label == "Ámbar Inglés":
        emit('show_link', {'label': label, 'link': 'https://culiacan.ambar.tecnm.mx/auth/Account/Login?ReturnUrl=%2Fauth%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Destudiantes-spa%26redirect_uri%3Dhttps%3A%2F%2Fculiacan.ambar.tecnm.mx%2Festudiantes%2Foidc-callback%26response_type%3Dcode%26scope%3Dopenid%20profile%20api-planteles%20api-escolares%20offline_access%26state%3Dba41363f5e754f43b947700513e51d0e%26code_challenge%3D5TK7QinRwgvTRRqc49ueqOifCl7e3Zg3fEr4g4O3Ln8%26code_challenge_method%3DS256%26response_mode%3Dquery'}, room=user_id)
    elif label.startswith("Novedades1"):
        emit('show_link', {'label': f"Evento Ingeniatec 2025", 'link': f'https://www.culiacan.tecnm.mx/se-realiza-con-exito-el-evento-ingeniatec-2025-en-la-extension-navolato-del-itc/'}, room=user_id)
    elif label.startswith("Novedades2"):
        emit('show_link', {'label': f"Proceso de carga de cursos de verano", 'link': f'https://www.culiacan.tecnm.mx/conoce-el-proceso-de-carga-para-los-cursos-de-verano-2025/'}, room=user_id)
    elif label.startswith("Novedades3"):
        emit('show_link', {'label': f"Estudiantes  de ingenieria desarrollan biodigestor", 'link': f'https://www.culiacan.tecnm.mx/estudiantes-de-ingenieria-mecanica-desarrollan-biodigestor-para-generar-gas-metano-como-combustible/'}, room=user_id)  

    elif label.startswith("Convocatoria1"):
        emit('show_image_link', {
            'label': 'Convocatoria abierta de plazas docentes febrero 2025',
            'image': f'/static/img/conv1.png',
            'link': f'https://www.culiacan.tecnm.mx/participa-en-la-convocatoria-abierta-de-plazas-docentes-febrero-2025/'
        }, room=user_id)
    elif label.startswith("Convocatoria2"):
        emit('show_image_link', {
            'label': 'Convocatoria abierta no docente',
            'image': f'/static/img/conv2.png',
            'link': f'https://www.culiacan.tecnm.mx/participa-en-la-convocatoria-abierta-no-docente/'
        }, room=user_id)        
    elif label.startswith("Convocatoria3"):
        emit('show_image_link', {
            'label': 'Convocatorias cerradas plazas administrativas 2025',
            'image': f'/static/img/conv3.png',
            'link': f'https://www.culiacan.tecnm.mx/convocatorias-cerradas-plazas-administrativas-febrero-2025/'
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




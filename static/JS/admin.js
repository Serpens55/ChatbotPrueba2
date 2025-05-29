const socket = io(); 
const chatList = document.getElementById("chat-list");
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("admin-message");
const sendButton = document.getElementById("send-admin");

let selectedChat = null;
let adminId = "Admin"; // Identificador fijo para el administrador

// Enviar mensaje al presionar botón o Enter
sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") sendMessage();
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "" && selectedChat) {
        const messageData = {
            user_id: selectedChat,
            text: message,
            sender: adminId
        };

        // Mostrar mensaje localmente
        displayMessage(messageData, true);

        // Enviar al servidor
        socket.emit("admin_message", messageData);

        // Limpiar input
        messageInput.value = "";
    }
}

function displayMessage(data, isLocal = false) {
    const messageElement = document.createElement("div");

    const senderIsAdmin = data.sender === "Admin" || data.sender === adminId;
    const senderLabel = isLocal || senderIsAdmin ? "Tú" : data.sender;

    if (data.audio_url) {
        const button = document.createElement("button");
        button.textContent = ` ${senderLabel}: Reproducir audio`;
        button.onclick = () => {
            const audio = new Audio(data.audio_url);
            audio.play();
        };
        messageElement.appendChild(button);
    } else {
        messageElement.textContent = `${senderLabel}: ${data.text}`;
    }

    messageElement.classList.add(senderIsAdmin ? "own-message" : "other-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Actualizar lista de clientes conectados
socket.on("update_chat_list", function (clients) {
    chatList.innerHTML = "";
    clients.forEach(client => {
        const name = client.name || client.user_id;
        const clientElement = document.createElement("button");
        clientElement.textContent = "Chat con " + name;
        clientElement.classList.add("chat-button");
        clientElement.addEventListener("click", function () {
            selectedChat = client.user_id;
            document.getElementById("selected-user").textContent = name;
            socket.emit("admin_select_chat", { user_id: selectedChat });
        });
        chatList.appendChild(clientElement);
    });
});

// Mostrar historial del chat seleccionado
socket.on("chat_history", function (messages) {
    chatBox.innerHTML = "";
    messages.forEach(msg => displayMessage(msg));
});

// Mostrar nuevos mensajes del cliente o del sistema
socket.on("message_admin", function (data) {
    if (selectedChat === data.user_id) {
        displayMessage({
            text: data.message.text,
            sender: data.message.sender,
            timestamp: data.message.timestamp,
            audio_url: data.message.audio_url || null
        });
    }
});
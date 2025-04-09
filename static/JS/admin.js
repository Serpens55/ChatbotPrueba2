const socket = io(); 
const chatList = document.getElementById("chat-list");
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("admin-message");
const sendButton = document.getElementById("send-admin");
let selectedChat = null;
let adminId = "admin"; // Identificador fijo para el administrador

sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "" && selectedChat) {
        const messageData = { user_id: selectedChat, text: message, sender: adminId };
        
        // Mostrar mensaje inmediatamente en la interfaz
        displayMessage(messageData, true);
        
        // Enviar mensaje al servidor
        socket.emit("admin_message", messageData);

        // Limpiar el campo de entrada
        messageInput.value = "";
    }
}

function displayMessage(data, isLocal = false) {
    console.log("Mensaje recibido para mostrar:", data); // Depuración

    const messageElement = document.createElement("div");
    messageElement.textContent = (data.sender === adminId ? "Tú: " : "Cliente: ") + data.text;
    messageElement.classList.add(data.sender === adminId ? "own-message" : "other-message"); 
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Marcar los mensajes locales para evitar duplicaciones cuando regresen del servidor
    if (isLocal) {
        messageElement.dataset.local = "true";
    }
}

socket.on("update_chat_list", function (clients) {
    chatList.innerHTML = "";
    clients.forEach(client => {
        const clientElement = document.createElement("button");
        clientElement.textContent = "Chat con " + client;
        clientElement.classList.add("chat-button");
        clientElement.addEventListener("click", function () {
            selectedChat = client;
            document.getElementById("selected-user").textContent = client;
            socket.emit("admin_select_chat", { user_id: client });
        });
        chatList.appendChild(clientElement);
    });
});

socket.on("chat_history", function (messages) {
    chatBox.innerHTML = "";
    messages.forEach(msg => displayMessage(msg));
});

socket.on("message_admin", function (data) {
    console.log("Mensaje recibido en el admin:", data); // Verificar estructura

    // Verificar si el mensaje ya fue mostrado localmente
    const existingMessages = Array.from(chatBox.children);
    const isDuplicate = existingMessages.some(msgEl => msgEl.textContent.includes(data.message.text) && msgEl.dataset.local === "true");

    if (!isDuplicate && selectedChat === data.user_id) {
        displayMessage({ text: data.message.text, sender: adminId });
    }
});


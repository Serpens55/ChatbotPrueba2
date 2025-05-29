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
    const messageElement = document.createElement("div");

    if (data.audio_url) {
        const button = document.createElement("button");
        button.textContent = data.text || "Reproducir audio";
        button.addEventListener("click", () => {
            const audio = new Audio(data.audio_url);
            audio.play();
        });
        messageElement.appendChild(button);
    } else {
    messageElement.textContent = `${data.sender}: ${data.text}`;
    }

    messageElement.classList.add(data.sender === adminId ? "own-message" : "other-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;

    if (isLocal) {
        messageElement.dataset.local = "true";
    }
}

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

}
);


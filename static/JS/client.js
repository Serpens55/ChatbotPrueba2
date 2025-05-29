const socket = io();
let userId = null;
let userName = null;

socket.on("connect", function () {
    socket.emit("register_name", { name: userName });
});

window.onload = function () {
    userName = prompt("Ingresa tu nombre:");
    if (!userName) userName = "Invitado";
    
    socket.emit("register_name", { name: userName });
};

socket.on("connected", function (data) {
    console.log("Conectado con ID:", data.user_id);
    userId = data.user_id;
    document.getElementById("user-id").textContent = userId;
    socket.emit("join");
}); 

const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send");

sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "") {
        socket.emit("message", { text: message }); // Solo enviamos el mensaje
        messageInput.value = ""; // Limpiamos el input después de enviarlo
    }
}

socket.on("message", function (data) {
    const messageElement = document.createElement("div");

    if (data.audio_url) {
        // Si hay un audio, crea un botón para reproducirlo
        const button = document.createElement("button");
        button.textContent = data.text || "Reproducir ▶";
        button.addEventListener("click", () => {
            const audio = new Audio(data.audio_url);
            audio.play();
        });
        messageElement.appendChild(button);
    } else {
        // Mensaje de texto normal
           messageElement.textContent = `${data.sender}: ${data.text} (${data.timestamp})`;
    }

    messageElement.classList.add(data.sender === userName ? "own-message" : "other-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});


;


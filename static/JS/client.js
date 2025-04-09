const socket = io();
let userId = null;

socket.on("connected", function (data) {
    console.log("User connected with ID:", data.user_id);  // Añade un log para comprobar
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
    messageElement.textContent = (data.sender === "cliente" ? "Tú: " : "Admin: ") + data.text + " (" + data.timestamp + ")";
    messageElement.classList.add(data.sender === "cliente" ? "own-message" : "other-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});

;


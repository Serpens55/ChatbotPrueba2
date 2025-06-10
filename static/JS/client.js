const socket = io();
let userId = null;
let userName = null;

window.addEventListener("DOMContentLoaded", () => {
    userName = prompt("Ingresa tu nombre:");
    if (!userName) userName = "Invitado";

    document.getElementById("user-name").textContent = userName;
    socket.emit("register_name", { name: userName });
});

socket.on("connected", function (data) {
    userId = data.user_id;
    socket.emit("join");
});

const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send");

sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") sendMessage();
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "") {
        socket.emit("message", { text: message });
        messageInput.value = "";
    }
}

socket.on("message", function (data) {
    const messageElement = document.createElement("div");

    if (data.audio_url) {

        
        const button = document.createElement("button");
        button.textContent = data.text || "Reproducir ▶";
        button.addEventListener("click", () => {
            const audio = new Audio(data.audio_url);
            audio.play();
        });
        messageElement.appendChild(button);
    } else {
        messageElement.textContent = `${data.sender}: ${data.text} (${data.timestamp})`;
    }

    messageElement.classList.add(data.sender === userName ? "own-message" : "other-message");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_menu", () => {
    const menuContainer = document.createElement("div");
    menuContainer.classList.add("other-message", "menu-container");

    const message = document.createElement("div");
    message.classList.add("menu-message");
    message.textContent = "Mensaje de prueba que va antes del menú:";
    menuContainer.appendChild(message);

    for (let i = 1; i <= 4; i++) {
        const btn = document.createElement("button");
        btn.textContent = `Opción ${i}`;
        btn.classList.add("menu-button");
        btn.onclick = () => {
            socket.emit("menu_option_selected", { option: String(i) });
        };
        menuContainer.appendChild(btn);
    }

    chatBox.appendChild(menuContainer);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_submenu", (data) => {
    const submenuContainer = document.createElement("div");
    submenuContainer.classList.add("other-message", "submenu-container");

    const message = document.createElement("div");
    message.classList.add("menu-message");
    message.textContent = `Opciones disponibles para ${data.option}:`;
    submenuContainer.appendChild(message);

    data.submenu.forEach((label) => {
        const btn = document.createElement("button");
        btn.textContent = label;
        btn.classList.add("submenu-button");
        submenuContainer.appendChild(btn);
    });

    chatBox.appendChild(submenuContainer);
    chatBox.scrollTop = chatBox.scrollHeight;
});
 

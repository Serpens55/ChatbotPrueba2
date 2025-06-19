const socket = io();
let userId = null;
let userName = null;

window.addEventListener("DOMContentLoaded", () => {
    userName = prompt("Ingresa tu nombre:");
    if (!userName) userName = "Invitado";

    document.getElementById("user-name").textContent = userName;
    socket.emit("register_name", { name: userName });
});

socket.on("connected", (data) => {
    userId = data.user_id;
    socket.emit("join");
});

const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send");

sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") sendMessage();
});

function getCurrentTimestamp() {
    return new Date().toLocaleString();
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "") {
        socket.emit("message", {
            text: message,
            timestamp: getCurrentTimestamp()
        });
        messageInput.value = "";
    }
}

function clearMenus() {
    document.querySelectorAll(".menu-container, .submenu-container, .info-container, .image-container").forEach(el => el.remove());
}

function createButton(label, id, className, emitEvent) {
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.classList.add(className);
    btn.onclick = () => {
        clearMenus();
        socket.emit(emitEvent, { id });
    };
    return btn;
}

function addReturnButton() {
    const returnBtn = createButton("🔙 Regresar al menú principal", "menu", "menu-button", "message");
    const container = document.createElement("div");
    container.classList.add("menu-container");
    container.appendChild(returnBtn);
    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
}

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
            socket.emit("menu_option_selected", { id: item.id }); // ✅ ENVÍA id correcto
        };
        menuContainer.appendChild(btn);
    }

    chatBox.appendChild(menuContainer);
    chatBox.scrollTop = chatBox.scrollHeight;
});



socket.on("show_submenu", (data) => {
    document.querySelectorAll(".submenu-container").forEach(el => el.remove());

    const submenuContainer = document.createElement("div");
    submenuContainer.classList.add("other-message", "submenu-container");

    data.submenu.forEach((item) => {
        const btn = document.createElement("button");
        btn.textContent = item.label;
        btn.classList.add("submenu-button");

        btn.onclick = () => {
            socket.emit("submenu_option_selected", { id: item.id }); // ✅ ENVÍA id
        };

        submenuContainer.appendChild(btn);
    });

    chatBox.appendChild(submenuContainer);
    chatBox.scrollTop = chatBox.scrollHeight;
});


socket.on("show_info", (data) => {
    clearMenus();

    const container = document.createElement("div");
    container.classList.add("info-container", "other-message");

    const title = document.createElement("strong");
    title.textContent = data.label;
    container.appendChild(title);

    const text = document.createElement("p");
    text.textContent = data.text;
    container.appendChild(text);

    chatBox.appendChild(container);
    addReturnButton();
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_map", (data) => {
    clearMenus();

    const container = document.createElement("div");
    container.classList.add("image-container", "other-message");

    const img = document.createElement("img");
    img.src = data.image;
    img.alt = "Mapa de instalaciones";
    container.appendChild(img);

    chatBox.appendChild(container);
    addReturnButton();
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("message", (data) => {
    const messageElement = document.createElement("div");

    if (data.audio_url) {
        const button = document.createElement("button");
        button.textContent = data.text || "Reproducir ▶";
        button.classList.add("menu-button");
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
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
    const returnBtn = document.createElement("button");
    returnBtn.textContent = "Regresar al menú principal";
    returnBtn.classList.add("return-button");
    returnBtn.onclick = () => {
        socket.emit("return_to_main_menu");
    };

    const container = document.querySelector(".submenu-container");
    if (container) {
        container.appendChild(returnBtn);
    }
}


socket.on("show_menu", () => {
    clearMenus();

    const menuOptions = [
        { id: "menu_ambar", label: "Ambar" },
        { id: "menu_asp", label: "Aspirantes" },
        { id: "menu_ofe", label: "Oferta Educativa" },
        { id: "menu_est", label: "Estudiantes" },
        { id: "menu_map", label: "Mapa" }
    ];

    const container = document.createElement("div");
    container.classList.add("menu-container");

    const title = document.createElement("div");
    title.classList.add("menu-message");
    title.textContent = "Menú Principal";
    container.appendChild(title);

    menuOptions.forEach(opt => {
        const btn = createButton(opt.label, opt.id, "menu-button", "menu_option_selected");
        container.appendChild(btn);
    });

    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_submenu", (data) => {
    clearMenus();

    const container = document.createElement("div");
    container.classList.add("submenu-container");

    data.submenu.forEach(item => {
        const btn = createButton(item.label, item.id, "submenu-button", "submenu_option_selected");
        container.appendChild(btn);
    });

    chatBox.appendChild(container);
    addReturnButton();
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_link", (data) => {
    clearMenus();

    const container = document.createElement("div");
    container.classList.add("submenu-container");

    const link = document.createElement("a");
    link.href = data.link;
    link.target = "_blank";
    link.textContent = data.label;
    link.classList.add("submenu-button");

    container.appendChild(link);
    chatBox.appendChild(container);
    addReturnButton();
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
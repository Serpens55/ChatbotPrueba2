const socket = io();
let userId = null;
let userName = null;
let menuFlow = [];

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
    return new Date().toLocaleString(); // Fecha y hora local del navegador
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== "") {
        socket.emit("message", { text: message,
        timestamp: getCurrentTimestamp()   
         });
        messageInput.value = "";
  
    }
}

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

function updateFlowDisplay() {
    const flowContainer = document.getElementById("navigation-flow");
    flowContainer.innerHTML = "";
    menuFlow.forEach(item => {
        const el = document.createElement("div");
        el.textContent = item;
        el.classList.add("flow-item");
        flowContainer.appendChild(el);
    });
}

socket.on("show_menu", () => {
    const menuContainer = document.createElement("div");
    menuContainer.classList.add("other-message", "menu-container");

    const message = document.createElement("div");
    message.classList.add("menu-message");
    message.innerHTML = "<strong>Menu Principal</strong><br>Selecciona una opción";
    menuContainer.appendChild(message);

    const menuOptions = [
        {
            label: "Aspirantes",
            submenu: ["Proceso de Reinscripcion"]
        },
        {
            label: "Oferta Educativa",
            submenu: ["Licenciaturas", "Posgrados", "Coordinacion de LE"]
        },
        {
            label: "Estudiantes",
            submenu: ["Centro de Informacion", "Division de Estudios Profesionales", "Desarrollo Academico", "Servicios Escolares"]
        },
        {
            label: "Mapa",
            submenu: null // Este muestra una imagen
        }
    ];

    menuOptions.forEach(opt => {
        const btn = document.createElement("button");
        btn.textContent = opt.label;
        btn.classList.add("menu-button");

                btn.onclick = () => {
                    // 🔥 Eliminar TODOS los submenús antes de abrir otro
                    document.querySelectorAll(".submenu-container").forEach(el => el.remove());

                    const existing = document.getElementById(`submenu-${opt.label}`);
                    if (existing) {
                        existing.remove(); // Si ya estaba abierto, lo cierra (toggle)
                        return;
                    }

                    const submenuDiv = document.createElement("div");
                    submenuDiv.id = `submenu-${opt.label}`;
                    submenuDiv.classList.add("submenu-container");

                    opt.submenu.forEach(sub => {
                        const subBtn = document.createElement("button");
                        subBtn.textContent = sub;
                        subBtn.classList.add("submenu-button");
                        subBtn.onclick = () => {
                            socket.emit("submenu_option_selected", { label: sub });
                        };
                        submenuDiv.appendChild(subBtn);
                    });

                    btn.insertAdjacentElement("afterend", submenuDiv);
                };

        menuContainer.appendChild(btn);
    });

    chatBox.appendChild(menuContainer);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_image_link", (data) => {
    const container = document.createElement("div");
    container.classList.add("other-message");

    const label = document.createElement("div");
    label.textContent = data.label;
    label.style.fontWeight = "bold";
    label.style.marginBottom = "5px";

    const img = document.createElement("img");
    img.src = data.image;
    img.alt = data.label;
    img.style.maxWidth = "100%";
    img.style.marginBottom = "5px";

    const link = document.createElement("a");
    link.href = data.link;
    link.target = "_blank";
    link.textContent = "Ver más";
    link.classList.add("submenu-button");

    container.appendChild(label);
    container.appendChild(img);
    container.appendChild(link);
    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_map", (data) => {
    const container = document.createElement("div");
    container.classList.add("other-message");

    const img = document.createElement("img");
    img.src = data.image;
    img.alt = "Mapa de instalaciones";
    img.style.maxWidth = "100%";

    container.appendChild(img);
    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("show_submenu", (data) => {
    // ❌ Eliminar todos los submenús anteriores
    document.querySelectorAll(".submenu-container").forEach(el => el.remove());

    // ✅ Crear nuevo submenú
    const submenuContainer = document.createElement("div");
    submenuContainer.classList.add("other-message", "submenu-container");

    data.submenu.forEach((label) => {
        const btn = document.createElement("button");
        btn.textContent = label;
        btn.classList.add("submenu-button");
        btn.onclick = () => {
            socket.emit("submenu_option_selected", { label });
        };
        submenuContainer.appendChild(btn);
    });

    chatBox.appendChild(submenuContainer);
    chatBox.scrollTop = chatBox.scrollHeight;
});

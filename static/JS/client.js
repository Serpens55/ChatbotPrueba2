const socket = io();
let userId = null;
let userName = null;

const menuStructure = {
  "Menu": ["Ambar", "Novedades", "Convocatorias", "Mapa"],
  "Ambar": ["Ambar Alumnos", "Ambar Ingles"],
  "Novedades": ["Novedad 1", "Novedad 2", "Novedad 3"],
  "Convocatorias": ["Convocatoria 1", "Convocatoria 2", "Convocatoria 3"]
};

let menuStack = [];

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
 
function displayInteractiveMenu(options, level = 0) {
    const container = document.createElement("div");
    container.classList.add("menu-options");

    options.forEach(option => {
        const button = document.createElement("button");
        button.textContent = option.label;
        button.classList.add("menu-button");
        button.onclick = () => {
            // Mostrar el flujo de navegación
            const history = document.createElement("div");
            history.textContent = "> " + option.label;
            history.classList.add("menu-path");
            chatBox.appendChild(history);
            chatBox.scrollTop = chatBox.scrollHeight;

            if (option.children) {
                displayInteractiveMenu(option.children, level + 1);
            } else if (option.callback) {
                option.callback();
            }
        };
        container.appendChild(button);
    });

    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
}



function renderMenu(options) {
  const chatBox = document.getElementById("chat-box");
  const menuContainer = document.createElement("div");
  menuContainer.classList.add("menu-container");

  options.forEach(option => {
    const button = document.createElement("button");
    button.textContent = option;
    button.classList.add("menu-button");
    button.onclick = () => handleMenuSelection(option);
    menuContainer.appendChild(button);
  });

  chatBox.appendChild(menuContainer);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function handleMenuSelection(option) {
  menuStack.push(option);
  displayMessage({ text: `Seleccionaste: ${option}`, sender: "Tú" });

  if (option === "Mapa") {
    displayImage("/static/imagenes/mapa.jpg");
  } else if (menuStructure[option]) {
    renderMenu(menuStructure[option]);
  } else {
    socket.emit("message", { text: option });
  }
}

function displayImage(src) {
  const chatBox = document.getElementById("chat-box");
  const img = document.createElement("img");
  img.src = src;
  img.style.maxWidth = "100%";
  chatBox.appendChild(img);
}

socket.on("show_menu", function(data) {
  renderMenu(data.options);
});

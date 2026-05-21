const messagesEl = document.getElementById("messages"); //Scrollable message list
const input = document.getElementById("messageInput"); //Text input field
const sendBtn = document.getElementById("sendBtn"); //Send button
const statusEl = document.getElementById("status"); //Connected/disconnected

const socket = io();

//Runs once WebSocket handshake with server succeeds
socket.on("connect", () => {
    statusEl.textContent = "Connected";
    statusEl.className = "status online";
});

//Runs if connection drops
socket.on("disconnect", () => {
    statusEl.textContent = "Disconnected";
    statusEl.className = "status offline";
});

//Receive chat history
socket.on("history", (messages) => {
    messagesEl.innerHTML = ""; //Clears previous content
    messages.forEach(renderMessage);
    scrollToBottom();
});

//Receive a new message
socket.on("message", (data) => {
    renderMessage(data);
    scrollToBottom();
});

function sendMessage() {
    const text = input.value.trim();

    //If text is blank
    if (!text) {
        return;
    }

    socket.emit("message", { message: text });

    input.value = ""; //Clears input once message is sent
}

sendBtn.addEventListener("click", sendMessage); //Message is sent once send button pressed

//Press enter to send
input.addEventListener("keydown", (e) => {
    if (e.key == "Enter" && !e.shiftKey) { //Enter + shift to not send
        e.preventDefault();

        sendMessage();
    }
});

function renderMessage({ email, message, timestamp }) {
    const div = document.createElement("div"); //Creates new div for message bubble
    div.className = "message";

    //If there is no timestamp
    const time = timestamp
        ? new Date(timestamp + "Z").toLocaleTimeString([], { hour: "2-digit", minute: "2-digit"})
        : new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit"});

    div.innerHTML = `
        <span class="msg-email">${escapeHTML(email)}</span>
        <span class="msg-time">${time}</span>
        <p class="msg-text">${escapeHTML(message)}</p>
    `;

    messagesEl.appendChild(div); //Append finished bubble to the list
}

//Forces container to bottom
function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

//Replaces characters which have a special meaning in HTML
function escapeHTML(str) {
  return str
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/"/g,  "&quot;")
    .replace(/'/g,  "&#039;");
}




let currentSessionId = null;

async function loadChatSessions() {
    const res = await fetch("/api/sessions/");
    const data = await res.json();
    const historyList = document.getElementById("history-list");
    historyList.innerHTML = "";

    data.sessions.forEach(session => {
        const li = document.createElement("li");
        li.textContent = `${session.created_at}: ${ session.title || session.preview}`;
        li.classList.add("history-item", "py-2", "border-bottom", "history-hover");
        li.dataset.sessionId = session.id;

        li.addEventListener("click", () => {
            loadChatMessages(session.id);
            currentSessionId = session.id;

            // Đánh dấu active
            document.querySelectorAll(".history-item").forEach(item => item.classList.remove("active"));
            li.classList.add("active");
        });

        historyList.appendChild(li);
    });
}

async function loadChatMessages(sessionId) {
    const res = await fetch(`/api/messages/${sessionId}/`);
    const data = await res.json();

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";
    data.messages.forEach(msg => {
        appendMessage(msg.sender === "user" ? "Bạn" : "Bot", msg.message, msg.sender);
    });
    currentSessionId = sessionId;
}

window.addEventListener("load", loadChatSessions);

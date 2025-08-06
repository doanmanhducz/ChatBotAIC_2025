document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");

    chatForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        appendMessage("Bạn", userMessage, "user");
        messageInput.value = "";

        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                message: userMessage,
                session_id: currentSessionId
            })
        });

        const data = await response.json();
        appendMessage("Bot", data.reply, "bot");

        if (!currentSessionId && data.session_id) {
            currentSessionId = data.session_id;
        }

        await loadChatSessions();
    });

    function getCSRFToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }
});
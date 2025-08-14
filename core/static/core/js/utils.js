function appendMessage(sender, message, type) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("mb-3", type === "user" ? "text-end" : "text-start");

    const formattedMessage = message.replace(/\n/g, "<br>");

    msgDiv.innerHTML = `
        <div class="d-inline-block p-2 rounded ${type === 'user' ? 'bg-primary text-white' : 'bg-secondary text-white'}">
            <strong>${sender}:</strong> ${formattedMessage}
        </div>
    `;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}



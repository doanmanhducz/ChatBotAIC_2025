async function loadChatSessions() {
    const res = await fetch("/api/sessions/");
    const data = await res.json();
    const historyList = document.getElementById("history-box");
    historyList.innerHTML = "";

    data.sessions.forEach(session => {
        const li = document.createElement("li");
        li.className = "history-item py-2 border-bottom history-hover d-flex justify-content-between align-items-center";
        li.dataset.sessionId = session.id;

        // text hiển thị
        const span = document.createElement("span");
        span.textContent = `${session.created_at}: ${ session.title || session.preview}`;
        span.classList.add("flex-grow-1");

        // nút xoá
        const delBtn = document.createElement("button");
        delBtn.className = "btn btn-sm btn-danger delete-btn";
        delBtn.innerHTML = "✖";

        // sự kiện xoá phiên
        delBtn.addEventListener("click", async (e) => {
            e.stopPropagation();
            if (confirm("Bạn có chắc muốn xóa phiên này?")) {
                 const res = await fetch(`/api/sessions/${session.id}/delete/`, { method: "DELETE" });
                const data = await res.json();
                if (data.success) {
                    window.location.reload();  
                } else {
                    alert("Xóa thất bại: " + (data.error || ""));
                }
            }
        });

        // sự kiện click cả dòng li => load tin nhắn
        li.addEventListener("click", () => {
            loadChatMessages(session.id);
            currentSessionId = session.id;

            document.querySelectorAll(".history-item").forEach(item => item.classList.remove("active"));
            li.classList.add("active");
        });

        li.appendChild(span);
        li.appendChild(delBtn);
        historyList.appendChild(li);
    });
}

window.addEventListener("load", loadChatSessions);

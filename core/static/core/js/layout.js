document.addEventListener("DOMContentLoaded", function () {
    const toggleSidebarBtn = document.getElementById('toggle-sidebar');
    const historyBox = document.getElementById('history-box');
    const chatLayout = document.getElementById('chat-layout');
    const mainCol = chatLayout.querySelector('.col-9, .col-12');

    let isSidebarVisible = true;

    toggleSidebarBtn.addEventListener('click', () => {
        isSidebarVisible = !isSidebarVisible;

        if (isSidebarVisible) {
            historyBox.classList.remove('d-none');
            historyBox.classList.add('d-block');
            mainCol.classList.remove('col-12');
            mainCol.classList.add('col-9');
        } else {
            historyBox.classList.remove('d-block');
            historyBox.classList.add('d-none');
            mainCol.classList.remove('col-9');
            mainCol.classList.add('col-12');
        }
    });
});
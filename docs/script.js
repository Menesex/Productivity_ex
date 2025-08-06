const listsContainer = document.getElementById('lists-container');

function addList() {
    const name = document.getElementById('new-list-name').value.trim();
    if (!name) return;

    const list = document.createElement('div');
    list.className = 'list';
    list.innerHTML = `
        <h3>${name}</h3>
        <div class="tasks"></div>
        <form class="add-task" onsubmit="return addTask(event, this)">
            <input type="text" placeholder="Nueva tarea..." required />
            <button type="submit">Agregar</button>
        </form>
    `;
    listsContainer.appendChild(list);
    document.getElementById('new-list-name').value = '';
}

function addTask(event, form) {
    event.preventDefault();
    const input = form.querySelector('input');
    const value = input.value.trim();
    if (!value) return;

    const task = document.createElement('div');
    task.className = 'task';
    task.innerHTML = `
        <div class="checkbox" onclick="toggleCheck(this)">✔️</div>
        <div class="task-content" onclick="toggleExpand(this)">
            <div class="task-title">${value}</div>
            <div class="task-details">Detalles: Puedes editar esto más adelante.</div>
        </div>
    `;

    form.parentElement.querySelector('.tasks').appendChild(task);
    input.value = '';
}

function toggleCheck(el) {
    el.classList.toggle('checked');
}

function toggleExpand(el) {
    const taskDiv = el.closest('.task');
    taskDiv.classList.toggle('expanded');
}

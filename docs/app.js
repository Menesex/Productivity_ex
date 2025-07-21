const API = 'http://localhost:5000';

const board = document.getElementById('board');
let listMap = {}; // folder_id -> HTML element

// Cargar listas y tareas desde el backend
async function loadData() {
    const foldersRes = await fetch(`${API}/folders`);
    const folders = await foldersRes.json();

    const tasksRes = await fetch(`${API}/tasks`);
    const tasks = await tasksRes.json();

    folders.forEach((folder, index) => {
        const list = createList(folder.nombre, folder.id);
        board.appendChild(list);
        listMap[folder.id] = list.querySelector('.task-container');
    });

    tasks.forEach(task => {
        const el = createTaskElement(task);
        listMap[task.folder_id]?.appendChild(el);
    });
}

function createList(name, folderId) {
    const div = document.createElement('div');
    div.className = 'list';
    div.innerHTML = `
    <h2>${name}</h2>
    <div class="task-container" id="tasks-${folderId}"></div>
    <button onclick="addTask(${folderId})">+ Nueva tarea</button>
  `;
    return div;
}

function createTaskElement(task) {
    const el = document.createElement('div');
    el.className = 'task';
    el.innerHTML = `
    <label style="display:flex; align-items:center; gap:0.5rem;">
      <input type="checkbox" ${task.completada ? 'checked' : ''} onchange="toggleComplete(${task.id}, this)">
      <div class="content">
        <strong>${task.titulo}</strong>
        <small>${task.descripcion}</small>
      </div>
    </label>
  `;
    el.querySelector('.content').addEventListener('click', () => {
        el.querySelector('.content').classList.toggle('expanded');
    });
    return el;
}

async function toggleComplete(taskId, checkbox) {
    await fetch(`${API}/tasks/${taskId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completada: checkbox.checked })
    });
}

async function addTask(folderId) {
    const titulo = prompt("Título:");
    if (!titulo) return;
    const descripcion = prompt("Descripción:") || "";

    const res = await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titulo, descripcion, completada: false, folder_id: folderId })
    });

    const data = await res.json();
    const task = { id: data.id, titulo, descripcion, completada: false, folder_id: folderId };
    listMap[folderId].appendChild(createTaskElement(task));
}

async function addList() {
    const nameInput = document.getElementById('list-name');
    const name = nameInput.value.trim();
    if (!name) return;

    const res = await fetch(`${API}/folders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: name })
    });

    const data = await res.json();
    const list = createList(name, data.id);
    board.appendChild(list);
    listMap[data.id] = list.querySelector('.task-container');
    nameInput.value = '';
}

loadData();

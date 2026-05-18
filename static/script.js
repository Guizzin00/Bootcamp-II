document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskTitleInput = document.getElementById('task-title');
    const taskList = document.getElementById('task-list');
    
    // Weather Widget elements
    const adviceLoader = document.getElementById('advice-loader');
    const adviceContent = document.getElementById('advice-content');
    const adviceMessage = document.getElementById('advice-message');
    const weatherIcon = document.querySelector('.weather-icon');
    const weatherDate = document.getElementById('weather-date');
    const weatherTemp = document.getElementById('weather-temp');

    // Load initial data
    loadTasks();
    loadWeatherAndAdvice();

    // Event Listeners
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = taskTitleInput.value.trim();
        if (title) {
            await addTask(title);
            taskTitleInput.value = '';
        }
    });

    async function loadTasks() {
        try {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            renderTasks(tasks);
        } catch (error) {
            console.error('Erro ao carregar tarefas:', error);
        }
    }

    async function addTask(title) {
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            
            if (response.ok) {
                await loadTasks();
            }
        } catch (error) {
            console.error('Erro ao adicionar tarefa:', error);
        }
    }

    window.toggleTask = async function(id) {
        const item = document.getElementById(`task-${id}`);
        const checkbox = document.getElementById(`cb-${id}`);
        
        if (!checkbox.checked) {
            try {
                const response = await fetch(`/api/tasks/${id}/complete`, { method: 'POST' });
                if (response.ok) {
                    item.classList.add('completed');
                    checkbox.checked = true;
                } else {
                    checkbox.checked = false;
                }
            } catch (error) {
                console.error('Erro ao completar tarefa:', error);
                checkbox.checked = false;
            }
        } else {
            checkbox.checked = true;
        }
    };

    window.removeTask = async function(id) {
        const item = document.getElementById(`task-${id}`);
        item.style.transform = 'scale(0.9)';
        item.style.opacity = '0';
        
        setTimeout(async () => {
            try {
                const response = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
                if (response.ok) {
                    await loadTasks();
                }
            } catch (error) {
                console.error('Erro ao remover tarefa:', error);
                await loadTasks();
            }
        }, 300);
    };

    function renderTasks(tasks) {
        taskList.innerHTML = '';
        
        tasks.sort((a, b) => a.completed === b.completed ? 0 : a.completed ? 1 : -1);
        
        const taskCountEl = document.getElementById('task-count');
        if (taskCountEl) taskCountEl.textContent = tasks.length;

        if (tasks.length === 0) {
            taskList.innerHTML = `
                <div class="empty-state">
                    Nenhuma nota pendente. Tudo limpo! ✨
                </div>
            `;
            return;
        }

        tasks.forEach((task, index) => {
            const div = document.createElement('div');
            div.className = `task-item ${task.completed ? 'completed' : ''}`;
            div.id = `task-${task.id}`;
            
            // Gerar timestamp visual (já que o backend ainda não salva data)
            const now = new Date();
            const dateOptions = { day: 'numeric', month: 'short' };
            const timeOptions = { hour: '2-digit', minute: '2-digit' };
            const dateStr = now.toLocaleDateString('pt-BR', dateOptions);
            const timeStr = now.toLocaleTimeString('pt-BR', timeOptions);
            
            div.innerHTML = `
                <div class="task-header">
                    <div class="task-doc-icon">
                        <i class="fa-regular fa-file-lines"></i>
                    </div>
                    <div class="task-actions">
                        <button class="btn-icon" onclick="toggleTask(${task.id})" title="${task.completed ? 'Desfazer' : 'Concluir'}">
                            <i class="fa-solid ${task.completed ? 'fa-rotate-left' : 'fa-check'}"></i>
                        </button>
                        <button class="btn-icon" onclick="removeTask(${task.id})" title="Remover">
                            <i class="fa-regular fa-trash-can"></i>
                        </button>
                    </div>
                </div>
                <div class="task-title">${escapeHTML(task.title)}</div>
                <div class="task-footer">
                    <span class="task-date">${dateStr}., ${timeStr}</span>
                </div>
            `;
            taskList.appendChild(div);
        });
    }

    async function loadWeatherAndAdvice() {
        try {
            // Display today's date
            const today = new Date();
            const options = { weekday: 'short', day: 'numeric', month: 'short' };
            weatherDate.textContent = today.toLocaleDateString('pt-BR', options);

            // Fetch weather and advice concurrently
            const [weatherRes, adviceRes] = await Promise.all([
                fetch('/api/weather').catch(() => null),
                fetch('/api/advice').catch(() => null)
            ]);

            let tempText = '--°C';
            if (weatherRes && weatherRes.ok) {
                const wData = await weatherRes.json();
                if (wData.status === 'success' && wData.current.temperature !== undefined) {
                    tempText = Math.round(wData.current.temperature) + '°C';
                }
            }
            weatherTemp.textContent = tempText;

            let adviceStatus = 'normal';
            if (adviceRes && adviceRes.ok) {
                const aData = await adviceRes.json();
                adviceStatus = aData.status;
            }

            adviceLoader.style.display = 'none';
            adviceContent.style.display = 'flex';
            
            switch(adviceStatus) {
                case 'hot':
                    adviceMessage.textContent = 'O clima está quente! Dobre sua ingestão de água hoje.';
                    weatherIcon.className = 'fa-solid fa-temperature-arrow-up weather-icon';
                    weatherIcon.style.color = 'var(--danger-color)';
                    break;
                case 'cold':
                    adviceMessage.textContent = 'O clima está frio. Hidrate-se mesmo sem sede e cuide da pele!';
                    weatherIcon.className = 'fa-solid fa-temperature-arrow-down weather-icon';
                    weatherIcon.style.color = '#38bdf8';
                    break;
                case 'normal':
                    adviceMessage.textContent = 'Clima agradável. Mantenha sua rotina normal de saúde e hidratação.';
                    weatherIcon.className = 'fa-solid fa-cloud-sun weather-icon';
                    weatherIcon.style.color = 'var(--success-color)';
                    break;
                default:
                    adviceMessage.textContent = 'Aproveite o seu dia e lembre-se de cuidar de si mesmo!';
                    weatherIcon.className = 'fa-solid fa-sun weather-icon';
                    weatherIcon.style.color = 'var(--note-1)';
            }
            
        } catch (error) {
            console.error('Erro ao carregar clima/dicas:', error);
            adviceLoader.style.display = 'none';
            adviceContent.style.display = 'flex';
            adviceMessage.textContent = 'Erro ao conectar com serviços.';
        }
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
});

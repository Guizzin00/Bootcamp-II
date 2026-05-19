document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskTitleInput = document.getElementById('task-title');
    const taskList = document.getElementById('task-list');
    
    // Weather Widget elements
    const adviceLoader = document.getElementById('advice-loader');
    const adviceContent = document.getElementById('advice-content');
    const weatherIcon = document.querySelector('.weather-icon');
    const weatherDate = document.getElementById('weather-date');
    const weatherTemp = document.getElementById('weather-temp');
    const weatherHumidity = document.getElementById('weather-humidity');
    const weatherCondition = document.getElementById('weather-condition');
    const healthTipsPanel = document.getElementById('health-tips-panel');
    const tipsGrid = document.getElementById('tips-grid');

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

    window.toggleTask = async function(id, event) {
        // Prevent the label from triggering a second click on the checkbox
        if (event) event.preventDefault();
        
        const item = document.getElementById(`task-${id}`);
        const checkbox = document.getElementById(`cb-${id}`);
        
        // Optimistically toggle checkbox visual
        const newState = !checkbox.checked;
        checkbox.checked = newState;
        
        if (newState) {
            item.classList.add('completed');
        } else {
            item.classList.remove('completed');
        }
        
        // Update label text
        const label = item.querySelector('.task-check-label');
        if (label) label.textContent = newState ? 'Concluída' : 'Pendente';
        
        try {
            const response = await fetch(`/api/tasks/${id}/complete`, { method: 'POST' });
            if (!response.ok) {
                // Revert on error
                checkbox.checked = !newState;
                item.classList.toggle('completed');
                if (label) label.textContent = !newState ? 'Concluída' : 'Pendente';
            }
        } catch (error) {
            console.error('Erro ao alternar tarefa:', error);
            checkbox.checked = !newState;
            item.classList.toggle('completed');
            if (label) label.textContent = !newState ? 'Concluída' : 'Pendente';
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
        
        // Sort: uncompleted first, then completed
        tasks.sort((a, b) => a.completed === b.completed ? 0 : a.completed ? 1 : -1);

        if (tasks.length === 0) {
            taskList.innerHTML = `
                <div class="empty-state">
                    Nenhuma nota pendente. Tudo limpo! ✨
                </div>
            `;
            return;
        }

        tasks.forEach((task) => {
            const div = document.createElement('div');
            div.className = `task-item ${task.completed ? 'completed' : ''}`;
            div.id = `task-${task.id}`;
            
            // Timestamp
            const now = new Date();
            const dateOptions = { day: 'numeric', month: 'short' };
            const timeOptions = { hour: '2-digit', minute: '2-digit' };
            const dateStr = now.toLocaleDateString('pt-BR', dateOptions);
            const timeStr = now.toLocaleTimeString('pt-BR', timeOptions);
            
            div.innerHTML = `
                <div class="task-header">
                    <label class="task-check-area" onclick="toggleTask(${task.id}, event)">
                        <div class="custom-checkbox">
                            <input type="checkbox" id="cb-${task.id}" ${task.completed ? 'checked' : ''} tabindex="-1">
                            <span class="checkmark"></span>
                        </div>
                        <span class="task-check-label">${task.completed ? 'Concluída' : 'Pendente'}</span>
                    </label>
                    <div class="task-actions">
                        <button class="btn-icon btn-delete" onclick="removeTask(${task.id})" title="Remover">
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
            const options = { weekday: 'long', day: 'numeric', month: 'short' };
            weatherDate.textContent = today.toLocaleDateString('pt-BR', options);

            // Fetch weather and advice concurrently
            const [weatherRes, adviceRes] = await Promise.all([
                fetch('/api/weather').catch(() => null),
                fetch('/api/advice').catch(() => null)
            ]);

            let temperature = null;
            let humidity = null;

            if (weatherRes && weatherRes.ok) {
                const wData = await weatherRes.json();
                if (wData.status === 'success') {
                    temperature = wData.current.temperature;
                    humidity = wData.current.humidity;
                    
                    if (temperature !== undefined && temperature !== null) {
                        weatherTemp.textContent = Math.round(temperature) + '°C';
                    }
                    if (humidity !== undefined && humidity !== null) {
                        weatherHumidity.textContent = Math.round(humidity) + '%';
                    }
                }
            }

            let adviceStatus = 'normal';
            if (adviceRes && adviceRes.ok) {
                const aData = await adviceRes.json();
                adviceStatus = aData.status;
            }

            adviceLoader.style.display = 'none';
            adviceContent.style.display = 'flex';
            
            // Set weather condition and icon
            setWeatherUI(adviceStatus, temperature, humidity);
            
            // Generate and display health tips
            generateHealthTips(adviceStatus, temperature, humidity);
            
        } catch (error) {
            console.error('Erro ao carregar clima/dicas:', error);
            adviceLoader.style.display = 'none';
            adviceContent.style.display = 'flex';
            weatherCondition.textContent = 'Indisponível';
        }
    }

    function setWeatherUI(status, temp, humidity) {
        let conditionText = '';
        let iconClass = '';
        let iconColor = '';

        switch(status) {
            case 'hot':
                conditionText = 'Quente';
                iconClass = 'fa-solid fa-temperature-arrow-up';
                iconColor = var_danger();
                if (humidity !== null && humidity < 40) conditionText = 'Quente e Seco';
                else if (humidity !== null && humidity > 70) conditionText = 'Quente e Úmido';
                break;
            case 'cold':
                conditionText = 'Frio';
                iconClass = 'fa-solid fa-temperature-arrow-down';
                iconColor = '#38bdf8';
                if (humidity !== null && humidity < 40) conditionText = 'Frio e Seco';
                else if (humidity !== null && humidity > 70) conditionText = 'Frio e Úmido';
                break;
            case 'normal':
            default:
                conditionText = 'Agradável';
                iconClass = 'fa-solid fa-cloud-sun';
                iconColor = var_success();
                if (humidity !== null && humidity < 30) conditionText = 'Ameno mas Seco';
                else if (humidity !== null && humidity > 80) conditionText = 'Ameno e Úmido';
                break;
        }

        weatherCondition.textContent = conditionText;
        weatherIcon.className = iconClass + ' weather-icon';
        weatherIcon.style.color = iconColor;
    }

    function var_danger() { return getComputedStyle(document.documentElement).getPropertyValue('--danger-color').trim() || '#ef4444'; }
    function var_success() { return getComputedStyle(document.documentElement).getPropertyValue('--success-color').trim() || '#22c55e'; }

    function generateHealthTips(status, temp, humidity) {
        const tips = [];

        // Temperature-based tips
        if (status === 'hot') {
            tips.push({ emoji: '💧', text: 'Beba pelo menos 3 litros de água ao longo do dia. Aumente em dias de atividade física.' });
            tips.push({ emoji: '🧴', text: 'Use protetor solar e evite exposição ao sol entre 10h e 16h.' });
            tips.push({ emoji: '🍉', text: 'Consuma frutas ricas em água: melancia, melão, abacaxi e pepino.' });
            tips.push({ emoji: '👕', text: 'Use roupas leves e de cores claras para ajudar na regulação térmica.' });
        } else if (status === 'cold') {
            tips.push({ emoji: '☕', text: 'Hidrate-se mesmo sem sede! Chás e sopas quentes ajudam a manter o corpo aquecido.' });
            tips.push({ emoji: '🧣', text: 'Mantenha-se agasalhado e proteja extremidades como mãos, pés e orelhas.' });
            tips.push({ emoji: '🏃', text: 'Faça exercícios leves em ambientes cobertos para manter a circulação ativa.' });
            tips.push({ emoji: '🍊', text: 'Reforce a vitamina C com laranjas, limões e acerolas para fortalecer a imunidade.' });
        } else {
            tips.push({ emoji: '💧', text: 'Mantenha sua rotina de 2 litros de água por dia. Distribua ao longo das refeições.' });
            tips.push({ emoji: '🚶', text: 'Aproveite o clima ameno para uma caminhada ao ar livre de pelo menos 30 minutos.' });
            tips.push({ emoji: '🥗', text: 'Inclua vegetais frescos e saladas nas refeições para manter o corpo nutrido.' });
            tips.push({ emoji: '😴', text: 'Clima agradável favorece o sono. Tente dormir entre 7 e 8 horas esta noite.' });
        }

        // Humidity-based tips
        if (humidity !== null) {
            if (humidity < 30) {
                tips.push({ emoji: '🏜️', text: `Umidade muito baixa (${Math.round(humidity)}%). Use soro fisiológico nas narinas e um umidificador.` });
                tips.push({ emoji: '👁️', text: 'Ar seco pode irritar os olhos. Use colírio lubrificante se necessário.' });
            } else if (humidity < 40) {
                tips.push({ emoji: '💨', text: `Umidade em ${Math.round(humidity)}%. Mantenha uma toalha úmida no ambiente para aliviar o ar seco.` });
            } else if (humidity > 80) {
                tips.push({ emoji: '🌧️', text: `Umidade alta (${Math.round(humidity)}%). Atenção a mofo em ambientes fechados — ventile a casa.` });
            }
        }

        // Time-of-day tips
        const hour = new Date().getHours();
        if (hour < 10) {
            tips.push({ emoji: '🌅', text: 'Bom dia! Comece o dia com um copo de água morna. Ajuda a ativar o metabolismo.' });
        } else if (hour < 14) {
            tips.push({ emoji: '☀️', text: 'Hora do almoço se aproxima. Prefira refeições leves e não esqueça de se hidratar.' });
        } else if (hour < 18) {
            tips.push({ emoji: '🍵', text: 'Reta final do dia! Um chá ou suco natural pode dar aquele boost de energia.' });
        } else {
            tips.push({ emoji: '🌙', text: 'Noite chegando. Evite telas 1h antes de dormir e hidrate a pele antes de deitar.' });
        }

        // Render tips
        tipsGrid.innerHTML = '';
        tips.forEach(tip => {
            const card = document.createElement('div');
            card.className = 'tip-card';
            card.innerHTML = `
                <span class="tip-emoji">${tip.emoji}</span>
                <span class="tip-text">${tip.text}</span>
            `;
            tipsGrid.appendChild(card);
        });

        healthTipsPanel.style.display = 'block';
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

let sessionId = null;

function showLogin() {
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('registerSection').style.display = 'none';
    document.getElementById('jobSection').style.display = 'none';
}

function showRegister() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('registerSection').style.display = 'block';
    document.getElementById('jobSection').style.display = 'none';
}

function showJobSection() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('registerSection').style.display = 'none';
    document.getElementById('jobSection').style.display = 'block';
    loadQueue(1); // Загружаем очередь для Printer 1 по умолчанию
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch('http://localhost:8000/auth/token?username=' + username + '&password=' + password, {
        method: 'POST'
    });
    if (response.ok) {
        const data = await response.json();
        sessionId = response.headers.get('set-cookie')?.match(/session_id=([^;]+)/)?.[1];
        showJobSection();
    } else {
        alert('Login failed');
    }
}

async function register() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const role = document.getElementById('regRole').value;
    const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, role })
    });
    if (response.ok) {
        alert('Registration successful. Please login.');
        showLogin();
    } else {
        alert('Registration failed');
    }
}

async function createJob() {
    const printerId = document.getElementById('printerId').value;
    const duration = document.getElementById('duration').value;
    const deadline = document.getElementById('deadline').value; // YYYY-MM-DD
    const materialAmount = document.getElementById('materialAmount').value;
    const response = await fetch('http://localhost:8000/jobs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `session_id=${sessionId}`
        },
        body: JSON.stringify({ printer_id: printerId, duration, deadline, material_amount: materialAmount })
    });
    if (response.ok) {
        alert('Job created');
        loadQueue(printerId);
    } else {
        alert('Job creation failed');
    }
}

async function loadQueue(printerId) {
    const response = await fetch(`http://localhost:8000/jobs/queue/${printerId}`, {
        headers: { 'Cookie': `session_id=${sessionId}` }
    });
    if (response.ok) {
        const jobs = await response.json();
        const queueList = document.getElementById('queueList');
        queueList.innerHTML = '';
        jobs.forEach(job => {
            const li = document.createElement('li');
            li.textContent = `Job #${job.id}: Printer ${job.printer_id}, Duration ${job.duration}h, Deadline ${job.deadline}, Material ${job.material_amount}`;
            queueList.appendChild(li);
        });
    }
}
// Global State
let currentSchedule = null;
let currentTheme = 'dark';

// Tab Navigation
const navBtns = document.querySelectorAll('.nav-btn');
const tabContents = document.querySelectorAll('.tab-content');

navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        navBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        tabContents.forEach(tab => {
            tab.classList.remove('active');
            if (tab.id === `${tabName}-tab`) {
                tab.classList.add('active');
            }
        });
    });
});

// Theme Toggle
const themeToggle = document.getElementById('theme-toggle');
themeToggle?.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.classList.toggle('light-theme');
    themeToggle.querySelector('.theme-icon').textContent = currentTheme === 'dark' ? '🌙' : '☀️';
});

// Export Schedule
const exportBtn = document.getElementById('export-btn');
exportBtn?.addEventListener('click', () => {
    if (!currentSchedule) {
        alert('Please generate a schedule first!');
        return;
    }

    const dataStr = JSON.stringify(currentSchedule, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'study-schedule.json';
    link.click();
});

// Add Course Button
const addCourseBtn = document.getElementById('add-course-btn');
const coursesContainer = document.getElementById('courses-container');

addCourseBtn?.addEventListener('click', () => {
    const courseItem = document.createElement('div');
    courseItem.className = 'course-item';
    courseItem.innerHTML = `
        <input type="text" class="course-name" placeholder="Course Name (e.g., Mathematics)" required>
        <input type="text" class="course-topics" placeholder="Topics (comma separated)" required>
        <select class="course-difficulty">
            <option value="low">Low Difficulty 😊</option>
            <option value="medium" selected>Medium Difficulty 😐</option>
            <option value="high">High Difficulty 😰</option>
        </select>
        <input type="date" class="course-exam" required>
        <button type="button" class="remove-course" title="Remove Course">×</button>
    `;

    // Add remove functionality
    const removeBtn = courseItem.querySelector('.remove-course');
    removeBtn.addEventListener('click', () => {
        if (coursesContainer.children.length > 1) {
            courseItem.remove();
        } else {
            alert('You must have at least one course!');
        }
    });

    coursesContainer.appendChild(courseItem);
});

// Remove course functionality for initial course
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-course').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const courseItem = e.target.closest('.course-item');
            if (coursesContainer.children.length > 1) {
                courseItem.remove();
            } else {
                alert('You must have at least one course!');
            }
        });
    });
});

// Schedule Form Submission
const scheduleForm = document.getElementById('schedule-form');
const generateBtn = document.getElementById('generate-btn');
const scheduleResult = document.getElementById('schedule-result');
const scheduleDisplay = document.getElementById('schedule-display');

scheduleForm?.addEventListener('submit', async (e) => {
    e.preventDefault();

    generateBtn.classList.add('loading');

    const courseItems = document.querySelectorAll('.course-item');
    const courses = {};

    courseItems.forEach(item => {
        const name = item.querySelector('.course-name').value;
        const topics = item.querySelector('.course-topics').value.split(',').map(t => t.trim());
        const difficulty = item.querySelector('.course-difficulty').value;
        const examDate = item.querySelector('.course-exam').value;

        courses[name] = {
            topics: topics,
            difficulty: difficulty,
            exam_date: examDate
        };
    });

    const preferences = {
        daily_max_hours: parseInt(document.getElementById('daily-hours').value),
        peak_hours: document.getElementById('peak-hours').value,
        session_duration: parseInt(document.getElementById('session-duration').value),
        preferred_days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    };

    try {
        const response = await fetch('/api/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ courses, preferences })
        });

        const data = await response.json();

        if (data.status === 'success') {
            currentSchedule = data.schedule;
            displaySchedule(data.schedule);
            updateDashboard(data.schedule, courses);
            scheduleResult.classList.remove('hidden');

            // Show success animation
            scheduleResult.style.animation = 'fadeIn 0.5s ease';
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate schedule. Please try again.');
    } finally {
        generateBtn.classList.remove('loading');
    }
});

function displaySchedule(schedule) {
    const dailySchedule = schedule.daily_schedule;
    let html = '';

    const dates = Object.keys(dailySchedule).sort().slice(0, 7);

    dates.forEach(date => {
        const sessions = dailySchedule[date];
        html += `
            <div class="schedule-day">
                <h4>📅 ${formatDate(date)}</h4>
        `;

        sessions.forEach(session => {
            const emoji = getSessionEmoji(session.topic);
            html += `
                <div class="schedule-session">
                    <strong>${emoji} ${session.start_time} - ${session.end_time}</strong>
                    <br><span style="font-size: 1.1rem;">${session.subject}: ${session.topic}</span>
                    <br><small style="color: var(--text-secondary);">Duration: ${session.duration}h</small>
                </div>
            `;
        });

        html += `</div>`;
    });

    scheduleDisplay.innerHTML = html;
}

function getSessionEmoji(topic) {
    if (topic.includes('MOCK')) return '📝';
    if (topic.includes('REVISION')) return '📖';
    if (topic.includes('Checkpoint')) return '✅';
    return '📚';
}

function updateDashboard(schedule, courses) {
    // Update stats
    document.getElementById('total-courses').textContent = Object.keys(courses).length;

    let totalHours = 0;
    Object.values(schedule.course_analysis).forEach(course => {
        totalHours += course.total_hours || 0;
    });
    document.getElementById('total-hours').textContent = Math.round(totalHours) + 'h';

    // Next exam
    const examDates = Object.entries(courses).map(([name, data]) => ({
        name,
        date: new Date(data.exam_date)
    })).sort((a, b) => a.date - b.date);

    if (examDates.length > 0) {
        const nextexam = examDates[0];
        const daysUntil = Math.ceil((nextexam.date - new Date()) / (1000 * 60 * 60 * 24));
        document.getElementById('next-exam').textContent = `${daysUntil}d`;
    }

    // Upcoming sessions
    const upcomingList = document.getElementById('upcoming-list');
    const today = new Date().toISOString().split('T')[0];
    const todaySessions = schedule.daily_schedule[today] || [];

    if (todaySessions.length > 0) {
        upcomingList.innerHTML = todaySessions.slice(0, 5).map(session => `
            <div class="session-item">
                <strong>${session.start_time}</strong> - ${session.subject}
                <br><small>${session.topic}</small>
            </div>
        `).join('');
    } else {
        upcomingList.innerHTML = '<p class="empty-state">No sessions today. Enjoy your day! 🎉</p>';
    }

    // Update progress chart if exists
    updateProgressChart(courses);
}

function updateProgressChart(courses) {
    const ctx = document.getElementById('progress-chart');
    if (!ctx) return;

    const labels = Object.keys(courses);
    const data = labels.map(() => Math.random() * 30 + 10); // Mock data

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'hsl(260, 80%, 60%)',
                    'hsl(200, 90%, 55%)',
                    'hsl(330, 80%, 60%)',
                    'hsl(140, 70%, 55%)',
                    'hsl(40, 95%, 60%)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'hsl(0, 0%, 95%)',
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Progress Tab
const refreshProgressBtn = document.getElementById('refresh-progress-btn');
const progressDisplay = document.getElementById('progress-display');

refreshProgressBtn?.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/progress');
        const data = await response.json();

        displayProgress(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch progress. Please try again.');
    }
});

function displayProgress(data) {
    const metrics = data.metrics.metrics;
    let html = '';

    if (metrics.subjects) {
        Object.entries(metrics.subjects).forEach(([subject, progress]) => {
            const percentage = Math.round(progress * 100);
            html += `
                <div class="progress-bar">
                    <h4>${subject}</h4>
                    <div class="progress-track">
                        <div class="progress-fill" style="width: ${percentage}%"></div>
                    </div>
                    <small style="color: var(--text-secondary); margin-top: 0.5rem; display: block;">${percentage}% Complete</small>
                </div>
            `;
        });
    }

    progressDisplay.innerHTML = html || '<p class="empty-state">No progress data available yet. Create a schedule first!</p>';
}

// Chat Tab
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatForm?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    chatInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        addMessage(data.response, 'agent');
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, something went wrong. Please try again.', 'agent');
    }
});

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// View toggles for schedule
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('view-toggle')) {
        document.querySelectorAll('.view-toggle').forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');

        const view = e.target.dataset.view;
        // Implement different views (list/calendar) here
        console.log('Switching to view:', view);
    }
});

// Initialize welcome message
if (chatMessages) {
    addMessage('Hello! 👋 I\'m your Study Planner AI assistant. I can help you create schedules, track progress, and stay motivated. How can I assist you today?', 'agent');
}

// Auto-animate elements on scroll
const observeElements = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
};

document.addEventListener('DOMContentLoaded', observeElements);

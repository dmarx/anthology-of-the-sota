// File: frontend-html/scripts/main.js
let recommendations = [];
let currentView = 'grid';
let currentSort = {
    column: 'topic',
    direction: 'asc'
};

async function loadData() {
    //const response = await fetch('./data/recommendations.json');
    const response = await fetch('./data/registry.json');
    recommendations = await response.json();
    renderView();
}

function setView(view) {
    currentView = view;
    document.getElementById('recommendations').classList.toggle('hidden', view !== 'grid');
    document.getElementById('recommendationsTable').classList.toggle('hidden', view !== 'table');
    renderView();
}

function renderView() {
    if (currentView === 'grid') {
        renderGrid();
    } else {
        renderTable();
    }
}

function renderGrid() {
    const grid = document.getElementById('recommendations');
    grid.innerHTML = recommendations
        .map(rec => `
            <div class="recommendation-card">
                <h3>${rec.topic}</h3>
                <p>${rec.recommendation}</p>
                <div>Status: ${rec.status}</div>
                <div>Source: ${rec.source}</div>
            </div>
        `).join('');
}

function renderTable() {
    const table = document.getElementById('recommendationsTable');
    table.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th onclick="sortBy('topic')">Topic ${getSortIndicator('topic')}</th>
                    <th onclick="sortBy('recommendation')">Recommendation ${getSortIndicator('recommendation')}</th>
                    <th onclick="sortBy('status')">Status ${getSortIndicator('status')}</th>
                    <th onclick="sortBy('source')">Source ${getSortIndicator('source')}</th>
                </tr>
            </thead>
            <tbody>
                ${recommendations.map(rec => `
                    <tr>
                        <td>${rec.topic}</td>
                        <td>${rec.recommendation}</td>
                        <td>${rec.status}</td>
                        <td>${rec.source}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function sortBy(column) {
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort = { column, direction: 'asc' };
    }
    
    recommendations = _.orderBy(
        recommendations,
        [currentSort.column],
        [currentSort.direction]
    );
    
    renderView();
}

function getSortIndicator(column) {
    if (currentSort.column !== column) return '↕';
    return currentSort.direction === 'asc' ? '↑' : '↓';
}

// Initialize
loadData();

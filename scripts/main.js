// File: web/scripts/main.js
let recommendations = [];
let currentView = 'grid';
let currentSort = {
    column: 'topic',
    direction: 'asc'
};

async function loadData() {
    const response = await fetch('../data/registry.yaml');
    const yamlText = await response.text();
    const data = jsyaml.load(yamlText);
    recommendations = data.recommendations;
    renderView();
}

function formatSource(source) {
    return `${source.first_author} et al. (${source.year})`;
}

function renderGrid() {
    const grid = document.getElementById('recommendations');
    grid.innerHTML = recommendations
        .map(rec => `
            <div class="recommendation-card">
                <h3>${rec.topic}</h3>
                <p>${rec.recommendation}</p>
                <div>Status: ${rec.status}</div>
                <div>Source: ${formatSource(rec.source)}</div>
                ${rec.source.arxiv_id ? 
                    `<div>arXiv: <a href="https://arxiv.org/abs/${rec.source.arxiv_id}" target="_blank">${rec.source.arxiv_id}</a></div>` 
                    : ''}
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
                    <th>Source</th>
                </tr>
            </thead>
            <tbody>
                ${recommendations.map(rec => `
                    <tr>
                        <td>${rec.topic}</td>
                        <td>${rec.recommendation}</td>
                        <td>${rec.status}</td>
                        <td>
                            ${formatSource(rec.source)}
                            ${rec.source.arxiv_id ? 
                                `<br><a href="https://arxiv.org/abs/${rec.source.arxiv_id}" target="_blank">arXiv:${rec.source.arxiv_id}</a>` 
                                : ''}
                        </td>
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
        [column],
        [currentSort.direction]
    );
    
    renderView();
}

function getSortIndicator(column) {
    if (currentSort.column !== column) return '↕';
    return currentSort.direction === 'asc' ? '↑' : '↓';
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

// Initialize
loadData();

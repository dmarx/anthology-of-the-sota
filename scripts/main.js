// File: web/scripts/main.js
let recommendations = [];
let currentView = 'grid';
let currentSort = {
    column: 'topic',
    direction: 'asc'
};

async function loadData() {
    try {
        const response = await fetch('./data/registry.yaml');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const yamlText = await response.text();
        const data = jsyaml.load(yamlText);
        
        // Validate and extract recommendations from registry format
        if (!data?.recommendations?.standard) {
            throw new Error('Invalid data format');
        }

        // Flatten recommendations by status and add status field
        recommendations = Object.entries(data.recommendations)
            .flatMap(([status, recs]) => 
                Object.values(recs).map(rec => ({...rec, status}))
            );

        renderView();
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('recommendations').innerHTML = '<div class="error">Error loading recommendations</div>';
        document.getElementById('recommendationsTable').innerHTML = '<div class="error">Error loading recommendations</div>';
    }
}

function formatSource(source) {
    const arxivLink = source.arxiv_id ? 
        `<a href="https://arxiv.org/abs/${source.arxiv_id}" target="_blank">[${source.arxiv_id}]</a>` : '';
    return `${source.first_author} et al. (${source.year}) ${arxivLink}`;
}

function getStatusClass(status) {
    return {
        'standard': 'status-standard',
        'experimental': 'status-experimental',
        'deprecated': 'status-deprecated'
    }[status] || 'status-standard';
}

function renderGrid() {
    const grid = document.getElementById('recommendations');
    if (!recommendations || recommendations.length === 0) {
        grid.innerHTML = '<div>No recommendations available</div>';
        return;
    }
    
    grid.innerHTML = recommendations
        .map(rec => `
            <div class="recommendation-card">
                <div class="card-topic">${rec.topic}</div>
                <p class="card-recommendation">${rec.recommendation}</p>
                <div class="card-metadata">
                    <span class="${getStatusClass(rec.status)}">${rec.status}</span>
                    ${rec.implementations?.length ? 
                        `<div class="implementations">
                            Implementations: ${rec.implementations.join(', ')}
                        </div>` : 
                        ''}
                </div>
                <div class="card-source">
                    Source: ${formatSource(rec.source)}
                </div>
            </div>
        `).join('');
}

function renderTable() {
    const table = document.getElementById('recommendationsTable');
    if (!recommendations || recommendations.length === 0) {
        table.innerHTML = '<div>No recommendations available</div>';
        return;
    }

    table.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th onclick="sortBy('topic')">Topic ${getSortIndicator('topic')}</th>
                    <th onclick="sortBy('recommendation')">Recommendation ${getSortIndicator('recommendation')}</th>
                    <th onclick="sortBy('status')">Status ${getSortIndicator('status')}</th>
                    <th>Source</th>
                    ${recommendations.some(r => r.implementations?.length) ? 
                        '<th>Implementations</th>' : ''}
                </tr>
            </thead>
            <tbody>
                ${recommendations.map(rec => `
                    <tr>
                        <td>${rec.topic}</td>
                        <td>${rec.recommendation}</td>
                        <td><span class="${getStatusClass(rec.status)}">${rec.status}</span></td>
                        <td>${formatSource(rec.source)}</td>
                        ${recommendations.some(r => r.implementations?.length) ? 
                            `<td>${rec.implementations?.join(', ') || ''}</td>` : ''}
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

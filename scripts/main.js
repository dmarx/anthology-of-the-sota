// File: web/scripts/main.js
let recommendations = [];
let currentView = 'grid';
let currentSort = {
    column: 'topic',
    direction: 'asc'
};
let filters = {
    search: '',
    topic: '',
    status: ''
};

async function loadData() {
    try {
        const response = await fetch('./data/registry.yaml');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const yamlText = await response.text();
        const data = jsyaml.load(yamlText);
        if (!data || !data.recommendations || !data.recommendations.standard) {
            throw new Error('Invalid data format');
        }
        // Flatten recommendations and add status
        recommendations = Object.entries(data.recommendations)
            .flatMap(([status, recs]) => 
                Object.values(recs).map(rec => ({...rec, status}))
            );
        
        setupFilters();
        renderView();
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('recommendations').innerHTML = '<div class="error">Error loading recommendations</div>';
        document.getElementById('recommendationsTable').innerHTML = '<div class="error">Error loading recommendations</div>';
    }
}

function setupFilters() {
    const topics = [...new Set(recommendations.map(r => r.topic))].sort();
    const statuses = [...new Set(recommendations.map(r => r.status))].sort();
    
    const controls = document.createElement('div');
    controls.className = 'filter-controls';
    controls.innerHTML = `
        <input 
            type="text" 
            placeholder="Search recommendations..." 
            class="search-input"
            value="${filters.search}"
        >
        <select class="topic-select">
            <option value="">All Topics</option>
            ${topics.map(t => `
                <option value="${t}" ${filters.topic === t ? 'selected' : ''}>
                    ${t}
                </option>
            `).join('')}
        </select>
        <select class="status-select">
            <option value="">All Statuses</option>
            ${statuses.map(s => `
                <option value="${s}" ${filters.status === s ? 'selected' : ''}>
                    ${s}
                </option>
            `).join('')}
        </select>
    `;
    
    const viewControls = document.querySelector('.view-controls');
    viewControls.insertBefore(controls, document.getElementById('activeFilters'));
    
    // Setup event listeners
    controls.querySelector('.search-input').addEventListener('input', e => {
        filters.search = e.target.value;
        renderView();
    });
    
    controls.querySelector('.topic-select').addEventListener('change', e => {
        filters.topic = e.target.value;
        renderView();
    });
    
    controls.querySelector('.status-select').addEventListener('change', e => {
        filters.status = e.target.value;
        renderView();
    });
}

function formatSource(source) {
    return `${source.first_author} et al. (${source.year})`;
}

function getFilteredRecommendations() {
    return recommendations.filter(rec => {
        const matchesSearch = filters.search === '' || 
            rec.recommendation.toLowerCase().includes(filters.search.toLowerCase()) ||
            rec.topic.toLowerCase().includes(filters.search.toLowerCase());
        
        const matchesTopic = filters.topic === '' || rec.topic === filters.topic;
        const matchesStatus = filters.status === '' || rec.status === filters.status;
        
        return matchesSearch && matchesTopic && matchesStatus;
    });
}

function renderGrid() {
    const grid = document.getElementById('recommendations');
    const filteredRecs = getFilteredRecommendations();
    
    if (!filteredRecs || filteredRecs.length === 0) {
        grid.innerHTML = '<div>No recommendations found</div>';
        return;
    }
    
    grid.innerHTML = filteredRecs
        .map(rec => `
            <div class="recommendation-card">
                <div class="card-topic">${rec.topic}</div>
                <p class="card-recommendation">${rec.recommendation}</p>
                <div class="card-status status-${rec.status}">
                    ${rec.status}
                </div>
                <div class="card-source">
                    <div>Source: ${formatSource(rec.source)}</div>
                    ${rec.source.arxiv_id ? 
                        `<div>arXiv: <a href="https://arxiv.org/abs/${rec.source.arxiv_id}" target="_blank">${rec.source.arxiv_id}</a></div>` 
                        : ''}
                </div>
            </div>
        `).join('');
}

function renderTable() {
    const table = document.getElementById('recommendationsTable');
    const filteredRecs = getFilteredRecommendations();
    
    if (!filteredRecs || filteredRecs.length === 0) {
        table.innerHTML = '<div>No recommendations found</div>';
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
                </tr>
            </thead>
            <tbody>
                ${filteredRecs.map(rec => `
                    <tr>
                        <td>${rec.topic}</td>
                        <td>${rec.recommendation}</td>
                        <td><span class="status-${rec.status}">${rec.status}</span></td>
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

// ... rest of the existing code (sortBy, getSortIndicator, setView, renderView) stays the same

// Global variables
let currentTeams = [];
let currentPlayers = [];

// Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Setup navigation
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            showSection(section);
        });
    });

    // Setup statistics tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.getAttribute('data-tab');
            showStatsTab(tab);
        });
    });

    // Setup search
    const searchInput = document.getElementById('playerSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value;
            if (searchTerm.trim() === '') {
                loadPlayers();
            } else {
                searchPlayers(searchTerm);
            }
        });
    }

    // Setup forms
    document.getElementById('teamForm').addEventListener('submit', handleTeamSubmit);
    document.getElementById('playerForm').addEventListener('submit', handlePlayerSubmit);

    // Initial load
    loadDashboard();
    loadTeams();
    loadPlayers();
});

// Section Navigation
function showSection(sectionId) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

    // Update sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');

    // Load data based on section
    if (sectionId === 'dashboard') {
        loadDashboard();
    } else if (sectionId === 'teams') {
        loadTeams();
    } else if (sectionId === 'players') {
        loadPlayers();
    } else if (sectionId === 'rankings') {
        loadRankings();
    } else if (sectionId === 'statistics') {
        loadStatistics();
    }
}

// Statistics Tabs
function showStatsTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

    document.querySelectorAll('.stats-tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
}

// DASHBOARD
async function loadDashboard() {
    try {
        const [teams, players] = await Promise.all([
            fetch('/api/teams').then(r => r.json()),
            fetch('/api/players').then(r => r.json())
        ]);

        const totalGoals = players.reduce((sum, p) => sum + (p.goals || 0), 0);
        const totalAssists = players.reduce((sum, p) => sum + (p.assists || 0), 0);

        document.getElementById('totalTeams').textContent = teams.length;
        document.getElementById('totalPlayers').textContent = players.length;
        document.getElementById('totalGoals').textContent = totalGoals;
        document.getElementById('totalAssists').textContent = totalAssists;

        // Load top players
        const topPlayers = await fetch('/api/players/top/5').then(r => r.json());
        displayTopPlayers(topPlayers);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function displayTopPlayers(players) {
    const container = document.getElementById('topPlayersTable');
    
    if (players.length === 0) {
        container.innerHTML = '<p class="empty-state">No players found</p>';
        return;
    }

    let html = `
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Team</th>
                    <th>Ranking</th>
                    <th>Goals</th>
                </tr>
            </thead>
            <tbody>
    `;

    players.forEach((player, index) => {
        html += `
            <tr>
                <td>${index + 1}</td>
                <td>${player.first_name} ${player.last_name}</td>
                <td>${player.team_name || 'No Team'}</td>
                <td>${player.ranking}</td>
                <td>${player.goals}</td>
            </tr>
        `;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

// TEAMS
async function loadTeams() {
    try {
        const teams = await fetch('/api/teams').then(r => r.json());
        currentTeams = teams;
        displayTeams(teams);
    } catch (error) {
        console.error('Error loading teams:', error);
        showNotification('Error loading teams', 'error');
    }
}

function displayTeams(teams) {
    const tbody = document.getElementById('teamsTableBody');
    
    if (teams.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No teams found. Click "Add Team" to create one.</td></tr>';
        return;
    }

    tbody.innerHTML = teams.map(team => `
        <tr>
            <td>${team.team_id}</td>
            <td><strong>${team.team_name}</strong></td>
            <td>${team.coach_name || '-'}</td>
            <td>${team.founded_year || '-'}</td>
            <td>${team.city || '-'}</td>
            <td>${team.stadium || '-'}</td>
            <td class="action-buttons">
                <button class="btn-edit" onclick="editTeam(${team.team_id})">Edit</button>
                <button class="btn-danger" onclick="deleteTeam(${team.team_id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

// PLAYERS
async function loadPlayers() {
    try {
        const players = await fetch('/api/players').then(r => r.json());
        currentPlayers = players;
        displayPlayers(players);
    } catch (error) {
        console.error('Error loading players:', error);
        showNotification('Error loading players', 'error');
    }
}

function displayPlayers(players) {
    const tbody = document.getElementById('playersTableBody');
    
    if (players.length === 0) {
        tbody.innerHTML = '<tr><td colspan="11" class="empty-state">No players found. Click "Add Player" to create one.</td></tr>';
        return;
    }

    tbody.innerHTML = players.map(player => `
        <tr>
            <td>${player.player_id}</td>
            <td><strong>${player.first_name} ${player.last_name}</strong></td>
            <td>${player.team_name || 'No Team'}</td>
            <td>${player.position || '-'}</td>
            <td>${player.jersey_number || '-'}</td>
            <td>${player.age || '-'}</td>
            <td><strong>${player.ranking}</strong></td>
            <td>${player.goals}</td>
            <td>${player.assists}</td>
            <td>${player.matches_played}</td>
            <td class="action-buttons">
                <button class="btn-edit" onclick="editPlayer(${player.player_id})">Edit</button>
                <button class="btn-danger" onclick="deletePlayer(${player.player_id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

async function searchPlayers(searchTerm) {
    try {
        const players = await fetch(`/api/players/search?q=${encodeURIComponent(searchTerm)}`).then(r => r.json());
        displayPlayers(players);
    } catch (error) {
        console.error('Error searching players:', error);
    }
}

// RANKINGS
async function loadRankings() {
    const limit = document.getElementById('rankingLimit').value;
    try {
        const players = await fetch(`/api/players/top/${limit}`).then(r => r.json());
        displayRankings(players);
    } catch (error) {
        console.error('Error loading rankings:', error);
    }
}

function displayRankings(players) {
    const tbody = document.getElementById('rankingsTableBody');
    
    if (players.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty-state">No players found</td></tr>';
        return;
    }

    tbody.innerHTML = players.map((player, index) => `
        <tr>
            <td><strong>${index + 1}</strong></td>
            <td>${player.first_name} ${player.last_name}</td>
            <td>${player.team_name || 'No Team'}</td>
            <td>${player.position || '-'}</td>
            <td><strong>${player.ranking}</strong></td>
            <td>${player.goals}</td>
            <td>${player.assists}</td>
            <td>${player.matches_played}</td>
        </tr>
    `).join('');
}

// STATISTICS
async function loadStatistics() {
    try {
        const [playerStats, teamStats] = await Promise.all([
            fetch('/api/stats/players').then(r => r.json()),
            fetch('/api/stats/teams').then(r => r.json())
        ]);

        displayPlayerStats(playerStats);
        displayTeamStats(teamStats);
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

function displayPlayerStats(stats) {
    const tbody = document.getElementById('playerStatsBody');
    
    if (stats.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="empty-state">No statistics available</td></tr>';
        return;
    }

    tbody.innerHTML = stats.map(stat => `
        <tr>
            <td><strong>${stat.player_name}</strong></td>
            <td>${stat.team_name || 'No Team'}</td>
            <td>${stat.position || '-'}</td>
            <td>${stat.jersey_number || '-'}</td>
            <td><strong>${stat.ranking}</strong></td>
            <td>${stat.goals}</td>
            <td>${stat.assists}</td>
            <td>${stat.matches_played}</td>
            <td>${stat.goals_per_match.toFixed(2)}</td>
        </tr>
    `).join('');
}

function displayTeamStats(stats) {
    const tbody = document.getElementById('teamStatsBody');
    
    if (stats.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No statistics available</td></tr>';
        return;
    }

    tbody.innerHTML = stats.map(stat => `
        <tr>
            <td><strong>${stat.team_name}</strong></td>
            <td>${stat.coach_name || '-'}</td>
            <td>${stat.city || '-'}</td>
            <td>${stat.total_players}</td>
            <td>${stat.total_goals}</td>
            <td>${stat.total_assists}</td>
        </tr>
    `).join('');
}

// TEAM MODAL
function showTeamModal() {
    document.getElementById('teamModalTitle').textContent = 'Add Team';
    document.getElementById('teamForm').reset();
    document.getElementById('teamId').value = '';
    document.getElementById('teamModal').style.display = 'block';
}

function closeTeamModal() {
    document.getElementById('teamModal').style.display = 'none';
}

async function editTeam(teamId) {
    try {
        const team = await fetch(`/api/teams/${teamId}`).then(r => r.json());
        
        document.getElementById('teamModalTitle').textContent = 'Edit Team';
        document.getElementById('teamId').value = team.team_id;
        document.getElementById('teamName').value = team.team_name;
        document.getElementById('coachName').value = team.coach_name || '';
        document.getElementById('foundedYear').value = team.founded_year || '';
        document.getElementById('city').value = team.city || '';
        document.getElementById('stadium').value = team.stadium || '';
        
        document.getElementById('teamModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading team:', error);
        showNotification('Error loading team', 'error');
    }
}

async function handleTeamSubmit(e) {
    e.preventDefault();
    
    const teamId = document.getElementById('teamId').value;
    const data = {
        team_name: document.getElementById('teamName').value,
        coach_name: document.getElementById('coachName').value,
        founded_year: parseInt(document.getElementById('foundedYear').value) || null,
        city: document.getElementById('city').value,
        stadium: document.getElementById('stadium').value
    };

    try {
        const url = teamId ? `/api/teams/${teamId}` : '/api/teams';
        const method = teamId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            closeTeamModal();
            loadTeams();
            loadPlayers(); // Refresh to update team names
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        console.error('Error saving team:', error);
        showNotification('Error saving team', 'error');
    }
}

async function deleteTeam(teamId) {
    if (!confirm('Are you sure you want to delete this team? This will remove the team association from all players.')) {
        return;
    }

    try {
        const response = await fetch(`/api/teams/${teamId}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            loadTeams();
            loadPlayers(); // Refresh to update team names
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting team:', error);
        showNotification('Error deleting team', 'error');
    }
}

// PLAYER MODAL
async function showPlayerModal() {
    document.getElementById('playerModalTitle').textContent = 'Add Player';
    document.getElementById('playerForm').reset();
    document.getElementById('playerId').value = '';
    
    // Load teams for dropdown
    await loadTeamsDropdown();
    
    document.getElementById('playerModal').style.display = 'block';
}

function closePlayerModal() {
    document.getElementById('playerModal').style.display = 'none';
}

async function loadTeamsDropdown() {
    try {
        const teams = await fetch('/api/teams').then(r => r.json());
        const select = document.getElementById('playerTeam');
        
        select.innerHTML = '<option value="">Select Team</option>';
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team.team_id;
            option.textContent = team.team_name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading teams dropdown:', error);
    }
}

async function editPlayer(playerId) {
    try {
        const player = await fetch(`/api/players/${playerId}`).then(r => r.json());
        
        await loadTeamsDropdown();
        
        document.getElementById('playerModalTitle').textContent = 'Edit Player';
        document.getElementById('playerId').value = player.player_id;
        document.getElementById('firstName').value = player.first_name;
        document.getElementById('lastName').value = player.last_name;
        document.getElementById('playerTeam').value = player.team_id || '';
        document.getElementById('position').value = player.position || '';
        document.getElementById('jerseyNumber').value = player.jersey_number || '';
        document.getElementById('age').value = player.age || '';
        document.getElementById('height').value = player.height || '';
        document.getElementById('weight').value = player.weight || '';
        document.getElementById('ranking').value = player.ranking || 0;
        document.getElementById('goals').value = player.goals || 0;
        document.getElementById('assists').value = player.assists || 0;
        document.getElementById('matchesPlayed').value = player.matches_played || 0;
        
        document.getElementById('playerModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading player:', error);
        showNotification('Error loading player', 'error');
    }
}

async function handlePlayerSubmit(e) {
    e.preventDefault();
    
    const playerId = document.getElementById('playerId').value;
    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        team_id: parseInt(document.getElementById('playerTeam').value) || null,
        position: document.getElementById('position').value,
        jersey_number: parseInt(document.getElementById('jerseyNumber').value) || 0,
        age: parseInt(document.getElementById('age').value) || 0,
        height: parseFloat(document.getElementById('height').value) || 0,
        weight: parseFloat(document.getElementById('weight').value) || 0,
        ranking: parseInt(document.getElementById('ranking').value) || 0,
        goals: parseInt(document.getElementById('goals').value) || 0,
        assists: parseInt(document.getElementById('assists').value) || 0,
        matches_played: parseInt(document.getElementById('matchesPlayed').value) || 0
    };

    try {
        const url = playerId ? `/api/players/${playerId}` : '/api/players';
        const method = playerId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            closePlayerModal();
            loadPlayers();
            loadDashboard(); // Refresh dashboard stats
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        console.error('Error saving player:', error);
        showNotification('Error saving player', 'error');
    }
}

async function deletePlayer(playerId) {
    if (!confirm('Are you sure you want to delete this player?')) {
        return;
    }

    try {
        const response = await fetch(`/api/players/${playerId}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            loadPlayers();
            loadDashboard(); // Refresh dashboard stats
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting player:', error);
        showNotification('Error deleting player', 'error');
    }
}

// NOTIFICATIONS
function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 600;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// SAMPLE DATA FUNCTIONS
async function loadSampleData() {
    if (!confirm('This will add sample teams and players to your database. Continue?')) {
        return;
    }

    try {
        const response = await fetch('/api/sample-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            // Reload all data
            loadDashboard();
            loadTeams();
            loadPlayers();
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        console.error('Error loading sample data:', error);
        showNotification('Error loading sample data', 'error');
    }
}

async function clearAllData() {
    if (!confirm('⚠️ WARNING: This will delete ALL teams and players from the database. This action cannot be undone. Are you sure?')) {
        return;
    }

    try {
        const response = await fetch('/api/clear-data', {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            // Reload all data
            loadDashboard();
            loadTeams();
            loadPlayers();
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        console.error('Error clearing data:', error);
        showNotification('Error clearing data', 'error');
    }
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

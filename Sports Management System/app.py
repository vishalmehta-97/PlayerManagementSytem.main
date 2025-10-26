from flask import Flask, render_template, request, jsonify
from database import Database
import json

app = Flask(__name__)
db = Database()

# HOME ROUTE
@app.route('/')
def index():
    return render_template('index.html')

# TEAM ROUTES
@app.route('/api/teams', methods=['GET'])
def get_teams():
    teams = db.get_all_teams()
    teams_list = []
    for team in teams:
        teams_list.append({
            'team_id': team[0],
            'team_name': team[1],
            'coach_name': team[2],
            'founded_year': team[3],
            'city': team[4],
            'stadium': team[5],
            'created_at': team[6]
        })
    return jsonify(teams_list)

@app.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = db.get_team_by_id(team_id)
    if team:
        return jsonify({
            'team_id': team[0],
            'team_name': team[1],
            'coach_name': team[2],
            'founded_year': team[3],
            'city': team[4],
            'stadium': team[5],
            'created_at': team[6]
        })
    return jsonify({'error': 'Team not found'}), 404

@app.route('/api/teams', methods=['POST'])
def add_team():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    result = db.add_team(
        data['team_name'],
        data.get('coach_name', ''),
        data.get('founded_year', None),
        data.get('city', ''),
        data.get('stadium', '')
    )
    return jsonify(result)

@app.route('/api/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    result = db.update_team(
        team_id,
        data['team_name'],
        data.get('coach_name', ''),
        data.get('founded_year', None),
        data.get('city', ''),
        data.get('stadium', '')
    )
    return jsonify(result)

@app.route('/api/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    result = db.delete_team(team_id)
    return jsonify(result)

# PLAYER ROUTES
@app.route('/api/players', methods=['GET'])
def get_players():
    players = db.get_all_players()
    players_list = []
    for player in players:
        players_list.append({
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'team_id': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'height': player[7],
            'weight': player[8],
            'ranking': player[9],
            'goals': player[10],
            'assists': player[11],
            'matches_played': player[12],
            'created_at': player[13],
            'team_name': player[14] if len(player) > 14 else None
        })
    return jsonify(players_list)

@app.route('/api/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = db.get_player_by_id(player_id)
    if player:
        return jsonify({
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'team_id': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'height': player[7],
            'weight': player[8],
            'ranking': player[9],
            'goals': player[10],
            'assists': player[11],
            'matches_played': player[12],
            'created_at': player[13]
        })
    return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    result = db.add_player(
        data['first_name'],
        data['last_name'],
        data.get('team_id', None),
        data.get('position', ''),
        data.get('jersey_number', 0),
        data.get('age', 0),
        data.get('height', 0.0),
        data.get('weight', 0.0),
        data.get('ranking', 0),
        data.get('goals', 0),
        data.get('assists', 0),
        data.get('matches_played', 0)
    )
    return jsonify(result)

@app.route('/api/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    result = db.update_player(
        player_id,
        data['first_name'],
        data['last_name'],
        data.get('team_id', None),
        data.get('position', ''),
        data.get('jersey_number', 0),
        data.get('age', 0),
        data.get('height', 0.0),
        data.get('weight', 0.0),
        data.get('ranking', 0),
        data.get('goals', 0),
        data.get('assists', 0),
        data.get('matches_played', 0)
    )
    return jsonify(result)

@app.route('/api/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    result = db.delete_player(player_id)
    return jsonify(result)

# STATISTICS AND VIEWS ROUTES
@app.route('/api/stats/players', methods=['GET'])
def get_player_stats():
    stats = db.get_player_stats()
    stats_list = []
    for stat in stats:
        stats_list.append({
            'player_id': stat[0],
            'player_name': stat[1],
            'team_name': stat[2],
            'position': stat[3],
            'jersey_number': stat[4],
            'age': stat[5],
            'ranking': stat[6],
            'goals': stat[7],
            'assists': stat[8],
            'matches_played': stat[9],
            'goals_per_match': stat[10]
        })
    return jsonify(stats_list)

@app.route('/api/stats/teams', methods=['GET'])
def get_team_stats():
    stats = db.get_team_stats()
    stats_list = []
    for stat in stats:
        stats_list.append({
            'team_id': stat[0],
            'team_name': stat[1],
            'coach_name': stat[2],
            'city': stat[3],
            'total_players': stat[4],
            'total_goals': stat[5],
            'total_assists': stat[6]
        })
    return jsonify(stats_list)

@app.route('/api/players/top/<int:limit>', methods=['GET'])
def get_top_players(limit):
    players = db.get_top_players_by_ranking(limit)
    players_list = []
    for player in players:
        players_list.append({
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'team_id': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'height': player[7],
            'weight': player[8],
            'ranking': player[9],
            'goals': player[10],
            'assists': player[11],
            'matches_played': player[12],
            'created_at': player[13],
            'team_name': player[14] if len(player) > 14 else None
        })
    return jsonify(players_list)

@app.route('/api/players/search', methods=['GET'])
def search_players():
    search_term = request.args.get('q', '')
    players = db.search_players(search_term)
    players_list = []
    for player in players:
        players_list.append({
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'team_id': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'height': player[7],
            'weight': player[8],
            'ranking': player[9],
            'goals': player[10],
            'assists': player[11],
            'matches_played': player[12],
            'created_at': player[13],
            'team_name': player[14] if len(player) > 14 else None
        })
    return jsonify(players_list)

@app.route('/api/teams/<int:team_id>/players', methods=['GET'])
def get_team_players(team_id):
    players = db.get_players_by_team(team_id)
    players_list = []
    for player in players:
        players_list.append({
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'team_id': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'height': player[7],
            'weight': player[8],
            'ranking': player[9],
            'goals': player[10],
            'assists': player[11],
            'matches_played': player[12],
            'created_at': player[13]
        })
    return jsonify(players_list)

@app.route('/api/sample-data', methods=['POST'])
def add_sample_data():
    """Add sample data to the database"""
    result = db.add_sample_data()
    return jsonify(result)

@app.route('/api/clear-data', methods=['DELETE'])
def clear_all_data():
    """Clear all data from the database"""
    result = db.clear_all_data()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

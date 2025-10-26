import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='sports_management.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL UNIQUE,
                coach_name TEXT,
                founded_year INTEGER,
                city TEXT,
                stadium TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                team_id INTEGER,
                position TEXT,
                jersey_number INTEGER,
                age INTEGER,
                height REAL,
                weight REAL,
                ranking INTEGER DEFAULT 0,
                goals INTEGER DEFAULT 0,
                assists INTEGER DEFAULT 0,
                matches_played INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
            )
        ''')
        
        # Create view for player statistics
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS player_stats AS
            SELECT 
                p.player_id,
                p.first_name || ' ' || p.last_name AS player_name,
                t.team_name,
                p.position,
                p.jersey_number,
                p.age,
                p.ranking,
                p.goals,
                
                p.assists,
                p.matches_played,
                CASE 
                    WHEN p.matches_played > 0 THEN ROUND(CAST(p.goals AS REAL) / p.matches_played, 2)
                    ELSE 0
                END AS goals_per_match
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.ranking DESC
        ''')
        
        # Create view for team statistics
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS team_stats AS
            SELECT 
                t.team_id,
                t.team_name,
                t.coach_name,
                t.city,
                COUNT(p.player_id) AS total_players,
                COALESCE(SUM(p.goals), 0) AS total_goals,
                COALESCE(SUM(p.assists), 0) AS total_assists
            FROM teams t
            LEFT JOIN players p ON t.team_id = p.team_id
            GROUP BY t.team_id
        ''')
        
        conn.commit()
        conn.close()
    
    # TEAM OPERATIONS
    def add_team(self, team_name, coach_name, founded_year, city, stadium):
        """Add a new team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO teams (team_name, coach_name, founded_year, city, stadium)
                VALUES (?, ?, ?, ?, ?)
            ''', (team_name, coach_name, founded_year, city, stadium))
            conn.commit()
            return {"success": True, "message": "Team added successfully", "id": cursor.lastrowid}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "Team name already exists"}
        finally:
            conn.close()
    
    def get_all_teams(self):
        """Get all teams"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM teams ORDER BY team_name')
        teams = cursor.fetchall()
        conn.close()
        return teams
    
    def get_team_by_id(self, team_id):
        """Get team by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM teams WHERE team_id = ?', (team_id,))
        team = cursor.fetchone()
        conn.close()
        return team
    
    def update_team(self, team_id, team_name, coach_name, founded_year, city, stadium):
        """Update team information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE teams 
                SET team_name = ?, coach_name = ?, founded_year = ?, city = ?, stadium = ?
                WHERE team_id = ?
            ''', (team_name, coach_name, founded_year, city, stadium, team_id))
            conn.commit()
            return {"success": True, "message": "Team updated successfully"}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "Team name already exists"}
        finally:
            conn.close()
    
    def delete_team(self, team_id):
        """Delete a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM teams WHERE team_id = ?', (team_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Team deleted successfully"}
    
    # PLAYER OPERATIONS
    def add_player(self, first_name, last_name, team_id, position, jersey_number, 
                   age, height, weight, ranking, goals, assists, matches_played):
        """Add a new player"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO players 
            (first_name, last_name, team_id, position, jersey_number, age, height, weight, 
             ranking, goals, assists, matches_played)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, team_id, position, jersey_number, age, height, weight,
              ranking, goals, assists, matches_played))
        conn.commit()
        player_id = cursor.lastrowid
        conn.close()
        return {"success": True, "message": "Player added successfully", "id": player_id}
    
    def get_all_players(self):
        """Get all players"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, t.team_name 
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.ranking DESC
        ''')
        players = cursor.fetchall()
        conn.close()
        return players
    
    def get_player_by_id(self, player_id):
        """Get player by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE player_id = ?', (player_id,))
        player = cursor.fetchone()
        conn.close()
        return player
    
    def get_players_by_team(self, team_id):
        """Get all players in a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM players 
            WHERE team_id = ? 
            ORDER BY ranking DESC
        ''', (team_id,))
        players = cursor.fetchall()
        conn.close()
        return players
    
    def update_player(self, player_id, first_name, last_name, team_id, position, 
                     jersey_number, age, height, weight, ranking, goals, assists, matches_played):
        """Update player information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE players 
            SET first_name = ?, last_name = ?, team_id = ?, position = ?, jersey_number = ?,
                age = ?, height = ?, weight = ?, ranking = ?, goals = ?, assists = ?, 
                matches_played = ?
            WHERE player_id = ?
        ''', (first_name, last_name, team_id, position, jersey_number, age, height, weight,
              ranking, goals, assists, matches_played, player_id))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Player updated successfully"}
    
    def delete_player(self, player_id):
        """Delete a player"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM players WHERE player_id = ?', (player_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Player deleted successfully"}
    
    # VIEW OPERATIONS
    def get_player_stats(self):
        """Get player statistics view"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM player_stats')
        stats = cursor.fetchall()
        conn.close()
        return stats
    
    def get_team_stats(self):
        """Get team statistics view"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM team_stats')
        stats = cursor.fetchall()
        conn.close()
        return stats
    
    def get_top_players_by_ranking(self, limit=10):
        """Get top players by ranking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, t.team_name 
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.ranking DESC
            LIMIT ?
        ''', (limit,))
        players = cursor.fetchall()
        conn.close()
        return players
    
    def search_players(self, search_term):
        """Search players by name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, t.team_name 
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            WHERE p.first_name LIKE ? OR p.last_name LIKE ?
            ORDER BY p.ranking DESC
        ''', (f'%{search_term}%', f'%{search_term}%'))
        players = cursor.fetchall()
        conn.close()
        return players
    
    def add_sample_data(self):
        """Add sample data to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM teams')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return {"success": False, "message": "Sample data already exists"}
        
        try:
            # Sample Teams
            teams_data = [
                ('Manchester United', 'Erik ten Hag', 1878, 'Manchester', 'Old Trafford'),
                ('Barcelona FC', 'Xavi Hernandez', 1899, 'Barcelona', 'Camp Nou'),
                ('Real Madrid', 'Carlo Ancelotti', 1902, 'Madrid', 'Santiago Bernabeu'),
                ('Bayern Munich', 'Thomas Tuchel', 1900, 'Munich', 'Allianz Arena'),
                ('Liverpool FC', 'Jurgen Klopp', 1892, 'Liverpool', 'Anfield'),
                ('Paris Saint-Germain', 'Luis Enrique', 1970, 'Paris', 'Parc des Princes')
            ]
            
            cursor.executemany('''
                INSERT INTO teams (team_name, coach_name, founded_year, city, stadium)
                VALUES (?, ?, ?, ?, ?)
            ''', teams_data)
            
            # Sample Players for Manchester United (team_id = 1)
            players_data = [
                # Manchester United
                ('Marcus', 'Rashford', 1, 'Forward', 10, 26, 180.0, 70.0, 92, 28, 12, 38),
                ('Bruno', 'Fernandes', 1, 'Midfielder', 8, 29, 179.0, 69.0, 90, 18, 20, 40),
                ('Casemiro', 'Silva', 1, 'Midfielder', 18, 31, 185.0, 84.0, 88, 5, 8, 35),
                ('Harry', 'Maguire', 1, 'Defender', 5, 30, 194.0, 100.0, 82, 3, 2, 32),
                
                # Barcelona FC (team_id = 2)
                ('Robert', 'Lewandowski', 2, 'Forward', 9, 35, 185.0, 81.0, 95, 35, 10, 40),
                ('Pedri', 'Gonzalez', 2, 'Midfielder', 8, 21, 174.0, 60.0, 91, 8, 15, 38),
                ('Gavi', 'Paez', 2, 'Midfielder', 6, 19, 173.0, 69.0, 89, 6, 12, 36),
                ('Ronald', 'Araujo', 2, 'Defender', 4, 24, 188.0, 83.0, 87, 4, 3, 35),
                
                # Real Madrid (team_id = 3)
                ('Vinicius', 'Junior', 3, 'Forward', 7, 23, 176.0, 73.0, 94, 30, 18, 42),
                ('Jude', 'Bellingham', 3, 'Midfielder', 5, 20, 186.0, 75.0, 93, 22, 14, 40),
                ('Luka', 'Modric', 3, 'Midfielder', 10, 38, 172.0, 66.0, 91, 8, 16, 38),
                ('Antonio', 'Rudiger', 3, 'Defender', 22, 30, 190.0, 85.0, 86, 2, 1, 39),
                
                # Bayern Munich (team_id = 4)
                ('Harry', 'Kane', 4, 'Forward', 9, 30, 188.0, 86.0, 96, 42, 15, 41),
                ('Jamal', 'Musiala', 4, 'Midfielder', 42, 21, 183.0, 70.0, 92, 16, 12, 38),
                ('Joshua', 'Kimmich', 4, 'Midfielder', 6, 28, 177.0, 75.0, 90, 6, 18, 40),
                ('Matthijs', 'de Ligt', 4, 'Defender', 4, 24, 189.0, 89.0, 88, 3, 2, 37),
                
                # Liverpool FC (team_id = 5)
                ('Mohamed', 'Salah', 5, 'Forward', 11, 31, 175.0, 71.0, 94, 32, 16, 40),
                ('Luis', 'Diaz', 5, 'Forward', 7, 26, 178.0, 67.0, 89, 18, 11, 38),
                ('Dominik', 'Szoboszlai', 5, 'Midfielder', 8, 23, 187.0, 74.0, 87, 9, 13, 36),
                ('Virgil', 'van Dijk', 5, 'Defender', 4, 32, 195.0, 92.0, 91, 5, 3, 39),
                
                # Paris Saint-Germain (team_id = 6)
                ('Kylian', 'Mbappe', 6, 'Forward', 7, 25, 178.0, 73.0, 98, 45, 20, 42),
                ('Ousmane', 'Dembele', 6, 'Forward', 10, 26, 178.0, 67.0, 90, 20, 15, 38),
                ('Vitinha', 'Silva', 6, 'Midfielder', 17, 23, 172.0, 64.0, 88, 7, 14, 40),
                ('Marquinhos', 'Correa', 6, 'Defender', 5, 29, 183.0, 75.0, 89, 4, 2, 41),
            ]
            
            cursor.executemany('''
                INSERT INTO players 
                (first_name, last_name, team_id, position, jersey_number, age, height, weight, 
                 ranking, goals, assists, matches_played)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', players_data)
            
            conn.commit()
            conn.close()
            return {"success": True, "message": f"Added {len(teams_data)} teams and {len(players_data)} players successfully"}
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return {"success": False, "message": f"Error adding sample data: {str(e)}"}
    
    def clear_all_data(self):
        """Clear all data from the database (useful for testing)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM players')
            cursor.execute('DELETE FROM teams')
            conn.commit()
            conn.close()
            return {"success": True, "message": "All data cleared successfully"}
        except Exception as e:
            conn.rollback()
            conn.close()
            return {"success": False, "message": f"Error clearing data: {str(e)}"}

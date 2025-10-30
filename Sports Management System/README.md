# 🏆 Sport Player Management System

A comprehensive web-based Sport Player Management System built with Python (Flask), SQLite, HTML, CSS, and JavaScript.

## Features

### 📊 Sample Data
- **One-Click Sample Data Loading**: Instantly populate the database with 6 teams and 24 players
- **Realistic Football Data**: Features real-world teams (Manchester United, Barcelona, Real Madrid, Bayern Munich, Liverpool, PSG)
- **World-Class Players**: Includes top players like Kylian Mbappe, Harry Kane, Lewandowski, Salah, and more
- **Complete Statistics**: All players have realistic rankings, goals, assists, and match data
- **Clear Data Option**: Ability to clear all data and start fresh
- See [SAMPLE_DATA.md](SAMPLE_DATA.md) for complete details

### 📊 Dashboard
- Overview of total teams, players, goals, and assists
- Top 5 players by ranking display
- Real-time statistics

### 👥 Team Management
- Add, edit, update, and delete teams
- Track team information: name, coach, founded year, city, stadium
- View all teams in a comprehensive table

### ⚽ Player Management
- Add, edit, update, and delete players
- Comprehensive player information:
  - Personal details (name, age, height, weight)
  - Team assignment
  - Position and jersey number
  - Performance metrics (goals, assists, matches played)
  - Ranking score
- Search functionality to find players quickly
- Filter players by team

### 🏅 Player Rankings
- View top players sorted by ranking score
- Adjustable ranking list (top 10, 25, 50, or 100)
- Comprehensive ranking display with performance metrics

### 📈 Statistics & Views
- **Player Statistics View**: Complete player performance analysis
  - Goals per match calculation
  - Comprehensive stats for all players
- **Team Statistics View**: Team-level analytics
  - Total players per team
  - Aggregate goals and assists
  - Team performance overview

### 🗄️ Database Features
- SQLite database with proper relationships
- SQL Views for advanced statistics
- Foreign key constraints for data integrity
- Automatic timestamps for record creation

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLite with SQL views
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: RESTful API architecture

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
Qoder/
│
├── app.py                  # Flask application and API routes
├── database.py             # Database operations and SQL queries
├── requirements.txt        # Python dependencies
├── sports_management.db    # SQLite database (auto-created)
│
├── templates/
│   └── index.html         # Main HTML template
│
└── static/
    ├── style.css          # CSS styling
    └── script.js          # JavaScript functionality
```

## Database Schema

### Teams Table
- `team_id` (Primary Key)
- `team_name` (Unique)
- `coach_name`
- `founded_year`
- `city`
- `stadium`
- `created_at`

### Players Table
- `player_id` (Primary Key)
- `first_name`
- `last_name`
- `team_id` (Foreign Key)
- `position`
- `jersey_number`
- `age`
- `height`
- `weight`
- `ranking`
- `goals`
- `assists`
- `matches_played`
- `created_at`

### SQL Views

#### player_stats View
Provides comprehensive player statistics including:
- Player name
- Team name
- Performance metrics
- Calculated goals per match

#### team_stats View
Provides team-level statistics including:
- Total players
- Aggregate goals and assists
- Team information

## API Endpoints

### Teams
- `GET /api/teams` - Get all teams
- `GET /api/teams/<id>` - Get team by ID
- `POST /api/teams` - Create new team
- `PUT /api/teams/<id>` - Update team
- `DELETE /api/teams/<id>` - Delete team

### Players
- `GET /api/players` - Get all players
- `GET /api/players/<id>` - Get player by ID
- `POST /api/players` - Create new player
- `PUT /api/players/<id>` - Update player
- `DELETE /api/players/<id>` - Delete player
- `GET /api/players/search?q=<term>` - Search players
- `GET /api/players/top/<limit>` - Get top players by ranking
- `GET /api/teams/<id>/players` - Get players by team

### Statistics
- `GET /api/stats/players` - Get player statistics view
- `GET /api/stats/teams` - Get team statistics view

## Usage Guide

### Adding a Team
1. Click on "Teams" in the navigation
2. Click the "+ Add Team" button
3. Fill in the team details
4. Click "Save"

### Adding a Player
1. Click on "Players" in the navigation
2. Click the "+ Add Player" button
3. Fill in player details including:
   - Name and personal information
   - Team assignment
   - Performance metrics
   - Ranking score
4. Click "Save"

### Viewing Rankings
1. Click on "Rankings" in the navigation
2. Select the number of top players to display
3. View players sorted by ranking score

### Viewing Statistics
1. Click on "Statistics" in the navigation
2. Toggle between "Player Statistics" and "Team Statistics" tabs
3. View comprehensive analytics

## Features Highlights

✅ **Full CRUD Operations**: Create, Read, Update, Delete for both teams and players  
✅ **SQL Views**: Advanced statistics using SQL views  
✅ **Responsive Design**: Works on desktop and mobile devices  
✅ **Search Functionality**: Quick player search  
✅ **Ranking System**: Sort and display players by performance  
✅ **Real-time Updates**: Instant UI updates after operations  
✅ **Data Validation**: Form validation for data integrity  
✅ **Foreign Key Relationships**: Proper database relationships  

## Future Enhancements

- User authentication and authorization
- Export data to CSV/Excel
- Advanced filtering and sorting
- Player performance graphs and charts
- Match management system
- Season tracking
- Image upload for players and teams

## License

This project is open-source and available for educational purposes.

## Author

Created as a comprehensive Sport Player Management System demonstration.

---

**Enjoy managing your sports teams and players! 🏆⚽🏀**

Delete Readme.md


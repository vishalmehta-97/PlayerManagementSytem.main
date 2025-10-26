# 📊 Sample Data Documentation

## Overview
The Sport Player Management System now includes comprehensive sample data featuring real-world football teams and players with realistic statistics.

## Sample Teams (6 Teams)

1. **Manchester United**
   - Coach: Erik ten Hag
   - Founded: 1878
   - City: Manchester
   - Stadium: Old Trafford

2. **Barcelona FC**
   - Coach: Xavi Hernandez
   - Founded: 1899
   - City: Barcelona
   - Stadium: Camp Nou

3. **Real Madrid**
   - Coach: Carlo Ancelotti
   - Founded: 1902
   - City: Madrid
   - Stadium: Santiago Bernabeu

4. **Bayern Munich**
   - Coach: Thomas Tuchel
   - Founded: 1900
   - City: Munich
   - Stadium: Allianz Arena

5. **Liverpool FC**
   - Coach: Jurgen Klopp
   - Founded: 1892
   - City: Liverpool
   - Stadium: Anfield

6. **Paris Saint-Germain**
   - Coach: Luis Enrique
   - Founded: 1970
   - City: Paris
   - Stadium: Parc des Princes

## Sample Players (24 Players)

### Manchester United (4 Players)
- **Marcus Rashford** - Forward #10 (Ranking: 92, Goals: 28)
- **Bruno Fernandes** - Midfielder #8 (Ranking: 90, Goals: 18, Assists: 20)
- **Casemiro Silva** - Midfielder #18 (Ranking: 88)
- **Harry Maguire** - Defender #5 (Ranking: 82)

### Barcelona FC (4 Players)
- **Robert Lewandowski** - Forward #9 (Ranking: 95, Goals: 35) ⭐ Top Scorer
- **Pedri Gonzalez** - Midfielder #8 (Ranking: 91)
- **Gavi Paez** - Midfielder #6 (Ranking: 89)
- **Ronald Araujo** - Defender #4 (Ranking: 87)

### Real Madrid (4 Players)
- **Vinicius Junior** - Forward #7 (Ranking: 94, Goals: 30)
- **Jude Bellingham** - Midfielder #5 (Ranking: 93, Goals: 22)
- **Luka Modric** - Midfielder #10 (Ranking: 91)
- **Antonio Rudiger** - Defender #22 (Ranking: 86)

### Bayern Munich (4 Players)
- **Harry Kane** - Forward #9 (Ranking: 96, Goals: 42) ⭐ Top Scorer
- **Jamal Musiala** - Midfielder #42 (Ranking: 92)
- **Joshua Kimmich** - Midfielder #6 (Ranking: 90, Assists: 18)
- **Matthijs de Ligt** - Defender #4 (Ranking: 88)

### Liverpool FC (4 Players)
- **Mohamed Salah** - Forward #11 (Ranking: 94, Goals: 32)
- **Luis Diaz** - Forward #7 (Ranking: 89)
- **Dominik Szoboszlai** - Midfielder #8 (Ranking: 87)
- **Virgil van Dijk** - Defender #4 (Ranking: 91)

### Paris Saint-Germain (4 Players)
- **Kylian Mbappe** - Forward #7 (Ranking: 98, Goals: 45) ⭐ Highest Ranking
- **Ousmane Dembele** - Forward #10 (Ranking: 90, Goals: 20)
- **Vitinha Silva** - Midfielder #17 (Ranking: 88)
- **Marquinhos Correa** - Defender #5 (Ranking: 89)

## Statistics Summary

### Top 5 Players by Ranking:
1. **Kylian Mbappe** (PSG) - Ranking: 98
2. **Harry Kane** (Bayern Munich) - Ranking: 96
3. **Robert Lewandowski** (Barcelona) - Ranking: 95
4. **Vinicius Junior** (Real Madrid) - Ranking: 94
5. **Mohamed Salah** (Liverpool) - Ranking: 94

### Top Goal Scorers:
1. **Kylian Mbappe** - 45 goals
2. **Harry Kane** - 42 goals
3. **Robert Lewandowski** - 35 goals
4. **Mohamed Salah** - 32 goals
5. **Vinicius Junior** - 30 goals

### Player Positions Distribution:
- **Forwards**: 10 players
- **Midfielders**: 10 players
- **Defenders**: 4 players

### Total Statistics:
- **Total Teams**: 6
- **Total Players**: 24
- **Total Goals**: 444 goals
- **Total Assists**: 245 assists
- **Average Ranking**: 89.75

## How to Use Sample Data

### Loading Sample Data:
1. Open the application in your browser
2. Navigate to the **Dashboard** section
3. Click the **"📊 Load Sample Data"** button
4. Confirm the action
5. The system will populate the database with all teams and players

### Clearing All Data:
1. Navigate to the **Dashboard** section
2. Click the **"🗑️ Clear All Data"** button
3. Confirm the action (⚠️ This cannot be undone!)
4. All teams and players will be removed

### API Endpoints:

#### Load Sample Data
```
POST /api/sample-data
```

#### Clear All Data
```
DELETE /api/clear-data
```

## Features Demonstrated

✅ **Realistic Data**: Based on real football players and teams  
✅ **Complete Information**: All fields populated with realistic values  
✅ **Ranking System**: Players ranked from 82 to 98  
✅ **Performance Metrics**: Goals, assists, and matches played  
✅ **Team Distribution**: 4 players per team  
✅ **Position Variety**: Forwards, Midfielders, and Defenders  

## Notes

- Sample data can only be loaded once (prevents duplicates)
- If data already exists, you'll receive an error message
- Use "Clear All Data" first if you want to reload sample data
- All player statistics are fictional but realistic
- Player rankings range from 82-98 (world-class players)

## Testing Scenarios

With sample data loaded, you can test:
1. **Rankings View**: See top players sorted by ranking
2. **Team Statistics**: View aggregate stats for each team
3. **Player Search**: Search for players like "Mbappe" or "Kane"
4. **Player Stats View**: See goals per match calculations
5. **CRUD Operations**: Edit, update, or delete any sample data
6. **Sorting**: Players automatically sorted by ranking

---

**Enjoy exploring the Sport Player Management System with realistic data! ⚽🏆**

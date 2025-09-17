# GeoGuessr Results Extractor

This tool extracts game data from GeoGuessr mHTML files and exports it to CSV format for analysis and visualization.

## Features

- **Player Results**: Extracts position, points, duration, and steps for each round (5 rounds per game)
- **Game Settings**: Captures map information, game settings, and time limits
- **Challenge Data**: Extracts challenge dates, unique IDs, and titles
- **CSV Export**: Generates structured CSV files for easy analysis

## Usage

1. **Save mHTML files**: Save GeoGuessr challenge results as mHTML files in the `games/` folder
2. **Run the extractor**: 
   ```bash
   python3 geoguessr_extractor.py
   ```
3. **View results**: Check `geoguessr_results.csv` for extracted data

## Output Format

The CSV contains columns for:
- Challenge metadata (file name, ID, date, title)
- Game settings (map name, creator, time limits, movement settings)
- Player data (position, name)
- Round-by-round scores (points, duration, steps for rounds 1-5)
- Total scores (total points, duration, steps)

## Requirements

- Python 3.6+
- beautifulsoup4
- lxml

Install dependencies:
```bash
pip3 install beautifulsoup4 lxml
```

## 🌐 Web Dashboard

A beautiful, interactive dashboard is included! 

**Features:**
- 📊 Interactive charts (performance over time, round analysis, scatter plots)
- 🏆 Live leaderboard with rankings and statistics
- 🔍 Smart filters (by player, game, chart type)
- 📱 Mobile-responsive design
- 🎨 Modern, clean interface

**Quick Start:**
1. Generate your data: `python3 geoguessr_extractor.py`
2. Test locally: `python3 serve_dashboard.py`
3. Visit: http://localhost:8000/dashboard.html

**Publishing Online:**
See `DEPLOYMENT.md` for easy ways to publish your dashboard online (GitHub Pages, Netlify, Vercel, etc.)

## Next Steps

This CSV data can be used to:
- ✅ **Interactive web dashboard** (included!)
- Analyze game statistics and trends
- Share results with friends online
- Track improvement and competition between players

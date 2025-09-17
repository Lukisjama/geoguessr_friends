# 🚀 Publishing Your GeoGuessr Dashboard Online

## Quick Start

1. **Generate your data**:
   ```bash
   python3 geoguessr_extractor.py
   ```

2. **Test locally**:
   ```bash
   python3 serve_dashboard.py
   ```
   Then visit: http://localhost:8000/dashboard.html

## 🌐 Publishing Options

### Option 1: GitHub Pages (Free & Easy)

1. **Create a GitHub repository**:
   - Go to GitHub.com and create a new repository
   - Name it something like `geoguessr-dashboard`

2. **Upload your files**:
   - Upload `dashboard.html`
   - Upload `geoguessr_results.csv`
   - Upload `README.md`

3. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Select "Deploy from a branch" → "main"
   - Your dashboard will be available at: `https://yourusername.github.io/geoguessr-dashboard/dashboard.html`

### Option 2: Netlify (Free & Easy)

1. **Prepare files**:
   - Put `dashboard.html` and `geoguessr_results.csv` in a folder

2. **Deploy**:
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop your folder
   - Get instant URL like: `https://amazing-name-123456.netlify.app`

### Option 3: Vercel (Free & Easy)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

### Option 4: Surge.sh (Free & Simple)

1. **Install Surge**:
   ```bash
   npm install -g surge
   ```

2. **Deploy**:
   ```bash
   surge
   ```

## 📱 Features of Your Dashboard

- **📊 Interactive Charts**: Performance over time, round analysis, scatter plots
- **🏆 Live Leaderboard**: Rankings based on total points, wins, averages
- **🔍 Smart Filters**: Filter by player, game, or chart type
- **📱 Mobile Responsive**: Works great on phones and tablets
- **🎨 Beautiful Design**: Modern, clean interface with smooth animations

## 🔄 Updating Your Dashboard

1. **Add new games**: Save new mHTML files to `games/` folder
2. **Regenerate data**: Run `python3 geoguessr_extractor.py`
3. **Update online**: Upload the new `geoguessr_results.csv` file

## 💡 Tips for Sharing

- **Share the direct link** to your dashboard with friends
- **Update regularly** to keep the competition fresh
- **Use descriptive names** for your challenges
- **Encourage friends** to save their mHTML files too

## 🎯 Customization Ideas

- **Add your own colors** by editing the CSS in `dashboard.html`
- **Change the title** and description in the header
- **Add more charts** using Chart.js
- **Include game screenshots** or maps
- **Add player avatars** or flags

Your dashboard is now ready to showcase your GeoGuessr skills! 🎉

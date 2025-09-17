# 🚀 GitHub + Netlify Auto-Deploy Setup

## Step 1: Create GitHub Repository

1. **Go to GitHub**: [github.com](https://github.com)
2. **Create new repository**:
   - Click "New repository" (green button)
   - Repository name: `geoguessr-dashboard`
   - Description: `Interactive GeoGuessr competition dashboard`
   - Make it **Public** (required for free Netlify)
   - ✅ Add README file
   - Click "Create repository"

## Step 2: Upload Your Files to GitHub

### Option A: Using GitHub Web Interface (Easiest)

1. **Upload files**:
   - Click "uploading an existing file"
   - Drag these files from your `publish` folder:
     - `index.html`
     - `dashboard.html` 
     - `geoguessr_results.csv`
   - Commit message: "Initial dashboard upload"
   - Click "Commit changes"

### Option B: Using Git Command Line

```bash
# Navigate to your project folder
cd "/Users/lukasjanmarek/Documents/Mentoring/Geoguessr scraper"

# Initialize git repository
git init

# Add files
git add publish/*

# Commit
git commit -m "Initial dashboard upload"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/geoguessr-dashboard.git

# Push to GitHub
git push -u origin main
```

## Step 3: Connect GitHub to Netlify

1. **Go to Netlify**: [netlify.com](https://netlify.com)
2. **Sign up/Login** with GitHub account
3. **New site from Git**:
   - Click "New site from Git"
   - Choose "GitHub" as provider
   - Authorize Netlify to access your GitHub
   - Select your `geoguessr-dashboard` repository
   - Click "Deploy site"

4. **Configure build settings**:
   - Build command: (leave empty)
   - Publish directory: `/` (root)
   - Click "Deploy site"

## Step 4: Get Your Live URL

- Netlify will give you a URL like: `https://amazing-name-123456.netlify.app`
- Your dashboard will be live at this URL!

## 🔄 Automatic Updates

Now whenever you update your data:

1. **Generate new data**:
   ```bash
   python3 geoguessr_extractor.py
   python3 prepare_publish.py
   ```

2. **Upload to GitHub**:
   - Go to your GitHub repository
   - Click "uploading an existing file"
   - Upload the new `geoguessr_results.csv`
   - Commit changes

3. **Netlify auto-deploys**:
   - Netlify automatically detects the change
   - Redeploys your site in ~30 seconds
   - Your dashboard updates with new data!

## 🎯 Benefits

✅ **Automatic updates** - No manual deployment needed
✅ **Version history** - GitHub tracks all your data changes
✅ **Professional URL** - Custom domain available
✅ **HTTPS** - Secure connection automatically
✅ **Fast deployment** - Updates go live in seconds

## 📱 Sharing

Share your Netlify URL with friends:
- They can bookmark it
- It updates automatically when you add new games
- Works on mobile and desktop

## 🔧 Custom Domain (Optional)

In Netlify:
1. Go to Site settings → Domain management
2. Add custom domain (like `yourname-geoguessr.netlify.app`)
3. Update DNS settings if needed

Your dashboard will now update automatically every time you add new GeoGuessr games! 🎉

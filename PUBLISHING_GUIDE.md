# 🚀 Quick Online Publishing Guide

## Option 1: Netlify Drop (Easiest - 2 minutes!)

1. **Prepare your files**:
   - Make sure you have `dashboard.html` and `geoguessr_results.csv` in your folder

2. **Go to Netlify**:
   - Visit [netlify.com](https://netlify.com)
   - Click "Deploy manually" or drag & drop

3. **Upload files**:
   - Drag your folder (or just the 2 files) onto the Netlify page
   - Wait 30 seconds for deployment

4. **Get your URL**:
   - You'll get a URL like: `https://amazing-name-123456.netlify.app`
   - Share this with your friends!

## Option 2: GitHub Pages (Free & Professional)

1. **Create GitHub account** (if you don't have one):
   - Go to [github.com](https://github.com) and sign up

2. **Create new repository**:
   - Click "New repository"
   - Name it `geoguessr-dashboard`
   - Make it public
   - Click "Create repository"

3. **Upload files**:
   - Click "uploading an existing file"
   - Drag `dashboard.html` and `geoguessr_results.csv`
   - Commit changes

4. **Enable Pages**:
   - Go to Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: "main"
   - Save

5. **Your URL**: `https://yourusername.github.io/geoguessr-dashboard/dashboard.html`

## Option 3: Surge.sh (Command Line - Super Fast)

1. **Install Surge**:
   ```bash
   npm install -g surge
   ```

2. **Deploy**:
   ```bash
   surge
   ```
   - Follow the prompts
   - Get instant URL!

## Option 4: Vercel (One Command)

1. **Install Vercel**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

## 🎯 Recommended: Netlify Drop

**Why Netlify?**
- ✅ **No account needed** (for drop method)
- ✅ **Instant deployment** (30 seconds)
- ✅ **Custom domain** available
- ✅ **HTTPS** automatically
- ✅ **Mobile-friendly** URLs

## 📱 After Publishing

1. **Test your dashboard**: Visit your URL
2. **Share with friends**: Send them the link
3. **Update data**: When you add new games:
   - Run `python3 geoguessr_extractor.py`
   - Upload new `geoguessr_results.csv` to your site

## 🔄 Updating Your Dashboard

**For Netlify Drop**:
- Just drag & drop the new CSV file

**For GitHub Pages**:
- Upload new CSV file to your repository

**For Surge/Vercel**:
- Run the deploy command again

Your dashboard will be live and shareable in minutes! 🎉

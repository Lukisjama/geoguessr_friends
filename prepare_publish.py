#!/usr/bin/env python3
"""
Prepare files for online publishing
"""

import os
import shutil
from pathlib import Path

def prepare_for_publishing():
    """Prepare files for online publishing"""
    
    print("🚀 Preparing GeoGuessr Dashboard for Online Publishing")
    print("=" * 50)
    
    # Create publish directory
    publish_dir = Path("publish")
    if publish_dir.exists():
        shutil.rmtree(publish_dir)
    publish_dir.mkdir()
    
    # Copy required files
    files_to_copy = [
        "dashboard.html",
        "geoguessr_results.csv"
    ]
    
    copied_files = []
    
    # Create index.html redirect file
    index_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoGuessr Dashboard</title>
    <meta http-equiv="refresh" content="0; url=dashboard.html">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        p {
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        .loading {
            font-size: 1rem;
            opacity: 0.8;
        }
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 GeoGuessr Dashboard</h1>
        <p>Redirecting to your dashboard...</p>
        <div class="spinner"></div>
        <p class="loading">If you're not redirected automatically, <a href="dashboard.html" style="color: white; text-decoration: underline;">click here</a></p>
    </div>
    
    <script>
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 1000);
    </script>
</body>
</html>'''
    
    # Write index.html
    with open(publish_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    copied_files.append("index.html")
    print(f"✅ Created index.html")
    
    # Copy other files
    for file_name in files_to_copy:
        source_file = Path(file_name)
        if source_file.exists():
            shutil.copy2(source_file, publish_dir / file_name)
            copied_files.append(file_name)
            print(f"✅ Copied {file_name}")
        else:
            print(f"❌ Missing {file_name}")
    
    if copied_files:
        print(f"\n📁 Files ready in '{publish_dir}' folder:")
        for file in copied_files:
            print(f"   - {file}")
        
        print(f"\n🌐 Publishing Options:")
        print(f"1. Netlify Drop: Drag the '{publish_dir}' folder to netlify.com")
        print(f"2. GitHub Pages: Upload files to a GitHub repository")
        print(f"3. Surge.sh: Run 'surge {publish_dir}'")
        print(f"4. Vercel: Run 'vercel {publish_dir}'")
        
        print(f"\n📖 See PUBLISHING_GUIDE.md for detailed instructions")
        
        # Show absolute path
        abs_path = publish_dir.absolute()
        print(f"\n📂 Full path: {abs_path}")
        
    else:
        print("❌ No files to publish. Make sure you have:")
        print("   - dashboard.html")
        print("   - geoguessr_results.csv")
        print("\nRun 'python3 geoguessr_extractor.py' first to generate the CSV")

if __name__ == "__main__":
    prepare_for_publishing()

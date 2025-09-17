#!/usr/bin/env python3
"""
Check files for GitHub/Netlify publishing
"""

import os
from pathlib import Path

def check_publishing_files():
    """Check if all required files are present for GitHub/Netlify publishing"""
    
    print("🚀 Checking GeoGuessr Dashboard for GitHub/Netlify Publishing")
    print("=" * 60)
    
    # Required files for Netlify
    required_files = [
        "dashboard.html",
        "geoguessr_results.csv"
    ]
    
    missing_files = []
    present_files = []
    
    for file_name in required_files:
        if Path(file_name).exists():
            present_files.append(file_name)
            print(f"✅ {file_name}")
        else:
            missing_files.append(file_name)
            print(f"❌ {file_name}")
    
    print(f"\n📊 Status:")
    print(f"   Present: {len(present_files)}/{len(required_files)} files")
    
    if missing_files:
        print(f"   Missing: {', '.join(missing_files)}")
        print(f"\n🔧 To fix missing files:")
        print(f"   1. Run 'python3 geoguessr_extractor.py' to generate CSV")
        print(f"   2. Make sure dashboard.html exists")
        return False
    
    print(f"\n🎉 All files ready for GitHub/Netlify!")
    print(f"\n📋 Next steps:")
    print(f"   1. Files are already in your GitHub repository")
    print(f"   2. Connect your GitHub repo to Netlify")
    print(f"   3. Set publish directory to '/' (root)")
    print(f"   4. Netlify will automatically deploy from GitHub")
    
    print(f"\n🌐 Your dashboard will be available at:")
    print(f"   https://your-netlify-site.netlify.app/dashboard.html")
    
    return True

if __name__ == "__main__":
    check_publishing_files()

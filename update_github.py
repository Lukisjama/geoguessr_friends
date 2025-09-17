#!/usr/bin/env python3
"""
Update GitHub repository with new GeoGuessr data
"""

import os
import subprocess
import sys
from pathlib import Path

def update_github():
    """Update GitHub repository with latest data"""
    
    print("🔄 Updating GeoGuessr Dashboard on GitHub")
    print("=" * 40)
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not a git repository!")
        print("Please follow GITHUB_NETLIFY_SETUP.md first")
        return
    
    # Regenerate data
    print("📊 Regenerating data...")
    try:
        subprocess.run(["python3", "geoguessr_extractor.py"], check=True)
        subprocess.run(["python3", "prepare_publish.py"], check=True)
        print("✅ Data regenerated")
    except subprocess.CalledProcessError:
        print("❌ Error regenerating data")
        return
    
    # Check git status
    try:
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, check=True)
        if not result.stdout.strip():
            print("✅ No changes to commit")
            return
        
        print("📝 Changes detected:")
        print(result.stdout)
        
        # Add changes
        subprocess.run(["git", "add", "publish/"], check=True)
        print("✅ Files staged")
        
        # Commit
        commit_msg = f"Update GeoGuessr data - {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        print("✅ Changes committed")
        
        # Push
        subprocess.run(["git", "push"], check=True)
        print("✅ Pushed to GitHub")
        
        print("\n🚀 Netlify will automatically deploy the updates!")
        print("⏱️  Check your Netlify dashboard in ~30 seconds")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        print("Make sure you have:")
        print("- Git configured with your credentials")
        print("- GitHub repository set up")
        print("- Netlify connected to your GitHub repo")

def setup_git():
    """Help set up git repository"""
    
    print("🔧 Setting up Git Repository")
    print("=" * 30)
    
    if Path(".git").exists():
        print("✅ Git repository already exists")
        return
    
    # Initialize git
    subprocess.run(["git", "init"], check=True)
    print("✅ Git repository initialized")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
games/
*.log
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore created")
    
    print("\n📋 Next steps:")
    print("1. Create GitHub repository")
    print("2. Add remote: git remote add origin https://github.com/USERNAME/REPO.git")
    print("3. Push: git push -u origin main")
    print("4. Connect to Netlify")
    print("\nSee GITHUB_NETLIFY_SETUP.md for detailed instructions")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_git()
    else:
        update_github()

if __name__ == "__main__":
    main()

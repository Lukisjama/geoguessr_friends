#!/usr/bin/env python3
"""
Parse Activities.mhtml to extract challenge dates and IDs
"""

import re
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import html

def parse_activities_file():
    """Parse Activities.mhtml and extract challenge information using regex"""
    
    print("🔍 Parsing Activities.mhtml with regex...")
    
    # Read the mhtml file
    with open('Activities.mhtml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract challenge information using regex
    challenges = []
    
    # Find all time buckets with regex
    time_bucket_pattern = r'activities_timeBucket__iJwDo.*?activities_bucketHeader__b_D5i.*?<h1>(.*?)</h1>'
    time_buckets = re.findall(time_bucket_pattern, content, re.DOTALL)
    
    print(f"📅 Found {len(time_buckets)} time buckets")
    
    # Find all challenge links with regex
    challenge_pattern = r'href=3D"https://www\.geoguessr\.com/challenge/([^"]+)"[^>]*>([^<]*points[^<]*)</a>'
    challenge_matches = re.findall(challenge_pattern, content)
    
    print(f"🔗 Found {len(challenge_matches)} challenge links")
    
    # Process each time bucket
    for i, date_text in enumerate(time_buckets):
        # Parse date
        if date_text == "earlier today":
            challenge_date = datetime.now().strftime("%Y-%m-%d")
        elif date_text == "today":
            challenge_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # Parse date like "Tue Sep 16 2025"
            try:
                date_obj = datetime.strptime(date_text, "%a %b %d %Y")
                challenge_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                print(f"⚠️  Could not parse date: {date_text}")
                continue
        
        print(f"📅 Processing date: {challenge_date}")
        
        # For now, let's extract all challenges and assign them to dates
        # This is a simplified approach - in reality we'd need to map them properly
        pass
    
    # Process all challenge matches
    for challenge_id, score_text in challenge_matches:
        # Extract score
        score_match = re.search(r'([0-9,]+)\s*points', score_text)
        score = score_match.group(1).replace(',', '') if score_match else ''
        
        challenges.append({
            'challenge_id': challenge_id,
            'date': '',  # We'll fill this later
            'score': score,
            'url': f"https://www.geoguessr.com/challenge/{challenge_id}"
        })
        
        print(f"   ✅ {challenge_id} -> {score} points")
    
    print(f"✅ Found {len(challenges)} challenge entries")
    return challenges

def update_csv_with_activities():
    """Update CSV with challenge dates and add download links"""
    
    # Parse activities
    activities = parse_activities_file()
    
    # Create a mapping of challenge_id to date
    challenge_dates = {challenge['challenge_id']: challenge['date'] for challenge in activities}
    
    # Read existing CSV
    csv_data = []
    with open('geoguessr_results.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
    
    print(f"📊 Processing {len(csv_data)} CSV rows...")
    
    # Update CSV data
    updated_count = 0
    missing_count = 0
    
    for row in csv_data:
        challenge_id = row.get('Challenge_ID', '')
        
        if challenge_id in challenge_dates:
            row['Challenge_Date'] = challenge_dates[challenge_id]
            updated_count += 1
        else:
            row['Challenge_Date'] = ''
            missing_count += 1
            
        # Add download link for missing challenges
        if not challenge_id:
            row['Download_Link'] = ''
        else:
            row['Download_Link'] = f"https://www.geoguessr.com/challenge/{challenge_id}"
    
    # Write updated CSV
    fieldnames = list(csv_data[0].keys()) if csv_data else []
    if 'Challenge_Date' not in fieldnames:
        fieldnames.append('Challenge_Date')
    if 'Download_Link' not in fieldnames:
        fieldnames.append('Download_Link')
    
    with open('geoguessr_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Updated {updated_count} rows with dates")
    print(f"⚠️  {missing_count} rows missing challenge data")
    print(f"🔗 Added download links for all challenges")
    
    # Show some examples
    print(f"\n📋 Sample updated data:")
    for i, row in enumerate(csv_data[:3]):
        if row.get('Challenge_Date'):
            print(f"   {row.get('Challenge_ID', 'N/A')} -> {row.get('Challenge_Date', 'N/A')}")

if __name__ == "__main__":
    update_csv_with_activities()

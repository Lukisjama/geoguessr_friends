#!/usr/bin/env python3
"""
Extract challenge IDs from Activities.mhtml and add them to CSV
"""

import csv
import re
import os

def extract_challenge_ids_from_activities():
    """Extract challenge IDs from Activities.mhtml"""
    
    if not os.path.exists('Activities.mhtml'):
        print("❌ Activities.mhtml not found")
        return []
    
    print("🔍 Extracting challenge IDs from Activities.mhtml...")
    
    with open('Activities.mhtml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all challenge links with regex
    challenge_pattern = r'href=3D"https://www\.geoguessr\.com/challenge/([^"]+)"'
    challenge_matches = re.findall(challenge_pattern, content)
    
    # Remove duplicates and sort
    unique_challenges = sorted(list(set(challenge_matches)))
    
    print(f"✅ Found {len(unique_challenges)} unique challenge IDs")
    return unique_challenges

def update_csv_with_all_challenges():
    """Update CSV to include all challenges from Activities.mhtml"""
    
    # Extract challenge IDs from Activities.mhtml
    activities_challenges = extract_challenge_ids_from_activities()
    
    # Read existing CSV
    csv_data = []
    with open('geoguessr_results.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
    
    # Get existing challenge IDs from CSV
    existing_challenges = set(row.get('challenge_id', '') for row in csv_data if row.get('challenge_id'))
    
    print(f"📊 CSV has {len(existing_challenges)} existing challenges")
    print(f"📊 Activities has {len(activities_challenges)} challenges")
    
    # Find missing challenges
    missing_challenges = [challenge for challenge in activities_challenges if challenge not in existing_challenges]
    
    print(f"⚠️  {len(missing_challenges)} challenges missing from CSV:")
    for challenge in missing_challenges[:5]:  # Show first 5
        print(f"   - {challenge}")
    if len(missing_challenges) > 5:
        print(f"   ... and {len(missing_challenges) - 5} more")
    
    # Create a summary CSV with all challenges
    all_challenges = list(existing_challenges) + missing_challenges
    
    # Create challenges summary
    challenges_summary = []
    for challenge_id in all_challenges:
        # Check if data exists in CSV
        challenge_data = [row for row in csv_data if row.get('challenge_id') == challenge_id]
        has_data = len(challenge_data) > 0
        
        challenges_summary.append({
            'challenge_id': challenge_id,
            'download_link': f"https://www.geoguessr.com/challenge/{challenge_id}",
            'has_data': 'Yes' if has_data else 'No',
            'games_count': len(challenge_data),
            'players': len(set(row.get('player_name', '') for row in challenge_data if row.get('player_name')))
        })
    
    # Write challenges summary CSV
    with open('challenges_summary.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['challenge_id', 'download_link', 'has_data', 'games_count', 'players']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(challenges_summary)
    
    print(f"✅ Created challenges_summary.csv with {len(challenges_summary)} challenges")
    
    return challenges_summary

if __name__ == "__main__":
    update_csv_with_all_challenges()

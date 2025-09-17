#!/usr/bin/env python3
"""
Simple script to add download links to CSV based on challenge IDs
"""

import csv
import re

def add_download_links():
    """Add download links to CSV based on existing challenge IDs"""
    
    print("🔗 Adding download links to CSV...")
    
    # Read existing CSV
    csv_data = []
    with open('geoguessr_results.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
    
    print(f"📊 Processing {len(csv_data)} CSV rows...")
    
    # Add download links
    updated_count = 0
    
    for row in csv_data:
        challenge_id = row.get('challenge_id', '').strip()
        
        if challenge_id:
            row['Download_Link'] = f"https://www.geoguessr.com/challenge/{challenge_id}"
            updated_count += 1
        else:
            row['Download_Link'] = ''
    
    # Write updated CSV
    fieldnames = list(csv_data[0].keys()) if csv_data else []
    if 'Download_Link' not in fieldnames:
        fieldnames.append('Download_Link')
    
    with open('geoguessr_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Added download links for {updated_count} challenges")
    
    # Show some examples
    print(f"\n📋 Sample download links:")
    for i, row in enumerate(csv_data[:3]):
        if row.get('Download_Link'):
            print(f"   {row.get('challenge_id', 'N/A')} -> {row.get('Download_Link', 'N/A')}")

if __name__ == "__main__":
    add_download_links()

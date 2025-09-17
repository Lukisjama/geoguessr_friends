#!/usr/bin/env python3
"""
GeoGuessr Results Extractor

This script extracts game data from GeoGuessr mHTML files and exports it to CSV format.
It extracts:
- Player results (position, points, duration, steps for each round)
- Game settings and map information
- Challenge date and unique ID
"""

import os
import re
import csv
import json
import html
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import argparse


class GeoGuessrExtractor:
    def __init__(self, games_folder: str = "games"):
        self.games_folder = Path(games_folder)
        self.extracted_data = []
        
    def extract_mhtml_content(self, file_path: Path) -> Optional[str]:
        """Extract HTML content from mHTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the HTML content section
            html_start = content.find('<!DOCTYPE html>')
            if html_start == -1:
                print(f"Warning: No HTML content found in {file_path}")
                return None
                
            # Extract HTML content
            html_content = content[html_start:]
            
            # Clean up HTML-encoded characters using Python's html module
            html_content = html.unescape(html_content)
            
            # Additional cleanup for quoted-printable encoding
            html_content = html_content.replace('=3D', '=')
            html_content = html_content.replace('=3C', '<')
            html_content = html_content.replace('=3E', '>')
            html_content = html_content.replace('=22', '"')
            html_content = html_content.replace('=20', ' ')
            html_content = html_content.replace('=0A', '')
            html_content = html_content.replace('=0D', '')
            html_content = html_content.replace('=\n', '')
            html_content = html_content.replace('=\r', '')
            
            # Fix UTF-8 encoded characters (like Czech characters)
            html_content = self.decode_utf8_entities(html_content)
            
            return html_content
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def decode_utf8_entities(self, text: str) -> str:
        """Decode UTF-8 encoded entities like =C5=A1 to proper characters"""
        import urllib.parse
        
        # Find all patterns like =XX=XX (UTF-8 encoded characters)
        def replace_utf8_entity(match):
            encoded_bytes = match.group(1)
            try:
                # Convert =XX=XX format to bytes
                hex_pairs = encoded_bytes.split('=')
                hex_pairs = [pair for pair in hex_pairs if pair]  # Remove empty strings
                byte_values = [int(pair, 16) for pair in hex_pairs]
                bytes_obj = bytes(byte_values)
                # Decode as UTF-8
                return bytes_obj.decode('utf-8')
            except (ValueError, UnicodeDecodeError):
                return match.group(0)  # Return original if decoding fails
        
        # Pattern to match =XX=XX sequences (UTF-8 encoded characters)
        pattern = r'=([A-F0-9]{2}(?:=[A-F0-9]{2})*)'
        return re.sub(pattern, replace_utf8_entity, text)
    
    def extract_challenge_info(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract challenge date and ID from mHTML content"""
        challenge_info = {
            'file_name': file_path.name,
            'challenge_id': None,
            'challenge_date': None,
            'challenge_title': None
        }
        
        # Extract date from mHTML header
        date_match = re.search(r'Date:\s*(.+)', content)
        if date_match:
            try:
                date_str = date_match.group(1).strip()
                # Parse the date format: "Wed, 17 Sep 2025 13:32:36 +0200"
                challenge_info['challenge_date'] = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z').isoformat()
            except ValueError:
                print(f"Warning: Could not parse date from {file_path}")
        
        # Extract challenge ID from URL
        url_match = re.search(r'https://www\.geoguessr\.com/results/([A-Za-z0-9]+)', content)
        if url_match:
            challenge_info['challenge_id'] = url_match.group(1)
        
        # Extract challenge title
        title_match = re.search(r'Subject:\s*(.+)', content)
        if title_match:
            challenge_info['challenge_title'] = title_match.group(1).strip()
        
        return challenge_info
    
    def extract_game_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract game settings and map information"""
        game_info = {
            'map_name': None,
            'map_creator': None,
            'game_settings': None,
            'time_limit': None,
            'movement': None,
            'panning': None,
            'zooming': None
        }
        
        # Find the game info section
        game_info_div = soup.find('div', class_='results_gameInfo__W1ggd')
        if not game_info_div:
            return game_info
        
        # Extract map information
        map_links = game_info_div.find_all('a', href=True)
        for link in map_links:
            href = link.get('href', '')
            if '/maps/' in href:
                game_info['map_name'] = link.get_text(strip=True)
                break
        
        # Extract map creator
        creator_text = game_info_div.get_text()
        creator_match = re.search(r'Created by\s*(.+)', creator_text)
        if creator_match:
            game_info['map_creator'] = creator_match.group(1).strip()
        
        # Extract game settings from info cards
        info_cards = game_info_div.find_all('div', class_='info-card_card__y3eBq')
        for card in info_cards:
            title_elem = card.find('h3', class_='info-card_title__QWuny')
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                if 'Game settings' in title_text or 'Settings' in title_text:
                    # Look for settings in the card content
                    content_div = card.find('div', class_='info-card_content___gJYt')
                    if content_div:
                        settings_text = content_div.get_text()
                        game_info['game_settings'] = settings_text.strip()
                        
                        # Try to extract specific settings
                        if 'Time limit' in settings_text:
                            time_match = re.search(r'Time limit[:\s]*(\d+)', settings_text)
                            if time_match:
                                game_info['time_limit'] = time_match.group(1)
                        
                        if 'Movement' in settings_text:
                            game_info['movement'] = 'Allowed' if 'Allowed' in settings_text else 'Disabled'
                        
                        if 'Panning' in settings_text:
                            game_info['panning'] = 'Allowed' if 'Allowed' in settings_text else 'Disabled'
                        
                        if 'Zooming' in settings_text:
                            game_info['zooming'] = 'Allowed' if 'Allowed' in settings_text else 'Disabled'
        
        return game_info
    
    def parse_duration(self, duration_str: str) -> str:
        """Convert duration from 'xx min, xx sec' format to 'HH:mm:ss' format"""
        if not duration_str or duration_str.strip() == '':
            return '00:00:00'
        
        duration_str = duration_str.strip()
        total_seconds = 0
        
        # Parse minutes
        min_match = re.search(r'(\d+)\s*min', duration_str)
        if min_match:
            total_seconds += int(min_match.group(1)) * 60
        
        # Parse seconds
        sec_match = re.search(r'(\d+)\s*sec', duration_str)
        if sec_match:
            total_seconds += int(sec_match.group(1))
        
        # Convert to HH:mm:ss format
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def extract_results_table(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract player results from the results table"""
        results = []
        
        # Find the results table
        table_div = soup.find('div', class_=re.compile(r'results_table'))
        if not table_div:
            return results
        
        # Find all player rows (skip header row)
        rows = table_div.find_all('div', class_='results_row__JCFGA')
        header_row = table_div.find('div', class_='results_headerRow__IQUH5')
        
        if header_row:
            rows = [row for row in rows if row != header_row]
        
        for row in rows:
            player_data = {
                'position': None,
                'player_name': None,
                'round_1_points': None,
                'round_1_duration': None,
                'round_1_steps': None,
                'round_2_points': None,
                'round_2_duration': None,
                'round_2_steps': None,
                'round_3_points': None,
                'round_3_duration': None,
                'round_3_steps': None,
                'round_4_points': None,
                'round_4_duration': None,
                'round_4_steps': None,
                'round_5_points': None,
                'round_5_duration': None,
                'round_5_steps': None,
                'total_points': None,
                'total_duration': None,
                'total_steps': None
            }
            
            # Extract position
            position_span = row.find('span', class_='results_position__3Hyv4')
            if position_span:
                position_text = position_span.get_text(strip=True).replace('.', '')
                if position_text.isdigit():
                    player_data['position'] = int(position_text)
            
            # Extract player name
            user_link = row.find('div', class_='results_userLink__1k2fP')
            if user_link:
                img_tag = user_link.find('img', alt=True)
                if img_tag:
                    player_data['player_name'] = img_tag.get('alt', '').strip()
            
            # Extract round data from columns
            columns = row.find_all('div', class_='results_column__pZWgz')
            
            # Skip the first column (player info) and last column (total)
            round_columns = columns[1:-1] if len(columns) > 2 else []
            
            for i, round_col in enumerate(round_columns[:5]):  # Only first 5 rounds
                round_num = i + 1
                
                # Extract score details
                score_details = round_col.find('div', class_='score-cell_scoreDetails__D_Ygp')
                if score_details:
                    spans = score_details.find_all('span')
                    if len(spans) >= 3:
                        # Format: distance, duration, steps
                        distance_text = spans[0].get_text(strip=True)
                        duration_text = spans[1].get_text(strip=True)
                        steps_text = spans[2].get_text(strip=True)
                        
                        player_data[f'round_{round_num}_duration'] = self.parse_duration(duration_text)
                        
                        # Extract steps number
                        steps_match = re.search(r'(\d+)', steps_text)
                        if steps_match:
                            player_data[f'round_{round_num}_steps'] = int(steps_match.group(1))
                
                # Extract points
                score_cell = round_col.find('div', class_='score-cell_score__oKM2x')
                if score_cell:
                    points_text = score_cell.get_text(strip=True)
                    # Extract number before "pts" - handle comma-separated numbers
                    points_match = re.search(r'([\d,]+)\s*pts', points_text)
                    if points_match:
                        # Remove commas and convert to int
                        points_str = points_match.group(1).replace(',', '')
                        player_data[f'round_{round_num}_points'] = int(points_str)
            
            # Extract totals from the last column
            if len(columns) > 1:
                total_column = columns[-1]
                total_div = total_column.find('div', class_='results_totalColumn__vlXbH')
                if total_div:
                    # Extract total points
                    total_score = total_div.find('div', class_='score-cell_score__oKM2x')
                    if total_score:
                        total_points_text = total_score.get_text(strip=True)
                        # Extract number before "pts" - handle comma-separated numbers
                        total_points_match = re.search(r'([\d,]+)\s*pts', total_points_text)
                        if total_points_match:
                            # Remove commas and convert to int
                            total_points_str = total_points_match.group(1).replace(',', '')
                            player_data['total_points'] = int(total_points_str)
                    
                    # Extract total details
                    total_details = total_div.find('div', class_='score-cell_scoreDetails__D_Ygp')
                    if total_details:
                        total_spans = total_details.find_all('span')
                        if len(total_spans) >= 3:
                            # Format: total distance, total duration, total steps
                            total_duration_text = total_spans[1].get_text(strip=True)
                            total_steps_text = total_spans[2].get_text(strip=True)
                            
                            player_data['total_duration'] = self.parse_duration(total_duration_text)
                            
                            # Extract total steps
                            total_steps_match = re.search(r'(\d+)', total_steps_text)
                            if total_steps_match:
                                player_data['total_steps'] = int(total_steps_match.group(1))
            
            results.append(player_data)
        
        return results
    
    def process_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Process a single mHTML file and extract all data"""
        print(f"Processing {file_path.name}...")
        
        # Extract HTML content
        html_content = self.extract_mhtml_content(file_path)
        if not html_content:
            return None
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract challenge info
        challenge_info = self.extract_challenge_info(html_content, file_path)
        
        # Extract game info
        game_info = self.extract_game_info(soup)
        
        # Extract results table
        player_results = self.extract_results_table(soup)
        
        # Combine all data
        file_data = {
            'challenge_info': challenge_info,
            'game_info': game_info,
            'player_results': player_results
        }
        
        return file_data
    
    def process_all_files(self) -> List[Dict[str, Any]]:
        """Process all mHTML files in the games folder"""
        if not self.games_folder.exists():
            print(f"Games folder '{self.games_folder}' does not exist!")
            return []
        
        mhtml_files = list(self.games_folder.glob('*.mhtml'))
        if not mhtml_files:
            print(f"No mHTML files found in '{self.games_folder}'")
            return []
        
        print(f"Found {len(mhtml_files)} mHTML files to process")
        
        all_data = []
        for file_path in mhtml_files:
            file_data = self.process_file(file_path)
            if file_data:
                all_data.append(file_data)
        
        return all_data
    
    def export_to_csv(self, data: List[Dict[str, Any]], output_file: str = "geoguessr_results.csv"):
        """Export extracted data to CSV format"""
        if not data:
            print("No data to export")
            return
        
        # Flatten the data for CSV export
        flattened_data = []
        
        for file_data in data:
            challenge_info = file_data['challenge_info']
            game_info = file_data['game_info']
            
            for player_result in file_data['player_results']:
                row = {
                    **challenge_info,
                    **game_info,
                    **player_result
                }
                flattened_data.append(row)
        
        # Define CSV columns
        columns = [
            'file_name', 'challenge_id', 'challenge_date', 'challenge_title',
            'map_name', 'map_creator', 'game_settings', 'time_limit', 'movement', 'panning', 'zooming',
            'position', 'player_name',
            'round_1_points', 'round_1_duration', 'round_1_steps',
            'round_2_points', 'round_2_duration', 'round_2_steps',
            'round_3_points', 'round_3_duration', 'round_3_steps',
            'round_4_points', 'round_4_duration', 'round_4_steps',
            'round_5_points', 'round_5_duration', 'round_5_steps',
            'total_points', 'total_duration', 'total_steps'
        ]
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(flattened_data)
        
        print(f"Data exported to {output_file}")
        print(f"Total records: {len(flattened_data)}")
    
    def run(self, output_file: str = "geoguessr_results.csv"):
        """Main method to run the extraction process"""
        print("Starting GeoGuessr data extraction...")
        
        # Process all files
        data = self.process_all_files()
        
        if data:
            # Export to CSV
            self.export_to_csv(data, output_file)
            
            # Print summary
            total_players = sum(len(file_data['player_results']) for file_data in data)
            print(f"\nSummary:")
            print(f"- Processed {len(data)} games")
            print(f"- Total player records: {total_players}")
        else:
            print("No data extracted")


def main():
    parser = argparse.ArgumentParser(description='Extract GeoGuessr data from mHTML files')
    parser.add_argument('--games-folder', default='games', help='Folder containing mHTML files')
    parser.add_argument('--output', default='geoguessr_results.csv', help='Output CSV file')
    
    args = parser.parse_args()
    
    extractor = GeoGuessrExtractor(args.games_folder)
    extractor.run(args.output)


if __name__ == "__main__":
    main()

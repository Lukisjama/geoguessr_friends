#!/usr/bin/env python3
"""
Simple HTTP server to serve the GeoGuessr dashboard locally
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def start_server(port=8000):
    """Start a local HTTP server to serve the dashboard"""
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if required files exist
    if not Path('dashboard.html').exists():
        print("❌ dashboard.html not found!")
        return
    
    if not Path('geoguessr_results.csv').exists():
        print("❌ geoguessr_results.csv not found!")
        print("Please run the extractor first: python3 geoguessr_extractor.py")
        return
    
    # Start server
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 GeoGuessr Dashboard Server")
        print(f"📊 Dashboard: http://localhost:{port}/dashboard.html")
        print(f"📁 Files: http://localhost:{port}/")
        print(f"⏹️  Press Ctrl+C to stop")
        print()
        
        # Open browser automatically
        try:
            webbrowser.open(f'http://localhost:{port}/dashboard.html')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped!")

if __name__ == "__main__":
    start_server()

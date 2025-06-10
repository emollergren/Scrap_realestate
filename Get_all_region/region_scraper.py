import requests
import time
import string
import json
from typing import Dict, List
from datetime import datetime

def get_regions(query: str) -> List[Dict]:
    url = f"https://suggest.realestate.com.au/consumer-suggest/suggestions"
    
    headers = {
        "referer": "https://www.realestate.com.au/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    
    params = {
        "max": "1000",
        "type": "suburb,region,precinct",
        "src": "customer-profile-home-mfe",
        "query": query
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        regions = []
        for suggestion in data.get("_embedded", {}).get("suggestions", []):
            if suggestion.get("type") == "region":
                regions.append({
                    "name": suggestion["source"]["name"],
                    "state": suggestion["source"].get("state", ""),
                    "id": suggestion["id"]
                })
        return regions
    except Exception as e:
        print(f"Error fetching data for query '{query}': {str(e)}")
        return []

def save_to_json(regions: List[Dict], filename: str):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(regions, f, indent=4, ensure_ascii=False)
        print(f"\nRegions data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON file: {str(e)}")

def main():
    # Get all uppercase letters A-Z
    letters = string.ascii_uppercase
    
    print("Starting to fetch regions...")
    all_regions = []  # Using list to store all region data
    
    for letter in letters:
        print(f"\nSearching for regions starting with '{letter}'...")
        regions = get_regions(letter)
        
        for region in regions:
            region_key = f"{region['name']}, {region['state']}"
            # Check if this region is already in our list
            if not any(r['name'] == region['name'] and r['state'] == region['state'] for r in all_regions):
                all_regions.append(region)
                print(f"Found new region: {region_key}")
        
        # Wait for 3 seconds before next request
        time.sleep(3)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"regions_{timestamp}.json"
    
    # Save to JSON file
    save_to_json(all_regions, filename)
    
    print("\nAll unique regions found:")
    for region in sorted(all_regions, key=lambda x: (x['name'], x['state'])):
        print(f"{region['name']}, {region['state']}")

if __name__ == "__main__":
    main()

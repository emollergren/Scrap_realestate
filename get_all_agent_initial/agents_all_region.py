import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List
from datetime import datetime
import re
import random
import csv
import os

def get_headers() -> Dict[str, str]:
    """Get headers for requests"""
    return {
        "authority": "www.realestate.com.au",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "reauid=13d8231797a83d00f9aa426811020000499f0300; Country=DE; KP_REF=; KP_IM=CiQ2OTFkMDZlZS03NmVmLTQ1OTMtODA3ZS1hZDUxNDA4OThlMzk; KP2_UIDz-ssn=0ax7hAtbAjYtUbkxbORK9syBUl9xWjAWM2231gI0FJ83ycvnRtq3M8X5ODhc5QyO3NiPHkFbSjYZJnFjhILkz93P5K99OsxumiBh9EwysmiVPlfZaLyHAuF7BNKBUlWIZi4tC9ZSIaujvOKdZeyCuL3dlyVRvOkKhpHyYpjVNCD; KP2_UIDz=0ax7hAtbAjYtUbkxbORK9syBUl9xWjAWM2231gI0FJ83ycvnRtq3M8X5ODhc5QyO3NiPHkFbSjYZJnFjhILkz93P5K99OsxumiBh9EwysmiVPlfZaLyHAuF7BNKBUlWIZi4tC9ZSIaujvOKdZeyCuL3dlyVRvOkKhpHyYpjVNCD; split_audience=c; pageview_counter.srs=1; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; s_nr30=1749199627245-New; utag_main=v_id:0197446c1b05001f5d18b6363c110506f005906700bd0$_sn:1$_se:2$_ss:0$_st:1749201426218$ses_id:1749199624965%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:realestate.com.au$_prevpage:undefined%3Bexp-1749203227254; s_ecid=MCMID%7C09166122703591472113487511986850489146; s_cc=true; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20246%7CMCMID%7C09166122703591472113487511986850489146%7CMCAAMLH-1749804427%7C3%7CMCAAMB-1749804427%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749206828s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; _gcl_au=1.1.2006358852.1749199631; DM_SitId1464=1; DM_SitId1464SecId12708=1; _ga_3J0XCBB972=GS2.1.s1749199633$o1$g0$t1749199633$j60$l0$h0; _ga=GA1.1.1872887338.1749199633; nol_fpid=qv0ucwa6b6d2fn6tdlsexmxizxdgv1749199633|1749199633568|1749199633568|1749199633568",
        "if-none-match": 'W/"8dac2-e1r4R+KW0Pw3OXfosAZTdDUhLno"',
        "priority": "u=0, i",
        "referer": "https://www.realestate.com.au/find-agent/armidale---greater-region-nsw?source=results",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

def extract_price(price_text: str) -> float:
    """Extract numeric price value from text like '$705k'"""
    if not price_text:
        return 0
    # Remove $ and convert k/m to actual numbers
    price_text = price_text.replace('$', '').strip()
    multiplier = 1
    if 'k' in price_text.lower():
        multiplier = 1000
        price_text = price_text.lower().replace('k', '')
    elif 'm' in price_text.lower():
        multiplier = 1000000
        price_text = price_text.lower().replace('m', '')
    try:
        return float(price_text) * multiplier
    except:
        return 0

def safe_get_text(element, default=''):
    """Safely get text from a BeautifulSoup element"""
    try:
        return element.text.strip() if element else default
    except:
        return default

def safe_get_int(text, default=0):
    """Safely convert text to integer"""
    try:
        if not text:
            return default
        # Extract first number found in text
        match = re.search(r'\d+', text)
        return int(match.group()) if match else default
    except:
        return default

def safe_get_float(text, default=0.0):
    """Safely convert text to float"""
    try:
        if not text:
            return default
        return float(text.strip())
    except:
        return default

def extract_agent_data(agent_card) -> Dict:
    """Extract data from a single agent card"""
    try:
        # Get the profile section
        profile_section = agent_card.find('div', class_='agent-card__profile')
        if not profile_section:
            print("Skipping agent card - missing profile section")
            return {}

        # Get agent URL and name
        agent_link = profile_section.find('a', href=lambda x: x and '/agent/' in x)
        agent_url = agent_link['href'] if agent_link else ''
        
        # Get agent profile details
        agent_details = profile_section.find('div', class_='agent-profile__agent-details')
        if not agent_details:
            print("Skipping agent card - missing agent details")
            return {}

        # Get agent name
        agent_name = safe_get_text(agent_details.find('div', class_='agent-profile__name'))

        # Get agency name
        agency_name = safe_get_text(agent_details.find('div', class_='agent-profile__agency'))

        # Get role
        role = safe_get_text(agent_details.find('div', class_='agent-profile__role'))

        # Get rating and reviews
        ratings_container = agent_details.find('div', class_='RatingsReviewsAggregate__RatingsReviewsAggregateContainer-sc-6n7u1i-0')
        rating = 0.0
        review_count = 0
        recent_reviews = 0
        review_timeframe = ''

        if ratings_container:
            # Get rating
            rating_elem = ratings_container.find('p', class_='RatingsReviewsAggregate__AggregatedReview-sc-6n7u1i-3')
            rating = safe_get_float(safe_get_text(rating_elem))

            # Get total reviews
            review_count_elem = ratings_container.find('p', class_='RatingsReviewsAggregate__TotalReviews-sc-6n7u1i-4')
            review_count = safe_get_int(safe_get_text(review_count_elem))

            # Get recent reviews
            timeframe_elem = ratings_container.find('p', class_='RatingsReviewsAggregate__RatingsReviewsTimeframe-sc-6n7u1i-5')
            if timeframe_elem:
                recent_reviews = safe_get_int(safe_get_text(timeframe_elem))
                review_timeframe = safe_get_text(timeframe_elem)

        # Get stats section
        stats_section = agent_card.find('div', class_='agent-card__stats--always-inline')
        properties_sold = 0
        median_price = 0
        days_advertised = 0
        all_suburbs_sold = 0

        if stats_section:
            # Get properties sold
            properties_elem = stats_section.find('div', class_='key-feature__value')
            properties_sold = safe_get_int(safe_get_text(properties_elem))

            # Get median price
            price_elem = stats_section.find('div', class_='agent_card__money')
            median_price = extract_price(safe_get_text(price_elem))

            # Get days advertised
            days_elem = stats_section.find('div', class_='key-feature__value', string=lambda x: x and x.strip().isdigit())
            days_advertised = safe_get_int(safe_get_text(days_elem))

            # Get all suburbs sold
            all_suburbs_elem = stats_section.find('div', class_='AgentCardStats__AllSuburbsStatsWrapper-ocqj95-3')
            if all_suburbs_elem:
                all_suburbs_sold = safe_get_int(safe_get_text(all_suburbs_elem.find('div', class_='key-feature__value')))

        # Get review text
        review_section = agent_card.find('div', class_='agent-card__review')
        review_text = ''
        if review_section:
            review_text_elem = review_section.find('p', class_='iGRVPQ')
            review_text = safe_get_text(review_text_elem)

        # Only return data if we have at least the agent name
        if not agent_name:
            print("Skipping agent card - missing agent name")
            return {}

        return {
            "agent_name": agent_name,
            "agent_url": agent_url,
            "agency_name": agency_name,
            "role": role,
            "rating": rating,
            "review_count": review_count,
            "recent_reviews": recent_reviews,
            "review_timeframe": review_timeframe,
            "properties_sold": properties_sold,
            "median_price": median_price,
            "days_advertised": days_advertised,
            "all_suburbs_sold": all_suburbs_sold,
            "review_text": review_text
        }
    except Exception as e:
        print(f"Error extracting agent data: {str(e)}")
        return {}

def get_total_agent_count(soup) -> int:
    """Get total number of agents from the results count"""
    try:
        # Look for the paragraph with the results count
        results_div = soup.find('p', class_='Text__Typography-zot5yv-0 hseMxs')
        if results_div:
            results_text = results_div.find('strong').text
            # Extract number from text like "1661 results"
            count = int(results_text.split()[0])
            return count
    except Exception as e:
        print(f"Error getting total agent count: {str(e)}")
    return 0

def get_agents_from_page(url: str, page: int, max_retries: int = 3) -> List[Dict]:
    """Get all agents from a specific page with retry mechanism"""
    headers = get_headers()
    # print('headers',headers)
    for attempt in range(max_retries):
        try:
            # Add small delay before each request
            delay = random.uniform(1, 2)
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get total agent count on first page
            
            
            agent_cards = soup.find_all('div', class_='agent-card')
            agents = []
            
            for i, card in enumerate(agent_cards, 1):
                print(f"\nProcessing agent {i} of {len(agent_cards)} on page {page}...")
                agent_data = extract_agent_data(card)
                if agent_data:
                    agents.append(agent_data)
                    print(f"Found agent: {agent_data['agent_name']} from {agent_data['agency_name']}")
            
            
            # if page == 1:
            total_agents = get_total_agent_count(soup)
            print(f"Total agents in region: {total_agents}")

            return agents

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                wait_time = (attempt + 1) * 30  # Exponential backoff: 30s, 60s, 90s
                print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"HTTP Error: {str(e)}")
                return []
        except Exception as e:
            print(f"Error fetching page {page}: {str(e)}")
            return []

    print(f"Failed to fetch page {page} after {max_retries} attempts")
    return []

def create_region_url(region_name: str, state: str) -> str:
    """Create URL for a region"""
    # Convert region name to URL format
    region_url = region_name.lower().replace(' - ', '---').replace(' ', '-')
    return f"https://www.realestate.com.au/find-agent/{region_url}-{state.lower()}"

def save_to_csv(agents_data: List[Dict], filename: str):
    """Save agents data to CSV file"""
    try:
        # Define CSV headers
        headers = [
            'agent_name', 'agent_url', 'agency_name', 'role', 'rating', 
            'review_count', 'recent_reviews', 'review_timeframe', 
            'properties_sold', 'median_price', 'days_advertised', 
            'all_suburbs_sold', 'review_text', 'region_name', 'region_state', 
            'region_id'
        ]
        
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(agents_data)
        print(f"\nData saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV file: {str(e)}")

def main():
    # Load regions from JSON file
    try:
        with open('regions.json', 'r', encoding='utf-8') as f:
            regions = json.load(f)
    except Exception as e:
        print(f"Error loading regions.json: {str(e)}")
        return

    # Initialize output files
    json_output = "Agents.json"
    csv_output = "Agents.csv"
    
    # Initialize data structures
    regions_data = {}  # For JSON: region-centric structure
    all_agents = []    # For CSV: flat agent list
    
    # Load existing data if file exists
    try:
        with open(json_output, 'r', encoding='utf-8') as f:
            regions_data = {region['id']: region for region in json.load(f)}
            # Convert existing data to flat list for CSV
            for region in regions_data.values():
                all_agents.extend(region['agents'])
            print(f"Loaded existing data from {json_output}")
    except FileNotFoundError:
        print(f"Starting new files: {json_output} and {csv_output}")
        # Initialize regions_data with empty agents list for each region
        for region in regions:
            region_id = region['id']
            regions_data[region_id] = {
                "name": region['name'],
                "state": region['state'],
                "id": region_id,
                "agents": []
            }
    except Exception as e:
        print(f"Error loading existing file: {str(e)}")
        # Initialize regions_data with empty agents list for each region
        for region in regions:
            region_id = region['id']
            regions_data[region_id] = {
                "name": region['name'],
                "state": region['state'],
                "id": region_id,
                "agents": []
            }

    # Process each region
    for region in regions:
        region_name = region['name']
        state = region['state']
        region_id = region['id']
        
        print(f"\nProcessing region: {region_name}, {state}")
        
        # Get first page to check total agent count
        base_url = create_region_url(region_name, state)
        first_page_url = f"{base_url}?source=results&page=1"
        response = requests.get(first_page_url, headers=get_headers())
        total_agents_from_page = get_total_agent_count(BeautifulSoup(response.text, 'html.parser'))
        
        # Get existing agent count from JSON
        existing_agents = regions_data[region_id]['agents']
        existing_agent_count = len(existing_agents)
        
        print(f"Agent count comparison for {region_name}:")
        print(f"- From page: {total_agents_from_page}")
        print(f"- From JSON: {existing_agent_count}")
        
        # If JSON count is higher than webpage count, remove region immediately
        # But keep region if both counts are 0
        if existing_agent_count >= total_agents_from_page and not (existing_agent_count == 0 and total_agents_from_page == 0):
            print(f"Removing region: {region_name} - JSON has {existing_agent_count} agents (webpage shows {total_agents_from_page})")
            # Remove region from regions.json
            try:
                # Read current regions
                with open('regions.json', 'r', encoding='utf-8') as f:
                    current_regions = json.load(f)
                
                # Filter out the current region
                updated_regions = [r for r in current_regions if r['id'] != region_id]
                
                # Save updated regions
                with open('regions.json', 'w', encoding='utf-8') as f:
                    json.dump(updated_regions, f, indent=4, ensure_ascii=False)
                
                print(f"Successfully removed {region_name} from regions.json")
            except Exception as e:
                print(f"Error removing region from regions.json: {str(e)}")
            continue
        elif existing_agent_count == 0 and total_agents_from_page == 0:
            print(f"Keeping region {region_name} - both JSON and webpage show 0 agents")
            continue
        
        page = 1
        # If webpage count is higher, clear existing agents and start fresh
        if existing_agent_count < total_agents_from_page:
            print(f"Agent count mismatch detected for {region_name}")
            print(f"Clearing existing {existing_agent_count} agents and starting fresh...")
            
            page=(existing_agent_count // 24)+1 if existing_agent_count > 0 else 1
            print('stopped page',page)
            print('stopped url',f"{base_url}?source=results&page={page}")
        
        while True:
            url = f"{base_url}?source=results&page={page}"
            print(f"\nFetching page {page} for {region_name}...")
            
            agents = get_agents_from_page(url, page)
            if not agents:
                break
                
            # Add agents to both data structures
            regions_data[region_id]['agents'].extend(agents)  # For JSON
            
            # Add region information to agents for CSV
            for agent in agents:
                agent_with_region = agent.copy()
                agent_with_region['region_name'] = region_name
                agent_with_region['region_state'] = state
                agent_with_region['region_id'] = region_id
                all_agents.append(agent_with_region)
            
            # Save data after every page
            try:
                # Save to JSON (region-centric structure)
                with open(json_output, 'w', encoding='utf-8') as f:
                    json.dump(list(regions_data.values()), f, indent=4, ensure_ascii=False)
                
                # Save to CSV (flat agent list)
                save_to_csv(all_agents, csv_output)
                
                print(f"\nSaved data to both {json_output} and {csv_output}")
                print(f"- JSON: {len(regions_data)} regions with their agents")
                print(f"- CSV: {len(all_agents)} total agents")
            except Exception as e:
                print(f"Error saving data: {str(e)}")
            
            page += 1
        
        # After completing all pages for a region, remove it from regions.json
        print(f"\nRegion {region_name} completed. Removing from regions.json...")
        try:
            # Read current regions
            with open('regions.json', 'r', encoding='utf-8') as f:
                current_regions = json.load(f)
            
            # Filter out the completed region
            updated_regions = [r for r in current_regions if r['id'] != region_id]
            
            # Save updated regions
            with open('regions.json', 'w', encoding='utf-8') as f:
                json.dump(updated_regions, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully removed {region_name} from regions.json")
        except Exception as e:
            print(f"Error removing region from regions.json: {str(e)}")
        
        # Take a longer break between regions
        delay = random.uniform(2, 3)
        print(f"\nCompleted region {region_name}. Taking a {delay:.1f} second break before next region...")
        time.sleep(delay)
    
    # Final save
    try:
        # Save to JSON (region-centric structure)
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump(list(regions_data.values()), f, indent=4, ensure_ascii=False)
        
        # Save to CSV (flat agent list)
        save_to_csv(all_agents, csv_output)
        
        print(f"\nFinal save completed:")
        print(f"- JSON: {len(regions_data)} regions with their agents")
        print(f"- CSV: {len(all_agents)} total agents")
    except Exception as e:
        print(f"Error saving final data: {str(e)}")

if __name__ == "__main__":
    main()
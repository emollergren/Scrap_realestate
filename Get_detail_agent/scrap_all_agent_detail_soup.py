import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import Dict
import re
import csv
import os

def safe_get_text(element, default=''):
    """Safely get text from a BeautifulSoup element"""
    try:
        return element.text.strip() if element else default
    except:
        return default

def get_headers() -> Dict:
    """Get headers for requests"""
    return {
        "authority": "www.realestate.com.au",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "Country=DE; ew_bkt=58; reauid=13d8231797a83d00568942688b00000009960300; split_audience=b; tracking_acknowledged=true; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; s_ecid=MCMID%7C79240456128296676171079287210162664689; DM_SitId1464=1; DM_SitId1464SecId12708=1; _gcl_au=1.1.60341695.1749191015; _ga=GA1.1.1568164722.1749191017; s_cc=true; appraisal_form_progress=landing; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20250%7CMCMID%7C79240456128296676171079287210162664689%7CMCAAMLH-1750144349%7C3%7CMCAAMB-1750144349%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749546749s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; KP2_UIDz-ssn=0buHQ5E2A5MEYZ20L4h9zMGClRA0kgBncH1R15zhLjHztaKxMoV1jBS7jlRup9JYK9eJZP8eq6hEvI3atZJQenwRsCK3VJk5S3r7ta4wXzu7doytgOFaw53h7pWa1tfVzxf9j5gjD0428TK5IIy8oNrysxrCQRBNG1gKC9re5CD; KP2_UIDz=0buHQ5E2A5MEYZ20L4h9zMGClRA0kgBncH1R15zhLjHztaKxMoV1jBS7jlRup9JYK9eJZP8eq6hEvI3atZJQenwRsCK3VJk5S3r7ta4wXzu7doytgOFaw53h7pWa1tfVzxf9j5gjD0428TK5IIy8oNrysxrCQRBNG1gKC9re5CD; pageview_counter.srs=3; QSI_SI_b7yBB0eituPt5vE_intercept=true; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fagency%2Farmidale-rentals-armidale-BUHLFK~1749539677844%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagency%2Flj-hooker-west-lakes-henley-beach-XLJSEB~1749540467957; KFC=JE0Bry/u0itQrPf0gEsmCDiE356gvVwtn4wJ/sHzv6w=|1749545535366; KP_UIDz-ssn=0cLuHcUjiHePYgm2Mm0djiysMO75OfhM9X3663T2cMRz5E1wMuuDhhZCo391GPiSTXWenunGTQkVABXeh37JnFccF26DbC9mOQUXyYQLdkctKRgnbG0HkmjconbvktkgfYWgWnFFQsHtVJaCVSbZrT2pW0IpbOuv5Vx8szlpcZF; KP_UIDz=0cLuHcUjiHePYgm2Mm0djiysMO75OfhM9X3663T2cMRz5E1wMuuDhhZCo391GPiSTXWenunGTQkVABXeh37JnFccF26DbC9mOQUXyYQLdkctKRgnbG0HkmjconbvktkgfYWgWnFFQsHtVJaCVSbZrT2pW0IpbOuv5Vx8szlpcZF; s_nr30=1749545561022-Repeat; legs_sq=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; nol_fpid=khnrmk00z7sndlycfx4gnv3r6rdbh1749191016|1749191016604|1749545563905|1749545564795; utag_main=v_id:019743e8a594000e709218b4ea550506f011d06700bd0$_sn:9$_se:1$_ss:1$_st:1749547358798$vapi_domain:realestate.com.au$ses_id:1749545558798%3Bexp-session$_pn:1%3Bexp-session$_prevpage:rea%3Afind%20agent%3Aprofiles%3Aagent%20profile%3Bexp-1749549161021$adform_uid:5032883578545086495%3Bexp-session; _ga_3J0XCBB972=GS2.1.s1749545543$o9$g1$t1749545567$j36$l0$h0",
        "priority": "u=0, i",
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

def safe_get_nested(data, *keys, default=None):
    """Safely get nested dictionary values"""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is None:
            return default
    return current

def extract_json_from_script(html_content: str, agent_url: str = '', regions: list = None) -> Dict:
    """Extract JSON data from the script tag containing ArgonautExchange"""
    try:
        # First try to find any script tags that might contain our data
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script')
        
        # Look for the ArgonautExchange data
        pattern = r'window\.ArgonautExchange\s*=\s*({.*?});'
        match = None
        
        for script in script_tags:
            if script.string and 'ArgonautExchange' in script.string:
                match = re.search(pattern, script.string, re.DOTALL)
                if match:
                    break
        
        if not match:
            print("Could not find ArgonautExchange data in any script tags")
            # Try alternative pattern
            pattern2 = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
            match = re.search(pattern2, html_content, re.DOTALL)
            if not match:
                print("Could not find alternative data pattern either")
                return {}
            print("Found alternative data pattern")
        
        # Parse the outer JSON
        try:
            outer_json = json.loads(match.group(1))
            print("Successfully parsed outer JSON")
        except json.JSONDecodeError as e:
            print(f"Error parsing outer JSON: {str(e)}")
            return {}
        
        # Try different possible paths to find agent data
        agent_data = None
        
        # Try first path
        if 'resi-agent_customer-profile-experience' in outer_json:
            agent_profile_str_1 = outer_json.get('resi-agent_customer-profile-experience', {}).get('AGENT_PROFILE')
            if agent_profile_str_1:
                try:
                    agent_profile1 = json.loads(agent_profile_str_1)
                    agent_data = agent_profile1.get('agent')
                    print("Found agent data in first path")
                except json.JSONDecodeError as e:
                    print(f"Error parsing AGENT_PROFILE JSON: {str(e)}")
        
        # Try second path if first failed
        if not agent_data and 'agent' in outer_json:
            agent_data = outer_json.get('agent')
            print("Found agent data in second path")
        
        # Try third path if others failed
        if not agent_data and 'agentProfile' in outer_json:
            agent_data = outer_json.get('agentProfile')
            print("Found agent data in third path")
        
        if not agent_data:
            print("Could not find agent data in any expected location")
            return {}
        
        # Get listings data
        agent_profile2 = {}
        if 'resi-agent_customer-profile-experience' in outer_json:
            agent_profile_str_2 = outer_json.get('resi-agent_customer-profile-experience', {}).get('AGENT_PROFILE_LISTINGS')
            if agent_profile_str_2:
                try:
                    agent_profile2 = json.loads(agent_profile_str_2)
                    print("Found listings data")
                except json.JSONDecodeError as e:
                    print(f"Error parsing AGENT_PROFILE_LISTINGS JSON: {str(e)}")
        
        # Split name into first and last name
        full_name = safe_get_nested(agent_data, 'name', default='')
        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # Construct the return data using safe_get_nested
        return {
            'agent_profile': {
                'profile_id': safe_get_nested(agent_data, 'profileId', default=''),
                'first_name': first_name,
                'last_name': last_name,
                'friendly_name': safe_get_nested(agent_data, 'friendlyName', default=''),
                'description': safe_get_nested(agent_data, 'description', default=''),
                'job_title': safe_get_nested(agent_data, 'jobTitle', default=''),
                'years_experience': safe_get_nested(agent_data, 'yearsExperience', default=0),
                'start_year': safe_get_nested(agent_data, 'startYearInIndustry', default=0),
                'rating': safe_get_nested(agent_data, 'avgRating', default=0),
                'total_reviews': safe_get_nested(agent_data, 'totalReviews', default=0),
                'power_profile': safe_get_nested(agent_data, 'powerProfile', default=False),
                'business_phone': safe_get_nested(agent_data, 'businessPhone', default=''),
                'mobile': safe_get_nested(agent_data, 'mobile', default=''),
                'agent_url': agent_url,
                'regions': regions if regions else [],
                'location': {
                    'suburb': safe_get_nested(agent_data, 'mostActiveLocation', 'suburb', default=''),
                    'state': safe_get_nested(agent_data, 'mostActiveLocation', 'state', default=''),
                    'postcode': safe_get_nested(agent_data, 'mostActiveLocation', 'postcode', default='')
                },
                'linked_salespeople_ids': safe_get_nested(agent_data, 'linkedSalespeopleIds', default=[]),
                'compliments': [
                    {
                        'tag': safe_get_nested(comp, 'tag', default=''),
                        'count': safe_get_nested(comp, 'count', default=0)
                    }
                    for comp in safe_get_nested(agent_data, 'compliments', default=[])
                ],
                'profile_image': safe_get_nested(agent_data, 'profileImage', 'templatedUrl', default=''),
                'agency': {
                    'id': safe_get_nested(agent_data, 'agency', 'id', default=''),
                    'name': safe_get_nested(agent_data, 'agency', 'name', default=''),
                    'logo': safe_get_nested(agent_data, 'agency', 'logo', 'templatedUrl', default=''),
                    'branding': safe_get_nested(agent_data, 'agency', 'branding', 'primaryColor', default=''),
                    'profile_url': safe_get_nested(agent_data, 'agency', '_links', 'profile', 'href', default='')
                },
                'social': {
                    'facebook': safe_get_nested(agent_data, 'social', 'facebook', default=''),
                    'instagram': safe_get_nested(agent_data, 'social', 'instagram', default=''),
                    'twitter': safe_get_nested(agent_data, 'social', 'twitter', default=''),
                    'linkedin': safe_get_nested(agent_data, 'social', 'linkedin', default='')
                },
                'agent_stats': {
                    'median_days_on_site': {
                        'townhouse': safe_get_nested(agent_data, 'agentStats', 'medianDaysOnSite', 'townhouse', default=0),
                        'apartment': safe_get_nested(agent_data, 'agentStats', 'medianDaysOnSite', 'apartment', default=0),
                        'house': safe_get_nested(agent_data, 'agentStats', 'medianDaysOnSite', 'house', default=0),
                        'overall': safe_get_nested(agent_data, 'agentStats', 'medianDaysOnSite', 'overall', default=0)
                    },
                    'median_sold_price': {
                        'townhouse': safe_get_nested(agent_data, 'agentStats', 'medianSoldPrice', 'townhouse', default=0),
                        'apartment': safe_get_nested(agent_data, 'agentStats', 'medianSoldPrice', 'apartment', default=0),
                        'house': safe_get_nested(agent_data, 'agentStats', 'medianSoldPrice', 'house', default=0),
                        'overall': safe_get_nested(agent_data, 'agentStats', 'medianSoldPrice', 'overall', default=0)
                    },
                    'sales_count': {
                        'apartment': safe_get_nested(agent_data, 'agentStats', 'salesCount', 'apartment', default=0),
                        'townhouse': safe_get_nested(agent_data, 'agentStats', 'salesCount', 'townhouse', default=0),
                        'as_lead_agent': safe_get_nested(agent_data, 'agentStats', 'salesCount', 'asLeadAgent', default=0),
                        'as_secondary_agent': safe_get_nested(agent_data, 'agentStats', 'salesCount', 'asSecondaryAgent', default=0),
                        'house': safe_get_nested(agent_data, 'agentStats', 'salesCount', 'house', default=0),
                        'overall': safe_get_nested(agent_data, 'agentStats', 'salesCount', 'overall', default=0)
                    }
                },
                'agent_sold_count': {
                    'total_result_count': safe_get_nested(agent_profile2, 'agentMapSoldListings', 'totalResultsCount', default=0),
                    'result_count': safe_get_nested(agent_profile2, 'agentMapSoldListings', 'resultsCount', default=0)
                },
                'agent_buy_count': {
                    'total_result_count': safe_get_nested(agent_profile2, 'agentMapBuyListings', 'totalResultCount', default=0),
                    'result_count': safe_get_nested(agent_profile2, 'agentMapBuyListings', 'resultsCount', default=0)
                },
                'agent_rent_count': {
                    'total_result_count': safe_get_nested(agent_profile2, 'agentMapRentListings', 'totalResultCount', default=0),
                    'result_count': safe_get_nested(agent_profile2, 'agentMapRentListings', 'resultsCount', default=0)
                }
            },
            'agent_profile_listing': {
                'agent_Sold': {
                    'listings': safe_get_nested(agent_profile2, 'agentMapSoldListings', 'listings', default=[])
                },
                'agent_Buy': {
                    'listings': safe_get_nested(agent_profile2, 'agentMapBuyListings', 'listings', default=[])
                },
                'agent_Rent': {
                    'listings': safe_get_nested(agent_profile2, 'agentMapRentListings', 'listings', default=[])
                }
            }
        }
    except Exception as e:
        print(f"Error extracting JSON from script: {str(e)}")
        print("HTML content preview (first 500 chars):")
        print(html_content[:500])
        return {}

# def normalize_agent_data(raw_data: Dict) -> Dict:
#     """Normalize the agent data into a consistent format"""
#     # print(agent_profile1.get('agentStats', {}))
    

def scrape_agent_profile(url: str, regions: list = None, max_retries: int = 3) -> Dict:
    """Scrape detailed information from an agent's profile page"""
    headers = get_headers()
    session = requests.Session()
    
    for attempt in range(max_retries):
        try:
            # Add delay before each request
            delay = random.uniform(1, 2)
            print(f"\nAttempt {attempt + 1}/{max_retries}:")
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            print(f"Making request to: {url}")
            response = session.get(url, headers=headers)
            response.encoding = "utf-8"
            print(f"Response status code: {response.status_code}")
            
            response.raise_for_status()
            
            # Extract JSON data from script tag
            normalized_data = extract_json_from_script(response.text, url, regions)
            return normalized_data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                wait_time = (attempt + 1) * 30  # Exponential backoff
                print(f"\nRate limited. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"\nHTTP Error: {str(e)}")
                return {}
        except Exception as e:
            print(f"\nError scraping agent profile: {str(e)}")
            return {}

    print(f"\nFailed to fetch agent profile after {max_retries} attempts")
    return {}

def flatten_dict(d, parent_key='', sep='_'):
    """Flatten nested dictionary for CSV export"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def replace_size_in_url(url: str, size_type: str) -> str:
    """Replace {size} placeholder in URL with appropriate size value"""
    if not url or not isinstance(url, str):
        return url
        
    size_mapping = {
        'profile_image': '192x192-gravity=north,quality=90',
        'agency_logo': '340x64',
        'listing_image': '500x300'
    }
    
    return url.replace('{size}', size_mapping.get(size_type, ''))

def process_media_urls(obj, size_type='listing_image'):
    """Recursively process all media URLs in an object"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'media':
                if isinstance(value, dict):
                    if 'mainImage' in value:
                        value['mainImage'] = replace_size_in_url(value['mainImage'], size_type)
                    if 'images' in value and isinstance(value['images'], list):
                        value['images'] = [replace_size_in_url(img, size_type) for img in value['images']]
            elif key == 'profile_image':
                obj[key] = replace_size_in_url(value, 'profile_image')
            elif key == 'logo' and isinstance(value, str):
                obj[key] = replace_size_in_url(value, 'agency_logo')
            else:
                process_media_urls(value, size_type)
    elif isinstance(obj, list):
        for item in obj:
            process_media_urls(item, size_type)
    return obj

def process_urls(data: Dict) -> Dict:
    """Process URLs in the data to replace size placeholders"""
    if not data:
        return data
    
    # Process the entire data structure recursively
    return process_media_urls(data)

def main():
    # Create Detailed_agent_data directory if it doesn't exist
    os.makedirs("Detailed_agent_data", exist_ok=True)
    
    # Read the agents data
    with open("all_agent_key=agent.json", "r", encoding="utf-8") as f:
        agents = json.load(f)
    
    # Initialize or load existing combined data
    try:
        with open('detailed_agent.json', 'r', encoding='utf-8') as f:
            all_profile_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_profile_data = []
    
    # Initialize or load existing failed data
    try:
        with open('failed.json', 'r', encoding='utf-8') as f:
            failed_agents = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        failed_agents = []
    
    # Process each agent
    total_agents = len(agents)
    remaining_agents = agents.copy()  # Create a copy to track remaining agents
    
    for index, agent in enumerate(agents, 1):
        print(f"\nProcessing agent {index}/{total_agents}: {agent['agent_name']}")
        
        # Scrape agent data with regions information
        agent_data = scrape_agent_profile(agent['agent_url'], agent.get('region', []))
        
        if not agent_data:
            print(f"Failed to scrape data for agent: {agent['agent_name']}")
            # Save failed agent info
            failed_agent_info = {
                'agent_name': agent['agent_name'],
                'agent_url': agent['agent_url'],
                'failure_point': 'initial_scrape',
                'description': 'Failed to extract data from the agent profile page'
            }
            failed_agents.append(failed_agent_info)
            # Save failed agents to file
            try:
                with open('failed.json', 'w', encoding='utf-8') as f:
                    json.dump(failed_agents, f, indent=4, ensure_ascii=False)
                print("Updated failed.json with failed agent info")
            except Exception as e:
                print(f"Error saving failed agent info: {str(e)}")
            continue
        
        # Process URLs to replace size placeholders
        agent_data = process_urls(agent_data)
        
        # Get profile data for file naming
        profile_data = agent_data.get('agent_profile', {})
        first_name = profile_data.get('first_name', '').lower()
        last_name = profile_data.get('last_name', '').lower()
        profile_id = profile_data.get('profile_id', '')
        
        # Create filename
        filename_base = f"{first_name}_{last_name}_{profile_id}"
        
        # Save individual agent data to JSON
        try:
            with open(f'Detailed_agent_data/{filename_base}.json', 'w', encoding='utf-8') as f:
                json.dump(agent_data, f, indent=4, ensure_ascii=False)
            print(f"Saved individual data to Detailed_agent_data/{filename_base}.json")
        except Exception as e:
            print(f"Error saving individual JSON file: {str(e)}")
            # Save failed agent info
            failed_agent_info = {
                'agent_name': f"{first_name} {last_name}",
                'profile_id': profile_id,
                'agent_url': agent['agent_url'],
                'failure_point': 'individual_json_save',
                'description': f'Failed to save individual JSON file: {str(e)}'
            }
            failed_agents.append(failed_agent_info)
            # Save failed agents to file
            try:
                with open('failed.json', 'w', encoding='utf-8') as f:
                    json.dump(failed_agents, f, indent=4, ensure_ascii=False)
                print("Updated failed.json with failed agent info")
            except Exception as e:
                print(f"Error saving failed agent info: {str(e)}")
            continue
        
        # Add profile data to the combined list and save immediately
        all_profile_data.append(profile_data)
        
        # Save combined profile data to JSON after each agent
        try:
            with open('detailed_agent.json', 'w', encoding='utf-8') as f:
                json.dump(all_profile_data, f, indent=4, ensure_ascii=False)
            print("Updated detailed_agent.json")
        except Exception as e:
            print(f"Error updating detailed_agent.json: {str(e)}")
            # Save failed agent info
            failed_agent_info = {
                'agent_name': f"{first_name} {last_name}",
                'profile_id': profile_id,
                'agent_url': agent['agent_url'],
                'failure_point': 'combined_json_save',
                'description': f'Failed to update combined JSON file: {str(e)}'
            }
            failed_agents.append(failed_agent_info)
            # Save failed agents to file
            try:
                with open('failed.json', 'w', encoding='utf-8') as f:
                    json.dump(failed_agents, f, indent=4, ensure_ascii=False)
                print("Updated failed.json with failed agent info")
            except Exception as e:
                print(f"Error saving failed agent info: {str(e)}")
            continue
        
        # Save combined profile data to CSV after each agent
        try:
            if all_profile_data:
                # Get all possible fields from the first profile
                fieldnames = list(flatten_dict(all_profile_data[0]).keys())
                
                with open('detailed_agent.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    # Write each profile's flattened data
                    for profile in all_profile_data:
                        flattened_data = flatten_dict(profile)
                        writer.writerow(flattened_data)
                print("Updated detailed_agent.csv")
        except Exception as e:
            print(f"Error updating detailed_agent.csv: {str(e)}")
            # Save failed agent info
            failed_agent_info = {
                'agent_name': f"{first_name} {last_name}",
                'profile_id': profile_id,
                'agent_url': agent['agent_url'],
                'failure_point': 'csv_save',
                'description': f'Failed to update CSV file: {str(e)}'
            }
            failed_agents.append(failed_agent_info)
            # Save failed agents to file
            try:
                with open('failed.json', 'w', encoding='utf-8') as f:
                    json.dump(failed_agents, f, indent=4, ensure_ascii=False)
                print("Updated failed.json with failed agent info")
            except Exception as e:
                print(f"Error saving failed agent info: {str(e)}")
            continue
        
        # Remove successfully scraped agent from remaining_agents
        remaining_agents = [a for a in remaining_agents if a['agent_url'] != agent['agent_url']]
        
        # Update all_agent_key=agent.json with remaining agents
        try:
            with open("all_agent_key=agent.json", "w", encoding="utf-8") as f:
                json.dump(remaining_agents, f, indent=4, ensure_ascii=False)
            print(f"Updated all_agent_key=agent.json. {len(remaining_agents)} agents remaining.")
        except Exception as e:
            print(f"Error updating all_agent_key=agent.json: {str(e)}")
        
        # Add a delay between requests
        # delay = random.uniform(2, 4)
        # print(f"Waiting {delay:.1f} seconds before next request...")
        # time.sleep(delay)

if __name__ == "__main__":
    main()

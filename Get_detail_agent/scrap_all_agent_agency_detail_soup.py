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
        "cookie": "Country=DE; ew_bkt=5; reauid=24142017854d000000504a688e000000aae30800; split_audience=a; s_fid=03606DEF184F55B9-39A54E77F143A926; s_cc=true; s_vi=[CS]v1|3425280401C56C5B-600019656EB15C63[CE]; _gcl_au=1.1.520317802.1749700682; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; _ga=GA1.1.1821553078.1749700683; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCAID%7C3425280401C56C5B-600019656EB15C63%7CMCIDTS%7C20252%7CMCMID%7C37329218910349853851968231497426871509%7CMCAAMLH-1750353592%7C3%7CMCAAMB-1750353592%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749755992s%7CNONE%7CMCSYNCSOP%7C411-20259%7CvVersion%7C5.5.0; DM_SitId1464=1; DM_SitId1464SecId12708=1; tracking_acknowledged=true; KFC=/RXo8zDvdHCNWEGfG1UWYiRuuijQ0XCO6NPstNlbal8=|1749748857679; KP_UIDz-ssn=0anDhwD0haZhNjHKjdDNkgFCq0apXC9RiW7GxjmnUhaCUkyk7PoGHNEUXRlySvzHEyohSVzJEYParlQeFgs3AeWpoU9eFzJ4jPrcku7ErBGBzffRp123RJsjxTySmeMpA8yyXWU7luELDoxKUceo5nY0XlGvHcZMBZ4qKv5m63q; KP_UIDz=0anDhwD0haZhNjHKjdDNkgFCq0apXC9RiW7GxjmnUhaCUkyk7PoGHNEUXRlySvzHEyohSVzJEYParlQeFgs3AeWpoU9eFzJ4jPrcku7ErBGBzffRp123RJsjxTySmeMpA8yyXWU7luELDoxKUceo5nY0XlGvHcZMBZ4qKv5m63q; s_nr30=1749748866688-Repeat; nol_fpid=jicdurpe9w11lpcq4jaxhv2qtxnvf1749748801|1749748801026|1749748868296|1749748869838; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fagent%2Frosemary-auricchio-55151%3FcampaignType%3Dinternal%26campaignChannel%3Din_product%26campaignSource%3Drea%26campaignName%3Dsell_enq%26campaignPlacement%3Dagent_search_result_card%26campaignKeyword%3Dagency_marketplace%26sourcePage%3Dagent_srp%26sourceElement%3Dagent_search_result_card~1749748794748%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagency%2Flj-hooker-west-lakes-henley-beach-XLJSEB~1749748892835; _ga_3J0XCBB972=GS2.1.s1749748804$o2$g1$t1749749703$j60$l0$h0; legs_sq=%5B%5BB%5D%5D; utag_main=v_id:01976249462400759973502eca280506f012006700bd0$_sn:3$_se:8$_ss:0$_st:1749751512068$vapi_domain:realestate.com.au$ses_id:1749748790755%3Bexp-session$_pn:4%3Bexp-session$_prevpage:rea%3Afind%20agent%3Aagency%20page%3Bexp-1749753312077; s_sq=%5B%5BB%5D%5D",
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
        # print(soup)
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

def extract_agency_profile(html_content: str) -> Dict:
    """Extract agency profile data from the script tag containing ArgonautExchange"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script')
        
        pattern = r'window\.ArgonautExchange\s*=\s*({.*?});'
        match = None
        
        for script in script_tags:
            if script.string and 'ArgonautExchange' in script.string:
                match = re.search(pattern, script.string, re.DOTALL)
                if match:
                    break
        
        if not match:
            print("Could not find ArgonautExchange data in any script tags")
            return {}
        
        try:
            outer_json = json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print(f"Error parsing outer JSON: {str(e)}")
            return {}
        
        # Extract agency profile data
        if 'resi-agent_customer-profile-experience' in outer_json:
            agency_profile_str = outer_json.get('resi-agent_customer-profile-experience', {}).get('AGENCY_PROFILE')
            if agency_profile_str:
                try:
                    agency_profile = json.loads(agency_profile_str)
                    return agency_profile.get('agencyProfile', {})
                except json.JSONDecodeError as e:
                    print(f"Error parsing AGENCY_PROFILE JSON: {str(e)}")
                    return {}
        
        return {}
    except Exception as e:
        print(f"Error extracting agency profile: {str(e)}")
        return {}

def sanitize_filename(filename: str) -> str:
    """Convert string to a valid filename"""
    # Replace invalid characters with underscore
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename

def scrape_agent_profile(url: str, regions: list = None, max_retries: int = 3) -> Dict:
    """Scrape detailed information from an agent's profile page"""
    headers = get_headers()
    session = requests.Session()
    
    for attempt in range(max_retries):
        try:
            # Add delay before each request
            delay = random.uniform(30,60)
            print(f"\nAttempt {attempt + 1}/{max_retries}:")
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            print(f"Making request to: {url}")
            response = session.get(url, headers=headers)
            # response.encoding = "utf-8"
            print(f"Response status code: {response.status_code}")
            # print(response.text)
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

def scrape_agency_profile(url: str, max_retries: int = 3) -> Dict:
    """Scrape detailed information from an agency's profile page"""
    headers = get_headers()
    session = requests.Session()
    
    for attempt in range(max_retries):
        try:
            # Add delay before each request
            delay = random.uniform(30,60)
            print(f"\nAttempt {attempt + 1}/{max_retries} for agency:")
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            print(f"Making request to agency URL: {url}")
            response = session.get(url, headers=headers)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()
            
            # Extract JSON data from script tag
            soup = BeautifulSoup(response.text, 'html.parser')
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
                print("Could not find ArgonautExchange data in agency page")
                # Try alternative pattern
                pattern2 = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
                match = re.search(pattern2, response.text, re.DOTALL)
                if not match:
                    print("Could not find alternative data pattern either")
                    return {}
                print("Found alternative data pattern")
            
            try:
                outer_json = json.loads(match.group(1))
                print("Successfully parsed agency JSON")
            except json.JSONDecodeError as e:
                print(f"Error parsing agency JSON: {str(e)}")
                return {}
            
            # Try different possible paths to find agency data
            agency_data = None
            
            # Try first path - resi-agent_customer-profile-experience
            if 'resi-agent_customer-profile-experience' in outer_json:
                agency_profile_str = outer_json.get('resi-agent_customer-profile-experience', {}).get('AGENCY_PROFILE')
                if agency_profile_str:
                    try:
                        agency_profile = json.loads(agency_profile_str)
                        agency_data = agency_profile.get('agencyProfile')
                        print("Found agency data in first path")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing AGENCY_PROFILE JSON: {str(e)}")
            
            # Try second path - resi-agency_customer-profile-experience
            if not agency_data and 'resi-agency_customer-profile-experience' in outer_json:
                agency_profile_str = outer_json.get('resi-agency_customer-profile-experience', {}).get('AGENCY_PROFILE')
                if agency_profile_str:
                    try:
                        agency_profile = json.loads(agency_profile_str)
                        agency_data = agency_profile.get('agencyProfile')
                        print("Found agency data in second path")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing AGENCY_PROFILE JSON: {str(e)}")
            
            # Try third path - agency directly
            if not agency_data and 'agency' in outer_json:
                agency_data = outer_json.get('agency')
                print("Found agency data in third path")
            
            # Try fourth path - agencyProfile directly
            if not agency_data and 'agencyProfile' in outer_json:
                agency_data = outer_json.get('agencyProfile')
                print("Found agency data in fourth path")
            
            # Try fifth path - agencyProfile in resi-agency_customer-profile-experience
            if not agency_data and 'resi-agency_customer-profile-experience' in outer_json:
                agency_data = outer_json.get('resi-agency_customer-profile-experience', {}).get('agencyProfile')
                if agency_data:
                    print("Found agency data in fifth path")
            
            if not agency_data:
                print("Could not find agency data in any expected location")
                # Print the available keys in outer_json for debugging
                print("Available keys in outer_json:", list(outer_json.keys()))
                return {}
            
            return agency_data

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
            print(f"\nError scraping agency profile: {str(e)}")
            return {}

    print(f"\nFailed to fetch agency profile after {max_retries} attempts")
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

def clean_agency_data(agency_data: Dict) -> Dict:
    """Remove unwanted fields from agency data"""
    if not agency_data:
        return {}
    
    # Create a copy of the data to avoid modifying the original
    cleaned_data = agency_data.copy()
    
    # Remove reviews if present
    if 'reviews' in cleaned_data:
        del cleaned_data['reviews']
    
    # Remove residentialChannels/listings if present
    if 'residentialChannels' in cleaned_data:
        if isinstance(cleaned_data['residentialChannels'], dict):
            # If residentialChannels is a dictionary, remove listings if present
            if 'listings' in cleaned_data['residentialChannels']:
                del cleaned_data['residentialChannels']['listings']
        elif isinstance(cleaned_data['residentialChannels'], list):
            # If residentialChannels is a list, remove listings from each channel
            for channel in cleaned_data['residentialChannels']:
                if isinstance(channel, dict) and 'listings' in channel:
                    del channel['listings']
    
    # Handle any string values that might be JSON
    for key, value in cleaned_data.items():
        if isinstance(value, str):
            try:
                # Try to parse the string as JSON
                parsed_value = json.loads(value)
                if isinstance(parsed_value, dict):
                    # If it's a dictionary, clean it recursively
                    cleaned_data[key] = clean_agency_data(parsed_value)
            except json.JSONDecodeError:
                # If it's not valid JSON, keep the original string
                pass
    
    return cleaned_data

def update_agent_agency_data(agent_data: Dict, agency_data: Dict) -> Dict:
    """Update agent's agency object with data from agency profile"""
    if not agent_data or not agency_data:
        return agent_data
    
    # Get the agency object from agent data
    agent_profile = agent_data.get('agent_profile', {})
    agency = agent_profile.get('agency', {})
    
    # Update agency data with new fields
    agency.update({
        'agencyUrl': agency_data.get('agencyUrl', ''),
        'businessPhone': agency_data.get('businessPhone', ''),
        'address': agency_data.get('address', {})
    })
    
    # Update the agency object in agent data
    agent_profile['agency'] = agency
    agent_data['agent_profile'] = agent_profile
    
    return agent_data

def extract_agency_fields(agency_data: Dict) -> Dict:
    """Extract specific fields from agency data"""
    return {
        'agencyId': agency_data.get('agencyId', ''),
        'name': agency_data.get('name', ''),
        'description': agency_data.get('description', ''),
        'agencyUrl': agency_data.get('agencyUrl', ''),
        'businessPhone': agency_data.get('businessPhone', ''),
        'address': agency_data.get('address', {})
    }

def main():
    # Create Detailed_agent_data directory if it doesn't exist
    os.makedirs("Detailed_agent_data", exist_ok=True)
    
    # Create Detailed_agency_data directory if it doesn't exist
    os.makedirs("Detailed_agency_data", exist_ok=True)
    
    # Read the agents data
    with open("all_agent_key=agent.json", "r", encoding="utf-8") as f:
        agents = json.load(f)
    
    # Initialize or load existing combined data
    try:
        with open('detailed_agent.json', 'r', encoding='utf-8') as f:
            all_profile_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_profile_data = []
    
    # Initialize or load existing agency data
    try:
        with open('detailed_agency.json', 'r', encoding='utf-8') as f:
            all_agency_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_agency_data = []
    
    # Create a dictionary for faster agency lookup
    agency_dict = {agency['agencyId']: agency for agency in all_agency_data}
    
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
        
        # Extract and save agency profile data
        try:
            agency_data = profile_data.get('agency', {})
            agency_id = agency_data.get('id', '')
            
            if agency_id:
                # Check if we already have this agency's data
                if agency_id in agency_dict:
                    print(f"\nUsing existing agency data for agency ID: {agency_id}")
                    existing_agency_data = agency_dict[agency_id]
                    
                    # Update agent data with existing agency information
                    agent_data = update_agent_agency_data(agent_data, existing_agency_data)
                else:
                    # If we don't have the agency data, scrape it
                    agency_url = agency_data.get('profile_url', '')
                    if agency_url:
                        print(f"\nScraping agency data from: {agency_url}")
                        agency_profile = scrape_agency_profile(agency_url)
                        
                        if agency_profile:
                            # Clean the agency data before saving
                            cleaned_agency_profile = clean_agency_data(agency_profile)
                            
                            # Update agent data with agency information
                            agent_data = update_agent_agency_data(agent_data, cleaned_agency_profile)
                            
                            # Extract specific agency fields
                            agency_fields = extract_agency_fields(cleaned_agency_profile)
                            
                            # Add to combined agency data
                            all_agency_data.append(agency_fields)
                            agency_dict[agency_id] = agency_fields
                            
                            # Save combined agency data to JSON
                            try:
                                with open('detailed_agency.json', 'w', encoding='utf-8') as f:
                                    json.dump(all_agency_data, f, indent=4, ensure_ascii=False)
                                print("Updated detailed_agency.json")
                            except Exception as e:
                                print(f"Error updating detailed_agency.json: {str(e)}")
                            
                            # Save combined agency data to CSV
                            try:
                                if all_agency_data:
                                    fieldnames = ['agencyId', 'name', 'description', 'agencyUrl', 'businessPhone', 'address']
                                    with open('detailed_agency.csv', 'w', newline='', encoding='utf-8') as f:
                                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                                        writer.writeheader()
                                        for agency in all_agency_data:
                                            writer.writerow(agency)
                                    print("Updated detailed_agency.csv")
                            except Exception as e:
                                print(f"Error updating detailed_agency.csv: {str(e)}")
                            
                            agency_name = cleaned_agency_profile.get('name', '')
                            
                            # Create sanitized filename for agency
                            agency_filename = sanitize_filename(f"{agency_name}_{agency_id}")
                            
                            # Save agency profile data
                            with open(f'Detailed_agency_data/{agency_filename}.json', 'w', encoding='utf-8') as f:
                                json.dump(cleaned_agency_profile, f, indent=4, ensure_ascii=False)
                            print(f"Saved agency data to Detailed_agency_data/{agency_filename}.json")
                        else:
                            print("Failed to extract agency profile data")
                    else:
                        print("No agency URL found in agent data")
            else:
                print("No agency ID found in agent data")
        except Exception as e:
            print(f"Error processing agency data: {str(e)}")
        
        # Save individual agent data to JSON
        try:
            with open(f'Detailed_agent_data/{filename_base}.json', 'w', encoding='utf-8') as f:
                json.dump(agent_data, f, indent=4, ensure_ascii=False)
            print(f"Saved individual data to Detailed_agent_data/{filename_base}.json")
        except Exception as e:
            print(f"Error saving individual JSON file: {str(e)}")
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

if __name__ == "__main__":
    main()

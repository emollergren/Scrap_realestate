import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import Dict, List, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def format_cookie_string(cookies: List[Dict]) -> str:
    """Format cookies into a single string like in browser requests."""
    # Define the order of cookies as they appear in the browser
    cookie_order = [
        'reauid',
        'Country',
        'split_audience',
        '_gcl_au',
        '_ga',
        'DM_SitId1464',
        'DM_SitId1464SecId12708',
        'tracking_acknowledged',
        'AMCVS_341225BE55BBF7E17F000101%40AdobeOrg',
        '_lr_geo_location_state',
        '_lr_geo_location',
        's_ecid',
        'legs_sq',
        's_cc',
        's_sq',
        'QSI_HistorySession',
        'ew_bkt',
        'KFC',
        'KP_UIDz-ssn',
        'KP_UIDz',
        'AMCV_341225BE55BBF7E17F000101%40AdobeOrg',  # Second occurrence
        'KP2_UIDz-ssn',
        'KP2_UIDz',
        'pageview_counter.srs',
        'utag_main',
        's_nr30',
        '_ga_3J0XCBB972',
        'nol_fpid'
    ]
    
    # Create a dictionary of cookies for easy lookup
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    
    # Add default values for required cookies
    default_cookies = {
        'split_audience': 'a',
        'pageview_counter.srs': '7',  # Updated to match browser
        '_gcl_au': '1.1.1545764079.1749100670',
        '_ga': 'GA1.1.1454637171.1749100670',
        'DM_SitId1464': '1',
        'DM_SitId1464SecId12708': '1',
        'tracking_acknowledged': 'true',
        'AMCVS_341225BE55BBF7E17F000101%40AdobeOrg': '1',
        '_lr_geo_location_state': 'HE',
        '_lr_geo_location': 'DE',
        's_ecid': 'MCMID%7C75503528588372506932777235831909784981',
        'legs_sq': '%5B%5BB%5D%5D',
        's_cc': 'true',
        's_sq': '%5B%5BB%5D%5D',
        'QSI_HistorySession': 'https%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Farmidale---greater-region-nsw%3Fsource%3Dresults~1749100694415',
        'ew_bkt': '41',
        'KFC': 'yw0PtJ3yFxLa6LOMKzfm63lq8/J31RaCzYubfmpMj9g=|1749107262838',
        'AMCV_341225BE55BBF7E17F000101%40AdobeOrg': '179643557%7CMCIDTS%7C20245%7CMCMID%7C75503528588372506932777235831909784981%7CMCAAMLH-1749713754%7C3%7CMCAAMB-1749713754%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749116154s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0',
        's_nr30': '1749109652439-Repeat',
        '_ga_3J0XCBB972': 'GS2.1.s1749106467$o2$g1$t1749109655$j52$l0$h0',
        'nol_fpid': 'sym6721ezdodteozyigh55n0lcc8l1749100670|1749100670831|1749109655798|1749109656547',
        'utag_main': 'v_id:01973e86265f001225e04a3daaaa0506f00550670086e$_sn:2$_se:7$_ss:0$_st:1749111450839$vapi_domain:realestate.com.au$ses_id:1749105628343%3Bexp-session$_pn:7%3Bexp-session$_prevpage:rea%3Afind%20agent%3Aagent%3Asearch%20results%3Bexp-1749113252438$adform_uid:47924083152249268%3Bexp-session'
    }
    
    # Update cookie_dict with default values
    cookie_dict.update(default_cookies)
    
    # Format cookies in the specified order
    cookie_parts = []
    for name in cookie_order:
        if name in cookie_dict:
            cookie_parts.append(f"{name}={cookie_dict[name]}")
    
    return '; '.join(cookie_parts)

def get_headers(cookies: List[Dict] = None, etag: str = None) -> Dict[str, str]:
    headers = {
        "authority": "www.realestate.com.au",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    
    if etag:
        headers["if-none-match"] = etag
    
    if cookies:
        headers["cookie"] = format_cookie_string(cookies)
    
    return headers

def add_tracking_cookies(session: requests.Session) -> None:
    # Add essential tracking cookies with updated values
    tracking_cookies = {
        'Country': 'DE',
        'split_audience': 'a',
        'pageview_counter.srs': '7',  # Updated to match browser
        'tracking_acknowledged': 'true',
        's_cc': 'true',
        's_sq': '%5B%5BB%5D%5D',
        'legs_sq': '%5B%5BB%5D%5D',
        '_lr_geo_location_state': 'HE',
        '_lr_geo_location': 'DE',
        's_nr30': '1749109652439-Repeat',
        '_ga_3J0XCBB972': 'GS2.1.s1749106467$o2$g1$t1749109655$j52$l0$h0'
    }
    
    for name, value in tracking_cookies.items():
        session.cookies.set(name, value, domain='.realestate.com.au')

def get_total_agent_count(soup) -> int:
    try:
        results_div = soup.find('p', class_='Text__Typography-zot5yv-0 hseMxs')
        if results_div:
            results_text = results_div.find('strong').text
            count = int(results_text.split()[0].replace(",", ""))
            return count
    except Exception as e:
        print(f"Error getting total agent count: {str(e)}")
    return 0

def create_region_url(region_name: str, state: str) -> str:
    region_url = region_name.lower().replace(' - ', '---').replace(' ', '-')
    return f"https://www.realestate.com.au/find-agent/{region_url}-{state.lower()}"

def get_selenium_cookies(url: str) -> Tuple[requests.Session, List[Dict]]:
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Add more realistic browser behavior
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    options.add_argument('--disable-site-isolation-trials')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    
    # Add random user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')

    driver = webdriver.Chrome(options=options)
    try:
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        # First visit the main page to get initial cookies
        driver.get("https://www.realestate.com.au")
        time.sleep(random.uniform(2, 3))
        
        # Get cookies
        selenium_cookies = driver.get_cookies()
        
        session = requests.Session()
        
        # Set cookies in the session
        for cookie in selenium_cookies:
            cookie_dict = {
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie.get('domain', ''),
                'path': cookie.get('path', '/')
            }
            if cookie.get('secure'):
                cookie_dict['secure'] = True
            session.cookies.set(**cookie_dict)
        
        # Add tracking cookies
        add_tracking_cookies(session)
            
        return session, selenium_cookies
    finally:
        driver.quit()

def print_headers(headers: Dict[str, str]) -> None:
    """Print headers in a readable format."""
    print("\n=== Request Headers ===")
    for key, value in headers.items():
        print(f"{key}: {value}")
    print("=====================\n")

def get_webpage_agent_count(url: str, max_retries: int = 3) -> int:
    base_url = "https://www.realestate.com.au"
    session, selenium_cookies = get_selenium_cookies(f"{base_url}/find-agent/armidale---greater-region-nsw?source=results")
    
    # First get the ETag for the specific page we're requesting
    initial_headers = get_headers(selenium_cookies)
    initial_response = session.get(url, headers=initial_headers)
    etag = initial_response.headers.get('ETag')
    print(f"Got ETag for {url}: {etag}")
    
    # If we got a 200 response, we can use the content directly
    if initial_response.status_code == 200:
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        return get_total_agent_count(soup)
    
    # If we got a 304 (Not Modified), we need to retry with the ETag
    for attempt in range(max_retries):
        try:
            # Random delay between requests
            delay = random.uniform(15, 20)
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            # Get headers with cookies and ETag
            headers = get_headers(selenium_cookies, etag)
            headers['referer'] = url
            print_headers(headers)
            print(f"URL: {url}")
            
            # Then make the actual request
            response = session.get(url, headers=headers)
            print("Status code:", response.status_code)
            
            # Update ETag for next request if available
            new_etag = response.headers.get('ETag')
            if new_etag:
                etag = new_etag
                print(f"Updated ETag: {etag}")
            
            if response.status_code == 429:
                wait_time = (attempt + 1) * 30
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return get_total_agent_count(soup)

        except Exception as e:
            print(f"Error fetching webpage: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 90
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            continue

    print(f"Failed to fetch webpage after {max_retries} attempts")
    return 0

def check_region_counts(region: Dict) -> Tuple[bool, int, int]:
    region_name = region['name']
    state = region['state']
    region_id = region['id']

    print(f"\nChecking region: {region_name}, {state}")

    base_url = create_region_url(region_name, state)
    webpage_count = get_webpage_agent_count(f"{base_url}?source=results&page=1")

    try:
        with open('Agents.json', 'r', encoding='utf-8') as f:
            regions_data = {region['id']: region for region in json.load(f)}
            json_count = len(regions_data.get(region_id, {}).get('agents', []))
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        json_count = 0

    counts_match = webpage_count == json_count

    print(f"Count comparison for {region_name}:")
    print(f"- Webpage count: {webpage_count}")
    print(f"- JSON count: {json_count}")
    print(f"- Status: {'✓ Match' if counts_match else '✗ Mismatch'}")

    return counts_match, webpage_count, json_count

def main():
    try:
        with open('regions.json', 'r', encoding='utf-8') as f:
            regions = json.load(f)
    except Exception as e:
        print(f"Error loading regions.json: {str(e)}")
        return

    total_regions = len(regions)
    matching_regions = 0
    mismatching_regions = []

    print(f"\nStarting count check for {total_regions} regions...")

    for region in regions:
        counts_match, webpage_count, json_count = check_region_counts(region)

        if counts_match:
            matching_regions += 1
        else:
            mismatching_regions.append({
                'region_name': region['name'],
                'state': region['state'],
                'webpage_count': webpage_count,
                'json_count': json_count
            })

        delay = random.uniform(2, 3)
        print(f"Taking a {delay:.1f} second break...")
        time.sleep(delay)

    print("\n=== Summary ===")
    print(f"Total regions checked: {total_regions}")
    print(f"Regions with matching counts: {matching_regions}")
    print(f"Regions with mismatched counts: {len(mismatching_regions)}")

    if mismatching_regions:
        print("\nMismatched regions:")
        for region in mismatching_regions:
            print(f"- {region['region_name']}, {region['state']}:")
            print(f"  Webpage: {region['webpage_count']}")
            print(f"  JSON: {region['json_count']}")

if __name__ == "__main__":
    main()

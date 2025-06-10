import time
import random
import json
from typing import Dict, List
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_api.log'),
        logging.StreamHandler()
    ]
)

# ScraperAPI configuration
API_KEY = "dae051283049b81d61e45cdee20f90e7"
BASE_URL = "http://api.scraperapi.com"

def get_selenium_cookies(url: str) -> List[dict]:
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
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
    
    # Create undetected-chromedriver instance
    driver = uc.Chrome(options=options)
    try:
        # Visit pages in sequence
        # pages = [
        #     "https://www.realestate.com.au/",
        #     "https://www.realestate.com.au/find-agent/adelaide---greater-region-sa?pid=rea:hp:search-box-search:find-agent",
        #     "https://www.realestate.com.au/find-agent/adelaide---greater-region-sa?pid=rea:hp:search-box-search:find-agent&page=2&source=results",
        #     url  # Final agent page
        # ]
        
        # for page in pages:
        #     print(f"Visiting: {page}")
        #     driver.get(page)
        #     # Random delay between page visits
        #     print(driver.page_source)
        #     time.sleep(random.uniform(3, 5))
        driver.get(url)
        print(driver.page_source)
        # Get cookies after visiting all pages
        cookies = driver.get_cookies()
        return cookies
    finally:
        driver.quit()

def format_cookie_string(cookies: List[dict]) -> str:
    return '; '.join([f"{c['name']}={c['value']}" for c in cookies])

def get_headers(cookie_string: str, url: str) -> dict:
    return {
        "authority": "www.realestate.com.au",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": cookie_string,
        "priority": "u=0, i",
        "referer": url,
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

def safe_get_text(element, default=''):
    """Safely get text from a Selenium element"""
    try:
        return element.text.strip() if element else default
    except:
        return default

def print_headers(headers: Dict[str, str]) -> None:
    """Print headers in a readable format."""
    print("\n=== Request Headers ===")
    for key, value in headers.items():
        print(f"{key}: {value}")
    print("=====================\n")

def add_tracking_cookies(session: requests.Session) -> None:
    """Add essential tracking cookies with updated values"""
    tracking_cookies = {
        'reauid': '1e142017754d00006b6c4168f80000009e490400',
        'KP2_UIDz-ssn': '0bbxMTO5zs4UZqCVDLmuyyRLemis8I2dvgDT0vKrsqjHbhdrj5I53gF6uPkCYLpLK9XTFZepn0Df95DFCeFN4BlNJ2kV0Xd5C9cdF2SfD7zCwQZ0BLviYkd8yrh3manGuxrwR3IIOmmb3nEYuxh3BWl1WGA2OsPS6Ig2JIIW7Ay',
        'KP2_UIDz': '0bbxMTO5zs4UZqCVDLmuyyRLemis8I2dvgDT0vKrsqjHbhdrj5I53gF6uPkCYLpLK9XTFZepn0Df95DFCeFN4BlNJ2kV0Xd5C9cdF2SfD7zCwQZ0BLviYkd8yrh3manGuxrwR3IIOmmb3nEYuxh3BWl1WGA2OsPS6Ig2JIIW7Ay',
        'split_audience': 'd',
        'pageview_counter.srs': '1',
        'AMCVS_341225BE55BBF7E17F000101%40AdobeOrg': '1',
        's_ecid': 'MCMID%7C28492635512625225263999861222495772143',
        's_cc': 'true',
        'AMCV_341225BE55BBF7E17F000101%40AdobeOrg': '179643557%7CMCIDTS%7C20245%7CMCMID%7C28492635512625225263999861222495772143%7CMCAAMLH-1749722875%7C3%7CMCAAMB-1749722875%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749125276s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0',
        'ew_bkt': '98',
        '_sp_ses.2fe7': '*',
        'DM_SitId1464': '1',
        'DM_SitId1464SecId12708': '1',
        '_gcl_au': '1.1.253743351.1749118096',
        '_ga': 'GA1.1.2059187313.1749118099',
        'Country': 'DE',
        'KFC': 'e0N51FFKXccKbjjd2Q0dE5BCYOoMoipEsbVVo+InFEA=|1749118180132',
        'KP_UIDz-ssn': '0aJmhJYA4v9p1SeaTxl9k5BnJrutpo4XDlIsNl2np288zy2I6kkdGnHhubUlPlB4G5CpqJUbdoD2BNw2i9pY3gl2LtXtQhGMliB1Zyef0GyZ7aXiXPBF9aWJUjVrpfEIEvlQySfZVSddpX9hn3DLjTkFZZC5wnNbMr12EFCbO0A',
        'KP_UIDz': '0aJmhJYA4v9p1SeaTxl9k5BnJrutpo4XDlIsNl2np288zy2I6kkdGnHhubUlPlB4G5CpqJUbdoD2BNw2i9pY3gl2LtXtQhGMliB1Zyef0GyZ7aXiXPBF9aWJUjVrpfEIEvlQySfZVSddpX9hn3DLjTkFZZC5wnNbMr12EFCbO0A',
        's_nr30': '1749118186438-New',
        'tracking_acknowledged': 'true',
        'legs_sq': '%5B%5BB%5D%5D',
        'utag_main': 'v_id:01973f8fb69b003a6f8c624fe8780506f00550670086e$_sn:1$_se:6$_ss:0$_st:1749119988482$ses_id:1749118072475%3Bexp-session$_pn:4%3Bexp-session$vapi_domain:realestate.com.au$_prevpage:undefined%3Bexp-1749121788490$dc_visit:1$dc_event:2%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session',
        's_sq': '%5B%5BB%5D%5D',
        '_sp_id.2fe7': '2bab1841-4c3a-474b-aa04-0a957839a734.1749118092.1.1749118188.1749118092.1e97a9a2-f0cc-4235-a7e5-4f56130c0143',
        '_ga_3J0XCBB972': 'GS2.1.s1749118099$o1$g1$t1749118189$j54$l0$h0',
        'nol_fpid': 'nkdgsbigfja78wktp4724f4rlprjn1749118099|1749118099620|1749118189298|1749118190432',
        'QSI_HistorySession': 'https%3A%2F%2Fwww.realestate.com.au%2Fagent%2Flachie-sewell-2509278%3FcampaignType%3Dinternal%26campaignChannel%3Din_product%26campaignSource%3Drea%26campaignName%3Dsell_enq%26campaignPlacement%3Dagent_search_result_card%26campaignKeyword%3Dagency_marketplace%26sourcePage%3Dagent_srp%26sourceElement%3Dagent_search_result_card~1749118214028'
    }
    
    for name, value in tracking_cookies.items():
        session.cookies.set(name, value, domain='.realestate.com.au')

def scrape_agent_profile(url: str, max_retries: int = 3) -> Dict:
    # 1. Get cookies from Selenium after visiting all required pages
    cookies = get_selenium_cookies(url)
    cookie_string = format_cookie_string(cookies)
    headers = get_headers(cookie_string, url)
    print_headers(headers)
    
    session = requests.Session()
    # Add tracking cookies to the session
    # add_tracking_cookies(session)
    
    for attempt in range(max_retries):
        try:
            # Add longer delay between retries
            delay = random.uniform(5, 10) if attempt > 0 else random.uniform(2, 3)
            print(f"\nAttempt {attempt + 1}/{max_retries}:")
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)
            
            print(f"Making request to: {url}")
            response = session.get(url, headers=headers)
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 429:
                wait_time = (attempt + 1) * 30
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()
            
            with open('response.txt', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("\nSaved raw HTML to response.txt")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            div_first = soup.find('div', id='argonaut-wrapper')
            if not div_first:
                print("\nCould not find argonaut-wrapper")
                continue
            header_div = div_first.find('header', class_='styles__Header-sc-1ifcqm-0')
            if not header_div:
                print("\nCould not find header")
                continue
            profile_section = soup.find('div', class_='styles__Grid-sc-1ifcqm-1')
            if not profile_section:
                print("\nCould not find agent profile section")
                continue
            photo_elem = profile_section.find('img', class_='Avatar__StyledImage-sc-1vvicio-0')
            photo_url = photo_elem.get('src', '') if photo_elem else ''
            name_elem = profile_section.find('h1', class_='Text__Typography-sc-1103tao-0')
            full_name = safe_get_text(name_elem)
            name_parts = full_name.split()
            first_name = name_parts[0] if name_parts else ''
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            job_elem = profile_section.find('p', attrs={'data-testid': 'job-description'})
            job_text = safe_get_text(job_elem)
            job_title = ''
            company_name = ''
            company_url = ''
            if job_text:
                parts = job_text.split(' at ')
                if len(parts) == 2:
                    job_title = parts[0]
                    company_link = profile_section.find('a', class_='LinkBase-sc-1ba0r3r-0')
                    if company_link:
                        company_name = safe_get_text(company_link)
                        company_url = company_link.get('href', '')
            experience_elem = profile_section.find('span', class_='Text__Typography-sc-1103tao-0')
            experience = safe_get_text(experience_elem)
            rating_elem = profile_section.find('p', class_='Text__Typography-sc-1103tao-0')
            rating_text = safe_get_text(rating_elem)
            rating = rating_text.split()[0] if rating_text else ''
            reviews_elem = profile_section.find('a', class_='LinkBase-sc-1ba0r3r-0')
            reviews_count = safe_get_text(reviews_elem).strip('()') if reviews_elem else ''
            compliments = []
            badges = profile_section.find_all('div', class_='styles__Badge-sc-1jpq4vo-0')
            for badge in badges:
                compliment = safe_get_text(badge.find('p', class_='Text__Typography-sc-1103tao-0'))
                if compliment:
                    compliments.append(compliment)
            phone_elem = profile_section.find('a', href=lambda x: x and x.startswith('tel:'))
            phone = phone_elem.get('href', '').replace('tel:', '') if phone_elem else ''
            return {
                'photo_url': photo_url,
                'first_name': first_name,
                'last_name': last_name,
                'job_title': job_title,
                'company_name': company_name,
                'company_url': company_url,
                'experience': experience,
                'rating': rating,
                'reviews_count': reviews_count,
                'compliments': compliments,
                'phone': phone
            }
        except Exception as e:
            print(f"\nError scraping agent profile: {str(e)}")
            if attempt == max_retries - 1:
                raise
            continue
    print(f"\nFailed to fetch agent profile after {max_retries} attempts")
    return {}

def test_scraper_api() -> bool:
    """Test if ScraperAPI is working correctly"""
    test_url = "https://www.realestate.com.au"
    params = {
        'api_key': API_KEY,
        'url': test_url
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            logging.info("ScraperAPI test successful")
            return True
        else:
            logging.error(f"ScraperAPI test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"ScraperAPI test failed with error: {str(e)}")
        return False

def extract_agent_data(agent_card) -> Dict:
    """Extract data from a single agent card"""
    try:
        # Get the profile section
        profile_section = agent_card.find('div', class_='agent-card__profile')
        if not profile_section:
            logging.warning("Skipping agent card - missing profile section")
            return {}

        # Get agent URL and name
        agent_link = profile_section.find('a', href=lambda x: x and '/agent/' in x)
        agent_url = agent_link['href'] if agent_link else ''
        
        # Get agent profile details
        agent_details = profile_section.find('div', class_='agent-profile__agent-details')
        if not agent_details:
            logging.warning("Skipping agent card - missing agent details")
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
            logging.warning("Skipping agent card - missing agent name")
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
        logging.error(f"Error extracting agent data: {str(e)}")
        return {}

def get_agents_from_page(url: str, page: int, max_retries: int = 3) -> List[Dict]:
    """Get all agents from a specific page with retry mechanism"""
    headers = get_headers()
    
    for attempt in range(max_retries):
        try:
            # Add small delay before each request
            delay = random.uniform(2, 3)
            logging.info(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            # Prepare ScraperAPI request
            params = {
                'api_key': API_KEY,
                'url': url,
                'country_code': 'au'
            }
            
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            agent_cards = soup.find_all('div', class_='agent-card')
            agents = []
            
            for i, card in enumerate(agent_cards, 1):
                logging.info(f"Processing agent {i} of {len(agent_cards)} on page {page}...")
                agent_data = extract_agent_data(card)
                if agent_data:
                    agents.append(agent_data)
                    logging.info(f"Found agent: {agent_data['agent_name']} from {agent_data['agency_name']}")
            
            return agents

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                wait_time = (attempt + 1) * 30  # Exponential backoff
                logging.warning(f"Rate limited. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                logging.error(f"HTTP Error: {str(e)}")
                return []
        except Exception as e:
            logging.error(f"Error fetching page {page}: {str(e)}")
            return []

    logging.error(f"Failed to fetch page {page} after {max_retries} attempts")
    return []

def create_region_url(region_name: str, state: str) -> str:
    """Create URL for a region"""
    # Convert region name to URL format
    region_url = region_name.lower().replace(' - ', '---').replace(' ', '-')
    return f"https://www.realestate.com.au/find-agent/{region_url}-{state.lower()}"

def main():
    # Test ScraperAPI first
    if not test_scraper_api():
        logging.error("ScraperAPI test failed. Exiting...")
        return

    # Load regions from JSON file
    try:
        with open('regions.json', 'r', encoding='utf-8') as f:
            regions = json.load(f)
    except Exception as e:
        logging.error(f"Error loading regions.json: {str(e)}")
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
            logging.info(f"Loaded existing data from {json_output}")
    except FileNotFoundError:
        logging.info(f"Starting new files: {json_output} and {csv_output}")
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
        logging.error(f"Error loading existing file: {str(e)}")
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
        
        logging.info(f"\nProcessing region: {region_name}, {state}")
        
        # Get first page to check total agent count
        base_url = create_region_url(region_name, state)
        first_page_url = f"{base_url}?source=results&page=1"
        
        # Get existing agent count from JSON
        existing_agents = regions_data[region_id]['agents']
        existing_agent_count = len(existing_agents)
        
        logging.info(f"Agent count from JSON: {existing_agent_count}")
        
        page = 1
        # If webpage count is higher, clear existing agents and start fresh
        if existing_agent_count > 0:
            logging.info(f"Starting from page {(existing_agent_count // 24) + 1}")
            page = (existing_agent_count // 24) + 1
        
        while True:
            url = f"{base_url}?source=results&page={page}"
            logging.info(f"\nFetching page {page} for {region_name}...")
            
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
                import csv
                headers = [
                    'agent_name', 'agent_url', 'agency_name', 'role', 'rating', 
                    'review_count', 'recent_reviews', 'review_timeframe', 
                    'properties_sold', 'median_price', 'days_advertised', 
                    'all_suburbs_sold', 'review_text', 'region_name', 'region_state', 
                    'region_id'
                ]
                with open(csv_output, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(all_agents)
                
                logging.info(f"\nSaved data to both {json_output} and {csv_output}")
                logging.info(f"- JSON: {len(regions_data)} regions with their agents")
                logging.info(f"- CSV: {len(all_agents)} total agents")
            except Exception as e:
                logging.error(f"Error saving data: {str(e)}")
            
            page += 1
        
        # Take a longer break between regions
        delay = random.uniform(2, 3)
        logging.info(f"\nTaking a {delay:.1f} second break before next region...")
        time.sleep(delay)
    
    # Final save
    try:
        # Save to JSON (region-centric structure)
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump(list(regions_data.values()), f, indent=4, ensure_ascii=False)
        
        # Save to CSV (flat agent list)
        import csv
        headers = [
            'agent_name', 'agent_url', 'agency_name', 'role', 'rating', 
            'review_count', 'recent_reviews', 'review_timeframe', 
            'properties_sold', 'median_price', 'days_advertised', 
            'all_suburbs_sold', 'review_text', 'region_name', 'region_state', 
            'region_id'
        ]
        with open(csv_output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_agents)
        
        logging.info(f"\nFinal save completed:")
        logging.info(f"- JSON: {len(regions_data)} regions with their agents")
        logging.info(f"- CSV: {len(all_agents)} total agents")
    except Exception as e:
        logging.error(f"Error saving final data: {str(e)}")

if __name__ == "__main__":
    main()

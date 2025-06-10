import time
import random
import json
from typing import Dict, List
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests

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

def main():
    url = "https://www.realestate.com.au/agent/shaun-roberts-2066698?campaignType=internal&campaignChannel=in_product&campaignSource=rea&campaignName=sell_enq&campaignPlacement=agent_search_result_card&campaignKeyword=agency_marketplace&sourcePage=agent_srp&sourceElement=agent_search_result_card"
    print(f"\nStarting scrape for URL: {url}")
    try:
        agent_data = scrape_agent_profile(url)
        with open('agent_one.json', 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=4, ensure_ascii=False)
        print("\nData saved to agent_one.json")
    except Exception as e:
        print(f"\nError in main: {str(e)}")

if __name__ == "__main__":
    main()

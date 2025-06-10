# import requests
# from bs4 import BeautifulSoup
# import time
# import random
#
# # Base configuration
# BASE_URL = "https://www.realestate.com.au"
# START_URL = BASE_URL + "/find-agent/"
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.realestate.com.au/",
#     "Upgrade-Insecure-Requests": "1",
#     "Connection": "keep-alive",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Cookie":"Country=DE; ew_bkt=73; reauid=24142017fd6b310009553f680b00000053210000; split_audience=e; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; _lr_geo_location_state=HE; _lr_geo_location=DE; _gcl_au=1.1.569147979.1748981023; s_ecid=MCMID%7C28492635512625225263999861222495772143; s_cc=true; _ga=GA1.1.1989317176.1748981024; DM_SitId1464=1; DM_SitId1464SecId12708=1; s_fid=0CA9FF112CCBF649-0AAE0BBF451175E3; s_vi=[CS]v1|341FAAA0D8A60ECE-400007EF38779535[CE]; tracking_acknowledged=true; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20243%7CMCMID%7C28492635512625225263999861222495772143%7CMCAAMLH-1749618027%7C3%7CMCAAMB-1749618027%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749020427s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-20250%7CvVersion%7C5.5.0; KFC=NqGmkqys+y8TN5Rr3Boi09ldS0tdDXXgmVhUtsnz4Mg=|1749013309299; legs_sq=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; KP_UIDz-ssn=0aY5jww8sxGKEGMdpTK26dNVi60rYnTikiKRpOc0FF3L1HxHAVxTv9K2Bf7NNhHnhRtJUcaz8qmyFS9OcUUqbsFhLv23AdDD5KOaFxcbqW2WZ0czWTIFdBEEvKwlutFs49qSUOJqOp2AAu4j2SXYTuC6s3p0UMSVtuVZngDivuX; KP_UIDz=0aY5jww8sxGKEGMdpTK26dNVi60rYnTikiKRpOc0FF3L1HxHAVxTv9K2Bf7NNhHnhRtJUcaz8qmyFS9OcUUqbsFhLv23AdDD5KOaFxcbqW2WZ0czWTIFdBEEvKwlutFs49qSUOJqOp2AAu4j2SXYTuC6s3p0UMSVtuVZngDivuX; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Farmidale-nsw-2350%3Fsource%3Dresults~1749013972403%7Chttps%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Farmidale-nsw-2350~1749014117124; KP2_UIDz-ssn=0b1J62BsYJXJCTM53oUVpdJa5heW0BDL0LcP5pQc2KYxn3E3YJ4MYr5QIy5xc4KnZsKt63n658VSDdLAbOfb8ZZuyPaIA26EeHdKCncbXAmIibEHgkdFrC32cUXaay98gVAJCOJA021MKGZTxIYCdX9QiMGpjb3mCj6jApZE809; KP2_UIDz=0b1J62BsYJXJCTM53oUVpdJa5heW0BDL0LcP5pQc2KYxn3E3YJ4MYr5QIy5xc4KnZsKt63n658VSDdLAbOfb8ZZuyPaIA26EeHdKCncbXAmIibEHgkdFrC32cUXaay98gVAJCOJA021MKGZTxIYCdX9QiMGpjb3mCj6jApZE809; pageview_counter.srs=4; utag_main=v_id:01973764651900126e899986ffeb0506f00280670086e$_sn:2$_se:13$_ss:0$_st:1749015968340$vapi_domain:realestate.com.au$ses_id:1749012599094%3Bexp-session$_pn:8%3Bexp-session$_prevpage:rea%3Afind%20agent%3Aagent%3Asearch%20results%3Bexp-1749017769535; s_nr30=1749014169536-Repeat; nol_fpid=84rvsky3kvta172cb5kqvd6rnrynu1748981024|1748981024769|1749014169781|1749014171635; _ga_3J0XCBB972=GS2.1.s1749012866$o2$g1$t1749014176$j60$l0$h0",
# }
#
# def fetch_with_retries(url, headers, max_retries=5):
#     """Handle retries for 429 Too Many Requests"""
#     session = requests.Session()
#     session.headers.update(headers)
#
#     for attempt in range(max_retries):
#         try:
#             response = session.get(url, timeout=10)
#             if response.status_code == 200:
#                 return response.text
#             elif response.status_code == 429:
#                 wait = 2 ** attempt + random.uniform(1, 3)
#                 print(f"[429] Too many requests. Waiting {wait:.1f}s before retrying...")
#                 time.sleep(wait)
#             else:
#                 print(f"[{response.status_code}] Error while fetching URL.")
#                 break
#         except requests.RequestException as e:
#             print("Request failed:", e)
#             time.sleep(2)
#     return None
#
# def get_region_links():
#     html = fetch_with_retries(START_URL, HEADERS)
#     if not html:
#         print("❌ Failed to fetch the main page.")
#         return []
#
#     soup = BeautifulSoup(html, "html.parser")
#     region_links = set()
#
#     for a in soup.find_all("a", href=True):
#         href = a["href"]
#         if href.startswith("/find-agent/") and "?" not in href and len(href) > len("/find-agent/"):
#             full_url = BASE_URL + href
#             region_links.add(full_url)
#
#     return sorted(region_links)
#
# # Run scraper
# if __name__ == "__main__":
#     print("🔍 Scraping region links...")
#     regions = get_region_links()
#
#     if regions:
#         print(f"\n✅ Found {len(regions)} region URLs:\n")
#         for url in regions:
#             print(url)
#     else:
#         print("⚠️ No region URLs found.")

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        "cookie": "Country=DE; ew_bkt=77; reauid=14d82317668c00001aca3e680301000066ca0000; split_audience=c; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; tracking_acknowledged=true; s_ecid=MCMID%7C75503528588372506932777235831909784981; s_cc=true; _gcl_au=1.1.1838469835.1748945454; _lr_geo_location_state=HE; _lr_geo_location=DE; DM_SitId1464=1; DM_SitId1464SecId12708=1; _ga=GA1.1.1733780461.1748945456; legs_sq=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20243%7CMCMID%7C75503528588372506932777235831909784981%7CMCAAMLH-1749666347%7C3%7CMCAAMB-1749666347%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749068747s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; KP2_UIDz-ssn=0b8ZQwTau0J61zjEW9bCVhPuOYmhiVhHIGgKbfzoiP9O8wr0tx0CXf2nl81nx9p8ChAyN2z5ytc32OjDEQB7TbEbiK8vM3131N0jguXzMN81NBG4quSBFu7WdDMhlzjOkTc3skmkM5ZjNHt5AbgxJs5DT9rK5DKYfZswY0DmuR2; KP2_UIDz=0b8ZQwTau0J61zjEW9bCVhPuOYmhiVhHIGgKbfzoiP9O8wr0tx0CXf2nl81nx9p8ChAyN2z5ytc32OjDEQB7TbEbiK8vM3131N0jguXzMN81NBG4quSBFu7WdDMhlzjOkTc3skmkM5ZjNHt5AbgxJs5DT9rK5DKYfZswY0DmuR2; pageview_counter.srs=8; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Farmidale---greater-region-nsw%3Fsource%3Dresults~1749061585140%7Chttps%3A%2F%2Fwww.realestate.com.au%2Ffind-agent~1749066125447%7Chttps%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Fadelaide---greater-region-sa%3FcampaignType%3Dinternal%26campaignChannel%3Din_product%26campaignSource%3Drea%26campaignName%3Dsell_enq%26campaignPlacement%3Dagent_search%26campaignKeyword%3Dagency_marketplace~1749066222581; KFC=pY9CpvuPuDSgWwlP8TKqTEjmd1tksCh503pmZL2gZEM=|1749068199930; KP_UIDz-ssn=0bM7TlRK7zdttqQ4p7iooJryW04OlJSQzajp3rXnFCMb3yw8pUNCynANEbULS6Pt0XXzrX5S8QlnbJbhZvrvXr37qOcza73W9Gs34jT7LOLfS43al9HlmZdxsSgASD6XMXOtEC3N92w5NLi0NcUO0NXrjFF9aAx2wHJlCdYW9eh; KP_UIDz=0bM7TlRK7zdttqQ4p7iooJryW04OlJSQzajp3rXnFCMb3yw8pUNCynANEbULS6Pt0XXzrX5S8QlnbJbhZvrvXr37qOcza73W9Gs34jT7LOLfS43al9HlmZdxsSgASD6XMXOtEC3N92w5NLi0NcUO0NXrjFF9aAx2wHJlCdYW9eh; s_nr30=1749068205422-Repeat; nol_fpid=liaknbuqw5h7jhijtvbffqnojab2y1748945457|1748945457030|1749068206718|1749068206929; _ga_3J0XCBB972=GS2.1.s1749068208$o8$g0$t1749068208$j60$l0$h0; utag_main=v_id:019735459c480052d33b76f986280506f00280670086e$_sn:9$_se:1$_ss:1$_st:1749070005006$vapi_domain:realestate.com.au$_prevpage:rea%3Afind%20agent%3Aprofiles%3Aagent%20profile%3Bexp-1749071805421$ses_id:1749068205006%3Bexp-session$_pn:1%3Bexp-session$adform_uid:639084199842066553%3Bexp-session",
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

def scrape_agent_profile(url: str, max_retries: int = None) -> Dict:
    """Scrape detailed information from an agent's profile page"""
    # Get configuration from environment variables
    max_retries = max_retries or int(os.getenv('MAX_RETRIES', 3))
    min_delay = float(os.getenv('MIN_DELAY', 5))
    max_delay = float(os.getenv('MAX_DELAY', 8))
    rate_limit_wait = int(os.getenv('RATE_LIMIT_WAIT', 30))

    headers = get_headers()
    session = requests.Session()
    
    for attempt in range(max_retries):
        try:
            # Add longer delay before each request
            delay = random.uniform(min_delay, max_delay)
            print(f"\nAttempt {attempt + 1}/{max_retries}:")
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            print(f"Making request to: {url}")
            response = session.get(url, headers=headers)
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            # Ensure we're getting text content
            if 'text/html' not in response.headers.get('Content-Type', ''):
                print(f"Unexpected content type: {response.headers.get('Content-Type')}")
                return {}

            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Debug: Print the first 500 characters of the response
            print("\nFirst 500 characters of response:")
            print(response.text[:500])

            # Get agent profile section
            profile_section = soup.find('header', class_='styles__Header-sc-1ifcqm-0')
            if not profile_section:
                print("\nCould not find agent profile section")
                print("Available header elements:")
                headers = soup.find_all('header')
                for h in headers:
                    print(f"Header classes: {h.get('class', [])}")
                return {}

            print("\nFound profile section. Available classes:")
            print(f"Profile section classes: {profile_section.get('class', [])}")

            # Get photo URL
            photo_elem = profile_section.find('img', class_='Avatar__StyledImage-sc-1vvicio-0')
            photo_url = photo_elem.get('src', '') if photo_elem else ''
            print(f"\nPhoto URL found: {photo_url}")

            # Get full name and split into first and last name
            name_elem = profile_section.find('h1', class_='Text__Typography-sc-1103tao-0 bTLtfw')
            print(f"\nName element found: {name_elem}")
            full_name = safe_get_text(name_elem)
            print(f"Full name: {full_name}")
            name_parts = full_name.split()
            first_name = name_parts[0] if name_parts else ''
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

            # Get job title and company
            job_elem = profile_section.find('p', attrs={'data-testid': 'job-description'})
            job_text = safe_get_text(job_elem)
            print(f"\nJob text: {job_text}")
            
            # Extract job title and company
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

            # Get experience
            experience_elem = profile_section.find('span', class_='Text__Typography-sc-1103tao-0 kONa-DJ')
            experience = safe_get_text(experience_elem)
            print(f"\nExperience: {experience}")

            # Get rating and reviews
            rating_elem = profile_section.find('p', class_='Text__Typography-sc-1103tao-0 QpMDc')
            rating_text = safe_get_text(rating_elem)
            rating = rating_text.split()[0] if rating_text else ''
            print(f"\nRating: {rating}")
            
            reviews_elem = profile_section.find('a', class_='LinkBase-sc-1ba0r3r-0 styles__StyledLink-sc-1doobco-1')
            reviews_count = safe_get_text(reviews_elem).strip('()') if reviews_elem else ''
            print(f"Reviews count: {reviews_count}")

            # Get compliments/tags
            compliments = []
            badges = profile_section.find_all('div', class_='styles__Badge-sc-1jpq4vo-0')
            print(f"\nFound {len(badges)} badges")
            for badge in badges:
                compliment = safe_get_text(badge.find('p', class_='Text__Typography-sc-1103tao-0 cFjzOq'))
                if compliment:
                    compliments.append(compliment)
            print(f"Compliments: {compliments}")

            # Get phone number
            phone_elem = profile_section.find('a', href=lambda x: x and x.startswith('tel:'))
            phone = phone_elem.get('href', '').replace('tel:', '') if phone_elem else ''
            print(f"\nPhone: {phone}")

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

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                wait_time = (attempt + 1) * rate_limit_wait  # Exponential backoff
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

def main():
    # Example usage
    url = "https://www.realestate.com.au/agent/thanasi-mantopoulos-2265710"
    print(f"\nStarting scrape for URL: {url}")
    agent_data = scrape_agent_profile(url)
    
    # Save to JSON file
    try:
        with open('agent_one.json', 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=4, ensure_ascii=False)
        print("\nData saved to agent_one.json")
    except Exception as e:
        print(f"\nError saving to JSON file: {str(e)}")

if __name__ == "__main__":
    main()
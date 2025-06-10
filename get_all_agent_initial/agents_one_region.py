import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List
from datetime import datetime
import re
import random

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

def get_agents_from_page(url: str, page: int, max_retries: int = 3) -> List[Dict]:
    """Get all agents from a specific page with retry mechanism"""
    headers = {
        "authority": "www.realestate.com.au",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "Country=DE; ew_bkt=73; reauid=24142017fd6b310009553f680b00000053210000; split_audience=e; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; _lr_geo_location_state=HE; _lr_geo_location=DE; _gcl_au=1.1.569147979.1748981023; s_ecid=MCMID%7C28492635512625225263999861222495772143; s_cc=true; _ga=GA1.1.1989317176.1748981024; DM_SitId1464=1; DM_SitId1464SecId12708=1; s_fid=0CA9FF112CCBF649-0AAE0BBF451175E3; s_vi=[CS]v1|341FAAA0D8A60ECE-400007EF38779535[CE]; tracking_acknowledged=true; DM_SitId1464SecId12707=1; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Falbany---greater-region-wa%3Fsource%3Dresults%26page%3D2~1749023132021%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagent%2Fthanasi-mantopoulos-2265710%3FcampaignType%3Dinternal%26campaignChannel%3Din_product%26campaignSource%3Drea%26campaignName%3Dsell_enq%26campaignPlacement%3Dagent_search_result_card%26campaignKeyword%3Dagency_marketplace%26sourcePage%3Dagent_srp%26sourceElement%3Dagent_search_result_card~1749029919733; KFC=1BAA38Kb0ZOWxgiLH8Z/Nq5qQTT2aqrLHVe61Ux5EfU=|1749037790028; KP_UIDz-ssn=0crf46liZlZ3SXmKq4p7tnHxhJXhe04puN60XSop5MWcoQ3A6eRMfJLwXjkOUx0qNf6kgIiD3e9bApOm20AigjWaQJejOW2zpI2JIPckIKyo0OzcGqe9MmCudk5dkPlHHyWnTEvGikOOd385bqRhWu3YIFOQ8LzeAa000pXO5c4; KP_UIDz=0crf46liZlZ3SXmKq4p7tnHxhJXhe04puN60XSop5MWcoQ3A6eRMfJLwXjkOUx0qNf6kgIiD3e9bApOm20AigjWaQJejOW2zpI2JIPckIKyo0OzcGqe9MmCudk5dkPlHHyWnTEvGikOOd385bqRhWu3YIFOQ8LzeAa000pXO5c4; KP_REF=; KP_IM=CiQxZDBhMWVkYS0wMTEzLTQ5YjQtOTJlNC1jOTk4ZGI4NTA4NGI; KP2_UIDz-ssn=0chAIaIZ8p3t6ZfhgwFB5OoggUK80QcqIvPRBTHj3j7Npw0GYHBRlaefKdRjMvHwbTfOjIvWCvwygXXIAFGSPbJ4v76NKSOyhVQ1GUdxs0oF1XUpHi0nLwNCZQFLElX4O1PbTfLyGjVcgI39ybT75QZXXv8jHR40xqEeEt86apw; KP2_UIDz=0chAIaIZ8p3t6ZfhgwFB5OoggUK80QcqIvPRBTHj3j7Npw0GYHBRlaefKdRjMvHwbTfOjIvWCvwygXXIAFGSPbJ4v76NKSOyhVQ1GUdxs0oF1XUpHi0nLwNCZQFLElX4O1PbTfLyGjVcgI39ybT75QZXXv8jHR40xqEeEt86apw; pageview_counter.srs=29; utag_main=v_id:01973764651900126e899986ffeb0506f00280670086e$_sn:6$_se:1$_ss:1$_st:1749059256319$vapi_domain:realestate.com.au$ses_id:1749057456319%3Bexp-session$_pn:1%3Bexp-session$_prevpage:rea%3Afind%20agent%3Aagent%3Asearch%20results%3Bexp-1749061073662; s_nr30=1749057473663-Repeat; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20243%7CMCMID%7C28492635512625225263999861222495772143%7CMCAAMLH-1749662275%7C3%7CMCAAMB-1749662275%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749064675s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-20250%7CvVersion%7C5.5.0; legs_sq=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; _ga_3J0XCBB972=GS2.1.s1749057483$o6$g0$t1749057483$j60$l0$h0; nol_fpid=84rvsky3kvta172cb5kqvd6rnrynu1748981024|1748981024769|1749057483797|1749057487930",
        "if-none-match": 'W/"7be3c-rLqOdtflSfVNtTSPynRzmysN+9k"',
        "priority": "u=0, i",
        "referer": "https://www.realestate.com.au/find-agent/albany---greater-region-wa",
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

    for attempt in range(max_retries):
        try:
            # Add small delay before each request
            delay = random.uniform(2, 3)
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            agent_cards = soup.find_all('div', class_='agent-card')
            agents = []
            
            for i, card in enumerate(agent_cards, 1):
                print(f"\nProcessing agent {i} of {len(agent_cards)} on page {page}...")
                agent_data = extract_agent_data(card)
                if agent_data:
                    agents.append(agent_data)
                    print(f"Found agent: {agent_data['agent_name']} from {agent_data['agency_name']}")
            
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

def save_to_json(data: List[Dict], filename: str):
    """Save data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nData saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON file: {str(e)}")

def main():
    base_url = "https://www.realestate.com.au/find-agent/albany---greater-region-wa"
    all_agents = []
    page = 1
    output_file = "AGENT_albany---greater-region-wa.json"
    
    # Try to load existing data if file exists
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            all_agents = json.load(f)
            print(f"Loaded {len(all_agents)} existing agents from {output_file}")
    except FileNotFoundError:
        print(f"Starting new file: {output_file}")
    except Exception as e:
        print(f"Error loading existing file: {str(e)}")
    
    while True:
        url = f"{base_url}?source=results&page={page}"
        print(f"\nFetching page {page}...")
        
        agents = get_agents_from_page(url, page)
        if not agents:
            break
            
        all_agents.extend(agents)
        
        # Save data every 4 pages
        if page % 4 == 0:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_agents, f, indent=4, ensure_ascii=False)
                print(f"\nSaved {len(all_agents)} agents to {output_file}")
                
                # Take a break after saving
                delay = random.uniform(15, 20)
                print(f"Taking a {delay:.1f} second break...")
                time.sleep(delay)
            except Exception as e:
                print(f"Error saving to JSON file: {str(e)}")
        
        page += 1
    
    # Final save at the end
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_agents, f, indent=4, ensure_ascii=False)
        print(f"\nFinal save: {len(all_agents)} agents saved to {output_file}")
    except Exception as e:
        print(f"Error saving final data to JSON file: {str(e)}")

if __name__ == "__main__":
    main()
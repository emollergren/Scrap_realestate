import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import Dict, List, Tuple

def get_cookies() -> str:
    """Get cookies string in the exact format as browser"""
    return (
        "reauid=1e142017754d00006e2841680b01000011e90300; "
        "Country=DE; "
        "split_audience=a; "
        "_gcl_au=1.1.1545764079.1749100670; "
        "_ga=GA1.1.1454637171.1749100670; "
        "DM_SitId1464=1; "
        "DM_SitId1464SecId12708=1; "
        "tracking_acknowledged=true; "
        "AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; "
        "_lr_geo_location_state=HE; "
        "_lr_geo_location=DE; "
        "s_ecid=MCMID%7C75503528588372506932777235831909784981; "
        "legs_sq=%5B%5BB%5D%5D; "
        "s_cc=true; "
        "s_sq=%5B%5BB%5D%5D; "
        "ew_bkt=41; "
        "KFC=yw0PtJ3yFxLa6LOMKzfm63lq8/J31RaCzYubfmpMj9g=|1749107262838; "
        "KP_UIDz-ssn=0adrbuOpmg19DS1ayBfRdnmOI2qatq4EkIhqJeZoC3BSiPyQQYQGdQwobhbyMGQSzuStCqg1CpcBZUv2wSsFqJbfDEFcm0bGZeqTbxCbHGypRp2JuxFSflMnH2DfmTtLlYSNm9yEaChjcb7EqY7NB7FkMOC5sPeArm0UioP8X9V; "
        "KP_UIDz=0adrbuOpmg19DS1ayBfRdnmOI2qatq4EkIhqJeZoC3BSiPyQQYQGdQwobhbyMGQSzuStCqg1CpcBZUv2wSsFqJbfDEFcm0bGZeqTbxCbHGypRp2JuxFSflMnH2DfmTtLlYSNm9yEaChjcb7EqY7NB7FkMOC5sPeArm0UioP8X9V; "
        "AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20245%7CMCMID%7C75503528588372506932777235831909784981%7CMCAAMLH-1749713754%7C3%7CMCAAMB-1749713754%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749116154s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; "
        "QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Farmidale---greater-region-nsw%3Fsource%3Dresults~1749100694415%7Chttps%3A%2F%2Fwww.realestate.com.au%2Ffind-agent%2Farmidale---greater-region-nsw%3Fsource%3Dresults%26page%3D2~1749109805681; "
        "KP2_UIDz-ssn=0cQ42oqA9uTmCkHRt7oA5QwxySTfKPPPf9tbfc917McZhOIpdaP17GfaSfkzJ1yp9kDZPYWgjGtQ3nCy21HyrBlcS9I5XFAFbKpD66ANdaE9icwxcfYwPfkoIJyHtgqUtuM5ZObFj9ahCeWQyilZzlZIbMyroEqpF6ISp8ylGT2; "
        "KP2_UIDz=0cQ42oqA9uTmCkHRt7oA5QwxySTfKPPPf9tbfc917McZhOIpdaP17GfaSfkzJ1yp9kDZPYWgjGtQ3nCy21HyrBlcS9I5XFAFbKpD66ANdaE9icwxcfYwPfkoIJyHtgqUtuM5ZObFj9ahCeWQyilZzlZIbMyroEqpF6ISp8ylGT2; "
        "pageview_counter.srs=9; "
        "utag_main=v_id:01973e86265f001225e04a3daaaa0506f00550670086e$_sn:2$_se:9$_ss:0$_st:1749112128692$vapi_domain:realestate.com.au$ses_id:1749105628343%3Bexp-session$_pn:9%3Bexp-session$_prevpage:rea%3Afind%20agent%3Aagent%3Asearch%20results%3Bexp-1749113929865$adform_uid:47924083152249268%3Bexp-session; "
        "s_nr30=1749110329866-Repeat; "
        "nol_fpid=sym6721ezdodteozyigh55n0lcc8l1749100670|1749100670831|1749110331440|1749110332423; "
        "_ga_3J0XCBB972=GS2.1.s1749106467$o2$g1$t1749110333$j52$l0$h0"
    )

def get_headers() -> Dict[str, str]:
    """Get headers for requests"""
    headers = {
        "authority": "www.realestate.com.au",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "reauid=13d8231797a83d00f9aa426811020000499f0300; Country=DE; KP_REF=; KP_IM=CiQ2OTFkMDZlZS03NmVmLTQ1OTMtODA3ZS1hZDUxNDA4OThlMzk; KP2_UIDz-ssn=0ax7hAtbAjYtUbkxbORK9syBUl9xWjAWM2231gI0FJ83ycvnRtq3M8X5ODhc5QyO3NiPHkFbSjYZJnFjhILkz93P5K99OsxumiBh9EwysmiVPlfZaLyHAuF7BNKBUlWIZi4tC9ZSIaujvOKdZeyCuL3dlyVRvOkKhpHyYpjVNCD; KP2_UIDz=0ax7hAtbAjYtUbkxbORK9syBUl9xWjAWM2231gI0FJ83ycvnRtq3M8X5ODhc5QyO3NiPHkFbSjYZJnFjhILkz93P5K99OsxumiBh9EwysmiVPlfZaLyHAuF7BNKBUlWIZi4tC9ZSIaujvOKdZeyCuL3dlyVRvOkKhpHyYpjVNCD; split_audience=c; pageview_counter.srs=1; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; s_nr30=1749199627245-New; utag_main=v_id:0197446c1b05001f5d18b6363c110506f005906700bd0$_sn:1$_se:2$_ss:0$_st:1749201426218$ses_id:1749199624965%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:realestate.com.au$_prevpage:undefined%3Bexp-1749203227254; s_ecid=MCMID%7C09166122703591472113487511986850489146; s_cc=true; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20246%7CMCMID%7C09166122703591472113487511986850489146%7CMCAAMLH-1749804427%7C3%7CMCAAMB-1749804427%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749206828s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; _gcl_au=1.1.2006358852.1749199631; DM_SitId1464=1; DM_SitId1464SecId12708=1; _ga_3J0XCBB972=GS2.1.s1749199633$o1$g0$t1749199633$j60$l0$h0; _ga=GA1.1.1872887338.1749199633; nol_fpid=qv0ucwa6b6d2fn6tdlsexmxizxdgv1749199633|1749199633568|1749199633568|1749199633568",
        "if-none-match": 'W/"8dac2-e1r4R+KW0Pw3OXfosAZTdDUhLno"',
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
    return headers

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

def create_region_url(region_name: str, state: str) -> str:
    """Create URL for a region"""
    # Convert region name to URL format
    region_url = region_name.lower().replace(' - ', '---').replace(' ', '-')
    return f"https://www.realestate.com.au/find-agent/{region_url}-{state.lower()}"

def get_webpage_agent_count(url: str, max_retries: int = 3) -> int:
    """Get agent count from webpage with retry mechanism"""
    headers = get_headers()
    session = requests.Session()
    
    # First visit the main page to get initial cookies
    session.get("https://www.realestate.com.au", headers=headers)
    time.sleep(random.uniform(2, 3))  # Add small delay after initial request
    
    for attempt in range(max_retries):
        try:
            # Add small delay before each request
            delay = random.uniform(2, 3)
            print(f"Waiting {delay:.1f} seconds before request...")
            time.sleep(delay)

            # Add referer header for subsequent requests
            headers['referer'] = url
            
            response = session.get(url, headers=headers)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return get_total_agent_count(soup)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                wait_time = (attempt + 1) * 30  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"HTTP Error: {str(e)}")
                return 0
        except Exception as e:
            print(f"Error fetching webpage: {str(e)}")
            return 0

    print(f"Failed to fetch webpage after {max_retries} attempts")
    return 0

def check_region_counts(region: Dict) -> Tuple[bool, int, int]:
    """Check agent counts for a single region"""
    region_name = region['name']
    state = region['state']
    region_id = region['id']
    
    print(f"\nChecking region: {region_name}, {state}")
    
    # Get count from webpage
    base_url = create_region_url(region_name, state)
    webpage_count = get_webpage_agent_count(f"{base_url}?source=results&page=1")
    
    # Get count from JSON
    try:
        with open('Agents.json', 'r', encoding='utf-8') as f:
            regions_data = {region['id']: region for region in json.load(f)}
            json_count = len(regions_data.get(region_id, {}).get('agents', []))
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        json_count = 0
    
    # Compare counts
    counts_match = webpage_count == json_count
    
    print(f"Count comparison for {region_name}:")
    print(f"- Webpage count: {webpage_count}")
    print(f"- JSON count: {json_count}")
    print(f"- Status: {'✓ Match' if counts_match else '✗ Mismatch'}")
    
    # Calculate stopped page number for mismatched regions
    if not counts_match and json_count > 0:
        stopped_page = (json_count // 24) + 1
        stopped_url = f"{base_url}?source=results&page={stopped_page}"
        print(f"- Stopped at page {stopped_page}")
        print(f"- Stopped URL: {stopped_url}")
    
    return counts_match, webpage_count, json_count

def main():
    # Load regions from JSON file
    try:
        with open('regions.json', 'r', encoding='utf-8') as f:
            regions = json.load(f)
    except Exception as e:
        print(f"Error loading regions.json: {str(e)}")
        return

    # Initialize counters
    total_regions = len(regions)
    matching_regions = 0
    mismatching_regions = []
    
    print(f"\nStarting count check for {total_regions} regions...")
    
    # Check each region
    for region in regions:
        counts_match, webpage_count, json_count = check_region_counts(region)
        
        if counts_match:
            matching_regions += 1
        else:
            stopped_page = (json_count // 24) + 1 if json_count > 0 else 0
            base_url = create_region_url(region['name'], region['state'])
            stopped_url = f"{base_url}?source=results&page={stopped_page}"
            
            mismatching_regions.append({
                'region_name': region['name'],
                'state': region['state'],
                'webpage_count': webpage_count,
                'json_count': json_count,
                'stopped_page': stopped_page,
                'stopped_url': stopped_url
            })
        
        # Take a break between regions
        delay = random.uniform(2, 3)
        print(f"Taking a {delay:.1f} second break...")
        time.sleep(delay)
    
    # Print summary
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
            print(f"  Stopped at page: {region['stopped_page']}")
            print(f"  Stopped URL: {region['stopped_url']}")

if __name__ == "__main__":
    main()

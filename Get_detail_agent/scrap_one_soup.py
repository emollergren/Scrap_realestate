import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import Dict
import re
import csv

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
        "cookie": "Country=DE; ew_bkt=57; reauid=13d8231797a83d00f81d4368a7030000d9b00300; split_audience=d; s_fid=3619558552FF58AF-0C79433CE5CB66A8; s_cc=true; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; s_ecid=MCMID%7C23299895489748296811735786085368238954; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=179643557%7CMCIDTS%7C20247%7CMCMID%7C23299895489748296811735786085368238954%7CMCAAMLH-1749887741%7C3%7CMCAAMB-1749887741%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749290141s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; s_vi=[CS]v1|3421F83B422BD0E4-40001D48C0F32FE8[CE]; tracking_acknowledged=true; _ga=GA1.1.1529139792.1749282944; _gcl_au=1.1.1063711179.1749282945; DM_SitId1464=1; DM_SitId1464SecId12708=1; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fagent%2Frosemary-auricchio-55151%3FcampaignType%3Dinternal%26campaignChannel%3Din_product%26campaignSource%3Drea%26campaignName%3Dsell_enq%26campaignPlacement%3Dagent_search_result_card%26campaignKeyword%3Dagency_marketplace%26sourcePage%3Dagent_srp%26sourceElement%3Dagent_search_result_card~1749283017266%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fagency%2Flj-hooker-west-lakes-henley-beach-XLJSEB~1749284165911; QSI_SI_b7yBB0eituPt5vE_intercept=true; legs_sq=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; appraisal_form_progress=landing; KP_UIDz-1-ssn=0cWNawwOHLluiV1oS5sRDZSmjcfK43N5E8JGTbytsdaOLYxgYJpFt1TWr5fHU2HrgwWHDCUVn0txirbX5e0IH2yt8pNYoJFKncfABzLETutvAu8u6qs68kU5r7QvA4JLJ37ma9wkeaHCdh8cLbJ6SGdLhejTbbwRNZj2yQYEj36; KP_UIDz-1=0cWNawwOHLluiV1oS5sRDZSmjcfK43N5E8JGTbytsdaOLYxgYJpFt1TWr5fHU2HrgwWHDCUVn0txirbX5e0IH2yt8pNYoJFKncfABzLETutvAu8u6qs68kU5r7QvA4JLJ37ma9wkeaHCdh8cLbJ6SGdLhejTbbwRNZj2yQYEj36; KFC=4tHANThTWyUMHFUk+roOeUONVLOlN6nwSxyVCqMiEqA=|1749286175370; KP_UIDz-ssn=0cxwQOmx4EZC1rfoi3mz0A6ILm8SwIK2bI2HAMrGWttvNu7aKpHNN5ICZhmESQj1blldb5HrfaPk10RnEA64O2qJErpdZMxUBLUK1EvWkzM9jAwAdepv3KCWoNZZnRZKzE9RoakYIbVnrQYUaB1ohjcRfUB5IAhxMZsiifT0oMS; KP_UIDz=0cxwQOmx4EZC1rfoi3mz0A6ILm8SwIK2bI2HAMrGWttvNu7aKpHNN5ICZhmESQj1blldb5HrfaPk10RnEA64O2qJErpdZMxUBLUK1EvWkzM9jAwAdepv3KCWoNZZnRZKzE9RoakYIbVnrQYUaB1ohjcRfUB5IAhxMZsiifT0oMS; utag_main=v_id:01974962bc630014ff976fedd41d0506f01230670086e$_sn:1$_se:15$_ss:0$_st:1749287985788$ses_id:1749282896995%3Bexp-session$_pn:6%3Bexp-session$vapi_domain:realestate.com.au$_prevpage:rea%3Afind%20agent%3Aprofiles%3Aagent%20profile%3Bexp-1749289787197; s_nr30=1749286187199-New; nol_fpid=pv1tyjv9trlp1zteyyzrbmg9mlvnf1749282949|1749282949176|1749286189186|1749286190901; _ga_3J0XCBB972=GS2.1.s1749282943$o1$g1$t1749286192$j60$l0$h0",
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

def extract_json_from_script(html_content: str) -> Dict:
    """Extract JSON data from the script tag containing ArgonautExchange"""
    try:
        # Find the script tag containing ArgonautExchange
        pattern = r'window\.ArgonautExchange\s*=\s*({.*?});'
        match = re.search(pattern, html_content, re.DOTALL)
        if not match:
            return {}
        
        # Parse the outer JSON
        outer_json = json.loads(match.group(1))
        
        # Get the AGENT_PROFILE data
        agent_profile_str_1 = outer_json.get('resi-agent_customer-profile-experience', {}).get('AGENT_PROFILE', '{}')
        agent_profile1 = json.loads(agent_profile_str_1)
        
        agent_profile_str_2 = outer_json.get('resi-agent_customer-profile-experience', {}).get('AGENT_PROFILE_LISTINGS', '{}')
        agent_profile2 =json.loads(agent_profile_str_2)

        # Split name into first and last name
        full_name = agent_profile1.get('agent', {}).get('name', '')
        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # return agent_profile_str
        return {
            'agent_profile' : {
            'profile_id': agent_profile1.get('agent', {}).get('profileId', ''),
            'first_name': first_name,
            'last_name': last_name,
            'friendly_name': agent_profile1.get('agent', {}).get('friendlyName', ''),
            'description': agent_profile1.get('agent', {}).get('description', ''),
            'job_title': agent_profile1.get('agent', {}).get('jobTitle', ''),
            'years_experience': agent_profile1.get('agent', {}).get('yearsExperience', 0),
            'start_year': agent_profile1.get('agent', {}).get('startYearInIndustry', 0),
            'rating': agent_profile1.get('agent', {}).get('avgRating', 0),
            'total_reviews': agent_profile1.get('agent', {}).get('totalReviews', 0),
            'power_profile': agent_profile1.get('agent', {}).get('powerProfile', False),
            'business_phone': agent_profile1.get('agent', {}).get('businessPhone', ''),
            'mobile': agent_profile1.get('agent', {}).get('mobile', ''),
            'location': {
                'suburb': agent_profile1.get('agent', {}).get('mostActiveLocation', {}).get('suburb', ''),
                'state': agent_profile1.get('agent', {}).get('mostActiveLocation', {}).get('state', ''),
                'postcode': agent_profile1.get('agent', {}).get('mostActiveLocation', {}).get('postcode', '')
            },
            'linked_salespeople_ids': agent_profile1.get('agent', {}).get('linkedSalespeopleIds', []),
            # 'inclusions': raw_data.get('inclusions', []),
            'compliments': [
                {
                    'tag': comp.get('tag', ''),
                    'count': comp.get('count', 0)
                }
                for comp in agent_profile1.get('agent', {}).get('compliments', [])
            ],
            'profile_image': agent_profile1.get('agent', {}).get('profileImage', {}).get('templatedUrl', ''),
            'agency': {
                'id': agent_profile1.get('agent', {}).get('agency', {}).get('id', ''),
                'name': agent_profile1.get('agent', {}).get('agency', {}).get('name', ''),
                'logo': agent_profile1.get('agent', {}).get('agency', {}).get('logo', {}).get('templatedUrl', ''),
                'branding': agent_profile1.get('agent', {}).get('agency', {}).get('branding', {}).get('primaryColor', ''),
                'profile_url': agent_profile1.get('agent', {}).get('agency', {}).get('_links', {}).get('profile', {}).get('href', '')
            },
            'social': {
                'facebook': agent_profile1.get('agent', {}).get('social', {}).get('facebook', ''),
                'instagram': agent_profile1.get('agent', {}).get('social', {}).get('instagram', ''),
                'twitter': agent_profile1.get('agent', {}).get('social', {}).get('twitter', ''),
                'linkedin': agent_profile1.get('agent', {}).get('social', {}).get('linkedin', '')
            },
            'agent_stats': {
                'median_days_on_site': {
                    'townhouse': agent_profile1.get('agentStats', {}).get('medianDaysOnSite', {}).get('townhouse', 0),
                    'apartment': agent_profile1.get('agentStats', {}).get('medianDaysOnSite', {}).get('apartment', 0),
                    'house': agent_profile1.get('agentStats', {}).get('medianDaysOnSite', {}).get('house', 0),
                    'overall': agent_profile1.get('agentStats', {}).get('medianDaysOnSite', {}).get('overall', 0)
                },
                'median_sold_price': {
                    'townhouse': agent_profile1.get('agentStats', {}).get('medianSoldPrice', {}).get('townhouse', 0),
                    'apartment': agent_profile1.get('agentStats', {}).get('medianSoldPrice', {}).get('apartment', 0),
                    'house': agent_profile1.get('agentStats', {}).get('medianSoldPrice', {}).get('house', 0),
                    'overall': agent_profile1.get('agentStats', {}).get('medianSoldPrice', {}).get('overall', 0)
                },
                'sales_count': {
                    'apartment': agent_profile1.get('agentStats', {}).get('salesCount', {}).get('apartment', 0),
                    'townhouse': agent_profile1.get('agentStats', {}).get('salesCount', {}).get('townhouse', 0),
                    'as_lead_agent': agent_profile1.get('agentStats', {}).get('salesCount', {}).get('asLeadAgent', 0),
                    'as_secondary_agent': agent_profile1.get('agentStats', {}).get('salesCount', {}).get('asSecondaryAgent', 0),
                    'house': agent_profile1.get('agentStats', {}).get('salesCount', {}).get('house', 0),
                    'overall': agent_profile1.get('agentStats', {}).get('salesCount', {}).get('overall', 0)
                }
            },
                'agent_sold_count' :{
                    'total_result_count' : agent_profile2.get('agentMapSoldListings', {}).get('totalResultsCount', 0),
                    'result_count': agent_profile2.get('agentMapSoldListings', {}).get('resultsCount', 0)
                },
                'agent_buy_count' :{
                    'total_result_count': agent_profile2.get('agentMapBuyListings', {}).get('totalResultCount', 0),
                    'result_count': agent_profile2.get('agentMapBuyListings', {}).get('resultsCount', 0)
                },
                'agent_rent_count' :{
                    'total_result_count': agent_profile2.get('agentMapRentListings', {}).get('totalResultCount', 0),
                    'result_count': agent_profile2.get('agentMapRentListings', {}).get('resultsCount', 0)
                }
            },
            'agent_profile_listing' : {
                # 'agent_Sold' : {
                #     # 'listings' : [
                #     #     {
                #     #         'id': comps.get('id', ''),
                #     #         'price': comps.get('price', ''),
                #     #         'address' : {
                #     #             'short_address' : comps.get('address', {}).get('short_address', ''),
                #     #             'suburb' : comps.get('address', {}).get('suburb', ''),
                #     #             'state' : comps.get('address', {}).get('state', ''),
                #     #             'postcode' : comps.get('address', {}).get('postcode', '')
                #     #         },
                #     #         'general_features' : {
                #     #             'bathrooms' : comps.get('generalFeatures', {}).get('bathrooms', 0),
                #     #             'bedrooms' : comps.get('generalFeatures', {}).get('bedrooms', 0),
                #     #             'parkingSpace' : comps.get('generalFeatures', {}).get('parkingSpace', 0)
                #     #         },
                #     #         'property_type' : comps.get('propertyType', ''),
                #     #         'product_depth': comps.get('productDepth', ''),
                #     #         'listing_company_id' : comps.get('listingCompany', {}).get('id', ''),
                #     #         'media' : {
                #     #             'main_image' : comps.get('media', {}).get('mainImage', ''),
                #     #             'images' : comps.get('media', {}).get('images', [])
                #     #         },
                #     #         'listing_status' : comps.get('listingStatus', ''),
                #     #         'geocode' : {
                #     #             'latitude' : comps.get('geocode', {}).get('latitude', ''),
                #     #             'longitude' : comps.get('geocode', {}).get('longitude', ''),
                #     #         },
                #     #         'type_name': comps.get('__typename', '')
                #     #     }
                #     #     for comps in agent_profile2.get('agentMapSoldListings', {}).get('listings', [])
                #     # ],
                #     'listings' : [
                #         {
                #             **listing,
                #             'media': {
                #                 'mainImage': listing.get('media', {}).get('mainImage', '')
                #             } if 'media' in listing else {}
                #         }
                #         for listing in agent_profile2.get('agentMapSoldListings', {}).get('listings', [])
                #     ]
                # },
                # 'agent_Buy': {
                #     'listings' : [
                #         {
                #             **listing,
                #             'media': {
                #                 'mainImage': listing.get('media', {}).get('mainImage', '')
                #             } if 'media' in listing else {}
                #         }
                #         for listing in agent_profile2.get('agentMapBuyListings', {}).get('listings', [])
                #     ]
                # },
                # 'agent_Rent': {
                #     'listings' : [
                #         {
                #             **listing,
                #             'media': {
                #                 'mainImage': listing.get('media', {}).get('mainImage', '')
                #             } if 'media' in listing else {}
                #         }
                #         for listing in agent_profile2.get('agentMapRentListings', {}).get('listings', [])
                #     ]
                # }
                'agent_Sold' : {
                    'listings' : agent_profile2.get('agentMapSoldListings', {}).get('listings', [])
                },
                'agent_Buy' : {
                    'listings' : agent_profile2.get('agentMapBuyListings', {}).get('listings', [])
                },
                'agent_Rent' : {
                    'listings' : agent_profile2.get('agentMapRentListings', {}).get('listings', [])
                }
            }
        }
    except Exception as e:
        print(f"Error extracting JSON from script: {str(e)}")
        return {}

# def normalize_agent_data(raw_data: Dict) -> Dict:
#     """Normalize the agent data into a consistent format"""
#     # print(agent_profile1.get('agentStats', {}))
    

def scrape_agent_profile(url: str, max_retries: int = 3) -> Dict:
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
            normalized_data = extract_json_from_script(response.text)
            # if not raw_data:
            #     print("\nCould not extract JSON data from script")
            #     return {}
            
            # # Normalize the data
            # normalized_data = normalize_agent_data(raw_data)
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
    # Example usage
    url = "https://www.realestate.com.au/agent/rosemary-auricchio-55151?campaignType=internal&campaignChannel=in_product&campaignSource=rea&campaignName=sell_enq&campaignPlacement=agent_search_result_card&campaignKeyword=agency_marketplace&sourcePage=agent_srp&sourceElement=agent_search_result_card"
    agent_data = scrape_agent_profile(url)
    
    # Process URLs to replace size placeholders
    agent_data = process_urls(agent_data)
    
    print("\nAgent Profile Data:")
    print(json.dumps(agent_data, indent=4, ensure_ascii=False))
    
    # Get profile data for file naming
    profile_data = agent_data.get('agent_profile', {})
    first_name = profile_data.get('first_name', '').lower()
    last_name = profile_data.get('last_name', '').lower()
    profile_id = profile_data.get('profile_id', '')
    
    # Create filename
    filename_base = f"{first_name}_{last_name}_{profile_id}"
    
    # Save to JSON file
    try:
        with open(f'{filename_base}.json', 'w', encoding='utf-8') as f:
            json.dump(agent_data, f, indent=4, ensure_ascii=False)
        print(f"\nData saved to {filename_base}.json")
    except Exception as e:
        print(f"\nError saving to JSON file: {str(e)}")

    # Save to CSV file
    try:
        # Get only the agent_profile data
        profile_data = agent_data.get('agent_profile', {})
        
        # Flatten the nested dictionary
        flattened_data = flatten_dict(profile_data)
        
        # Write to CSV
        with open(f'{filename_base}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(flattened_data.keys())
            # Write data
            writer.writerow(flattened_data.values())
        print(f"\nData saved to {filename_base}.csv")
    except Exception as e:
        print(f"\nError saving to CSV file: {str(e)}")

if __name__ == "__main__":
    main()

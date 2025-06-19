import csv
import json
import os
from typing import List, Dict, Any

def save_agents_to_csv(agents: List[Dict[str, Any]], csv_path: str):
    fieldnames = [
        "profile_id", "first_name", "last_name", "friendly_name", "description", "job_title", "years_experience", "start_year", "rating", "total_reviews", "power_profile", "business_phone", "mobile", "agent_url_realestate", "regions", "location", "linked_salespeople_ids", "compliments", "profile_image", "agency_id", "agency_name", "agency_logo", "agency_profile_url", "agencyUrl", "agency_businessPhone", "agency_streetAddress", "agency_suburb", "agency_state", "agency_postcode", "social_facebook", "social_instagram", "social_twitter", "social_linkedin", "agent_stats_median_days_on_site", "agent_median_sold_price", "agent_sales_count", "agent_sold_count", "agent_buy_count", "agent_rent_count"
    ]
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for agent in agents:
            agency = agent.get("agency", {})
            social = agent.get("social", {})
            agent_stats = agent.get("agent_stats", {})
            row = {
                "profile_id": agent.get("profile_id"),
                "first_name": agent.get("first_name"),
                "last_name": agent.get("last_name"),
                "friendly_name": agent.get("friendly_name"),
                "description": agent.get("description"),
                "job_title": agent.get("job_title"),
                "years_experience": agent.get("years_experience"),
                "start_year": agent.get("start_year"),
                "rating": agent.get("rating"),
                "total_reviews": agent.get("total_reviews"),
                "power_profile": agent.get("power_profile"),
                "business_phone": agent.get("business_phone"),
                "mobile": agent.get("mobile"),
                "agent_url_realestate": agent.get("agent_url"),
                "regions": json.dumps(agent.get("regions", [])),
                "location": f"{agent.get('location', {}).get('suburb', '')}, {agent.get('location', {}).get('state', '')}, {agent.get('location', {}).get('postcode', '')}",
                "linked_salespeople_ids": json.dumps(agent.get("linked_salespeople_ids", [])),
                "compliments": json.dumps(agent.get("compliments", [])),
                "profile_image": agent.get("profile_image"),
                "agency_id": agency.get("id"),
                "agency_name": agency.get("name"),
                "agency_logo": agency.get("logo"),
                "agency_profile_url": agency.get("profile_url"),
                "agencyUrl": agency.get("agencyUrl"),
                "agency_businessPhone": agency.get("businessPhone"),
                "agency_streetAddress": agency.get("address", {}).get("streetAddress", ""),
                "agency_suburb": agency.get("address", {}).get("suburb", ""),
                "agency_state": agency.get("address", {}).get("state", ""),
                "agency_postcode": agency.get("address", {}).get("postcode", ""),
                "social_facebook": social.get("facebook"),
                "social_instagram": social.get("instagram"),
                "social_twitter": social.get("twitter"),
                "social_linkedin": social.get("linkedin"),
                "agent_stats_median_days_on_site": json.dumps(agent_stats.get("median_days_on_site", {})),
                "agent_median_sold_price": json.dumps(agent_stats.get("median_sold_price", {})),
                "agent_sales_count": json.dumps(agent_stats.get("sales_count", {})),
                "agent_sold_count": json.dumps(agent.get("agent_sold_count", {})),
                "agent_buy_count": json.dumps(agent.get("agent_buy_count", {})),
                "agent_rent_count": json.dumps(agent.get("agent_rent_count", {})),
            }
            writer.writerow(row)

def save_agencies_to_csv(agencies: List[Dict[str, Any]], csv_path: str):
    fieldnames = [
        "id", "name", "description", "agencyUrl", "businessPhone", "streetAddress", "suburb", "state", "postcode"
    ]
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for agency in agencies:
            address = agency.get("address", {})
            row = {
                "id": agency.get("agencyId") or agency.get("id"),
                "name": agency.get("name"),
                "description": agency.get("description"),
                "agencyUrl": agency.get("agencyUrl"),
                "businessPhone": agency.get("businessPhone"),
                "streetAddress": address.get("streetAddress", ""),
                "suburb": address.get("suburb", ""),
                "state": address.get("state", ""),
                "postcode": address.get("postcode", ""),
            }
            writer.writerow(row)

def load_json_objects(filepath):
    """
    Loads a list of JSON objects from a file that is either:
    - a JSON array (single large array)
    - or JSONL (one object per line)
    """
    objs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        # Peek at the first non-whitespace character
        while True:
            pos = f.tell()
            first = f.read(1)
            if not first:
                return []  # empty file
            if not first.isspace():
                break
        f.seek(pos)
        if first == '[':
            # JSON array
            try:
                objs = json.load(f)
            except Exception as e:
                print(f"Error loading JSON array from {filepath}: {e}")
                return []
        else:
            # JSONL
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    objs.append(json.loads(line))
                except Exception as e:
                    print(f"Skipping line due to error: {e}")
    return objs

def main():
    base_dir = os.path.dirname(__file__)
    agent_json_path = os.path.join(base_dir, 'detailed_agent_result.json')
    agency_json_path = os.path.join(base_dir, 'detailed_agency_result.json')
    agent_csv_path = os.path.join(base_dir, 'detailed_agent_result.csv')
    agency_csv_path = os.path.join(base_dir, 'detailed_agency_result.csv')

    if os.path.exists(agent_json_path):
        print(f"Processing {agent_json_path} ...")
        agents = load_json_objects(agent_json_path)
        print(f"Loaded {len(agents)} agent objects.")
        save_agents_to_csv(agents, agent_csv_path)
        print(f"Saved {agent_csv_path}")
    else:
        print(f"Agent JSON file not found: {agent_json_path}")

    if os.path.exists(agency_json_path):
        print(f"Processing {agency_json_path} ...")
        agencies = load_json_objects(agency_json_path)
        print(f"Loaded {len(agencies)} agency objects.")
        save_agencies_to_csv(agencies, agency_csv_path)
        print(f"Saved {agency_csv_path}")
    else:
        print(f"Agency JSON file not found: {agency_json_path}")

if __name__ == "__main__":
    main()

# Example usage:
# agents = [ ... ]  # List of agent dicts
# agencies = [ ... ]  # List of agency dicts
# save_agents_to_csv(agents, 'detailed_agent_result.csv')
# save_agencies_to_csv(agencies, 'detailed_agency_result.csv')

import json
import os
from collections import OrderedDict
import csv

def normalize_phone(phone):
    if not phone:
        return ''
    return ''.join(filter(str.isdigit, str(phone)))

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
mail_path = os.path.join(script_dir, 'mail.json')
agent_path = os.path.join(script_dir, 'detailed_agent_result.json')
enrich_path = os.path.join(script_dir, 'detailed_agent_enrich.json')
enrich_csv_path = os.path.join(script_dir, 'detailed_agent_enrich.csv')

# Step 1: Build phone1->email lookup from mail.json
print('Building phone1 to email lookup from mail.json...')
phone_to_email = {}
with open(mail_path, 'r', encoding='utf-8') as f:
    mail_data = json.load(f)
    for entry in mail_data:
        phone1 = normalize_phone(entry.get('phone1'))
        email = entry.get('email')
        if phone1 and email:
            phone_to_email[phone1] = email
print(f'Loaded {len(phone_to_email)} phone1->email pairs.')

# Step 2: Enrich agent data and reorder keys
print('Enriching agent data...')
with open(agent_path, 'r', encoding='utf-8') as fin, open(enrich_path, 'w', encoding='utf-8') as fout:
    agent_data = json.load(fin)
    enriched_count = 0
    unriched_count = 0
    ordered_agents = []
    for agent in agent_data:
        mobile = normalize_phone(agent.get('mobile'))
        agent_email = phone_to_email.get(mobile)
        if agent_email:
            agent['agent_email'] = agent_email
            enriched_count += 1
        else:
            agent['agent_email'] = None
            unriched_count += 1
        # Reorder keys
        ordered = OrderedDict()
        for key in [
            'profile_id', 'first_name', 'last_name', 'friendly_name', 'business_phone', 'mobile', 'agent_email', 'description', 'job_title', 'years_experience', 'start_year', 'rating', 'total_reviews', 'power_profile', 'agent_url', 'regions', 'location', 'linked_salespeople_ids', 'compliments', 'profile_image', 'agency', 'social', 'agent_stats', 'agent_sold_count', 'agent_buy_count', 'agent_rent_count']:
            if key in agent:
                ordered[key] = agent[key]
        # Add the rest of the keys
        for k, v in agent.items():
            if k not in ordered:
                ordered[k] = v
        ordered_agents.append(ordered)
    json.dump(ordered_agents, fout, indent=4, ensure_ascii=False)
print(f'Enriched data written to {enrich_path}')
print(f'Enriched agents: {enriched_count}')
print(f'Unriched agents: {unriched_count}')

# Step 3: Write CSV in the same style as organize.py, with agent_email after mobile
print(f'Writing enriched CSV to {enrich_csv_path}...')
def save_enriched_agents_to_csv(agents, csv_path):
    fieldnames = [
        "profile_id", "first_name", "last_name", "friendly_name", "business_phone", "mobile", "agent_email", "description", "job_title", "years_experience", "start_year", "rating", "total_reviews", "power_profile", "agent_url_realestate", "regions", "location", "linked_salespeople_ids", "compliments", "profile_image", "agency_id", "agency_name", "agency_logo", "agency_profile_url", "agencyUrl", "agency_businessPhone", "agency_streetAddress", "agency_suburb", "agency_state", "agency_postcode", "social_facebook", "social_instagram", "social_twitter", "social_linkedin", "agent_stats_median_days_on_site", "agent_median_sold_price", "agent_sales_count", "agent_sold_count", "agent_buy_count", "agent_rent_count"
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
                "business_phone": agent.get("business_phone"),
                "mobile": agent.get("mobile"),
                "agent_email": agent.get("agent_email"),
                "description": agent.get("description"),
                "job_title": agent.get("job_title"),
                "years_experience": agent.get("years_experience"),
                "start_year": agent.get("start_year"),
                "rating": agent.get("rating"),
                "total_reviews": agent.get("total_reviews"),
                "power_profile": agent.get("power_profile"),
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

save_enriched_agents_to_csv(ordered_agents, enrich_csv_path)
print(f'Enriched CSV data written to {enrich_csv_path}')

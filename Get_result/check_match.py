import json
import os

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_phone(phone):
    if not phone:
        return ''
    return ''.join(filter(str.isdigit, str(phone)))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mail_path = os.path.join(script_dir, 'mail.json')
    agent_path = os.path.join(script_dir, 'detailed_agent_result.json')
    result_path = os.path.join(script_dir, 'check_result.json')

    mail_list = load_json(mail_path)
    agent_list = load_json(agent_path)

    # Build lookup for agent by name and phone
    agent_by_name = {}
    agent_by_business_phone = {}
    agent_by_mobile = {}
    for agent in agent_list:
        name = f"{agent.get('first_name', '').strip()} {agent.get('last_name', '').strip()}".strip()
        agent_by_name[name.lower()] = agent
        agent_by_business_phone[normalize_phone(agent.get('business_phone'))] = agent
        agent_by_mobile[normalize_phone(agent.get('mobile'))] = agent

    results = []
    for mail in mail_list:
        name = mail.get('name', '').strip()
        name_lc = name.lower()
        phone1 = normalize_phone(mail.get('phone1'))
        phone2 = normalize_phone(mail.get('phone2'))

        match_name = name_lc in agent_by_name
        match_phone1_business = phone1 in agent_by_business_phone
        match_phone1_mobile = phone1 in agent_by_mobile
        match_phone2_business = phone2 in agent_by_business_phone
        match_phone2_mobile = phone2 in agent_by_mobile

        # Combinations with logic-style keys
        result = {
            'name': name,
            'name & scraped_name': match_name,
            'phone1 & business_phone': match_phone1_business,
            '(name & scraped_name) & (phone1 & business_phone)': match_name and match_phone1_business,
            'phone1 & mobile': match_phone1_mobile,
            '(name & scraped_name) & (phone1 & mobile)': match_name and match_phone1_mobile,
            'phone2 & business_phone': match_phone2_business,
            '(name & scraped_name) & (phone2 & business_phone)': match_name and match_phone2_business,
            'phone2 & mobile': match_phone2_mobile,
            '(name & scraped_name) & (phone2 & mobile)': match_name and match_phone2_mobile,
            '(phone1 & business_phone) & (phone2 & mobile)': match_phone1_business and match_phone2_mobile,
            '(name & scraped_name) & ((phone1 & business_phone) & (phone2 & mobile))': match_name and match_phone1_business and match_phone2_mobile,
            '(phone1 & mobile) & (phone2 & business_phone)': match_phone1_mobile and match_phone2_business,
            '(name & scraped_name) & ((phone1 & mobile) & (phone2 & business_phone))': match_name and match_phone1_mobile and match_phone2_business
        }
        results.append(result)

    # Write results to check_result.json
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    # Print counts for each of the 13 cases with new keys
    keys = [
        'name & scraped_name',
        'phone1 & business_phone',
        '(name & scraped_name) & (phone1 & business_phone)',
        'phone1 & mobile',
        '(name & scraped_name) & (phone1 & mobile)',
        'phone2 & business_phone',
        '(name & scraped_name) & (phone2 & business_phone)',
        'phone2 & mobile',
        '(name & scraped_name) & (phone2 & mobile)',
        '(phone1 & business_phone) & (phone2 & mobile)',
        '(name & scraped_name) & ((phone1 & business_phone) & (phone2 & mobile))',
        '(phone1 & mobile) & (phone2 & business_phone)',
        '(name & scraped_name) & ((phone1 & mobile) & (phone2 & business_phone))'
    ]
    print("Match counts for each case:")
    for key in keys:
        count = sum(r[key] for r in results)
        print(f"{key}: {count}")

    # Print statistics
    # count_name = sum(r['match_name'] for r in results)
    # count_name_phone1 = sum(r['match_name'] and r['match_phone1'] for r in results)
    # count_name_phone2 = sum(r['match_name'] and r['match_phone2'] for r in results)
    # count_all = sum(r['match_name'] and r['match_phone1'] and r['match_phone2'] for r in results)
    # count_phone1_mobile = sum(r['match_phone1_mobile'] for r in results)
    # count_all_with_mobile = sum(r['match_name'] and r['match_phone1'] and r['match_phone2'] and r['match_phone1_mobile'] for r in results)

    # print(f"match_name count: {count_name}")
    # print(f"match_name & match_phone1 count: {count_name_phone1}")
    # print(f"match_name & match_phone2 count: {count_name_phone2}")
    # print(f"match_name & match_phone1 & match_phone2 count: {count_all}")
    # print(f"match_phone1_mobile count: {count_phone1_mobile}")
    # print(f"match_name & match_phone1 & match_phone2 & match_phone1_mobile count: {count_all_with_mobile}")

if __name__ == '__main__':
    main()

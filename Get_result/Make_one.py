import json
import csv
import os
from collections import defaultdict

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def write_csv_file(data, file_path, fieldnames):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def process_files():
    base_dir = "Get_result/Seperated_data"
    result_dir = "Get_result/result"
    
    # Create result directory if it doesn't exist
    os.makedirs(result_dir, exist_ok=True)
    
    # Initialize dictionaries to store unique objects and their duplicates
    all_agents = {}
    detailed_agencies = {}
    detailed_agents = {}
    
    # Initialize dictionaries to track duplicates
    all_agents_duplicates = defaultdict(list)
    detailed_agencies_duplicates = defaultdict(list)
    detailed_agents_duplicates = defaultdict(list)
    
    # Statistics
    stats = {
        'all_agents': {'total': 0, 'unique': 0},
        'detailed_agencies': {'total': 0, 'unique': 0},
        'detailed_agents': {'total': 0, 'unique': 0}
    }
    
    # Process all files
    for i in range(2, 8):  # Files are numbered from 2 to 7
        # Process all_agent_key files
        agent_file = f"{base_dir}/all_agent_key=agent_{i}.json"
        if os.path.exists(agent_file):
            agents = read_json_file(agent_file)
            stats['all_agents']['total'] += len(agents)
            for agent in agents:
                key = agent.get('agent_name')
                if key:
                    if key in all_agents:
                        all_agents_duplicates[key].append({
                            'file': f"all_agent_key=agent_{i}.json",
                            'data': agent
                        })
                    else:
                        all_agents[key] = agent
        
        # Process detailed_agency files
        agency_json = f"{base_dir}/detailed_agency_{i}.json"
        if os.path.exists(agency_json):
            agencies = read_json_file(agency_json)
            stats['detailed_agencies']['total'] += len(agencies)
            for agency in agencies:
                key = agency.get('agencyId')
                if key:
                    if key in detailed_agencies:
                        detailed_agencies_duplicates[key].append({
                            'file': f"detailed_agency_{i}.json",
                            'data': agency
                        })
                    else:
                        detailed_agencies[key] = agency
        
        # Process detailed_agent files
        agent_json = f"{base_dir}/detailed_agent_{i}.json"
        if os.path.exists(agent_json):
            agents = read_json_file(agent_json)
            stats['detailed_agents']['total'] += len(agents)
            for agent in agents:
                key = agent.get('profile_id')
                if key:
                    if key in detailed_agents:
                        detailed_agents_duplicates[key].append({
                            'file': f"detailed_agent_{i}.json",
                            'data': agent
                        })
                    else:
                        detailed_agents[key] = agent
    
    # Update unique counts
    stats['all_agents']['unique'] = len(all_agents)
    stats['detailed_agencies']['unique'] = len(detailed_agencies)
    stats['detailed_agents']['unique'] = len(detailed_agents)
    
    # Write result files
    write_json_file(list(all_agents.values()), f"{result_dir}/all_agent_key=agent.json")
    write_json_file(list(detailed_agencies.values()), f"{result_dir}/detailed_agency_result.json")
    write_json_file(list(detailed_agents.values()), f"{result_dir}/detailed_agent_result.json")
    
    # Write CSV files
    if detailed_agencies:
        write_csv_file(list(detailed_agencies.values()), f"{result_dir}/detailed_agency_result.csv", 
                      fieldnames=list(detailed_agencies.values())[0].keys())
    if detailed_agents:
        write_csv_file(list(detailed_agents.values()), f"{result_dir}/detailed_agent_result.csv", 
                      fieldnames=list(detailed_agents.values())[0].keys())
    
    # Write duplicate files
    if all_agents_duplicates:
        write_json_file(dict(all_agents_duplicates), f"{result_dir}/all_agent_key_duplicates.json")
    if detailed_agencies_duplicates:
        write_json_file(dict(detailed_agencies_duplicates), f"{result_dir}/detailed_agency_duplicates.json")
    if detailed_agents_duplicates:
        write_json_file(dict(detailed_agents_duplicates), f"{result_dir}/detailed_agent_duplicates.json")
    
    # Print statistics
    print("\nProcessing Statistics:")
    print("\nAll Agents:")
    print(f"Total objects: {stats['all_agents']['total']}")
    print(f"Unique objects: {stats['all_agents']['unique']}")
    print(f"Duplicated objects: {stats['all_agents']['total'] - stats['all_agents']['unique']}")
    print(f"Number of objects with duplicates: {len(all_agents_duplicates)}")
    
    print("\nDetailed Agencies:")
    print(f"Total objects: {stats['detailed_agencies']['total']}")
    print(f"Unique objects: {stats['detailed_agencies']['unique']}")
    print(f"Duplicated objects: {stats['detailed_agencies']['total'] - stats['detailed_agencies']['unique']}")
    print(f"Number of objects with duplicates: {len(detailed_agencies_duplicates)}")
    
    print("\nDetailed Agents:")
    print(f"Total objects: {stats['detailed_agents']['total']}")
    print(f"Unique objects: {stats['detailed_agents']['unique']}")
    print(f"Duplicated objects: {stats['detailed_agents']['total'] - stats['detailed_agents']['unique']}")
    print(f"Number of objects with duplicates: {len(detailed_agents_duplicates)}")

if __name__ == "__main__":
    process_files()

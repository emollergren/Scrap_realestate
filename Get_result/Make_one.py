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
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, "Seperated_data")
    result_dir = os.path.join(current_dir, "result")
    
    print(f"Base directory: {base_dir}")
    print(f"Result directory: {result_dir}")
    
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
    
    # Initialize dictionaries to track file sources
    all_agents_sources = defaultdict(list)
    detailed_agencies_sources = defaultdict(list)
    detailed_agents_sources = defaultdict(list)
    
    # Statistics
    stats = {
        'all_agents': {'total': 0, 'unique': 0},
        'detailed_agencies': {'total': 0, 'unique': 0},
        'detailed_agents': {'total': 0, 'unique': 0}
    }
    
    # Process all files
    for i in range(1, 8):  # Files are numbered from 1 to 7
        # Process all_agent_key files
        agent_file = os.path.join(base_dir, f"all_agent_key=agent_{i}.json")
        if os.path.exists(agent_file):
            print(f"Processing {agent_file}")
            agents = read_json_file(agent_file)
            stats['all_agents']['total'] += len(agents)
            for agent in agents:
                key = agent.get('agent_name')
                if key:
                    all_agents_sources[key].append({
                        'file': f"all_agent_key=agent_{i}.json",
                        'data': agent
                    })
                    if key in all_agents:
                        all_agents_duplicates[key].append({
                            'file': f"all_agent_key=agent_{i}.json",
                            'data': agent
                        })
                    else:
                        all_agents[key] = agent
        else:
            print(f"File not found: {agent_file}")
        
        # Process detailed_agency files
        agency_json = os.path.join(base_dir, f"detailed_agency_{i}.json")
        if os.path.exists(agency_json):
            print(f"Processing {agency_json}")
            agencies = read_json_file(agency_json)
            stats['detailed_agencies']['total'] += len(agencies)
            for agency in agencies:
                key = agency.get('agencyId')
                if key:
                    detailed_agencies_sources[key].append({
                        'file': f"detailed_agency_{i}.json",
                        'data': agency
                    })
                    if key in detailed_agencies:
                        detailed_agencies_duplicates[key].append({
                            'file': f"detailed_agency_{i}.json",
                            'data': agency
                        })
                    else:
                        detailed_agencies[key] = agency
        else:
            print(f"File not found: {agency_json}")
        
        # Process detailed_agent files
        agent_json = os.path.join(base_dir, f"detailed_agent_{i}.json")
        if os.path.exists(agent_json):
            print(f"Processing {agent_json}")
            agents = read_json_file(agent_json)
            stats['detailed_agents']['total'] += len(agents)
            for agent in agents:
                key = agent.get('profile_id')
                if key:
                    detailed_agents_sources[key].append({
                        'file': f"detailed_agent_{i}.json",
                        'data': agent
                    })
                    if key in detailed_agents:
                        detailed_agents_duplicates[key].append({
                            'file': f"detailed_agent_{i}.json",
                            'data': agent
                        })
                    else:
                        detailed_agents[key] = agent
        else:
            print(f"File not found: {agent_json}")
    
    # Update unique counts
    stats['all_agents']['unique'] = len(all_agents)
    stats['detailed_agencies']['unique'] = len(detailed_agencies)
    stats['detailed_agents']['unique'] = len(detailed_agents)
    
    # Write result files
    write_json_file(list(all_agents.values()), os.path.join(result_dir, "all_agent_key=agent.json"))
    write_json_file(list(detailed_agencies.values()), os.path.join(result_dir, "detailed_agency_result.json"))
    write_json_file(list(detailed_agents.values()), os.path.join(result_dir, "detailed_agent_result.json"))
    
    # Write CSV files
    if detailed_agencies:
        write_csv_file(list(detailed_agencies.values()), os.path.join(result_dir, "detailed_agency_result.csv"), 
                      fieldnames=list(detailed_agencies.values())[0].keys())
    if detailed_agents:
        write_csv_file(list(detailed_agents.values()), os.path.join(result_dir, "detailed_agent_result.csv"), 
                      fieldnames=list(detailed_agents.values())[0].keys())
    
    # Write duplicate files with all occurrences
    if all_agents_sources:
        # Filter only entries that appear in multiple files
        all_agents_duplicates = {k: v for k, v in all_agents_sources.items() if len(v) > 1}
        write_json_file(all_agents_duplicates, os.path.join(result_dir, "all_agent_key_duplicates.json"))
    
    if detailed_agencies_sources:
        # Filter only entries that appear in multiple files
        detailed_agencies_duplicates = {k: v for k, v in detailed_agencies_sources.items() if len(v) > 1}
        write_json_file(detailed_agencies_duplicates, os.path.join(result_dir, "detailed_agency_duplicates.json"))
    
    if detailed_agents_sources:
        # Filter only entries that appear in multiple files
        detailed_agents_duplicates = {k: v for k, v in detailed_agents_sources.items() if len(v) > 1}
        write_json_file(detailed_agents_duplicates, os.path.join(result_dir, "detailed_agent_duplicates.json"))
    
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

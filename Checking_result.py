import json
import os
from collections import defaultdict

def read_json_file(file_path):
    """Read and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

def check_agent_data():
    """Check if all agents in result files exist in detailed data"""
    print("\nChecking Agent Data...")
    
    # Read result files
    result_agents = read_json_file("Get_result/result/all_agent_key=agent.json")
    detailed_agents = read_json_file("Get_result/result/detailed_agent_result.json")
    
    if not result_agents or not detailed_agents:
        print("Error: Could not read result files")
        return
    
    # Create sets of identifiers
    result_agent_names = {agent['agent_name'] for agent in result_agents}
    detailed_agent_ids = {agent['profile_id'] for agent in detailed_agents}
    
    # Check detailed agent files
    detailed_dir = "Get_detail_agent/Detailed_agent_data"
    if not os.path.exists(detailed_dir):
        print(f"Error: Directory {detailed_dir} does not exist")
        return
    
    # Get all JSON files in detailed directory
    detailed_files = [f for f in os.listdir(detailed_dir) if f.endswith('.json')]
    
    # Track missing and found files
    missing_files = []
    found_files = []
    
    # Check each detailed agent file
    for file in detailed_files:
        file_path = os.path.join(detailed_dir, file)
        agent_data = read_json_file(file_path)
        
        if agent_data:
            profile_id = agent_data.get('agent_profile', {}).get('profile_id')
            if profile_id in detailed_agent_ids:
                found_files.append(file)
            else:
                missing_files.append(file)
    
    # Print results
    print(f"\nTotal agents in result file: {len(result_agent_names)}")
    print(f"Total agents in detailed result: {len(detailed_agent_ids)}")
    print(f"Total detailed agent files: {len(detailed_files)}")
    print(f"Found matching files: {len(found_files)}")
    print(f"Missing matching files: {len(missing_files)}")
    
    if missing_files:
        print("\nMissing files:")
        for file in missing_files[:10]:  # Show first 10 missing files
            print(f"- {file}")
        if len(missing_files) > 10:
            print(f"... and {len(missing_files) - 10} more")

def check_agency_data():
    """Check if all agencies in result files exist in detailed data"""
    print("\nChecking Agency Data...")
    
    # Read result files
    detailed_agencies = read_json_file("Get_result/result/detailed_agency_result.json")
    
    if not detailed_agencies:
        print("Error: Could not read agency result file")
        return
    
    # Create set of agency IDs
    detailed_agency_ids = {agency['agencyId'] for agency in detailed_agencies}
    
    # Check detailed agency files
    detailed_dir = "Get_detail_agent/Detailed_agency_data"
    if not os.path.exists(detailed_dir):
        print(f"Error: Directory {detailed_dir} does not exist")
        return
    
    # Get all JSON files in detailed directory
    detailed_files = [f for f in os.listdir(detailed_dir) if f.endswith('.json')]
    
    # Track missing and found files
    missing_files = []
    found_files = []
    
    # Check each detailed agency file
    for file in detailed_files:
        file_path = os.path.join(detailed_dir, file)
        agency_data = read_json_file(file_path)
        
        if agency_data:
            agency_id = agency_data.get('agencyId')
            if agency_id in detailed_agency_ids:
                found_files.append(file)
            else:
                missing_files.append(file)
    
    # Print results
    print(f"\nTotal agencies in detailed result: {len(detailed_agency_ids)}")
    print(f"Total detailed agency files: {len(detailed_files)}")
    print(f"Found matching files: {len(found_files)}")
    print(f"Missing matching files: {len(missing_files)}")
    
    if missing_files:
        print("\nMissing files:")
        for file in missing_files[:10]:  # Show first 10 missing files
            print(f"- {file}")
        if len(missing_files) > 10:
            print(f"... and {len(missing_files) - 10} more")

def check_duplicates():
    """Check for any duplicate entries in the result files"""
    print("\nChecking for Duplicates...")
    
    # Check agent duplicates
    agent_duplicates = read_json_file("Get_result/result/detailed_agent_duplicates.json")
    if agent_duplicates:
        print(f"\nAgent Duplicates: {len(agent_duplicates)} entries")
        for key, duplicates in list(agent_duplicates.items())[:5]:  # Show first 5 duplicates
            print(f"- {key}: {len(duplicates)} duplicates")
        if len(agent_duplicates) > 5:
            print(f"... and {len(agent_duplicates) - 5} more")
    
    # Check agency duplicates
    agency_duplicates = read_json_file("Get_result/result/detailed_agency_duplicates.json")
    if agency_duplicates:
        print(f"\nAgency Duplicates: {len(agency_duplicates)} entries")
        for key, duplicates in list(agency_duplicates.items())[:5]:  # Show first 5 duplicates
            print(f"- {key}: {len(duplicates)} duplicates")
        if len(agency_duplicates) > 5:
            print(f"... and {len(agency_duplicates) - 5} more")

def main():
    print("Starting Data Consistency Check...")
    
    # Check agent data
    check_agent_data()
    
    # Check agency data
    check_agency_data()
    
    # Check duplicates
    check_duplicates()
    
    print("\nData Consistency Check Complete!")

if __name__ == "__main__":
    main()

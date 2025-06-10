import json
from collections import defaultdict
import csv

# Read the agents data
with open("Agents.json", "r", encoding="utf-8") as f:
    regions = json.load(f)

# Dictionary to store unique agents with their regions
unique_agents = {}

# Process each region and its agents
for region in regions:
    region_info = {
        "region_name": region["name"],
        "region_state": region["state"],
        "region_id": region["id"]
    }
    
    for agent in region.get('agents', []):
        agent_name = agent['agent_name']
        
        if agent_name not in unique_agents:
            # Create new agent entry
            agent_data = agent.copy()
            agent_data['region'] = [region_info]
            unique_agents[agent_name] = agent_data
        else:
            # Add region to existing agent's regions list
            unique_agents[agent_name]['region'].append(region_info)

# Convert dictionary to list of agents
unique_agents_list = list(unique_agents.values())

# Save to JSON file
with open("all_agent_key=agent.json", "w", encoding="utf-8") as f:
    json.dump(unique_agents_list, f, indent=4, ensure_ascii=False)

# Save to CSV file
with open("all_agent_key=agent.csv", "w", newline='', encoding='utf-8') as f:
    # Get all possible fields from the first agent
    if unique_agents_list:
        fieldnames = list(unique_agents_list[0].keys())
        # Move 'region' to the end
        fieldnames.remove('region')
        fieldnames.append('region')
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for agent in unique_agents_list:
            # Create a copy of the agent data
            row_data = agent.copy()
            # Convert region list to JSON string
            row_data['region'] = json.dumps(row_data['region'], ensure_ascii=False)
            writer.writerow(row_data)

# Print summary
print(f"\nProcessing Complete:")
print(f"Total unique agents: {len(unique_agents_list)}")

# Count agents with multiple regions
multi_region_agents = sum(1 for agent in unique_agents_list if len(agent['region']) > 1)
print(f"Agents appearing in multiple regions: {multi_region_agents}")

# Print some example agents with multiple regions
print("\nExample agents with multiple regions:")
for agent in unique_agents_list:
    if len(agent['region']) > 1:
        print(f"\nAgent: {agent['agent_name']}")
        print(f"Appears in {len(agent['region'])} regions:")
        for region in agent['region']:
            print(f"- {region['region_name']} ({region['region_state']})")
        break  # Just show one example

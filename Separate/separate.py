import json
import math
import os

def separate_agents(input_file, num_files=7):
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        agents = json.load(f)
    
    # Calculate number of agents per file
    total_agents = len(agents)
    print("All Agents:", total_agents)
    agents_per_file = math.ceil(total_agents / num_files)
    
    # Split agents into groups and save to separate files
    for i in range(num_files):
        start_idx = i * agents_per_file
        end_idx = min((i + 1) * agents_per_file, total_agents)
        
        # Get the group of agents for this file
        agent_group = agents[start_idx:end_idx]
        
        # Create output filename in the same directory
        output_file = f'all_agent_key=agent_{i+1}.json'
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(agent_group, f, indent=4, ensure_ascii=False)
        
        print(f"Created {output_file} with {len(agent_group)} agents")

if __name__ == "__main__":
    input_file = "all_agent_key=agent_remain.json"
    separate_agents(input_file)

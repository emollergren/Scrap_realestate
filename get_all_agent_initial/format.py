import json
from collections import Counter

# Read the agents data
with open("Agents.json", "r", encoding="utf-8") as f:
    regions = json.load(f)

# Collect all agent names
all_agents = []
for region in regions:
    for agent in region.get('agents', []):
        all_agents.append(agent['agent_name'])

# Count total agents
total_agents = len(all_agents)

# Count unique agents
unique_agents = len(set(all_agents))

# Find duplicated agents
agent_counts = Counter(all_agents)
duplicated_agents = {name: count for name, count in agent_counts.items() if count > 1}

# Print results
print(f"\nAnalysis Results:")
print(f"Total number of agents: {total_agents}")
print(f"Number of unique agents: {unique_agents}")
print(f"Number of duplicated agents: {len(duplicated_agents)}")

# Print detailed information about duplicates
if duplicated_agents:
    print("\nDetailed Duplicate Information:")
    for name, count in duplicated_agents.items():
        print(f"Agent '{name}' appears {count} times")

# Save the analysis results to a file
analysis_results = {
    "total_agents": total_agents,
    "unique_agents": unique_agents,
    "duplicated_agents_count": len(duplicated_agents),
    "duplicated_agents_details": duplicated_agents
}

with open("agent_analysis.json", "w", encoding="utf-8") as f:
    json.dump(analysis_results, f, indent=4, ensure_ascii=False)
print("\nAnalysis results saved to agent_analysis.json")
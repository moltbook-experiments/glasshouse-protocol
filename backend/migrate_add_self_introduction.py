#!/usr/bin/env python3
"""
Migration script to add self_introduction field to existing agent records.
This script reads the agents.jsonl file, adds the self_introduction field to each record,
and writes it back.
"""

import json
import os
import sys
from datetime import datetime

def migrate_agents(agents_file_path):
    """Add self_introduction field to all agent records."""
    
    if not os.path.exists(agents_file_path):
        print(f"Error: {agents_file_path} not found")
        return False
    
    # Read all agent records
    agents = []
    try:
        with open(agents_file_path, 'r') as f:
            for line in f:
                if line.strip():
                    agents.append(json.loads(line))
    except Exception as e:
        print(f"Error reading agents file: {e}")
        return False
    
    if not agents:
        print("No agents found in file")
        return True
    
    # Create backup
    backup_file = f"{agents_file_path}.backup.{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    try:
        with open(agents_file_path, 'r') as src:
            with open(backup_file, 'w') as dst:
                dst.write(src.read())
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
    
    # Migrate records
    migrated_count = 0
    for agent in agents:
        if 'self_introduction' not in agent:
            agent['self_introduction'] = ""
            migrated_count += 1
    
    # Write back
    try:
        with open(agents_file_path, 'w') as f:
            for agent in agents:
                f.write(json.dumps(agent) + "\n")
        print(f"Migration successful: {migrated_count} agents updated")
        print(f"Total agents: {len(agents)}")
        return True
    except Exception as e:
        print(f"Error writing agents file: {e}")
        return False

if __name__ == "__main__":
    # Get the agents file path
    if len(sys.argv) > 1:
        agents_file = sys.argv[1]
    else:
        # Default to backend/data/agents.jsonl relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        agents_file = os.path.join(script_dir, "..", "data", "agents.jsonl")
    
    agents_file = os.path.abspath(agents_file)
    print(f"Migrating agents file: {agents_file}")
    
    success = migrate_agents(agents_file)
    sys.exit(0 if success else 1)

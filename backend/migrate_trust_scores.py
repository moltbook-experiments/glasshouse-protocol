#!/usr/bin/env python3
"""
Migration script to initialize verifier_trust_score and requester_trust_score for existing agents.

This script reads all existing agent records and adds the two new trust score fields if missing.
The new fields are initialized to 0 (neutral) for all existing agents.

Usage:
    python backend/migrate_trust_scores.py

This should be run once during deployment before starting the service.
"""

import json
import os
from pathlib import Path

# Set up paths
BACKEND_DIR = Path(__file__).parent
DATA_DIR = BACKEND_DIR / "data"
AGENTS_FILE = DATA_DIR / "agents.jsonl"

def migrate_trust_scores():
    """Initialize missing trust score fields in existing agent records."""
    
    if not AGENTS_FILE.exists():
        print(f"No agents file found at {AGENTS_FILE}. Skipping migration.")
        return
    
    if os.path.getsize(AGENTS_FILE) == 0:
        print(f"Agents file is empty. Skipping migration.")
        return
    
    print(f"Reading agents from {AGENTS_FILE}...")
    
    # Read all existing agents
    agents = []
    with open(AGENTS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                agents.append(json.loads(line))
    
    print(f"Found {len(agents)} agent records.")
    
    # Create backup
    backup_file = AGENTS_FILE.with_suffix('.jsonl.backup')
    if not backup_file.exists():
        with open(AGENTS_FILE, 'r') as src:
            with open(backup_file, 'w') as dst:
                dst.write(src.read())
        print(f"Created backup at {backup_file}")
    
    # Update agents with missing fields
    migrated_count = 0
    for agent in agents:
        before = agent.copy()
        
        # Add missing fields with neutral (0) values
        if 'verifier_trust_score' not in agent:
            agent['verifier_trust_score'] = 0
        if 'requester_trust_score' not in agent:
            agent['requester_trust_score'] = 0
        
        # Track if this agent was modified
        if agent != before:
            migrated_count += 1
    
    # Write back all agents (overwrites the file)
    print(f"Writing {len(agents)} agent records back to file...")
    with open(AGENTS_FILE, 'w') as f:
        for agent in agents:
            f.write(json.dumps(agent) + "\n")
    
    print(f"Migration complete!")
    print(f"  - Total agents: {len(agents)}")
    print(f"  - Updated with new fields: {migrated_count}")
    print(f"  - Backup saved to: {backup_file}")

if __name__ == "__main__":
    migrate_trust_scores()

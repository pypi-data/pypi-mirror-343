"""
Example showing how to list stored teams and switch between them
"""

import sys
import os
import time
from typing import Any, Dict, List

# Add the parent directory to the path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agentds.client import BenchmarkClient


def main():
    """
    Main function demonstrating team switching functionality.
    """
    # Check if token exists and output that information
    token_file = os.path.expanduser("~/.agentds_token")
    if os.path.exists(token_file):
        print(f"Found saved credentials in {token_file}")
    else:
        print(f"No saved credentials found at {token_file}")
        print("Please run simple_client.py first to authenticate at least one team.")
        return

    # List all stored teams
    teams = BenchmarkClient.list_stored_teams()
    if not teams:
        print("No teams found in token file.")
        print("Please run simple_client.py first to authenticate at least one team.")
        return

    print(f"Found {len(teams)} stored teams: {', '.join(teams)}")
    
    # Create client with no arguments to auto-load the default team
    client = BenchmarkClient()
    if client.is_authenticated:
        print(f"Auto-authenticated as team: {client.team_name}")
        
        # Get status for current team
        status = client.get_status()
        if isinstance(status, dict):
            print(f"Competition status: {status.get('status', 'unknown')}")
    else:
        print("Failed to auto-authenticate. Your token file may be corrupted.")
        return
    
    # If there are multiple teams, demonstrate switching
    if len(teams) > 1:
        # Select a different team (not the current one)
        other_team = next((t for t in teams if t != client.team_name), None)
        if other_team:
            print(f"\nSwitching to team: {other_team}")
            success = BenchmarkClient.switch_team(other_team)
            
            if success:
                # Create a new client to use the switched team
                new_client = BenchmarkClient()
                if new_client.is_authenticated:
                    print(f"Now authenticated as team: {new_client.team_name}")
                    
                    # Get status for new team
                    status = new_client.get_status()
                    if isinstance(status, dict):
                        print(f"Competition status: {status.get('status', 'unknown')}")
                else:
                    print("Failed to authenticate after switching teams.")
            else:
                print(f"Failed to switch to team {other_team}")
    else:
        print("\nOnly one team found. To demonstrate switching, authenticate another team first.")
        
    print("\nDone! You can modify this example to add more teams or switch between them.")


if __name__ == "__main__":
    main() 
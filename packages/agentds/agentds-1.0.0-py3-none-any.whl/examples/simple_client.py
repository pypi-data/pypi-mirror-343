"""
Simple example of using the BenchmarkClient
"""

import sys
import os
import time
from typing import Any, Dict, List

# Add the parent directory to the path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agentds.client import BenchmarkClient
from agentds.task import Task


def simple_agent(task: Task) -> Any:
    """
    A very simple agent that just returns the task data.
    In a real agent, this would be where you perform your data science tasks.
    
    Args:
        task: The task to complete
        
    Returns:
        The response to the task
    """
    print(f"\nWorking on task: #{task.task_number} (Domain: {task.domain}, Category: {task.category})")
    print(f"Instructions: {task.get_instructions()}")
    
    # In a real agent, you would analyze the data and produce a response
    # For this simple example, we just return the data if it's a dict or list,
    # or a dummy response otherwise
    data = task.get_data()
    
    if isinstance(data, (dict, list)):
        print("Returning the task data as response")
        return data
    else:
        print("Returning a dummy response")
        return {"result": "Example response", "confidence": 0.9}


def main():
    """
    Main function that demonstrates the use of the BenchmarkClient.
    """
    # Check if token exists and output that information
    token_file = os.path.expanduser("~/.agentds_token")
    if os.path.exists(token_file):
        print(f"Found saved credentials in {token_file}")
        print("Will attempt to use saved credentials first")
    
    # Create client with no arguments to attempt auto-loading credentials
    client = BenchmarkClient()
    
    # Check if auto-authentication worked
    if client.is_authenticated:
        print(f"Auto-authenticated using saved credentials for team: {client.team_name}")
    else:
        # If auto-authentication failed, ask for credentials
        print("No valid saved credentials found. Manual authentication required.")
        api_key = os.environ.get("AGENTDS_API_KEY") or input("Enter your API key: ")
        team_name = os.environ.get("AGENTDS_TEAM_NAME") or input("Enter your team name: ")
        
        # Now authenticate with the provided credentials
        client = BenchmarkClient(api_key, team_name)
        if not client.authenticate():
            print("Authentication failed. Please check your API key and team name.")
            return
        else:
            print(f"Successfully authenticated and saved credentials to {token_file}")
            print("Future runs will auto-authenticate using these credentials")
    
    # Start the competition if not already started
    status = client.get_status()
    if isinstance(status, dict):
        status_value = status.get("status", "unknown")
        if status_value == "inactive":
            print("Starting the competition...")
            client.start_competition()
        elif status_value == "completed":
            print("Competition already completed!")
            return
        elif status_value == "error":
            print(f"Error getting competition status: {status.get('message', 'Unknown error')}")
        else:
            print(f"Competition status: {status_value}")
    else:
        print(f"Competition status: {status}")
    
    # Get available domains
    domains = client.get_domains()
    if not domains:
        print("No domains available.")
        return
    
    print(f"Available domains: {domains}")
    
    # Process one task from each domain as an example
    for domain in domains[:2]:
        print(f"\nProcessing domain: {domain}")
        
        # Get the next task for this domain
        task = client.get_next_task(domain)
        if not task:
            print(f"No task available for domain {domain}.")
            continue
        
        # Process the task with our simple agent
        response = simple_agent(task)
        
        # Validate the response
        if task.validate_response(response):
            print("Response validation successful, submitting...")
            
            # Submit the response
            success = client.submit_response(domain, task.task_number, response)
            if success:
                print("Response submitted successfully!")
            else:
                print("Failed to submit response.")
        else:
            print("Response validation failed. Please check the response format.")
        
        # Add a small delay between tasks
        time.sleep(1)
    
    print("\nExample completed!")


if __name__ == "__main__":
    main() 
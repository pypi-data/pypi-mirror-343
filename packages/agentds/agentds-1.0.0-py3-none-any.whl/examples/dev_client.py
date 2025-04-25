"""
Development mode example for testing the client without a backend
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
    Main function that demonstrates the use of the BenchmarkClient in dev mode.
    """
    print("=== RUNNING CLIENT IN DEV MODE ===")
    print("This allows testing without a backend server")
    
    # Hard-coded credentials for testing
    api_key = "test-api-key"
    team_name = "test-team"
    
    # Create client in dev mode
    client = BenchmarkClient(api_key, team_name, dev_mode=True)
    print(f"Dev client created with team: {team_name}")
    
    # Check authentication status
    if client.is_authenticated:
        print("Client is authenticated (simulated in dev mode)")
    else:
        print("Authentication failed even in dev mode. Check your code.")
        return
    
    # Get competition status
    status = client.get_status()
    print(f"Competition status: {status.get('status')}")
    
    # In dev mode, we'll use hardcoded domains for testing
    domains = ['Wine-Quality', 'Housekeeping', 'Diabetes', 'Titanic']
    print(f"Available domains: {domains}")
    
    # Create a simulated task
    print("\nCreating a simulated task for testing")
    task = Task(
        task_number=1,
        domain="Wine-Quality",
        category="Classification",
        data={"features": [1, 2, 3, 4], "target": [0, 1, 0, 1]},
        instructions="Predict wine quality using the given features",
        side_info={"scoring": "accuracy"},
        response_format={"predictions": [0, 1, 0, 1]},
        test_size=4
    )
    
    # Process the task with our simple agent
    response = simple_agent(task)
    
    # Validate the response
    if task.validate_response(response):
        print("Response validation successful")
    else:
        print("Response validation failed. Please check the response format.")
    
    print("\nDev mode example completed!")


if __name__ == "__main__":
    main() 
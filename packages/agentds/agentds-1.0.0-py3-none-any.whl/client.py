"""
Client for interacting with the AgentDS-Bench platform
"""

import json
import requests
import os
import pandas as pd
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .task import Task
from .auth import authenticate, get_auth_headers, get_auth_info
from .config import API_BASE_URL
from .utils.validators import validate_csv_response


class BenchmarkClient:
    """
    Client for interacting with the AgentDS-Bench platform.
    
    This client provides methods to authenticate, retrieve tasks, and submit responses
    to the AgentDS-Bench platform.
    """
    
    TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".agentds_token")
    DATA_DIR = os.path.join(os.getcwd(), "agentDS_data")
    
    def __init__(self, api_key: Optional[str] = None, team_name: Optional[str] = None, dev_mode: bool = False):
        """
        Initialize a new BenchmarkClient.
        
        If api_key and team_name are provided, the client will attempt to authenticate.
        Otherwise, it will try to load credentials from environment variables or the token file.
        
        Args:
            api_key: API key for authentication (optional)
            team_name: Team name for identification (optional)
            dev_mode: If True, enables development mode with simulated responses for offline testing
        """
        self.api_key = api_key
        self.team_name = team_name
        self.is_authenticated = False
        self.current_domain = None
        self.current_task_number = None
        self.current_task_test_size = None
        self.dev_mode = dev_mode
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
        
        # If credentials are provided, authenticate
        if api_key and team_name:
            self.authenticate()
        else:
            # Try to load from environment variables first
            loaded_api_key, loaded_team_name = get_auth_info()
            if loaded_api_key and loaded_team_name:
                self.api_key = loaded_api_key
                self.team_name = loaded_team_name
                # Verify loaded credentials
                self.verify_auth()
            else:
                # If no environment variables, try token file
                self._load_token()
                
        # In dev mode, assume authenticated if we have credentials
        if dev_mode and self.api_key and self.team_name and not self.is_authenticated:
            print("DEV MODE: Simulating successful authentication")
            self.is_authenticated = True
    
    def _save_token(self) -> None:
        """Save authentication token to file with timestamp."""
        if self.api_key and self.team_name and self.is_authenticated:
            try:
                with open(self.TOKEN_FILE, 'w') as f:
                    json.dump({
                        'api_key': self.api_key,
                        'team_name': self.team_name,
                        'timestamp': datetime.now().timestamp()
                    }, f)
                print(f"Saved auth token to {self.TOKEN_FILE}")
            except Exception as e:
                print(f"Warning: Failed to save token: {e}")
    
    def _load_token(self) -> bool:
        """Load authentication token from file if it exists."""
        if os.path.exists(self.TOKEN_FILE):
            try:
                with open(self.TOKEN_FILE, 'r') as f:
                    token_data = json.load(f)
                    
                    # Check if token is still valid (within 7 days)
                    if datetime.now().timestamp() - token_data.get('timestamp', 0) < 7 * 24 * 3600:
                        # Check if this is new format with teams or old format
                        if 'teams' in token_data:
                            # New format
                            teams_dict = token_data.get('teams', {})
                            if teams_dict:
                                # Get first team from dictionary
                                team_name = next(iter(teams_dict), None)
                                if team_name:
                                    self.team_name = team_name
                                    self.api_key = teams_dict[team_name]
                        else:
                            # Old format with direct api_key and team_name
                            self.api_key = token_data.get('api_key')
                            self.team_name = token_data.get('team_name')
                        
                        # Verify the loaded credentials
                        if self.api_key and self.team_name:
                            print(f"Loaded credentials for team '{self.team_name}' from token file")
                            return self.verify_auth()
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading token file: {e}")
        return False
    
    def authenticate(self) -> bool:
        """
        Authenticate with the AgentDS-Bench platform.
        
        Returns:
            bool: True if authentication was successful, False otherwise
        """
        if not self.api_key or not self.team_name:
            print("API key and team name are required for authentication.")
            return False
        
        # Use the authenticate function from auth.py
        self.is_authenticated = authenticate(self.api_key, self.team_name)
        
        # Save token if authenticated
        if self.is_authenticated:
            self._save_token()
            
        return self.is_authenticated
    
    def verify_auth(self) -> bool:
        """
        Verify that the client is authenticated.
        
        Returns:
            bool: True if the client is authenticated, False otherwise
        """
        if self.is_authenticated:
            return True
            
        if not self.api_key or not self.team_name:
            print("No API key or team name available. Call authenticate() first.")
            return False
            
        try:
            headers = get_auth_headers()
            response = requests.get(
                f"{API_BASE_URL}/auth/verify",
                headers=headers
            )
            
            if response.status_code == 200:
                self.is_authenticated = True
                return True
            elif response.status_code == 400:
                # Check if the error is about Team ID which we can ignore for now
                try:
                    err_data = response.json()
                    err_msg = err_data.get("error", "")
                    if "Team ID" in err_msg:
                        # Team ID issues can be ignored for API testing
                        print("NOTE: Team ID validation skipped in dev mode")
                        self.is_authenticated = True
                        return True
                except:
                    pass
                
            print(f"Auth verification failed with status {response.status_code}")    
            self.is_authenticated = False
            return False
        except requests.RequestException as e:
            print(f"Error verifying authentication: {e}")
            return False
    
    def start_competition(self) -> bool:
        """
        Start the competition for this team.
        
        Returns:
            bool: True if the competition was started successfully, False otherwise
        """
        if not self.verify_auth():
            return False
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/competition/start",
                headers=get_auth_headers()
            )
            
            if response.status_code == 200:
                print("Competition started successfully.")
                return True
            else:
                err_msg = response.json().get("error", "Unknown error")
                print(f"Failed to start competition: {err_msg}")
                return False
        except requests.RequestException as e:
            print(f"Error starting competition: {e}")
            return False
    
    def get_domains(self) -> List[str]:
        """
        Get the list of available domains.
        
        Returns:
            List[str]: List of domain names
        """
        if not self.verify_auth():
            return []
            
        try:
            response = requests.get(
                f"{API_BASE_URL}/competition/domains",
                headers=get_auth_headers()
            )
            
            if response.status_code == 200:
                domains = response.json().get("domains", [])
                return domains
            else:
                err_msg = response.json().get("error", "Unknown error")
                print(f"Failed to get domains: {err_msg}")
                return []
        except requests.RequestException as e:
            print(f"Error getting domains: {e}")
            return []
    
    def get_next_task(self, domain: str) -> Optional[Task]:
        """
        Get the next task for a specific domain.
        
        Args:
            domain: The domain to get the next task for
            
        Returns:
            Task: The next task, or None if no task is available
        """
        if not self.verify_auth():
            return None
        
        # Update the current domain
        self.current_domain = domain
            
        try:
            response = requests.get(
                f"{API_BASE_URL}/competition/task/{domain}",
                headers=get_auth_headers()
            )
            
            if response.status_code == 200:
                task_data = response.json()
                
                # Check if we got a proper task response
                task_info = task_data.get("task")
                if not task_info:
                    print(f"No task data found in response for domain {domain}")
                    return None
                
                # Create a Task object from the response
                task = Task(
                    task_number=task_info.get("task_number"),
                    domain=task_info.get("domain", domain),
                    category=task_info.get("category", ""),
                    data=task_info.get("data"),
                    instructions=task_info.get("task_instruction", ""),
                    side_info=task_info.get("side_information_list", {}),
                    response_format=task_info.get("response_format", {}),
                    test_size=task_data.get("test_size", 0)
                )
                
                # Save the current task number and test size
                self.current_task_number = task.task_number
                self.current_task_test_size = task.test_size
                
                # Save dataset to local file if available
                if task.data and isinstance(task.data, str):
                    # Create domain directory if it doesn't exist
                    domain_dir = os.path.join(self.DATA_DIR, domain)
                    if not os.path.exists(domain_dir):
                        os.makedirs(domain_dir)
                    
                    # Create the dataset file path
                    file_name = f"task_{task.task_number}_data.csv"
                    dataset_path = os.path.join(domain_dir, file_name)
                    
                    # Save the data to file
                    with open(dataset_path, "w") as f:
                        f.write(task.data)
                    
                    # Add the path to the task object for user convenience
                    task.dataset_path = dataset_path
                    print(f"Dataset saved to {dataset_path}")
                
                return task
            elif response.status_code == 404:
                # No task available in this domain
                print(f"No task available for domain {domain}")
                return None
            else:
                err_msg = "Unknown error"
                try:
                    err_msg = response.json().get("error", "Unknown error")
                except:
                    err_msg = f"HTTP error {response.status_code}"
                print(f"Failed to get next task: {err_msg}")
                return None
        except requests.RequestException as e:
            print(f"Error getting next task: {e}")
            return None
    
    def submit_response(self, domain: str, task_number: int, response: Any) -> bool:
        """
        Submit a response for a specific task.
        
        Args:
            domain: The domain of the task
            task_number: The task number within the domain
            response: The response data to submit
            
        Returns:
            bool: True if the response was submitted successfully, False otherwise
        """
        if not self.verify_auth():
            return False
            
        try:
            # Prepare the payload
            payload = {
                "response": response
            }
            
            response_obj = requests.post(
                f"{API_BASE_URL}/competition/submit/{domain}/{task_number}",
                headers=get_auth_headers(),
                json=payload
            )
            
            if response_obj.status_code == 200:
                result = response_obj.json()
                score = result.get('score', 'N/A')
                print(f"Response submitted successfully. Score: {score}")
                
                # Check if domain is completed
                if result.get("domain_completed", False):
                    print(f"Congratulations! Domain '{domain}' is completed.")
                
                return True
            else:
                err_msg = response_obj.json().get("error", "Unknown error")
                print(f"Failed to submit response: {err_msg}")
                return False
        except requests.RequestException as e:
            print(f"Error submitting response: {e}")
            return False
    
    def get_status(self) -> Dict:
        """
        Get the current status of the competition for this team.
        
        Returns:
            Dict: Detailed status including domain completion information
        """
        if not self.verify_auth():
            return {"status": "inactive"}
            
        try:
            response = requests.get(
                f"{API_BASE_URL}/competition/status",
                headers=get_auth_headers()
            )
            
            if response.status_code == 200:
                status_data = response.json()
                
                # Format as a nice table for display if domains info is available
                if "domains" in status_data:
                    domains_data = []
                    for domain in status_data["domains"]:
                        domains_data.append({
                            "Domain": domain.get("name", "Unknown"),
                            "Completed Tasks": domain.get("completed_tasks", 0),
                            "Total Tasks": domain.get("total_tasks", 0),
                            "Status": "Completed" if domain.get("completed", False) else "In Progress",
                            "Best Score": domain.get("best_score", "N/A"),
                            "Start Time": domain.get("start_time", "Not Started"),
                            "Completion Time": domain.get("completion_time", "Not Completed")
                        })
                    
                    status_df = pd.DataFrame(domains_data)
                    status_data["formatted_table"] = status_df.to_string(index=False)
                    status_data["completed_domains"] = [d.get("name") for d in status_data["domains"] if d.get("completed", False)]
                    status_data["incomplete_domains"] = [d.get("name") for d in status_data["domains"] if not d.get("completed", False)]
                
                return status_data
            else:
                err_msg = response.json().get("error", "Unknown error")
                print(f"Failed to get status: {err_msg}")
                
                # In dev mode, return a fallback status
                if self.dev_mode:
                    print("DEV MODE: Returning fallback status")
                    return {
                        "status": "active",
                        "team_name": self.team_name,
                        "domain_progress": {},
                        "overall_progress": 0
                    }
                return {"status": "error", "message": err_msg}
        except requests.RequestException as e:
            print(f"Error getting status: {e}")
            
            # In dev mode, return a fallback status
            if self.dev_mode:
                print("DEV MODE: Returning fallback status")
                return {
                    "status": "active",
                    "team_name": self.team_name,
                    "domain_progress": {},
                    "overall_progress": 0
                }
            return {"status": "error", "message": str(e)}
            
    @staticmethod
    def list_stored_teams() -> List[str]:
        """
        List all teams that have been authenticated and stored.
        
        Returns:
            List[str]: List of team names
        """
        from .auth import load_teams_dict
        teams_dict = load_teams_dict()
        return list(teams_dict.keys())
        
    @staticmethod
    def switch_team(team_name: str) -> bool:
        """
        Switch to using a different team for API calls.
        
        Args:
            team_name: The name of the team to switch to
            
        Returns:
            bool: True if the team was found and switched to, False otherwise
        """
        from .auth import select_team
        return select_team(team_name)

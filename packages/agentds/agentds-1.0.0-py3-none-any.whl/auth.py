# TODO: Track and manage API call limits and membership

import os
import requests
from typing import Optional, Tuple, Dict, List
from .config import API_BASE_URL, TOKEN_FILE

def authenticate(api_key: str, team_name: str) -> bool:
    """
    Authenticates a team with the AgentDS-Bench platform using API key.
    
    Args:
        api_key: The API key generated for the team
        team_name: The name of the team
    
    Returns:
        bool: True if authentication was successful, False otherwise
    """
    # Save API key and team name to environment variables for current session
    os.environ["AGENTDS_API_KEY"] = api_key
    os.environ["AGENTDS_TEAM_NAME"] = team_name
    
    # Verify with the server
    if verify_api_key(api_key, team_name):
        # Load existing teams dictionary or create new one
        teams_dict = load_teams_dict()
        
        # Add or update this team
        teams_dict[team_name] = api_key
        
        # Save updated teams dictionary
        save_teams_dict(teams_dict)
        return True
    
    return False


def verify_api_key(api_key: str, team_name: str) -> bool:
    """
    Verifies the API key with the server.
    
    Args:
        api_key: The API key to verify
        team_name: The name of the team associated with the API key
    
    Returns:
        bool: True if verification was successful, False otherwise
    """
    # Use the correct header format that backend expects (X-API-Key)
    headers = {
        "X-API-Key": api_key,
        "X-Team-Name": team_name,
        "X-Team-ID": "placeholder"  # Add placeholder for Team ID since it's required by the backend
    }
    
    try:
        print(f"AGENTDS AUTH: Attempting to connect to {API_BASE_URL}/auth/verify")
        response = requests.post(
            f"{API_BASE_URL}/auth/verify", 
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"Successfully authenticated team '{team_name}'.")
            return True
        else:
            try:
                err_data = response.json()
                err_msg = err_data.get("error", "Unknown error")
                if err_msg == "API key is required":
                    print(f"Authentication failed: Invalid API key or team name")
                elif err_msg == "Invalid API key":
                    print(f"Authentication failed: The API key is invalid or doesn't match the team name")
                elif err_msg == "Team ID is required":
                    # This is fine for now, the Team ID is created on first login
                    print(f"Team ID will be assigned on first login")
                    return True
                else:
                    print(f"Authentication failed: {err_msg}")
            except:
                print(f"Authentication failed: Server returned status code {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"Network error during authentication: {e}")
        print(f"DEBUG INFO: API URL={API_BASE_URL}, Headers={headers}")
        return False


def load_teams_dict() -> Dict[str, str]:
    """
    Load the dictionary of team names and API keys from the token file.
    
    Returns:
        Dict[str, str]: Dictionary with team names as keys and API keys as values
    """
    teams_dict = {}
    
    if os.path.exists(TOKEN_FILE):
        try:
            import json
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                
                # Handle both legacy and new format
                if isinstance(data, dict):
                    if "teams" in data:
                        # New format with teams dictionary
                        teams_dict = data.get("teams", {})
                        print(f"DEBUG: Loaded teams from new format: {list(teams_dict.keys())}")
                    elif "team_name" in data and "api_key" in data:
                        # Legacy format - single team
                        team_name = data.get("team_name")
                        api_key = data.get("api_key")
                        if team_name and api_key:
                            teams_dict[team_name] = api_key
                            print(f"DEBUG: Loaded team from legacy format: {team_name}")
                    else:
                        print(f"WARNING: Token file has unexpected format: {data.keys()}")
        except Exception as e:
            print(f"Error reading token file: {e}")
    
    return teams_dict


def save_teams_dict(teams_dict: Dict[str, str]) -> None:
    """
    Save the dictionary of team names and API keys to the token file.
    
    Args:
        teams_dict: Dictionary with team names as keys and API keys as values
    """
    try:
        import json
        with open(TOKEN_FILE, "w") as f:
            json.dump({"teams": teams_dict}, f)
    except Exception as e:
        print(f"Warning: Could not save token file: {e}")


def get_auth_info() -> Tuple[Optional[str], Optional[str]]:
    """
    Retrieves the API key and team name from environment variables or token file.
    
    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the API key and team name,
        or (None, None) if not found.
    """
    # First try environment variables for current session
    api_key = os.getenv("AGENTDS_API_KEY")
    team_name = os.getenv("AGENTDS_TEAM_NAME")
    
    if api_key and team_name:
        print(f"DEBUG: Using credentials from environment variables for team '{team_name}'")
        return api_key, team_name
    
    # If not in environment, try the token file and use the first team
    teams_dict = load_teams_dict()
    if teams_dict:
        # Get the first team in the dictionary
        team_name = next(iter(teams_dict), None)
        if team_name:
            api_key = teams_dict[team_name]
            
            # Store in environment for this session
            os.environ["AGENTDS_API_KEY"] = api_key
            os.environ["AGENTDS_TEAM_NAME"] = team_name
            print(f"DEBUG: Loaded credentials from token file for team '{team_name}' and set as environment variables")
            return api_key, team_name
    
    # No valid auth info found
    print("DEBUG: No valid authentication information found")
    return None, None


def get_auth_headers() -> dict:
    """
    Returns the authentication headers for API requests.
    
    Returns:
        dict: Headers containing the API key and team name
    """
    api_key, team_name = get_auth_info()
    
    if not api_key or not team_name:
        print("No authentication information found. Please call authenticate() first.")
        return {}
    
    return {
        "X-API-Key": api_key,
        "X-Team-Name": team_name,
        "X-Team-ID": "placeholder"  # Add placeholder since Team ID is required by backend
    }


def list_teams() -> List[str]:
    """
    List all teams that the user has authenticated with.
    
    Returns:
        List[str]: List of team names
    """
    teams_dict = load_teams_dict()
    return list(teams_dict.keys())


def select_team(team_name: str) -> bool:
    """
    Select a team to use for subsequent API calls.
    
    Args:
        team_name: The name of the team to select
        
    Returns:
        bool: True if team was found and selected, False otherwise
    """
    teams_dict = load_teams_dict()
    
    if team_name in teams_dict:
        api_key = teams_dict[team_name]
        
        # Set as current team in environment variables
        os.environ["AGENTDS_API_KEY"] = api_key
        os.environ["AGENTDS_TEAM_NAME"] = team_name
        
        print(f"Selected team: {team_name}")
        return True
    else:
        print(f"Team '{team_name}' not found. Use authenticate() to add this team.")
        return False

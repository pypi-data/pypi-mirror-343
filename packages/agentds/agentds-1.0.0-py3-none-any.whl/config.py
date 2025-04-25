import os

# Check for environment variables to determine API URL
# Default to production URL if not specified
# API_BASE_URL = "https://api.agentds.org/api"
API_BASE_URL = "http://localhost:5202/api"  # Use port 5202
 
# Token file location in user's home directory
TOKEN_FILE = os.path.expanduser("~/.agentds_token")

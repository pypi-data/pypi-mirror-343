import requests
from requests.auth import HTTPBasicAuth

# Define HTTP success status code
HTTP_SUCCESS = 200

def fetch_jira_data(url, auth, params=None):
    """
    Fetch data from Jira REST API.
    
    Args:
        url (str): The Jira API endpoint URL
        auth: Authentication object (e.g., HTTPBasicAuth)
        params (dict, optional): Query parameters for the request
    
    Returns:
        dict: JSON response data if successful, None otherwise
    """
    response = requests.get(url, auth=auth, params=params)
    if response.status_code == HTTP_SUCCESS:
        return response.json()
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return None
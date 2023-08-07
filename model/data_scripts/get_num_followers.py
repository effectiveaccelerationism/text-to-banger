import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
print(bearer_token)

# Ensure the bearer token is provided
if not bearer_token:
    raise ValueError("Please set your BEARER_TOKEN as an environment variable.")

def get_followers_from_username(username):
    # Obtain user ID from username
    user_id = get_user_id_from_username(username)

    # Create URL to fetch followers
    url = f"https://api.twitter.com/2/users/{user_id}/following"

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
        
    return response.json()

def get_user_id_from_username(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
        
    user_data = response.json()
    return user_data['data']['id']

def main():
    username = "codethazine"
    json_response = get_followers_from_username(username)
    print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()

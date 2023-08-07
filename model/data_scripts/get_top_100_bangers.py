import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

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
    # Obtain user ID from username
    username = "codethazine"  # Replace with the desired username
    user_id = get_user_id_from_username(username)

    # Create URL to fetch tweets
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    
    # Get parameters
    params = {
        "tweet.fields": "created_at",
        "max_results": 100  # Get the last 100 tweets
    }
    
    # Set headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserTweetsPython"
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)
    
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
        
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()

import os
import csv
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
print(bearer_token)

# Ensure the bearer token is provided
if not bearer_token:
    raise ValueError("Please set your BEARER_TOKEN as an environment variable.")

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

def main():
    # Open the input CSV file for reading
    with open('data/raw/banger_accounts.csv', mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        usernames = [row[0] for row in reader]

    # Create a list to store follower data
    all_data = []

    for username in usernames:
        try:
            json_response = get_followers_from_username(username)
            all_data.append(json_response)
        except Exception as e:
            print(f"Error fetching data for {username}: {e}")

    # Write the data to the output CSV file
    with open('data/raw/banger_accounts_w_followers.csv', mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write header
        writer.writerow(['username', 'followers'])
        for data in all_data:
            user = data.get('data', {}).get('username', 'Unknown')
            followers = len(data.get('data', {}).get('followers', []))
            writer.writerow([user, followers])

if __name__ == "__main__":
    main()

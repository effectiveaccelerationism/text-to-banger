import requests
import os
import json
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

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

def get_last_100_tweets(user_id):
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
    
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
        
    return response.json()

def main():
    with open('data/banger_accounts.csv', 'r') as infile:
        reader = csv.reader(infile)
        # Assuming the first column contains usernames
        usernames = [row[0] for row in reader]

    tweets_data = []

    for username in usernames:
        user_id = get_user_id_from_username(username)
        tweets = get_last_100_tweets(user_id)
        
        # Extract required fields from the response (or modify as per requirement)
        for tweet in tweets.get('data', []):
            tweets_data.append([username, tweet['id'], tweet['text'], tweet['created_at']])

    # Writing the tweets to an output CSV
    with open('data/last_100_tweets_from_bangerers.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["username", "tweet_id", "tweet_text", "created_at"])  # CSV headers
        writer.writerows(tweets_data)

if __name__ == "__main__":
    main()

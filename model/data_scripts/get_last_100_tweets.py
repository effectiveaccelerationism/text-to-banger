import os
import csv
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

# Ensure the bearer token is provided
if not bearer_token:
    raise ValueError("Please set your BEARER_TOKEN as an environment variable.")

def handle_rate_limit(response):
    if response.status_code == 429:
        print("Rate limit exceeded. Waiting for 15 minutes + 1 second...")
        time.sleep(15 * 60 + 1)  # 15 minutes + 1 second
        return True
    return False

def get_user_id_from_username(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }
    response = requests.get(url, headers=headers)

    while handle_rate_limit(response):
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
        "tweet.fields": "created_at,public_metrics,attachments",  # Added 'attachments' to check for media attachments
        "exclude": "retweets,replies",  # Exclude retweets and replies
        "max_results": 100  # Get the last 100 tweets
    }
    
    # Set headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserTweetsPython"
    }
    response = requests.get(url, headers=headers, params=params)

    while handle_rate_limit(response):
        response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    return response.json()

def main():
    with open('data/banger_accounts_w_followers.csv', 'r') as infile:
        reader = csv.reader(infile)
        # Skip the first row as it contains the header
        next(reader)
        usernames = [row[0] for row in reader]

    tweets_data = []

    for username in usernames:
        print(f"Getting tweets for {username}")
        user_id = get_user_id_from_username(username)
        tweets = get_last_100_tweets(user_id)
        
        # Extract required fields from the response (or modify as per requirement)
        for tweet in tweets.get('data', []):
            # Skip tweets with attachments
            if "attachments" in tweet:
                continue

            like_count = tweet['public_metrics']['like_count']
            tweets_data.append([username, tweet['id'], tweet['text'], like_count, tweet['created_at']])

    # Writing the tweets to an output CSV
    with open('data/last_100_tweets_from_bangerers.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["username", "tweet_id", "tweet_text", "like_count", "created_at"])  # CSV headers
        writer.writerows(tweets_data)

if __name__ == "__main__":
    main()

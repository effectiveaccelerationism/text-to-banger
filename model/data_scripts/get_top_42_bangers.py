import os
import tweepy
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API credentials
consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_SECRET')

# Set up authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Read CSV file and extract usernames
usernames = []
with open('data/banger_accounts.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        usernames.append(row[0])  # Assuming the username is in the first column

# Get top 42 tweets for each username
for username in usernames:
    try:
        tweets = api.user_timeline(
            screen_name=username,
            count=42,
            tweet_mode='extended'  # To get the full text of tweets
        )
        print(f'Top 42 tweets for {username}:')
        for tweet in tweets:
            print(tweet.full_text)
    except Exception as e:
        print(f'Error retrieving tweets for {username}: {e}')

import tweepy
import csv
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))

# Create API object
api = tweepy.API(auth)

# Get the list of accounts you follow
following = []
for follow in tweepy.Cursor(api.friends).items():
    following.append(follow.screen_name)

# Save the accounts to a CSV file
with open('data/following.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username'])
    for follow in following:
        writer.writerow([follow])

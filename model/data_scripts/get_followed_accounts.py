import os
import json
import csv
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the bearer token from environment variables
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Create URL with your user ID
user_id = os.getenv("TWITTER_USER_ID")
url = f"https://api.twitter.com/2/users/{user_id}/following"

print(user_id)

# Set parameters
params = {"user.fields": "username"}

# Set headers
headers = {"Authorization": f"Bearer {bearer_token}", "User-Agent": "v2FollowingLookupPython"}

# Send request
response = requests.request("GET", url, headers=headers, params=params)

# Check response status
if response.status_code != 200:
    raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

# Parse response
json_response = response.json()

# Extract usernames
following = [user['username'] for user in json_response['data']]

# Save the accounts to a CSV file
with open('data/following.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username'])
    for user in following:
        writer.writerow([user])

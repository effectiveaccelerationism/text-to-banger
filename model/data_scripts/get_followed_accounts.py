import os
import json
import csv
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the bearer token and user ID from environment variables
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
user_id = os.getenv("TWITTER_USER_ID")

# Create URL with user ID
url = f"https://api.twitter.com/2/users/{user_id}/following"

# Set parameters and headers
params = {"user.fields": "username"}
# bearer_oauth = {"Authorization": f"Bearer {bearer_token}", "User-Agent": "v2FollowingLookupPython"}
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r

# Send request
response = requests.request("GET", url, auth=bearer_oauth, params=params)

print(response)

# Check response status
if response.status_code != 200:
    raise Exception(f"Request returned an error: {response.status_code} {response.text}")

# Parse response
json_response = response.json()

# Extract usernames and write to CSV
following = [user['username'] for user in json_response['data']]

# Save the accounts to a CSV file
with open('data/following.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username'])
    for user in following:
        writer.writerow([user])

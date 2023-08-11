import pandas as pd

# Load the tweets data
tweets_df = pd.read_csv('data/last_100_tweets_from_bangerers.csv')

# Load the accounts data
accounts_df = pd.read_csv('data/banger_accounts_w_followers.csv')

# Merge the two dataframes on the username or account column (change as appropriate)
merged_df = pd.merge(tweets_df, accounts_df, on='username', how='left')

# Filter out tweets with links, replies, and RTs
merged_df = merged_df[~merged_df['tweet_text'].str.contains('http://|https://|@|RT ', na=False)]

# Define a followers/likes ratio
RATIO = 10  # Example ratio
merged_df = merged_df[merged_df['followers'] / merged_df['like_count'] > RATIO]

# Save the filtered data back to a new CSV
merged_df.to_csv('data/filtered_tweets.csv', index=False)

print("Filtered tweets saved to 'data/filtered_tweets.csv'")

import os
import csv
import json
import openai
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Remember to put in your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_boring_versions(tweet):
    """Function that uses OpenAI's GPT-3 to generate boring versions of a given tweet."""
    boring_versions = []
    banger_opposites_prompts = ["Write an original tweet loosely related to the topic of the following tweet",
                                "Write a boring tweet related to the topic of the following tweet",
                                "Write a short tweet related to the topic of the following tweet"]
    
    try:
        for opposite_prompt in banger_opposites_prompts:
            # Make a call to the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant in charge of writing new tweets. " \
                                                  "You only reply through tweets."},
                    {"role": "user", "content": f"{opposite_prompt}: '{tweet}'"}
                ])
            
            # Get the boring version from the response
            boring_versions.append(response.choices[0].message.content)
    except Exception as e:
        print(e)
        print("Retrying this tweet...")
        return get_boring_versions(tweet)
        
    if len(boring_versions) == 0:
        boring_versions.append("")

    return boring_versions

def create_json(data):
    """Function to write the data into a json file."""
    with open('data/processed/bangers_w_boring_vers.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    # Will contain the original tweets as keys and the boring versions as values
    tweet_dict = {}

    # Open the csv file and read the tweets
    with open('data/processed/filtered_banger_tweets.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip the headers

        # Wrap the csv_reader with tqdm for a progress bar
        for row in tqdm(list(csv_reader), desc="Processing tweets"):
            # Assuming that the tweet is in the first column
            tweet = row[2]
            # Get the boring versions for the tweet
            boring_versions = get_boring_versions(tweet)
            # Add to the dict
            tweet_dict[tweet] = boring_versions

    # Create a json file with the dictionary
    create_json(tweet_dict)

if __name__ == '__main__':
    main()

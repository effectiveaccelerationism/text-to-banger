import re
import json

import re

def clean_tweet(tweet):
    # Remove hashtags
    tweet = re.sub(r'#\w+', '', tweet)
    
    # Remove weird characters like \ud83c \udf1f \u2728
    tweet = re.sub(r'[\u2000-\u3300]|[\ud83c\udc00-\udfff\ud83d\ude00-\udfff]', '', tweet)
    
    # Remove all emojis
    tweet = re.sub(r'[^\x00-\x7F]+', '', tweet)
    
    # Change \u2019 to '
    tweet = re.sub(r'\u2019', '\'', tweet)
    
    # Remove starting and ending whitespace
    tweet = tweet.strip()
    
    # Remove starting and ending single and double quotes
    tweet = re.sub(r'^\'|^\"|\'$|\"$', '', tweet)
    
    # Remove ending dots
    tweet = re.sub(r'\.$', '', tweet)
    
    return tweet

def transform_data(input_file, output_file):
    # Load the data from the given JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Prepare the transformed data
    transformed_data = []

    for banger_tweet, boring_versions in data.items():
        for boring_version in boring_versions:
            # Clean the boring version
            boring_version = clean_tweet(boring_version)

            # Create a dict for each pair and append to transformed_data
            transformed_data.append({
                "prompt": boring_version,
                "completion": re.sub(r'\.$', '', clean_tweet(banger_tweet)) # Remove ending dots for data consistency
            })

    # Write the transformed data to the output file in the desired format
    with open(output_file, 'w') as f:
        for item in transformed_data:
            f.write(json.dumps(item) + '\n')

if __name__ == '__main__':
    input_filepath = 'data/processed/bangers_w_boring_vers.json'
    output_filepath = 'data/final/bangers_finetuning_data.json'
    transform_data(input_filepath, output_filepath)

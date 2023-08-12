import re
import json

def clean_boring_tweet(tweet):
    # Remove the hashtags using re
    tweet = re.sub(r'#\w+', '', tweet)

    # Remove starting and ending single and double quotes
    tweet = re.sub(r'^\'|^\"|\'$|\"$', '', tweet)

    # Remove starting and ending whitespace
    tweet = tweet.strip()

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
            boring_version = clean_boring_tweet(boring_version)

            # Create a dict for each pair and append to transformed_data
            transformed_data.append({
                "prompt": boring_version,
                "completion": re.sub(r'\.$', '', banger_tweet) # Remove ending dots for data consistency
            })

    # Write the transformed data to the output file in the desired format
    with open(output_file, 'w') as f:
        for item in transformed_data:
            f.write(json.dumps(item) + '\n')

if __name__ == '__main__':
    input_filepath = 'data/bangers_w_boring_vers.json'
    output_filepath = 'data/bangers_finetuning_data.json'
    transform_data(input_filepath, output_filepath)

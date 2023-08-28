import re
import json

import re

def clean_tweet(tweet):
    # Remove hashtags
    tweet = re.sub(r'#\w+', '', tweet)

    # Remove all emojis
    tweet = re.sub(r'[^\x00-\x7F]+', '', tweet)

    # Change \u2019 to '
    tweet = re.sub(r'\u2019', '\'', tweet)

    # Remove and replace with "" all the starting and ending single and double quotes, 
    # even when they are nested or preceded by spaces or other characters
    tweet = re.sub(r'^[\s\'\"]+|[\s\'\"]+$', '', tweet)

    # Remove all the starting and ending spaces
    tweet = re.sub(r'^\s+|\s+$', '', tweet)

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
            if boring_version != banger_tweet and boring_version != '' and banger_tweet != '':
                transformed_data.append({
                    "prompt": boring_version,
                    "completion": re.sub(r'\.$', '', clean_tweet(banger_tweet)) # Remove ending dots for data consistency
                })

    # Remove duplicates
    transformed_data = list({v['prompt']:v for v in transformed_data}.values())

    # Write the transformed data to the output file in the desired format
    with open(output_file, 'w') as f:
        for item in transformed_data:
            f.write(json.dumps(item) + '\n')

    # Write a JSONL version of the transformed data for the fine-tuning job
    finetuning_data = []

    # Set \n\n###\n\n common separator at the end of prompt key
    for item in transformed_data:
        item['prompt'] += '\n\n###\n\n'
        # Set space at the beginning of completion key and " END" at the end
        item['completion'] = ' ' + item['completion'] + ' END'
        finetuning_data.append(item)

    with open(output_file.replace('.json', '_prepared.jsonl'), 'w') as f:
        for item in finetuning_data:
            f.write(json.dumps(item) + '\n')

if __name__ == '__main__':
    input_filepath = 'data/processed/bangers_w_boring_vers.json'
    output_filepath = 'data/final/bangers_finetuning_data.json'
    transform_data(input_filepath, output_filepath)

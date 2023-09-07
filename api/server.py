import os
import re
import json
import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
hostName = "0.0.0.0"
server_port = int(os.environ.get('PORT', 8080))

app = Flask(__name__)
CORS(app)

@app.route('/generate-banger', methods=['POST', 'GET'])
def generate_banger():
    data = request.json
    original_text = data.get('originalText')

    banger_tweet = create_banger(original_text)

    if banger_tweet:
        return jsonify(banger_tweet), 200
    else:
        return jsonify("Error generating banger tweet."), 500

def create_banger(tweet_text):
    print(f"Generating banger for tweet: '{tweet_text}'")

    # For OAI chat-based finetuned models, e.g. gpt-3.5-turbo 
    if ":" in model_name and "gpt-3.5-turbo" in model_name: 
        prompt = "You are a bot instructed to to turn this tweet into a solid banger, where a banger is a tweet of shocking " \
                 "and mildly psychotic comedic value, that's prone to go viral. Reply only with the banger."
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": tweet_text}
            ],
            max_tokens=100,
            temperature=0.7
        )
        banger_tweet = response.choices[0]["message"]["content"].strip()
    
    # For OAI legacy finetuned models, e.g. curie
    elif ":" in model_name and "gpt-3.5-turbo" not in model_name:
        prompt = f"{tweet_text}\n\n###\n\n"
        response = openai.Completion.create(
            model=model_name,
            prompt=prompt,
            max_tokens=100,
            temperature=1,
            stop=["END"]
        )
        banger_tweet = response.choices[0].text.strip()
        banger_tweet = re.sub(r'END', '', banger_tweet)
    
    # For OAI base models, e.g. davinci, gpt-4 (honestly, not recommended and boring)
    else:
        prompt = f"Turn this tweet into a solid banger, where a banger is a tweet of shocking and mildly psychotic comedic value, that's prone to go viral: '{tweet_text}'"
        response = openai.Completion.create(
            model=model_name,  # You can choose a different engine based on your subscription
            prompt=prompt,
            max_tokens=100, 
            temperature=0.7 # Adjust the temperature for more randomness (0.2 to 1.0)
        )
        banger_tweet = response.choices[0].text.strip()

    # Remove hashtags
    banger_tweet = re.sub(r'#\S+', '', banger_tweet)  # Remove hashtags

    # Remove emojis
    # banger_tweet = banger_tweet.encode('ascii', 'ignore').decode('ascii')

    # Remove starting and ending single and double quotes
    banger_tweet = re.sub(r'^"|"$|^\'|\'$', '', banger_tweet)

    # Remove dot at the end if they exists
    banger_tweet = re.sub(r'\.$', '', banger_tweet.strip())

    if not banger_tweet:
        return None

    print(f"Generated banger: '{banger_tweet}'")
    return banger_tweet

if __name__ == '__main__':
    app.run(host=hostName, port=server_port)

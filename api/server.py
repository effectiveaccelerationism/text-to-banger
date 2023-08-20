
import re
import openai
import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app


def generate_banger(tweet_text):
    print(f"Generating banger for tweet: '{tweet_text}'")
    prompt = f"Turn this tweet into a solid banger, where a banger is a tweet of shocking and mildly psychotic comedic value, that's prone to go viral: '{tweet_text}'"
    response = openai.Completion.create(
        # You can choose a different engine based on your subscription
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        # Adjust the temperature for more randomness (0.2 to 1.0)
        temperature=0.7,
    )
    banger_tweet = response.choices[0].text.strip()

    # Remove hashtags
    banger_tweet = re.sub(r'#\S+', '', banger_tweet)

    # Remove starting and ending single and double quotes
    banger_tweet = re.sub(r'^"|"$|^\'|\'$', '', banger_tweet)

    # Remove dot at the end if it exists
    banger_tweet = re.sub(r'\.$', '', banger_tweet.strip())

    if not banger_tweet:
        return None

    print(f"Generated banger: '{banger_tweet}'")
    return banger_tweet


@app.route('/generate-banger', methods=['POST'])
def generate_banger_route():

    try:
        if request.content_type == 'application/json':
            data = request.get_json()
            originalText = data['originalText']
        else:
            originalText = request.form.get('originalText')
        # data = request.get_json()
        # originalText = data['originalText']
        banger_tweet = generate_banger(originalText)

        if banger_tweet:
            response = jsonify({"bangerTweet": banger_tweet})
        else:
            response = jsonify({"error": "Error generating banger tweet."})

        # Add minimal CORS headers
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8081)))

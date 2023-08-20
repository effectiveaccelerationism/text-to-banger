# import re
# import openai
# import json
# import os
# from dotenv import load_dotenv
# from http.server import BaseHTTPRequestHandler, HTTPServer

# # Load environment variables
# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# model_name = os.getenv("OPENAI_MODEL_NAME")
# openai.api_key = api_key
# hostName = "localhost"
# serverPort = 8080


# def generate_banger(tweet_text):
#     print(f"Generating banger for tweet: '{tweet_text}'")
#     if ":" in model_name:  # For finetuned models
#         prompt = f"{tweet_text}\n\n###\n\n"
#         response = openai.Completion.create(
#             model=model_name,  # You can choose a different engine based on your subscription
#             prompt=prompt,
#             max_tokens=100,
#             # Adjust the temperature for more randomness (0.2 to 1.0)
#             temperature=1,
#             stop=["END"]
#         )
#         banger_tweet = response.choices[0].text.strip()
#         banger_tweet = re.sub(r'END', '', banger_tweet)
#     else:
#         prompt = f"Turn this tweet into a solid banger, where a banger is a tweet of shocking and mildly psychotic comedic value, that's prone to go viral: '{tweet_text}'"
#         response = openai.Completion.create(
#             model=model_name,  # You can choose a different engine based on your subscription
#             prompt=prompt,
#             max_tokens=100,
#             # Adjust the temperature for more randomness (0.2 to 1.0)
#             temperature=0.7,
#         )
#         banger_tweet = response.choices[0].text.strip()

#     # Remove hashtags
#     banger_tweet = re.sub(r'#\S+', '', banger_tweet)  # Remove hashtags

#     # Remove emojis
#     # banger_tweet = banger_tweet.encode('ascii', 'ignore').decode('ascii')

#     # Remove starting and ending single and double quotes
#     banger_tweet = re.sub(r'^"|"$|^\'|\'$', '', banger_tweet)

#     # Remove dot at the end if they exists
#     banger_tweet = re.sub(r'\.$', '', banger_tweet.strip())

#     if not banger_tweet:
#         return None

#     print(f"Generated banger: '{banger_tweet}'")
#     return banger_tweet


# class MyServer(BaseHTTPRequestHandler):
#     def do_OPTIONS(self):
#         self.send_response(200, "ok")
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
#         self.send_header("Access-Control-Allow-Headers",
#                          "X-Requested-With, Content-type")
#         self.end_headers()
#         return

#     def do_POST(self):
#         url = self.path
#         if (url == '/generate-banger'):
#             content_length = int(self.headers['Content-Length'])
#             post_data = self.rfile.read(content_length)
#             post_data = post_data.decode('utf-8')
#             parsedData = json.loads(post_data)
#             originalText = parsedData['originalText']
#             banger_tweet = generate_banger(originalText)

#             if banger_tweet:
#                 self.send_response(200)
#             else:
#                 self.send_response(500)
#                 banger_tweet = "Error generating banger tweet."

#             self.send_header("Content-type", "text/html")
#             self.send_header('Access-Control-Allow-Origin', '*')
#             self.end_headers()
#             self.wfile.write(bytes(banger_tweet, "utf-8"))
#         else:
#             self.send_response(404)
#             self.send_header("Content-type", "text/html")
#             self.send_header('Access-Control-Allow-Origin', '*')
#             self.end_headers()
#             self.wfile.write(bytes('null', "utf-8"))


# 3
# if __name__ == "__main__":
#     webServer = HTTPServer((hostName, int(serverPort)), MyServer)
#     print("Server started http://%s:%s" % (hostName, serverPort))

#     try:
#         webServer.serve_forever()
#     except KeyboardInterrupt:
#         pass

#     webServer.server_close()
#     print("Server stopped.")


import re
import openai
import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
openai.api_key = api_key

app = Flask(__name__)
# Enable CORS for the entire app with credentials support
CORS(app, resources={r"/generate-banger": {"origins": "*"}},
     supports_credentials=True)


def generate_banger(tweet_text):
    print(f"Generating banger for tweet: '{tweet_text}'")
    if ":" in model_name:
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
    else:
        prompt = f"Turn this tweet into a solid banger, where a banger is a tweet of shocking and mildly psychotic comedic value, that's prone to go viral: '{tweet_text}'"
        response = openai.Completion.create(
            model=model_name,
            prompt=prompt,
            max_tokens=100,
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


# Allow OPTIONS requests
@app.route('/generate-banger', methods=['POST', 'OPTIONS'])
def generate_banger_endpoint():
    try:
        data = request.get_json()
        original_text = data['originalText']
        banger_tweet = generate_banger(original_text)

        if banger_tweet:
            response = jsonify({"bangerTweet": banger_tweet})
        else:
            response = jsonify({"error": "Error generating banger tweet."})

        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8081)))

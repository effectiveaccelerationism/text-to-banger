from http.server import BaseHTTPRequestHandler, HTTPServer
import openai, json, os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
hostName = "localhost"
serverPort = 8080

def generate_banger(tweet_text, settings = None, retry = True):
    print(f"Generating banger for tweet: '{tweet_text}'")
    prompt = f"Turn this tweet into a solid banger with no hashtags, where a banger is a tweet of higher quality compared to most others, usually in comedic value and wording: '{tweet_text}'"
    if settings: prompt += get_settings_string(settings)
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose a different engine based on your subscription
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,  # Adjust the temperature for more randomness (0.2 to 1.0)
    )
    banger_tweet = response.choices[0].text.strip()
    if not validate_settings_compliance(settings, banger_tweet) and retry:
        banger_tweet = generate_banger(tweet_text, settings, False)
    print(f"Generated banger: '{banger_tweet}'")
    return banger_tweet

def get_settings_string(settings):
    if not settings: return ''
    if not any(settings.values()): return ''
    ret = '\nThe response must follow the following rules:'
    if settings['suppressHashtags']:
        ret += "\nDo not include hashtags in the response."
    if settings['suppressEmojis']:
        ret += "\nDo not include emojis in the response."
    return ret

def validate_settings_compliance(settings, banger_tweet):
    if not settings: return True
    if not any(settings.values()): return True
    if settings['suppressHashtags'] and '#' in banger_tweet: return False
    if settings['suppressEmojis']:
        emojiRegex = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emojiRegex.search(banger_tweet): return False
    return True

class MyServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()
        return
    def do_POST(self):
        url = self.path
        if(url == '/generate-banger'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            parsedData = json.loads(post_data)
            originalText = parsedData['originalText']
            settings = parsedData['settings']
            banger_tweet = generate_banger(originalText, settings)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes(banger_tweet, "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes('null', "utf-8"))
3
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, int(serverPort)), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
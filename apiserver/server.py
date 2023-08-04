from http.server import BaseHTTPRequestHandler, HTTPServer
import openai, json, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
hostName = "localhost"
serverPort = 8080

def generate_banger(tweet_text):
    print(f"Generating banger for tweet: '{tweet_text}'")
    prompt = f"Turn this tweet into a solid banger, where a banger is a banger is a tweet of higher quality compared to most others, usually in comedic value and wording: '{tweet_text}'"
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose a different engine based on your subscription
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,  # Adjust the temperature for more randomness (0.2 to 1.0)
    )
    banger_tweet = response.choices[0].text.strip()
    print(f"Generated banger: '{banger_tweet}'")
    return banger_tweet

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
        if(url == '/generateBanger'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            parsedData = json.loads(post_data)
            originalText = parsedData['originalText']
            banger_tweet = generate_banger(originalText)
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
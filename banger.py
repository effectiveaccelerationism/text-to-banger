import openai

# Set your OpenAI GPT-3 API key here
api_key = 'YOUR_API_KEY'
openai.api_key = api_key

def generate_banger():
    tweet_text = input("Enter the tweet you want to turn into a banger: ")   # Added Input
    prompt = f"Turn this tweet into a solid banger, where a banger is a tweet of higher quality compared to most others, usually in comedic value and wording: '{tweet_text}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7, 
    )
    banger_tweet = response.choices[0].text.strip()
    return banger_tweet

if __name__ == "__main__":
    banger_tweet = generate_banger()
    print("Banger tweet:", banger_tweet)

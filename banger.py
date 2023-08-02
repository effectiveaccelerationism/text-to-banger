import openai

# Set your OpenAI GPT-3 API key here
api_key = 'YOUR_API_KEY'
openai.api_key = api_key

def generate_banger(tweet_text):
    prompt = f"Turn this tweet into a solid banger, where a banger is a banger is a tweet of higher quality compared to most others, usually in comedic value and wording: '{tweet_text}'"
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose a different engine based on your subscription
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,  # Adjust the temperature for more randomness (0.2 to 1.0)
    )
    banger_tweet = response.choices[0].text.strip()
    return banger_tweet

if __name__ == "__main__":
    tweet_text = "I am having a good time. Thanks for the tweet!"
    banger_tweet = generate_banger(tweet_text)
    print("Original tweet:", tweet_text)
    print("Banger tweet:", banger_tweet)

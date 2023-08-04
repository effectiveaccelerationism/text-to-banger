const express = require('express');
const bodyParser = require('body-parser');
require('dotenv').config({ path: '/Users/finn/Desktop/APPS/TTB/text-to-banger/server/.env' });
console.log(process.env.OPENAI_API_KEY); // Prints the API key
const { Configuration, OpenAIApi } = require('openai');

const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

app.post('/api/generate-tweet', async (req, res) => {
  const tweetIdea = req.body.tweetIdea;
  console.log('Received tweet idea:', tweetIdea);
  try {
    const response = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'Turn this tweet into a solid banger, where a banger is a tweet of higher quality compared to most others, usually in comedic value and wording. Do not use hashtags.',
        },
        {
          role: 'user',
          content: `Write a tweet about ${tweetIdea}.`,
        },
      ],
      temperature: 0.8,
      max_tokens: 256,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
    });
    console.log('OpenAI response:', JSON.stringify(response.data, null, 2));

    if (response.data && response.data.choices && response.data.choices.length > 0) {
      const generatedTweet = response.data.choices[0].message.content;
      console.log('Sending generated tweet:', generatedTweet);
      res.json({ generatedTweet });
    } else {
      res.status(400).json({ error: 'No valid response data.' });
    }
  } catch (error) {
    console.error('Error generating the tweet:', error.message); // Only log the error message
    res.status(500).json({ error: 'An error occurred while generating the tweet.' });
  }
});

app.listen(3001, () => {
  console.log('Server running on port 3001');
});

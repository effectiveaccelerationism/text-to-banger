# Text-to-banger

A simple API converting a user's proposed tweet into a veritable banger.

## To run the app locally

### Clone the repo

```
gh repo clone effectiveaccelerationism/text-to-banger
```

### Install and run the app

```
npm install
npm run dev
```

The app will be running on http://localhost:3000

### Run the OpenAI api server

Currently the app runs with an OpenAI API server, soon to be dismissed in favor of a custom finetuned model. To run the OpenAI API server, you need to have an OpenAI API key. You can get one [here](https://platform.openai.com/account/api-keys). Once you have your API key, rename the file named `.env.example` to `.env` and add your API key to the file like so:

```
OPENAI_API_KEY=your-openai-key
```
## Model TODOs

- [x] Get down a list of banger accounts
- [x] Script getting the last 100 text tweets from the account in the banger accounts list
- [x] Script filtering the tweets by a set likes/followers ratio 
- [x] Script augmenting data rewriting the bangers in 10 boring ways through the OAI API
- [ ] Fine-tuning script taking as input the boring bangers and outputting the bangers

## API TODOs

- [x] Create OAI API server
- [ ] Add Custom API server with finetuned model

## WebApp TODOs

- [x] Add dark mode and set it as default
- [ ] Get BANGER OAI API prompt
- [ ] Deploy webapp

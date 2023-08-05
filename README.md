# Text-to-banger
A simple API converting a user's proposed tweet into a veritable banger.

## To run the app locally
### Clone the repo

```
gh repo clone effectiveaccelerationism/text-to-banger
```

### Install and run the app
```
cd webapp
npm install
npm start
```
The app will be running on http://localhost:3000

### Run the OpenAI api server
Currently the app runs with an OpenAI API server, soon to be dismissed in favor of a custom finetuned model. To run the OpenAI API server, you need to have an OpenAI API key. You can get one [here](https://platform.openai.com/account/api-keys). Once you have your API key, create a file named `.env` in the `apiserver` directory and add the following line to it:
```
OPENAI_API_KEY=your-openai-key
```
Then, run the server with
```
cd api
python -m venv env
pip install -r requirements.txt
source env/bin/activate # on Windows use `env\Scripts\activate`
python server.py
```

NOTE: You must have both the webapp and the apiserver running in two separate terminal instances to use the app.

## Model TODOs
- [ ] Script getting the account the user is following
- [ ] Script getting the top 100 tweets from the account the user is following
- [ ] Script augmenting data rewriting the bangers in 10 boring ways through the OAI API
- [ ] Fine-tuning script taking as input the boring bangers and outputting the bangers

## API TODOs
- [x] Create OAI API server
- [ ] Add Custom API server with finetuned model

## WebApp TODOs
- [x] Add dark mode and set it as default
- [ ] Get BANGER OAI API prompt
- [ ] Deploy webapp

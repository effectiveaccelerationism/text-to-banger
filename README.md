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

### Start the server
```
node server/api.js

## TODOs
- [X] Local API server taking as input the user's proposed tweet and outputting the banger
- [ ] Script getting the account the user is following
- [ ] Script getting the top 100 tweets from the account the user is following
- [ ] Script augmenting data rewriting the bangers in 10 boring ways through the OAI API
- [ ] Fine-tuning script taking as input the boring bangers and outputting the bangers

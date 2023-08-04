import React, { useState } from 'react';
import axios from 'axios';
// import logo from './TTB.png';
import './App.css';

function App() {
  const [tweetIdea, setTweetIdea] = useState('');
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleTweetIdeaChange = (e) => {
    setTweetIdea(e.target.value);
  }

  const handleGenerateTweet = () => {
    const suppressHashtags = document.getElementById('suppress-hashtags').checked;
    const suppressEmojis = document.getElementById('suppress-emojis').checked;

    setIsLoading(true);
    setGeneratedTweet(null);
    // Send the tweet idea to the server to generate a tweet
    axios.post('http://localhost:8080/generate-banger', {
      originalText: tweetIdea,
      settings: {
        'suppressHashtags': suppressHashtags,
        'suppressEmojis': suppressEmojis
      }
    })
    .then(response => {
      if (response.status !== 200) {
        throw new Error(`Request failed with status code ${response.status}`);
      }
      return response.data;
    })
    .then(data => {
      setGeneratedTweet(data);
      setIsLoading(false);
    })
    .catch(error => {
      console.error('An error occurred:', error);
      setIsLoading(false);
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="logo-container">
          {/* <img src={logo} className="App-logo" alt="logo" /> */}
          <h1 className="text-logo">text-to-banger</h1>
        </div>
        <div className="content-container"> {/* This new div wraps both the form and the generated tweet container */}
          <div className="tweet-form">
            <textarea
              id="tweetIdea"
              value={tweetIdea}
              onChange={handleTweetIdeaChange}
              placeholder="What's happening?"
              rows="4"
            />
            <button className="tweet-button" onClick={handleGenerateTweet} disabled={isLoading}>Generate Banger Tweet</button>
            <div id='tweet-settings-container'>
              <div>
                <input type='checkbox' id='suppress-hashtags' name='suppress-hashtags' />
                <label htmlFor='suppress-hashtags'>Suppress Hashtags</label>
              </div>
              <div>
                <input type='checkbox' id='suppress-emojis' name='suppress-emojis' />
                <label htmlFor='suppress-emojis'>Suppress Emojis</label>
              </div>
            </div>
          </div>
          {isLoading && <p>generating a banger...</p>}
          <div className="generated-tweet-container">
            {generatedTweet && (
              <>
                <p>{generatedTweet}</p>
                <a
                  className="tweet-button"
                  href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(generatedTweet)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Post Banger Tweet
                </a>
              </>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;

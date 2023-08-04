import React, { useState } from 'react';
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
    setIsLoading(true);
    // Send the tweet idea to the server to generate a tweet
    fetch('https://localhost:8080/generate-banger', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tweetIdea })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`An error occurred: ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      setGeneratedTweet(data.generatedTweet);
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
